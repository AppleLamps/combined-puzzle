# 16 — Round 8: Reader gap pilot G1–G7

**Spec:** `team/preregister_reader_gap.json`  
**Code:** `team/round8_reader_gap.py` → `artifacts/round8_reader_gap.json`  
**Budget:** 2 000 (used **1 995**)  
**Control:** §4.1 `causality` **PASS**  
**Detector:** `step1_btcseed.classify` + `win_key` on plaintext; `is_win_uncompressed` on `sha256(answer)`

## Gaps executed

| Gap | Item | Tries | Result |
|-----|------|------:|--------|
| **G1** | Cosmic Duality / Time-Life title strings (14 × std + sal MD5 + cosmic raw32) | 70 | null |
| **G2** | #6913 **21** / **1812** bit windows on 6 bit sources (offsets preregistered) | 1 776 | null |
| **G3** | Sal **full page** operands (compact, span concat, dbbi+faed, labels) + cosmic raw32 | 30 | null |
| **G4** | `shabefour…` vs `sha256our…` / `anstoo` families (+ sha256hex) | 63 | null |
| **G5** | Derived **binary → sha256hex** (host bits, mask6 zero, xor salt) | 12 | null |
| **G6** | **H2** filler first-appearance Bifid square + Beaufort (`btcseed`, flower hash); canonical square control | 36 | null |
| **G7** | **H3** door-index deletion on filler/faed → sha256hex / literal | 8 | null |

## Falsification (Reader audit rows 1–7)

| # | Reading | Status |
|---|---------|--------|
| 1 | Cosmic Duality title | **Tested null** (this pilot) |
| 2 | #6913 bit-width windows | **Tested null** (registered offsets/packings) |
| 3 | Sal full 1075-char key | **Tested null** |
| 4 | shabefour vs sha256our | **Tested null** |
| 5 | Derived-binary sha pipeline | **Tested null** |
| 6 | H2 filler-square Beaufort factory | **Tested null** (+ canonical square control null) |
| 7 | H3 door-index deletion | **Tested null** |

## Notes

- G2 does **not** exhaust all bit offsets — frozen list in JSON only; expand only with new preregistration.
- G6 Beaufort on Bifid output uses **lowercase a–z** mapping; phase32 symbol alphabet not retested here.
- Rows **8–15** from Reader audit (`ledger/15-team-audit.md`) remain open (Bifid periods ≠570, dbbi past 97, roses tuples, etc.).

## Result

**0** structured plaintext, **0** prize hash160 under registered detectors and KDF matrix.
