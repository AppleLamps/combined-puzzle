# 19 — Round 11: Sal `enter` layout + Terminal-first + joint #8000

**Spec:** `team/preregister_round11_pipeline.json`  
**Code:** `team/round11_pipeline.py` → `artifacts/round11_pipeline.json`  
**Budget:** 2 000 (used **530** in first run; expandable in JSON)  
**Control:** §4.1 `causality` **PASS**

## Hypothesis (from structural review)

1. **G1 — Sal layout:** Short container is **b64 half₁ ∥ half₂** with `enter` (ab) between spans on the page; passwords should come from **z-stage** literals (`lastwords`, `thispassword`, shabef blocks) and **enter**-aware recipes, not only global label concat.
2. **G2 — Terminal-first:** Phase 3.2-only operands (checkerboard, 149 digits, Architect after `SELECT`, riddle, phase-1 hash) unlock **Terminal** first; plaintext derivations feed **Sal** (EVP-MD5) then **Cosmic** (raw32).
3. **G3 — Joint #8000:** Door indices `{1,4,21}` on digits/spiral/host bits, combined with faed door-zero / mask6 digests and host-bit joints (#8000: primes + zeroing + another door).

## G1 checks

| Check | Result |
|-------|--------|
| `concat_raw(half₁, half₂)` equals `salphaseion_short.bin` | **PASS** (96 B) |
| Joined blob / Sal / Terminal / Cosmic decrypts with stage passwords | **0** structured |

## Result

**0** structured plaintext, **0** prize hash160. Sal ciphertext layout is **confirmed** as split-at-`enter`; stage-local passwords still **null** on locked containers.

## Open

- XOR/interleave of halves **before** base64 decode (not in this pilot).  
- Liberal CBC (no pad gate) on chain step 0 — R7-style; not duplicated here.  
- Full z₁→z₂→z₃ **program** (each stage output as next operand).
