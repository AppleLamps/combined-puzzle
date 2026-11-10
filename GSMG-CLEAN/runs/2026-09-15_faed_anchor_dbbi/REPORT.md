# FAED 5/479/484 anchors applied to DBBI logical cells

## Result

The requested construction was tested without operating on raw DBBI character
offsets. **No plaintext, known instruction, or uniquely distinguished output was
recovered.** The direct anchor characters are small and partially degenerate:

| Index convention | FAED[5] | FAED[479] | FAED[484] |
|---|---:|---:|---:|
| zero-based | `g` = 7 | `a` = 1 | `g` = 7 |
| one-based | `g` = 7 | `i` = 9 | `g` = 7 |

Thus the blue operand and difference-prime operand are identical under both
index conventions. Only the yellow operand changes (`a`/1 versus `i`/9).

## Source-accounting correction

The complete **84-cell** DBBI parse contains 23 prime cells and **61** ordinary
cells. The complete **83-cell** alternative contains 23 prime cells and the
requested **60** ordinary cells. Both were run separately. No ordinary logical
cell was altered or dropped in either branch.

## Bounded family

- anchors 5, 479 and 484 under zero- and one-based indexing;
- circular symmetric FAED neighborhoods of radius 0 through 12;
- forward and reversed neighborhood order;
- DBBI token colors and the first 23 poster colors as separate schedules;
- yellow -> 479, blue -> 484, with logical prime cell 5 -> anchor 5;
- prime-cell operations: replacement, addition, subtraction, reverse
  subtraction and XOR, reduced to the page's a..i digit alphabet;
- every exact rectangular factorization of the 83/84-cell result, with complete
  row and column sums rendered as decimal, modulo 26 and modulo 9;
- each complete transformed logical-cell field used as a keyed Bifid square on
  all 570 FAED characters.

The test generated 1,040 candidates and 940 distinct logical-cell streams.
Every ordinary-cell round trip passed. None exactly equals `matrixsumlist`,
`lastwordsbeforearchichoice`, `thispassword`, `privatekey`, or `btcseed` in any
retained rendering.

The highest Bifid continuation score was 15. In 20,000 deterministic controls
that preserve the same 61 ordinary cells and randomize only the 23 prime-cell
values, the maximum was 21 and 229 controls scored at least 15. Therefore the
best apparent fragments are below noise and are not promoted.

## Direct primary output

For the 84-cell DBBI-token schedule, zero-based anchor characters, radius zero,
and direct replacement, the resulting complete logical-cell field is:

```text
dggigfghccaggihagegeihaggegeabggehheghhfgagfdhaffcdbgfcccggfaeggecadcigfgffgigaeeage
```

Its 7x12 row sums are:

```text
69 74 67 69 57 58 66
```

Its column sums are:

```text
39 43 47 37 43 30 33 38 32 44 32 42
```

No retained rendering of these sums is an instruction. The 83-cell/60-ordinary
control differs at the terminal parse and is retained in `candidates.jsonl`.

## Consequence

This closes the literal interpretation in which FAED's characters or short
neighborhoods at 5/479/484 replace or arithmetically modify DBBI's prime logical
cells while the ordinary cells remain fixed. It does not close an operation in
which the anchors specify lengths, traversal changes, or positions inside the
60/61-cell ordinary payload itself.

Reproduce:

```text
python tools/test_test_faed_anchor_dbbi.py
python tools/test_faed_anchor_dbbi.py
```
