# CLAUDE.md

Work on the GSMG.io 5 BTC puzzle. Read `START-HERE.txt`, `claude/status.md`, `claude/119-current-evidence-ledger.md` and `claude/118-correctness-audit-remediation.md`, then `claude/GSMG-PUZZLE-DOSSIER.md` (sections 1, 2, 10 and 12 at minimum) before proposing or running anything.

## Rules
- Never submit to `gsmg.io/phase1verification`. Never contact, locate or profile the creator.
- On-chain OP_RETURN text and today's gsmg.io are not puzzle material unless they match a pre-2022 capture or a hash the dossier holds.
- A null counts only when its planted control fired. Report tests, valid pads against expected, and flags.
- Nulls must sample the class of outcome (shuffle nulls), not the specific answer.
- Do not filter for printable plaintext; use the recogniser in `h3` and `chk_flags.py`.
- Generate data blocks by script, never retype them.
- Never propose anything that needs another person. No new method gets CPU unless it retrodicts phases 2, 3 and 3.2 (`claude/riddle-method/retro.py`). No more coverage sweeps.
- A joint-password null kills the pair tested, not either reading alone (`claude/117`, section 11). Keep a pair ledger.
- Check dossier section 10 and section 12 ("Spent leads") before proposing a lead. A new word list is not a lead; a derivation with an exact structural fit is (doc 115 section 7).

## Running the harness
These are historical instructions, not a statement that current encrypted runtime
checks passed. Doc 118 records verification limits. The 6 October update is docs-only;
no search is running. Do not revive blocked runs or Atlas from an old task list.

Build in a scratch folder, not in the repo:
```
pip install pycryptodome coincurve numpy pillow english-words
mkdir -p work && cp tools/* work/ && python3 tools/setup.py . work
cd work && python3 mk.py && python3 mkctl.py
gcc -O3 -march=native -Wno-deprecated-declarations -o h3 h3.c -lcrypto -lm
python3 verify.py ../claude/GSMG-PUZZLE-DOSSIER.md     # 60 checks, 0 failed
```
Run the planted controls in `tools/README-tools.md` before any sweep.

## Recording results
New findings go in a numbered log doc under `claude/` (next is 121) and are folded into the dossier, sections 10 and 12. `work/` is scratch; do not commit it.

## Canonical ledger (added 2026-11-10)

This directory is a frozen snapshot inside the combined repository. The single source of truth is
`../GSMG-CLEAN/`. Read `CANONICAL_NOTICE.md` in this directory before relying on any claim here: it
lists the statements the canonical ledger contradicts. Two rules from
`../GSMG-CLEAN/16_CANONICAL_LEDGER_AND_WORKING_RULES_2026-11-10.md` apply here as well:

- No envelope sweeps. A password is tried only through
  `../GSMG-CLEAN/tools/check_candidate.py --derivation runs/<dir>`, after that derivation checked
  itself without AES.
- Every new experiment states the second artifact it predicts before it generates candidates
  (`../GSMG-CLEAN/tools/prereg.py`), and its result is recorded in `../GSMG-CLEAN/`.

This directory's own rules above still hold inside it.
