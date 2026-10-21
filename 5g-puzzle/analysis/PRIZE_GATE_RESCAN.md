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

- `packet/run_packet.py`, `run_kdf_audit.py`, `run_140_length.py`, `run_fefefe_read.py` (and `run_architect_delta.py`, which imports from `run_kdf_audit`) compared candidates with **Half's uncompressed public key only**, over at most four windows (`pt32`, `sha256(pt)`, `pt[:32]`, `pt[-32:]`).
- Their `pubkey_uncompressed()` returned `None` whenever the `ecdsa` package was missing, so in that environment no candidate could ever match and the run still reported "0 prize hits".
- All of them now call `tools/prize_gate.py`: both targets, both serializations, every window and every text encoding. A planted Better Half key fires through each patched function.
- Consequence for the record: the "0 prize hits" of packets 1 to 4, the KDF audit, the Architect-delta, the 140-length and the FEFEFE packets were Half-only and limited to those four windows. Their decrypted `packet/out/*.bin` files are not committed, so this rescan cannot regate them; re-running the packets now does.

## Scope

- Files scanned: 122 (0 binary), 12.6 MB
- Unique scalars gated: 33,867 (duplicates across files gated once)
- Run time: 3 s with the `coincurve` backend

| Candidate kind | Count |
| --- | ---: |
| `hex64` | 20,891 |
| `b64blob/raw32` | 12,709 |
| `derived_sha256` | 120 |
| `derived_sha256_stripped` | 93 |
| `b64` | 17 |
| `dec` | 15 |
| `wif_compressed` | 8 |
| `wif_uncompressed` | 8 |
| `b64blob/hex64` | 4 |
| `mini` | 2 |

Files with the most candidates:

- `2025.txt`: 9,988
- `2026.txt`: 6,460
- `2024.txt`: 6,026
- `2023.txt`: 3,370
- `packet/out/results_140_length.json`: 2,271
- `reddit1.txt`: 1,219
- `packet/out/results_fefefe_read.json`: 1,182
- `analysis/cosmic_blob.txt`: 838
- `analysis/phase32_blob.txt`: 563
- `2021.txt`: 465

## Not covered

- Media and archives, skipped by extension: 1 `.pdf`, 12 `.png`.
- Raw 32-byte windows are taken only over binary files; text files get the text parsers.
- Outputs that were never committed (for example gitignored run directories) cannot be rescanned.

## Reproduce

```
pip install coincurve            # optional, about 18,000 scalars per second
python3 tools/prize_gate.py selftest
python3 tools/prize_gate.py scan . --json /tmp/rescan.json
```

The compact summary is `analysis/prize_gate_rescan.json`.
