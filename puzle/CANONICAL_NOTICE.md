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
| `README.md:26-36`, `STATE_OF_PLAY.md` | "The strongest new result is the creator-named yin-yang milestone": blue 484, yellow 479, zero the blue prime 5, Architect[479:] = `PRIVATEKEY...` (tagged fitted) | A pointer with no payload. All 476 literal outputs of the construction are null against every exact oracle (GSMG-CLEAN 14 section M4, `runs/2026-09-14_m4_zeroing_oracles/REPORT.md`). Do not treat yinyang as located |
| `round55.md:40`, `SOLVE_SESSION_2026-08-06.md:110` | The final key is `sha256(X)` for a short personal text known to the creator's friends, so no further search can reach it | An unresolved tension, not a conclusion. Creator #9607 "No need. You have all the info." is a direct reply to that question, and #16624 says the internet is not required (GSMG-CLEAN 02 section 10, 15) |
| `SOLUTION.md`, `gsmgio-5btc-puzzle-master/` chain-1, chain-2, Cosmic, base-38, Chain 4 material | Presented in places as "not padding luck" | Chance padding. `docs/ATTEMPT_LOG.md` section 14d and GSMG-CLEAN 05 section 1 agree; the older narrative text does not |
| `gsmgio-5btc-puzzle-master/solver/`, families v1 to v78 | Blind envelope families | Stopped. No envelope sweeps (rule 1) |

This directory's own rules still hold inside it: `docs/ATTEMPT_LOG.md` is append-only and `solver/targets.py` is its only acceptance gate. Its evidence hierarchy (creator material first, prior-agent negatives cited by scope) is adopted by the ledger.
