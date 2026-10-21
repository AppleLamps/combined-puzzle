# The board shape: DBBI 84-cell values under both shapes — 2026-09-14

**Result: null under the folder's own judging standard. The known `HILLFEXMGSGQ` output is recovered as a
sanity check, but it loses the contest it created: it is one of 744 outputs, it is the *only* strong word any
model produces, and 25,015 shuffle controls of the same families beat or match it.** `14_CRITICAL_REVIEW_2026-09-14.md` §M2 / move 2.

## 1. What was tested

The complete 84-cell DBBI parse (23 primes / 16 `b` / 7 `be`, two `b` letters on ordinary cells) under five
value models — **signed** (L2: `b` = −slot, `be` = +slot, ordinary 1–9), **unsigned**, **colour** (2 / 25),
**signed/unsigned with the M4 prime-5 cell zeroed** — and four board shapes (**6 × 14**, 14 × 6, 7 × 12, 12 × 7),
plus the 83-cell parse as a 1 × 83 control: row and column sums, reversed and cumulative forms, both
concatenation orders, through five decode families (mod-26 A0/A1, A1Z26, ASCII, the page's decimal-integer
codec, index into the Architect letters). **744 outputs.**

Each letter output was scored by common-English-trigram count and judged against **25,015** control readings
(each model × each parse, shuffled, run through the same shapes and decodes). Every decoded string also went
through the exact oracles: the DBBI sha256 equality pattern and the three marker plus two prize addresses
(sha256 / sha256d, compressed and uncompressed). No envelope bytes were read; no AES was run.

## 2. Findings

- **The sanity control reproduces the community's word.** 84-cell / signed / 7 × 12 / column sums / mod-26 reads
  `hillfexmgsgq`. The code path is the same one that produces every other output here.
- **That is the only strong word.** The highest-scoring outputs are score 2 (`LREECTATLREA`,
  `LFIFRDRANDGGFL…`, `LFSAANNCE…` — fragments, not language), and the 25,015 controls reach **4**. Zero of 744
  outputs score above control. Under the judging standard this folder itself uses (the 09 §5 pipeline: real
  must beat controls; planted controls must beat all), the HILL-family result is a *weakness* of the 7 × 12
  model, not evidence for it.
- **Exact oracles: 0 of 744.** No decoded string carries the DBBI token pattern; none derives a marker or
  prize address. (Also: the folder's own FAED/DBBI pipelines already null on the same gate at much larger
  scale, so this is a consistency result, not a scope claim.)
- **The M4 zeroing variants change nothing readable.** Signed/unsigned with prime cell 5 zeroed produce no
  output above control and no oracle hit under these decodes.

## 3. What this closes, and what it leaves open

**Closed.** The 7 × 12 signed model's one readable word does not survive controlled judging, and the 6 × 14
shape the source sentence points at produces nothing readable here either. So DBBI's 84 values, under *any*
of these five value models × four shapes × five decodes, do not reconstruct readable text or any exact
oracle hit. Repeating row/column-sum runs with new word lists or new paddings is the documented failure mode;
this run is on the record as the controlled version.

**Left open.** The untested cells of the model space, in the order the sources suggest:

1. **The colour interpretation of the prime values** (b = 2 = B, be = 25 = Y, the one reading with source
   support) used as something other than lattice weights — e.g. as colour *selectors* on the ordinary cells
   before summing. This run used colours only as values.
2. **The DBBI material as a key rather than as a value lattice** — e.g. the balanced prime numbers
   (479, 484, 5) or the 84-cell values as a Vigenère/Beaufort key over FAED. The workspace's 10 §7 / 14 §M5
   reading (labels name transformations on the *other* field) has barely been touched.
3. **The 64-letter `DBBI − VIC` tail** (24 distinct letters) as a cipher object in its own right.

## 4. Reproduce

```powershell
python tools\audit_board_shape_sums.py
```

Writes `manifest.json` (pre-registered scope, models, shapes, control count) and `results.json`
(744 outputs, 25,015-control maximum, above-control set, oracle hits, top-8). No envelope byte is read by
the script.

**Limits.** The scoring metric is trigram count (one metric, stated); the decode families are the five listed
above (checkerboard-style, homophonic and polyalphabetic decodes are outside); the zeroing row covers only the
prime-5 cell; the 83-cell control is a 1 × 83 row only.