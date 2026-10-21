# Cosmic Duality checkpoint: 4f7a1e4e vs a5502d09

Date of check: 2026-10-08. Container: `files/cosmic-duality.b64` (1794 base64 chars, 1328 ciphertext bytes, mod 16 = 0).
Salt: `2d3f6fe06dc950e6` (matches the `CD:` salt in the 2026-09-03 chat post and `Naddiseo_17`).

## Result

| claim | derivation | reproduced here? |
|---|---|---|
| `4f7a1e4e…c081` (SHA-256 of 1327-byte plaintext) | master key `a795de11…0735` used as 32 raw bytes, EVP_BytesToKey MD5 (one iteration), AES-256-CBC, PKCS#7 | **Yes.** Body 1327 bytes, SHA-256 `4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081`. |
| `a5502d09…` ("our reproducible result") | not stated anywhere in the export | **No.** No method was published, so it cannot be reproduced or compared byte for byte. |

## Master key `a795de11…` (the input to the 4f7a1e4e derivation)

- Master = XOR of SHA-256 over five tokens: `enter`, `lastwordsbeforearchichoice`, `thispassword`, `yourlastcommand`, `secondanswer`.
- Found by testing all 32,767 non-empty subsets of 15 candidate token strings. One subset gives `a795de117e472590e572dc193130c763e3fb555ee5db9d34494e156152e50735`; no other subset does.
- The candidate pool was chosen by hand, so the hit is only as good as the pool. A 256-bit match by chance is not a real risk, so the token set itself is solid.

## Attempts at `a5502d09`

Simple hashes of the same decryption do not match `a5502d09`:

- `sha256(body)` = `4f7a1e4e` (the known checkpoint)
- `sha256(padded plaintext)` = `c5ebb50d`
- `sha256(body minus last byte)` = `dc059af3`
- `sha256(ciphertext)` = `43cb531c`
- `sha256(full container)` = `b1895055`
- `sha256(salt + body)` = `7d103641`

Other variants also fail. Under the same master key, EVP-SHA256 and the hex-string form of the master key give no valid padding.

## Sources

- Telegram export `ChatExport_2026-10-08/result.json`, message id 71309 (2026-09-09 15:29 UTC, "peter chen"): "Community checkpoint 4f7a1e4e proven incorrect — Our reproducible result is a5502d09". No method given.
- Same export, id 71310 (2026-09-09 15:38 UTC, "Denis Golovkin"): links a Hugging Face space, `CoruNethron/openssl-for-restless-souls`. Not opened. It is an unvetted third-party link posted in the chat and may be the tool behind the a5502d09 claim.
- `mywork2/web/issues/puzzlehunt_104.md` (Anvexis, 2026-08-23): the 4f7a1e4e derivation and master key, as above.
- `mywork2/web/issues/puzzlehunt_108.md`: states the CADEIA 3 link (cosmic 1327 B, sha `4f7a1e4e…`) through the WIF chain. The derivation here (master key, not WIF) does not depend on that chain.
- `mywork2/web/issues/Naddiseo_17.md`: reports that the cosmic blob does not open with WIF(K_S1) or related passwords. This agrees with the finding here: the blob opens with the master key, not with the WIF chain.

## What this means

- The 4f7a1e4e value is arithmetically reproducible from public inputs (five tokens plus the blob). The dispute is not about arithmetic. Whether a 1327-byte plaintext is the intended checkpoint is a separate question, and this check does not settle it.
- The a5502d09 claim is unverifiable as published. A byte-for-byte comparison needs its method, plaintext length, or key.
- Next step if the a5502d09 method is wanted: ask the poster (peter chen) for the key, plaintext length, and hash input. Do not open the unvetted link from the chat without review.

## Reproduce

Scripts are in the session scratchpad (outside the project):

- `cosmic_check.py`: EVP-MD5 decryption with the master key and SHA-256 of the body.
- `master_xor_check.py`: subset search for the master key.

Commands:

```bash
python -I cosmic_check.py
python -I master_xor_check.py
```
