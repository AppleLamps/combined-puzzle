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
| `packet/RESULTS.md:16`, `AUDIT.md:41`, `SYNTHESIS.md:15` and `:23` | The published 7-XOR password "decrypts" Cosmic Duality (1,327 bytes, sha256 `4f7a1e4e...`); it is used as the harness self-test and described as "already open" | Not a decrypt. It is a pad-1 output under MD5 key derivation and was retracted (GSMG-CLEAN 05 section 1). This directory's own `analysis/FINDINGS.md` Addendum 11 says the same. A harness should self-test on the Phase 3.2 envelope, which is authenticated |
| `WHAT_THE_GROUP_MISSED.md:38` and `:180`, `NEXT_BEST_MOVE.md:33`, `SYNTHESIS.md:26` | Creator #8000 (primes, "zeroed out") is unsafe because it was edited on 2026-02-15 | The wording is safe: it is forwarded verbatim in #29342 (2024-11-10) and pasted with its original date in #30086 (2024-11-14). Most late edit stamps are reaction bumps (GSMG-CLEAN 02) |
| `analysis/FINDINGS.md` (btcseed sections) | btcseed is a false positive | Agreed, and stronger: FAED has no letter-level structure for a Bifid or Hill layer to act on (GSMG-CLEAN 16 section 5) |
| Root documents and `analysis/` | Two layers that disagree on the Cosmic Duality claim and on what to do next | Use GSMG-CLEAN 16 section 3 |

`analysis/zeroed.py` zeroes only the poster URL, never FAED or DBBI, and has hard-coded external paths. It is not a test of the "zeroed out" hint on the unread fields.
