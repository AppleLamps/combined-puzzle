# FAED structure before another key search

**Outcome:** no new decryption or established cipher. The work tests the representation instead of assuming FAED is decimal-encoded text. A weak tail-frequency change is retained for follow-up; neither short-period statistics nor variable-length token counts establish a method.

## 1. Raw-symbol structure with controls

`profile_faed_structure.py` predeclares four test families. Each observed maximum is compared with 1000 permutations preserving FAED's exact nine symbol counts. The family-wise decision threshold is p <= .0125 for these four tests; all candidate lags, periods and split locations are included in their corresponding control maximum.

| Family | Empirical p | Interpretation |
|---|---:|---|
| Maximum equal-symbol rate at lags 1–60 | .429 | No unusual repetition in this family |
| Maximum same-symbol coincidence within residue classes, periods 2–60 | .899 | No unusual periodic grouping in this family |
| Adjacent-symbol mutual information | .254 | No unusual immediate-symbol dependence |
| Maximum frequency-distribution change, with at least 40 symbols on each side | .018 | Weak tail lead; does not pass the four-family threshold |

Strong planted paired-symbol, period-19 and two-region controls all exceed the original-input permutation maxima in their corresponding families. These check detection of deliberately strong structure; they do not prove sensitivity to every encrypted or weaker signal.

**The tail lead is preserved, not dismissed.** The strongest split is at FAED offset 523, leaving 47 characters:

```text
beiichiedifbehgbccahhbiibibbibdcbahaidhfahiihic
```

`g` occurs 106 times in the first 523 symbols and once in the last 47. The ending has more i/b/h. The split was selected by scanning, so it is not a source-defined boundary. It is not legitimate to trim or reset the cipher there without additional support. The value p=.018 is already corrected for searching split locations through the maximum statistic, but not small enough for the four-family threshold. No p-value here measures the probability that the puzzle is random.

## 2. Variable-length symbols: test an alternative to “570 digits”

The existing DBBI lead treats b/g as two-character introducers. A nine-column checkerboard with two prefix rows would provide 7 single-character and 18 double-character codes: 25 total. Such a modified board is a hypothesis, not the earlier puzzle's verified ten-column board.

Applying b/g consistently:

| Field | Source characters | Tokens | Distinct tokens |
|---|---:|---:|---:|
| DBBI | 91 | 64 | 16 |
| FAED | 570 | 451 | 25 |

This illustrates why ciphertext character count need not be plaintext length. But **all 29 prefix pairs that completely parse FAED also use all 25 codes**. Therefore FAED's 25-code coverage is not independent validation of b/g. The other seven of the 36 two-prefix families end with a dangling prefix and fail complete parsing.

`test_faed_variable_tokens.py` checks the entire token stream, forward and reversed, against contiguous full-length windows in the modified speech, the film dialogue and the Architect-only dialogue. Both ordinary letters and I/J merging are covered. Mapping constraints require a bijection: repeated tokens must give repeated letters, and different tokens cannot silently collapse to the same letter.

**940,016 complete-window comparisons produced zero exact matches.** No key was guessed and no short word/prefix counted as success. This excludes only those complete source-passage substitution models, not arbitrary English plaintext, a different text source, or an additional cipher layer. The comparison count includes overlapping windows and is not a count of statistically independent experiments.

## Direction supported by this pass

FAED does not supply a detected short period under the declared tests, and the simple variable-token substitution model does not reconstruct the known passages. Further short-key or literal-quotation sweeps lack a new supporting observation.

Two issues remain explicitly separate: the nine-symbol representation has not been identified, and the weak final-region change may or may not reflect internal structure. A future construction should predict a boundary or relationship that was not chosen to improve its output, then reproduce the complete field. Do not promote 451 tokens, 25 symbols, or the offset-523 split to a solved instruction.

## Reproduce and retain

- `python tools/profile_faed_structure.py`: manifest, complete score profiles, 1000 permutation scores, and planted controls.
- `python tools/test_faed_variable_tokens.py`: every complete parse and source-character span, family manifest and exact-match summary.

Files: `summary.json`, `permutation_scores.json`, `token_parses.json`, `token_summary.json`, and the two manifests. No source data was modified, no password candidates were generated and no AES trials were performed.
