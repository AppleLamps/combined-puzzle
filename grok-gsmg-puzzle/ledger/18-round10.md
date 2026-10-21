# 18 — Round 10: methodology cleanup + G12 phase-3 parts

**Code:** `team/round10_phase3_g12.py` → `artifacts/round10_phase3_g12.json`  
**Control:** §4.1 `causality` **PASS**

## Methodology (audit R15 follow-up)

| Item | Change |
|------|--------|
| **dbbi host string** | `round2_battery.py`: target `BBBBYBBBYYBBBBYBBYYBFYY`; shuffle labeled simplified null |
| **`planted_control()`** | `round5_preregistered.py` at `main()` start (not only M1); `deletion_sweep_faed.py` uses shared helper |
| **§9 / experiments** | `uploads/GSMG-handoff.md` §9 footnote + `ledger/experiments.md` shuffle row |
| **`classify_unified`** | Already in R9; `cryptanalyst_tests` + round8 |

## G12 — seven-part phase 3

| Test | Result |
|------|--------|
| Canonical 7-part concat → phase 3 plaintext | **Matches** `artifacts/phase3.txt` (4090 B) |
| Alternates (5): lower Safenet, EO11110, genesis w/o `0x`, wrong FEN side, `Luna ` | **All diverge** from artifact |
| §4.1 on locked containers with alt/canonical passwords | **0** structured |

Alternates are **falsified** as equivalent readings of the solved chain; canonical tuple remains the only [V] reproducer in-repo.

## Result

Locked containers still **null**; upstream phase-3 tuple **confirmed** for handoff/archivist strings.
