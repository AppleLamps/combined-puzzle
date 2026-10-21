# 11 — Team brainstorm: path forward (Composer agents)

**Agents:** [Strategist path synthesis](bc-7eeec15f-a0fa-5fdb-b800-73c2e6d9b17d) · [Reader untested readings](bc-5fd657d0-8b88-5cc6-a514-aa6139dc8e89) · [Cryptanalyst mechanisms](bc-46981599-b782-5833-aee3-ffe351b5d31b) · [Skeptic kill paths](bc-44253c05-3417-5daf-83ef-10d28f862e42) · [Tester Round 5 plan](bc-ece5ab54-8b32-506f-a6b1-0209a6c879f6)

**Win:** uncomp hash160 `a9553269572a317e39f0f518cb87c1a0ee1dbae4`. **Offline only.**

---

## Executive summary

1. **Stop** treating `btcseed`, `szqu`, filler deletion-at-scale, and Sal-short MD5 padding as progress ([Skeptic kill paths](bc-44253c05-3417-5daf-83ef-10d28f862e42)).
2. **Pivot** from “one password string” to a **pre-registered pipeline**: poster/`matrixsumlist` **operation** → Sal-short → plaintext feeds Terminal/Cosmic ([Cryptanalyst mechanisms](bc-46981599-b782-5833-aee3-ffe351b5d31b) M3, [Strategist path synthesis](bc-7eeec15f-a0fa-5fdb-b800-73c2e6d9b17d) H1).
3. **Round 5 executed:** `ledger/12-round5.md` — **15,753** decrypts + M1–M5 **280** → **null**; controls PASS.

---

## What we are not doing next

| STOP | Why |
|------|-----|
| More Bifid/Beaufort §4.1 on period-570 prefix | R2–3 null; 8/362 880 calibration |
| MASK6 / `szqu` / head `yM` as passwords | Search artifacts; deletion kills pins |
| Filler deletion C(60,k) for k≥3 without new rule | **1.68M** §4.1 null (R3–4) |
| Community MD5 template permutations | 79 B pad only; retracted |
| Spiral **scalar sums** as passwords | R3–4 null |

---

## Coordinated hypotheses (register before run)

### A — `#8446` multi-container pipeline (Strategist H1 + Cryptanalyst M3)

```
tok23 ──► msl = fn(poster)     [list joins, ab-bytes, 14 spiral row-sums — NOT sum=56 alone]
         ──► sha256hex ──► decrypt Sal-short (§4.1 ± EVP-MD5 plain)
         ──► pt₁ ──► sha256hex(pt₁ ‖ lw) ──► Terminal
         ──► pt₂ ──► sha256hex(… ‖ yinyang) ──► Cosmic
```

`lastwords`: per-`CHOICE` word extraction **or** checkerboard 149-digit `msl` ([Reader](bc-5fd657d0-8b88-5cc6-a514-aa6139dc8e89) priorities 1–2).

**Falsify:** no structured plaintext on step 2/3; padding ≈ chance per step.

### B — Per-container KDF (Cryptanalyst M1)

Same operand, **different** (password encoding, EVP digest) per blob — e.g. Sal-short MD5 plain, Terminal sha256hex, Cosmic raw32 digest.

**Falsify:** structured hit only on **assigned** (container, profile) cell; cross-cells null.

### C — Cosmic via yin-yang / XOR material (Cryptanalyst M2 + Reader #5)

Password = f(interleaved terminal⊕sal variants), **cosmic only**.

**Falsify:** structured cosmic decrypt; terminal null for same answer.

### D — Faed **tail channel** only (Cryptanalyst M4)

Bifid prefix = checksum; material in `pt[8:]`, odd/even streams, mask6 integer — **not** full 570 as password.

**Falsify:** small §4.1 battery on channels only (≤10k).

### E — `another door` **structured** deletion (Strategist H3)

Delete filler/faed at **{1,4,21} ∪ primes≤23**, not random C(60,k).

**Falsify:** encode survivors → §4.1 on Terminal/Cosmic only.

---

## Reader top 5 (not in R2–4)

1. Phase 3.2 text **after** `SELECT` (cipher/encryption list)
2. Checkerboard **149 digits** as `matrixsumlist`
3. Creator **#6509** “unforeseen hint” → pick one `fn(matrixsumlist)`
4. **Yinyang** as phase (yin-yang container targets)
5. **`enter` as XOR** (combine stage bytes, not concat)

Full table: `ledger/round5/reader.md`.

---

## Recommended sequence (5 steps)

| Step | Action | Budget | Stop if |
|------|--------|--------|---------|
| **1** | Run `team/round5_preregistered.py` M1 pilot (KDF profiles) | ≤240 | No profile-specific structured hit |
| **2** | Run Round 5 plan H1–H4 ([Tester](bc-ece5ab54-8b32-506f-a6b1-0209a6c879f6)) | ~15k | Null + controls OK |
| **3** | If H1 null: **after-SELECT** + 149-digit msl only (Reader #1–2) | ~500 | Null |
| **4** | If still null: **pipeline M3** with checkerboard HALF/BETTERHALF lw | ~300 | No chained structured pt |
| **5** | If still null: **door-index deletion E** + Sal **full page** 1075-char key ([Reader](bc-5fd657d0-8b88-5cc6-a514-aa6139dc8e89)) | ~1k | Null → revisit [R] phase-3 part strings & off-page lore (explicitly weaker) |

---

## Epistemic bar ([Skeptic](bc-44253c05-3417-5daf-83ef-10d28f862e42))

- One construction per ledger entry; operands from §6.2 / primary text only.
- Planted control per KDF before counting nulls.
- Pilot before six-figure sweeps.
- Prize likely still **behind** a container decrypt; direct scalar from faed tail remains **unregistered fishing** until a single map is written.

---

## Artifacts

| File | Role |
|------|------|
| `ledger/round5/strategist.md` | Ruled out / plausible / H1–H3 |
| `ledger/round5/reader.md` | Untested readings + falsification tests |
| `ledger/round5/cryptanalyst.md` | Mechanisms M1–M5 |
| `ledger/round5/skeptic.md` | STOP list + evidence bar |
| `ledger/round5/tester.md` | Round 5 decrypt budget (~15k) |
| `team/round5_preregistered.py` | Executable M1–M5 skeleton |
