# 2026-09-14_adversarial_reanalysis

- `REPORT.md` — evidence-status table, ranked mistakes, dependency map, three A–G explanations, experiments, final answer.
- `ERRATA.md` — corrections to earlier documents (originals untouched).
- `exp0_reproduction/` — independent reproduction of spiral / DBBI parses / marker strings / L1 / L2 (`repro_dbbi_parse.py`, `.json`).
- `exp1_address_oracle_rerun/` — valid hash160-set oracle over the 38,615 retained candidates; SPEC, controls, manifest, hits (none), voided v1 logs.
- `exp2_first_hint_last_command/` — validated AES harness (Phases 2/3/3.2 reproduced), 900 retained decrypts in `outputs/`, `results.jsonl.json`, `summary.json`, `run.log`.

Reproduce: run each experiment's script from its own directory with `python <script>.py`.
