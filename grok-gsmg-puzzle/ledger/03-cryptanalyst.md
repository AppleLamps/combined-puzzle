# 03 — Cryptanalyst: decodes as code, small batteries

**Agent:** CRYPTANALYST  
**Run:** `python3 team/cryptanalyst_tests.py` → **18/18 checks PASS**, **108 decrypts**, **0 structured container hits**, **0 uncomp hash160 wins**  
**Artifact:** `artifacts/cryptanalyst_summary.json`  
**Convention:** §4.1 — `password = sha256(answer).hexdigest()` (64 lowercase hex ASCII), EVP_BytesToKey md=SHA-256 ×1, AES-256-CBC, PKCS#7.  
**Win test:** uncompressed pubkey hash160 `a9553269572a317e39f0f518cb87c1a0ee1dbae4` only.

Hard limits: offline only; no gsmg.io submission.

---

## Proposed decodes (code)

These are the primitives Tester should treat as **named operands**, not re-derive ad hoc.

### §6.2 page integer (`ai_decimal_hex`)

```python
def ai_decimal_hex(s: str) -> bytes:
    n = int("".join("0" if c == "o" else str(ord(c) - 96) for c in s))
    h = format(n, "x")
    if len(h) % 2:
        h = "0" + h
    return bytes.fromhex(h)
```

### §6.2 a/b binary runs (`ab_bits`)

```python
def ab_bits(s: str) -> bytes:
    return bytes(int(s[i:i+8].replace("a","0").replace("b","1"), 2) for i in range(0, len(s), 8))
```

### §6.3 Bifid (period 570, square `dbifhcegaklmnopqrstuvwxyz`)

```python
def bifid_decrypt(ct, square, period): ...  # see team/cryptanalyst_tests.py
```

**[V] reproduced:** plaintext starts `btcseedd`, sha256 `15d62c8228c1a30f3f6280fcdce2251fe616135e9de291b0c7b8a792dd8d0507`.  
**Calibration:** 8 of 362 880 nine-letter square prefixes yield `btcseed`; all eight agree on output indices `0..7` (`btcseedd`), **diverge at index 8** (`b` vs `e` vs `d`…).

### faed whole-block decimal (not ASCII)

```python
digits = [ord(c)-96 for c in faed]  # a=1..i=9, g=7
whole = int("".join(map(str, digits))).to_bytes(237, "big")
```

**[V] reproduced:** head `1bd5951d`, tail `c7bbc075`, only **78/237** printable — interior is not prose.

### mask6 **zero** vs **delete** (positions 1-based `{1,3,551,557,561,563}`)

| transform | bytes | ends | interior printable |
|---|---:|---|---|
| zero digits at mask6 | 236 | `yM` / `szqu` | 84/230 (chance ASCII) |
| **delete** those six letters | 234 | pins **lost** (`p\x1b` / `\xc63\x04u`) | 81/234 |

Deletion null matches lead log: one-shot, not a path to printable whole-block text.

### Beaufort on Bifid plaintext (key `btcseed`)

Reciprocal Beaufort on the 570-letter Bifid output (same rule as phase 3.2 symbols, on `a-z`):

```python
def beaufort_reciprocal(cipher, key):  # P = (K - C) mod 26
```

### §7.1 message #8446

```python
bits = "".join(groups)  # 161×8 from appendix
text = bytes(int(bits[::-1][i:i+8], 2) for i in range(0, len(bits), 8)).decode()
# → yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyangwewont...
```

### New Year dots (#53335–#53342)

- Dot-only messages → literal `.`, `..`, …, `.....` and count string `12345`.
- #53342 → standard 8-bit ASCII (not bit-reversed): `Happy new year! … tiny hint …`.

### Recipe operands (three locked containers)

From page layout + #8446 hint string:

| operand | construction |
|---|---|
| `matrixsumlist` | `ab_bits(sal[91:195])` |
| `enter` | `ab_bits(sal[959:999])` |
| `lastwords` | `ai_decimal_hex(sal[766:829])` → ASCII |
| `thispassword` | `ai_decimal_hex(sal[830:859])` |
| `tok23` | yellow/blue walk token string (step3) |
| `msl-row` / `msl-col` | poster 14×14 bit grid row/column sums |
| `8446` | full #8446 decoded string |
| `sha256hex(flower)` | creator #225 control `5ac40783…` |

---

## Batteries run (this pass)

| hypothesis | exact candidate construction | containers | convention | candidates | decrypts | valid pads vs ~decrypts/256 | planted control | detector | result |
|---|---|---|---|---:|---:|---|---|---|---|
| Beaufort(Bifid, key=btcseed) + bifid tail | `beaufort_reciprocal(pt,"btcseed")`, `pt`, `pt[7:]`, each ± `sha256hex` | terminal, sal_short, cosmic | §4.1 std-hex | 5 | 15 | 0 structured; ~0.06 expected 1-byte pads | phase2 `causality` decrypt | structured prose / uncomp h160 | **null** |
| fillers decimal→hex | `ai_decimal_hex(60 fillers)` → hex string / sha256hex | 3 | §4.1 | 4 | 12 | 0 | #225 flower hash | structured / h160 | **null** (25 B `4f2672e2…`) |
| #8446 as password | full 161-char string + sha256hex + fragments | 3 | §4.1 | 4 | 12 | 0 | #225 | structured / h160 | **null** |
| dots binary | dot literals, `12345`, #53342 greeting ± sha256hex | 3 | §4.1 | 8 | 14 | 0 | #225 | structured | **null** |
| recipe operands | 9 singles + 5 chains (incl. retracted long concat) | 3 | §4.1 | 14 | 42 | 0 | #225 | structured | **null** |
| scalar from fillers / Beaufort | `sha256(beaufort)`, raw 25 B fillers | — | n/a | 3 | 0 decrypt | — | privkey 1 not prize | uncomp `a9553269…` | **null** |

**Totals:** 108 decrypts, **0** structured hits, **0** wins. Planted §4.1 control **PASS** (phase 2).

---

## Confirmed negatives (do not re-litigate without new operand)

1. **faed integer** — not ASCII; mask6 zero pins ends only; interior remains non-text.  
2. **mask6 deletion** — 234 B, **loses** `yM`/`szqu`; no container/key signal in this script.  
3. **Bifid** — `btcseed` prefix is real but **8 squares** diverge immediately after `btcseedd`; Beaufort layer does not yield a container password at this size.  
4. **fillers** alone — 25-byte binary blob; not a §4.1 password at tested forms.  
5. **#8446 / dots / recipe singles** — no structured plaintext under §4.1 std-hex on three containers.

---

## What Tester should batch next

Scale only where Cryptanalyst named an **operand** or an **untested composition**; keep §4.1 + planted phase2 control on every run.

| priority | batch | why | scale hint |
|:---:|---|---|---|
| P0 | **deletion** variants on faed / fillers / dbbi | handoff §8: deletion not exhausted; mask6 null is only 6 positions | all 2^6 delete masks on faed → int bytes; top printable scores → §4.1 |
| P0 | **Beaufort** keys beyond `btcseed` | cipher family already validated on phase 3.2 | keys: `THEMATRIXHASYOU`, `btcseedd`, `matrixsumlist`, sha256hex(bifid), on even/odd bifid channels |
| P1 | **8 Bifid squares** — full plaintexts | diverge after index 8; tail may encode differently per square | 8× (password = sha256hex(plaintext), tail, even stream) × 3 containers × {std-hex, md5} |
| P1 | **fillers** × **mask6** / tail `szqu` | operands never crossed with pinned integer | `sha256hex(fillers_hex + mask6_text)`, XOR with `4f2672e2…`, base-9 24 B from step1 |
| P1 | **recipe** full grid | step3 ran yellow-blue × matrix × lastwords; not all §7.1 chains | `tok23` × `msl-{row,col,diag}` × `{lastwords,thispassword,8446}` × seps × {plain, sha256hex, double} × 3 containers |
| P2 | **dots** as **bits** | only literals tried here | map 1..5 dots to 3-bit patterns; prepend to #53342 message; New Year + `tiny hint` as passphrase to cosmic only |
| P2 | **matrixsumlist(lastwords)** | operation inputs still missing | use Architect speech windows, phase32 Beaufort text, checkerboard 149 digits as list inputs before `enter` |

**Do not batch** without new evidence: whole-block zero on **only** `g`/`e` (closed §6.3); raw PKCS#7 pad without structured detector; compressed-only hash160 match.

---

## Code map

- `team/cryptanalyst_tests.py` — this ledger’s executable spec  
- Reuses: `src/crypto_known.py`, `src/step1_btcseed.load_containers`, `src/step3_mask` operands
