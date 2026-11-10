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
| `STATUS.md` "Latest result" (2026-10-15), `review_leads/cryptanalysis_2026_10_15/README.md` | The DBBI parse gives `HILLFEXMGSGQ`, a full-period Bifid of FAED gives `BTCSEED`, and a mod-25 Hill gives `IFINDO`; the open interface is "the operation after the coordinate split" | A tested hypothesis, not a result. The 7x12 board that spells `HILL` is chosen, not derived (the puzzle's own sentence points to 14 wide); `btcseed` appears for 4 of 40,320 key orders; `IFINDO` needs a change of modulus. FAED's letters show no structure for a Bifid or Hill layer to act on (GSMG-CLEAN 14 section M2, 03 section 4, 16 section 5). Do not extend this chain |
| `mywork/LOG.md` entry 8 | FAED read as a decimal number with `g` as a disguised zero: negative, three runs truncated at the node cap | Agreed and now complete: the last 32 letters hold no `g`, so the low four bytes are fixed at `c7 bb c0 75` for every choice. No truncation is involved (GSMG-CLEAN 16 section 5) |
| `ChatExport_2026-10-08/` | Messages #73708 and #73710 (`Yellowblueprimes : 317/557`, `Another door : 137/143`) | Posted by a solver, not the creator. Two other directories carry them as a clue; they are the 84-cell model's own outputs (GSMG-CLEAN 16 section 4) |
