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

- This repository has no gate code of its own. The shared checker is added as `tools/prize_gate.py`.

## Scope

- Files scanned: 13 (0 binary), 33.4 MB
- Unique scalars gated: 27,987 (duplicates across files gated once)
- Run time: 5 s with the `coincurve` backend

| Candidate kind | Count |
| --- | ---: |
| `hex64` | 18,223 |
| `b64blob/raw32` | 9,675 |
| `b64` | 26 |
| `dec` | 16 |
| `derived_sha256` | 13 |
| `derived_sha256_stripped` | 12 |
| `wif_compressed` | 8 |
| `wif_uncompressed` | 8 |
| `b64blob/hex64` | 4 |
| `mini` | 2 |

Files with the most candidates:

- `gsmg-group-telegram-by-year/2025.json`: 8,100
- `gsmg-group-telegram-by-year/2026.json`: 6,455
- `gsmg-group-telegram-by-year/2024.json`: 5,780
- `gsmg-group-telegram-by-year/2023.json`: 3,524
- `GSMG-PUZZLE-DOSSIER.md`: 2,099
- `source/pages/phase2_choice.html`: 1,652
- `source/pages/salphaseion_phase3.html`: 236
- `gsmg-group-telegram-by-year/2020.json`: 88
- `gsmg-group-telegram-by-year/2021.json`: 46
- `gsmg-group-telegram-by-year/2019.json`: 2

## Not covered

- Media and archives, skipped by extension: 10 `.png`.
- Raw 32-byte windows are taken only over binary files; text files get the text parsers.
- Outputs that were never committed (for example gitignored run directories) cannot be rescanned.

## Reproduce

```
pip install coincurve            # optional, about 18,000 scalars per second
python3 tools/prize_gate.py selftest
python3 tools/prize_gate.py scan . --json /tmp/rescan.json
```

The compact summary is `tools/prize_gate_rescan.json`.
