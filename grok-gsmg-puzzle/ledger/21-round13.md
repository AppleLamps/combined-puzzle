# 21 — Round 13: byte XOR `enter`, poster `matrixsumlist`, full Sal stage-0

**Spec:** `team/preregister_round13_pipeline.json`  
**Code:** `team/round13_pipeline.py` → `artifacts/round13_pipeline.json`  
**Budget:** 2 000 (used **1 025**)  
**Control:** §4.1 `causality` **PASS**

## G1 — `enter` as byte XOR of b64 halves

Decode Sal spans `[895,959)` and `[999,1063)` to **48+48 B**; build:

| Blob | Rule |
|------|------|
| `xor_full_48` | Byte XOR of equal-length halves |
| `xor_ct_only` | Same salt prefix; XOR ciphertext tails |
| `xor_salt_prefix_rest_xor` | `Salted__` + salt + XOR(ct₁, ct₂) |
| `concat_then_xor_ct` | XOR of ct streams with length padding |
| `canonical_concat` | Control (= `salphaseion_short.bin`) |

Passwords: z-chain lit sha, `enter`, lw/tp literals, phase-1 hash, **sha256(xor bytes)**. Profiles: std-hex, plain-MD5 (Sal), raw32 (Cosmic).

## G2 — Poster `matrixsumlist` in z-chain

Nine preregistered poster sums (`sum-rows`, `spiral-bits`, full `row`/`col` digit strings, etc.) chained with `lastwords` + `thispassword` + `enter` via rolling sha256hex and literal concat; singles + sha on all three containers.

## G3 — Full Sal page (1075) as stage-0

Stage-0 forms: sha256hex(compact page), literal prefix 512, sha256hex(dbbi‖faed), sha256hex(pre-shabef), sha256hex(shabef…tail). Chained with lw/tp/shabef and poster row/spiral sums.

## Result

**0** structured, **0** prize hash160. Byte-XOR “enter” blobs and full-page stage-0 still **null** on locked containers.

## Open

- XOR **only after** stripping `Salted__` headers from each half separately.  
- `matrixsumlist` = **spiral list row sums** with separators (R4 family) inside z-chain.  
- Stage-0 = EVP decrypt of **inline** Sal ciphertext using page hash as password.
