# 115 - The 29 September queue: dbbi with `b` as the zero, letter and mod-10 crosses, operand fit tests (all null)

**6 October 2026 interpretation notice.** This is a dated research record.
Its candidate counts and original logs are preserved, not freshly rerun.
Read [doc 118](118-correctness-audit-remediation.md) for detector/coverage
limits and [doc 119](119-current-evidence-ledger.md) for current findings.
A null applies only to its complete tested tuple.

Reported no-fit and no-flag outcomes do not prove a stream has no payload or that every operand family was covered. Reconstructed pools are not evidence of vanished original membership.

Date: 2026-09-29. Works the queue set out of the dossier's "What remains" (section 12) and doc 114:

1. `dbbi` with `b` as the merged zero (2^25 choices).
2. The letter and mod-10 forms of the `matrixsumlist` pool, crossed with the `lastwordsbeforearchichoice` pool.
3. A derivation that names the operand of `lastwordsbeforearchichoice` and comes with an exact-fit test, the way the `dbbi` parse consumed 91 of 91.

Results: items 1 and 2 are closed. Item 3 has no derivation. Every fit test below sits at its shuffle null, and every decrypt run sits at its expected pad statistics.

Provenance note: the user compared the later Wayback captures of the SalPhaseIon page with the working copy in other projects and found them identical. That closes the "was the page edited" question for this project (dossier section 12).

## 1. Harness and controls

Win test (Python, `wintest.py`): private scalar = sha256(candidate), optionally sha256 twice; both point forms checked against the prize hash160, the sentinel, the compressed twin and the four EC neighbours (dossier section 1). Controls before every run: key 1 gives `751e76e8...`, a planted single-hash key and a planted double-hash key are found.

Container test (C, `h3`): password = sha256 of the candidate as 64 hex characters (form 1), raw sha256 (form 2), sha256 twice as hex (form 4) or sha256 of the hex (form 8), under both EVP digests (md0 SHA-256, md1 MD5), against Terminal, SalPhaseIon short and Cosmic Duality. Recogniser as in dossier section 2: printable >= 0.80, bit bias |z| >= 6, distinct-byte deficit z <= -6, UTF-16 zero alternation, nested `Salted__`, magic headers, pad >= 3. Every pad >= 3 flag is decrypted again in Python and content-checked (`chk_flags.py`). Planted controls (text, EBCDIC, random 77 bytes, UTF-16, and planted `dbbi` numeric and string forms) fire under the harness before the runs.

Live pad statistics are the evidence that the harness decrypts what it says it decrypts: valid PKCS#7 pads are counted against the 1/256 + 1/65536 + ... expectation for every run.

## 2. Item 1: `dbbi` with `b` as the zero

`dbbi` has 25 `b` characters and 91 characters in all. Each of the 2^25 = 33,554,432 subsets of the `b` occurrences was replaced by the zero (`o`, value 0) and the result was read under rule 2 (a..i = 1..9, o = 0).

| form | direction | decrypt tests | valid pads (observed / expected) | flags |
|---|---|---:|---:|---:|
| integer bytes, hex text | forward | 1,207,959,552 | 4,739,361 / 4,737,096 | 76 |
| integer bytes, hex text | reversed | 1,207,959,552 | 4,739,003 / 4,737,096 | 78 |
| digit string and letter string (`o` for zero) | forward | 805,306,368 | 3,159,203 / 3,158,064 | 70 |
| digit string and letter string (`o` for zero) | reversed | 805,306,368 | 3,156,906 / 3,158,064 | 52 |

4.03 billion decrypt tests. The numeric forms total 9,478,364 valid pads against 9,474,192 expected. The string forms total 6,316,109 against 6,316,128 expected. No line was printable text and no flag survived the content check.

Closed: `dbbi` with `b` as the merged zero. The dossier's open-by-size list (section 6.4) now holds only `faed` with arbitrary `g` choices (2^107).

## 3. Item 2: letter and mod-10 forms crossed with the last-words pool

**Pools.**

| pool | size | content |
|---|---:|---|
| `msl_new` | 4,218 | the sum lists of the poster (1,547 lists in 17 encodings) as letters (a1z26 mod 26 with 0 as `z`, a0 form) and as mod-10 digits, forward and reversed |
| `msl_old` | 6,459 | the digit-concat, comma, space, ASCII-character, hex and list-total forms, forward and reversed |
| `msl_all` | 10,677 | the union of the two |
| `lw_core` | 175 | Architect windows, the last 3 to 27 letters before offsets 341, 371, 472, 479, 1238, 1483 and 1539 |
| `lw_loc` | 6,613 | Architect windows ending at each poster-list total |
| `lw_words` | 6,341 | the last 1 to 20 words at every word boundary of the Architect text (334 words) |

The pool rebuild is approximate: 1,547 lists in 17 encodings here against 1,558 in 13 in doc 111.

**Runs.** The joint password is the `matrixsumlist` string followed by the `lastwordsbeforearchichoice` string, with and without `thispassword` between them (the literal reading of #8446).

| cross | pairs | decrypt tests | valid pads (obs / exp) | flags |
|---|---:|---:|---:|---:|
| `msl_new` x `lw_core` | 738,150 | 35,431,200 | 138,965 / 138,946 | 2 |
| `msl_old` x `lw_core` | 1,130,325 | 54,255,600 | 212,267 / 212,767 | 5 |
| `msl_new` x `lw_loc` | 27,893,634 | 334,723,608 | 1,312,820 / 1,312,642 | 25 |
| `msl_all` x `lw_words` | 67,702,857 | 812,434,284 | 3,183,057 / 3,186,017 | 56 |

## 4. Item 3: operand derivations and their fit tests

A derivation counts when it names the operand and gives an exact structural fit. The bar is the `dbbi` parse: 91 of 91 characters consumed by a 25-symbol program with a definite host walk. Each family below was given a fit test against a null built from the same material, and then run against the locks as decrypts.

**Fit tests.** All at the null.

| family | material | real | shuffled null |
|---|---|---|---|
| Sum lists of page objects as English | the textarea blocks, the four container base64 strings, the Architect text and the checker91 string; six value maps; every grid factorisation; rows, columns, rows plus columns and diagonals; letter forms L1, L0, A | 10,094 letter strings; 3 with a dictionary word of 7 or more letters; longest word 7 | 4, 0 and 11 with a word of 7 or more (three shuffles); longest word 7, 6 and 7 |
| Sum lists as indices into the chain texts | 2,173 distinct lists (poster and page-object) as 1-based, 0-based and mod-length indices into six letter texts (Architect, phase 2, phase 3, intro, riddle, checker91) | 25,660 selections; 914 with a dictionary word of 6 or more; longest word 8 | 870, 871 and 875; longest word 8 in each |
| Digit-form lists against `faed`, `dbbi` and the residue | 23,417 digit strings (1,565,346 digits), both directions, in `g`-space (0 and 7 merged to `g`), seed of 7 letters extended exactly | longest exact match 9; 140 strings with a match of 8 or more | longest 11; 129 with 8 or more |
| Mathematical constants and sequences against `faed`, `dbbi` and the residue | 73 corpora (pi, e, phi, square roots, logarithms, cube roots, zeta(3), prime and semiprime sequences and further concatenations), 473,421 digits, both directions, seed of 8 | no match extends past the seed of 8 | not needed |

**Decrypt runs.** These families produce candidate operands with no target to fit, so the locks are the only test.

| family | strings | how they were made |
|---|---:|---|
| Page-object sum lists | 24,454 distinct | the family of the first fit-test row, all forms and reversals |
| Remainder forms | 19,913 | the sum lists reduced mod 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 and 13 |
| RGB and pixel values | 14,936 | the poster as RGB24, BGR24, per channel, luminance, pixel sums, red-ink, black and white pixel counts, then the same sum-list treatment |
| Adjacent operand | 5,709 and 3,935 | the reading in which `matrixsumlist` acts on the text next to it: `dbbi` sum lists with slices of the head and tail of `faed` |
| Walk numbers | 411 and 2,116 | L=83 host-prime sums (yellow 400, blue 474, total 874; offsets 420 and 494) and L=84 sums (yellow 317, blue 557), as sums and as Architect positions |
| Textarea substrings | 404,796 | every substring of the textarea in letter and digit forms, alone as passwords |
| Playing cards and gardeners | 13,319 | pip strings for the New Year dots (dossier section 7.3) and the *Alice* Chapter VIII gardeners as cards |

| run | decrypt tests | valid pads (obs / exp) | flags |
|---|---:|---:|---:|
| page-object lists alone | 293,448 | 1,107 / 1,151 | 0 |
| page-object lists x `lw_core` | 102,706,800 | 402,090 / 402,772 | 7 |
| remainder forms alone | 238,956 | 900 / 937 | 0 |
| remainder forms x `lw_core` | 167,269,200 | 657,416 / 655,958 | 15 |
| RGB and pixel alone | 179,232 | 703 / 703 | 0 |
| RGB and pixel x `lw_core` | 62,731,200 | 246,093 / 246,005 | 4 |
| RGB and pixel x `lw_words` (two halves) | 1,136,510,112 | 4,456,710 / 4,456,902 | 85 |
| adjacent operand pools crossed | 269,578,980 | 1,057,871 / 1,057,172 | 15 |
| walk numbers x Architect windows | 41,744,448 | 163,160 / 163,704 | 3 |
| walk numbers x `lw_words` | 125,095,248 | 490,655 / 490,570 | 10 |
| textarea substrings alone | 4,857,552 | 19,000 / 19,049 | 1 |
| cards and gardeners alone | 159,828 | 652 / 627 | 0 |
| cards and gardeners x `lw_core` | 111,879,600 | 438,858 / 438,744 | 3 |

**Win test.** Base pools of about 497,000 strings under single and double hashing: no hit. The card strings: no hit. The union pool (71,022 `matrixsumlist` strings) crossed with `lw_core`, with and without `thispassword`, 24.86 million strings under single hash: no hit in 1,906 seconds.

## 5. Totals and flag accounting

22 completed runs: **7,286,621,136 decrypt tests, 28,576,797 valid pads against 28,574,986 expected** (an excess of 1,811 at a standard deviation near 5,300), **507 flags**, all accounted for.

- **426 flags at pad 3 or more.** Each was decrypted again in Python and run through the whole recogniser: 0 hits. A genuine plaintext can carry any pad from 1 to 16, so pad >= 3 flags need the content check; the pad statistics alone cannot dismiss them.
- **85 flags at pad 1 on Cosmic Duality for a distinct-byte deficit**, z from -6.45 to -7.32. Each body of 1,327 bytes lacks 9 or 10 of the 256 byte values, a Poisson tail with mean 1.4 missing values. Simulation gave a false-positive rate of 7.5e-6 per cosmic pad-1 decrypt, which predicts about 71 in this volume. Secondary features of all 85: printable fraction at most 0.41, byte-histogram chi-square 251 to 358 (df 255). Noise.
- **1 magic-header flag**, a gzip signature in a random body: the header CRC check fails, so it is not a gzip stream.

An aborted first attempt at the RGB by `lw_words` cross (killed and restarted as two halves) left five more flag lines. They were content-checked with the rest.

## 6. Limits

- The four large crosses (`msl_new` x `lw_loc`, `msl_all` x `lw_words`, the adjacent-operand cross, RGB x `lw_words`) ran with one password order (`matrixsumlist` string first) and the hex-sha256 form only. The `msl_new` x `lw_core`, `msl_old` x `lw_core`, remainder, walk-number and card crosses ran both orders and both forms (48 decrypts per pair). The page-object cross and the RGB x `lw_core` cross ran half of that (24 per pair).
- The double-hash password forms were not run in the C harness. Double hashing was covered only in the win test, on the base pools.
- The win test on the crossed pools ran single hash, one order, on `lw_core` only.
- The pool rebuild differs from doc 111 (1,547 lists in 17 encodings against 1,558 in 13).
- Five pools (`msl_adj`, `lw_adj`, `msl_walk`, `lw_walk`, `cards`) have no script and `msl_rem` has an approximate one (section 8).
- The operand pools hold what could be derived from the objects the puzzle shows. A pool cannot contain an operand that the puzzle never shows.

## 7. What a real derivation still needs

The `dbbi` parse had four properties: a definite alphabet, a definite program length, a definite walk rule and a full-consumption count (91 of 91) that a random string does not reach. For `lastwordsbeforearchichoice` a derivation needs the same four:

1. It names the object the operation reads (which text, which offset or choice point).
2. It defines "last words" as a length (how many) or a boundary.
3. It states what the "choice" is, since the only choice the Architect offers is the red pill against the blue.
4. It reports a count that a shuffled object does not reach, against a shuffle null.

The same holds for `matrixsumlist`: a named matrix, a sum rule, and an output length that a shuffle does not reproduce. Neither has been named by a source. The only definite matrix in the puzzle is the poster, and the poster's 1,547 sum lists (17 encodings, 91 list types each) contain none that fits.

## 8. Status

Queue items 1 and 2 are closed. Item 3 has no candidate. The wall is unchanged: two unknown operations feed one password, and their operands are not named in anything decoded so far.

Scripts: all under `tools/` in this Project, tested from a clean folder built from the Project's own files (`tools/README-tools.md`).

| script | does |
|---|---|
| `setup.py` | rebuilds `ta.txt`, the stage plaintexts, the Architect text and the container files, and checks each against the dossier's hashes |
| `h3.c` | the container harness: stdin, `--cross` and `--dbbi` modes |
| `wintest.py`, `chk_flags.py` | the win test; the content check of every pad >= 3 flag |
| `mk.py`, `mkctl.py` | container files and planted controls |
| `pools.py`, `mkpools.py`, `mkmore.py`, `mk_rgb.py`, `n2.py` | the poster encodings and the pools: `msl_new`, `msl_old`, `msl_all`, `lw_core`, `lw_loc`, `lw_words`, `subs`, `msl_rgb`, `n2_cands` rebuild identically |
| `mkrem_approx.py` | 74% of `msl_rem` |
| `n1.py`, `n2.py`, `fit.py`, `constfit.py` | the fit tests of section 4 |

The pools `msl_adj`, `lw_adj`, `msl_walk`, `lw_walk` and `cards` were built by one-off snippets that were not kept. Their definitions are in dossier section 10.9 and `tools/README-tools.md`.
