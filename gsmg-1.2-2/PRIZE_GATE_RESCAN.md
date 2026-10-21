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

- `tools/gsmg_verify/lib.py` already computed Better Half (as `SENTINEL_H160`) under both forms, and `gsmg_solve/harness.py` reported it as a finding, but `win_raw()` and `win_from_answer()` returned true for Half only. They now count Better Half as a win. A planted key in the sentinel slot wins; a random key does not.
- Unrelated and pre-existing: `tools/gsmg_verify/verify_chain.py` stops with `KeyError: 1` while parsing the dossier's seven answer parts, on the branch as it was before this change too. Left as found.

## Scope

- Files scanned: 44 (0 binary), 33.6 MB
- Unique scalars gated: 28,990 (duplicates across files gated once)
- Run time: 4 s with the `coincurve` backend

| Candidate kind | Count |
| --- | ---: |
| `hex64` | 19,141 |
| `b64blob/raw32` | 9,698 |
| `derived_sha256` | 44 |
| `derived_sha256_stripped` | 43 |
| `b64` | 26 |
| `dec` | 16 |
| `wif_compressed` | 8 |
| `wif_uncompressed` | 8 |
| `b64blob/hex64` | 4 |
| `mini` | 2 |

Files with the most candidates:

- `gsmg-group-telegram-by-year/2025.json`: 8,100
- `gsmg-group-telegram-by-year/2026.json`: 6,454
- `gsmg-group-telegram-by-year/2024.json`: 5,780
- `gsmg-group-telegram-by-year/2023.json`: 3,524
- `GSMG-PUZZLE-DOSSIER.md`: 2,100
- `source/pages/phase2_choice.html`: 1,652
- `source/onchain/2aa9a4a90be819d5122d70c993280785a0508f163521e7b38cebb4db0b071b13.json`: 433
- `source/onchain/a798905f53fdcadcbd2e2a1e61d23ba69a07e26130a78c76da4bf4d7a170f383.json`: 245
- `source/pages/salphaseion_phase3.html`: 236
- `source/onchain/f28b0b68684b41c98c8c59f43558e2bfbe5aba30fef05fd7dc465dea62fbaed1.json`: 153

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
