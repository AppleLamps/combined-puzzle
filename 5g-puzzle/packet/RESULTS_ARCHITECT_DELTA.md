# Architect substitution delta as leftover-3.2 key (2026-09-09)

Closed list: `packet/password_list_architect_delta.json` (42 strings × raw + sha256hex × 4 KDFs × 3 blobs = **1008** attempts). Spec SHA-256 `7a752931…bc7f`. Harness self-tested against the published Cosmic Duality 7-XOR decrypt (`4f7a1e4e…c081`). No 7-interleave. No brute force.

Machine log: `packet/out/results_architect_delta.json`.

## What the request got right

Almost the entire Beaufort 3.2.1 block is the Reloaded Architect speech. What he **changed** is the message. Packet 1 had already tried `reinserting the prime basics` (the film’s “prime program”). The replacement *phrases themselves* — `THIS PUZZLE`, `SEDULOUSLY AVOID IT`, `THE YOU`, `THE SOURCE CODES`, `HOPEFULLY`, `PRIME BASICS`, `OVER twenty three CIPHERS`, `ENCRYPTIONS`, `INTERTWINED PASSWORDS`, `FIND THE ACTUAL PRIVATE KEY`, the inserted brute-force note, `YOUR WILLPOWER`, `YOUR WILL TO LIVE`, `THE ENTIRENESS OF YOURSELF SELF`, and `CIAO BELLA O` — had never been in a frozen password list. Neither had the concatenation of those substitutions in order.

The inserted sentence `NOTE THAT ALSO BRUTE FORCING MIGHT BE REQUIRED` has no film counterpart. That is a warning, not a method. This packet does not brute.

## AES result

**The substitutions do not decrypt leftover 3.2.** 7 PKCS#7 successes in 1008 attempts (chance rate is ~4; all seven are `pt_len` = blob-max, i.e. `pad=0x01`). Zero readable, zero `gsmg.io/` paths, zero `1GSMG` hits.

Tried, all closed: each substitution as it appears (spaced and compacted); `OVER TWENTY-THREE` hyphen variant; `SIXTEEN ENCRYPTIONS` / `SEVEN INTERTWINED PASSWORDS` as full replacements for “sixteen female” / “seven male”; the full in-order concat (spaced, compacted upper, compacted lower); the token-only concat; `CIAO BELLA O`. Each as OpenSSL password and as SHA-256 hex, under `evp_md5` / `evp_sha1` / `evp_sha256` / `pbkdf2_sha256_10000`, against leftover 3.2, the 79-byte Salph fragment, and Cosmic Duality.

## After this packet

The Architect paragraph remains **instructions**, not an AES password. “Seven intertwined passwords” already has a published meaning (XOR of seven SHA-256s) that opened Cosmic Duality; do not resume interleave. “OVER twenty three” is not a licence to grow a 24th cipher list. Do not unbounded-brute leftover 3.2. Do not encode these same phrases again (more case folds, more concatenations). Leftover 3.2 is still unopened; this operand is now closed.
