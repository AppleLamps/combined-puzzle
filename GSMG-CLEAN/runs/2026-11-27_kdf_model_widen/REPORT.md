# KDF model check, 2026-11-27

The 11.3M candidate dump from the previous pass is not in this repository.
This run uses the saved step-2, step-3 and step-4 strings and the
top-scoring creator-message fragments. It does not rebuild a password family
and it does not repeat the whole-message hashed-raw sweep.
The 84-cell parse stands: 23 prime tokens, 16 `b` and 7 `be`.

## 1. Ciphertext, before any decrypt

| Envelope | Decoded bytes | First 16 bytes | Salted__ | Salt | Ciphertext bytes | Validated round-trip |
|---|---:|---|---|---|---:|---|
| terminal_phase3_2_end | 96 | `53616c7465645f5fb45a5e3d827593ca` | yes | `b45a5e3d827593ca` | 80 | no |
| salphaseion_short | 96 | `53616c7465645f5f3ab585348552415d` | yes | `3ab585348552415d` | 80 | no |
| cosmic_duality | 1344 | `53616c7465645f5f2d3f6fe06dc950e6` | yes | `2d3f6fe06dc950e6` | 1328 | no |
| phase3_2_control | 2448 | `53616c7465645f5feefc4c5befc1656a` | yes | `eefc4c5befc1656a` | 2432 | yes |

Salted__ is the ASCII magic `53 61 6c 74 65 64 5f 5f`. Where it is present, bytes 8–15 are the salt and the ciphertext starts at byte 16.
Terminal, SalPhaseIon short and Cosmic Duality have no validated round-trip. Phase 3.2 does, and it is the control only.

## 2. Control: the one envelope that opens

Answer `jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple`. An open is pad 10 and the 2,422-byte plaintext beginning `I've been waiting`.

| Form | KDF | IV | Pad | Opens |
|---|---|---|---:|---|
| literal | evp-md5 | derived | 0 | no |
| literal | evp-md5 | zero | 0 | no |
| literal | evp-sha256 | derived | 0 | no |
| literal | evp-sha256 | zero | 0 | no |
| literal | pbkdf2-sha256-10000 | derived | 0 | no |
| literal | pbkdf2-sha256-10000 | zero | 0 | no |
| sha256hex | evp-md5 | derived | 0 | no |
| sha256hex | evp-md5 | zero | 0 | no |
| sha256hex | evp-sha256 | derived | 10 | yes |
| sha256hex | evp-sha256 | zero | 10 | no |
| sha256hex | pbkdf2-sha256-10000 | derived | 0 | no |
| sha256hex | pbkdf2-sha256-10000 | zero | 0 | no |
| rawdigest | evp-md5 | derived | 0 | no |
| rawdigest | evp-md5 | zero | 0 | no |
| rawdigest | evp-sha256 | derived | 0 | no |
| rawdigest | evp-sha256 | zero | 0 | no |
| rawdigest | pbkdf2-sha256-10000 | derived | 0 | no |
| rawdigest | pbkdf2-sha256-10000 | zero | 0 | no |

## 3. Candidates

19106 unique strings. A string can belong to more than one source.

- `chat-fragment`: 589
- `standing-84cell`: 5
- `step2-84cell-decode`: 78
- `step2-84cell-digits`: 36
- `step23-selection`: 2720
- `step3-lastwords`: 15676
- `step4-label`: 6

Forms on every string: literal UTF-8, lowercase sha256 hex, raw 32-byte sha256.
Runtime 178s.

## 4. Matrix

`pad>=1` is the chance PKCS#7 gate (about 1/256). `pad>=3` is the signal named for this run (about 1/16.8M). Structured means the unpadded bytes score as English (quadgram ≥ -4.6) or are at least 90% printable and 20 bytes or longer.

| Envelope | KDF | IV | Tests | pad≥1 | expected | pad≥3 | expected | structured |
|---|---|---|---:|---:|---:|---:|---:|---:|
| terminal_phase3_2_end | evp-md5 | derived | 57318 | 229 | 223.9 | 0 | 0.0034 | 0 |
| terminal_phase3_2_end | evp-md5 | zero | 57318 | 229 | 223.9 | 0 | 0.0034 | 0 |
| terminal_phase3_2_end | evp-sha256 | derived | 57318 | 233 | 223.9 | 0 | 0.0034 | 0 |
| terminal_phase3_2_end | evp-sha256 | zero | 57318 | 233 | 223.9 | 0 | 0.0034 | 0 |
| terminal_phase3_2_end | pbkdf2-sha256-10000 | derived | 57318 | 210 | 223.9 | 0 | 0.0034 | 0 |
| terminal_phase3_2_end | pbkdf2-sha256-10000 | zero | 57318 | 210 | 223.9 | 0 | 0.0034 | 0 |
| salphaseion_short | evp-md5 | derived | 57318 | 207 | 223.9 | 0 | 0.0034 | 0 |
| salphaseion_short | evp-md5 | zero | 57318 | 207 | 223.9 | 0 | 0.0034 | 0 |
| salphaseion_short | evp-sha256 | derived | 57318 | 237 | 223.9 | 0 | 0.0034 | 0 |
| salphaseion_short | evp-sha256 | zero | 57318 | 237 | 223.9 | 0 | 0.0034 | 0 |
| salphaseion_short | pbkdf2-sha256-10000 | derived | 57318 | 219 | 223.9 | 0 | 0.0034 | 0 |
| salphaseion_short | pbkdf2-sha256-10000 | zero | 57318 | 219 | 223.9 | 0 | 0.0034 | 0 |
| cosmic_duality | evp-md5 | derived | 57318 | 226 | 223.9 | 0 | 0.0034 | 0 |
| cosmic_duality | evp-md5 | zero | 57318 | 226 | 223.9 | 0 | 0.0034 | 0 |
| cosmic_duality | evp-sha256 | derived | 57318 | 230 | 223.9 | 0 | 0.0034 | 0 |
| cosmic_duality | evp-sha256 | zero | 57318 | 230 | 223.9 | 0 | 0.0034 | 0 |
| cosmic_duality | pbkdf2-sha256-10000 | derived | 57318 | 200 | 223.9 | 0 | 0.0034 | 0 |
| cosmic_duality | pbkdf2-sha256-10000 | zero | 57318 | 200 | 223.9 | 0 | 0.0034 | 0 |

## 5. Hits

No pad≥3 decrypt and no structured plaintext on the three locked envelopes.

## 6. What this separates

A fixed or zero IV does not kill the PKCS#7 gate. In CBC the last block is chained to the previous ciphertext block, so the padding bytes never see the message IV. The phase 3.2 control shows it: sha256 hex with EVP-SHA256 and a zero IV still has pad 10, and the plaintext does not open, because the first block is the one the IV changes. On the three locked envelopes, derived IV and zero IV produce the same pad≥1 count in every row.

Every KDF sits on the 1/256 line. EVP-MD5, EVP-SHA256 and PBKDF2-HMAC-SHA256 at 10,000 iterations, each with a derived IV and a zero IV, give pad≥1 counts of 200–237 against 224 expected. None of them produces a pad≥3 hit. Across 1,031,724 decrypts the expected pad≥3 count is about 0.06, so zero is the ordinary result for wrong passwords under a working decryptor.

The model that opens phase 3.2 is unchanged and narrow: passphrase = sha256(answer) as lowercase hex, EVP_BytesToKey with SHA-256, IV taken from that same stream, AES-256-CBC. Literal bytes, the raw digest, MD5, PBKDF2 and a zero IV all fail that control. MD5 and PBKDF2 do not suddenly produce pad≥3 hits on SalPhaseIon short or Cosmic Duality, so this run does not move the full password search onto a new KDF.

The previous 11.3M artifact is not in the repository, so this is not a byte-for-byte replay of that list. It is the saved step-2 84-cell sums, the saved step-2/3 selections, the saved last-words list, the step-4 yin-yang labels, and the top-scoring creator fragments. The 84-cell census used here is 23 prime tokens, 16 `b` and 7 `be`.

