# 20 — Round 12: z-program, pre-decode joins, liberal Terminal-first

**Spec:** `team/preregister_round12_pipeline.json`  
**Code:** `team/round12_pipeline.py` → `artifacts/round12_pipeline.json`  
**Budget:** 2 000 (filled; stopped early)  
**Control:** §4.1 `causality` **PASS**

## G1 — z-stage program

Sal layout stages (`faed` → z → `lastwords` → z → `thispassword` → z → shabef) modeled as **ordered ops** with reducers:

- `concat_sha256hex_each` (rolling hash after each z-separated operand)
- `concat_literals_final_sha256hex`
- Named chains: host→faed→lw→tp, tok23→msl→lw, faed→lw→tp→shabef, msl→lw→tp→enter
- **Singles:** each stage operand alone (+ sha256hex) on three containers

## G2 — Pre-decode b64 join

Before base64 decode, combine half₁/half₂ with:

`interleave_chars`, `reverse_half2_concat`, `xor_char_codes_mod256`, `swap_halves_concat`

Passwords from z-program final, `enter`, phase-1 hash, host bits, faed bifid sha, literal concat. Targets Sal (+ std/MD5), Terminal, Cosmic on decoded bytes.

## G3 — Liberal Terminal-first

Phase 3.2 initials → **raw AES-CBC** (`aes_full_blocks`, no pad gate) + sliding-window structured scan → seeds for Sal (MD5) / Cosmic (raw32) / direct probes + **T→S→C** chain with `derivations_from_pt` on liberal byte windows (8-byte stride).

## Result

**0** structured, **0** prize hash160. Pre-decode joins and z-chained operands still **null**; liberal CBC did not surface pad-valid or scanner-detected plaintext that unlocks downstream containers.

## Open (Round 13+)

- z-program where **matrixsumlist** is an op on poster lists (not only ab-bit sum).  
- `enter` = XOR of decoded half raw ciphertext bodies (not char-level).  
- Sal **full page** 1075 as stage-0 input to the same program.
