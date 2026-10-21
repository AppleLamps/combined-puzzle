# GSMG puzzle session log — records 135–140: actual solve attempts

Following record 131-134's verification work, the user explicitly asked for
a genuine solve attempt, not just infrastructure verification. This log
records six independent, named candidate families tested against all three
locked containers this session, each with controls confirmed before and
during the run. **None succeeded.** Puzzle remains unsolved.

**Third revision (same session, PR #3 review).** A reviewer (Codex) caught
that `test_candidate` never deduplicated: different generators in one script
routinely emit the same string (a 1-character window and a 1-word window are
both the same letter; concatenated word windows overlap character windows),
and each repeat was decrypted and, when it collided, *counted* again. The
harness now dedupes on exact candidate bytes and reports
"distinct candidates actually tested (N duplicate invocations skipped)".
Re-running all six scripts: records 135 (148→132 distinct), 136 (180→164;
and its hit count drops from 8 to 5 — three "hits" were one candidate
counted three times), 139 (140→137) and 140 (175→140) were inflated;
137 and 138 had no duplicates. **Candidate and hit counts below are the
deduplicated final numbers.** Totals: 2,061 distinct candidates, ~24,700
primary decrypts. Every verdict is unchanged: null.

**Second revision (same session, PR #2 review, round 2).** A second
automated reviewer (Copilot) then found the first revision's own scripts
had a real bug: every `attempt_*.py` script's final verdict was gated on
`if not all_hits`, but `all_hits` included the routine pad-1/pad-2 chance
hits — so none of the six scripts could ever actually print `NULL`, even
though the write-up said they did. Centralized the fix in a new
`harness.report()` used by all six: it still prints every hit for
transparency, but the NULL verdict is now gated on *meaningful* hits only
(`findings` non-empty or `pad>=3`) — confirmed all six now correctly print
`NULL`. The same review also caught record 137's `BUT`/`HYE` keys being
mislabeled `a1z26` while actually computed as 0-indexed (A=0) values;
fixed by adding the genuinely 1-indexed A1Z26 variants alongside the
original (correctly relabeled `vigkey0`) ones. It also caught record
139's label-subset test only trying each subset's textarea-order
concatenation, not every ordering of it (fixed: now permutes each
subset), and record 136's matrix-width sweep excluding the two degenerate
endpoint widths 1 and 1,539 (fixed: both now included). **Numbers below
are final, after both rounds of review fixes; all still null.**

**First revision (same session, PR #2 review, round 1).** An automated review of the
solve harness (3 P1 findings, all legitimate) identified that it was
weaker than the dossier's own established methodology in three ways: it
only tested the EVP-SHA256 KDF digest and never EVP-MD5 (which the
dossier's own harnesses test as a matter of course, since the unopened
containers' KDF digest is not established); its recognizer omitted the
dossier's calibrated bit-position-bias and distinct-byte-deficit
statistical tests; and it never chained a valid-padding plaintext as a
candidate password against the *other* two containers, which the dossier
explicitly requires because a correct short binary intermediate can look
exactly like random noise until it opens the next lock. All three were
fixed in `tools/gsmg_solve/harness.py`: both EVP digests are now tried for
every candidate (roughly doubling decrypt volume), the recognizer now
includes both missing statistical tests (each independently controlled:
ASCII text's bit7 always 0 fires bit-bias, a two-byte repeating buffer
fires distinct-byte-deficit), and every valid-padding hit is now
automatically chained (raw bytes / hex-of-bytes / sha256-hex, both
digests) against the other two containers up to depth 2, with a new
`run_chaining_control()` mirroring the dossier's own stated control (a
random plaintext whose hex encoding keys a second envelope holding UTF-16
text — confirmed found). All six candidate families below were re-run
under the strengthened harness; **results and hit counts below are the
final, strengthened numbers**, not the original weaker ones.

## Harness and controls (used for every record below)

A fresh harness (`try_password` / `test_candidate` in this session's
scratchpad, built on `tools/gsmg_verify/lib.py`) was used for every attempt:

- **Positive control**: `causality` still decrypts the real phase-2
  textarea to the pinned plaintext (sha256 `e2f9dd65...`). Confirmed PASS
  before every run.
- **Negative control**: a known-wrong password produces no valid PKCS7
  padding on any of the three containers. Confirmed PASS before every run.
- **Recognizer controls**: the content-recognizer (printable-ASCII,
  EBCDIC across 6 codepages, UTF-16 zero-byte alternation, magic headers,
  and — critically — scanning every 32-byte window of any valid-padding
  plaintext as a raw private key against both the prize and sentinel
  HASH160 targets) was itself controlled: confirmed it does NOT
  false-fire on 20 random 80-byte buffers, DOES fire on planted ASCII,
  EBCDIC, and UTF-16 text, and that the raw-key-window scan mechanism
  correctly detects an embedded known scalar (verified against the public
  scalar=1 test vector, since the real prize scalar is unknown by
  definition). Confirmed PASS before every run.

Every candidate was tried under two password profiles (the proven
`sha256(answer)`-as-64-hex-ASCII convention, and the answer's raw UTF-8
bytes directly as the openssl passphrase, in case a short answer isn't
hashed) against all three containers (Terminal, SalPhaseIon-short, Cosmic
Duality). A "hit" required either `findings` from the recognizer (content
match) or `pad >= 3` (the dossier's own noise threshold — pad=1 or pad=2
alone is expected roughly 1 in 255 tries and is not evidence).

## Record 135 — words before "SELECT" in our own verified Architect text

**Derivation.** `lastwordsbeforearchichoice` decodes to that literal
25-character string (verified, section 6.2). The puzzle's own 1,539-letter
Architect text (independently re-derived from the real ciphertext this
session, see record 131) contains no literal word `CHOICE` at all — the
film's door-choice scene is deleted. But it does contain the one
CHOOSING-verb in the text: `SELECT` ("...AFTER WHICH YOU WILL BE REQUIRED
TO SELECT FROM OVER TWENTY THREE CIPHERS..."). This session fetched the
actual Matrix Reloaded Architect-scene transcript (scottmanning.com) live
and confirmed this phrasing matches the film's own line ("After which you
will be required to select from the matrix 23 individuals...") almost
verbatim — so the segmentation is not guesswork.

**Candidates.** Character-count windows of 1–60 characters ending
immediately before `SELECT` in the canonical text (both cases), plus
hand-segmented word windows of 1–7 words ("TO", "REQUIRED TO", ...,
"AFTER WHICH YOU WILL BE REQUIRED TO"), concatenated and space-separated,
both cases. **148 distinct candidate strings.**

**Result.** 148 invocations, **132 distinct candidates** (16 duplicates
between the character and word windows) × 3 containers × 2 password
profiles × 2 EVP digests = 1,584 decrypts. 5 valid-padding hits, all pad=1,
zero recognizer findings (bit-bias/distinct-byte-deficit included). 0 of
the 5 chained to either other container. **NULL.**

## Record 136 — Architect text reshaped as a matrix, row/column sums

**Derivation.** `matrixsumlist` decodes to that literal string (verified).
1,539 = 3⁴ × 19, with divisors {3, 9, 19, 27, 57, 81, 171, 513}. For each
divisor width, the Architect text was reshaped into a rectangle and its
row sums and column sums computed under two letter-value conventions
(A=0/A=1), then turned into candidate strings four ways: sums mod 26 as
letters, sums as two-digit-pair strings, and the sums written out as a
plain comma-separated list (a literal reading of "matrix sum list").
**144 distinct candidate strings.**

**Result.** 180 invocations, **164 distinct candidates** (10 widths
including the two degenerate endpoints 1 and 1,539; the endpoints and the
A=0/A=1 conventions produce 16 repeats) → 1,968 decrypts. **5 valid-padding
hits** (an earlier draft said 8; three were one candidate counted three
times), all pad=1, zero recognizer findings, 0 chained hits. **NULL.**

## Record 137 — dbbi's macro key (574061 / [23,16,7] / BUT / HYE) as a Vigenère/Beaufort key over the SELECT window

**Derivation.** Rather than testing the "last words before SELECT" text
raw (record 135), this keys it: the review-124 macro derivation (poster
colour sequence → 574061 → digit matrix → [23,16,7] → boundary words
BUT/HYE) gives four candidate key streams (`574061` digits, `231607`
digit reordering, and the A1Z26 values of `BUT`/`HYE`). Each was applied
to the SELECT-anchored windows (length 2–40) as a repeating-key Vigenère
(both directions) and Beaufort cipher.

**Candidates.** 39 lengths × 6 keys (574061-digits, 231607-digits,
BUT/HYE as both a standard 0-indexed Vigenère key and, after a review
correction, the genuinely 1-indexed A1Z26 values) × 3 operations × 2 cases
= **1,404 distinct candidate strings.**

**Result.** 1,404 candidates → 16,848 decrypts. 60 valid-padding hits
(pad=1/2), zero recognizer findings. 2 of the 60 chained to a second
container with valid padding, but with zero recognizer findings and
pad=1 on the chained decrypt too. **NULL.**

## Record 138 — faed reshaped as a matrix, row/column sums

**Derivation.** `matrixsumlist`'s decoded position in the textarea sits
immediately before `faed` — the most spatially direct reading of "here is
a matrix, sum it" is faed itself, not the Architect text. 570 = 2×3×5×19,
giving 14 nontrivial divisors. Note: the dossier's own doc 96 already
reports "faed as a matrix: row and column sums at every width dividing
570, as ASCII: 28 lists, noise" — 14×2=28 matches exactly, so **this
family very likely overlaps prior work**; the encodings tried here (sums
as raw bytes, sums via the textarea's own established rule2 decimal→hex→
ASCII convention, and sums mod 26 as letters) may or may not be the exact
"as ASCII" reading doc 96 used, so it was run anyway as a cheap check,
with this overlap flagged per the "if uncertain, say so" instruction.
**84 distinct candidate strings.**

**Result.** 84 candidates → 1,008 decrypts. 3 valid-padding hits, all
pad=1, zero recognizer findings. 1 chained to a second container (pad=1,
no findings). **NULL.**

## Record 139 — the five decoded labels themselves, literally, alone and combined

**Derivation.** The most literal possible reading of the whole exercise:
maybe the answer is simply the decoded label text itself. Tested each of
the five `#8446`/textarea labels alone; every non-empty subset and
ordering of `matrixsumlist`/`lastwordsbeforearchichoice`/`thispassword`
(the three labels actually co-located with the unopened SalPhaseIon-short
container); and all 120 permutations of the full five-label set.

**Candidates.** 5 (alone) + 15 (every subset **and every ordering of it**,
after a review correction — 3+6+6 for subset sizes 1/2/3) + 120 (full
5-label permutations) = **140 distinct candidate strings.**

**Result.** 140 invocations, **137 distinct candidates** (the three
single-label permutations repeat the label-alone tests) → 1,644 decrypts.
7 valid-padding hits, all pad=1, zero recognizer findings. 0 chained hits.
**NULL.**

## Record 140 — the literal word "Choice" in the film, one level up from SELECT

**Derivation.** A live fetch of the Architect-scene transcript (this
session; not from memory) shows the literal word "Choice." is spoken by
Neo, not the Architect, immediately after four lines of other-Neos'
monitor dialogue ("You can't control me! Fuck you! I'm going to kill you!
You can't make me do anything!"). This is the *only* verbatim occurrence
of the word "choice" in this transcript, and — unlike the SELECT anchor —
it directly matches the literal word inside "archi**choice**". These
monitor lines are not part of the Architect's own speech and so don't
appear in the puzzle's word-for-word-aligned custom text at all; this
candidate uses the film's wording directly, on the theory that
"archichoice" points at the film scene itself rather than at the puzzle's
rewritten copy of it.

**Candidates.** Word windows of 1–17 words before "Choice." (concatenated
and space-separated, both cases) plus character windows of 1–56 characters
(both cases). **175 distinct candidate strings.**

**Result.** 175 invocations, **140 distinct candidates** (35 duplicates
between the word and character windows) → 1,680 decrypts. 6 valid-padding
hits, all pad=1, zero recognizer findings. 0 chained hits. **NULL.**

## Totals and honest assessment

**2,061 distinct candidate strings (2,131 invocations), ~24,700 primary
decrypt operations** (three containers × two password profiles × two EVP
digests) **plus lock chaining of every valid-padding hit against the other
two containers. All null** — every primary hit was pad-1 (or one pad-2), the content
recognizer (printable, EBCDIC, UTF-16, magic headers, bit-position bias,
distinct-byte deficit, and a raw-key-window scan — independently confirmed
working via its own controls, including the chaining mechanism itself)
found nothing in any successfully-padded plaintext, and the handful of
chained secondary decrypts (3 total, from records 137 and 138) were
themselves unstructured pad-1 noise with zero recognizer findings.

**What this does and doesn't show.** These six families were chosen because
each names a specific, motivated derivation rather than blindly guessing,
and two of them (SELECT-anchor, film-Choice-anchor) are, as far as this
session could determine, distinct from the character-window sweeps already
recorded in dossier sections 10.6/10.7 (which most likely anchor on the
Architect text's YOU/ME speaker-turn markers, not on SELECT or on the raw
film transcript). The faed-matrix family (record 138) most likely does
overlap prior work and is reported as a probable duplicate rather than a
new negative. None of this proves the underlying ideas (SELECT as the
"choice", faed/Architect-as-matrix, the 574061 macro as a cipher key,
literal label concatenation) are wrong — only that these specific encodings
of them, at these specific window lengths, are not the container's password.

**The puzzle is still unsolved.** No candidate this session reproduced the
prize HASH160, matched the sentinel, or produced recognizably structured
plaintext on any of the three containers.
