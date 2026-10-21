# ZERO construction → all three locked envelopes (2026-09-13)

**Result: clean null.** No Half / Better Half key, no key-shaped string (64-hex, WIF, 32-byte base64), no readable plaintext and no pad ≥ 3 in 333,670 decrypts. Every pad rate is at chance.

## Setup (pre-registered)

`python run_zero_envelopes.py prepare` wrote the candidate files and `manifest.json` (hashes of candidates, envelopes and the script, plus the acceptance rules) **before** any decrypt. `run` refuses to start if a candidate file changed.

| Arm | Materials | Derivations | Envelopes | Decrypts |
|---|---|---|---|---|
| A. ZERO family | DBBI 7×13 prime cells coloured by a 24-label schedule → selected values, yellow/blue-zeroed lists, blue/yellow lists, signed row differences (−26,−21,−8,15), row sums, 72/32/40/104, zeroed DBBI (digits, `0` letters, deleted cells) and 7×13 row/column "matrix sum lists" for no/yellow/blue/all-24 zeroing; 7 text forms each (decimal, csv, space, A1/A0 upper/lower); ZERO words. Observed schedule = poster; controls = the other **149** nine-yellow schedules that also spell ZERO. 8,163 unique texts (214 from the poster schedule, 18 of them unique to it). | sha256-hex, raw, sha256-raw × EVP SHA-256 / MD5 → AES-256-CBC | Terminal, SalPhaseIon short, Cosmic | 146,934 |
| B. fresh-start `prime_matrix_cross_stage.py` | 5,076 byte passwords (captured from its own generator, not re-typed) | EVP SHA-256 / MD5 | all three | 30,456 |
| C. astra zero-mask checkerboard | 944 unique zeroed digit inputs and board decodes (previously decode-only) | as arm A | all three | 16,992 |
| D. fresh-start `openssl_cipher_family_audit.py` | 1,514 passwords | 46 OpenSSL cipher configs (AES/DES/3DES/Blowfish/CAST/RC2 in CBC/ECB/CFB/OFB, RC4) × EVP MD5 / SHA-256 | **full 96-byte** Terminal (its earlier run loaded 48 B) | 139,288 |

Detection on every surviving output: PKCS#7 pad length; Half / Better Half match on every raw 32-byte window, 64-hex run, WIF and 32-byte base64 run (compressed and uncompressed); printable/letter ratios; for arm D also fresh-start's own `coherent()` / `nested()` gates, applied to all CFB/OFB/RC4 outputs too.

## Controls (all passed)

- The envelope code opens the real Phase 3.2 envelope (pad 10, 2,422 B).
- The key detector finds a planted k=1 key as raw32 and WIF.
- **Loader control:** arm B on SalPhaseIon short gave **45** pad hits, exactly what fresh-start recorded, so its `stream_80` and our `locked_salphaseion_short.bin` are the same envelope and the materials were captured correctly.
- ZERO arithmetic re-derived from `data/DBBI_91.txt`: row differences −26,−21,−8,15 → ZERO; sums 72/32/40/104; exactly 150 ZERO schedules of C(24,9) = 1,307,504 (matches astra).
- No file in `E:\testing-btc-p\fresh-start` or `D:\astra` was modified (checked by mtime).

## Results

| Arm / group | Envelope | Trials | Pad hits | Expected |
|---|---|---:|---:|---:|
| A control-only | Cosmic / SalPhaseIon / Terminal | 47,694 each | 182 / 176 / 193 | 187 |
| A poster-only | same | 108 each | 0 / 1 / 0 | 0.4 |
| A shared | same | 1,176 each | 1 / 3 / 4 | 4.6 |
| B | same | 10,152 each | 47 / 45 / 47 | 39.8 |
| C | same | 5,664 each | 25 / 27 / 14 | 22.2 |
| D CBC / ECB | Terminal | 33,308 each | 134 / 128 | 130 |

- Arms A–C: 762 pad-1 and 3 pad-2 hits (≈3.0 pad-2 expected in 194,382 trials). The three pad-2 outputs are binary noise (printable ≤ 0.42); two come from control schedules, one from arm C.
- Arm D: 0 coherent or nested outputs, 0 keys, including all 72,672 stream-mode outputs.
- Key matches: **0**. Key-shaped strings of any kind: **0**.

## What this closes

- The ZERO prime-grid construction, in the direct forms above (values, zeroed lists, signed differences, sums, zeroed DBBI, matrix sum lists), does not open any locked envelope under the proven convention or the MD5/raw variants.
- The fresh-start ZERO materials are now tested on all three envelopes, not SalPhaseIon only.
- astra's zero-masked checkerboard strings are now hashed and tested.
- The voided fresh-start Terminal cipher-family null is **restored as a valid null** on the full envelope.

## What it does not close

- Uses of ZERO as an *instruction* applied to other material (FAED, the Architect text, the 83-token parse, the poster bits) beyond the masks listed; combined answers (e.g. ZERO output + another answer); multi-step pipelines; other KDFs (PBKDF2, more EVP iterations).
- ZERO's post-hoc status is unchanged: it is still a controlled coincidence with no demonstrated use.

## Files

`run_zero_envelopes.py` (prepare / run), `manifest.json` (pre-registration), `arm_*` candidate files, `results.json` (all pad hits with plaintext hex, tallies), `run_log.txt`, `summarize.py` (prints the table above).
