# 23 - Detector audit of rounds 1-14

**Date:** 18 Oct 2026
**Code:** `team/audit_rerun.py` → `artifacts/audit_<script>.json`

## Why

Every battery decided "structured" with `step1_btcseed.classify`, either directly or through `classify_unified`. That detector needs about 90% printable text. On the phase 3.2 plaintext, the one solved output that is not prose, it returns `opaque p=0.60`. A 32-byte binary key also comes back `opaque`. So the nulls in rounds 1-14 only covered outcomes that look like English. The one planted control, phase 2 with `causality`, is prose, so it could not catch this.

Two more faults showed up when the batteries were re-run on the current code:

1. **False positives.** `classify` counted any body whose first byte is `{` as JSON. That happens for 1 in 256 valid-pad bodies. The current code reported 28 "structured" hits in round 4, 2 in round 3 (Terminal, filler pairs 25/35 and 26/35, which give one password) and 1 in round 7. All 31 were random bodies starting `0x7b`. The committed JSON showed 0 because it predates the round 9 detector change. Fixed: `{` and `-----` now also need at least 80% printable. After the fix all three rounds report 0 again.
2. **Stale counts.** Some committed JSON did not match the code next to it. Regenerated: round 7 went from 35,007 to 35,018 decrypts, round 13 from 1,025 to 1,162, round 12's gap split changed (G2 168 to 126, G3 1,550 to 1,592), and round 2 gained its host-string note. Round 8 had stopped reaching G6 and G7 inside its 2,000 budget, though ledger 16 lists both as tested. Its budget is now 2,200, so all of G1-G7 run (2,051 decrypts, 0 structured).

`artifacts/step3_summary.json` was left as committed. Its `interior_rate`, `chance_rate` and `g_beam` fields are not written by the `src/step3_mask.py` in this repo, so they come from code that was never committed.

## Method

`audit_rerun.py` wraps `Crypto.Cipher.AES.new` before it runs a battery, so every CBC decrypt the battery makes is recorded while the battery code stays unchanged. Each decrypt is matched to its container by ciphertext, then gets a PKCS#7 check and the gsmg-puzzle-kit `h3.c` recogniser: printable at least 0.80, any bit-position |z| of 6 or more, distinct-byte deficit z of -6 or less, UTF-16 zero alternation at least 0.6, nested `Salted__`, or file magic. Padding values of 3 or more are counted separately. The recogniser runs on the unpadded body of every valid pad, and on the full block output of every decrypt, which covers the "liberal" chains that skip the pad check.

Planted controls ran before any battery and both fired. The full phase 3.2 plaintext flags as `bitbias`, and a 64-byte slice of it encrypted under the Terminal salt with a random password flags as `printable` after decryption. 2,000 random 64-byte bodies gave 0 false flags. Each battery's own phase 2 control also went through the wrapper and was flagged.

## Result

Counts are AES calls on the three locked ciphertexts, including liberal scans and repeated passwords, so some run above the battery's own total.

| Script | Locked decrypts | Valid pads | Expected (N/255) | Pad ≥ 3 | Flagged bodies |
|---|---:|---:|---:|---:|---:|
| `team/cryptanalyst_tests.py` | 108 | 1 | 0.4 | 0 | 0 |
| `team/deletion_sweep_faed.py` | 576 | 3 | 2.3 | 0 | 0 |
| `team/round10_phase3_g12.py` | 63 | 0 | 0.2 | 0 | 0 |
| `team/round11_pipeline.py` | 500 | 5 | 2.0 | 0 | 0 |
| `team/round12_pipeline.py` | 1,964 | 4 | 7.7 | 0 | 0 |
| `team/round13_pipeline.py` | 1,127 | 6 | 4.4 | 0 | 0 |
| `team/round14_clues.py` | 1,634 | 7 | 6.4 | 0 | 0 |
| `team/round2_battery.py` | 960 | 6 | 3.8 | 0 | 0 |
| `team/round3_battery.py` | 16,082 | 56 | 63.1 | 0 | 0 |
| `team/round4_battery.py` | 1,671,724 | 6,558 | 6,555.8 | 0 | 0 |
| `team/round5_battery.py` | 15,754 | 68 | 61.8 | 0 | 0 |
| `team/round5_preregistered.py` | 280 | 3 | 1.1 | 0 | 0 |
| `team/round6_battery.py` | 460 | 3 | 1.8 | 0 | 0 |
| `team/round7_chained_pipeline.py` | 37,778 | 117 | 148.1 | 0 | 0 |
| `team/round8_reader_gap.py` | 2,051 | 6 | 8.0 | 0 | 0 |
| `team/round9_reader_gap.py` | 2,003 | 9 | 7.9 | 0 | 0 |
| `src/step1_btcseed.py` | 825 | 2 | 3.2 | 0 | 0 |
| `src/step3_mask.py` | 9,216 | 32 | 36.1 | 0 | 0 |
| **Total** | **1,763,105** | **6,886** | **6,914.1** | | **0** |

Valid pads match chance overall (6,886 against 6,914) and no body was flagged on any locked container. Round 7 sits low (117 against 148) because its liberal chains decrypt Terminal with many repeated passwords, which makes pad counts clump; a deficit is not a signal either way. The nulls in rounds 1-14 now hold for the phase 3.2 class of outcome too. They still cover only the candidate sets those rounds built, the AES-256-CBC with EVP conventions they used, and outcomes this recogniser can see.

## Wording

A null on a few password forms does not exclude a reading, because the open step takes two unknown operands. The result tables in ledgers 13, 14, 16 and 22 now say **Tested null** where they said **Falsified**. Ledger 18 keeps "falsified" for the phase 3 alternates, because that is a checked byte fact: they do not decrypt phase 3.
