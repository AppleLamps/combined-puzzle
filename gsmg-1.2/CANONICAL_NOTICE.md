# Canonical ledger notice (2026-11-10)

This directory is a frozen snapshot of one research repository. The single source of truth for the
combined repository is [`GSMG-CLEAN/`](../GSMG-CLEAN/README.md). Where this directory and the
canonical ledger disagree, the ledger stands. The full table of disagreements, with the evidence, is
[`GSMG-CLEAN/16_CANONICAL_LEDGER_AND_WORKING_RULES_2026-11-10.md`](../GSMG-CLEAN/16_CANONICAL_LEDGER_AND_WORKING_RULES_2026-11-10.md).

The puzzle is unsolved. Nothing in this notice opens an envelope.

## Working rules that now apply here too

1. No envelope sweeps. Do not run this directory's AES harnesses or batteries. A password is tried
   only through `GSMG-CLEAN/tools/check_candidate.py --derivation runs/<dir>`, and only after that
   derivation checked itself without AES.
2. Every new experiment states the second artifact it predicts (readable text, an authenticated
   digest, a marker or prize address, or an exact reconstruction) before it generates candidates:
   `GSMG-CLEAN/tools/prereg.py`.
3. A null counts only when its planted control fired.
4. New findings are recorded in `GSMG-CLEAN/`, not here.

## Statements in this directory that the canonical ledger contradicts or qualifies

| Here | Statement | Canonical position |
|---|---|---|
| `GSMG-PUZZLE-DOSSIER.md:996` | "Open by size alone: faed with arbitrary `g` choices (2^107, not enumerable)" | **Closed as text.** The last 32 letters of FAED contain no `g`, and the low four bytes of the integer depend only on the last 32 digits, so they are `c7 bb c0 75` for every choice. As a binary object it cannot be checked without AES, which the working rules exclude (GSMG-CLEAN 16 section 5) |
| `GSMG-PUZZLE-DOSSIER.md:972` | FAED is "homogeneous, P = 0.45 at 19 blocks, once the last 32 chars are removed" | Not homogeneous: blind quarters p = 0.001, quarters of the first 538 letters p = 0.004, corrected for choosing the cuts p = 0.005 (GSMG-CLEAN 16 section 5) |
| `GSMG-PUZZLE-DOSSIER.md:14-18` and `:1784` | "Recent evidence": the user's screenshot reports `Yellowblueprimes:317/557` and `Another door:137/143`, and this "supports replacement over insertion" (the 84-cell model) | **Not evidence.** The screenshot is of two chat messages from a solver, not the creator (#73708 and #73710, 2026-09-26, in `gsmg-haiku/ChatExport_2026-10-08`), posted eight days after the same account described the 84-cell model (#72215). The numbers are that model's own outputs, so the agreement is circular (GSMG-CLEAN 16 section 4) |
| `GSMG-PUZZLE-DOSSIER.md:936` | The earlier "L=83, settled" is withdrawn in favour of an 84-cell reading | Withdrawing "settled" is right. Preferring 84 is not supported: both complete parses stand (GSMG-CLEAN `runs/2026-09-14_dbbi_forward_comparison/REPORT.md`) |
