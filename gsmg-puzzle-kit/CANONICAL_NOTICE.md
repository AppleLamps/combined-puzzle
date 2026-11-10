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
| `claude/GSMG-PUZZLE-DOSSIER.md:1129` and `:2057`, `claude/115-...md:42`, `claude/116-coverage-gaps-closed.md:89`, `claude/67-document-index.md:362` | "Open by size alone: faed with arbitrary `g` choices (2^107, not enumerable)" | **Closed as text.** The last 32 letters of FAED contain no `g`, and the low four bytes of the integer depend only on the last 32 digits, so they are `c7 bb c0 75` for every choice. As a binary object it cannot be checked without AES, which the working rules exclude (GSMG-CLEAN 16 section 5) |
| `claude/GSMG-PUZZLE-DOSSIER.md:1100`, with "Carry faed as one object" | FAED is "homogeneous, P = 0.45 at 19 blocks, once the last 32 chars are removed" | Not homogeneous: blind quarters p = 0.001, quarters of the first 538 letters p = 0.004, corrected for choosing the cuts p = 0.005 (GSMG-CLEAN 16 section 5) |
| `claude/119-current-evidence-ledger.md:44` | "L=83 is preferred" under the fixed first-23-event correspondence | Both complete parses stand (83 and 84 cells); neither is selected (GSMG-CLEAN `runs/2026-09-14_dbbi_forward_comparison/REPORT.md`) |
| `CLAUDE.md` "Running the harness", `tools/` | Build and run the `h3` decrypt harness | Historical. No envelope sweeps (rule 1). The file's own rules already say "No more coverage sweeps" |

What this directory gets right and the ledger adopts: a null counts only when its planted control fired, and a new word list is not a lead.
