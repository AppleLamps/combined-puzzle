# Prize-gate rescan of stored outputs (2026-10-21)

**Result: 0 prize matches.** Every candidate key that the shared checker can find in this
repository's committed files was gated against both prize targets under both public-key
serializations. This is a bounded negative over the files and encodings below, nothing more.

## The checker

`tools/prize_gate.py` (prize_gate 1.0.1, sha256 `9dfa1d2fb4769d57…`) is byte-identical across the
GSMG repositories. It gates:

- **Half** `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`: hash160 under both serializations, plus its on-chain public key;
- **Better Half** `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`: hash160 under both serializations (it has never spent).

Inside each file it parses raw 32-byte windows (binary files), every 64-character hex window, WIF
(compressed and uncompressed), mini keys, 32-byte base64 tokens, 60 to 78 digit decimals, sha256 of the
whole file, and hex or base64 blobs decoded and parsed once more. `python3 tools/prize_gate.py selftest`
plants a key in every one of those encodings, in both target slots and both serializations; all 55
checks passed before this scan ran.

## Gate defects fixed in this repository

- None found. `tools/check_candidate.py` already compares compressed and uncompressed hash160 with both Half and Better Half. The shared checker adds the plaintext parsers (hex, WIF, mini, base64, decimal) used for this rescan.

## Scope

- Files scanned: 1,379 (905 binary), 232.0 MB
- Unique scalars gated: 7,338,104 (duplicates across files gated once)
- Run time: 450 s with the `coincurve` backend

| Candidate kind | Count |
| --- | ---: |
| `hex64` | 6,728,335 |
| `raw32` | 415,300 |
| `b64blob/raw32` | 192,977 |
| `dec` | 576 |
| `derived_sha256` | 362 |
| `derived_sha256_stripped` | 296 |
| `b64` | 102 |
| `mini` | 96 |
| `hexblob/dec` | 37 |
| `wif_uncompressed` | 10 |
| `wif_compressed` | 8 |
| `b64blob/hex64` | 4 |
| `hexblob/wif_uncompressed` | 1 |

Files with the most candidates:

- `runs/2026-09-14_lossy_hill/passages.json`: 1,271,072
- `runs/2026-09-13_assumption_audit/all_padding_valid.jsonl`: 709,798
- `runs/2026-09-13_faed_constraints/required_keystreams.json`: 683,108
- `runs/2026-09-13_seven_key_bifid/candidates.json`: 665,408
- `runs/2026-09-13_seven_key_bifid/results.json`: 587,689
- `runs/2026-09-14_lossy_hill/control_pair_survivors.jsonl`: 526,316
- `runs/2026-09-13_salphaseion_roles/all_padding_valid.jsonl`: 504,322
- `runs/2026-09-13_prime_control_faed/outputs.json`: 436,205
- `runs/2026-09-13_zero_envelopes/arm_B_passwords.hex`: 357,672
- `runs/2026-09-14_lossy_hill/pair_survivors.jsonl`: 332,087

## Not covered

- Media and archives, skipped by extension: 1 `.exe`, 10 `.jpg`, 2 `.mp3`, 13 `.mp4`, 14 `.png`, 1 `.tgs`, 1 `.webp`.
- Raw 32-byte windows are taken only over binary files; text files get the text parsers.
- Outputs that were never committed (for example gitignored run directories) cannot be rescanned.

## Reproduce

```
pip install coincurve            # optional, about 18,000 scalars per second
python3 tools/prize_gate.py selftest
python3 tools/prize_gate.py scan . --json /tmp/rescan.json
```

The compact summary is `runs/2026-10-21_prize_gate_rescan/summary.json`.
