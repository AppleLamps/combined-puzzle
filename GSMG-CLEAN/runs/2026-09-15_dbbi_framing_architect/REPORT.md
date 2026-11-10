# DBBI prime markers as framing metadata

## Result

The 83-cell DBBI parse produces exactly **23 fixed prime boundaries, 24 ordered gaps, and 60 ordinary cells**. Every ordinary cell round-trips unchanged. Prime-token values are absent from every operand.

The bounded run generated **518 candidates** (118 complete, 62 unique complete outputs). It found **0 exact Architect-differential matches** and **0 known-instruction hits**.

The best complete English score was **4**; the randomized-control maximum was **6**, with **471/5000** control trials reaching or exceeding the real maximum. The best descriptive differential similarity was **0.625**; acceptance still requires an exact match or readable output, not a fuzzy ratio.

No tested framing read rises above the fixed-gap shuffled controls.

Direct ordered-vector comparison is also null. The gap-length vector's strongest absolute Pearson correlation is **0.439** (permutation p=0.086); the terminal-value vector's is **0.318** (p=0.530).

## Exact framing

- Marker schedule: `BBBBYBBBYYBBBBYBBYYBBYY`
- Gap lengths: `1,0,1,1,3,1,3,1,3,5,1,5,3,1,3,5,5,1,5,3,1,5,3,0`
- Gaps: `d | ∅ | i | f | hcc | g | iha | e | eih | ggege | b | gehhe | hhf | a | fdh | ffcdb | fcccg | f | eggec | dci | f | ffgig | eea | ∅`
- Terminal letters: `d ∅ i f c g a e h e b e f a h b g f c i f g a ∅`
- Terminal values: `4 ∅ 9 6 3 7 1 5 8 5 2 5 6 1 8 2 7 6 3 9 6 7 1 ∅`

The gap-length sequence is fixed by the locations of the primes; it is not independent ciphertext. The terminal sequence is payload-derived and retains empty gaps explicitly.

## Tested operations

1. Align the 24 DBBI gaps one-to-one with each 24-row Kedri/spelled Architect edit table.
2. Use the gap length or terminal value as a row-local index into removed or inserted letters, from either end, under zero/one-based and strict/cyclic conventions.
3. Reverse complete DBBI gap intervals: all intervals, blue-closing intervals, yellow-closing intervals, and the corresponding marker-opens-next-gap convention. Internal character order changes; gap order and boundaries do not.
4. Use every ordinary value in each interval as a row-local Architect index under the same declared conventions.
5. Compare complete outputs with all retained Architect-differential streams and the exact instruction oracles.

## Scope

This closes direct row-local indexing and whole-gap reversal under the framing model. It does not test arbitrary permutations, arithmetic on ordinary values, or treating prime markers as values. The latter is excluded by design.

Reproduce with `python tools/audit_dbbi_framing_architect.py` and verify with `python tools/test_audit_dbbi_framing_architect.py`.
