# What the GSMG.io 5 BTC puzzle group has been doing wrong

An audit of the Telegram export (2019-04-20 to 2026-09-08, 61,349 messages), the
two Reddit threads, and the Bitcointalk topic.

Short version: the group's front line has been resting on a false positive since
June 2025, it entered the endgame through a side door without solving the stage
that produces the data the endgame needs, and it has never re-derived its own
inherited assumptions. Below, each claim is backed by evidence and, where
possible, a script you can run.

---

## 1. "btcseed" is a coincidence, and it is currently the group's main anchor

**The claim in the chat.** In June 2025 a Bifid decode of the `faed...` string
(period 570, keyed by the deduplicated head of `dbbi...` -> `dbifhceg`) produced
a 570-character output beginning `btcseed`. The chat computed the odds of that
at "1 in 8,031,810,176" (`2025.txt:32240`), and by 2026 it is written up as
"SEG-0 / SEG-1 — solved & creator-confirmed" (`2026.txt:60065`). The current
open-problem list is built on it: "Consumer of the 96-state object — how to
convert the btcseed matrix into a seed or private key" (`2026.txt:65086`).

**It reproduces.** I confirmed the decode exactly.

**It is not rare.** Run `analysis/verify_btcseed.py`:

- Of the 40,320 orderings of the *same eight key letters*, **480 (1.19%)** put
  `seed` in the first eight characters. Four of them give exactly `btcseed`.
- Sibling keys produce `faeseed`, `fadseed`, `facseed`, `fagseed`, `fahseed`,
  `fabseed`, `ehfseed`, `eogseed`... The `seed` is nearly key-invariant; only
  the first three letters move. Several of those prefixes just echo the
  ciphertext's own opening (`fae`, `fad` from `faed...`).

So the true rate is ~1 in 84 within one narrow key family, before counting the
periods, ciphers and keyword variants that were also searched. The quoted figure
is off by about eight orders of magnitude. It is the classic error: computing
the probability of the specific thing you found, after searching a large space
for anything that looked meaningful.

**The "96-state object" is an artifact of the group's own transform.** The tail
after `btcseed` has only four distinct letters at alternating positions, which
the chat reads as a 4-state / 96-state / "281 states" structure. That same
structure appears when you decode with `abcdefghi` or `hgfedcbai` as the key —
nonsense keys. It is what Bifid does to a 9-letter-alphabet ciphertext at period
= ciphertext length. There is no message in it.

**The provenance claim is false.** The creator has never written the words
"btcseed" or "Bifid" in any of his 521 messages across seven years. "Creator-
confirmed" was invented, almost certainly by an LLM write-up that then got
treated as record.

**Cost:** roughly fifteen months, and it is still the frontier.

---

## 2. The group is standing in a room it entered through the window

Salphaseion was never reached by solving the puzzle. It was reached by hashing
`"GSMGIO5BTCPUZZLECHALLENGE" + 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` and using the
digest as a URL — the "second door" from the Decentraland hint. I verified the
hash: it gives `89727c59...52f6a32`, the known page. Members said so at the
time: "i wouldnt say salph is 3.2.2 because you dont need 3.2 or any previous
steps to reach it" (`2024.txt:12078`).

Phase 3.2 itself has never been solved. Members said this plainly in September
2026: "3.2 is most definitely NOT solved" and "funny that we were able to skip
ahead, isn't it???" (`2026.txt:65013`).

The creator's own instructions inside Salphaseion say the solver arrives
carrying something: *"a temporary dissemination of the code you hopefully
carry"*. The group is not carrying it. Everything since 2021 has been an attempt
to brute-force the last door with the key still sitting in the room they
skipped. "Jrk performed his best in 3.2 phase para, like beauford, ebcidc, vic
cipher just to provide an aes blob? We are missing something" (`2026.txt`,
#71200) is, I think, exactly right.

---

## 3. A hint was misread as its opposite, and the misreading stuck

The Salphaseion text says:

> **REINSERTING THE PRIME BASICS**

In December 2021 the creator added: *"some characters need to be 'zeroed out'"*
(#8000). The 2023 chat converts this into "I've tried replacing all digits in
prime locations of dbbib with 0" (`2023.txt:5068`) and that reading has been
the default ever since.

But *reinserting* is not *replacing*. The evidence favours insertion:

- The confirmed encoding for this stage is a=1..i=9, o=0, digits read as a big
  integer, then as hex, then as ASCII. I re-derived it from scratch: it turns
  `agdafaoahe...` into `lastwordsbeforearchichoice` and `cfobfdhgdo...` into
  `thispassword`. Both of those contain `o`.
- `dbbi...` and `faed...` contain **no `o` at all**. Their zeros are missing.
  Noticed in 2023 (`2023.txt:5130`) and again in 2024 (`2024.txt:30194`).
- The arithmetic is clean. To insert a zero at every prime position: 91 letters
  needs total length **121** (= 11²), 570 letters needs **695**. Both are exact.

I tested it and it did not yield plaintext.

**Correction, and a caution about this whole finding.** An earlier draft called
the replacement reading a five-year blind spot. It was not: ArchOptic wrote
"Maybe zeroed out = insert" in November 2024 (`2024.txt:53146`). The insertion
reading has been on the table. Around 136 messages across 2023-2026 work this
hint. Treat it as heavily trodden ground, not a fresh lead.

Two further reasons to rank it low:

- **The hint's own text is not trustworthy.** Message #8000 carries an edit
  timestamp of **2026-02-15** — four years and two months after it was posted.
  That is precisely the anomaly this document flags in Finding 5, and it applies
  to the sentence being parsed. Nobody, including this audit, can currently say
  the wording was the wording.
- **`dbbi`/`faed` are in SalPhaseIon — the side branch.** Working them is the
  thing this document argues against everywhere else, and it is the exact soil
  btcseed grew in. One member reached the sharper doubt in November 2024
  (`2024.txt:37724`): since SalPhaseIon was already known when the hint was
  given, "primes" and "zeroed out" may point at door 3 or the 3.3 blob rather
  than at dbbi/faed at all.

Related and unexamined:
the group's very first stumble in this puzzle was the creator's `giveit` /
`givetit` typo, which required **adding one character between the answers**. The
same shape recurs: `dbbi` is 91 letters; `lastwordsbeforearchichoice` (63) +
`thispassword` (29) is 92. One character apart.

---

## 3b. The earliest orphan: `# X 2 S H 4 Y 0 Q B 15 #`

Phase 2's plaintext ends with a ten-token block and riddles for four of its
tokens. Run `analysis/x2sh.py`.

What is solid: **S = 32** (Klingon, `cha' + vagh*jav`), **H = ±42**
(Hitchhiker's, negated), **Q = 82** (Qwerty is Elliot's fish in Mr. Robot;
extend to QWERTYUIOP under the digit row, where I sits under 8 and W under 2),
**B = −16** (the part number is an Intel Core i5-750, so `(5i − i)² = (4i)²`).
Signs on H and B are still argued.

**X and Y are the only tokens the puzzle never writes a riddle for.** It defines
exactly what it wants substituted and leaves two unknowns.

And nothing ever consumes it. The Phase 3 password is the seven clue-parts —
causality / Safenet / Luna / HSM / 11110 / genesis hex / chess FEN — and X2SH is
not among them. It is the earliest thing in the chain that was walked past:

> 2021: "it is still uncertain what that is for"
> 2023: "X 2 S H 4 Y 0 Q B 15 doesn't seem usefull as well to go to phase 3"
> 2026: still being argued on the final day of the export

Two readings have been tried and both miss by a hair. As coordinates for the
ex-SafeNet building in Rotterdam they are "several hundred meters off … assuming
the coordinates go down to seconds we should have a match down to a meter
accuracy" (2023). As Decentraland parcels, pairing to (2,0) (32,82) (−42,−16)
(4,15), the GSMG estate is at (−41,−16) and (−41,−17) while the block gives
(−42,−16) — one parcel east. The solver's own verdict in September 2026: *"jrk
didn't make the coordinates land directly on the old safenet address either …
strong argument for 'we got our interpretation wrong thinking we are right
here'."* In a puzzle where every other answer lands exactly, a near-miss is a
wrong reading, not a sloppy author.

**The thread that was dropped.** Phase 3.2's VIC hint reads: *"A fubcd-king &
oracle-queen, thingky mvps, on a sad board but **as wide as the first one
seen**."* In September 2023 a member asked what that first board is, ruled out
the rabbit matrix (14) and the chess board (8), and named X2SH as a candidate.
The answer he got was "I don't think we've figured that out yet." Nothing since.

| width | board | when you meet it |
|---|---|---|
| 14 | rabbit matrix | phase 1 |
| 8 | chess position | phase 2, part 7 |
| **10** | QWERTYUIOP over the digit row | phase 2, inside the Q riddle |
| **10** | the X2SH block itself | phase 2 |
| **10** | VIC straddling checkerboard | phase 3.2.2 |

The X2SH block is ten tokens, and the Q riddle inside it constructs a ten-wide
board. Those are the first ten-wide objects in the puzzle, and the VIC
checkerboard is ten wide. This is a lead, not a solution — the VIC decode
already succeeded without it. But in seven years nobody has tested whether X2SH
is the board that hint points at, and it is the only orphan early enough to be
carrying something the endgame still wants.

## 4. There is no verified shared state, so nothing ever gets re-derived

The canonical reference is still `github.com/puzzlehunt/gsmgio-5btc-puzzle`,
last meaningfully current around 2020-2021 ("Whoever is running the GitHub has
not updated it in a while", `2023.txt:10206`). Everyone who arrives after that
inherits its interpretations as facts and starts from the frontier.

The symptoms are everywhere in the log:

- "no progress since May 2021", said in August 2023 (`2023.txt:10200`). Still
  true in September 2026.
- `# X 2 S H 4 Y 0 Q B 15 #` is from **stage 2**. It was never fully solved, was
  walked past, and members were still arguing about what `B` means on the last
  day of the export (`2026.txt`, #71218).
- Volume replaced progress: 228 messages in 2022, then 8,587 / 14,237 / 15,957 /
  15,441 in 2023-2026. AI mentions went 27 -> 71 -> 81 -> 194. Six numbered
  "Gsmgpanishad" dossiers circulate. Members have noticed —"people claiming
  they'd solved it only for us to find it was llm hallucinations"
  (`2026.txt:7560`) — but the dossiers are still the working documents, and one
  of them is where "creator-confirmed" came from.

Nobody maintains a list of *what has actually been verified, by whom, with what
script*. That is why a 2025 false positive is still load-bearing in 2026.

---

## 5. Concrete creator hints that were dropped

From all 521 creator messages, these got one reply or none and were never worked:

| # | Date | Message | Context |
|---|---|---|---|
| 4105 | 2020-05-21 | **"First or zero"** | Direct answer to "the answer to another door from the 1st piece". An indexing instruction for the second door. Mentioned once more, in 2023, then never again. |
| 3404 | 2020-04-08 | **"And Oen"** | Reply to "Neo is anagram for One". Two mentions in 2020, nothing in the six years since. |
| 6250 | 2021-03-05 | **"Infrared"** | Dropped bare between two "no hints" jokes. |
| 6913 | 2021-04-01 | **"R=18 A=1 B=2 ... could also be 21 or 1812 bit"** | Discarded as an April Fools joke because #6884 above it was one. #6913 is a separate message. |
| 66574 | 2026-07-12 | **"NOTE: that is a hint."** | Explicitly flagged, attached to "my close friends have the best chance of solving it... they don't have the skills some of you do", alongside "Some of you can find me. Quite a few in this chat already met me." The chat argued about what it *meant* and never tried anything. |

The last one is the only hint in seven years the creator labelled as a hint.
Read with "I have a hidden laptop... on that thing is the actual answer" (#66568)
and "technically my friends and family can get to all my data if they'd work
together" (#9595), it points at something personal and low-skill-accessible —
not another cipher.

---

## 6. The creator has been quietly editing his 2019-2022 messages

Run `analysis/audit_creator_edits.py`:

| | messages 2019-2022 | edited >=2 years later | rate |
|---|---|---|---|
| all users | 6,487 | 241 | 3.7% |
| **creator (user9815232)** | **223** | **79** | **35.4%** |

**9.5x the baseline.** 63 of those edits are dated 2025, 28 more in 2026 — i.e.
recent, and concentrated on the hint-bearing messages: #77, #866, #867, #871,
#879, #881, #1710 (the Roses hint), #1837 ("Only -41,-17 matters"), #3404,
#4105. Editing a two-word message five years after posting it is not
housekeeping.

In 61,349 messages the group noticed this once, as a joke (`2026.txt:6434`).

Caveat, stated plainly: an edit flag records that a message changed, not what
changed, and Telegram does not expose edit history. This is a lead, not a
finding. But it is cheap to chase — the 2020-2021 GitHub write-ups, the Reddit
quotes, and any older export are independent copies. If any hint text differs
from what the group has been working from, that alone could explain seven years.

---

## What I would actually do next

1. **Retire `btcseed`.** Run the script, publish the numbers, and stop building
   on the 96-state object. It is the group's own transform reflected back.
2. **Go back and solve Phase 3.2 properly.** The endgame expects data the side
   door never handed over. This is the single highest-value unblocked task and
   it has been skipped for five years because Salphaseion was more exciting.
3. **Diff the hints against external archives.** Cheap, mechanical, and if it
   turns up anything it reframes everything.
4. **Re-test "reinserting the prime basics" as insertion,** not replacement —
   at 121 and 695 digits, and with the neighbouring off-by-one variants.
5. **Keep a verified-facts file in git.** Every entry: the claim, the script
   that reproduces it, who checked it, and a false-positive estimate. Anything
   without a script is a hypothesis, including anything an LLM wrote.

A note on method that covers all five: this puzzle rewards search, and search
over a large space *always* returns something that looks like a message. Before
a find becomes an anchor, measure how often the same procedure returns
something equally good from noise. `btcseed` would not have survived one hour of
that discipline, and it has had fifteen months.

---

# Addendum: where to restart

## The last point the group had proof it was right

**Correction to an earlier draft of this document.** It said Phase 3.2's blob had
never been solved and that Phase 3 was the last proven step. That is wrong, and
the error mattered enough to fix in place rather than bury.

Phase 3.2's *envelope* was decrypted in 2020 and the chain is real. Phase 3's
plaintext poses three riddles — Jacque Fresco, "giveit"/"just one second" from
Alice, and Heisenberg — whose answers concatenate and hash to
`250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c`, which opens
it. Verified here with openssl (`analysis/blobs.py`). Both sections inside it are
solved too: 3.2.1 through EBCDIC-1141 then Beaufort keyed `THEMATRIXHASYOU`,
giving the "YOUR LIFE IS THE SUM…" speech; 3.2.2 through a VIC cipher whose
alphabet comes from "fubcd-king & oracle-queen, thingky mvps", giving
`INCASEYOUMANAGETOCRACKTHIS…`.

Phases 1 → 2 → 3 → 3.2 are all self-validating: each ends in a clean AES decrypt,
and a clean decrypt is a checksum.

**What is actually still encrypted is exactly two AES-256-CBC blobs:**

| blob | salt | ciphertext | status |
|---|---|---|---|
| Phase 3.2, inner — the main line | `b45a5e3d827593ca` | 80 B, 5 blocks | never opened |
| SalPhaseIon — the side branch | `3ab585348552415d` | 80 B, 5 blocks | never opened |

So the first unproven joint is the **Phase 3.2 inner blob**, not the envelope.
That does not weaken the restart argument, it sharpens it: the inner blob is the
main line's continuation, and SalPhaseIon is the branch reached through the side
door. Members saying "3.2 is most definitely NOT solved" in 2026 mean this blob
and the taunt paragraph around it — and they are right about it.

## A trap in the SalPhaseIon blob

The SalPhaseIon page uses `z` as a segment separator — it is what divides
`lastwordsbeforearchichoice` from `thispassword`. The AES blob there is also
split, by a 40-character run of `a`/`b` that decodes to `enter` and has to be
removed. But the blob's first half legitimately **ends in `z`**:
`…GWVHefvdrd9z` + `QvX0t8v3jPB4…`.

Strip that `z` as though it were another separator and you get 127 base64
characters → 95 bytes → 79 bytes of ciphertext → **4.94 AES blocks**. Not a whole
number. It cannot decrypt under any password, ever. It looks like tidying and it
is fatal.

Most of the chat carries the correct 128-character form (14 occurrences against
3), so this is not the seven-year explanation. But the truncated version does
circulate — including in the September 2026 message that laid both blobs out
side by side as "1st half / 2nd half", which is the framing the current work is
built on. Nobody in 61,349 messages ever checked either blob's block alignment.
Anyone brute-forcing SalPhaseIon should confirm they are on a 128-character
string before spending another CPU-year on it.

## The creator's own answer, and why Salphaseion isn't it

His self-declared final hint (January 2020, #1710):

> Roses are White but often Red. **Yellow has a number and so does Blue. Go back
> to the first puzzle piece without further ado.** It might have shown you only
> one door, beware that **the rabbits nest may contain a whole lot more.**

The group treated Salphaseion as the door this refers to. The timeline says
otherwise:

| date | event |
|---|---|
| 2020-08-02 | "Really nobody managed to find the extra door" (#4590) |
| 2021-03-14 | first team reaches Salphaseion (#6491) |
| 2021-03-22 | "Nr 5 in salph" — five teams inside (#6712) |
| **2021-12-02** | **"There is / Another / D O O R"** (#7914) |
| **2021-12-26** | "The previous 'there is another door hint' is still a thing. **We're not sure if anyone has found another door so far.** ... prime numbers ... some characters need to be 'zeroed out'" (#8000) |

Nine months after five teams were already inside Salphaseion, the creator says
another door exists and nobody has found it. Salphaseion is not the door the
Roses hint points at, or at least not the last one.

## What is actually still unspent in the first puzzle piece

This section was first written against a transcription of the image posted on
Reddit. It has since been redone against **the real PNG** — `analysis/puzzle.png`,
1048x1556, from the community mirror `github.com/puzzlehunt/gsmgio-5btc-puzzle`,
since gsmg.io itself went down in 2026. Run `analysis/first_piece.py`.

Three things the transcription got wrong, and they matter:

- It has **three cell errors** (row 6 col 12, row 6 col 13, row 7 col 4). Against
  the real file the spiral decodes cleanly, no corrupted characters.
- It contains **no red at all**. The real image does: `#ed1c24`, 15,705 px — a
  15px divider bar under the matrix. Anyone reasoning about "Roses are White but
  often Red" from a transcription was reasoning about an image with no red in it.
- It renders the off-colour cell as `#fffeff`. The real value is **`#fefefe`**.

What the real file establishes:

- **The spiral decode confirms exactly.** Counterclockwise, inward from the
  top-left, black/blue = 1, white/yellow = 0 → `gsmg.io/theseedisplanted`.
- **Blue and yellow are redundant.** All 24 coloured cells sit on *bit 7* — the
  low bit of a character, exactly one per character — and blue appears precisely
  where that character's ASCII code is odd. It is a character-boundary marker.
  Any theory treating blue/yellow as an independent payload is dead. Which also
  means "Yellow has a number and so does Blue" is not pointing at the bit values,
  known since 2019. The only numbers it leaves are the counts: **9 and 15**.
- **Four cells are surplus, and the rabbit is drawn on them.** 196 cells, 192
  consumed by the URL. The leftover four are the innermost 2x2 (rows 6-7,
  cols 6-7) — and the rabbit's head and ears occupy exactly those four cells.
  That is the rabbit's nest, literally. In 2023 one member noticed the 192/196
  gap and dismissed it as padding in one line (`2023.txt:19253`).
- **The off-colour cell is real** — `#fefefe` against `#ffffff` everywhere else,
  one whole cell (5,625 px) at row 7 col 4, 1-indexed (8,5). This confirms the
  group's own 2023 sighting. It sits at **spiral index 163, which is prime** —
  and primes are one of the two hints the creator issued after Salphaseion.
- **The native design grid is 70x70** at 15px units, five sub-units per cell.
  At that resolution, exactly 62 sub-units depart from their cell's flat colour,
  and **every one of them is part of the rabbit**. Nothing else in the image is
  hidden below cell level.
- **No steganography in this copy.** Alpha is uniformly 255; no bytes after
  IEND; no text chunks; the red-channel LSB split is 120,654 / 60,996, nothing
  like the ~50/50 a payload would give. The footer QR decodes to
  `https://www.blockchain.com/btc/address/1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`
  and carries nothing else.

Caveat worth keeping: this is a mirrored file and may have been re-encoded on its
way to GitHub. The stego negative is a statement about *this copy*, not provably
about the bytes gsmg.io originally served. In 2020 the creator said of the image,
"There must at least be something hidden in there" (#2918). If that was literal
rather than about the spiral, the original bytes are worth chasing — a 2019-2020
Wayback capture of `gsmg.io/puzzle` would settle it.

So the honest state of the first puzzle piece: the image is fully determined by
its URL, its colour channel is redundant, and it hides nothing below the cell
grid. What is left over is small and specific — **four unused cells with a rabbit
drawn on them, and one cell deliberately shaded off-white at a prime index.**

## So: restart at the first puzzle piece, on the main line

Two moves, in this order.

**1. Work the two things the real PNG leaves over.** Not the whole image — that
is now measured and accounted for. Just the four surplus centre cells the rabbit
is drawn on, and the `#fefefe` cell at spiral index 163, a prime. "The rabbits
nest may contain a whole lot more" is the creator naming the centre of the
spiral, and the rabbit is sitting on the only cells the URL does not use. The
group's own conclusion — that the matrix is fully determined by the URL — was
reached and then used as a reason to stop, when it is the reason to look: in a
fully determined image, anything left over is deliberate. Separately, chase a
2019-2020 Wayback capture of the original file, since the mirrored copy cannot
settle what the original bytes contained.

**2. Attack Phase 3.2's blob, not Salphaseion's.** It is the first unproven
joint, its plaintext is what the endgame expects you to be carrying, and unlike
Salphaseion it sits on ground that is cryptographically verified. Bring the two
unspent creator hints from December 2021 with you: **primes are required**, and
**some characters need to be zeroed out** — an instruction issued after
Salphaseion was already reachable, and therefore about the main line.

Everything else — btcseed, the 96-state object, cosmic duality — should be parked
until one of those two produces something that validates itself.


---

# Addendum 2: a documented null result

`analysis/sweep.py`. The point of this one is that it is written down.

**Harness, and two bugs it caught.** Before trusting any sweep, it self-tests
against the Phase 3.2 envelope, whose password is known. That test failed twice:

1. The KDF digest. OpenSSL changed the default `-md` for `enc` from MD5 to
   SHA-256 in 1.1.0. A sweep built on the MD5 assumption tests nothing.
2. The content filter. The real Phase 3.2 plaintext is only **60% printable
   ASCII**, because of the EBCDIC blob inside it. A 90%-printable filter — the
   obvious thing to write — silently discards a correct decrypt.

Either bug alone produces a confident, meaningless "no results". Both are the
kind of thing that never surfaces without a known-answer test.

**What was swept.** Every answer the chain has produced — causality, Safenet,
Luna, HSM, 11110, jacquefresco, giveit/givetit, justonesecond, Heisenberg,
thematrixhasyou, theseedisplanted, matrixsumlist, enter, thispassword,
lastwordsbeforearchichoice, hashthetext, yinyang, shabef, the address, the
X2SH values, 163 — alone, in the documented combinations, and in every ordered
pair and triple, each as raw text and as SHA-256 hex in both cases, against both
blobs under both KDF digests. 196,947 passphrases, 787,788 trials.

**Result.**

| | |
|---|---|
| passed PKCS#7 padding | 3,105 |
| expected from chance alone | ~3,077 |
| plaintext-looking (≥95% printable) | **0** |

The padding pass rate is indistinguishable from noise, which is the whole lesson
restated in one line: **3,105 "hits" that mean nothing.** Anyone brute-forcing
these blobs and stopping at "the padding validated" will find one every 256
tries, forever.

**What it rules out.** Whatever opens these two blobs is not a recombination of
what the group already has. That closes off the space most of the brute-forcing
of the last five years has been searching, and it points the remaining effort at
the three things that could supply a genuinely new answer: the two unspent
December 2021 hints (primes are required; some characters need to be zeroed
out), and the orphaned X2SH block.


---

# Addendum 3: X2SH worked, and two hypotheses killed

Both tests below are validated against a known answer before being trusted, and
both are negatives. Written down so nobody spends another year on them.

## The VIC board reproduces exactly

Built from `FUBCDORA.LETHINGKYMVPS.JQZXW` with 1 and 4 straddling:

```
single : 0=F 2=U 3=B 5=C 6=D 7=O 8=R 9=A
row 1  : 10=. 11=L 12=E 13=T 14=H 15=I 16=N 17=G 18=K 19=Y
row 4  : 40=M 41=V 42=P 43=S 44=. 45=J 46=Q 47=Z 48=X 49=W
```

Fed the 3.2.2 digit string it returns `INCASEYOUMANAGETOCRACKTHIS…` exactly. The
board is correct, so anything it fails to decode, it fails for real.

## Hypothesis 1 — X2SH is the ten-wide board the VIC hint points at. DEAD.

Substituting S=32, Q=82, and sweeping H ∈ {42, −42}, B ∈ {−16, 16, 25}, X and Y
over −99…99, forwards and reversed ("worst gear"), feeding the resulting digit
string through the validated board: **475,212 combinations**. 2,004 produced a
decode containing any dictionary word at all — 0.4%, indistinguishable from
noise — and the best of them are `INRUFOR.UBUUAA` and similar. There is no
assignment of X and Y that makes the block VIC-decode into anything.

## Hypothesis 2 — X and Y resolve to a blob passphrase. DEAD.

The substituted block written every way this puzzle has ever written a
concatenated answer (plain, absolute values, spaced, hyphens stripped, `#`-wrapped,
reversed), each as raw text and as SHA-256 hex in both cases, against both blobs
under both KDF digests, for every X and Y in −99…99 and every sign variant:

| | |
|---|---|
| distinct passphrases | 5,702,544 |
| trials | 22,810,176 |
| passed PKCS#7 padding | 89,325 |
| expected from chance alone | ~89,102 |
| plaintext-looking | **0** |

89,325 against 89,102 expected. Pure noise, again. X and Y do not resolve to
anything either blob accepts in this family of formats.

## One observation, correctly discounted

The six letters in the block — X S H Y Q B — sit exactly two per QWERTY row
(Q and Y top, S and H home, X and B bottom), which looks meaningful next to a
riddle that explicitly builds the keyboard. It is not. Six letters drawn at
random land two-per-row **14.8% of the time**: a 1-in-6.8 coincidence. Recording
it as a non-finding, because this is exactly the shape of thing that becomes
next year's btcseed if someone writes it down excitedly instead of measuring it.

## Where that leaves X2SH

Still an orphan, and now with two of its three plausible jobs eliminated. It is
not a VIC board and it is not a passphrase. What remains: it is data to be
carried forward and consumed by a step nobody has reached, which is what
"the code you hopefully carry" would imply — or X and Y are not numbers at all.


---

# Addendum 4: primary evidence only — the three ciphertexts

Restricted to the puzzle's own artifacts, the creator's own words, and
measurements. No community interpretation except where a reading is confirmed by
its own downstream consequences, which is noted as such.

## Measurements

| block | salt | ciphertext | blocks | max plaintext |
|---|---|---|---|---|
| Phase 3.2, inner | `b45a5e3d827593ca` | 80 B | 5 | 79 B |
| SalPhaseIon | `3ab585348552415d` | 80 B | 5 | 79 B |
| **Cosmic Duality** | `2d3f6fe06dc950e6` | **1,328 B** | **83** | 1,327 B |

All three are OpenSSL `Salted__` AES-256-CBC. Distinct salts, so three distinct
ciphertexts. The Cosmic Duality salt is identical across every independent copy
posted to the chat in 2021, 2024, 2025 and 2026.

The size asymmetry is the most useful fact here and it is rarely stated: the two
small blocks can hold a key or one short instruction and nothing more. Cosmic
Duality holds roughly 1.3 KB — a document.

## Cosmic Duality

- It is a **separate section on the same page** as SalPhaseIon, under its own
  heading, with its own blob. Confirmed against the page capture in the mirror.
  It is not the small SalPhaseIon block, and conflating the two is common.
- **The creator has never written "cosmic" or "duality" in any of his 521
  messages across seven years.** The name exists only on the page.
- The only creator statement adjacent to it: in December 2022 barrystyle posted
  an image (377×499) after "googl[ing] a phrase which would be assumed to be
  part of a hint", and the creator replied *"…That is very specific"* and *"If
  the puzzle is solved you'll see how scary specific that is."* This is the only
  time in the whole export the creator endorsed a community find. **The image
  binary is not in the export**, so what it showed cannot be verified from these
  sources — only that the creator called it specific.

## The SalPhaseIon block

- Sits inside the letter stream, split by a 40-character `a`/`b` run decoding to
  `enter`.
- Its first half ends in `z`, which is also the stream's segment separator —
  hence the truncated 127-character version in circulation. The correct form is
  128 characters and 5 whole blocks.
- Immediately before it in the stream: `shabef` and
  `ourfirsthintisyourlastcommand`. Immediately after it: `shabefanstoo`.
- Under the page's own scheme `shabef` reads as `sha` + b=2, e=5, f=6 → **sha256**,
  and `shabefanstoo` as **sha256 ans too**. This reading is how the a=1…i=9,
  o=0 mapping was derived in the first place, and it is confirmed by that
  mapping then correctly decoding `lastwordsbeforearchichoice` and
  `thispassword`. So the page states its own password format.
- Unconsumed adjacent text: **"our first hint is your last command."**

## The Phase 3.2 block

- The last item in the Phase 3.2 plaintext, which decrypts cleanly and is
  therefore certain.
- The line immediately before it: *"Raising the stakes without extra chances of
  winning. A fubcd-king & oracle-queen, thingky mvps, on a sad board but as wide
  as the first one seen."* The second sentence is the VIC alphabet, already
  consumed by 3.2.2. **The first sentence has never been consumed by anything.**

## What the creator said that bears on all three

- 2021, on SalPhaseIon: *"Breaking salphation, should be giving the feeling of
  the phase's name."*
- 2023: *"Once you hit a 'ying yang', you'll be able to solve it the same day."*
- 2025, asked directly whether yinyang is found after decoding an AES
  ciphertext: *"It's the next phase, but I await the day someone finally gets
  there."* — so an AES decrypt is what leads to yinyang.
- 2025: *"when yingyang is reached, 2 hours max."*
- The 2023 binary hint, decode verified: *"…yinyang we wont give away the
  password its in front of your eyes but youre not seeing it very last step is a
  true giveaway promised."*

## What we do not have

No creator statement naming any of the three blocks. No statement of which one
leads to yinyang. No confirmation that Cosmic Duality is reachable at all from
the current state, and nothing that dates it relative to SalPhaseIon. The
barrystyle image, the one artifact the creator ever endorsed, is absent from the
export.


---

# Addendum 5: which block to attack next

## A correction to a circulating claim

A 2025 message states the Cosmic Duality section is "14 base64 encoded AES
encrypted blobs, each 64 bytes long". It is not. The section is 1,792 base64
characters — 28 lines of 64 — and decodes as **one contiguous OpenSSL blob**:
the magic `Salted__` appears exactly once, and (length − 16) is an exact
multiple of 16. Split into 14 chunks, only the first carries the magic. Anyone
attacking it as fourteen independent 48-byte blobs is attacking a target shape
that does not exist.

## Effort already spent, measured

Times each ciphertext was actually posted to the chat, 2023-2026:

| block | ciphertext posted | named in chat |
|---|---|---|
| Phase 3.2 inner | 83 | 846 |
| SalPhaseIon | 79 | 1,740 |
| **Cosmic Duality** | **9** | 877 |

Cosmic Duality is an order of magnitude less worked than the other two while
being talked about just as much. That looks like an opportunity and is not one —
see below.

## Recommendation: the Phase 3.2 inner blob

**1. It is the only one standing on proven ground.** Its container decrypts
cleanly and verifiably. SalPhaseIon was reached through the side door, and
Cosmic Duality sits on that same side-door page.

**2. It has a closed candidate space — the only one that does.** Every password
in this puzzle has come from riddles in the immediately preceding plaintext.
Inside Phase 3.2's plaintext every sentence is now accounted for except one:

> "Raising the stakes without extra chances of winning."

One unspent sentence, immediately above the ciphertext, in a text that is
otherwise fully consumed. That is the narrowest well-defined target in the
puzzle.

**3. Dependency order argues against Cosmic Duality first.** It carries 1,327
bytes — a document, not a key — and has **no adjacent hint text whatsoever**,
just a heading. A payload that large at the end of a chain with no clue attached
is almost certainly opened by material manufactured upstream. Its low prior
effort reflects that absence of a foothold, not an oversight.

Second choice is SalPhaseIon, which at least states its own password format on
the page (`shabef` → sha256, `shabefanstoo` → sha256 ans too) and has one
unconsumed line, "our first hint is your last command". But it is side-branch
and as heavily trodden as 3.2.

Expected switch point: if either 80-byte block opens, Cosmic Duality probably
becomes derivable, and its 1,327 bytes are where the substance is.


---

# Addendum 6: the unconsumed sentence, worked — and my own premise weakened

`analysis/raise_sweep.py`.

## What was tested

Readings of *"Raising the stakes without extra chances of winning."* — poker
(bluff, ante, all-in, overbet, pot-committed, dead money), probability
(martingale, doubling cube, Kelly, St Petersburg, gambler's fallacy, sunk cost,
zero-sum, house edge), chess (promotion, underpromotion, zugzwang, gambit,
stalemate, pyrrhic victory), and the literal phrasings. Each alone, each paired
with every established chain answer both ways, each with the Phase 3.2
passphrase, and all ordered pairs of readings. **21,717 passphrases, 86,868
trials.** 369 passed PKCS#7 padding against ~339 expected from chance. **Zero
plaintext.**

Then the puzzle's own stated convention, `shabefanstoo` = "sha256 ans too":
SHA-256 of the 3.2.2 answer, of the 3.2.1 answer, of both concatenated, plus
double-hashes. 80 trials, **zero padding passes**.

Then "our first hint is your last command" read literally: the creator's first
posted hash from April 2019, the "giveit = givetit" fix, the Roses poem, the
phase-1 password. 92 trials, **zero padding passes**. (That first hash turns out
to be nothing new — it is exactly
`SHA256("theflowerblossomsthroughwhatseemstobeaconcretesurface")`, the phase-1
answer, posted because the site was throwing token errors.)

## The premise itself is weaker than I stated

I argued this blob was the best target because it has "one unspent sentence" and
therefore a closed candidate space. That reasoning does not survive contact:

**1. The sentence probably belongs to the VIC clue.** In a straddling
checkerboard, twenty of the twenty-eight letters cost two digits instead of one
and yield nothing extra for it. "Raising the stakes without extra chances of
winning" describes that mechanism, and it sits in the same breath as the
alphabet spec it would be describing.

**2. This author demonstrably writes flavour that is never a clue.** Phase 2
ends with *"Ok kid, on the highway, let put it in the worst gear."* The group has
chased it since 2020 as an instruction to reverse or go back. In seven years it
has produced nothing. There is direct precedent in this puzzle for a sentence
that reads like a clue and is not one.

So "every sentence is a clue" is an assumption, not a property of this puzzle,
and I imported it. **Reason 2 for choosing the Phase 3.2 inner blob is
withdrawn.** Reason 1 — that it is the only block standing on cryptographically
proven ground — still holds, and it is now the only reason.

## What that changes

If none of the three blocks has an adjacent clue, then all three take a password
manufactured elsewhere, and the ranking between them matters much less than
finding that source. The creator's own framing points the same way: *"we wont
give away the password its in front of your eyes but youre not seeing it"* — not
"it is written next to the ciphertext".


---

# Addendum 7: step back — what this audit got wrong, and what is left

## Where I went wrong

Five errors in this audit, all the same error:

1. **Imported "every sentence is a clue."** Used it to argue the Phase 3.2 blob
   had a closed candidate space. Withdrawn — this author writes flavour that is
   never a clue, and "Ok kid, on the highway, let put it in the worst gear" has
   proved it for seven years.
2. **Claimed a five-year blind spot that was not one.** The insert-vs-replace
   reading of "zeroed out" was raised in November 2024. Corrected.
3. **Nearly ran the dbbi/faed side branch** immediately after spending the whole
   audit arguing that working the side branch is what lost the group five years.
4. **Shipped a sweep with two bugs** — wrong KDF digest, over-strict content
   filter — each of which alone produces a confident, meaningless negative. Only
   a known-answer self-test caught them.
5. **Quoted creator hint text as authoritative** in the same document that
   proves the creator retroactively edited 35% of those messages.

The pattern: I held the community's work to a standard I did not hold my own to.
That is the identical failure mode that produced btcseed. Anyone using this
document should assume it contains more of the same, and re-run the scripts.

## New findings from the step-back

- **"dbbib most definitely is [decryptable]" is a community assertion, never a
  creator statement.** Asked directly "can you confirm if dbbib is decryptable?",
  the creator answered *"No hints 🤡"* (`2023.txt:3547-3555`). The confirmation
  everyone cites came from another member in the next message.
- **The author used the legacy EVP-BytesToKey(SHA-256) KDF, not PBKDF2.**
  Verified against the blob whose password is known: legacy decrypts, PBKDF2 at
  1k/10k/100k iterations does not. Every passphrase sweep here is on the right
  KDF.
- **The SalPhaseIon letter stream length-reconciles; it is not fully decoded.**
  Its 1,075 characters match dbbi (91) + the matrixsumlist run (104) + faed (570)
  + lastwords (63) + thispassword (29) + 3 `z` separators + the shabef line (35)
  + the AES blob (128) + the enter run (40) + shabefanstoo (12). **No leftover
  characters.** `dbbi` and `faed` (661 symbols, no `o`) are still unread. Length
  accounting is not a decode. Do not declare SalPhaseIon a closed null.
- **Raw-key mode is under-explored.** Everyone, this audit included, has assumed
  the blobs open with a passphrase through a KDF. The creator wrote that the
  solver *"will find a way to 'decrypt' it"* — his quotation marks. A first
  sweep of raw `-K`/`-iv` decryption using keys taken directly from puzzle
  material (the stage password hashes, SHA-256 of chain answers, and XOR chains
  of those) across all three blobs: 516 trials, **0 padding passes**. Not a
  solution, but the mode is cheap and barely touched.

## The one asymmetry left standing

Everything this puzzle manufactures gets consumed, and we can now say that with
measurements rather than impressions:

| artifact | status |
|---|---|
| rabbit matrix | fully determined by its URL — **except 4 surplus cells and one `#fefefe` cell at prime index 163** |
| the 8 /theseedisplanted images | consumed by the phase-1 password |
| phase 2 plaintext | seven clue-parts consumed — **except the X2SH block** |
| phase 3 plaintext | three riddles, all consumed |
| phase 3.2 plaintext | every section consumed |
| SalPhaseIon stream | length-reconciles; **dbbi (91) and faed (570) unread** |
| Cosmic Duality | one 83-block blob, no adjacent text at all |

**Three pieces of manufactured material in this entire puzzle were never
consumed by anything, and all three are in phases 1 and 2** — the two stages
nobody has worked since 2020. The endgame text says the solver arrives carrying
something. These are the only candidates for what that is.


---

# Addendum 8: the three unconsumed pieces, worked

`analysis/carry_sweep.py`.

## First, the primary text

Phase 2's plaintext was decrypted here rather than taken from the transcription:
648 bytes, CRLF line endings, ending exactly at `worst gear.` with no trailing
bytes. The canonical transcription is faithful — no dropped characters, and no
`~$` shell prompt (a member's own terminal, quoted into the chat in 2020 and
mistaken for puzzle text ever since).

One structural detail the transcription does preserve and nobody remarks on: the
block lists its tokens `X 2 S H 4 Y 0 Q B 15`, with the letter pairs (S,H) and
(Q,B) adjacent — but defines them in the order **Q, B, H, S**. The second pair
in order, then the first pair reversed.

## The sweep

X2SH with X and Y drawn from every number the image actually yields — 163 (the
off-colour cell's prime spiral index), 192-195 (the surplus cells), the cell
coordinates, the colour counts 9 and 15, the 86/86 black/white census, 121, 70 —
in both sign variants, forwards and reversed; those numbers alone and in ordered
pairs and triples; and each concatenated with the chain's own answers both ways.
Against all three blobs, both KDF digests.

| | |
|---|---|
| distinct passphrases | 19,326 |
| trials | 115,956 |
| passed PKCS#7 padding | 489 |
| expected from chance | ~453 |
| plaintext-looking | **0** |

## What the cumulative negative is worth

Across every sweep in this document: **~5.94 million distinct passphrases**, all
returning padding-pass rates statistically indistinguishable from chance and zero
plaintext. What has now been ruled out:

- every answer the chain has produced, alone, in the documented combinations, and
  in all ordered pairs and triples
- the entire X2SH space over X, Y ∈ [−99, 99] and over the image-derived numbers
- every reading of the one unconsumed Phase 3.2 sentence
- the puzzle's own stated convention, "sha256 ans too", over both 3.2 answers
- the creator's first posted hash, the Roses poem, "giveit = givetit"
- raw-key mode with keys taken directly from puzzle material

**The password is not a recombination of known material, hashed.** Seven years of
community effort and everything in this document have been searching that space.
It is now closed to a useful depth, and closing it is the most solid thing here.

What remains must be one of: a new answer nobody has derived; a construction that
is not `SHA256(concatenation)`; or a decryption that is not a passphrase at all —
which is the reading the creator's own scare quotes around *"the solver will find
a way to 'decrypt' it"* would support.


---

# Addendum 9: "how do you know it's plaintext?" — I didn't

The criterion used everywhere above was *is the decrypt printable ASCII*. That is
wrong, and it is the third instance of the same bug in this document.

## What the plaintext could actually be

Both small blobs are 5 blocks, so their plaintext is 64-79 bytes.

| candidate content | printable? | old filter |
|---|---|---|
| WIF key (51-52 base58 chars) | yes | caught |
| hex key (64 chars) | yes | caught |
| short instruction / URL / base64 | yes | caught |
| gzip / zlib / bzip2 | **no** | **missed** |
| EBCDIC text — and this puzzle already uses cp1141 | **no** | **missed** |
| **two raw 32-byte private keys = 64 bytes** | **no** | **missed** |

That last row matters: 64 bytes is exactly two 32-byte scalars, it pads to
exactly 5 blocks, and the puzzle says *"the private keyS belong to half and
better half"* — plural. It is the single best structural fit for a blob this
size, it is ~0% printable, and my filter would have discarded it in silence.

## The sharp filter I threw away

PKCS#7 pad value *k* requires the last *k* bytes to equal *k*, so on random data
**P(pad = k) = 256⁻ᵏ**. pad=1 is pure noise. pad=2 is 1 in 65,536. **pad=16 —
which is precisely what a 64-byte plaintext produces — is 2⁻¹²⁸.** Observing one
at all is near-proof of a correct key.

I counted "padding passes" in aggregate for eight addenda and never once looked
at the distribution of the pad value. That was the real signal, sitting in data
I had already computed.

## The re-run

`analysis/inspect_pt.py` + `analysis/recheck.py`. Every candidate space re-tested
against all three blobs, judged structurally: printable ASCII, EBCDIC cp1141,
compression magic bytes, all-base58, and — for any 32- or 64-byte plaintext —
secp256k1 derivation of both halves compared against the prize address.

**1,181,682 trials.**

| pad | observed | expected on noise |
|---|---|---|
| 1 | 4,593 | ~4,620 |
| 2 | 16 | ~18 |
| ≥3 | **0** | ~0 |

Both observed values sit within a couple of percent of the noise prediction, at
two independent points. Nothing above pad=2. No structural hit of any kind on any
candidate.

**This is a much stronger negative than the eight addenda above it.** Those ruled
out "produces ASCII". This rules out "produces anything at all" — no key pair, no
compressed payload, no EBCDIC, no base58, in the entire searched space. The
earlier claims should be read as the weaker statement they actually were.


---

# Addendum 10: the original page sources, found

The Wayback Machine is unreachable from this container, but archived copies of
the original gsmg.io pages and the eight source images exist in
`github.com/AppleLamps/puzle` (`fresh-start/archives/`, `fresh-start/images/rebus/`).
Everything below is measured from those, not from a transcription.

## Every measurement in this document is confirmed

From `salphaseion_phase3.html` — the page as served, two `<textarea>` elements:

| | measured from source |
|---|---|
| SalPhaseIon stream | **1,075 chars** — matches the reconciliation in Addendum 7 exactly |
| SalPhaseIon AES blob | **128 base64 chars, salt `3ab585348552415d`, 80 B, 5.00 blocks** |
| Cosmic Duality | **1,792 chars → 1,344 bytes, salt `2d3f6fe06dc950e6`, 83.00 blocks, magic appears once** |

**The `z` question is settled.** In the source the blob reads
`…GWVHefvdrd9z` + the `enter` run + `QvX0t8v3…`. Keeping the `z` gives 128
characters and exactly 5 blocks; dropping it as a separator gives 127 and 4.94
blocks, which cannot decrypt. The `z` is ciphertext. The truncated form in
circulation is wrong, from the horse's mouth.

One detail the source adds: the `enter` run sits at **offset 64** inside the
128-character blob. The blob is split exactly in half — 64 characters, `enter`,
64 characters. Given the plaintext of this stage says *"the private keys belong
to half and better half"*, that is at least a nice piece of authorship.

## The eight rebus images

The directory is called **`rebus`** — the author's own word for what the page is.

| file | image | block | pad L | pad R |
|---|---|---|---|---|
| black_banking - war | 78×70 | 70 | 0 | 8 |
| blue_ca | 78×70 | 70 | 0 | 8 |
| blue_dig_i | 77×70 | 70 | 0 | 7 |
| blue_lock_lo | 82×70 | 66 | 0 | 16 |
| red_crypto_gic | 79×70 | 67 | 12 | 0 |
| red_n_you | 80×70 | 67 | 13 | 0 |
| red_open_lock_n_ing | 82×70 | 66 | 16 | 0 |
| red_t | 79×70 | 67 | 12 | 0 |

**The 2019 observation is real and now explained.** A Redditor noted in October
2019 that the images "have different widths … they're all off by a few pixels",
and it has sat unresolved ever since. The widths do vary, 77 to 82 — but the
variation is layout, not code: **black and blue pad on the right, red pads on
the left, without exception.** Each blue/black tile carries its trailing margin
and each red tile its leading margin, so that a blue+red pair renders as one
word — `ca|n you`, `dig i|t`, `lo|gic`, `war|n ing`. The block widths (70, 70,
70, 66, 67, 67, 66, 67) track glyph content; the two 66s are the two padlock
tiles, which are the designated "opposites attract" pair.

Every height is **exactly 70** — the same 70 as the rabbit matrix's native
70×70 design grid.

No steganography: alpha uniformly 255 on all six RGBA files, no `tEXt`/`iTXt`/
`zTXt` chunks, nothing after IEND in any of the eight.

## What this closes

`/theseedisplanted` now joins the rabbit matrix and the SalPhaseIon stream as
**fully accounted for**. Three of the puzzle's four visual artifacts are
measured and explained. The only surplus material anywhere remains what
Addendum 7 identified: the X2SH block, the four cells under the rabbit, and the
`#fefefe` cell at prime index 163.


---

# Addendum 11: the "solved Cosmic Duality" claim is a pad=1 false positive

The archive repo contains `artifacts/bin/cosmic_plaintext.bin`. Its SHA-256 is

```
4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081
```

which is **exactly the hash the bitcointalk claimant published** for their
`cosmic_decrypted_1327_2.bin` — the file underneath GitHub issue #79's "Half &
Better Half Derived" and issue #80's request that the creator hand over the
prize. So this is their artifact, and it can be tested directly.

| measurement | value | uniform random |
|---|---|---|
| length | **1,327 bytes** — Cosmic ciphertext is 1,328, so **PKCS#7 pad = 1** | |
| Shannon entropy | 7.8702 bits/byte | 8.000 |
| distinct byte values | 255 of 256 | 256 |
| index of coincidence | 0.00382 | 0.00391 |
| zlib compresses to | 1,338 bytes — **larger than the input** | incompressible |
| chi-square (255 dof) | 225.8 | ~255 |

Every statistic says uniform random. **It is not a decryption.** It is a pad=1
hit — the single most likely PKCS#7 false positive, probability 1 in 256 — and
the entire published pipeline (1,327 bytes → 10,616 bits → a 103×103 matrix →
row and column sums → base-38 → "Half" and "Better Half") was run over 1,327
bytes of noise.

Which explains the two loose ends in that claim exactly:

- the derived keys produce `1JG648yaB7Wp2dpUfcZoRSD4q35oq47vCu` and
  `145ZQ9siLrsXBKf465wjdyQYAP5dRwhRhQ`, neither of which is the prize address —
  because any 32 bytes look like a private key
- the claimant had to *ask the creator to send them the balance*, because they
  never held a key to it

This is the same error this document opened with, at the other end of the chain.
btcseed was a coincidence mistaken for a message; this is a padding collision
mistaken for a decryption. **The failure mode is the puzzle's real adversary.**

## Also checked, from the original page sources

- `TheArchitectChoice.html` is the GSMG corporate app shell — no puzzle content,
  no ciphertext, no textareas. `phase1verification.html` as archived is a 2023
  "Page Not Found". Both dead ends, recorded so nobody re-walks them.
- Phase 2 ciphertext: 656 bytes, 41 blocks, salt `06286612d43ed7ed`.
  Phase 3 ciphertext: **4,096 bytes exactly, 256 blocks**, salt `9fbc451d13d071f4`.
  Phase 3 decrypted here from source with the known password — the chain is now
  verified end to end from the pages as served, not from transcriptions.
- The page states a format spec after each riddle that the README compresses
  away: `/(aaa, connected enf)`, `/(aBa, connected enf)`,
  `/(aBa, connected not enf)` — casing and whitespace rules, per part.


---

# Addendum 12: converging with prior work, and one correction to it

`github.com/AppleLamps/puzle` holds a large, provenance-disciplined corpus that
is further along than this audit assumed. Two results from checking it.

## Verified independently: the 479 balance

Take the 24 poster colour markers in spiral order and map them onto the first 24
primes:

```
B2 B3 B5 B7 Y11 B13 B17 B19 Y23 Y29 B31 B37 B41 B43 Y47 B53 B59 Y61 Y67 B71 Y73 Y79 B83 Y89
```

| | sum |
|---|---|
| Blue (15 markers) | **484** |
| Yellow (9 markers) | **479** |
| imbalance | **5** — itself a prime, carrying a Blue marker |

Zero out that 5 and both sides read **479 = 479**. Reproduced here from my own
grid extraction, not from their notes.

This is the best construction anyone has, and the reason is that it consumes
three creator hints simultaneously and exactly:

- *"Yellow has a number and so does Blue"* — the two sums
- *"prime numbers … definitely an aspect which is required to proceed"*
- *"some characters need to be 'zeroed out'"*

and it produces a **balanced pair**, which is what a yin-yang is. Architect
plaintext `[479:]` then reads `PRIVATEKEYYOUVEEARNEDITBUTPLEASE…`.

Note what this does to Addendum 6, where I withdrew the "zeroed out" hint as
trodden ground on the basis that it pointed at dbbi/faed. It does not point
there. It points here, and here it lands exactly.

## Correction to that corpus: F73D92 is not independent data

The same corpus lists `F73D92` — the 24 markers read as blue=1, yellow=0 —
among the authenticated artifacts. I reproduce the value exactly. But per
Addendum 6 of this document, the marker colours are **fully determined by the
URL**: blue appears precisely where the character's ASCII code is odd. So

```
low bit of each char of "gsmg.io/theseedisplanted"
  = 111101110011110110010010
  = F73D92
```

**F73D92 is computable from the URL string with no image at all.** It is the
parity bitmap of text everybody already has, and carries no entropy of its own.
Anyone using it as key material is using 24 bits they already had. The 479
balance is different — it uses the marker *positions* against the primes, which
is real structure.

## Where the frontier actually is

Two independent efforts have now closed two large search spaces: ~5.9 million
passphrases here, ~1.59 million gated scalars and millions of AES trials there,
against an exact on-chain oracle. Neither hit.

That agreement is itself the finding. **The gap is a missing idea, not a missing
computation**, and the creator said as much in the only hint he ever labelled as
one: his close friends, who lack the cryptanalytic skill, are better placed than
the people who have it. That describes personal context, not more search.


---

# Addendum 13: where this audit stands relative to prior work

After reading the corpus properly, the honest position:

**Most of this document is an independent re-derivation of work that already
exists and is further along.** `AppleLamps/puzle` had already established the
poster spiral and residual `0000`, the 24 markers, the 479 balance, the rebus,
the full authenticated chain, the authentication boundary after phase 3.2, and —
critically — the same methodological rule this document arrives at in Addendum 9,
stated there as: *"Clean padding, readable fragments, vanity prefixes, community
labels, and solver-published-address activity are not evidence."*

Two of my "findings" were already theirs and I withdraw the framing:

- **F73D92 redundancy.** I presented this as a correction to them. Their own
  table already reads "24 markers on every 8th spiral bit; **marker colour
  restates that bit**". Same conclusion, recorded earlier. Not a correction.
- **The btcseed false positive.** Their treatment is stronger than mine: they
  carried it downstream to the BIP39 claim and showed 13 of 3,624
  mapping×offset windows are checksum-valid by chance against an expected 14.

The `cosmic_plaintext.bin` debunk in Addendum 11 also lands on a file they
already hold and already treat as a checkpoint rather than a solution.

## What in this document does appear to be new

- **The creator's retroactive edit rate** — 35.4% of his 2019-2022 messages
  carry an edit timestamp two or more years later, against a 3.7% baseline
  across all users, concentrated in 2025-26 and on the hint-bearing posts. No
  equivalent appears in their docs. This matters to them specifically, because
  their entire method rests on separating creator statements from solver
  interpretation — and it means the *text* of a creator statement is not
  automatically the text as posted.
- **The SalPhaseIon `z` truncation trap**, and the measured resolution of the
  October 2019 rebus-width question.

## What is actually next

Their statement of the frontier is correct and I have nothing to add to it: a
convention-free reading of the 479 instruction, or personal context about how
the creator thinks. Everything runnable without one of those is exhausted, and
this session's ~5.9M passphrases plus 1.18M structural trials are one more
confirmation of that, not a counterexample.

Of the two, only the second is something I can serve: the full 2019-2026 export
is here with tooling over it, and the creator's 521 messages are the record of
how he thinks. That is what his one self-declared hint points at, and it is the
one remaining task that is research rather than search.


---

# Addendum 14: why I am not running the recognition sweep

The obvious next action after the profile is to sweep its §4 "volunteered but
never used" list. I read the prior attempt log first, and I am not going to.

**v52 already ran it.** The corpus built the same hint into a preregistered
55-string recognition set — Fresco / Venus Project, GSMG as "Globally Supporting
My Generation", better half, Matrix callbacks, Neo's passport date, "ASCII 127",
the Hope quote, **Dutch and purple asides**, Bella Ciao, Witteveen — across 6
password forms × 2 KDFs × 6 envelope modes. 3,960 AES trials, 110 scalar gate
tests, 0 legible, 0 prize matches, 20 padding hits against ~14.7 expected. The
entry notes it was deliberately bounded: *"Not open-ended identity research."*

Related families are closed too: v61 (the July 2026 NOTES thread as phrases),
v62 (spiral edits at the off-white eye index 163), v63 (Architect windows
bounded by named anchors including `PRIVATEKEY` at 479, no free offsets).

**My delta is small and low-prior.** What §4 adds beyond v52 is roughly:
Cyberpunk 2077, South Park, Rust, Blueprint / NAD / Bryan Johnson, psychedelic
specifics, BIP 360, the DAO, the Turing test, bitconnect, the Guinness Book.
As password material that is the tail of plausibility, and the strong items on
the list were already in v52.

**And my infrastructure is weaker than theirs.** They preregister and seal each
family, gate scalars through one module against an on-chain oracle, search under
a legibility gate, and run an integrity audit that has already caught its own
CRLF-corrupted seals. I have none of that. Running an unsealed sweep and
reporting another null would add noise to a corpus whose entire value is
disciplined recording — and this document has already had to withdraw four
claims for exactly that kind of haste.

**What the profile is actually for.** Not as a wordlist. Two things in it are
usable regardless of any sweep:

1. **Wordplay is his primitive.** Every authenticated stage rewards hearing a
   pun; none requires original mathematics. Seven years of escalating structural
   search is a category error by his own design, and his one labelled hint says
   so.
2. **Irregularity is not signal.** He works in 800% frenzies, ships unchecked,
   and shipped `givetit` after verifying three times. Anomaly-hunting in his
   artifacts has a high false-positive floor for that reason alone.

**The remaining input is not in any archive.** He is alive, still posting — last
message 2026-09-01 — and he answers well-formed structural questions even while
refusing hints: asked directly whether `yinyang` follows an AES decrypt, he
answered *"It's the next phase, but I await the day someone finally gets there."*
Nobody has spent that channel carefully. It costs nothing, and it is the only
source of genuinely new information anyone has left.


---

# Addendum 15: offline-solvable — three connections tested, all null

**Correction accepted.** Addendum 14 ended by pointing at the creator as the
remaining source of information. That was wrong and I withdraw it. He stated
plainly, asked whether the internet is still required given available knowledge:
**"Nope"** [#16624], and separately *"No need. You have all the info"* [#9607].
Everything required is in the artifacts. A failure to solve is therefore a
failure to read what is already in hand — mine included.

## The artifact set is complete

Checked rather than assumed. Every page in the chain is archived and held:
poster → `/theseedisplanted` (rebus + hidden form) → `/choiceisanillusion…`
(phase 2 and phase 3 ciphertexts) → phase 3 plaintext (carries the 3.2 blob) →
3.2 plaintext (carries 3.2.1, 3.2.2 and the inner blob) → `/89727c…`
(SalPhaseIon + Cosmic Duality) → Decentraland audio. There is no separate phase
3.2 page to find; that ciphertext lives inside phase 3's plaintext. Nothing is
missing.

## Three connections tested this pass

**1. `matrixsumlist` read literally on the poster.** Row sums
`[6,10,8,7,6,6,5,4,9,9,7,8,7,9]`, column sums `[8,10,8,10,8,7,3,6,7,5,9,6,6,8]`,
101 ones / 95 zeros. Derived offsets (100, 101, 744, 767, 777) land mid-word in
the Architect plaintext. Step 1 of the roadmap landed exactly on `PRIVATEKEY`;
none of these land on anything. **Null.**

**2. `lastwordsbeforearchichoice` anchored on the text's own choice.** The
SalPhaseIon stream reads as a sentence that defines its own password —
`lastwordsbeforearchichoice` `z` `thispassword` `z` `shabef` — i.e. sha256 of
the last words before the Architect offers a choice. In the authenticated
plaintext the selection is offered at index 1114, and the words immediately
before it are **`REINSERTINGTHEPRIMEBASICS`**, a clean 25-character word
boundary. Tested every natural boundary ending at that anchor plus the film's
own "…the anomaly revealed as both beginning, and end", each as raw, sha256,
double-sha256, upper, against all three blobs under both KDFs: 624 trials, 2
padding passes against ~2.4 expected, **0 structural hits. Null.**

**3. X2SH as a list of offsets into the Architect plaintext.** The earliest
orphan against the authenticated text — direct indexing, signed and absolute
cumulative sums, and all of it re-based at 479. Outputs `UUELYZOM`, `UBTPPTSE`,
`ITHAPHAE`. **Null.**

## What that leaves

The material is all present, the passphrase space is closed here, and ~65
sealed structural families are closed in the prior corpus. So the missing thing
is a *reading* of something already in hand, and the items with the least
interpretation successfully applied to them remain exactly three: the X2SH
block, "our first hint is your last command", and "Raising the stakes without
extra chances of winning."

I do not currently have that reading. Recording the three negatives so the next
attempt does not spend itself here.


## Addendum 15a: correcting my own null — the 193 landing

Flagged by the user: I reported `sum abs 193 -> 'HARMONYOFMATHEMATICALPRECISION'`
as null alongside genuinely meaningless outputs. That was sloppy, and the two
halves of the correction point in opposite directions.

**Where the challenge is right.** 193 lands on a **word boundary**, which is the
acceptance test 479 passed and the test I had just claimed to be applying. The
other candidates do not: 161 → `ETOELIMINATEFROM…`, 101 → `ALITYOFANANOMALY…`,
both mid-word. I lumped a passing candidate in with failing ones.

**Where "it's English" is not the signal.** The Architect plaintext is 1,539
characters of unspaced English. *Every* offset lands on English, including all
the ones I called null. Recognisable text is guaranteed by the source, not
produced by the construction. Only the boundary test carries information, and
about **20.9%** of offsets begin a word — so one clean landing is a 1-in-5
event.

**What 193 costs to build.** The sum needs three unforced choices: drop X and Y
rather than solve for them; use |H| = 42 when the text defines H as 42 × −1;
use |B| = 16 when the text defines B as (5i − i)² = −16. The signed sum, which
takes **no** free choices, is 161 — and lands mid-word.

**Tested anyway.** `t[193:]` windows, `t[193:479]`, and the phrase itself as raw
and hashed passwords against all three blobs under both KDFs: 216 trials, 3
padding passes against ~0.8 expected (n is far too small for that ratio to
mean anything), **0 structural hits**, all outputs ~40% printable.

So: a real observation I was wrong to discard without testing, and still not
evidence once tested. Both errors are the same error — deciding before
measuring. `193` and `479` are both prime, which is worth writing down for
whoever picks this up next.


## Addendum 15b: the word-boundary test, run systematically

The user segmented the eight offsets by hand. That segmentation settles the
question, and it settles it against the reading that they are all meaningful:

| offset | first fragment | word it sits inside | clean? |
|---|---|---|---|
| 100 | `UALITY` | EVENTUALITY | no |
| 101 | `ALITY` | EVENTUALITY | no |
| 161 | `E` | UNABLE | no |
| **193** | `HARMONY` | HARMONY | **yes** |
| **479** | `PRIVATEKEY` | PRIVATEKEY | **yes** |
| 744 | `M` | IM | no |
| 767 | `E` | BECOME | no |
| 777 | `AR` | FAR | no |

Six of eight open on a stranded tail. "E TO ELIMINATE FROM" and "M SORRY TO
TELL YOU" read as English because the source is English, not because the offset
means anything.

**Then run it properly.** The spaced reading reconstructs to 332 words and
matches the authenticated plaintext exactly, giving a full boundary map: 332
word starts over 1,539 positions, **21.6%**. Testing every number the puzzle
produces — 5, 9, 15, 16, 24, 32, 42, 70, 82, 91, 95, 101, 121, 161, 163, 192,
193, 196, 479, 484, 570, 963 — and excluding the three offsets (1010, 1089,
1114) that are word starts *by construction* because I defined them as a word's
index:

| | |
|---|---|
| numbers tested | 22 |
| clean landings | 7 (31.8%) — 16, 32, 42, 95, 192, 193, 479 |
| expected by chance | 4.8 (21.6%) |
| P(≥7 by chance) | **0.18** |

**Not significant.** The landings are at the chance rate.

So 193's landing is real, and I was wrong to bin it — but it is not part of a
pattern, and a clean landing is not by itself evidence for any number.

**What actually distinguishes 479 is not where it lands.** It is that the
construction producing it has **zero free parameters** — 24 markers, first 24
primes, sum by colour, and the imbalance is itself a marker-carrying prime — and
that it consumes three separate creator hints exactly while producing a balanced
pair, which is the shape `yinyang` names. 193 needs three free choices to exist
and produces no balance. That difference, not the word it points at, is why one
is the frontier and the other is a coincidence.

## Addendum 16 — Executing "return to the source codes, reinserting the prime basics"

Read the phase 3.2 Architect block against the screenplay it was built from
(`gsmgio-5btc-puzzle-master/tmp/pdfs/architect-source.txt`). Almost all of it is
the film verbatim; what he changed is the message. The operative line:

| The Matrix Reloaded | His version |
| --- | --- |
| the function of **the One** | the function of **THE YOU** |
| return to **the Source** | return to **THE SOURCE CODES** |
| the code **you carry** | the code you **HOPEFULLY** carry |
| reinserting the **prime program** | reinserting the **PRIME BASICS** |
| **the Matrix** twenty three **individuals** | **OVER** twenty three **CIPHERS** |
| sixteen **female** | sixteen **ENCRYPTIONS** |
| seven **male** | seven **INTERTWINED PASSWORDS** |
| to **rebuild Zion** | to **FIND THE ACTUAL PRIVATE KEY** |
| *(nothing)* | **NOTE THAT ALSO BRUTE FORCING MIGHT BE REQUIRED** |

23/16/7 are the film's Zion repopulation quota, carried over with the nouns
swapped, so those counts are not an inventory of the puzzle. But the creator's
2023-02-23 image does decode to exactly **seven** phrases, in a stated order,
and phrase 1 is `yellowblueprimes` — "the prime basics."

### The terminal target, sized exactly

The phase 3.2 plaintext ends with an envelope: 128 base64 chars, 96 raw bytes,
salt `b45a5e3d827593ca`, **80 ciphertext bytes = 5 AES blocks**. The only
plaintext length matching the checkerboard's "half and better half" (two 32-byte
keys) is 64 bytes, which pads with 16 bytes of `0x10`.

**P(a wrong password yielding pad 16) = 2^-128.** This is the one target in the
puzzle where a hit proves itself. Every earlier sweep fought a 1/256 pad-1
false-positive rate; here there is effectively none.

### What was run, and what it returned

Three sweeps against that envelope, each candidate in raw and sha256-hex form,
under both the MD5 and SHA-256 EVP KDFs:

| Sweep | Candidates | Decrypts | Result |
| --- | ---: | ---: | --- |
| `final_block.py` — all five archived page sources whole, with `yellowblueprimes` and the first 24 primes reinserted at prime *offsets* (insert, never replace); source characters standing at prime offsets; all 5,040 orderings of the seven phrases concatenated; all 5,040 round-robin character intertwinings; prime-derived numbers fore and aft | 11,739 | 46,956 | pad 1×190 (183 expected), pad 2×2. Noise. |
| `lastwords.py` — phrase 3 names the sentence directly above this envelope; that sentence, the preamble, the 149-digit VIC string and the Architect tail, in seven normalisations, each combined with all seven phrases | 1,450 | 5,800 | pad 1×20 (22.7 expected). Noise. |
| `pipeline.py` — the seven phrases as an ordered pipeline, fed their actual derived values | 2,238 | 8,952 | pad 1×42 (35 expected). Noise. |

61,708 decrypts. The pad distribution matches chance at every point. The literal
reading of the instruction, applied to the archived source codes, yields nothing.

### One thing that did come out of it

`matrixsumlist` (phrase 2) had never been turned into a value. From the 350×350
poster read as a 14×14 grid, black/blue = 1:

    row sums  [6, 10, 8, 7, 6, 6, 5, 4, 9, 9, 7, 8, 7, 9]
    col sums  [8, 10, 8, 10, 8, 7, 3, 6, 7, 5, 9, 6, 6, 8]
    total     101

### Where this leaves the pipeline

Phrase 1 `yellowblueprimes` has a derived value (479). Phrase 2 now has one.
Phrase 3 names a locatable sentence. Phrase 4 `yinyang` has none — and it is the
only one the creator has spoken about operationally: *"when yingyang is reached,
2 hours max"*, *"It's the next phase."* Phrases 5–7 read as taunts, not
operations. `yinyang` is the gap.

## Addendum 17 — The two envelopes are twins

Sizing every envelope in the puzzle by its ciphertext length:

| Envelope | Raw | Salt | Ciphertext | Blocks |
| --- | ---: | --- | ---: | ---: |
| phase 2 keymaker | 672 | `06286612d43ed7ed` | 656 | 41 |
| phase 3 riddles | 4,112 | `9fbc451d13d071f4` | 4,096 | 256 |
| phase 3.2 | 2,448 | `eefc4c5befc1656a` | 2,432 | 152 |
| Cosmic Duality | 1,344 | `2d3f6fe06dc950e6` | 1,328 | 83 |
| **SalPhaseIon inner** | **96** | `3ab585348552415d` | **80** | **5** |
| **phase 3.2 terminal** | **96** | `b45a5e3d827593ca` | **80** | **5** |

The last two are the same size to the byte, and no other envelope is close. They
sit at the two ends of the unsolved region: one inside the SalPhaseIon letter
stream on a public page, one closing the phase 3.2 plaintext at the very end of
the chain.

80 ciphertext bytes hold at most 79 bytes of plaintext. **One 32-byte private key
padded to 64 bytes** fits, with 16 bytes of `0x10`. Two envelopes, one key each:

> INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALF

Keys, plural. Half and better half. **That is the duality** — not a symbol to
find, a pair of containers already built into the puzzle. It also explains why
`yinyang` is described as a *phase* reached *through a decryption* rather than as
a password: it is what these two blocks are.

### The inner envelope is not in the reference corpus

`ciphertexts/` extracts four blobs. The SalPhaseIon inner envelope is not one of
them — it is spliced across the letter stream, its two halves separated by the
word `enter` written as a 40-bit `a`/`b` run:

    …fidhz shabefour firsthintisyourlastcommand
    U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z
    abbaabababbabbbaabbbabaaabbaabababbbaaba          -> "enter"
    QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ
    shabefanstoo

Reassembled it is exactly 128 base64 characters and decodes to a well-formed
`Salted__` envelope. This is the **earliest-reachable unsolved target in the
puzzle** — it is on a page the creator published openly, behind no decryption —
and it carries the same 2^-128 self-proving property as the terminal block.

### Swept, null

- `yinyang` as a complement read of the poster: every spiral direction and
  orientation crossed with every inversion of the black/white/blue/yellow bit
  mapping. Only the known counter-clockwise inward read produces ASCII
  (`gsmg.io/theseedisplanted`). The poster is fully consumed.
- `twins.py`: both envelopes against everything the SalPhaseIon page states in
  plain text, the seven ordered phrases in all 5,040 orders, the pipeline values,
  and pairwise concatenations. 5,969 candidates, 47,752 decrypts —
  pad 1 × 196 (186.5 expected), pad 2 × 3. Noise.

### What is left un-actioned

One plain-English instruction in the whole puzzle has never been executed:
**`firsthintisyourlastcommand`**, written openly on the SalPhaseIon page,
immediately above the envelope it presumably opens.

## Addendum 18 — Executing `firsthintisyourlastcommand`; and placing the `#fefefe` cell

### The instruction, executed

Every candidate for "the first hint" from primary sources — the poster image name
and its decode, the rebus reading, the phase 2 gate and its URL, the page's own
neighbouring literals — in five normalisations, each used as the final password.
`shabefour`, the literal sitting immediately before the instruction, read as
"SHA, be four" gives an iteration count, so every candidate was also tried under
SHA-256 applied 1–8 times, in raw-digest, lowercase-hex and uppercase-hex form,
plus the puzzle's own hex-of-text chaining to depth 4.

69 candidates, 8,004 decrypts against both 5-block envelopes. Pad 1 × 25 against
31.3 expected. Nothing above pad 1. **Null.**

### The `#fefefe` cell — verified, indexed, and not new

The poster is RGBA truecolour, no palette, uniform alpha, and contains **five**
colours where the decode uses four. The fifth is `#FEFEFE`, and it occupies
exactly 625 pixels — one whole cell of the 196, perfectly aligned, every pixel of
it. Confirmed against an independent PNG decoder.

**This is not a discovery.** The chat has it from 2020 (`chat_transcript.txt:8952`,
"what about the white square which is fefefe color instead of ffffff") and 179
further mentions. It has been looked at for years and never resolved. Recorded
here so it is not re-found a fourth time.

What is worth adding is its exact position in the decode, which the write-ups do
not state:

    cell (row 7, column 4)
    counter-clockwise inward spiral index 163   (163 is prime)
    byte 20, bit 3 of the 192-bit payload
    character 20 of "gsmg.io/theseedisplanted" -- the 'n' of "planted"
    not one of the 24 marker positions (those are 7, 15, … 191)
    reads as 0 because the grid reader buckets it white; forcing it to 1 gives
      "gsmg.io/theseedispla~ted"  ('n' 0x6E -> '~' 0x7E)

Swept as password material against all three remaining envelopes in every form —
the index, the coordinates, the hex, the flipped message — crossed with the seven
phrases. 341 candidates, 6,138 decrypts, pad 1 × 28 against 24 expected. Null.

### Where the session's arithmetic now stands

Roughly 124,000 decrypts across this session against self-proving targets, every
pad distribution at chance. **Guessing passwords is finished as a method** — not
because the space is exhausted, but because the space has no structure to guide a
guess and the creator said the last step takes two hours once seen.

Six of the seven phrases now have an object. Phrase 6,
`itsinfrontofyoureyesbutyourenotseeingit`, is the one whose description fits the
`#fefefe` cell exactly: invisible on screen, invisible to the grid reader, sitting
in the very first artifact he published. Phrases 5 and 7 have no object at all.

### A note on how to read these sweep outputs

`pad` is not a score. It is the last byte of the decrypted block. PKCS#7 says a
plaintext ends with *N* bytes of value *N*; a wrong key produces 80 random bytes,
and if the last one happens to be `0x01` that is a **valid** padding of length 1.
It happens once in 256 tries and means nothing.

So a sweep of 8,004 decrypts should throw about **31** pad-1 passes by pure
chance. The `firsthintisyourlastcommand` sweep threw **25** — fewer than chance.
Every one of the 25 decrypts to 79 bytes of high-entropy noise, 25–54% printable:

    iwroteitmyself         sha6-raw  -> d4fc0a068f33f5569942789ff5b992eb…  28% printable
    follow the white rabbit    raw   -> 7efb61e841f5f3806c29207a0678cfa2…  37% printable
    half and better half   sha3-hex  -> e904861265276cea8ce218d0b6de657c…  39% printable

English runs about 99% printable. A private key is 0% printable but is exactly 32
bytes. Neither shape appears anywhere in the list.

The only outcome that means anything on these two envelopes is **pad 16** — a
64-byte plaintext, one 32-byte key — at probability 2^-128. The sweep scripts have
been changed to stop printing pad-1 rows at all: listing them makes noise read as
a shortlist.

## Addendum 19 — Re-running everything through the on-chain gate

**The correction.** Addendum 8 replaced a printable-ASCII filter with a PKCS#7 pad
filter, because a private key is 0% printable and the text filter would throw the
answer away. I then dismissed 25 pad-1 decrypts from the `firsthintisyourlastcommand`
sweep by citing their printability — the same mistake, one addendum later. Pad 1
is *uninformative*, not disqualifying: one wrong key in 256 produces it. The
structural detector was never actually run on those decrypts.

**The fix.** Two addresses held puzzle funds, so an acceptance test exists that
assumes nothing about what the plaintext looks like:

    Half         1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
                 hash160 a9553269572a317e39f0f518cb87c1a0ee1dbae4
                 uncompressed pubkey known on chain from its spends
    Better Half  17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa
                 hash160 4bc468447fe1b048ad030a2f9a125478eabc4ed6

`gate.py` decrypts, then slides a **32-byte window over all 80 bytes at every
offset**, derives the secp256k1 public key in both encodings, and compares against
those two hash160s and Half's exact public key. No pad filter. No text assumption.
Structural signals — EBCDIC cp1141, compression magic, printability — are reported
alongside but never used to reject. Self-tested against a key planted at an
arbitrary offset in random noise.

**The result.** `regate.py`, over both 5-block envelopes:

| | |
| --- | ---: |
| distinct candidate strings | 11,810 |
| password forms each (raw, sha256-hex, then SHA-256 ×1–8 in raw/hex/HEX) | 27 |
| decrypts | **1,228,240** |
| 32-byte windows derived and checked | ~120 million |
| **keys controlling either prize address** | **0** |

The 25 pad-1 decrypts that prompted this are included and hold no key at any
offset. The only structural flags raised were 2-byte compression-magic prefixes,
at 4 in 65,536 per decrypt — about 75 expected across the run by chance — and not
one of them decompresses under zlib, raw-deflate or gzip.

**What this closes.** The negative result no longer rests on any judgement of mine
about what a plaintext should look like. It rests on the blockchain. Every
candidate this session generated — the archived page sources with the prime basics
reinserted at prime offsets, all 5,040 orderings and all 5,040 character
intertwinings of the seven phrases, the pipeline values, the first-hint sweep under
repeated SHA-256, the `#fefefe` material — produces no key that controls Half or
Better Half.

## Addendum 20 — "Go back to the first puzzle piece": auditing the second-door hint

The creator's most-repeated unsolved hint, 2020-01-14, verbatim:

> "Roses are White but often Red. **Yellow has a number and so does Blue.** Go back
> to the first puzzle piece without further ado. It might have shown you only one
> door, beware that **the rabbits nest may contain a whole lot more.**"

He returned to it for two years: *"who knows what you'll find after opening the 2nd
door"* (2020-05-11), *"Really nobody managed to find the extra door"* (2020-08-02),
*"There is / Another / D O O R"* (2021-12-02), *"still a thing … we're not sure if
anyone has found another door so far"* (2021-12-25).

Taking it clause by clause against the actual image.

**"Yellow has a number and so does Blue."** The 24 markers on the first 24 primes,
Blue 484 / Yellow 479, imbalance 5 (itself blue-marked), zeroed → 479. Consumed.

**The community analyses a crop.** `gsmg.io/img/follow_the_white_rabbit.png` is
350×350 and holds only the grid. The poster page image is 1048×1556: the same grid
at 1047×1047, then a **15px `#ed1c24` bar spanning the full width at rows
1047–1061**, then 458 rows of branding. So the red exists only in the full poster.
"Roses are White but often Red" reads as a pointer to the uncropped image.

Checked what the crop discards:

| | |
| --- | --- |
| red `#ed1c24` | 15,705 px = 1047 × 15, one solid divider bar, no structure |
| below the bar | GSMG logo, "GSMG.IO 5 BTC PUZZLE CHALLENGE", a QR code, the address |
| QR payload | `https://www.blockchain.com/btc/address/1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` |
| `#fefefe` | 5,625 px = 9 × 625 — the *same single cell*, scaled 3× |

**The two images agree exactly.** Sampling both grids at cell centres: **0 of 196
cells differ.** (An earlier NEAREST downscale of 1047→350 reported a difference;
that was a resampling artifact at a non-integer ratio, not a discrepancy.)

**"The rabbit's nest may contain a whole lot more" — tested, and it does not.**
80 read orders (both spiral directions under all 8 dihedral symmetries, forward
and reversed, plus row-major, column-major and boustrophedon variants) × 8
bit-mappings × 8 start offsets = **5,120 readings** of the same 196 cells. The
only genuine string produced is `gsmg.io/theseedisplanted`. Everything else that
scores high is all-spaces (yellow and blue are too sparse to carry bytes) or a
transposed scramble of the same URL.

### What that leaves

The second door is in the first puzzle piece, by his own instruction. It is not a
second readable message, not the red bar, not the QR, and not a difference between
the two published images. The only anomalous object in the poster is the `#fefefe`
cell at (7,4) — spiral index 163, byte 20 bit 3, the `n` of "planted" — which is
white where nothing else in the image is off-palette, has been known since 2020,
and has never resolved.

Note the collision with the other standing hint: *"some characters need to be
'zeroed out'"* (2021-12-25). The `#fefefe` cell marks exactly one character
position in the one string the poster encodes.

## Addendum 21 — The gate was blind to keys stored as text

Addendum 19 replaced the pad and printability filters with an on-chain gate: slide
a 32-byte window over the plaintext, derive, compare against the two prize
hash160s. That is sound only under an assumption I never stated — **that the blob
holds the key as 32 raw binary bytes.**

People do not store keys that way. They write them down. And the fits are exact:

| what the 64-byte plaintext could hold | size | old gate |
| --- | ---: | --- |
| two raw 32-byte keys | 64 | caught |
| **one key as 64 ASCII hex characters** | **64** | **blind** |
| one WIF key (51–52 base58 chars) | 51–52 | blind |
| one raw key + 32 bytes of anything | 64 | caught |

A 64-character hex string fits these envelopes exactly — as good a fit as two raw
keys, and the likelier one for a human-authored payload. The gate would have
decrypted it correctly and reported nothing.

`gate.fullcheck()` now checks binary windows **and** text encodings: hex in either
case, hex re-scanned with whitespace stripped so a wrapped key still matches, WIF
with full checksum validation, and base64. Self-test, same key planted six ways:

    raw binary @8   FOUND      hex + newlines  FOUND
    64-char hex     FOUND      WIF             FOUND
    hex uppercase   FOUND      base64          FOUND
    control: 2,000 random 80-byte blocks -> 0 false positives

The `zeroed.py` run in progress under the old gate was killed rather than allowed
to finish; its result would have been unsound in exactly this way. **Addendum 19's
1,228,240-decrypt null is now a weaker claim than it reads** — it rules out keys
stored as raw bytes, not keys stored as text, and needs re-running on this basis.

Scope this still does not cover: if a blob holds the next stage's instructions or
a password for a further envelope rather than a key, no key-gate fires. That is
what `structure()` reports, and it stays advisory rather than a filter.

## Addendum 22 — The poster QR is pristine

A codeword-level parse of the poster QR shows:

    [bit 0]   ECI designator = 26 (UTF-8)
    [bit 12]  BYTE len=73: 'https://www.blockchain.com/btc/address/1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
    [bit 608] TERMINATOR
    612 of 640 bits consumed, 28 remaining: 0000111011000001000111101100

**The 28 trailing bits are standard padding, not payload.** Read from bit 612 they
look like `0e c1 1e`; realigned across the 4-bit terminator to the byte boundary
they are `EC 11 EC` — the ISO/IEC 18004 pad pattern, 0xEC and 0x11 alternating.
The data codewords end `... 42 65 00 ec 11 ec`.

**Version and geometry, from the image.** The QR occupies exactly 231 × 231 px and
231 = 33 × 7, so 7px modules and 33 modules across → version 4. V4 holds 100
codewords; 80 data + 20 EC is V4 at EC level L with a single Reed–Solomon block —
matching the parse.

**The only place a QR can hide anything is its error-correction capacity.** Flip
some modules, let Reed–Solomon silently repair them on decode, and the payload
still reads clean while the error pattern carries the real data. Tested directly:

    syndromes S0..S19: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

    EC recomputed from the data: 32801c47d4426e091d7fed6583b7cf7ee08a12af
    EC as printed on the poster : 32801c47d4426e091d7fed6583b7cf7ee08a12af   identical

All twenty syndromes zero and the EC codewords recompute byte-for-byte. **No module
was ever altered**, so there is no repaired-error pattern to recover. The symbol is
a stock encoding of the URL.

On the ECI header: emitting ECI 26 for an all-ASCII URL is unnecessary and costs
12 bits, but several generators (ZXing with a forced charset among them) do it by
default. It identifies the tool, not a secret. It is also why OpenCV logs
"ECI is not supported properly" when decoding this symbol.

The QR is closed. It carries the prize address and nothing else.

## Addendum 23 — The diagonal is the redundancy restated

A proposed finding: *all 24 coloured modules lie on diagonals where
`(col − row) mod 4 == 1`.* Verified — all 24, no exceptions. Module census also
verified: black 86, white 85, blue 15, yellow 9, one off-white, 196 total.

But it is not independent information. Asking where **every** cell at the marker
positions falls, regardless of colour:

    spiral index ≡ 1 mod 8 -> (col-row) mod 4 == 3  (all 25)
    spiral index ≡ 3 mod 8 -> (col-row) mod 4 == 1  (all 25)
    spiral index ≡ 5 mod 8 -> (col-row) mod 4 == 3  (all 24)
    spiral index ≡ 7 mod 8 -> (col-row) mod 4 == 1  (all 24)   <- the markers

The spiral changes `col − row` by ±1 per step, so the residue cycles with period 4
along it and odd spiral indices force odd residues. The markers sit at index ≡ 7
mod 8 — the last bit of every byte. **"All 24 lie on that diagonal class" is
therefore the same fact as "the markers land on every 8th spiral cell", expressed
in Cartesian coordinates instead of spiral ones.** It is the F73D92 redundancy
again, not a second structure.

Filed because it is a clean example of the failure mode this audit exists to
catch: a restatement in new coordinates reads as a discovery.

### The ledger reading, and what blocks it here

The proposal that *"the rabbits nest may contain a whole lot more"* points at the
prize address's **transaction history** rather than at the poster is coherent —
the poster's last remaining output is that one blockchain.com link, and outputs to
vanity addresses are a known way to push data onto the chain.

Two things to weigh against it. The creator answered *"Nope"* when asked in
2023-11 whether internet was still required, and *"No need. You have all the
info."* Reading a ledger is not offline. Against that, he also said
*"I only need to look at the address"* (2026-03-03) — though in context that reads
as watching for the prize to move, not as a pointer to its history.

**Untestable in this environment:** `blockchain.info`, `mempool.space` and
`blockstream.info` are all refused at the egress proxy (403 on CONNECT, logged in
the proxy's own `recentRelayFailures`). Anyone with chain access should check:

1. Every output address in Half's spending transactions, for vanity prefixes.
2. `OP_RETURN` outputs in any transaction touching either address.
3. Whether Better Half's funding transaction has an unusual output structure.
4. Signature `r`-values across Half's spends, for nonce reuse — the one flaw that
   would recover a private key directly, historically common, and apparently never
   checked by anyone in the corpus.

## Addendum 24 — The chain, verified; and a balance claim corrected

Chain data was fetched by an agent with network access (this environment's egress
proxy refuses block explorers). **None of its parse is taken on trust.**
`verify_chain.py` works from the raw transaction hex alone: it recomputes both
txids by double-SHA256, re-extracts `r`/`s` from the DER in each scriptSig,
rebuilds the legacy sighash `z` from scratch, and verifies every signature against
the public key. Every value reproduces, and **all six signatures verify** — which
is what makes the result below trustworthy rather than merely asserted, since a
wrong `z` construction would fail verification rather than pass silently.

### Correction: the prize

Earlier addenda and the PR body say *"The prize address holds ~1.25 BTC, unmoved."*
**Wrong on both counts.**

| | | |
| --- | ---: | --- |
| Half `1GSMG1…prBe` | 125,635,374 sat = 1.25635374 BTC | has **spent, twice** |
| Better Half `17ucy1…fyHa` | 375,055,856 sat = 3.75055856 BTC | never spent |
| **total** | **500,691,230 sat = 5.00691230 BTC** | |

The full 5 BTC is still there. It is split across the two addresses, and Half is
not untouched.

### The halving pattern — creator-authored, verified

    2019-04-13  block 571497  funded            5.000 BTC
    2020-05-11  block 630001  -> Better Half    2.500 BTC   halving at 630000
    2024-04-24  block 840725  -> Better Half    1.250 BTC   halving at 840000

Each spend moves **exactly half** of the round original, at the halving. The first
was created at tip 629998 — two blocks *before* the 2020 halving — and confirmed at
630001, one block after. The second was created at tip 840003, three blocks after
the 2024 halving, and confirmed 722 blocks later at a low fee.

Caveat kept explicit: Bitcoin Core sets `nLockTime` to the current tip to
discourage fee sniping, so **629998 and 840003 are wallet artifacts recording when
he broadcast, not digits he chose.** The deliberate part is the timing and the
exact-half amounts. This is "half and better half" enacted on chain — a gesture
confirming the structure, not a channel carrying bits. The next halving (block
1,050,000, ~2028) predicts a 0.625 BTC move.

**He signed with Half's key in April 2024.** The keys are live and held.

### The four checks: all null

| check | result |
| --- | --- |
| 1 — vanity / message-bearing outputs | The two spends produce four outputs, all P2PKH, all to the two puzzle addresses. No third-party outputs, no dust fan-out. |
| 2 — OP_RETURN | 105 OP_RETURNs across transactions touching the addresses, and **every one is inbound, written by solvers.** Neither puzzle key has ever published a byte. |
| 3 — Better Half's funding | The two spends above. Exactly round values, standard P2PKH, ordinary fees, nothing embedded. Output order flips between them, which is ordinary randomised change position. |
| 4 — nonce reuse | 6 signatures, 6 distinct `r`, all verified. **No reuse. The prize is cryptographically safe.** |

The inbound OP_RETURN traffic is worth naming for what it is: solvers guessing at
each other and at the creator — `hereismysecret`, `#SOLUTION`, `isolveditwithanabacus`,
`matrixsumlistenterlastwordsbeforearchichoicethispassword`, `yourlastcommand`.
Anyone mining the chain for creator hints will find this instead and mistake it for
signal. It is a mirror of the community, not a message from him.

**Verdict on the ledger reading of "the rabbits nest may contain a whole lot more":
closed.** The transaction history is not the second door.

## Addendum 25 — The halving split was designed, announced, and confirmed live

Was the halving structure planned, or improvised? The transcript settles it. All
times converted from the export's UTC−05:00 to UTC.

    2019-04-13 16:32  puzzle funded, 5.00000000 BTC        394 days before the halving
    2020-05-09 06:36  a solver posts the decrypted checkerboard message:
                      "IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG
                       TO HALF AND BETTER HALF AND THEY ALSO NEED FUNDS TO LIVE"
    2020-05-11 19:23  halving, block 630000
    2020-05-11 19:24  "game over"
    2020-05-11 19:25  x7x7x7x6: "the half of prize went to better half"
    2020-05-11 19:26  CREATOR: "Well spotted"
    2020-05-11 19:26  CREATOR: "Happy halving!"
    2020-05-11 19:31  CREATOR: "It'll high likely be worth more than it once the
                       price was 5 btc. Next halving in 209999"
    2020-05-11 20:02  2.5 BTC lands in Better Half, block 630001

So:

1. **The instruction predates the event by two days** — and it was inside an
   AES blob, so the creator wrote it well before that. He could not have added it
   afterwards; the ciphertext was already public and already broken.
2. **The transaction was pre-built.** Its `nLockTime` is 629998 — two blocks
   *before* the halving. He had it signed and waiting.
3. **He confirmed the design in real time**, in chat, sixty seconds after a solver
   called it, and immediately named the next one: *"Next halving in 209999."*
   630000 + 210000 = **840000**, which is exactly where the second split happened.

The puzzle was **not** launched to catch the halving — 13 months is not timing.
What was designed is the *prize's behaviour*: it halves itself at every Bitcoin
halving, moving into Better Half, and he said so on the day.

    2019   5.000 BTC funded
    2020   2.500 -> Better Half   (block 630000, announced)
    2024   1.250 -> Better Half   (block 840000, as announced in 2020)
    2028   0.625 predicted        (block 1,050,000)

This reframes what "half and better half" is. It is not only a phrase in the
checkerboard and not only a pair of key containers — it is a **live mechanism**
that has executed twice on schedule. It also explains the shape of the two 5-block
envelopes: two keys, because there have always been two addresses, by design,
from before the first split.

One thing it is not: a channel. Nothing in it carries bits. And the locktimes are
Bitcoin Core anti-fee-sniping artifacts, not chosen digits — 629998 records *when
he built the transaction*, which is the interesting fact, but the number itself is
not a message.

## Addendum 26 — "Hundred fourty" is a character count, and a dating constraint

### The 140 is a pointer, not a multiplier

The Phase 2 page sends you to Bitcoin's raw data:

> "a chancellor awaiting banks to be bailed out decided to write an anarchist
> digital answer to this worlds' misery. **Its' raw data after 4 on row 1616**"

The community resolved "row 1616" to **line 1616 of Satoshi's source**, holding the
genesis coinbase scriptSig. The Architect plaintext then back-references it:

> "THAT WHAT A WISE MAN ABOVE HINTED AT IS WORTH **HUNDRED FOURTY** OF THE INVESTMENT"

    genesis coinbase message : 69 bytes
    as hex                   : 138 characters
    with a leading "0x"      : 140 characters   <-- HUNDRED FOURTY

**Correction.** Addendum 16 and the creator profile read that line as "worth 140×
the investment" — a Venus Project fundraising remark. It is not. It is a character
count pointing at a specific 140-character string, and "a wise man above" is the
chancellor/Satoshi figure described earlier on the Phase 2 page, not a vague
reference to the text above.

### A dating constraint that closes a direction without any chain data

Whether halving-block data *can* key a ciphertext depends on whether the
ciphertext existed before the block did. Earliest appearance in the Telegram
export (times converted from UTC−05:00; the 2020 halving is 2020-05-11 19:23 UTC):

| ciphertext | first seen | vs the 2020 halving |
| --- | --- | --- |
| **phase 3.2 terminal envelope** `U2FsdGVkX1+0…` | 2020-05-09 13:44 | **30 hours BEFORE** |
| phase 3.2 plaintext (checkerboard message) | 2020-05-09 06:36 | 2 days before |
| Cosmic Duality `U2FsdGVkX18tP2…` | 2021-04-16 09:44 | 339 days after |
| SalPhaseIon letter stream | 2021-04-16 09:38 | 339 days after |
| SalPhaseIon page URL `89727c59…` | 2022-05-27 14:11 | 745 days after |
| SalPhaseIon inner envelope `U2FsdGVkX186tY…` | 2023-08-06 00:23 | 1,181 days after |

**The terminal envelope cannot be keyed by block 630000 or 840000.** A solver
posted its ciphertext 30 hours before block 630000 was mined; the block did not
exist. That closes the direction for that target with no chain access required.

For Cosmic Duality and the SalPhaseIon inner envelope it stays open — but stated
precisely, that is *not ruled out*, not *supported*. First-seen-in-chat is a lower
bound on publication, not a creation date.

### Genesis swept

The genesis block is reconstructed from protocol constants in `genesis.py` and
**verified by its own hash** (`000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f`),
so nothing here is recalled. 690 candidate strings — the message in every casing,
its hex forward and reversed, with and without `0x`, the scriptSig with and without
the `04ffff001d0104` push ("raw data *after 4*"), the full raw block, header,
merkle root, block hash, and the nTime / nonce / bits constants — each crossed with
the seven phrases and run through the on-chain gate against all three remaining
envelopes.

## Addendum 27 — The whitepaper: forensically clean, and not the "1616" target

The Bitcoin whitepaper PDF, examined as a possible carrier.

**Identity.** `sha256 b1674191a88ec5cdd733e4240a81803105dc412d6c6708d53ab94fc248f4f553`
— the canonical paper, the same bytes embedded in the blockchain.
184,292 bytes, 9 pages, PDF 1.4, `/Producer OpenOffice.org 2.4`, `/Creator Writer`,
`/CreationDate D:20090324113315-06'00'`.

**Container: clean.** Parsed with pikepdf rather than by hand:

| check | result |
| --- | --- |
| streams | 23, **every one decodes exactly as its dictionary declares** |
| embedded files / attachments | none |
| JavaScript, `/Launch`, `/AA`, `/RichMedia`, `/GoToE` | none |
| `/Names`, `/Metadata`, `/AcroForm` | absent |
| `/OpenAction` | present, but only `[page1 /XYZ null null 0]` — OpenOffice's "open at page 1" |
| object types | Catalog, Pages, Page, Font, FontDescriptor — nothing else |
| appended data | none; one `%%EOF`, one trailing newline |
| encryption / linearization | neither |

Two of my own scanning passes produced false positives before this and are worth
recording, since both are the standard way to imagine a discovery into a PDF:

- A regex for `stream\r?\n` also matches the tail of **end**`stream`, which
  "found" a non-inflating `/FlateDecode` stream at offset 82704. There is no
  stream there.
- Searching backwards for `/Length` picked up unrelated values (3, 6, 9, 12 …,
  which are object numbers), making every stream look mis-declared.

Neither survived using a real parser. **All 23 streams are exactly what they say.**

**Why the text will not extract.** The paper embeds subset fonts with **no
`/ToUnicode` CMap**; content streams are raw glyph indices (`<01><02><03>…`).
That is a known quirk of Satoshi's OpenOffice export and the reason the original
resists copy-paste. It is not a hiding place.

**It is not the "row 1616" target.** In the plain-text paper (21,395 chars, 643
lines, 3,568 words) there is no line 1616, and nothing meaningful sits at char
1616, word 1616, or any byte-row width. Decisively:

    "chancellor"  0 occurrences        "hundred"  0 occurrences
    "bailout"     0 occurrences        "fourty"   0 occurrences
    "anarchist"   0 occurrences        "1616"     0 occurrences

Every one of those words comes from the genesis block coinbase or the creator's
own prose, not from the paper. The Phase 2 clue points at **line 1616 of Satoshi's
source code**, which holds the genesis coinbase scriptSig — as the community
resolved it, and as the 140-character count in Addendum 26 confirms.

`whitepaper.py` sweeps the file's identifying values anyway — its three digests,
size, dates, producer string, title, author, and the raw file bytes as a password
— against all three envelopes through the on-chain gate.

## Addendum 28 — Genesis block dossier

`genesis_dossier.py`. Nothing recalled: the block is rebuilt from protocol
constants and the reconstruction is **proved by its own double-SHA256 matching the
known genesis hash** — one wrong byte and it would not match. The address
derivation carries a second assertion against the known genesis address.

    block hash    000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f

**Header, 80 bytes**

| field | value |
| --- | --- |
| version | 1 |
| prev block | all zero |
| merkle root | `4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b` |
| nTime | 1231006505 = **2009-01-03 18:15:05 UTC** |
| nBits | `0x1d00ffff` (difficulty 1) |
| nonce | 2083236893 |

**Coinbase transaction** — txid equals the merkle root, since the block holds one
transaction. Output 50 BTC to a bare P2PK script; pubkey hash160
`62e907b15cbf27d5425399ebf6f0fb50ebb88f18`, address
`1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`. **Not spendable** — the genesis coinbase is
excluded from the UTXO set by consensus.

**The scriptSig, which is what "row 1616" holds**

    04 ffff001d   push 4 bytes -> 0x1d00ffff little-endian, the nBits value
    01 04         push 1 byte  -> the number 4        <-- the "4" in "after 4"
    45 <69 bytes> push 0x45    -> "The Times 03/Jan/2009 Chancellor on brink
                                  of second bailout for banks"

**Line 1616 of Satoshi's `main.cpp`** renders that scriptSig as a comment:

    // txNew.vin[0].scriptSig = 486604799 4 0x736B6E616220726F662074756F6C6961…

`486604799` is `0x1d00ffff`; `4` is the second push; and everything **after the 4**
is the hex — which is the message **byte-reversed** (`73`=s `6b`=k `6e`=n `61`=a
`62`=b → "sknab" = "banks" backwards). Its length is `2 + 138 = ` **140**. That is
the Phase 2 clue and the Architect's "HUNDRED FOURTY" resolved against verified
data.

**Sizes:** full raw block 285 bytes, coinbase tx 204, scriptSig 77, message 69
(138 hex chars).

### A bug of my own, recorded

The first run of this dossier printed the genesis address as
`12PNCrQmt3MD962F7R2Lf1AnZb9jEdTDXL`. Wrong: I hashed `scriptPubKey[1:]`, which
keeps the trailing `0xac` OP_CHECKSIG, instead of `scriptPubKey[1:-1]`. That
address is an artifact and appears nowhere in Bitcoin. The script now asserts the
derivation against `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa` so the error cannot recur
silently.

Note the shape of that mistake: the block hash still verified, because the raw
bytes were right — only my *interpretation* of them was wrong. A self-check on one
part of a pipeline does not validate the rest of it.

## Addendum 29 — I was wrong about Cosmic Duality. The hash is a live door.

**Retracting Addendum 3.** That addendum called `cosmic_plaintext.bin` a padding
collision — 1,327 bytes against a 1,328-byte ciphertext (PKCS#7 pad 1), entropy
7.87, incompressible — and dismissed the whole claimed Cosmic Duality solution as
noise. The measurements were right. **The conclusion was wrong.**

The Wayback CDX index for gsmg.io settles it:

    sha256(cosmic_plaintext.bin) = 4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081
    captured  https://gsmg.io/4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081
              2026-07-08 02:03:44   200   1,253 bytes   digest GQEFKYYM6SDEVTLMJJNQDISN23QSVDSB

**gsmg.io serves a real page at the SHA-256 of that file.**

### Why this is a real page and not a 404

The GSMG site is a single-page app that answers 200 for unknown paths, so status
means nothing — but capture size separates them cleanly. Among 70 html captures
from 2026:

| | |
| --- | ---: |
| `/choiceisanillusioncreatedbetweenthosewithpowerandthosewithout` — the real Phase 2 page | **1,223** |
| `/4f7a1e4efe…9c081` | **1,253** |
| `/phase1` `/phase2` `/phase3` `/salphaseion` `/merovingian` `/whiterose` `/followthewhiterabbit` … | ~12,2xx |
| the same Phase 2 path with extra text appended (a wrong guess) | 12,970 / 13,059 |

Two orders of magnitude apart. And **eight other 64-hex-character paths were tried
by solvers in 2026 — `f9719d6d…`, `21ef0533…`, `c1780cbb…`, `c2eef34b…`,
`673e3b1a…`, `0b0f37ec…`, `e24bd2c0…`, `10d6a2c5…` — and every one returned the
~12,2xx shell.** One hash out of nine resolves. That one is the hash of this file.

This also matches the puzzle's own convention: the SalPhaseIon page is served at
`/89727c598b9cd1cf…`, a 64-hex path. **Decrypt a stage, SHA-256 the plaintext, and
that digest is the next URL.** Under that convention a 1,327-byte high-entropy
plaintext is exactly what you would expect — it is not meant to be read, it is
meant to be hashed.

### Where my reasoning failed

Pad 1 occurs for 1 wrong key in 256, so it is **uninformative** — it is not
evidence the decrypt is wrong. I treated weak evidence against as proof against,
then stacked entropy and incompressibility on top, when both are equally consistent
with a plaintext that is itself key material or compressed data. This is the mirror
image of the error the rest of this audit was written to catch: I was so tuned to
reject false positives that I manufactured a false negative, and I did it to the
one piece of community work that was actually correct.

### Timeline

    2026-07-08 02:03  the archive captures gsmg.io/4f7a1e4e…  (200, 1,253 bytes)
    2026-07-12        creator: "Some already found it. And understood not to
                      risk it… 🤐"

Four days.

### The immediate action

    https://web.archive.org/web/20260708020344/https://gsmg.io/4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081

This environment's egress proxy refuses `web.archive.org`, so it must be fetched
elsewhere. That page is the next stage.

## Addendum 30 — Retracting Addendum 29. My "live door" was an era artifact.

**Addendum 29 is wrong and is withdrawn in full.** The live site settles it:

    GET gsmg.io/4f7a1e4efe…9c081   -> 404, 9 bytes, "Hello :-)"
    GET gsmg.io/4f7a1e4efe…9c08 2  -> 404, 9 bytes, "Hello :-)"     (last char changed)

A deliberately wrong hash returns exactly the same thing. The site does not
discriminate. There is no door.

### The control I did not run

I compared a 2026-07-08 capture (1,253 bytes) against 2026-01/04 captures
(~12,2xx) and attributed the gap to real-page-versus-404. It is
**before-versus-after a site change**:

    2026 captures BEFORE 2026-07-01 :  61   sizes 10,595 – 13,059
    2026 captures AFTER  2026-07-01 :   9   sizes    794 –  2,040

    last big capture   2026-04-24  12,221  /89727c598b9c
    first small one    2026-07-07     846  /

Everything after the change is small because gsmg.io now serves a 9-byte
placeholder. And the small band contains obvious garbage — three of the nine are
**lodash source-code fragments** a scanner submitted as URLs
(`/returns truthy for **all** elements of` at 1,216 bytes, `/. */ function
baseInRange(number, start, end) {…` at 1,411). My "real page" at 1,253 sits
between them.

My control was broken too: `/choiceisanillusion…` at 1,223 bytes is dated
**2026-08-09**, also after the change. I compared two placeholders and called one
a door.

The distinct content digests I also leaned on prove nothing either — every small
capture has a unique digest, because the placeholder response varies per request.

### Restoring the record

Addendum 3 is **not** thereby vindicated. Its measurements were right and its
reasoning was still weak: pad 1 occurs for 1 wrong key in 256 and is
*uninformative*, and high entropy is equally consistent with key material. The
honest status of `cosmic_plaintext.bin` is **unresolved** — not proven wrong, not
proven right. The archive capture of that path means only that a solver once
requested it.

### What actually happened here

Within one hour I produced both failure modes this audit exists to catch, in
sequence, on the same object:

1. **Addendum 3** — a false negative. Treated uninformative evidence as
   disproof.
2. **Addendum 29** — a false positive. Found a striking coincidence, verified the
   hash match rigorously, wrote it up with tables and a timeline, and never asked
   the one question that mattered: *are these two numbers even measured on the
   same thing?*

The hash match was real and exactly verified. Everything I built on it was
worthless, because the comparison underneath it was not controlled. Verifying a
component says nothing about the inference drawn from it — the same lesson as the
genesis address bug in Addendum 28, learned again two addenda later at much
higher cost.

## Addendum 31 — Sweep status at close of session

| sweep | candidates | decrypts | prize-key matches | status |
| --- | ---: | ---: | ---: | --- |
| `regate.py` (all earlier candidate sets) | 11,810 | 1,228,240 | 0 | complete — but under the *old* gate; see Addendum 21 |
| `genesis.py` | 690 | 41,400 | 0 | complete, `fullcheck` gate |
| `whitepaper.py` | 729 | 43,758 | 0 | complete, `fullcheck` gate |
| `zeroed.py` | 16,491 | ~300,160 of ~659,640 | 0 | **INCOMPLETE — the process died at 45%** |

`zeroed.py` was killed twice by shell teardown and, on its third run under
`setsid`, stopped at roughly 300,160 decrypts without printing its summary. **It is
not a completed null.** Anyone continuing should re-run it to completion rather
than cite it.

The only structural flags across all runs were 2-byte compression-magic prefixes
at 4 in 65,536 per decrypt — the expected rate — and none decompresses.

**Addendum 19's 1.23M-decrypt result also still needs re-running**, because it
predates the `fullcheck` gate and therefore only rules out keys stored as raw
bytes, not keys stored as hex, WIF or base64.

## Addendum 32 — Extra door measured; named twin opening; Gate C is for decrypts

**Date.** 9 Sep 2026. Scripts: `extra_door_right_object.py`,
`yinyang_carry_values.py`, `unique_use.py`, `next_object.py`,
`open_named_envelope.py`. Status file: `analysis/EVIDENCE_STATUS.md`.

### The three envelopes are still the lock

Nothing in this session opened Phase 3.2 nested (`b45a5e3d827593ca`),
SalPhaseIon AES (`3ab585348552415d`), or Cosmic Duality
(`2d3f6fe06dc950e6`). Prize keys still belong *in a decrypt* (VIC: Half and
Better Half). Gate C on already-solved plains is the wrong object.

`next_object.py` slid 32-byte windows of Architect, outer 3.2, VIC, and the
first-hint SHA-256s (including Jrk `#225` / phase-1 flower hash
`5ac40783…`) as secp256k1 scalars against both prize hash160s. coincurve
available; compressed and uncompressed. **0 hits.** That closes those
readings only. It does not close the blobs.

### Extra door: values, not a GET

Door 1 control still holds: 14×14 CCW inward, black/blue=1, skip nest,
start 0 → `gsmg.io/theseedisplanted`.

The eight seed tiles in HTML order, red=1, pack to byte **15** — the same
15 as Blue's poster count and the X2SH literal. Yellow is still 9; no
yellow tile on the seed page. Packed `09||0f` is not a URL.

Unused *Warning* verses through the same 8-bit codec start-0 round-trip the
verse. That is tautology, not a second door. They name the mechanic
(opposites → 479=479; physical → local extra door; red/black → tile bit).
`gsmg.io/<lyric>` is not a path.

The 9th yellow cell is spiral index 191 `(5,6)`; the 15th blue is 183
`(8,5)`. Both already spend as door-1 bits of `planted` (`d` / `e`).
`#fefefe` at `(7,4)` is 0-based **163** (prime). The `second_door.py`
comment that said 162 was off by one; Addendum 18's 163 was right.

The extra door in the first piece is **still unfound**. These measurements
stop treating 9, 15, and leftover lyrics as OpenSSL passwords or Wayback
paths.

### Y=9 is not an X2SH fill

Two-row board as in `board_80_81.py`: X-row `|H|=42` → 80; Y-row `B=-16`
→ 81. Putting Yellow's 9 into Y makes 90 vs 80. QWERTY puts Y over 6, I
over 9. Drop Y=9 as a fill. 9 stays an index. X stays a hole. Raising the
stakes: do not invent a third number.

479=479 remains the yellowblueprimes construction (yellow 479, blue 484,
imbalance 5 zeroed). Whitespace-strip compact is **1544** (punctuation
kept); letters-only is **1539**. Addendum 32's 479/480 first-or-zero pair
is the 1544 reading. See Addendum 33: that pair is an apostrophe artifact.

### Named way to open a twin: landings + Salph KDF — null on A/C

Declared arrival: A or C on a **decrypt**, twins first. Cosmic Duality has
no adjacent password and is the 1.3 KB document (gate D); the chat's own
dependency is that a Salph result opens it.

Materials were the landings, not the digits:

    arch[479:511]  EPRIVATEKEYYOUVEEARNEDITBUTPLEAS
    arch[480:512]  PRIVATEKEYYOUVEEARNEDITBUTPLEASE

plus concat, both interleaves, `THEPRIVATEKEY` / `PRIVATEKEY`, the last
working Phase 3.2 OpenSSL hex, and the SalPhaseIon literals
`ourfirsthintisyourlastcommand` / `thispassword`.

KDF 1: EVP SHA-256, same as every solved envelope (raw, sha256-hex,
sha256-raw). 114 trials on both twins.

KDF 2, SalPhaseIon-only reading of `shabef` / `shabefanstoo`: AES-256-CBC
`key = sha256(pw)`, `iv = sha256(pw || salt)[:16]`. 44 trials.

Pad-1 omitted. **0 Gate A, 0 Gate B, 0 Gate C.** Barrystyle PNG: IHDR /
IDAT / IEND only, LSB planes not printable. Cosmic was not decrypted.

This is a closed named attempt, not a proof the landings are unused
elsewhere. Guessing more phrasings of 479 is not the next step.

### Binaries (already in EVIDENCE_STATUS)

Puzzle PNG `sha256 38125bbd…` recovered; byte-identical across Reddit /
Wayback 2020-11-12 / GitHub. No CDX row before Nov 2020. Barrystyle Cosmic
cover `sha256 3a9b0a6e…` recovered from Telegram `#8310`.

## Addendum 33 — Compaction rule, unread Salph blocks, nest-module Gate A

**Date.** 9 Sep 2026. Script: `analysis/nest_module_door1.py`. Log:
`analysis/out/nest_module_door1.txt`.

### 1544 vs 1539 is punctuation, not first-or-zero

`"".join(text.split())` keeps 4 apostrophes and 1 hyphen → **1544**.
Letters-only → **1539**, which is how every solved password in this puzzle
is built. Apostrophes in the whitespace-compact sit at 352, 595, 746, 788;
only **352** is before offset 479. That one mark is why 1544 opens
`EPRIVATEKEY…` at 479 and `PRIVATEKEY…` at 480. Under letters-only, 479
opens `PRIVATEKEY` and there is no first-or-zero pair.

Addendum 32's named-twin 0-arrival used the 1544 landings. That null is
about a manufactured object. Do not re-run those landings in any KDF.
Do not treat 1539 landings as already closed.

`second_door.py` called `#fefefe` spiral 162 0-based. Measured 0-based
index of `(7,4)` is **163** (prime). The 162 password material is removed.

### Nest at module resolution — the packing that was missing

FINDINGS already named the 70×70 / 15px raster. `rabbit_subunits` and
`wrong_object_doors.py` sampled the nest **row-major**, or spiralled the
whole 70×70. This pass ran door 1 unchanged on:

- nest 10×10 (modules 30–39): black/white only, 22 K / 78 W
- seven mixed cells `(6,6)(6,7)(7,6)(7,7)(7,8)(7,9)(8,6)` (175 modules),
  concatenated in door-1 cell order, each 5×5 spiralled

Black-module counts 4,9,6,3,9,4,2. At 15px **every one of the seven
cells is majority-white** (W = 21,16,19,22,16,21,23). `(7,6)` is K=6 /
W=19 — 19 is white, not ink. Black counts and minority counts are the
same number; there was no majority/minority conflation. Seven-cell black
total 37; nest 10×10 is 22 K / 78 W.

Door 1's 75px vote can still label `(7,6)` black. The spill cells
`(7,8)(7,9)(8,6)` are majority-white at both scales, so door 1 packed
them as **white = 0**. The drawing perturbs nothing in door 1's output.

Variants: CCW (door 1) and CW, invert, start 0/1. Remainder bits dropped.
EVP SHA-256, both 5-block twins, 246 trials (123 unique passwords).
**null-for-Gate-A.** The nest carries no payload under door 1's alphabet.
"The rabbits nest may contain a whole lot more" is not pointing at bits
in those 100 modules. Lead retired. Do not re-run. Cosmic not attacked.

The 175-module footprint is not a rectangle, so one spiral over it would
invent an order; seven 5×5 spirals was the defensible read and is done.
100 bits is not 12 bytes — dropping 4 is a choice, not a mechanic — but
the failure mode is the named one: line art in door 1's two colours.

### SalPhaseIon `dbbi` / `faed`

661 symbols, no `o`. Length-reconciled in the 1,075-char stream. Not
decoded. Not a closed null. No construction in this addendum.

## Addendum 34 — `#fefefe` as operator, not passphrase

**Date.** 9 Sep 2026. Scripts: `analysis/fefefe_operator.py`,
`analysis/matrix_coords.py`. Logs: `analysis/out/fefefe_operator.txt`,
`analysis/out/matrix_coords.txt`.

The remaining cluster was an *interpretation* problem: `#fefefe` → 254 →
half 127 (`DEL`) → “zeroed out” → “first or zero” as one binary/edit
operation on known strings, then hash or decrypt. Prior sweeps replaced
URL index 20 with `0` / NUL / DEL; they did not AND-mask `0xFE`, insert
`0x7F`/`0x00`, wrap first-or-zero onto shorter strings, door-hash the
mutated bytes, or treat orig/mutated as a yinyang pair.

### Operator family (Gate A + E)

Bases: `gsmg.io/theseedisplanted`, `theseedisplanted`, `/theseedisplanted`,
letters-only Architect `[479:511]` =
`PRIVATEKEYYOUVEEARNEDITBUTPLEASE` (1539, not the 1544 pair),
`ourfirsthintisyourlastcommand`.

Locations: 19, 20, 21, and those indices modulo length (so the short
path is not stuck at `163 % 16 = 3` only). Ops: delete; insert/replace
`0x7F` and `0x00`; mask char / all / prime indices with `0xFE`; flip
LSB; replace with `t`. Identity mutations dropped (`maskFE` on an even
byte is a no-op).

Then: raw / sha256-hex / sha256-raw / shabef-ans-too KDF against both
twins; `sha256` and double-`sha256` of the mutated bytes vs pre-2026-07
CDX. Gate E now also rejects the ~12,2xx SPA shell (Add.29), not only
the 700–2100 placeholder band.

**147 unique mutations. 0 Gate A. 0 Gate E.**

A first-pass CDX row `e24bd2c0…` (2026-01-05, html 12276) was
`maskFE` on `hint[18]='l'` — already even, so the unmutated
`sha256(ourfirsthintisyourlastcommand)` SPA shell already listed in
Add.29. Not a door.

The unmutated 1539 landing was included in this KDF pass. Still 0.
Do not re-run 1544 landings.

### Twin protocol (still `#fefefe` / yinyang, not 479/484)

For each (original, mutation) pair plus named pairs `half`/`betterhalf`,
`first`/`zero`, `one`/`zero`, `\xfe`/`\x7f`, `254`/`127` (both orders):

- `p1||p2`, `p2||p1`, `sha256` of each concat, EVP SHA-256
- `key=sha256(p1), iv=sha256(p2)[:16]` and the swap; XOR of the two
  hashes as key
- SalPhaseIon `enter` split: first 2 ciphertext blocks with `p1`, last 3
  with `p2`, second IV from KDF or from the last block of the first half

Digits 9 / 15 / 479 were not used. Cosmic not attacked.

**3,688 trials. 0 pad-16.**

### `matrixsumlist` as coordinates (criterion 5, no AES)

Add.15 used the sums as Architect offsets. This pass used them as
`(row, col)` on QWERTYUIOP, a 3-row keyboard, the validated VIC board,
and a 10×10 Polybius, 0-based and 1-based. Known X2SH two-digit values
`32,42,82,16` as digit pairs only — X and Y not invented.

Best-looking string is VIC 1-based `D?RODDP?AAOROA` (2 misses). No
dictionary words. First-or-zero does not turn it into a sentence. X2SH
pairs are four points (`X??Y` on 1-based Q3). **null-for-clean-words.**
X2SH remains carried data, not a closed null.

### What this does not close

ASCII 127 as a hint; yinyang as some other pair protocol; Cosmic Duality;
SalPhaseIon `dbbi`/`faed`; creator-message wording diffs (Priority 4, not
run). Next envelope is still the nested twin.

## Addendum 35 — Terminal envelope only (main line)

**Date.** 9 Sep 2026. Script: `analysis/term_mainline.py`. Log:
`analysis/out/term_mainline.txt`.

SalPhaseIon is a side door (Add.2). Cosmic is the document after a twin.
This pass loads **only** salt `b45a5e3d827593ca` (96 raw, 80 B ciphertext,
5 blocks). KDF is EVP SHA-256. No MD5, no shabef, no Salph literals.

Materials (56 unique), all from the chain that ends at this blob:

- letters-only Architect **1539**: `PRIVATEKEY` at 479, 34 word-windows
  through 160 letters, and the 140-letter “hundred fourty” slice
- 3.2.1∥3.2.2: landing-32 concatenated with VIC 91, both orders
- last line of `phase3_2_plaintext.bin` before `U2FsdGVk` (the VIC hint
  sentence)
- prime-basics (`0` at prime offsets) on Architect letters and on VIC 91
- the “function of THE YOU … PRIME BASICS” block; `CIAO BELLA O` tail
- carried main-line openssl hex (phase 2+3+3.2; phase 1 hash + 3.2)
- genesis 140-char `0x…` string; X2SH token block with holes left open

**168 trials. 0 pad-16. null-for-Gate-A.**

The 1539 `PRIVATEKEY` family is now a null on the *terminal* envelope, not
only a null on the 1544 pair. The blob is still locked. Further decrypts
stay on this salt until it opens.

## Addendum 36 — Carried orphans and 479/163 as index

**Date.** 9 Sep 2026. Script: `analysis/term_carry.py`. Log:
`analysis/out/term_carry.txt`.

Solved main-line envelopes all fed OpenSSL a SHA-256 hex of concatenated
riddle output (or that hex itself). This pass keeps that KDF
(`password_forms`: raw / sha256-hex / sha256-raw) and applies it to the
three unconsumed Phase 1–2 objects, plus 479 and 163 as **indexes**.

Measured:

- X2SH with riddle values, holes left open:
  `X 2 32 -42 4 Y 0 82 -16 15` (H and B are the signed riddle answers)
- nest 2×2 cell-level bits (not module packing): **0100**, same in spiral
  order 192–195 and in CCW-from-(6,6)
- `#fefefe` still one cell at 0-based `(7,4)`, 5625 px
- Beaufort letter-CT length **1539**, same as Architect letters

Materials (24 unique, 72 EVP SHA-256 trials on salt `b45a5e3d827593ca`):

- X2SH spaced / comma / `#…#` / reversed (“worst gear”) / prime-0 insert /
  `0xFE` mask; X2SH concatenated with nest `0100`
- 32-byte windows at **479** and **163** into Architect letters, Beaufort
  CT, and `phase3_2_plaintext.bin`
- yinyang concat of those 479-windows (arch∥CT, arch∥p32, both orders)
- genesis 69-byte ASCII; 138-char reversed hex (no `0x`); forward hex

Digits 9 / 15 / 479 / 163 were not passwords. X and Y were not filled.

**0 pad-16. null-for-Gate-A.**

Carrying the orphans as OpenSSL material, and using 479=479 as a pair of
equal-length slices from two 1539-letter buffers, does not open the
terminal envelope. The blob is still locked.

## Addendum 37 — SalPhaseIon door hash is not the AES password

**Date.** 9 Sep 2026. Script: `analysis/salph_doorhash.py`. Log:
`analysis/out/salph_doorhash.txt`.

Hypothesis: `shabef` + `ourfirsthintisyourlastcommand` names the command
that reached the page, and the page is self-opening.

    SHA256(GSMGIO5BTCPUZZLECHALLENGE || Half address)
    = 89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32

That hex is the URL. It had been used as a secp scalar (`next_object.py`),
not as OpenSSL material. Phrase 6 (“in front of your eyes”) fits the
address bar.

Tested against salt `3ab585348552415d` only: door hex, raw 32-byte digest,
sha256 of each (EVP SHA-256 and shabef-ans-too), plus the caption||address
preimage. **22 trials. 0 pad-16.**

The blob is not keyed by its own URL. `f9719d6d…` (sha256 of the 32-byte
door digest) is a path solvers already GETted (Add.29 SPA shell); it is
also not the AES password.

## Addendum 38 — Named leftover tests (phrase 7, halves, primes, dbbi, PNG)

**Date.** 9 Sep 2026. Logs: `analysis/out/phrase7_and_halves.txt`,
`analysis/out/del_primes_pt.txt`, `analysis/out/dbbi_classical.txt`.

Door-hash vs SalPhaseIon was Addendum 37 (already null).

**Phrase 7 vs Cosmic Duality.** `verylaststepisatruegiveawaypromised` as
EVP SHA-256 (raw / sha256-hex / sha256-raw) against salt
`2d3f6fe06dc950e6`. Arrival: Gate D (`is_intel`) or pad-16. **3 trials.
0.** Phrase 7 is not the Cosmic password in the solved-stage KDF.

**SalPhaseIon half-split.** First 2 AES blocks with p1, last 3 with p2;
second IV from KDF or from the last block of the first half. Named pairs
include door-hex / sha256(door), HASHTHETEXT / door, thispassword /
lastwords, half / betterhalf, caption / address, phrase 6 / phrase 7.
**44 trials. 0 pad-16.**

**Deletion-at-primes on Phase 2 and 3.2 text.** Delete / replace-with-DEL
/ replace-with-NUL at 0-based and 1-based prime positions in phase-2
plaintext, 3.2 text before the nested blob, Architect, letters-only
Architect, VIC 91. Leftovers still contain THE/KEY/HALF because the
*source* is English with holes, not a new message. EVP SHA-256 of those
results against the terminal envelope: **66 trials. 0 pad-16.**

**dbbi/faed keyed classical suite.** Alphabet is a–i (no `o`). 412
decodes: mod-9 Vigenere / Beaufort / autokey / Nihilist, 3×3 Bifid
(periods 5, 9, keylen, ctlen), 3×3 Polybius, page codec a=1…i=9 → hex →
ASCII, 26-letter Beaufort (mismatch control). Keys = solved-stage
answers (causality, flower, THEMATRIXHASYOU, HASHTHETEXT, VIC, 1539
landing, phrases, fresco/heisenberg/giveit, …). **0 English-like
decodes. 0 Gate A.** This does not exhaust every classical cipher; it
exhausts the alphabet-honest keyed suite. dbbi/faed remain unread.

**2019–2020 original PNG.** Wayback CDX 2019-04-01…2020-11-11 for
`gsmg.io/puzzle`: one row, 2020-11-09, `text/html` `/Puzzle` (Vue SPA),
not an image. `gsmg.io/*` in 2019-04-20…2019-06-10 has the homepage and
assets, **no puzzle image**. `i.redd.it/09jszg03cf231.png` has no CDX
row in Apr–Jul 2019. Arctic Shift `bf7siz` (created 2019-04-20, edited
2019-06-05) now holds only `09jszg03cf231` as `image/png`. Pre-June-5
bytes are still missing. Stego-negative remains about the mirrored PNG
only.

## Addendum 39 — 24-marker selector vs 161, and 16 AES blocks

**Date.** 9 Sep 2026. Script: `analysis/marker24_phrases.py`. Log:
`analysis/out/marker24_phrases.txt`.

Hypothesis: the three leftover counts work at once — **24** is the
blue/yellow pattern (`F73D92`, URL LSB = poster colours, 15 blue / 9
yellow), **7** is the password material (phrase concat = 161), **16** is
AES blocks (nested 5 + Salph 5 + Cosmic remainder 6). The 6 is forced
once both 5-block twins are taken in full: 16 − 5 − 5 = 6. Head and tail
of Cosmic were both tried (first-or-zero on which end).

161 in binary is not used as a key. It is the length that lets the first
24 primes (2…89) index the concat with no wrap. Spiral marker positions
7…191 need wrap: 4 of 24 are ≥ 161.

Colour-split is new relative to Add.19's 5,040 round-robin intertwinings.
0-based and 1-based prime indices, spiral-mod-161, 15∥9 / 9∥15 /
interleave, repeating 24-bit mask (103 / 58 — not 102 / 59), deque zipper
(blue-left and yellow-left), and the 24-char window at `F73D92 % 161`.
An even/odd phrase zipper does **not** drain: remainder 17 bits of
`F73D92` have 13 ones, even-tape is 102.

Selected strings are gappy English, not a sentence (`p0` blue
`llwlmarssoecaew`, yellow `rulhgtwps`). The mod-161 windows land inside
phrase 6–7 (`enotseeingitverylaststep`) because any 24-char slice of the
concat is still that English.

EVP SHA-256, three real envelopes plus 12 fake 16-block OpenSSL wrappers
(order TSC/STC × Cosmic head/tail × each of the three salts). Digits
9/15/479 not passwords.

**35 unique materials, 15 targets, 1,575 trials. 0 pad-16. 0 Gate D.**

The 16-block reading is a null for this password family, not a proof that
no other 16-block construction exists. 5+5+6 is still the only partition
of 16 that spends both twins whole. It does not open under the 24-marker
selector.





