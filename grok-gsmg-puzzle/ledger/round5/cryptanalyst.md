# 11 — Cryptanalyst brainstorm: five container-lock **mechanisms**

**Agent:** CRYPTANALYST (brainstorm + pre-registration only; battery not executed in this pass)  
**Code (skeleton):** `team/round5_preregistered.py` → `artifacts/round5_preregistered.json` (when run)  
**Hard limits:** offline; no `gsmg.io`; win = uncomp hash160 `a9553269572a317e39f0f518cb87c1a0ee1dbae4` only.  
**Planted control (every battery):** phase-2 `causality` decrypt under that mechanism’s stated KDF must **PASS** before any null is recorded.

These are **mechanisms** (how ciphertext relates to prior artifacts), not new password guesses. Each block lists one falsifiable battery capped at **≤10 000 decrypts** (or scalar-only where noted).

---

## Why containers stay locked under one global §4.1 recipe

Rounds 2–4 exhausted **one password string → sha256hex → EVP-SHA256 → try same three blobs**. Null there is consistent with any of the five mechanisms below: the failure mode is **wrong stage graph**, not necessarily wrong English.

---

## M1 — Per-Container KDF Profile

**Claim:** Solved phases share §4.1, but **Terminal**, **SalPhaseIon-short**, and **Cosmic** were sealed with **different EVP digest / password encoding** (community Sal-short MD5 is one leg of this, not the whole puzzle).

| Field | Specification |
|--------|----------------|
| **Construction** | Operand set **O** = 12 fixed strings from `ledger/08-round2.md` recipe table (`tok23`, `msl-sum-bits`, `lw-arch-tail40`, `8446` head, `FLOWER` hash, community retracted literal, spiral `list_row_sums`, `spiral-list-rowsums-sep`, `sha256hex(flower)`, `recipe-8446-order`, `msl-row`, `msl-col`). For each `o ∈ O`, password bytes **P** ∈ {`utf8(o)`, `sha256(o).hex()`, `sha256(o).digest()`, `md5(o).hex()`, `sha256(sha256(o).hex())`}. KDF **K** ∈ {`EVP-SHA256`, `EVP-MD5`}. Decrypt **only the named container** for each profile row in the table below (do not cross-apply). |
| **Profile table** | `terminal` → (P=`sha256hex`, K=`SHA256`); `salphaseion_short` → (P=`plain`, K=`MD5`); `cosmic` → (P=`raw32`, K=`SHA256`); plus **cross-check rows** that deliberately mismatch (same P,K on wrong container). |
| **Decrypt budget** | \|O\|×\|P\|×\|K\| = 12×5×2 = **120** primary tries + 120 cross-check = **240** (≪10k). |
| **Detector** | `structured` plaintext (≥8 B, ≥90% printable, ≥4 letters) **or** nested `Salted__` / PEM / JSON magic; **not** 1-byte PKCS#7 alone. |
| **Signal if true** | ≥1 **structured** hit on the **assigned** (container, P, K) cell; **zero** structured hits on deliberately mismatched cells for the same `o`. Sal-short MD5 **plain** community string may reproduce known **79 B pad** (calibration, not a win). |
| **Null if false** | 0 structured across all 240; valid 1-byte pads ≈ **240/256 ≈ 0.94** total (binomial; no cell with structured). |
| **Control** | `causality` with (`sha256hex`, `SHA256`) on phase-2 blob **PASS**. |

---

## M2 — Cosmic Yin-Yang Interleave Key

**Claim:** **Cosmic** is not opened by SalPhaseIon recipe strings; it needs a **key or password derived from yin–yang recombination** of the earlier two AES blobs (creator #39237: yinyang follows AES decoding).

| Field | Specification |
|--------|----------------|
| **Construction** | From `load_containers()`: variants **V** = {`sal_yinyang_blocks`, `sal_yinyang_ct_bytes`, `sal_yinyang_b64_chars`, `term_sal_block_ab`, `term_sal_block_ba`, `xor_ct_salt_terminal`, `xor_ct_salt_salphaseion`} (7). For each `v`, candidate answers **A** = {`sha256hex(v)`, `sha256hex(v[:16])`, `sha256hex(v[16:])`, `latin1(v)` if decodable, `sha256hex(term⊕sal salt)`}. Target blob: **`cosmic.bin` only** (1328 B). KDF: §4.1 default + EVP-MD5 with `plain` and `sha256hex` for cosmic only. |
| **Decrypt budget** | 7×5×2 KDF variants = **70** cosmic decrypts (+ 7×5=35 sanity tries on **terminal** expecting null) = **105**. |
| **Detector** | Same `structured` as M1; optional **length gate** cosmic plaintext >200 B printable (book-title / prose tease). |
| **Signal if true** | ≥1 structured cosmic decrypt where password is a **function of interleave variant** `v` (document which `v`); terminal/sal remain unstructured for the same `A`. |
| **Null if false** | 0 structured on cosmic; 0 on cross-container sanity; pads ≈ **105/256**. |
| **Control** | Phase-2 `causality` unchanged (interleave not involved). |

---

## M3 — MatrixSumList → Operand, Enter → Decrypt Step

**Claim:** `matrixsumlist` is **`fn(poster)` → operand** (list or string), and `enter` is a **pipeline verb**: output of step *k* becomes the password (or intermediate `Salted__` blob) for step *k+1*, not a token inside one long concat.

| Field | Specification |
|--------|----------------|
| **Construction** | **fn** family **F** (8): spiral `list_row_sums`, `list_row_sums_sep`, spiral 14 diagonal sums, `msl-row`, `msl-col`, `sum(ab_bits sal[91:195])`, `int(spiral_bits)`, `tok23+list_row_sums`. **lastwords** **L** (4): `lw-arch-tail40`, first 8 `#8446` tokens, `sha256hex(flower)`, checkerboard phrase `HALFANDBETTERHALF…` abbreviated to 40 chars. **Pipeline:** (1) `pw₁ = sha256hex(f"{msl}")`; decrypt **`salphaseion_short`** → `pt₁`. (2) If `pt₁` passes pad, `pw₂ = sha256hex(pt₁.decode latin-1)` or literal `pt₁` prefix 64 chars; decrypt **`cosmic`**. (3) If `pt₂` passes pad, `pw₃ = sha256hex(lw)`; decrypt **`terminal`**. Also single-step baselines: `sha256hex(f"{msl}enter{lw}")` on each container (null baseline). |
| **Decrypt budget** | \|F\|×\|L\|×3 steps ×2 pw forms = 8×4×3×2 = **192** pipeline paths + 8×4×3 = **96** baselines = **288**. |
| **Detector** | Structured on **step 2 or 3** with provenance chain (label includes `msl` id + `lw` id); or `pt₁` itself structured (nested message). |
| **Signal if true** | Structured plaintext on **cosmic or terminal** only after a **successful prior sal decrypt** in the same chain; single-step baselines remain null. |
| **Null if false** | 0 structured on all 288; no chain where step1 pad-only and step2 structured (forbids lucky double-pad). |
| **Control** | `causality` single-step §4.1. |

---

## M4 — Faed Tail Channel Split (Bifid ≠ Password Material)

**Claim:** The **570-letter Bifid body** is a checksum channel (`btcseedd`); **password/key material lives in a secondary channel**—tail after index 8, **odd/even letter streams**, or **mask6-pinned integer**—and Beaufort is applied **only on that channel**.

| Field | Specification |
|--------|----------------|
| **Construction** | Canonical square + **8** `btcseed`-prefix squares. Channels **C** (6): `pt[8:]`, odd indices, even indices, `digits_to_bytes(mask6 zero)`, `digits_to_bytes(mask6 delete)`, Beaufort(`pt[8:]`, key=`btcseed`). Answers **A** = {channel text, `sha256hex(channel)`}. Containers: all three. KDF: §4.1 only (isolate channel, not KDF confusion). |
| **Decrypt budget** | 8 squares × 6 channels × 2 × 3 containers = **288** (canonical square only) + 8 alt squares × 4 channels × 2 × 3 = **192** = **480**. |
| **Detector** | Structured **or** uncomp hash160 from `sha256(channel)` raw32 (scalar branch, no extra decrypt). |
| **Signal if true** | Hit concentrated in **one channel type** across squares (e.g. odd stream) while full-`pt` and Beaufort-full-`pt` stay null (Rounds 2–3 already null full-pt—re-test as explicit negative stratum). |
| **Null if false** | 0 structured; 0 prize scalars; pads ≈ **480/256**. |
| **Control** | Bifid `btcseedd` + sha256 pins from `cryptanalyst_tests.py`. |

---

## M5 — Phase32 Plaintext Key Slot (Not Container Password)

**Claim:** The prize **private key is embedded in phase 3.2 plaintext** (Beaufort speech / **149-digit checkerboard** / tail regions), and the three AES containers hold **intel or red herrings**, not the final scalar.

| Field | Specification |
|--------|----------------|
| **Construction** | **Scalar probes** (no decrypt): sliding 32-byte windows over `phase32.bin` Beaufort bytes, checkerboard ASCII, decoded “half and better half” phrase, XOR of even/odd Architect bytes; each window → `is_win_uncompressed`. **Negative container bind:** phrases `checkerboard.txt`, `lw-arch-tail40`, `thispassword` label literal, and `sha256hex` thereof → §4.1 on all three containers (confirm containers are not keyed by obvious phase32 prose). |
| **Decrypt budget** | Windows ≈ **2200** scalars (cheap) + 12 strings × 3 containers = **36** decrypts. Report as **36 decrypts + 2200 scalars** (decrypt cap ≪10k). |
| **Detector** | **Win** = uncomp hash160 match; secondary: 32-byte window with valid secp256k1 range and **not** control key 1. |
| **Signal if true** | ≥1 win scalar from a **named window** (offset + encoding); container decrypts remain null for same strings. |
| **Null if false** | 0 wins; 0 structured container opens; archivist checkerboard phrase already [V] as ASCII—not a key. |
| **Control** | Private key 1 hash160; checkerboard decode string equals archivist #46. |

---

## Execution order (Round 5)

1. Run planted control for the active mechanism’s KDF.  
2. Execute mechanism battery; write `artifacts/round5_preregistered.json` with per-mechanism counts.  
3. Stop early if **structured** or **win**; still log partial budget.

**Total decrypt ceiling if all five run:** 240 + 105 + 288 + 480 + 36 = **1 149** (under 10k each and under 10k combined).

---

## Code map

- `team/round5_preregistered.py` — executable pre-registration for M1–M5  
- Reuses: `src/step1_btcseed.load_containers`, `src/crypto_known.decrypt_salted`, `team/cryptanalyst_tests.classify_plaintext`, `ledger/08-round2.md` operand list
