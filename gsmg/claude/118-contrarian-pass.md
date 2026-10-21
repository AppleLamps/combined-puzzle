# Doc 118: the contrarian pass

26 September 2026. The user's instruction: seven years of the same approach have
failed, so stop doing what everyone does and look for what everyone missed. This doc
records that pass. It found **one structural fact the dossier had wrong** (faed is not
one homogeneous object), closed several never-tested readings, and pulled the primary
pages from the Wayback Machine so their exact wording is in the repository. No lock
opened. Harness: doc 115's, controls fired on every screen.

## 1. faed is not homogeneous: it is several pieces

The dossier (section 6.4) carries faed as one object, "filler from a fixed biased
generator", homogeneous at p = 0.45 over 19 blocks. That test used 30-character blocks
and had little power. Larger windows show the letter mix drifting along the string,
and a permutation test confirms it:

| test | statistic | permutation p |
|---|---|---|
| 2 equal parts, G-test of homogeneity | 17.6 | 0.029 |
| 4 equal parts | 59.0 | 0.0018 |
| best single cut (searched), at 540 | 30.9 | 0.010 |
| best 2 cuts (searched), at 220, 540 | 51.5 | 0.007 |
| best 3 cuts (searched), at 220, 435, 540 | 70.5 | < 0.017 (0 of 60 null searches reached it) |

The pieces the search finds:

| piece | length | signature |
|---|---:|---|
| [0, 220) | 220 | `g` 22%, `h`+`i` 14%, `a` 14% |
| [220, 435) | 215 | `g` 21%, `h`+`i` 29%, `a` 7% |
| [435, 540) | 105 | `g` 12%, `b` and `e` up |
| [540, 570) | 30 | **no `e`, no `g`**, `h`+`i` 47% (the dossier's "last 32" anomaly, p = 0.004) |

Under the null of one generator, the whole string's composition is the same
everywhere. It is not. So faed is a **concatenation of differently composed parts**,
which is what a *list* looks like, and `matrixsumlist` is the label that sits between
dbbi and faed. The dossier's residue argument (the dbbi residue "carries faed's
signature excess of `g`") compared against faed as a whole; against the pieces, the
residue (g 17%) matches the first two pieces, not the last two.

**What this changes.** faed goes back from "filler" to "unread payload with internal
structure". The cut positions are search results, not proven boundaries (a 5-step grid,
minimum piece 30), so the next step is to find boundaries from the data itself rather
than from composition: a per-piece decode under rule 2 was tried at these four cuts
and is noise (printable 0.23 to 0.40, forward and reversed; `claude/scripts/118/faed_pieces.py`),
which says only that these cuts are approximate or the encoding is not rule 2.

## 2. Readings tested for the first time, all null

| reading | why it was worth a test | candidates | result |
|---|---|---:|---|
| **zero insertion** at prime positions of faed, dbbi, the residue and dbbi+faed, before or after the index, counted in the input or the output stream, 0- and 1-based, then rule 2 | the Architect text says "REINSERTING the prime basics"; every earlier test substituted or deleted, none inserted | 96 decodes | printable 0.38 to 0.62, all inside the 570-digit null (median 0.37, max 0.48 on shorter strings) |
| deletion of, and restriction to, prime positions, then rule 2 | same hint | included above | noise |
| a..i as 0..8 (so `a` is the zero, "zeroed out") in base 10 and base 9; bijective and packed readings; digit pairs | the relabeling sweeps used 1..9 | 40 | noise; the residue's 0.93 "printable" under digit pairs is forced by the pair range 11..99 |
| best-grouping A1Z26 over faed's digits (dynamic programme against English letter frequencies) | never tried | 3 objects | at the digit-forced baseline |
| whole objects hashed as the password: the 1,075-character textarea and its parts, the Architect text, the checkerboard message, the phase-2 plaintext, the intro, the riddles, the chain of all four earlier passwords and of all four answers | "it's in front of your eyes" | 36 | 0 |
| the Matrix's own first hint ("Wake up, Neo... The Matrix has you... Follow the white rabbit. Knock, knock, Neo."), the site's robots.txt line, the bunny-hunter comment, the labels as bare words, `HASHTHETEXT`, `{1},{4},{21}`, `RAB`, `1812`, `42`, `127` | "our first hint is your last command" read as the film's first message, which is itself a command | 92 | 0 |
| the poster read row-major and column-major (bits, bytes, inverted, reversed), its row and column sums as strings and lists, the total 101 | `sum(matrix, [])` flattens a matrix; nobody had hashed the flattened grid | 23 | 0 |
| the words before each "choice" in the Architect scene: the Architect's first mention ("as long as they were given a"), the words before Neo's "Choice. The problem is choice.", the door speech, the "moment of truth" line; last 1 to 30 words, four forms, alone and crossed with the labels | the dossier's earlier film tests used the door speech only | 3,816 | 0 |

## 3. The pages themselves, from the Wayback Machine

Fetched on 26 September (captures of 2023-06-01 and 2022-12-23) so the wording is on
record rather than paraphrased.

**The side page** is two headings and two textareas and nothing else: `<h1> SalPhaseIon </h1>`,
the soup with one space between every character, `<h1> Cosmic Duality </h1>`, the
container wrapped at 64. No prose, no comment, no form, no hidden element. The page
gives no instruction beyond what the soup decodes to.

**The choice page** (phase 2 and 3), verbatim where it matters:

- `"1... are you looking for the private keymaker?" You come to me, without it. Come to
  me with it and you'll have the power to continue. It'll grant the first part.
  /(aaa, connected enf)`
- `Ciphered with aes-256-cbc /w base64 sha-256(password)`
- `--> parts 1..7 --> sha-256 -> dgst is the password to enter Phase 3. Phase 3 is also
  ciphered with aes-256-cbc /w base64.`

The `1...` carries three dots. The dot table in dossier section 7.3 does not list it;
it reads as the part number followed by an ellipsis, but it is now on record.

**A reading of the soup as a sentence.** In page order the decoded pieces say:
`matrixsumlist` | `lastwordsbeforearchichoice` | `thispassword` | `sha256 our first
hint is your last command` | [container] | `enter` | [container] | `sha256 the
answers too`. Read straight through, "last words before archi choice: this password"
is a statement, and "sha256 ... the answers too" says the answers are hashed. The
dossier's model (two operations feeding one hash) is one reading; "the password is the
last words before the choice, hashed" is the plainer one, and every literal candidate
for it is spent (sections 10.5 to 10.7, and section 2 above).

## 4. "Infrared": the region below the red line, examined

#6250 "Infrared" answers Janusz asking whether to XOR the colours "or we need sum for
red" (#6247 to #6249), followed by "No hints 🤡". Read literally, infra-red is what
lies below the red divider: the lower panel, which the dossier's audit (section 4.6)
explicitly left unexamined as a data surface. Examined now from the verified file:

- The panel is `#F5F5F5` with four bands: a 5-row white strip, the logo and title
  (rows 1112 to 1252), the QR and address (rows 1289 to 1519), a 3-row white strip.
- The title and the address are Windows ClearType text: four gray levels and the
  standard orange/blue subpixel fringes (`F5AF62`, `388AD2`, `62AFF5`, `D28A38`) on
  every glyph edge. No glyph uses a level or a colour the others do not; no isolated
  pixel; no rare gray value.
- The QR region has nine colours, all module edges; it re-encodes exactly (doc 115).
- The logo is a 371-colour anti-aliased hexagon with no foreign palette.

Nothing below the red line carries a mark. "Infrared" stays what its context makes it,
a quip at "sum for red".

## 5. Where this leaves the puzzle

The one thing everyone (this project included) assumed and which the data contradicts
is that faed is uniform filler. It is four differently composed pieces in a row, under
a label that names a list. The dossier's section 9 model already puts `matrixsumlist`'s
operand "outside the page"; the pieces say the operand may be on the page after all,
and the operation is to read the list. What is not known: the true boundaries, the
per-piece encoding, and what the pieces mean. The boundary at 540 is the firmest (the
30-character tail with no `e` and no `g`); the tail is 30 characters over seven
symbols, which is the size of a short string, not of filler.

Everything else in this pass closes a reading rather than opening one, and the
closures are worth keeping: zero insertion, the flattened matrix, the film's other
"choice" lines, the region below the red line, the whole objects as passwords.

## 6. Follow-up: boundaries from the data (same day)

Pushed as far as the data allows in one session. Everything below is a permutation
test against shuffles of faed or a decode with a printability score against the
570-digit null (median 0.37).

| test | result |
|---|---|
| faed as a **sorted list** of fixed-width numbers (the drift looked like leading digits rising): descents between consecutive chunks, widths 1 to 6, every offset, `g` as 7 and as 0 | at chance everywhere (z between -2.3 and +0.8; no width beats the null cleanly) |
| faed as an **interleave** of k streams, k = 2 to 10 (residue classes of position) | no split is inhomogeneous (k = 2 p = 0.08, the rest above 0.15) |
| longest **absence** of each letter | `h` absent for 62 characters at [63,125), `i` absent for 49 at [323,372), `a` for 59 at [216,275), `d` for 59 at [53,112), `g` and `e` for the last 32; each about 0.08 to 0.25 expected on its own |
| the **dominant letter** in sliding windows of 60 and 90 | `g` at 20 to 28% from 0 to about 250, then `h`/`i` to about 315, then `g` again to about 405 (up to 32%), then `e` to about 465, then `b`/`i`, then `i`/`h` in the tail. The over-drawn letter changes along the string |
| each piece decoded under rule 2 with its dominant letter as the hidden zero, and as its own digit, forward and reversed (10 piece definitions) | printable 0.21 to 0.55, noise |
| **successive differences and pair sums** mod 9 and mod 10 (a running-sum reading of "sum list") | uniform, no digram structure (permutation p 0.28 to 0.70) |
| **hand-typing signature** on a QWERTY layout: adjacent-key digrams, repeated letters, left/right hand alternation | adjacent keys +1.7 sigma, alternation -1.9 sigma, repeats +1.0 sigma: all in the direction a person mashing keys produces, none decisive |

**Reading.** The drift is real, and it is not a sorted list, not an interleave, not a
running sum, and not four rule-2 numbers with a per-piece zero. Two explanations
remain and the data does not separate them:

1. faed is a list of differently encoded pieces whose encoding is not rule 2 (the
   over-drawn letter changes from piece to piece, which is what a per-piece
   substitution or a per-piece zero letter would produce).
2. faed was **typed by hand**. A person mashing keys drifts between favourite keys
   over time, holds a key now and then (`gggg`, `ggggg`), favours one hand (seven of
   the nine letters are left-hand keys; `g` is the left index finger's reach), and
   produces exactly this kind of inhomogeneity with no digram structure. The creator
   built the puzzle in "a couple hours" and "rushed (t)it".

Under explanation 2 the dossier's "filler" verdict is right for the wrong reason, and
faed carries nothing. Under explanation 1 the pieces are the operand of
`matrixsumlist`. The test that separates them is a decode that reads, and none has.
The boundaries as best the data gives them: about 250, 315, 405, 465 and 538 (the
window analysis), or 220, 435, 540 (the likelihood search); both put a cut near 540.
