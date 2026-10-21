# #8446 as a pipeline: yellow/blue primes → matrix sum list → last words — 2026-09-13

**Result: null.**
- **Readable text:** no decode family produces more readable text from the real inputs than from shuffled inputs.
  - In all 10 letter-decode families the real maximum is at or below the control median-to-p99 range.
  - The planted positive controls in those families beat all 400 controls.
- **L5 gate:** 0 matches in 110,832 checks.
- **Envelopes:** 0 notable results in 110,832 trials; pad=1 437 vs 431.2 expected.
- **Word-index families** (2 of 12): **no detection power**. A planted 12-word sentence does not beat the controls (below), so their null says nothing.

The reasoning behind it is in `09_UNFORESEEN_HINT_AND_LAST_WORDS.md` §4.

## Construction (pre-registered in `manifest.json`)

**Colour order**
- The 24 coloured poster cells in spiral order: `BBBBYBBBYYBBBBYBBYYBYYBY` (asserted; yellow primes sum to 479).
- The i-th coloured cell is paired with the i-th prime.

**69 matrices**

| Source | Matrices |
|---|---|
| Poster 14×14 (from `originals/poster/puzzle.png`) | Yellow primes, blue primes, all primes, signed B+Y− and Y+B−, yellow / blue / all prime ordinals, the black+blue bit matrix |
| DBBI (a..i = 1..9) at 7×13 and 13×7 | Full; prime positions zeroed / only; the first-24 prime positions coloured Y/B (only, zeroed, signed both ways); the prime numbers themselves at Y, B or coloured positions |
| FAED at 19×30, 30×19, 15×38, 38×15, 10×57, 57×10 | Full; prime positions zeroed / only; Y-only and B-only on the first 24 prime positions |
| L2 prime-parse values (84) at 7×12 and 12×7 | Values; negatives zeroed; abs of negatives only |

**552 sum lists**
- Row sums and column sums of each matrix.
- Each as forward, reversed, non-zero entries only, and cumulative sum.

**12 decode families → 4,677 real outputs**

| Kind | Families |
|---|---|
| The page's own and standard encodings | `a1z26`, `mod26a0`, `mod26a1`, `ascii`, `parity8` (parity bits → 8-bit ASCII), `decimal_bytes` (digits → integer → bytes, the SalPhaseIon a–i/o method) |
| Index decodes into the 1,539-letter Architect text | `arch_idx0` / `arch_idx1` |
| Index decodes into the Scott Manning transcript letters | `sm_idx0` / `sm_idx1` |
| Index decodes into words | `puzzle_word_idx1` (puzzle-text words), `sm_word_idx1` (transcript words) |

**Scores**
- **Letter families:** best segmentation of the output into vocabulary words (3,868 words of length ≥ 3, from *Looking Forward*, the transcript and the puzzle text), scoring Σ(len−2)².
- **Word families:** adjacent word pairs found among the 37,201 *Looking Forward* bigrams.

**Controls: 400 shuffled-input runs through the identical pipeline**
- poster cell classes permuted (census kept; colour order and positions follow)
- DBBI, FAED and L2 values permuted
- target texts fixed

**Decision rule:** a family is SIGNAL only if its real max beats **every** control max (p ≤ 1/401, Bonferroni-safe for 12 families) and its planted control also passes.

## Results (v2; identical to v1 for the 10 letter families)

| Family | Real max | Control max | Control p99 | p | Planted (beats all controls?) | Verdict |
|---|---|---|---|---|---|---|
| a1z26 | 1 | 9 | 8 | 0.97 | 47 (yes) | null |
| mod26a0 | 9 | 17 | 16 | 0.27 | — | null |
| mod26a1 | 5 | 16 | 16 | 0.52 | 47 (yes) | null |
| ascii | 1 | 11 | 8 | 0.95 | — | null |
| parity8 | 0 | 1 | 1 | 1.0 | — | null |
| decimal_bytes | 0 | 1 | 1 | 1.0 | — | null |
| arch_idx0 | 9 | 22 | 19 | 0.83 | 56 (yes) | null |
| arch_idx1 | 9 | 27 | 19 | 0.88 | — | null |
| sm_idx0 | 5 | 25 | 20 | 1.0 | — | null |
| sm_idx1 | 14 | 27 | 20 | 0.35 | — | null |
| puzzle_word_idx1 | 14 | 21 | 18 | 0.44 | 7 (**no**) | **no power** |
| sm_word_idx1 | 18 | 19 | 17 | 0.01 | not planted | not signal (the top output is word salad: "will to control to possible a was stumbled program…") |

**Planted controls**
- `a1z26` / `mod26a1`: the A1Z26 list for "thelastwordsbeforethechoice".
- `arch_idx0`: indices of "TAKETHEPRIVATEKEYYOUVEEARNEDIT".
- `puzzle_word_idx1`: word indices of "THE FUNCTION OF THE YOU IS NOW TO RETURN TO THE SOURCE".

**Top real outputs** (all at control level; the full list is in `results.json`):
- `mod26a0` "itrapmchartbqn"
- `arch_idx0` "EQTOWFBOMBSSH"
- `arch_idx1` "TOOOINTOONTOAO"

**L5 and envelopes (v2)**
- 9,236 unique text forms (8 forms per output).
- L5 gate (4 hash views × 3 orientations): 110,832 checks, **0 hits**.
- 3 envelopes × 4 profiles: 110,832 trials, pad histogram {0: 110,394, 1: 437, 2: 1}, **0 with pad ≥ 3, 0 keys**.

## Self-tests (both runs)

- `check_candidate.selftest()` PASSED: the Phase 3.2 envelope opens, plus hash160, EC, WIF and detectors.
- `coincurve` key scan == pure-Python on 24 scalars.
- L5 gate accepts a synthetic DBBI-shaped hex and rejects a one-nibble change.
- The script refuses to run if the script or any input hash differs from the manifest.

## History (kept honest)

**v1** (`v1/`, script sha256 `2d51146b…`)
- The word score counted *every* adjacent bigram, so index wrap-around repeats ("of of of …") dominated.
- Planted sentence scored 7 vs control max 53, so the word families had no power.
- The letter families were null exactly as above.

**v2** (script sha256 `76b11ac5…`)
- The only change is the word score, which now counts *distinct* pairs of *different* words (plus the version fields). It was re-registered and re-run.
- The letter-family results are byte-identical to v1.
- The word families still fail the planted control (7 vs 21): chance bigrams in 57-word random lists outscore a 12-word sentence.
- **No further tuning was done**, to avoid fitting the statistic to the data. Those two families are reported as uninformative.

## Scope of this null

**Covers:** the 552 sum lists above under the 10 letter decodes, judged by readability against shuffled inputs, and every output string as a literal answer (L5 gate and envelopes).

**Does not cover:**
- other matrix readings: diagonals, spiral rings, blocks, sums mod n, products
- other colour → cell assignments (for example colours on FAED beyond the first 24 primes)
- other target texts for index decodes (the film's full script, subtitles)
- word-index decodes (no power)
- any use of the lists as keys for a cipher

## Verification

```
python run_pipeline.py build   # 69 matrices, 552 sum lists, 4,677 real outputs; script 76b11ac5…
python run_pipeline.py run     # ~45 s: self-tests passed; 0 SIGNAL families; gate_hits 0; notable 0
```

## Files

| File | Contents |
|---|---|
| `run_pipeline.py` | v2 `build` / `run` |
| `manifest.json` | v2 pre-registration |
| `results.json` | summary per family, planted scores, L5/envelope counts, top 12 outputs per family, all 400 control maxima |
| `sum_lists.json` | all 552 real sum lists |
| `run_stdout.txt` | v2 console output |
| `v1/` | v1 script, manifest, results, sum lists and stdout |
