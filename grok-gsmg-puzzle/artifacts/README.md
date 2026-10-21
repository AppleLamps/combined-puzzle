# Artifacts

Generated and checked outputs for offline GSMG cryptanalysis. Most files have a `.sha256` sidecar from `step0_trust.py`.

## Core chain (from handoff)

| Files | Role |
|-------|------|
| `phase2.txt`, `phase3.txt`, `phase32.bin` | Solved decrypt plaintexts |
| `phase32_beaufort.txt`, `phase32_checkerboard.txt` | Phase 3.2 interior decodings |
| `phase3_password.txt` | Seven-part phase-3 password (concat) |
| `terminal.bin`, `cosmic.bin`, `salphaseion_short.bin` | Locked containers (binary) |
| `*.b64` | Same blobs, base64 for OpenSSL-style tools |

## SalPhaseIon / poster

| Files | Role |
|-------|------|
| `faed.txt`, `dbbi.txt`, `salphaseion.txt` | Letter blocks |
| `faed_bifid.txt` | Full-period Bifid decrypt on canonical square |
| `matrix.json`, `poster_*.txt` | Bit grid and spiral encodings |
| `yellowblue_*.txt` | Prime-walk filler / colour streams |

## Batteries (team rounds)

`round2`–`round7` battery JSON, `round8`/`round9` reader-gap JSON, `round10_phase3_g12.json`, `round11_pipeline.json`–`round14_clues.json`, plus `deletion_sweep_faed.json`, `cryptanalyst_summary.json`, `tester_battery_report.json`, and `step0`–`step3` summaries. Specs live in `team/preregister_*.json`.

## Regenerable (not in git)

Recreated by pipeline scripts; listed in root `.gitignore`:

- `decode_*.bin` — `src/step1_btcseed.py`
- `attempts.jsonl`, `step2_attempts.jsonl`, `step3_attempts.jsonl` — per-step decrypt logs
- `peel_*.txt`, `mask6_deleted.bin`, `yellowblue_base9.bin`, `yellowblue_decimal.bin` — `step2_peel.py` / `step3_mask.py`
