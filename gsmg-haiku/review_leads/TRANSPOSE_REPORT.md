# Digit transposition before checkerboard parsing

The prepared test was run. **No remaining container opened and no target key matched.**

Inputs: whitespace-free SalPhaseIon textarea slices S[:91] and S[195:765], each forwards and backwards. Column keys, exactly:

```
matrixsumlist
thematrixhasyou
lastwordsbeforearchichoice
fubcdoraclethingkymvps
```

For each, apply the columnar permutation and its inverse, sorting columns by (key character, original column index), with ragged columns and no added padding. This is 2 runs × 2 directions × 4 keys × 2 permutations = 32 cases. Map a–i to 1–9 only after rearranging the stream, then parse with the established checkerboard. Uppercase/lowercase complete board outputs, decimal digit strings, decimal-integer bytes, and paired decimal bytes for the even-length stream become candidate answers. Apply the established SHA256(answer).hex password convention and SHA-256 EVP derivation against all three remaining containers.

## Completed results

- 32 transposition cases; 29 complete checkerboard parses, 3 incomplete parses.
- 138 distinct candidate byte strings; 414 AES trials.
- 3 padding-valid outputs; maximum printable fraction 0.4937, no recognized binary structure.
- 478 distinct scalar/public-point comparisons from answer hashes and saved payload interpretations; no target match.

Complete parses are not evidence of success: this board accepts most available digit combinations. None of the 29 decoded strings visibly forms sustained grammatical language. All 32 transformed streams and their decoded outputs are retained in `transpose-inspection.json`; all padding-valid bytes are retained in `next-transpose-padding.jsonl`. Binary inspection did not repeat AES decryptions.

## A constraint independent of the transposition key

The 91-digit run contains:

```
1:3  2:25  3:8  4:4  5:18  6:10  7:10  8:8  9:5
```

Under the fixed board, L,E,T,H,I,N,G,K,Y require a leading 1. Any permutation therefore produces **at most three such letters combined**. A 2 maps to U unless consumed as the second digit of a 1- or 4-prefixed symbol. There are only seven possible prefix digits, so any complete parse forces **at least 18 U characters**. A complete parse has at least 84 characters, because at most seven two-digit symbols can be formed.

These bounds are mathematical deductions from the current run and board. They make ordinary English unlikely under this fixed mapping regardless of the columnar key. They do not establish another language, nor exclude a later cipher layer. The imbalance may instead indicate the wrong digit mapping or checkerboard. This is a stronger reason to deprioritize further key-only transposition searches on R1 than the 32 negative cases alone.

## Reproduction

Commands executed:

```powershell
python review_leads/next_tests.py transpose
python review_leads/inspect_transpose.py
```

Scripts refuse to overwrite their existing result JSON files. Existing results are `next-transpose-results.json` and `transpose-inspection.json`.
