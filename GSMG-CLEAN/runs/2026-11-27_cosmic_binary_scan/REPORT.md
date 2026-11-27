# Binary, Magic, Entropy, and Decompression Scan of Retained Pad-Valid Plaintexts

**Result: NULL (0 flagged files).** Scanned **97** retained pad-valid plaintexts across the entire repository (**49** Cosmic Duality, **48** SalPhaseIon short; all unique SHA-256; **0** new decrypts performed). No file triggered any magic-byte, PGP/armor, alphabet-fraction, low-entropy, repeated-block, or `zlib`/`gzip` decompression flag.

## 1. Counts Scanned per Envelope

| Envelope | Files scanned | Unique SHA-256 | Pad lengths | Size (B) | Flagged | `zlib` ok | `gzip` ok |
|---|---:|---:|---|---:|---:|---:|---:|
| Cosmic Duality (`locked_cosmic_duality`) | 49 | 49 | pad 1: 49 | 1,327 | 0 | 0 | 0 |
| SalPhaseIon short (`locked_salphaseion_short`) | 48 | 48 | pad 1: 48 | 79 | 0 | 0 | 0 |
| **Total** | **97** | **97** | all pad 1 | — | **0** | **0** | **0** |

### Breakdown by run folder

| Envelope | Run / artifact folder | Files scanned |
|---|---|---:|
| Cosmic Duality | `GSMG-CLEAN/runs/2026-11-27_fefefe_replay` | 2 |
| Cosmic Duality | `GSMG-CLEAN/runs/2026-11-27_lastwords_preamble_replay` | 5 |
| Cosmic Duality | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | 41 |
| Cosmic Duality | `puzle/gsmgio-5btc-puzzle-master/artifacts/bin` | 1 |
| SalPhaseIon short | `GSMG-CLEAN/runs/2026-09-14_adversarial_reanalysis/exp2_first_hint_last_command` | 1 |
| SalPhaseIon short | `GSMG-CLEAN/runs/2026-11-27_fefefe_replay` | 1 |
| SalPhaseIon short | `GSMG-CLEAN/runs/2026-11-27_lastwords_preamble_replay` | 3 |
| SalPhaseIon short | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | 41 |
| SalPhaseIon short | `GSMG-CLEAN/runs/2026-11-27_review_candidates` | 1 |
| SalPhaseIon short | `puzle/gsmgio-5btc-puzzle-master/artifacts/bin` | 1 |

## 2. Flagged Files

| Envelope | Run folder | File | Candidate | Pad | Size | First 16 bytes (hex) | Flags |
|---|---|---|---|---:|---:|---|---|
| *(none)* | — | — | — | — | — | — | **0 files flagged across both envelopes** |

## 3. Summary Statistics and Diagnostics

- **Self-test (synthetic controls, no AES):** PASSED across all **22** positive test vectors (`PNG`, `JPEG`, `GIF`, `BMP`, `gzip`, `zlib` `78 01/5E/9C/DA`, `bzip2`, `zip`, `PDF`, `Salted__`, PGP armor, Base64 > 0.9, hex > 0.9, printable > 0.8, low entropy < 7.0 on > 256 B, aligned and shifted repeated 16-byte blocks, and valid `zlib`/`gzip` payloads), **0** flags on the 1,327 B pseudo-random negative control (H = 7.8387 bits/byte), and verified that the `< 7.0` entropy flag does not fire on files <= 256 B.
- **Cosmic Duality (49 files, 1,327 B each):** Shannon entropy H in `[7.8226, 7.8799]` bits/byte (consistent with 1,327 uniform random bytes, expected ~7.86); max Base64-alphabet fraction `0.2766` (random mean 0.2539); max hex-alphabet fraction `0.1070` (random mean 0.0859); max printable fraction `0.4205` (random mean 0.3828).
- **SalPhaseIon short (48 files, 79 B each):** Shannon entropy H in `[5.7941, 6.2025]` bits/byte (for 79 bytes, the maximum possible entropy is log2(79) = 6.3038 and uniform random bytes average ~6.08; the `< 7.0` flag applies only to files > 256 B); max Base64-alphabet fraction `0.3671`; max hex-alphabet fraction `0.1646`; max printable fraction `0.5063`.
- **Decompression diagnostics:** `zlib.decompress` succeeded on **0/97** files; `gzip.decompress` succeeded on **0/97** files; scanning every internal `78 01/5E/9C/DA` or `1F 8B` offset across all 97 files yielded **0** valid streams. As an extra headerless diagnostic (`zlib.decompressobj(-15)` raw deflate), one Cosmic Duality file (`GSMG-CLEAN/runs/2026-11-27_matrixsum_replay/outputs/cosmic_duality/12.bin`, prefix `63615507c4...`) happened to start with 5 random bytes forming a valid 3-byte final fixed-Huffman deflate block (`040527`), leaving **1,322 of 1,327 bytes unused** — a routine random prefix artifact, not a compressed payload.
- **Embedded 4+-byte magics (`PNG`, `zip`, `PDF`, `Salted__`):** **0** occurrences at any offset in any of the 97 files.
- **Padded-storage note:** `GSMG-CLEAN/runs/2026-09-14_adversarial_reanalysis/exp2_first_hint_last_command/outputs/00019_F1_raw_sha256_locked_salphaseion_short.bin` is stored on disk as the 80-byte raw padded decrypt (PKCS#7 pad = 1, trailing `0x01`); its 1-byte pad was stripped before scanning (79 B), and scanning the raw 80-byte file also yields 0 flags. In `puzle/gsmgio-5btc-puzzle-master/artifacts/bin/`, the unpadded files `cosmic_plaintext.bin` (1,327 B) and `chain1_plaintext.bin` (79 B) were scanned once each (avoiding double-counting their paired padded copies `cosmic_padded_plaintext.bin` and `chain1_padded_plaintext.bin`).

## 4. Complete Inventory — Cosmic Duality (49 files)

| # | Run folder | File | Candidate | Pad | Size | First 16 bytes (hex) | H (bits/B) | B64 | Hex | Print | Flags |
|---:|---|---|---|---:|---:|---|---:|---:|---:|---:|---|
| 1 | `GSMG-CLEAN/runs/2026-11-27_fefefe_replay` | `outputs/cosmic_duality/0.bin` | `cicggifdcgaaggfbigaicfbh` | 1 | 1327 | `1df029eff52d6e4cc9d863a94e316787` | 7.8736 | 0.257 | 0.092 | 0.365 | none |
| 2 | `GSMG-CLEAN/runs/2026-11-27_fefefe_replay` | `outputs/cosmic_duality/1.bin` | `ihbegge` | 1 | 1327 | `e1823f13d6ffbb5884e9bc24d4fa11b3` | 7.8660 | 0.252 | 0.089 | 0.392 | none |
| 3 | `GSMG-CLEAN/runs/2026-11-27_lastwords_preamble_replay` | `outputs/cosmic_duality/cand_104.bin` | `1516594312197240916917121375895181314154313141242815419131218...` | 1 | 1327 | `c366c00b563fbd847dbbb517387ed549` | 7.8599 | 0.248 | 0.080 | 0.387 | none |
| 4 | `GSMG-CLEAN/runs/2026-11-27_lastwords_preamble_replay` | `outputs/cosmic_duality/cand_18.bin` | `... am I here? Wake up, you... I've designed you a beautiful ...` | 1 | 1327 | `397d97c1f1b9210934ae871042362e3c` | 7.8799 | 0.255 | 0.090 | 0.383 | none |
| 5 | `GSMG-CLEAN/runs/2026-11-27_lastwords_preamble_replay` | `outputs/cosmic_duality/cand_24.bin` | `... am I here? Wake up, you... I've designed you a beautiful ...` | 1 | 1327 | `1fb2d1a76cadbd91ba1ff533dc411bc3` | 7.8431 | 0.243 | 0.093 | 0.368 | none |
| 6 | `GSMG-CLEAN/runs/2026-11-27_lastwords_preamble_replay` | `outputs/cosmic_duality/cand_272.bin` | `AMIHEREWAKEUPYOUIVEDESIGNEDYOUABEAUTIFULSTRATEGICPOSITIONONEF...` | 1 | 1327 | `9ad8ee90377de5ee0436e7d160a1976c` | 7.8422 | 0.252 | 0.083 | 0.378 | none |
| 7 | `GSMG-CLEAN/runs/2026-11-27_lastwords_preamble_replay` | `outputs/cosmic_duality/cand_586.bin` | `yinyang479...amIhere?Wakeup,you...I'vedesignedyouabeautifulst...` | 1 | 1327 | `fb1733c0f6383075a16dd155c117a9af` | 7.8436 | 0.249 | 0.086 | 0.382 | none |
| 8 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/0.bin` | `PATGNH` | 1 | 1327 | `b3e6b96256ec3c8bc1fc2f09138409fc` | 7.8226 | 0.264 | 0.095 | 0.390 | none |
| 9 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/1.bin` | `NOOANNMEFIENN` | 1 | 1327 | `25ec2fc9909d35e31dc1db757e286d5d` | 7.8538 | 0.260 | 0.085 | 0.392 | none |
| 10 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/10.bin` | `hillfexmgsgq` | 1 | 1327 | `3e6d79ef5e1a6231dc18af2da9cca296` | 7.8373 | 0.263 | 0.095 | 0.385 | none |
| 11 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/11.bin` | `KXDECJQ` | 1 | 1327 | `f4add17b4d6f4c5f13b6648a7a154aab` | 7.8651 | 0.258 | 0.090 | 0.378 | none |
| 12 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/12.bin` | `rnkafarbhatfa` | 1 | 1327 | `63615507c4b220062c50e82232d0471e` | 7.8414 | 0.235 | 0.074 | 0.372 | none |
| 13 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/13.bin` | `HALIDLFINHJPI` | 1 | 1327 | `a9459a2a642c95199edc765e5a383c99` | 7.8592 | 0.229 | 0.073 | 0.358 | none |
| 14 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/14.bin` | `qmjzezqagzne` | 1 | 1327 | `4f2f0a3bf2c5e378f722ac9effc1c422` | 7.8795 | 0.250 | 0.092 | 0.380 | none |
| 15 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/15.bin` | `BJQWZJM` | 1 | 1327 | `133f652964e6c511f7d952eb85f50557` | 7.8695 | 0.235 | 0.074 | 0.372 | none |
| 16 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/16.bin` | `life an of eventuality anomaly to what` | 1 | 1327 | `928a6bef1534171da8d3c99cb906d68a` | 7.8470 | 0.255 | 0.080 | 0.384 | none |
| 17 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/17.bin` | `notityourlastafterneverthelessburden` | 1 | 1327 | `2522e394389c2a770910faf9c55c403e` | 7.8445 | 0.251 | 0.083 | 0.384 | none |
| 18 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/18.bin` | `andyouharmonytoofitnot` | 1 | 1327 | `f2c9da20959b9c0eddf8acde5ab49a53` | 7.8534 | 0.254 | 0.075 | 0.388 | none |
| 19 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/19.bin` | `otherwiseunexpectedcompletethat'sthisayou` | 1 | 1327 | `28a75b79dba1594f471dc1a7893643a6` | 7.8585 | 0.262 | 0.087 | 0.400 | none |
| 20 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/2.bin` | `ATGGGGGGGGGGGGG` | 1 | 1327 | `3571a5c4f5ea6dcc66d8fb2291f58115` | 7.8681 | 0.258 | 0.090 | 0.384 | none |
| 21 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/20.bin` | `REMAINDEROFEVENTUALITYEFFORTSISITWHICHYOUMEWASFINDTAKETHE` | 1 | 1327 | `c29a6fcbcaa0084640e6a2f5fb5f3fcc` | 7.8410 | 0.246 | 0.089 | 0.375 | none |
| 22 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/21.bin` | `life life life life life life a a a a an an of of of of you y...` | 1 | 1327 | `3134ab6e753d9e59c8ec4706a09858b7` | 7.8442 | 0.262 | 0.092 | 0.387 | none |
| 23 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/22.bin` | `ISEQUATIONEQUATIONTHEMYISISISISISISISISISISISISISISISISISISIS...` | 1 | 1327 | `5a73e92bf04b9961b49ea1fdc8d1cdc2` | 7.8565 | 0.265 | 0.102 | 0.391 | none |
| 24 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/23.bin` | `despitetoareianomalyyouwhatbeensincerestwhichofofthiswhichide...` | 1 | 1327 | `583c90668c072eae591b0b4f77694055` | 7.8627 | 0.250 | 0.082 | 0.369 | none |
| 25 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/24.bin` | `guysinvestmentainsteadyourof` | 1 | 1327 | `592ea67b79a1c1f519be2b2348e199f1` | 7.8629 | 0.268 | 0.093 | 0.402 | none |
| 26 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/25.bin` | `YOUR PROGRAMMING HARMONY AND ME EARNED EARNED WORTH TO TO WAI...` | 1 | 1327 | `3bd7e5542c7c3195ab4d4e438f922cd8` | 7.8519 | 0.259 | 0.093 | 0.405 | none |
| 27 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/26.bin` | `EVENTUALITYTHUSHEREMYWHILEBYQUESTIONUNBALANCED` | 1 | 1327 | `a0660c7126570785448d85302529ff6c` | 7.8537 | 0.243 | 0.077 | 0.370 | none |
| 28 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/27.bin` | `OWUFHSUUNOOUGEY` | 1 | 1327 | `77176d5974ac61e32c415dd075fa32a9` | 7.8779 | 0.257 | 0.081 | 0.398 | none |
| 29 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/28.bin` | `eoenlooeh` | 1 | 1327 | `94829d3c28f9e777c0ff2e04a8b05b75` | 7.8518 | 0.255 | 0.076 | 0.396 | none |
| 30 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/29.bin` | `EOOTXGN` | 1 | 1327 | `39d05e95c63777fce82f9b90aade9d87` | 7.8657 | 0.232 | 0.082 | 0.373 | none |
| 31 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/3.bin` | `OUMUEECBARNUARUONNN` | 1 | 1327 | `ec0852461f6924bfa40e88fb2c643ac8` | 7.8552 | 0.243 | 0.074 | 0.372 | none |
| 32 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/30.bin` | `ETEAIAT` | 1 | 1327 | `7cdc0a54bdeb717e1ed63e52ef9941e7` | 7.8402 | 0.269 | 0.081 | 0.390 | none |
| 33 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/31.bin` | `ATOTTTTTTTTTTTTTTTT` | 1 | 1327 | `b533183f86916bae2f43bc2e39436a25` | 7.8454 | 0.269 | 0.100 | 0.387 | none |
| 34 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/32.bin` | `ttttttttttttttttttttttttttttttttneooyh` | 1 | 1327 | `f9c5b94695ac0111338b9d039de8a07a` | 7.8527 | 0.252 | 0.089 | 0.388 | none |
| 35 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/33.bin` | `dsfloloucyloshw` | 1 | 1327 | `9ea357ccccdae0a6289940cea5ecf447` | 7.8681 | 0.264 | 0.092 | 0.385 | none |
| 36 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/34.bin` | `NOACAEIEIYMTDT` | 1 | 1327 | `10469978a8659f42314cbf12ce98375d` | 7.8681 | 0.248 | 0.093 | 0.374 | none |
| 37 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/35.bin` | `NEOAMIVEIVEIVEIVEIVETHEALTEREDSOMEANSWERSANSWERSANSWERS` | 1 | 1327 | `e8840c2fd3fbdc4dd66df36b6a13b971` | 7.8465 | 0.277 | 0.094 | 0.420 | none |
| 38 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/36.bin` | `EXPLANATIONSISAMWHICHYOUR` | 1 | 1327 | `fa98b592064d2e03a35a3aa530162308` | 7.8394 | 0.277 | 0.107 | 0.405 | none |
| 39 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/37.bin` | `youifirstpertinentnotmostthe` | 1 | 1327 | `3318110e128ae6338b38e327bcd33234` | 7.8511 | 0.255 | 0.083 | 0.374 | none |
| 40 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/38.bin` | `understandfirstofismytheyourconcordantlyorwhy` | 1 | 1327 | `d8f7b1cd56e6870e036a4094fc5944f5` | 7.8710 | 0.245 | 0.092 | 0.378 | none |
| 41 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/39.bin` | `YOUTHEI’VEMATRIXHASHELLOFORAMHAVEWAITINGANDI` | 1 | 1327 | `ffc9e5eea0aa3c3081864d9868ae091c` | 7.8375 | 0.255 | 0.084 | 0.375 | none |
| 42 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/4.bin` | `OEAAHEHTOZ` | 1 | 1327 | `f719d586b2a314ec4439fa8d5a3b7960` | 7.8647 | 0.255 | 0.081 | 0.389 | none |
| 43 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/40.bin` | `created human concordantly most of has of which gathering a n...` | 1 | 1327 | `a9f0f66a0e7af84f4d0b1fd818f54b64` | 7.8553 | 0.253 | 0.083 | 0.375 | none |
| 44 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/5.bin` | `oguunar` | 1 | 1327 | `9e45616a56b24b3b380a243073147f39` | 7.8583 | 0.261 | 0.087 | 0.403 | none |
| 45 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/6.bin` | `MUMLOIOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO` | 1 | 1327 | `9a1237ec71f03706193f0b0b00b12f73` | 7.8458 | 0.255 | 0.075 | 0.396 | none |
| 46 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/7.bin` | `UHUOCCCCCCCCCCCCCCCCCCCCCCCCCC` | 1 | 1327 | `9e4e48afc71fb2e4c8867dd2b56aab8a` | 7.8687 | 0.255 | 0.081 | 0.372 | none |
| 47 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/8.bin` | `uiust` | 1 | 1327 | `51bd06ebb47510065113c3e8f59148a9` | 7.8747 | 0.245 | 0.079 | 0.361 | none |
| 48 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/cosmic_duality/9.bin` | `ISUUASNUOROEUY` | 1 | 1327 | `acac8f754de8149b18fd3fa0452d4db8` | 7.8620 | 0.257 | 0.087 | 0.382 | none |
| 49 | `puzle/gsmgio-5btc-puzzle-master/artifacts/bin` | `cosmic_plaintext.bin` | `<raw 32B salphaseion_seven_digest_xor: a795de117e472590e572dc...` | 1 | 1327 | `44d19415009a2929a83b2f4e0da7b180` | 7.8702 | 0.265 | 0.089 | 0.402 | none |

## 5. Complete Inventory — SalPhaseIon Short (48 files)

| # | Run folder | File | Candidate | Pad | Size | First 16 bytes (hex) | H (bits/B) | B64 | Hex | Print | Flags |
|---:|---|---|---|---:|---:|---|---:|---:|---:|---:|---|
| 1 | `GSMG-CLEAN/runs/2026-11-27_fefefe_replay` | `outputs/salphaseion_short/0.bin` | `faedggeedfcbdabhhggca` | 1 | 79 | `0d9a4f3887a2959c18db4bbc331e1d58` | 6.0759 | 0.367 | 0.165 | 0.430 | none |
| 2 | `GSMG-CLEAN/runs/2026-11-27_lastwords_preamble_replay` | `outputs/salphaseion_short/cand_38.bin` | `... am i here? wake up, you... i've designed you a beautiful ...` | 1 | 79 | `73bfebbbf5285a8ac1d8123ec07a3358` | 6.1266 | 0.253 | 0.063 | 0.380 | none |
| 3 | `GSMG-CLEAN/runs/2026-11-27_lastwords_preamble_replay` | `outputs/salphaseion_short/cand_481.bin` | `verylaststepisatruegiveawaypromised15165943121972409169171213...` | 1 | 79 | `59871d757a3791e838de7ec7e9071ea4` | 6.0506 | 0.215 | 0.038 | 0.354 | none |
| 4 | `GSMG-CLEAN/runs/2026-11-27_lastwords_preamble_replay` | `outputs/salphaseion_short/cand_564.bin` | `yinyang... am i here? wake up, you... i've designed you a bea...` | 1 | 79 | `15a09730b9ead11092c56267ce172942` | 6.0917 | 0.228 | 0.063 | 0.342 | none |
| 5 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/0.bin` | `nipnnai` | 1 | 79 | `2ad58d5fa8ad3f9b33a72ff07b4480d4` | 6.0759 | 0.291 | 0.114 | 0.430 | none |
| 6 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/1.bin` | `ueuuuuudolccc` | 1 | 79 | `0f5fc61419261a7f7bcd07c89fd3dbd6` | 5.9556 | 0.165 | 0.089 | 0.354 | none |
| 7 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/10.bin` | `TNTNNXNINX` | 1 | 79 | `8b2e8b5d6e6d22a5e5581b49e762414f` | 6.0000 | 0.342 | 0.076 | 0.506 | none |
| 8 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/11.bin` | `IZ` | 1 | 79 | `994a99a82b22399192da33779cf111b4` | 6.0411 | 0.304 | 0.051 | 0.405 | none |
| 9 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/12.bin` | `by you please above efforts remains of` | 1 | 79 | `88226c1b69588a7d82eb74c53f16837c` | 6.0506 | 0.291 | 0.101 | 0.430 | none |
| 10 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/13.bin` | `PUZZLE EVENTUALITY ANOMALY HARMONY DESPITE DESPITE EVENTUALIT...` | 1 | 79 | `5765dbf408c5854c858305749b2279be` | 6.0315 | 0.241 | 0.025 | 0.380 | none |
| 11 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/14.bin` | `AAREOFSEDULOUSLYITWHATTHIS` | 1 | 79 | `a4dbf5aee9a749593d3dd16d042dbe42` | 6.1519 | 0.354 | 0.139 | 0.430 | none |
| 12 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/15.bin` | `FROMHAVEEVENTUALITYEFFORTSIEVENTUALITYTHEHAVEOFELIMINATEUNABL...` | 1 | 79 | `1f91c7849d5ae3d3a758818f4b96f1c6` | 6.0759 | 0.215 | 0.051 | 0.367 | none |
| 13 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/16.bin` | `MY THE HERE MY RESPONSES` | 1 | 79 | `6d079df6fdfd9cf090ba568b0e68377b` | 5.9651 | 0.203 | 0.025 | 0.304 | none |
| 14 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/17.bin` | `despitefromaeliminateofhavethebeenunablewhatanomalyhavefrom` | 1 | 79 | `30d3681575c1a212cdc56efd6d61fa9f` | 5.9049 | 0.278 | 0.076 | 0.354 | none |
| 15 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/18.bin` | `ITWISEMANWELLBASICSWILLPOWERDESPITEPLEASE` | 1 | 79 | `224c6861208f7cd8ef7c4797fd965c73` | 6.0759 | 0.316 | 0.051 | 0.481 | none |
| 16 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/19.bin` | `eventualitywhatthiswhichyoudespiteofofprogrammingwhichianomal...` | 1 | 79 | `28a2764073218dccbd61301042cbc163` | 6.1012 | 0.203 | 0.101 | 0.316 | none |
| 17 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/2.bin` | `DDAAEOFEEQEOH` | 1 | 79 | `495ccee160de842627ebc5679c7ffa5b` | 5.9460 | 0.190 | 0.025 | 0.304 | none |
| 18 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/20.bin` | `eliminateremainderequationisof` | 1 | 79 | `35f38f93d508f2740a3e3c7303f2d440` | 6.0000 | 0.278 | 0.089 | 0.405 | none |
| 19 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/21.bin` | `exceedinglymetowillheretothat'sreallyyou'llandthelifetimeburd...` | 1 | 79 | `928fdd2274a4f50a76ff3e0535579ec5` | 5.9747 | 0.278 | 0.076 | 0.418 | none |
| 20 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/22.bin` | `a mathematical of a avoid avoid is a of while of harmony to u...` | 1 | 79 | `1da3b5aebc98924dd24017ec80619186` | 6.0157 | 0.266 | 0.101 | 0.380 | none |
| 21 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/23.bin` | `the it last worth sorry bullshit exceedingly code find your y...` | 1 | 79 | `46eb11e66d8a31e4e2f1f2d0d0139a53` | 6.2025 | 0.228 | 0.076 | 0.342 | none |
| 22 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/24.bin` | `pleaseofanheartrequiredprecisionyouinthat'stothehavesincerest...` | 1 | 79 | `b740cc5c7b344c6f0107c178d728cdd0` | 5.8605 | 0.304 | 0.089 | 0.443 | none |
| 23 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/25.bin` | `youriinyoutheresultthissayofthat` | 1 | 79 | `2c6ec040479efb5adc14c968835e033f` | 6.1266 | 0.266 | 0.076 | 0.380 | none |
| 24 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/26.bin` | `IVREHXI` | 1 | 79 | `ae907578ee4fc8f1519903c46e420b8f` | 5.9493 | 0.304 | 0.089 | 0.405 | none |
| 25 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/27.bin` | `eeettvv` | 1 | 79 | `02d51f17d5b0f2cd928392718c8dd4b8` | 6.0917 | 0.241 | 0.063 | 0.316 | none |
| 26 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/28.bin` | `URETCAEBITAE` | 1 | 79 | `30e750f47f504bda35eedf7ee6fac3c2` | 5.7941 | 0.266 | 0.089 | 0.367 | none |
| 27 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/29.bin` | `ucssiihhhhii` | 1 | 79 | `4a8638356c51b283fd898f0d309200d1` | 6.1266 | 0.342 | 0.127 | 0.418 | none |
| 28 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/3.bin` | `yuiyeyiyyyyyluyyiyeyyyyyyfyyyyeyyyyyoyyyeyoyyyyyyyyylyyyy` | 1 | 79 | `a7576b413ce0c2dc55b11431356cc09f` | 5.8954 | 0.278 | 0.114 | 0.418 | none |
| 29 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/30.bin` | `HCUSTMIINITA` | 1 | 79 | `b548ab094e0cca552bf954d1c8a7a97b` | 5.9904 | 0.291 | 0.101 | 0.456 | none |
| 30 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/31.bin` | `eaurrmo` | 1 | 79 | `db8e4261bf5afbdeffa5f81c98056760` | 6.0157 | 0.278 | 0.139 | 0.367 | none |
| 31 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/32.bin` | `NTTEVSTANLAUSHSAEYUAUTENIGAOUE` | 1 | 79 | `a35d0dc57952e4ef75ff84577cd7b475` | 6.0664 | 0.278 | 0.051 | 0.380 | none |
| 32 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/33.bin` | `YOUUNDERSTANDALSOTOOFKNOWSIXTHGATHERINGQUITEINAGAINANSWERTHE` | 1 | 79 | `d4272d391878aa03c3b52f4bba2de5bf` | 5.9747 | 0.253 | 0.076 | 0.481 | none |
| 33 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/34.bin` | `neoamamiveiveyouyouyouyouyouyouandthethetheirrevocablyirrevoc...` | 1 | 79 | `8504bf2ee745374d8dccb70d8fa4d7e4` | 6.0759 | 0.278 | 0.114 | 0.392 | none |
| 34 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/35.bin` | `been the` | 1 | 79 | `d3449a7b9bc57f8c67fc6e91892f8086` | 6.0664 | 0.203 | 0.089 | 0.304 | none |
| 35 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/36.bin` | `ELUDEDFAILUREMINDPARAMETERSANOTHERPARAMETERSFAILUREUNDERSTAND...` | 1 | 79 | `6f9167c7715668761127362880dfcd37` | 6.0917 | 0.329 | 0.139 | 0.430 | none |
| 36 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/37.bin` | `OF THAN QUESTION THUS COUNTING QUESTION WHICH THIS ONE THAN T...` | 1 | 79 | `ce88c61bbc07c294f66b6f7fbf6eb787` | 6.0917 | 0.241 | 0.051 | 0.354 | none |
| 37 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/38.bin` | `concordantly you of the art again father near of it matrix ra...` | 1 | 79 | `16a42694ca5ef441dbf53e9829df7254` | 6.0506 | 0.291 | 0.152 | 0.456 | none |
| 38 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/39.bin` | `amunbalancedampertinentmostammayyoumaymay` | 1 | 79 | `b45fefa6eea3da85828d4bfbe54b4337` | 6.0411 | 0.253 | 0.089 | 0.342 | none |
| 39 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/4.bin` | `YSYAMYTMQAYYYI` | 1 | 79 | `931c68b374965bf359f656a3f29c706e` | 6.1772 | 0.278 | 0.038 | 0.430 | none |
| 40 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/40.bin` | `created the was you your am may and` | 1 | 79 | `da58a5c17974e442b5ad8d181925fa79` | 6.0062 | 0.215 | 0.038 | 0.342 | none |
| 41 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/5.bin` | `hmesaittvtru` | 1 | 79 | `5c1402d7d5358a775c19703edc236f0e` | 6.0664 | 0.203 | 0.076 | 0.316 | none |
| 42 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/6.bin` | `NERLDROQFENFE` | 1 | 79 | `8658e6127b30709c5d318fa0c4161f60` | 6.0506 | 0.241 | 0.101 | 0.380 | none |
| 43 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/7.bin` | `TETALTRLTCUTT` | 1 | 79 | `02f83a3bf8bb2191611b7358ed19c48b` | 5.8954 | 0.329 | 0.089 | 0.430 | none |
| 44 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/8.bin` | `IOEIEEE` | 1 | 79 | `86a80348ca3ec21147a5b1e54f4e99b0` | 5.9145 | 0.266 | 0.013 | 0.354 | none |
| 45 | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay` | `outputs/salphaseion_short/9.bin` | `hun` | 1 | 79 | `a9cabb466d8a8ccb576becb05cd9a4d4` | 6.1266 | 0.241 | 0.076 | 0.367 | none |
| 46 | `GSMG-CLEAN/runs/2026-11-27_review_candidates` | `outputs/salphaseion_short/cand_20.bin` | `X2SH4Y0QB15` | 1 | 79 | `4fc850496de1d796a722c0f1bf2ea4a8` | 6.0157 | 0.215 | 0.089 | 0.418 | none |
| 47 | `GSMG-CLEAN/runs/2026-09-14_adversarial_reanalysis/exp2_first_hint_last_command` | `outputs/00019_F1_raw_sha256_locked_salphaseion_short.bin` | `follow the white rabbit [rep=raw, kdf=sha256]` | 1 | 79 | `7efb61e841f5f3806c29207a0678cfa2` | 6.0411 | 0.241 | 0.051 | 0.367 | none |
| 48 | `puzle/gsmgio-5btc-puzzle-master/artifacts/bin` | `chain1_plaintext.bin` | `matrixsumlistenterlastwordsbeforearchichoicethispasswordmatri...` | 1 | 79 | `9fa9db91a9dee0e38b93694ec874630b` | 6.1266 | 0.316 | 0.152 | 0.392 | none |

## 6. Excluded `.bin` Directories Audited

Every other `.bin` file in the repository was checked and classified as out of scope:

| Path | `.bin` count | Reason excluded |
|---|---:|---|
| `GSMG-CLEAN/runs/2026-11-27_fefefe_replay/controls` | 2 | synthetic planted control outputs (not puzzle envelopes) |
| `GSMG-CLEAN/runs/2026-11-27_fresh_eyes_candidates/controls` | 2 | synthetic planted control outputs (not puzzle envelopes) |
| `GSMG-CLEAN/runs/2026-11-27_lastwords_preamble_replay/outputs/terminal_phase3_2_end` | 1 | terminal_phase3_2_end envelope (out of scope) |
| `GSMG-CLEAN/runs/2026-11-27_lastwords_preamble_replay/controls` | 2 | synthetic planted control outputs (not puzzle envelopes) |
| `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay/outputs/terminal_phase3_2_end` | 29 | terminal_phase3_2_end envelope (out of scope) |
| `GSMG-CLEAN/runs/2026-11-27_review_candidates/controls` | 1 | synthetic planted control outputs (not puzzle envelopes) |
| `GSMG-CLEAN/runs/2026-09-14_adversarial_reanalysis/exp2_first_hint_last_command/outputs` | 899 | 599 non-pad-valid raw decrypts (cosmic_duality/salphaseion_short) + 300 terminal_phase3_2_end raw decrypts |
| `GSMG-CLEAN/runs/2026-09-14_payload60_matrixsum/direct_integer.bin` | 1 | 25-byte direct integer encoding, not an envelope plaintext |
| `puzle/gsmgio-5btc-puzzle-master/artifacts/bin` | 134 | padded duplicates (cosmic_padded_plaintext.bin, chain1_padded_plaintext.bin), envelopes, keys/IVs/salts, chain2 (terminal), chain4, solved phase3.2, and JSON audit dumps |
| `grok-gsmg-puzzle/artifacts` | 7 | locked ciphertext envelopes, masks, and solved phase32 artifacts |
| `GSMG-CLEAN/data` | 6 | locked ciphertext envelopes and solved Phase 2/3/3.2 plaintexts |
| `gsmg-haiku/derived` | 1 | solved phase3.2 plaintext and quadgram table |
| `gsmg-haiku/review_leads/cryptanalysis_2026_10_15` | 1 | solved phase3.2 plaintext and quadgram table |
| `gsmg-haiku/review_leads/cryptanalysis_2026_10_15/inputs` | 1 | solved phase3.2 plaintext and quadgram table |
| `puzle/gsmgio-5btc-puzzle-master/artifacts/blockchain_cache/raw_txs` | 204 | cached raw Bitcoin transactions, sighash preimages, and Wayback bodies |
| `puzle/gsmgio-5btc-puzzle-master/artifacts/blockchain_cache/sighash_preimages` | 187 | cached raw Bitcoin transactions, sighash preimages, and Wayback bodies |
| `puzle/gsmgio-5btc-puzzle-master/artifacts/wayback_cache/bodies` | 124 | cached raw Bitcoin transactions, sighash preimages, and Wayback bodies |

## 7. Files in This Run

| File | Description |
|---|---|
| `scan.py` | Read-only scanner and deterministic report generator (0 AES/decrypt calls) |
| `results.json` | Full machine-readable per-file metrics, flags, self-test, and excluded-file audit |
| `REPORT.md` | This report |
