# 115. The poster, re-inventoried as a prime operand

26 September 2026. Follows doc 114 (the joint #8446 halves and the 231607 selection),
which concluded that `matrixsumlist` and `lastwordsbeforearchichoice` cannot be reached
by combining what is already decoded and that their operands lie outside the
SalPhaseIon page. Docs 111 to 114 are not in this repository; this session worked from
the 25 September dossier (current through doc 110) and doc 114's conclusion as relayed.

**Question.** Doc 114 left the poster as the most promising outside operand, because
`matrixsumlist`'s sibling `yellowblueprimes` took the poster as its operand. What on
the poster could a prime operation consume that is not the colour program?

**Answer.** Nothing that can carry a designed value. Every pixel of the poster is now
accounted for, including the parts the dossier had only described (the QR code, the
canvas edges, the lower panel). The poster's only free information is the URL, the
`0000` centre, the position of the off-white cell and the rabbit drawing. So any
operation on the poster outputs a fixed function of the URL. It cannot be read, and it
can only be validated by opening a lock, which needs the partner operand as well. That
is the wall again, now from the poster's side. A closed family of `{2, 5, 7}` sum-list
operations was run anyway, with controls: null on structure and null on the locks.

One new observation, not consumed: dbbi marks its hosts with `b` = 2 and `e` = 5,
and faed's single over-drawn letter is `g` = 7. These are the gardeners' primes. The
direct test of that reading is null (section 3).

---

## 1. Harness

Rebuilt from scratch in this session (`scripts/115/harness.py`), per dossier sections
1 and 2:

- win test, single sha256, `sha256(sha256(x))` and sha256 of the hex digest, both
  point forms; private key 1 validated against `751e76e8...`
- all three containers, hashes asserted (`291dfd6f...`, `9e2831e1...`, `b1895055...`)
- password profiles: sha256 hex (canonical), raw, double-hash hex, hex-of-hex; EVP with
  SHA-256 and MD5
- the structure-agnostic recogniser on every valid pad: pad >= 3, printable >= 0.80,
  bit-position bias, distinct-byte deficit, magic headers and nested `Salted__`,
  EBCDIC at 0.95, UTF-16, and every 32-byte window as a key against both targets

Every run plants its own seeded controls (`scripts/115/controls.py`): a container
keyed by one of the run's own candidates, holding random 70- or 71-byte plaintext so
only its padding identifies it, and a target address added for another candidate's
sha256 (and, in section 4, for one raw scalar). They reach the worker processes
through the pool initializer. The runner uses the spawn start method on every
platform, so a run does not depend on forked globals. Every control fired in every
run below. Because a planted container holds random bytes, a wrong candidate can also
hit pad >= 3 on it by chance; the scripts report such a hit separately.

---

## 2. The poster, every pixel

Poster fetched from the `puzzlehunt/gsmgio-5btc-puzzle` mirror; sha256 `38125bbd...`,
byte-identical to the dossier's file. Grid, spiral decode (`gsmg.io/theseedisplanted`
+ `0000`), colour counts 86/85/15/9/1 and the 25-symbol program were re-derived and
match sections 3.0, 4.1 and 4.2.

| element | measured | status |
|---|---|---|
| 14x14 bit grid | spiral reads the URL + `0000` | consumed (URL) |
| colour layer | LSB of each character, 15 blue / 9 yellow | consumed (dbbi) |
| `#FEFEFE` cell | row 7, col 4; spiral 163 | consumed (forced blue) |
| 15-px lattice | the grid is drawn on a 70 x 70 lattice (70 = 2 x 5 x 7) of 15-px tiles, cropped to 1047 x 1047 px. Checked pixel by pixel over the whole grid area: 0 non-uniform tiles, 0 pixels outside the five colours | **new**: the lattice size is the gardeners' product; carries nothing |
| sub-cell content | exactly 37 full tiles (8,325 pixels) differ from their cell's colour, all black in white cells: (6,6):4 (6,7):9 (7,6):6 (7,7):3 (7,8):9 (7,9):4 (8,6):2 | the rabbit drawing (doc 105); no other sub-cell content anywhere |
| canvas geometry | 1048 x 1556, alpha 255 everywhere. Cell edges at multiples of 75 up to 975; the last column and last row are 72 px; column x = 1047 is white top to bottom | cropped Paint canvas; no data |
| divider | `#ED1C24`, rows 1047 to 1061 (exactly 15 px), x 0 to 1046 | design element |
| lower panel | white rows 1062 to 1064; `#F5F5F5` panel from 1065 (its top two rows stop at x = 876, white beyond); white rows 1553 to 1555 | canvas margins |
| logo, title, address | anti-aliased raster text and the GSMG logo; in panel rows 1067 to 1552, 0 pixels outside the logo, title, QR and address boxes differ from `#F5F5F5` | standard |
| QR code | 33x33 (version 4), 7-px modules (all 49 pixels of every module checked: 0 mixed), EC level L, mask 2, 547 dark modules. Stream: ECI designator 26 (UTF-8), byte mode, 73 characters, the blockchain.com URL, terminator, pad `EC 11 EC`; Reed-Solomon parity valid | **new**: re-encoded with `segno` (v4, L, mask 2, byte, ECI UTF-8) it matches **module for module, 0 differences**. Without the ECI header, 372 modules differ, which is why earlier module-level comparisons looked "different". No free module |

The dossier's "no spare capacity" (section 4.6) now covers the whole image, not only
the grid. Everything outside the grid is standard output or canvas margin.

**What follows for `matrixsumlist`.** If its operand is the poster, its output is a
deterministic function of 192 URL bits plus the conventions. The creator could not
have written a message into it, because the grid was already fully spent on the URL.
Two things follow. First, a readable output is not a possible acceptance test for any
poster operation. Second, only a lock can validate it, and the password also needs
`lastwordsbeforearchichoice`. The only other kind of evidence is a structural echo
elsewhere, like the one dbbi gives for the colour program. Section 3 looks for such an
echo.

---

## 3. The gardener letters

| object | letters | reading |
|---|---|---|
| dbbi hosts | `b` (15 blue hosts, the off-white cell included) and `be` (8 yellow hosts) | 2 and 2,5 |
| dbbi residue | `b` under-drawn, 2 of 60 | the generator kept `b` (2) out of the filler |
| faed | `g` = 107, about double every other letter | 7 over-drawn |
| faed's last 32 characters | no `e`, no `g` (dossier P = 0.004); the next longest `e`/`g`-free run in faed is 11 | 5 and 7 both absent |

So the three marker letters of the a..i blocks are {b, e, g} = {2, 5, 7}. Those are
the gardeners Two, Five and Seven of *Alice* Ch. VIII, the planned final hint's prime
set (section 7.2). If the host letters and the excess letter were chosen without
regard to the poem, the chance that they form exactly that set is 1 in C(9,3) = 1 in
84. The pairing was noticed after the fact, so the look-elsewhere price is higher than
that.

**Competing explanation, equally good on counts.** faed fits "uniform filler over a..i
plus about 49 inserted `g` markers" (χ² = 10.8 over the other eight letters, 7 df,
p = 0.15) as well as it fits the dossier's merged-zero model (p = 0.175). It fits
equally well a filler generator whose alphabet string contained `g` twice, which would
also explain why the residue shares faed's `g` excess (doc 101). Counts cannot separate
these three explanations. Positions can: markers that some rule placed must sit where
the rule puts them.

**Tests.**

| test | scale | control | result |
|---|---|---|---|
| `g`-specific periodicity in faed: best (period, offset) enrichment, periods 2 to 200 | 199 periods; 200 seeded shuffles | a shuffled faed with `g` forced at every 7th position from 3 scores z = 13.7 at (7, 3) | best z = 4.05 at (87, 85); null median 4.65; p = 0.97 |
| poster sum lists (section 4) as gap sequences (gap = a·v + b, a in 1..3, b in 0..7) or as sorted positions, from start offsets 0 to 24, on faed, dbbi, dbbi+faed and the residue; score = binomial tail of the most frequent landing letter | 5,603 configurations x 25 starts per block; 20 to 40 seeded shuffles per block | seeded plant: faed-like filler with `g` markers at gaps 2v + 1 of the bit grid's row sums, from position 11. It scores log10 P = -12.3 on exactly that configuration; the next best configuration scores -6.3 | faed p = 0.40 to 0.47; dbbi p = 0.35 to 0.40; residue p = 0.80 to 0.85. dbbi+faed p = 0.00, which is **dbbi's own hosts rediscovered**: every position of the top configuration (the colour program as 2x2 block sums, gap = v + 1) lies inside dbbi. An in-data control |
| the same scan restricted to landings on `g` in faed | 5,603 x 25; 40 seeded shuffles | the same plant scores -12.3 | best log10 P = -4.36; p = 0.78 |

The first runs tried sorted-position configurations only at start offset 0, because
of a stray `break` (found in review). With it removed, every configuration is tried at
all 25 offsets. The re-run results are identical, because no position configuration
comes near the top of any block.

No poster-derived list places faed's `g`s. The {2, 5, 7} letter match stays an
observation. It is added to the surplus list and is not consumed.

---

## 4. The `{2, 5, 7}` sum-list family

Built to be new with respect to the dossier's closed rows (row and column sums, 14
variants x 12 encodings; 54 sum lists as keys; the 70-scalar row/column/diagonal run;
the 126 gardener transforms on the 1-D spiral string).

**Operand matrices (8).** The bit grid with `#FEFEFE` as 0 and as 1; the colour grid
under six numberings (K, W, B, Y, F): gardeners (1, 0, 2, 5, 7) and (1, 0, 2, 5, 2),
resistor code (0, 9, 6, 4, 9), dbbi consumption (1, 0, 1, 2, 1), colour-only
(0, 0, 1, 2, 1), and a1z26 of the colour initials (11, 23, 2, 25, 6).

**Operations.** Row, column, diagonal and anti-diagonal sums; the 7 spiral ring sums;
**2x2 block sums** (a 7x7 matrix, read by row, column and 7x7 spiral); **7x7 block
sums** (2x2); the spiral and row-major value strings; run lengths of both; row and
column sums at the prime indices 2, 3, 5, 7, 11, 13, both 0- and 1-based; rows and
columns 2, 5, 7. Each list forward and reversed. Added: the rabbit ink counts in
spiral and row-major order, the colour cells' spiral positions and gaps. 263 distinct
lists after deduplication.

**2x2 block sums as base-5, all three gardeners at once.** On the bit grid every 2x2
block sums to 0 to 4, which is one base-5 digit. That gives a 7x7 matrix of 49 base-5
digits (total 101, the poster's prime set-cell count). Read as a single base-5
integer by rows, columns or spiral, forward and reversed, with the off-white cell as 0
and as 1, the 12 readings give 14- or 15-byte values that are 13% to 57% printable.
No text, as section 2 predicts.

**Lock screen.** Each list in up to 11 encodings (digits joined, comma- and
space-separated, a1z26, a1z26 with `o` for zero, base-5 and base-10 integers as decimal
and hex, sum, rule 2, raw bytes). Each alone, and each crossed front and back with 27
last-words and label strings (the Hope line in three lengths, "we won't", "if I were
you...", "the problem is choice", "there are two doors", "causality", "stop it",
`TAKETHE`, `TAKETHEPRIVATEKEY`, `CIAOBELLA(O)`, "I really hope you're the one", faed's `e`/`g`-free tail,
`thispassword`, the four #8446 labels). The three integer readings were also tried
directly as private scalars.

| run | candidates | decrypts | valid pads | expected | flags |
|---|---:|---:|---:|---:|---|
| sum lists x last words | 114,565 | 3,666,080 | 14,285 to 14,512 over five runs | 14,321 | only the planted controls (the container once per identical encoding, 22 times; the key once) |
| raw scalars | 421 | | | | only the planted scalar control |

---

## 5. Sum lists as pointers ("last words before")

The shape of the 479 lead: a number from the poster points into a decoded text, and
the words just before it are the "last words". 135 distinct pointer values came from
the family above: list sums, list entries (for lists of 14 or fewer), counts and sums
of spiral and row-major positions of every value class, both 0- and 1-based. They
point into five texts: the Architect letters, the checkerboard message, and the
letters of the phase-2 plaintext, the phase-3.2 intro and the phase-3 riddle head.
The last 3 to 40 letters before each pointer, bare, with `thispassword`, and with the
number on either side.

| run | candidates | decrypts | valid pads | expected | flags |
|---|---:|---:|---:|---:|---|
| pointer last words | 67,280 | 2,152,960 | 8,376 to 8,422 over three runs | 8,410 | the planted control; in the seeded run also one chance pad 3 on the planted container itself (`ltinthispassword`, hex-of-hex profile, MD5 EVP; 0.03 expected), which holds random bytes. None on the real containers |

---

## 6. What this changes

**Dossier section 4.5.** Replace "pristine, no hidden data" with the measurement: the
QR is an exact standard encoding (v4-L, mask 2, ECI 26 UTF-8 header, byte mode), 0
modules differ from a reference encoder, and RS parity is valid. Section 4.6 extends to
the whole image: every pixel outside the grid is standard output or canvas margin.

**Section 12, lead 1** ("`matrixsumlist` as a prime operation on the poster matrix").
Lower it. The family the dossier proposed has now been run: {2, 5, 7} blocks, prime
rows and columns, rings, diagonals, colour numberings, the rabbit. It is null as
structure, null as passwords, and null as pointers. The poster's lack of spare capacity
means no poster operation can have a readable acceptance test. Any further poster work
has to specify the operation in advance, from a creator statement, not from a family.

**Surplus, add.** The {b, e, g} = {2, 5, 7} match of the a..i marker letters to the
gardeners (about 1 in 84, post hoc); the 70 x 70 lattice.

**Where the operands could still be.** Section 2 applies to every object whose
content is fully forced, not only the poster. Taking doc 114's conclusion with this
one: the password needs at least one operand that no decoded object supplies. The
creator's own words point at objects outside the published corpus ("You have all the
info", #9607, against the 2026 laptop and room statements, #66568 and #66903). This
project's standing rule stops at locating people or places. Within that rule, what
remains is:

1. a creator statement that names the operation exactly, found by re-reading, not by a
   new sweep;
2. the four-dot reply (#8311) and the New Year dots, elided words of known length;
3. doc 114's option 2: text before the Architect's choice outside the chain. It was not
   run here. Every literal reading in the dossier (film, Hope line, chain choice
   points, song, both books) is already null, so it needs a new pointer, not a new
   corpus.

---

## 7. Reproduce

```
cd claude/scripts/115
python3 prep.py          # builds data/ from the dossier + poster; asserts hashes and decodes
python3 poster_audit.py  # section 2 and the base-5 readings in section 4
python3 gperiod.py       # section 3, g periodicity, with control
python3 gapwalk.py 40    # section 3, marker walks with shuffle nulls and the planted walk
python3 gonly.py         # section 3, g-only, with the planted walk
python3 run_lists.py     # section 4 lock screen, with planted controls
python3 run_pointers.py  # section 5, with planted control
```

Requires `coincurve pycryptodome pillow numpy segno`. `data/` is generated, not
committed. `prep.py` downloads the poster from the GitHub mirror and checks its sha256.
