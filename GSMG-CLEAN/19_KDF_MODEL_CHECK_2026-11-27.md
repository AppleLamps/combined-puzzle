# 19 — The decryption model for the two unopened envelopes

**Status: unsolved.** No locked envelope opened. Evidence: `runs/2026-11-27_kdf_model_widen/REPORT.md`.

The question was whether SalPhaseIon short and Cosmic Duality were failing because the passwords were wrong or because the key derivation was wrong. The derivation had only been proven on phase 3.2.

## Ciphertext

All three locked envelopes, and the phase 3.2 control, begin with `Salted__` (`53 61 6c 74 65 64 5f 5f`). The next 8 bytes are the salt. The ciphertext starts at byte 16.

| Envelope | Decoded bytes | Salt | Ciphertext | Validated round-trip |
|---|---:|---|---:|---|
| Terminal | 96 | `b45a5e3d827593ca` | 80 | no |
| SalPhaseIon short | 96 | `3ab585348552415d` | 80 | no |
| Cosmic Duality | 1344 | `2d3f6fe06dc950e6` | 1328 | no |
| Phase 3.2 | 2448 | `eefc4c5befc1656a` | 2432 | yes |

## What was varied

Same passphrase forms as the last pass: literal UTF-8, sha256 hex, raw sha256 digest. Three derivations, each with the IV from the derivation and with a zero IV:

- EVP_BytesToKey, MD5, one iteration
- EVP_BytesToKey, SHA-256, one iteration
- PBKDF2-HMAC-SHA256, 10,000 iterations, 48 bytes split into key and IV

The strings are the saved 84-cell step-2 sums, the saved step-2/3 selections, the saved last-words list, the yin-yang labels, and the top-scoring creator-message fragments. 19,106 unique strings, 57,318 tests per cell. The 84-cell census is unchanged: 23 prime tokens, 16 `b`, 7 `be`. The whole-message hashed-raw sweep was not repeated. The 11.3M dump itself is not in the repository.

## Result

Phase 3.2 opens under one cell only: sha256 hex, EVP-SHA256, derived IV, pad 10, 2,422 bytes. A zero IV on that same key still has pad 10 and does not open. CBC padding is decided by the last block, which is chained to the previous ciphertext block, so a wrong IV cannot make a correct key fail the padding gate.

On the three locked envelopes every cell, including MD5 and PBKDF2, has pad≥1 on the 1/256 line (200–237 against 224 expected) and pad≥3 of 0. No plaintext scored as structured. A new KDF did not produce the pad≥3 hits that SHA-256 lacked. The null on these strings is the passwords, under a decryptor that is alive for all three derivations. The full search stays on EVP-SHA256 with the salt-derived IV.
