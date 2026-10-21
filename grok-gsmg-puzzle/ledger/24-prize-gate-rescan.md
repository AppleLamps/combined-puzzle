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

- `src/crypto_known.py` `is_win_uncompressed()`, which every battery and round script in `team/` calls, compared Half's uncompressed hash160 only. It now delegates to `tools/prize_gate.py` (both targets, both serializations); `is_win()` does the same. The old name is kept so the callers are unchanged.
- `src/step0_trust.py` still passes 49/49, and a planted Better Half key now wins through `is_win_uncompressed()`.
- Consequence for the record: every battery result in `ledger/` that reports 0 wins was a Half-only result. The batteries' decrypts were not stored, so they can only be regated by re-running them.

## Scope

- Files scanned: 165 (8 binary), 0.8 MB
- Unique scalars gated: 9,393 (duplicates across files gated once)
- Run time: 1 s with the `coincurve` backend

| Candidate kind | Count |
| --- | ---: |
| `b64blob/raw32` | 5,215 |
| `raw32` | 3,083 |
| `hex64` | 783 |
| `derived_sha256` | 162 |
| `derived_sha256_stripped` | 145 |
| `b64` | 2 |
| `b64blob/dec` | 1 |
| `dec` | 1 |
| `wif_compressed` | 1 |

Files with the most candidates:

- `uploads/GSMG-handoff.md`: 2,653
- `artifacts/phase32.bin`: 2,512
- `artifacts/cosmic.b64`: 1,315
- `artifacts/phase3.txt`: 868
- `artifacts/mask6.txt`: 322
- `artifacts/mask12.bin`: 206
- `artifacts/mask6.bin`: 167
- `ledger/01-archivist.md`: 141
- `src/check_report3_2026-10-17.py`: 137
- `artifacts/poster_spiral_bits.txt`: 135

## Not covered

- Media and archives, skipped by extension: 1 `.png`.
- Raw 32-byte windows are taken only over binary files; text files get the text parsers.
- Outputs that were never committed (for example gitignored run directories) cannot be rescanned.

## Reproduce

```
pip install coincurve            # optional, about 18,000 scalars per second
python3 tools/prize_gate.py selftest
python3 tools/prize_gate.py scan . --json /tmp/rescan.json
```

The compact summary is `ledger/24-prize-gate-rescan.json`.
