# Errata to earlier GSMG workspace documents — 2026-09-14 adversarial reanalysis

Each item names the document, the exact location, what it says, why it is wrong or overstated, and the replacement
statement. Originals are untouched.

## E1 — TEST INVALID: address oracle compares hash160 against dictionary keys (addresses)

Files and lines (absolute path prefix `E:\rabbit-combined\GSMG-CLEAN\tools\`):

| script | dict built | membership test |
|---|---|---|
| `audit_m4_zeroing_oracles.py` | 86-87 (`{address: hash160}`) | 252-256 (`hh in TARGET_H160`) |
| `audit_pointer_selectors.py` | 157 | 218 |
| `audit_board_shape_sums.py` | 127 | 162 |
| `audit_colour_selectors.py` | 164-167 | 200 |
| `audit_keyed_faed.py` | 139-142 | 175 |
| `audit_tail_cipher.py` | 160-163 | 194 |

The keys are Base58 addresses; the tested value is a 40-hex hash160; the test can never be true. The self-tests in these
scripts reproduce the marker addresses through a different path (`addresses(k)['compressed'] == MARKER_ADDRS[i]`), so they
pass without exercising the production loop. Affected statements: every "0 marker/prize address hits" line in
`runs\2026-09-14_m4_zeroing_oracles\REPORT.md`, `runs\2026-09-14_pointer_selectors\REPORT.md`,
`runs\2026-09-14_board_shape_sums\REPORT.md`, `runs\2026-09-14_colour_selectors\REPORT.md`, `runs\2026-09-14_keyed_faed\REPORT.md`,
`runs\2026-09-14_tail_cipher\REPORT.md`.

Replacement: those statements are void. The null is re-established validly by
`runs\2026-09-14_adversarial_reanalysis\exp1_address_oracle_rerun\` (planted controls 42/42, 0 hits over 476,912 unique scalars).

## E2 — `runs\2026-09-14_structural_key_formats\REPORT.md`: coverage claim

`tools\audit_structural_key_formats.py` builds its target set correctly but derives scalars only from raw 32-byte windows,
64-hex, WIF, base64 and decimal tokens. It never computes `sha256(candidate)`, `sha256d`, `sha3_256` or `sha256(hex)`. Any
sentence implying that the retained outputs were checked "as keys" in the sense that produced the three solved markers is
overstated. Replacement: the hashed derivations were first validly run in exp1.

## E3 — `runs\2026-09-14_dbbi_forward_comparison\REPORT.md` line 152

Text: "preferring 84 merely because 23/16/7 appears elsewhere cannot supply that prediction."
Correction: the b/be census differs between the parses (84: 16 b, 7 be; 83: 15 b, 8 be; `exp0_reproduction/repro_dbbi_parse.json`).
The Architect numbers "SIXTEEN … SEVEN" therefore do predict the endpoint-dependent final token (b, i.e. 84), conditional on
reading `b` = encryption and `be` = intertwined password. The report's sentence should read: "23/16/7 supplies a one-bit
prediction of the final token in favour of 84, conditional on the b/be assignment; it does not predict additional data."

## E4 — `04_DEAD_ENDS_TESTED.md` lines 52 and 81 (firsthint 8,004; G2 15,060) and `08_SALPHASEION_RECIPE.md` line 41 (tested column)

These rows present the firsthint sweeps as tests of the "first hint = last command" reading. Per the round-1 ledger
(`prior_research_ledgers\rabbit_r1\FINDINGS_round1.md` lines 1594-1600) the acceptance rule was printable-ASCII, later
acknowledged as uninformative, key oracles were raw-only, and no outputs were retained. Status should be NOT TESTED (as
recorded). Replacement: the source-supported core of the family (50 strings × raw/sha256/sha256² × SHA-256/MD5 KDF × 3
envelopes) is now a VERIFIED null with retained outputs in
`runs\2026-09-14_adversarial_reanalysis\exp2_first_hint_last_command\outputs\`.

## E5 — `runs\2026-09-14_aligned_replacement_v2\REPLACEMENT_TABLE.md`: 24-row variants

Not an error in the report (it flags the dependence), but restated for downstream users: rows 'in'→'TO' at letters [58,60)
and 'then'→'THAN' at [408,412) exist only against the kedri transcript ("inherent in the programming", "quicker then the
others"); the Scott transcript has "than". Any construction that uses 24 rows is using two transcription artefacts.

## E6 — This reanalysis's own pre-compaction note

An interim tally of "16 B + 8 Y + 1 O" poster markers was wrong. Correct: 15 blue, 9 yellow, 1 off-white
(`data\verify_log.txt:2` is right). No document was written with the wrong count.

## Not errata (checked, found correct)

- `data\verify_log.txt` lines 1-2 (spiral rule, colour string).
- `01_PROVEN_CHAIN.md` passwords, salts, plaintext sizes and hashes (byte-exact reproduction in exp2 validation).
- `08_SALPHASEION_RECIPE.md` stream boundaries; the 128-char base64 decodes exactly to `locked_salphaseion_short.bin`.
- Telegram ids cited in `08`, `09` and the forward reports (quoted from the export this session).
- `tools\check_replacement_outputs.py` and `tools\audit_structural_key_formats.py` target dictionaries (keyed by hash160).
