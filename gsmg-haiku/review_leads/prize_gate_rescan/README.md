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

- `review_leads/cryptanalysis_2026_10_15/oracle_checks.py` and `free_rows.py` compared candidates with **Half's uncompressed public key only**. They now call `tools/prize_gate.py`.
- `mywork/lib.py` `TARGET` held Half's two hash160 forms but not Better Half's; added.
- `work/btc_check.py` `check_private_key_for_target()` checked Half only; it now calls the shared gate first.
- `python3 -m pytest -q tests`: 15 passed before and after. A planted Better Half key fires through `lib.check_key` and `btc_check`.
- Consequence for the record: the scalar checks recorded by `oracle_checks.py` and `free_rows.py` were Half-only. Their stored JSON outputs in `review_leads/cryptanalysis_2026_10_15/` are covered by this rescan.

## Scope

- Files scanned: 331 (3 binary), 70.5 MB
- Unique scalars gated: 18,034,798 (duplicates across files gated once)
- Run time: 1,040 s with the `coincurve` backend

| Candidate kind | Count |
| --- | ---: |
| `hex64` | 17,290,570 |
| `raw32` | 651,859 |
| `b64blob/raw32` | 80,380 |
| `dec` | 6,871 |
| `hexblob/dec` | 4,251 |
| `derived_sha256` | 270 |
| `derived_sha256_stripped` | 269 |
| `hexblob/b64` | 242 |
| `b64` | 45 |
| `hexblob/mini` | 18 |
| `wif_compressed` | 8 |
| `wif_uncompressed` | 8 |
| `b64blob/hex64` | 4 |
| `mini` | 3 |

Files with the most candidates:

- `review_leads/mapping_boards/boards/padding.jsonl`: 9,126,589
- `review_leads/hash_scope/padding.jsonl`: 2,231,428
- `review_leads/double_cbc/padding.jsonl`: 1,475,968
- `review_leads/genesis_slices/padding.jsonl`: 1,457,585
- `review_leads/mapping_boards/digit-map/padding.jsonl`: 1,353,006
- `review_leads/cryptanalysis_2026_10_15/quadgrams.bin`: 650,785
- `review_leads/hash_scope/followup-padding.jsonl`: 504,479
- `review_leads/binary_envelopes/padding.jsonl`: 427,355
- `review_leads/numeric-key-padding.jsonl`: 358,344
- `review_leads/weighted-primes-padding.jsonl`: 81,376

## Not covered

- Media and archives, skipped by extension: 46 `.png`.
- Raw 32-byte windows are taken only over binary files; text files get the text parsers.
- Outputs that were never committed (for example gitignored run directories) cannot be rescanned.

## Reproduce

```
pip install coincurve            # optional, about 18,000 scalars per second
python3 tools/prize_gate.py selftest
python3 tools/prize_gate.py scan . --json /tmp/rescan.json
```

The compact summary is `review_leads/prize_gate_rescan/summary.json`.
