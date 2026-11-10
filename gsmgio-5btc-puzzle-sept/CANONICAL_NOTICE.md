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
| `README.md` (community walkthrough) | Stops at the SalPhaseIon labels and lists the three blobs as unsolved | Correct as far as it goes. It has no status, leads or corrections; use GSMG-CLEAN 01 for the proven chain and 05 for retracted community claims |
| `README.md`, SalPhaseIon AES blob quoted on two lines | The blob is shown split around the `enter` label | The two halves are one envelope, and the `z` that ends the first half is ciphertext. A 127-character copy without it can never decrypt (GSMG-CLEAN 01 section 6) |
| `telegram-export-gsmg-group/` | Export to 2026-09-15 | Later exports exist: `gsmg-haiku/ChatExport_2026-10-08` runs to 2026-10-08. No creator message appears after 2026-09-01 in any of them |
