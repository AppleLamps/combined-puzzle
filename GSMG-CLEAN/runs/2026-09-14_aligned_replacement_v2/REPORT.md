# Aligned replacement table and bounded matrix pipeline

## Result

**The replacement table is complete under declared alignment conventions. No intended matrix or new
password/key has been established.** Eight alignments account for every normalized token; an independent
verifier checks all 1,944 sum lists and numerical byte serializations. No AES or network operations were used.

The important finding is that the apparent **24-edit-row construction is transcript-dependent**. Both
transcripts have the same 22 puzzle-edit intervals under spelled-number alignment. The second transcript
adds exactly two rows: `in -> TO` and `then -> THAN`. Scott's text already has `to` and `than`.
Thus 24 edits cannot be called independent confirmation of the 24 poster colours.

## Read these artifacts

All paths below are relative to this report's containing directory:

- `REPLACEMENT_TABLE.md`: readable complete Scott/spelled-number table, including the large narrative replacement.
- `replacement_table.csv`: every row of all eight alternatives, with exact source/puzzle spans and offsets.
- `tables.json`: full tokens, character/letter coordinates, alignment operations, and row measurements.
- `scott_source.json`, `kedri_source.json`: dialogue extraction and excluded source lines, with file line numbers.
- `stability.json`: method agreement and cross-transcript edit locations.
- `matrix_inventory.json`, `sum_lists.json`: every tested matrix and complete list of sums.
- `all_outputs.jsonl`: all text and binary outputs, not a top-score shortlist.
- `independent_verification.json`: separate accounting/arithmetic/serialization/reconstruction checks.
- `key_format_check.json`: format controls and complete prize-key scan result.

## What “exact aligned” means

The saved readable puzzle text compacts exactly to the authoritative 1,539-letter file. Its whitespace,
word boundaries (including `KEYNOTE`), and punctuation are editorial, not independently authenticated.
The two saved film transcripts are witnesses, not proof of the author's exact working source.

Speaker labels, navigation text, and stage directions are excluded from the dialogue token stream; excluded
lines remain catalogued. Internal apostrophes normalize away (`HAVEN'T -> HAVENT`), not into separate words.
Numbers are retained in the literal view, and explicitly expanded in the spelled-number view. Raw source
spans still show the original digits. No unmatched words are truncated by positional `zip()`.

Twenty-one matching anchors constrain order. The large passage between `THE OTHERS` and `DENIAL...` is kept as
one narrative replacement rather than splitting it wherever common words happen to match. That grouping is
an explicit analyst choice. Two algorithms compare the other gaps: SequenceMatcher and exact LCS with a
declared tie rule. Both agree on the spelled-number tables within each transcript. This is reproducibility
under a specified model, not proof of a unique author edit history.

## Dimensions and stable replacements

| Source / numbers | Edit rows | Removed words | Replacement words | Removed letters | Replacement letters |
|---|---:|---:|---:|---:|---:|
| Scott / literal / SequenceMatcher | 19 | 343 | 164 | 1,674 | 731 |
| Scott / spelled / both algorithms | 22 | 341 | 160 | 1,685 | 709 |
| Second transcript / literal / SequenceMatcher | 21 | 354 | 166 | 1,729 | 737 |
| Second transcript / spelled / both algorithms | 24 | 352 | 162 | 1,740 | 715 |

Literal-number LCS alternatives preserve the word counts but change the removed/replacement letter totals
by one; see `summary.json`. This is another reason not to treat an arbitrary diff statistic as fixed puzzle data.

Selected rows from the stable Scott/spelled table (zero-based, end-exclusive puzzle letter intervals):

| Source | Replacement | Puzzle interval |
|---|---|---|
| the matrix | THIS PUZZLE | [76,86) |
| absent | CODES | [1027,1032) |
| absent | HOPEFULLY | [1075,1084) |
| program | BASICS | [1108,1114) |
| the matrix | OVER | [1153,1157) |
| individuals | CIPHERS | [1168,1175) |
| female | ENCRYPTIONS AND OR | [1182,1198) |
| male | INTERTWINED PASSWORDS | [1203,1223) |
| rebuild Zion | FIND THE ACTUAL PRIVATE KEYNOTE THAT ALSO BRUTE FORCING MIGHT BE REQUIRED | [1225,1287) |

The source's 23/16/7 numbers match the puzzle's spelled numbers; they are not new numerical insertions.
No tested unpadded rectangular stream has a dimension of 14. This does **not** rule out other representations,
nor does it establish that the instruction must require width 14.

## Matrix and command-chain tests

**264 matrix candidates**, of two kinds:

1. Natural two-column (and transposed) source/replacement tables of word counts, letter counts and A1Z26 sums.
2. Explicitly exploratory exact factorizations of complete removed/replacement word-length streams,
   letter-value streams, and per-edit signed feature differences. Factorization is not evidence of intent.

For `yellowblueprimes`, the primary declared schedule assigns all 24 poster colours to prime positions
2 through 89. Only 156 candidates contain enough positions; shorter matrices are ineligible, not partially
decoded. Colour selection uses either original cell values or values weighted by their prime positions.
Yellow, blue and yellow-minus-blue grids supply row/column sums. No sign is silently discarded.

An alternate schedule assigns one colour/prime per edit row and is therefore only eligible for the
second transcript's 24-row tables. Its counts, weighted sums and differences are retained even though the
24-row interpretation is not stable across sources.

For `lastwordsbeforearchichoice`, sums index four declared passages: Architect dialogue before Neo's
`Choice`, the immediately preceding Architect utterance, the common final speech cut before physical door
selection, and the puzzle speech before `SELECT`. Both ordinary indexing (zero/one-based) and counting
backward from the passage end are tested. Whole words with/without spaces, initials and finals are retained;
final letters are an additional hypothesis, not the literal meaning of “last words.”

No padding, modulo wrapping, absolute values, or dropped zero entries repair an invalid index list. The
zero-based case can select the first word repeatedly when a masked sum is zero. Such repetition is a
deterministic consequence of the model, not readable-message evidence.

Results:

- 1,944 complete sum lists (including alternate-row schedules).
- 8,852 word-selection output records; 480 each from start-one and end-one indexing, 7,892 from start-zero.
- 28,170 retained output records including numerical serializations.
- 0 exact complete matches to the declared DBBI, FAED, Architect, and known instruction targets.
- No claimed plaintext or uniquely justified matrix. The absence of a target match cannot disqualify an
  intermediate that has another purpose.

## Binary/key checks, not English-only acceptance

In addition to text, sum lists are retained as nonnegative decimal-integer bytes where defined and as
representable signed/unsigned 1/2/4-byte arrays in both endiannesses. These byte encodings are explicit models.
Every resulting output is inspected, without a prose score, for sliding big/little-endian 32-byte values,
hex64, complete valid WIF at both lengths, decimal scalars, and recursive hex/base64/binary/decimal children.
The scanner compares both compressed and uncompressed public-key encodings to both prize targets.

- 28,170 records; 11,177 unique decoded nodes.
- 2,028,665 raw32 windows per byte order; 425,198 unique valid scalars.
- **0 prize-key matches; 0 optional DBBI SHA-256 equality-pattern matches.**
- No valid WIF or isolated hex64 was reported. Raw windows already include both halves of every 64-byte node.
- Two recursive decode levels; no arbitrary inter-record joining. Complete WIF fragments are not brute-forced.

The controls exercise the real extraction functions: known key, embedded raw halves, hex64, Base64, valid WIF,
mutated WIF rejection and wrong-target rejection. Six pipeline unit tests cover token preservation,
unequal replacement spans, direct/end indexing, colour schedule completeness, sums, and a planted
mask/sum/word-selection example with a mutation test. No statistical English exclusion is claimed.

## Scope and next implication

The earlier claim that the edit map was *the correct operand* was too strong. This pass supplies a usable
exact table and tests concrete constructions; it does not prove that the intended puzzle operates on edits.
The main retained clue is the shared replacement structure, especially the changed instruction nouns.
Before another expansion, a new model needs to explain **why these replacements choose a particular operation
or layout**, not merely select a convenient count. The puzzle remains unsolved; required data has not been
shown to be missing.

## Reproduce (use a fresh output directory)

```powershell
python E:\rabbit-combined\GSMG-CLEAN\tools\test_aligned_replacement_pipeline.py
python E:\rabbit-combined\GSMG-CLEAN\tools\aligned_replacement_pipeline.py --out E:\rabbit-combined\GSMG-CLEAN\runs\aligned_replacement_replay
python E:\rabbit-combined\GSMG-CLEAN\tools\verify_replacement_artifacts.py E:\rabbit-combined\GSMG-CLEAN\runs\aligned_replacement_replay
python E:\rabbit-combined\GSMG-CLEAN\tools\check_replacement_outputs.py E:\rabbit-combined\GSMG-CLEAN\runs\aligned_replacement_replay\all_outputs.jsonl
```

The v1 directory is a preliminary run retained for provenance. v2 additionally tests the per-edit-row
schedule and preserves binary sum serializations. Original puzzle data, original pages, and outside
workspaces were not edited.