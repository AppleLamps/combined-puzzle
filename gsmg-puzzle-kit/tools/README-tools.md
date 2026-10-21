# tools/: the scripts behind the dossier's negative results

Historical versions were run on 29 September 2026 (doc 115) or earlier. Source changed in the 5 October correctness remediation and AES-import restoration. Read [doc 118](../claude/118-correctness-audit-remediation.md) for exact checks and limits; current encrypted runtime and C compilation were not established by those source-only checks. Without them a new session has to rebuild the harness and the candidate pools from prose.

## Historical quick start

These commands were not run for the 6 October documentation update. No search is
active; old commands and pool descriptions are not an instruction to resume one.
Current research interpretation is [doc 119](../claude/119-current-evidence-ledger.md).


Requirements: Python 3 with `pycryptodome coincurve numpy pillow english-words`, and `gcc` with the OpenSSL headers.

1. Put the Project files and every file in this `tools/` folder into one folder. The setup script needs `phase2.b64`, `phase3.b64`, `terminal.b64`, `salphaseion-short.b64`, `cosmic-duality.b64`, `salphaseion-textarea.txt`, `architect_letters_1539.txt`, `puzzle.png` and `GSMG-PUZZLE-DOSSIER.md` (it also looks in `claude/`).
2. `python3 setup.py` builds `ta.txt`, `b64/*.b64`, `pt2.bin`, `pt3.bin`, `pt32.bin`, `architect.txt`, `puzzle.png` and `words.txt`. Every step checks its result against the length or sha256 the dossier records (section 13) and stops on a mismatch.
3. Build the container files and the planted controls: `python3 mk.py`, then `python3 mkctl.py`.
4. Build the harness: `gcc -O3 -march=native -Wno-deprecated-declarations -o h3 h3.c -lcrypto -lm`.
5. Build pools (below), run, then check flags with `chk_flags.py` and run the win test with `wintest.py`.

## The harness, `h3`

Tests each candidate answer against locked containers. Password = sha256 of the candidate under the forms selected by the mask, with legacy `EVP_BytesToKey` under both SHA-256 (md0) and MD5 (md1), AES-256-CBC, PKCS#7. Each candidate is run against every container named with `-c`.

```
./h3 -c NAME file.bin [-c NAME2 file2.bin ...] [-f MASK]        candidates on stdin, one per line
./h3 -c ... --cross A.txt B.txt [--mid thispassword] [--both] [--part K N] [-f MASK]
./h3 -c ... --dbbi LETTERS --zero 2 [--rev] [--part K N] [--strforms] [--nonum] [--textonly]
```

- `-f MASK`: 1 = hex(sha256(x)) as the password, 2 = raw sha256(x), 4 = hex(sha256(sha256(x))), 8 = hex(sha256(hex(sha256(x)))). Default 3 (forms 1 and 2).
- `--cross A B`: every line of A followed by every line of B (A + B), and with `--mid` also A + B + mid (the string `thispassword` after the pair). `--both` adds the orders B + A and B + A + mid; `--order 1|2|3` picks A + B only, B + A only, or both. `--part K N` runs every N-th row of A starting at row K, so N processes can split a run.
- `--dbbi LETTERS --zero 2`: enumerate every subset of the letters whose digit value is 2 (`b`) and read each as the zero, then test the resulting integer as raw bytes and as hex text. `--rev` reverses the digit string. `--strforms` tests the digit string and the letter string (with `o` for the zero) as candidates, `--nonum` skips the integer forms.
- Current source output on stdout: `FLAG<TAB>container<TAB>formN<TAB>mdN<TAB>padN<TAB>reason-or-unranked<TAB>bodylen=...<TAB>candhex=...<TAB>body=...`. It retains complete padding-valid records independently of ranking, up to its explicit bound. Stderr reports progress, pad histograms, summary counts and retained/omitted audit counts.
- The recognizer ranks printable >= 0.80, bit-position bias |z| >= 6, distinct-byte deficit z <= -6, UTF-16 zero alternation >= 0.6, nested `Salted__`, magic headers and pad >= 3. Ranking does not decide retention: current source retains unranked valid pads 1 and 2 too. `chk_flags.py 'GLOB'` reads all retained padding values using explicit `candhex=` encoding. Padding alone is not validation; a lack of heuristic recognition is not proof that binary output is meaningless.
- Expected statistics: valid pads = tests x (1/256 + 1/65536 + 1/16777216). `SUMMARY` prints the expected value. A run whose observed count is far from it did not decrypt what it claims to.

Controls (run them first, and confirm they fire):

```
printf 'plantedone\nplantedtwo\nplantedthree\nplantedfour\n' | ./h3 -c a pl_text.bin -c b pl_ebcdic.bin -c c pl_rand77.bin -c d pl_utf16.bin
./h3 -c c pl_dbbi.bin --dbbi $(cat ctl_letters.txt) --zero 2               # numeric integer form
./h3 -c c pl_dstr.bin --dbbi $(cat ctl_letters.txt) --zero 2 --strforms    # digit-string form
./h3 -c c pl_lstr.bin --dbbi $(cat ctl_letters.txt) --zero 2 --strforms    # letter-string form
```

`mk.py` writes `phase2.bin terminal.bin short.bin cosmic.bin` (the containers as raw files for `-c`) and `pl_text pl_ebcdic pl_rand77 pl_utf16 pl_dbbi` plus `ctl_letters.txt`. `mkctl.py` writes `pl_dstr.bin` and `pl_lstr.bin`.

## The win test, `wintest.py`

```
python3 wintest.py base FILE...                       every line of each file as an answer
python3 wintest.py cross A B [--mid STR] [--both]     every A+B (and A+B+STR), as h3 --cross
add --dbl to also test sha256(sha256(x)) as the private scalar
```

Private scalar = sha256(x); both point forms are hashed to hash160 and compared with the prize, the sentinel, the compressed twin and the four EC-neighbour hash160s (dossier section 1). It runs the key-1 control, a planted single-hash control and a planted double-hash control before it starts and stops if any fails. About 10,000 to 14,000 candidates per second on two cores.

## The shared prize gate, `prize_gate.py` (doc 120)

```
python3 prize_gate.py selftest            55 planted checks; must print PASS
python3 prize_gate.py key <hex|WIF|...>   gate one candidate
python3 prize_gate.py scan PATH... [--json OUT]
```

Byte-identical in every GSMG repository. Unlike `wintest.py`, which hashes each answer
into a scalar, it finds keys stored as data: raw 32-byte windows, hex, WIF, mini keys,
base64, decimal, plus sha256 of the whole text. Both targets, both serializations.

## The two 80-byte envelopes, `envelope_campaign.py` (doc 120)

`prereg` builds the candidate list from puzzle files and seals it; `run` checks the seal,
retrodicts phases 2, 3 and 3.2, fires three planted envelopes, then tries every string
on Terminal and SalPhaseIon-short and flags pad >= 15, recogniser hits or prize hits.

## Pools, and how each one is rebuilt

Names are those used in doc 115 and dossier section 10.9.

| pool | strings | script | status |
|---|---:|---|---|
| `msl_new`, `msl_old`, `msl_all`, `lw_core`, `lw_loc` | 4,218 / 6,459 / 10,677 / 175 / 6,613 | `mkpools.py` (uses `pools.py`, `architect.txt`) | rebuilt, identical files |
| `lw_words` | 6,341 | `mkmore.py` (uses `arch_words.txt`) | rebuilt, identical set of strings |
| `subs` | 404,796 | `mkmore.py` | rebuilt, identical set of strings |
| `msl_rgb` | 14,936 | `mk_rgb.py` | rebuilt, identical set of strings |
| `n2_cands` | 24,454 | `n2.py` | rebuilt, identical set of strings |
| `msl_union` | 71,022 | `sort -u msl_all.txt n2_cands.txt msl_rem.txt msl_rgb.txt msl_adj.txt` | identical when built from the archived `msl_rem` and `msl_adj` |
| `msl_rem` | 19,913 | `mkrem_approx.py` | approximate: rebuilds 14,823 of 19,913 (74%) |
| `msl_adj`, `lw_adj` | 5,709 / 3,935 | none | not rebuilt (definitions below) |
| `msl_walk`, `lw_walk` | 411 / 2,116 | none | not rebuilt (definitions below) |
| `cards` | 13,319 | none | not rebuilt (definition below) |

`seg.py` gives a first-pass split of the Architect text into words. The 334-word split used for `lw_words` was corrected by hand and is kept as `arch_words.txt`. Do not run `seg.py` over it; its output differs in a few words.

**The 17 poster encodings** (`pools.py`, dictionary `E`; `cell` is the 14x14 grid of K, W, B, Y, F letters and `bit` the 196 bits, both in `matrix.json`). Each encoding maps a cell to a number, and `matrix_lists` then builds the sum lists (rows, columns, reversed, rows+columns, prime-indexed rows and columns from 1 and from 0, gardener subsets of {2, 5, 7} by index and by multiple, diagonals and anti-diagonals, 2x2 and 7x7 blocks, flat and spiral chunks and windows of 2, 5 and 7, sums at prime positions, cumulative sums, mod-2/5/7 classes, and the 3x3 gardener sub-matrix):

| name | rule |
|---|---|
| `bit_F0`, `bit_F1` | the cell's bit; the painted cell F counts as 0 or as 1 |
| `res_Fwhite`, `res_Fred`, `res_Fblue` | resistor colour code: K 0, Y 4, B 6, W 9, and F as 9, 2 or 6 |
| `consume` | dbbi consume counts: K 0, W 0, B 1, Y 2, F 1 |
| `idx_kbyw` | Paint palette position: K 1, B 2, Y 3, W 4, F 4 |
| `idx_wkyb` | W 1, K 2, Y 3, B 4, F 1 |
| `pal1`, `pal0` | 1-based and 0-based Paint palette index: K 1/0, W 11/10, B 9/8, Y 6/5, F 11/10 |
| `w1_F0`, `w1_F1` | 1 for white (F as 0 or as 1) |
| `painted`, `colour_only`, `blue_only`, `yellow_only`, `dark` | 1 for F; for B or Y; for B; for Y; for K or B |

**Forms** (`pools.forms`): `D` digits joined, `Dc` comma-joined, `Ds` space-joined, `L1` a1z26 mod 26 (0 as `z`), `L0` a0 mod 26, `M10` each value mod 10, `A` ASCII characters (all values 32 to 126), `H` two hex digits per value (all values below 256), `T` the list total. `msl_new` holds L1, L0 and M10; `msl_old` holds the rest. Each form is used forward and reversed, length at most 400.

**The last-words pools** (`mkpools.py`, `mkmore.py`), all cut from the 1,539-letter Architect text `A`:

- `lw_core`: `A[o-k:o]` for k = 3 to 27 and the offsets o = 341, 371, 472, 479, 1238, 1483, 1539.
- `lw_loc`: the same windows for o equal to each distinct sum-list total of the poster lists, minus `lw_core`.
- `lw_words`: the last 1 to 20 words, joined without spaces, at every word boundary of the 334-word split.

**Definitions of the pools that are not rebuilt** (as recorded, not reconstructible from a script):

- `msl_adj`: the adjacent-operand reading, in which `matrixsumlist` acts on the text next to it: sum lists of `dbbi` with head and tail slices of `faed`, in digit, comma, space, letter and ASCII forms. About half are digit, comma or space strings.
- `lw_adj`: head and tail windows of up to 150 characters of `faed` and of the 60-character `dbbi` residue, in letter form and in digit form (`g` as 0 or as 7), forward and reversed, plus about 1,500 strings in other encodings (hex among them). About 60% are windows of those objects.
- `msl_walk`: the walk numbers as candidates in several writings (L=83 host-prime sums 400 (yellow), 474 (blue) and 874 (total); offsets 420 and 494; L=84 sums 317 and 557; zero-padded, reversed, joined and separated, and the hex list of the 23 host positions of the L=83 parse).
- `lw_walk`: Architect windows anchored at the walk numbers.
- `cards`: rank sequences (Ace to Five ascending and descending, contiguous runs, and orderings of the gardeners' 2, 5 and 7), each rank as a digit or as a word (Ace as `ace` or `one`), with or without `of`, with a suit (club, diamond, heart, spade, singular and plural) at the end or after each card, joined with space, comma, underscore, hyphen or nothing.

## Fit tests (doc 115, section 4)

- `n2.py`: sum lists of every page object (textarea blocks, container base64, Architect text, checker string) under six value maps and every grid factorisation, read as English by dictionary segmentation, against shuffled values. Also writes `n2_cands.txt`.
- `n1.py`: sum lists as 1-based, 0-based and mod-length indices into six chain texts, English fit against shuffled lists. About 7 minutes.
- `fit.py FILE...`: digit-form lists against `faed`, `dbbi` and the residue in `g`-space (0 and 7 merged), longest exact match from a 7-letter seed.
- `constfit.py`: 73 constant and sequence corpora against the same targets, seed 8.

## Checking the dossier

`verify.py DOSSIER.md` recomputes the dossier's data blocks from the primary files (60 checks). `poster.py DOSSIER.md` checks the poster's spiral, cell counts and colour sequence (12 checks). Both need the files `setup.py` builds. Every check printed PASS on 29 September.

## Correctness audit (5 October 2026)

`h3` retains the first 1,000 padding-valid outputs in deterministic traversal order,
including unranked pads 1 and 2, as full body hex with `candhex=` for every candidate.
`flags` counts heuristic ranks; `validpads` counts padding validity. Overflow is
reported and returns exit status 2 (incomplete review), so it cannot support a no-solution claim.
`chk_flags.py` checks every retained padding value and requires the explicit encoding;
legacy `cand=` records are rejected because printable literal `0x` text was ambiguous.
Python testers retain 1,000 complete records, print retained/total/omitted counts and
return exit status 2 on overflow. Controls require exact planted plaintext or solved hashes,
so retaining unranked results cannot make a wrong-key padding event pass a control.
None of these scripts proves correctness from padding alone; downstream validation
is required. Historical logs have not been rewritten or rerun.

`python -m unittest discover -s tests -v` exercises only plain synthetic bytes, source
functions with cipher calls replaced by deterministic stubs, assembly membership and
process exit contracts. It performs no encryption, decryption, puzzle searches or wallet operations.

## Known limits

- Doc 116 (3 October) reports runs on named doc 115 gaps, subject to detector and membership limits: every cross in the second order and under forms 2, 4 and 8, and the crossed win test in both orders under double hash. [`claude/doc116-runs/rungaps.sh`](../claude/doc116-runs/rungaps.sh) is retained; doc 116 section 4 lists each job's pools, `--order` and `-f` mask.
- `mkmissing.py` re-derives `msl_adj`, `lw_adj`, `msl_walk`, `lw_walk` and `cards` from the definitions above, and adds the base-m part of `msl_rem` (`msl_rem_ext.txt`). These are re-derivations, not copies of the files doc 115 ran (doc 116 section 2 compares the counts).
- `plant.py OUT CAND FORM [md]` plants a control for any candidate and password form; run it through the same `--cross`/`--order`/`-f` path before a sweep.
- `h3` tests only the containers named with `-c`; name all three for a real run.
