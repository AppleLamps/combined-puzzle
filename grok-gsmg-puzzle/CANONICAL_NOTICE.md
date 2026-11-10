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
| `README.md`, `ledger/00-lead.md`, rounds 1 to 14, `team/*battery*.py` | Each round ends in a battery of decryptions against the three containers | Stopped. No envelope sweeps (rule 1). The batteries were sound as code (the detector audit in `ledger/23` shows pads at expectation); they carry no information |
| `README.md:39`, `src/step3_mask.py` | Zeroing FAED digits at six positions gives ends `yM` and `szqu` | Search artifacts, as this directory's own skeptic says (`ledger/06`). FAED is not text under the page's decimal codec for any single hidden-zero letter (GSMG-CLEAN 16 section 5) |
| `ledger/02-reader.md`, `experiments.md` | Letter deletion on FAED and DBBI is the open lead | Open only in the sense that it is not exhausted. It has no self-check without AES as posed, so under rule 2 it needs a stated second artifact before any run |
| `README.md:31`, `ledger/00-lead.md:25` | The Bifid of FAED begins `btcseedd`; 8 of 362,880 squares share it | Agreed that it is not a checksum. FAED has no letter-level structure for a Bifid layer to act on (GSMG-CLEAN 16 section 5) |

What this directory gets right and the ledger adopts: `src/archivist_check2.py:680` proves that the last 32 digits of FAED fix its last four bytes. That argument closes the "`g` as zero, 2^107" gap that four other directories still list as open.
