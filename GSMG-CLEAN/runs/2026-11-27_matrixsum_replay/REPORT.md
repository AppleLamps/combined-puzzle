# NULL: matrix-sum pipeline replay -- 0 hits in 27,708 decrypts

**Result: NULL.** Zero notable outputs (pad >= 3 or key match) across 27,708 AES-256-CBC
decrypts (9,236 forms x 3 envelopes x 1 profile). All 111 pad-valid outputs are pad = 1,
consistent with the chance rate.

## Forms

- Unique text forms regenerated: **9,236** (matches the 2026-09-13 run exactly)
- Real outputs: 4,677 (12 decode families x 552 sum lists, filtered by family guards)
- Excluded forms (splitlines breakers): **0**
- forms.txt SHA256: `1ae404a0b6d8e97d91fd6c2f71d2374e73c4b95db8ca9015be41e80a98dcfcb2`

Source: `runs/2026-09-13_matrixsum_pipeline/sum_lists.json` (552 sum lists, unchanged)
with the same decode families and `text_forms()` from `run_pipeline.py`.

## Pinned profile

**gsmg**: passphrase = lowercase hex of sha256(form) as 64 ASCII bytes;
OpenSSL EVP_BytesToKey SHA-256, 1 iteration; AES-256-CBC; salt = bytes 8..16 of envelope;
strict PKCS#7 unpadding. No MD5, no raw passphrase, no PBKDF2.

## Controls

1. **check_candidate.py --selftest**: PASSED
   Phase 3.2 envelope opens, pad = 10, plaintext = 2,422 B.
2. **Planted control**: Synthetic Salted__ envelope encrypted with gsmg profile
   (passphrase = sha256-hex of `planted_control_matrixsum_replay_2026_11_27`).
   Decrypted correctly: pad = 7, plaintext matches planted bytes.

## Preregistration

- Sealed: 2026-11-27T18:16:39Z
- PREREG SHA256: `71eae87ac4ab3438f9623df72c973666ee26f59372e1822f42cfd372c84bc790`
- Self-check: **passed** (forms count = 9,236, no splitlines breakers, controls pass)

## Pad histograms

### terminal_phase3_2_end (9,236 decrypts)

| pad | count | expected |
|-----|-------|----------|
| 0   | 9,207 | 9,199.9  |
| 1   | 29    | 35.9     |

### salphaseion_short (9,236 decrypts)

| pad | count | expected |
|-----|-------|----------|
| 0   | 9,195 | 9,199.9  |
| 1   | 41    | 35.9     |

### cosmic_duality (9,236 decrypts)

| pad | count | expected |
|-----|-------|----------|
| 0   | 9,195 | 9,199.9  |
| 1   | 41    | 35.9     |

Expected pad = 1 per envelope: N * (255/256) * (1/256) = 35.9.
Expected pad >= 3 per envelope: ~1 in 16.8M per decrypt. With 9,236 trials, P(any pad >= 3) ~ 0.00055.

### Comparison with 2026-09-13 run

The original run tested 9,236 forms x **4 profiles** x 3 envelopes = 110,832 trials and saw
pad0 = 110,394, pad1 = 437, pad2 = 1 (expected pad1 ~ 431). This replay uses only the
pinned gsmg profile (27,708 trials) and sees pad1 = 111 (expected ~ 108). Both are
consistent with chance.

## Poisson tail (null validation)

**Cosmic Duality alone**: lambda = 35.94, observed pad >= 1 = 41. P(X >= 41) = 0.2197.

**All envelopes combined**: lambda = 107.81, observed pad >= 1 = 111. P(X >= 111) = 0.3921.

Both are well within the null distribution. Pad 1 at the chance rate is the null.

## Retained plaintexts

All 111 pad-valid outputs retained as full plaintext bytes in `outputs/ENVELOPE/ROW.bin`,
with metadata in `results.json`.

| envelope                 | count | files                              |
|--------------------------|-------|------------------------------------|
| terminal_phase3_2_end    | 29    | `outputs/terminal_phase3_2_end/0.bin` ... `28.bin` |
| salphaseion_short        | 41    | `outputs/salphaseion_short/0.bin` ... `40.bin`     |
| cosmic_duality           | 41    | `outputs/cosmic_duality/0.bin` ... `40.bin`        |

All are pad = 1, printable ratio 25-49% (random bytes), no key matches detected.
None reads as language.

## Source hashes

| file | SHA256 |
|------|--------|
| run_pipeline.py (2026-09-13) | `76b11ac5a455e01c2f11bc1247780d7283f310720018597cf4444310be0d1dd5` |
| sum_lists.json (2026-09-13)  | `949845b9c673d4d59b18511725e3301fd399be0724d6e2216da7360a9a2552b9` |
| replay.py                    | `7227427bcdccf1e51a3fadbb5fe2eb9051eb52e07dc786422d37682bb5d98bd8` |
| puzzle.png                   | `38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830` |
| DBBI_91.txt                  | `ec374000d5f070de550469ae0f24b414dbb2673f9f41aa498ae00d8f97355565` |
| FAED_570.txt                 | `a8f4d4c255deeba1cd2c9ba0b87af6bc6b737eee74ebbc45b457fe68965b3d35` |
