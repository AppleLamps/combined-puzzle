# 116 - The doc 115 coverage gaps: second order, raw and double-hash forms, scripted pools (all null)

**6 October 2026 interpretation notice.** This is a dated research record.
Its candidate counts and original logs are preserved, not freshly rerun.
Read [doc 118](118-correctness-audit-remediation.md) for detector/coverage
limits and [doc 119](119-current-evidence-ledger.md) for current findings.
A null applies only to its complete tested tuple.

“Coverage gaps closed” is this historical run title. Later detector defects and missing original pool membership remain limits; the corrected doc 118 set was not rerun.

Date: 2026-10-03. Works the limits listed in doc 115, section 6:

1. The four large crosses ran one password order (`matrixsumlist` string first) and the hex-sha256 form only.
2. The double-hash password forms were never run in `h3`.
3. Five pools had no script and `msl_rem` rebuilt at 74%.
4. The win test on the crossed pools ran single hash and one order.

Result: every gap is closed and null. 26.8 billion decrypt tests, valid pads at expectation, 1,940 flags, all content-checked as noise.

## 1. Tooling changes (in `tools/`)

- `h3 --order N`: 1 = A+B only, 2 = B+A only, 3 = both (`--both` is still 3). Lets a run cover only the order not yet tested.
- `wintest.py --order N --procs P`: the same order switch, and the worker count.
- `plant.py OUT CAND FORM [md]`: a control container for any candidate under any password form (1, 2, 4, 8) and either EVP digest. 70 random bytes, so the right password gives pad 10.
- `mkmissing.py`: scripted re-derivations of `msl_adj`, `lw_adj`, `msl_walk`, `lw_walk`, `cards` and the base-m part of `msl_rem` (`msl_rem_ext.txt`), from the definitions in `tools/README-tools.md`.
- `chk_flags.py`: now re-decrypts forms 2 and 3 (double hash) correctly and asserts that the re-decrypt reproduces the flagged pad. Before this fix it treated every non-hex form as raw sha256, which had no effect on earlier runs because none used the double-hash forms.

## 2. Pools

| pool | doc 115 | this run | note |
|---|---:|---:|---|
| `msl_new`, `msl_old`, `msl_all`, `lw_core`, `lw_loc`, `lw_words`, `subs`, `msl_rgb`, `n2_cands` | as doc 115 | identical counts | existing scripts |
| `msl_adj` | 5,709 | 27,852 | `dbbi`, the residue, and `dbbi` joined to head/tail slices of `faed` (7 to 91), every grid factorisation, `g` as 7 or 0, forms D, Dc, Ds, L1, A, both directions. Broader reconstruction; original membership unknown |
| `lw_adj` | 3,935 | 3,188 | head and tail windows (3 to 150) of `faed` and the residue, letter form, digit form with `g` as 7 or 0, both directions, ASCII hex, rule-2 hex |
| `msl_walk` | 411 | 153 | 400, 474, 874, 420, 494, 317, 557 in six writings, their permutations with six separators, and the 23 host positions (logical and stream offsets) in five list forms |
| `lw_walk` | 2,116 | 2,081 | Architect windows of 3 to 52 letters before and after offsets n-1, n, n+1 for each walk number |
| `cards` | 13,319 | 12,366 | the README definition |
| `msl_rem` | 19,913 | 70,253 | `mkrem_approx.py` (51,001) plus the lists as base-m integers in hex and decimal (20,821) |

The re-derived pools are not byte copies of the 29 September files, which were not kept. Where a count is lower (`lw_adj`, `msl_walk`, `cards`) the definition was followed as written and the writings that doc 115 used beyond it are not recorded.

## 3. Harness and controls

All three containers, both EVP digests, `thispassword` appended as the mid in every cross. Before each cross job, `plant.py` built a control from row 1 of A and the last row of B in that job's own order, under form 8 (sha256 of the hex digest) and the MD5 digest, and `h3` was run on that row against the whole of B with the job's own flags. **All 14 controls fired** (exactly one pad-10 flag each). The base job used the existing controls, which fired at setup.

## 4. Runs

Forms: 1 hex sha256, 2 raw sha256, 4 hex of sha256 twice, 8 sha256 of the hex digest. Mask 14 = forms 2, 4, 8 (form 1 already run); mask 15 = all four; mask 12 = the two double-hash forms.

| job | cross | orders | mask | decrypt tests | valid pads (obs / exp) | flags |
|---|---|---|---:|---:|---:|---:|
| base | every pool alone (about 584,000 strings) | n/a | 15 | 14,013,240 | 54,396 / 54,954 | 1 |
| core_all | `msl_all` x `lw_core` | both | 12 | 89,686,800 | 351,495 / 351,713 | 7 |
| core_rem | `msl_rem` x `lw_core` | both | 15 | 1,180,250,400 | 4,631,050 / 4,628,434 | 90 |
| core_n2 | `n2_cands` x `lw_core` | both | 15 | 410,827,200 | 1,609,838 / 1,611,088 | 24 |
| core_rgb | `msl_rgb` x `lw_core` | both | 15 | 250,924,800 | 983,838 / 984,020 | 19 |
| core_cards | `cards` x `lw_core` | both | 15 | 207,748,800 | 816,874 / 814,700 | 19 |
| walk_lw | `msl_walk` x `lw_walk` | both | 15 | 30,565,728 | 120,501 / 119,867 | 1 |
| walk_words | `msl_walk` x `lw_words` | both | 15 | 93,136,608 | 364,970 / 365,243 | 6 |
| new_loc_ab | `msl_new` x `lw_loc` | A+B | 14 | 1,004,170,824 | 3,936,050 / 3,937,924 | 60 |
| new_loc_ba | `msl_new` x `lw_loc` | B+A | 15 | 1,338,894,432 | 5,252,853 / 5,250,566 | 95 |
| all_words_ab | `msl_all` x `lw_words` | A+B | 14 | 2,437,302,852 | 9,562,303 / 9,558,051 | 181 |
| all_words_ba | `msl_all` x `lw_words` | B+A | 15 | 3,249,737,136 | 12,741,090 / 12,744,066 | 244 |
| rgb_words_ab | `msl_rgb` x `lw_words` | A+B | 14 | 3,409,530,336 | 13,367,596 / 13,370,708 | 254 |
| rgb_words_ba | `msl_rgb` x `lw_words` | B+A | 15 | 4,546,040,448 | 17,826,497 / 17,827,608 | 317 |
| adj_adj | `msl_adj` x `lw_adj` | both | 15 | 8,524,048,896 | 33,433,068 / 33,427,640 | 622 |
| **total** | | | | **26,786,878,500** | **105,052,419 / 105,046,582** | **1,940** |

The pad excess of 5,837 sits at about 0.6 standard deviations.

## 5. Flag accounting

- **1,590 flags at pad 3 or 4** (1,580 pad 3, 10 pad 4; about 1,597 and 6.2 expected). Each was re-decrypted in Python (`chk_flags.py`, the corrected version), the pad reproduced, and the body run through the full recogniser: 0 hits.
- **341 pad-1 and pad-2 flags on Cosmic Duality for a distinct-byte deficit.** Over 34,882,653 Cosmic pad-1 decrypts that is 9.8e-6 per decrypt; a fresh simulation of 400,000 random 1,327-byte bodies gave 1.0e-5 (doc 115 estimated 7.5e-6). Secondary features: printable at most 0.41, byte chi-square 238 to 367 on 255 df, 9 to 12 byte values missing. Noise, as in doc 115.
- **9 magic-header flags**, all a bare 3-byte gzip signature (about 6 expected at 2^-24 per decrypt). None decompresses as gzip, zip, bzip2 or xz.

## 6. Win test on the crossed pools

`wintest.py` with its three controls (key 1, a planted single-hash key, a planted double-hash key), all of which passed before each run. The union pool rebuilt to the doc 115 definition (`sort -u msl_all n2_cands msl_rem msl_rgb msl_adj`, 139,770 strings with the re-derived pools against 71,022) crossed with `lw_core`, with and without `thispassword`, single and double hash, on all seven targets (prize, sentinel, compressed twin, four EC neighbours).

| order | strings | private scalars | hits | time |
|---|---:|---:|---:|---:|
| A+B | 48,919,500 | 97,839,000 | 0 | 1,207 s |
| B+A | 48,919,500 | 97,839,000 | 0 | 1,206 s |

## 7. What is still open

- The re-derived `msl_adj`, `lw_adj`, `msl_walk` and `cards` are not the files doc 115 ran; the parts of those files that came from writings no definition records cannot be rebuilt.
- `faed` with arbitrary `g` choices (2^107) remains open by size alone.
- None of this touches the wall: the operands of `matrixsumlist` and `lastwordsbeforearchichoice` are still unnamed. These runs describe the reconstructed sets only. Without the vanished original artifacts or membership manifests, exact coverage or superset inclusion cannot be established by larger counts.
