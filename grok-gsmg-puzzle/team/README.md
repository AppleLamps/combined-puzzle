# Team batteries

Preregistered null-hypothesis decrypt grids. Each runner calls `planted_control()` before counting results.

| Script | Ledger | Output |
|--------|--------|--------|
| `cryptanalyst_tests.py` | — | Shared containers, §4.1 helpers, planted control |
| `classify_unified.py` | — | Structured-plaintext detector |
| `round2_battery.py` … `round7_chained_pipeline.py` | `ledger/08`–`14` | `artifacts/round*_*.json` |
| `round5_battery.py`, `round5_preregistered.py` | `ledger/12`, `ledger/round5/` | Round 5 pilot + M1–M5 |
| `round6_battery.py` | `ledger/13` | Reader top 5 |
| `round8_reader_gap.py` | `ledger/16` | G1–G7 (`preregister_reader_gap.json`) |
| `round9_reader_gap.py` | `ledger/17` | G8–G15 (`preregister_reader_gap9.json`) |
| `round10_phase3_g12.py` | `ledger/18` | Phase-3 part falsification |
| `round11_pipeline.py` | `ledger/19` | Sal `enter` join + Terminal-first + #8000 joint (`preregister_round11_pipeline.json`) |
| `round12_pipeline.py` | `ledger/20` | z-program + pre-decode b64 + liberal T→S→C (`preregister_round12_pipeline.json`) |
| `round13_pipeline.py` | `ledger/21` | Byte XOR enter + poster MSL + full Sal stage-0 (`preregister_round13_pipeline.json`) |
| `round14_clues.py` | `ledger/22` | Missed connections clue battery (`preregister_round14_clues.json`) |
| `deletion_sweep_faed.py` | `ledger/07` | MASK6 letter-deletion 2⁶ |
| `statistician_repro.py` | `ledger/04` | dbbi / host-bit null repro |
| `audit_rerun.py` | `ledger/23` | Re-runs any battery with every AES decrypt checked by the kit recogniser (`artifacts/audit_*.json`) |

Run from repo root: `python3 team/<script>.py`
