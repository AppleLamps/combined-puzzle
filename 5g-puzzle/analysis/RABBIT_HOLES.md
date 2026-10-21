# Community rabbit holes

Lines of work the GSMG solver community pursued that were, on measurement, dead —
with what killed each one. Mention counts are `grep -ci` over the 51,177-message
Telegram export, as a rough proxy for how much attention each consumed.

A note on what is **not** here. A branch that was genuinely explored and exhausted
is not a rabbit hole; neither is an anomaly that is real but unexplained. Those are
listed separately at the end so this document cannot be used to dismiss them.

---

## 1. `btcseed` and the "one in eight billion" Bifid result — 110 + 61 mentions

The strongest and longest-lived. A Bifid decode of a puzzle string produces
`btcseed` in its opening characters, and the chat circulated the odds of that as
**"1 in 8,031,810,176"**.

**Measured:** of the 40,320 orderings of the same key letters, **480 put `seed` in
the first eight characters — 1.19%.** The quoted figure is off by roughly eight
orders of magnitude. It treats a search over orderings as if it were a single
prespecified draw.

The companion claim, a "96-state object" emerging from the same pipeline,
**reproduces with nonsense keys such as `abcdefghi`.** It is an artifact of running
Bifid at period = ciphertext length, not a property of the data.

`verify_btcseed.py`. Note the prior corpus had already measured this independently
and more carefully than I first did; credit is theirs.

## 2. The truncated SalPhaseIon blob — a structural trap, 557 mentions

The SalPhaseIon page uses `z` as a field separator **and** the embedded base64
legitimately ends its first half in a `z`. Strip it as a separator and you get
**127 base64 characters → 4.94 AES blocks**, which cannot decrypt under any
password, ever.

The truncated form circulates. Anyone who inherited it spent their time on a blob
that is mathematically undecryptable. This is not a wrong theory, it is a corrupted
input — the most expensive kind, because no amount of correct reasoning downstream
can recover.

## 3. The circulating poster cell-dump — the same failure, upstream

The transcribed 14×14 grid that circulates has **three wrong cells and no red at
all**, though the poster page image carries a 15px `#ed1c24` bar. Work built on the
transcription rather than the image inherits the errors.

Both published poster images are in fact identical where they overlap: sampling
both grids at cell centres, **0 of 196 cells differ.**

## 4. "Cosmic Duality is fourteen blobs" — 466 mentions

A 2025 message asserts the Cosmic Duality ciphertext is fourteen separate blobs. It
is **one 83-block blob**, 1,328 ciphertext bytes, verifiable by extracting it from
the archived page.

## 5. The "master XOR key" — 164 mentions of XOR

A published key claimed to unlock the remaining ciphertexts. **It fails on all
three.** Reproducible in a few lines.

## 6. `{1},{4},{21}` — an April Fools' joke taken as a coordinate

Posted 2021-04-01 06:57 UTC as `Hint: "another door might be found on {1 },{4} ,{21}"`.

The same thread disposes of it: at 08:06 a participant parodies it with
`{30},{2},{77}`; at 08:15 another asks "April fool's? 😄"; at 08:34 the creator
replies **"Good one V ;-)"** — to the parody; and at 13:29 he posts
`R=18 / A=1 / B=2 … Could also be 21 or 1812 bit 🧐`, which is RAB + BIT =
**RABBIT**. On 2021-04-18 he asked, unprompted, *"Do you know what usually happens
on the first of april?"*

**Still live in the corpus:** `SALPHASEION_PREREGISTRATION.md:405` builds "a 21-row
layout corresponding to `{1},{4},{21}`" on that line.

## 7. `hopeisthequintessentialhumandelusion` as a URL path

Posted 2020-04-08 20:33, followed **eleven seconds later** by the creator writing
**"(not a hint btw, just fooling around)"**. Four spelling variants of it appear in
the Wayback CDX index as attempted gsmg.io paths; all return the 404 shell.

## 8. Typos as encoded clues

2020-02-22 16:11, the creator: *"Typos: Horrible mistakes due to rushed work… **No
clues to be found in those typos** might you wonder 😉."* Restated 2020-04-08:
*"errors and typos are mostly not intended."*

The one exception is documented and was handed over outright: `giveit` → `givetit`,
a real bug he apologised for.

## 9. "The last number of pi" — 104 mentions of pi

2024-11-29 11:06: *"You only need the last number of pi and it might get you
somewhere."* Pi has no last digit. This is a joke about the puzzle being
unsolvable, delivered in a long run of banter about supplements and grey hair.

## 10. On-chain OP_RETURNs read as creator messages

**105 OP_RETURN outputs** touch the two prize addresses. **Every single one is
inbound, written by solvers.** Neither puzzle key has ever published a byte on
chain.

The payloads are solvers guessing at each other — `hereismysecret`, `#SOLUTION`,
`isolveditwithanabacus`, `yourlastcommand`,
`matrixsumlistenterlastwordsbeforearchichoicethispassword`. Anyone mining the chain
for creator hints finds this and mistakes a mirror for a window.

The same applies to the GSMG-styled vanity addresses appearing in inbound
transactions (`1GSMG1ABC95GES…`, `1GSMG1CLxGXuFtn…`): those were ground by solvers
imitating the creator, not by the creator.

## 11. Reading the halving transactions for payload

The 2020 and 2024 splits are real, designed and announced — but they carry **no
bits**. Four outputs total, all to the puzzle's own two addresses, exactly round
values, standard P2PKH, ordinary fees. The `nLockTime` values 629998 and 840003 are
**Bitcoin Core anti-fee-sniping artifacts** recording when he broadcast, not chosen
digits. Do not read the numbers.

## 12. Method traps, which cost more than any single theory

These are not theories but habits, and they generated most of the wasted effort on
both sides — including mine.

**Printability as a success test.** A decrypt was judged by whether it looked like
text. Two 32-byte private keys are **0% printable**, and the real Phase 3.2
plaintext is only ~60% printable because it contains a binary block. This filter
throws away the answer. *I used it for eight addenda before catching it, then leaned
on it again one addendum after correcting it.*

**PKCS#7 pad 1 as evidence.** A wrong key produces random bytes; if the last one
happens to be `0x01` that is *valid* padding. It occurs for **1 wrong key in 256**
and is therefore **uninformative** — evidence neither for nor against. Both
directions of this error appear in the record: treating pad 1 as success, and
treating it as disproof.

**Restatement mistaken for discovery.** "All 24 coloured modules lie on
`(col − row) mod 4 == 1`" is true and is the *same fact* as "the markers sit at
every 8th spiral cell", in different coordinates. Every cell at those positions has
that residue regardless of colour.

**Uncontrolled comparison.** My own worst error: I found `sha256(cosmic_plaintext.bin)`
is a real gsmg.io path, verified the hash match exactly, and wrote it up as a live
second door. The 1,253-byte capture I compared against ~12,200-byte 404s was
**post-site-change**; the site now serves a 9-byte placeholder. Three of the small
captures I implicitly grouped with it are lodash source fragments a scanner
submitted as URLs. Verifying a component says nothing about the inference built on
it.

**Brute force applied to a missing rule.** Repeatedly, the group enlarged password
spaces when what was missing was an instruction, not entropy. Roughly 5.9M
passphrases plus ~1.31M gated decrypts across this session alone, all null.

---

## Not rabbit holes — do not use this document to dismiss these

| | status |
| --- | --- |
| **The `#fefefe` cell** (179 mentions) | A genuine, deliberate anomaly: one cell of 196 is `#FEFEFE`, all 625 pixels, in an RGBA image with no palette. Known since 2020, still unexplained. Cell (7,4), spiral index 163 (prime), byte 20 bit 3 — the `n` of "planted". |
| **`cosmic_plaintext.bin`** (466 mentions) | **Unresolved.** I called it a padding collision (Addendum 3), then retracted that on bad evidence (29), then retracted the retraction (30). Pad 1 is uninformative and high entropy is consistent with key material. Neither proven nor disproven. |
| **The `dbbi` / `faed` streams** (1,081 + 650 mentions) | A real side branch of the puzzle, heavily worked. Expensive, but not false. |
| **The rebus pixel offsets** | The 2019 "images are off by a few pixels" question is real — and resolves to layout: black and blue pad right, red pads left, without exception. Answered, not a hole. |
| **`yinyang`** (555 mentions) | The creator's own named next phase. Unreached, not disproven. |
| **Prime numbers** (2,284 mentions) | Creator-confirmed as required. The 479 balance verifies exactly. |

---

## The pattern

Nine of the twelve entries above share one shape: **a number or a string that looks
too specific to be chance, adopted without the base rate being computed.** `btcseed`
needed one line of arithmetic. Pad 1 needed the observation that 1/256 is common.
The `{1},{4},{21}` "coordinate" needed reading forty more minutes of the same
thread.

The cheapest defence is not more cryptanalysis. It is asking, before building:
*how often would this happen anyway?*
