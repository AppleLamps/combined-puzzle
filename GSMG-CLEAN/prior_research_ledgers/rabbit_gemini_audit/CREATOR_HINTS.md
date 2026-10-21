# GSMG.IO 5 BTC puzzle — every creator hint, in order

Everything the puzzle's creator (`Jrk Bgrt`, handle @SoWut, `user9815232`) said
that bears on solving, in chronological order.

## Provenance

Re-extracted 2026-09-09 from the full JSON export (`D:\newest-puzzle-9.9.26`,
61,418 messages, 2019-04-20 → 2026-09-09): **492 messages authored by the
creator**, all under the single account `Jrk Bgrt` (no other name variants; he
also solemnly denies running other accounts, #5672, 2021-01-18). This supersedes
the earlier extraction (411 messages, export ending 2026-05-28).

All times are **UTC**, converted from the export's UTC−05:00. The export renders
local time, so any list quoting these in local time will be five hours off.

Caveats to carry:

- **The creator retroactively edited 244 of his 492 messages** (49.6% overall;
  35.4% of the 2019–2022 set, against a 3.7% baseline for other participants),
  concentrated on the hint-bearing posts. A message's current text is not
  necessarily its text as posted.
- During 2026-09-09 re-verification every previously "second-hand" 2026
  statement was located in this export and is now first-hand below. The only
  pairing that remains **unattributable** is the claimed "salphaseion is 100%
  solvable? → Yes": the "Yes" (#66588, 2026-07-12) carries no reply target and
  its question cannot be recovered from threading.
- Several one-word AMA answers ("Yes"/"Nope", 2026-07-12 20:56–21:01) have no
  recoverable question. They are listed where their flow context makes the
  referent clear, marked as such.

Hints are graded:

| | |
| --- | --- |
| **[M]** | **Mechanical** — names an operation, object or constraint you can act on |
| **[S]** | Status or scope — tells you where you are, not what to do |
| **[X]** | Explicitly not a hint, or a joke |

---

## 2019 — construction and one confessed bug

**2019-04-20 16:21 [S]** — "The first part. Maybe the puzzle has multiple stages 😉."

**2019-04-20 18:18 [S]** — "Ok.. somebody has cracked the first code." / "that
was way faster than expected." (#74/75)

**2019-04-22 19:48 [M]** — posts a bare hash so solvers can test passwords offline
rather than against the rate-limited site:
`5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75`
("just try hit your options against that hash", #226). The stated reason for
providing it: "A hash which we provided as the website was giving a lot of token
errors" (#257, edited later). The hash is SHA-256 of the phase-1 answer.

**2019-05-08 [S]** — "Apparently somebody managed to get into Phase 3 🧐" (#660).
Phase 3 reached within three weeks of launch.

**2019-05-14 15:01 [S]** — "I suppose the btc price will be above 10k at the next
halving." First mention of the halving, eleven months before the split.

**2019-05-17 22:39 [M]** — the typo confession:
> "there might be a mistake in phase III and that is correct unfortunately. The
> mistake makes it nearly impossible to solve unless you'd know where to add **1
> extra character between the 3 answers**."

**2019-05-17 22:43 [M]** — the fix, given outright: **`giveit = givetit`**

**2019-05-18 02:30 [M]** — "The issue is within the 3th phase. Not in going from 2
to 3. Once you have to work with give(t)it you'll know."

**2019-05-18 13:13 [S]** — "No hints after stage 2 (except the 't' to fix my stupid
mistake)". Same day, #887: "Part III consist out of a few stages. The last few
stages are, how shall I say it, not really easy to solve for most."

**2019-05-31 [S]** — "Apparently folks found a new piece." (#991) — the
out-of-puzzle piece (Decentraland) surfacing in month five.

**2019-09-22 19:00 [M]** — asked whether something "is long": **"7 parts right?"**
(#1465). His only in-chat confirmation of the seven-part structure that phase 3
consumes (and that "SEVEN INTERTWINED PASSWORDS" later back-references).

**2019-12-31 10:30 [S]** — the promised hint is coming "at the start of 2020 indeed,
**way before the halving**."

---

## 2020 — the door, and the halving mechanism

**2020-01-04 [S/X]** — "Note: I might be in a trolling mood." (#1659, edited) —
posted ten days before the Roses hint; a standing caveat for everything in
January 2020.

**2020-01-13 16:40 [S]** — "Hint to be expected within a few days. Note: not
trolling with scripted cake this time."

### 2020-01-14 10:38:06 [M] — the central hint

> Roses are White but often Red.
> Yellow has a number and so does Blue.
> Go back to the first puzzle piece without further ado.
>
> It might have shown you only one door, beware that the rabbits nest may contain
> a whole lot more.
>
> Hush hush.

This is the **only** message that says go back to the first puzzle piece.
Everything else about doors refers to it.

**2020-01-27 10:21 [M]** — asked "besides the givetit mistake, are there any other
confirmed spelling/grammatical errors in phase 3.2?": **"Might have been fixed fyi
👆"** (#1726). **Tested against Wayback (FINDINGS Addendum 33): no fix was ever
deployed.** The typo sits inside phase 3's encrypted plaintext; the ciphertext is
byte-identical in every capture (2020-11 → 2026-04), still decrypts with the
givetit chain, and the 2019 password hash would have broken under any patch. The
fix he meant was the *hint* itself.

**2020-02-22 16:11 [X]** — "Typos: Horrible mistakes due to rushed work… **No clues
to be found in those typos** might you wonder 😉."

**2020-02-25 18:09–18:15 [S]** — "Or nobody found the direction" / "I'd dive in the
puzzle **from the beginning** before making assumptions" / "**3.2 is a thing btw**"
/ "most see 3.2 as the last part." Also: "A few guys here cracked phase 2 in 2
days" (#2024).

**2020-03-24 [M]** — of the phase-1 image: **"There must at least be something
hidden in there."** (#2918, in reply to a solver analysing the picture). Refused
the follow-up: "Answering that would be too much of a hint" (#2910).

**2020-04-08 18:38 [S]** — "Those hints are the last hints. Although I can say that
one team managed to find something… something others haven't yet found."

**2020-04-08 20:33 [X]** — "Hope, it is the quintessential human delusion…"
immediately followed by "**(not a hint btw, just fooling around)**". Solvers later
submitted this as a URL path anyway; it 404s.

**2020-05-11 19:31 [M]** — 8 minutes after the halving split landed:
> "It'll high likely be worth more than it once the price was 5 btc. **Next halving
> in 209999**"

630000 + 210000 = **840000**, which is exactly where the 2024 split happened.

**2020-05-11 20:31 [M] (#3923, edited 2024-12-23)** — "Let's see what bitcoin is worth the next halving and who knows what you'll find after **opening the 2nd door**. The price is in half, but what does it mean 🤔."

### 2020-05-20–21 [M] — "answer is there" / "First or zero" — the full exchange

A solver reasons aloud (#4101): *"first piece is a zero piece? hard to count all
steps. in usual talking first mean first, but in puzzle first is a 'crypto logic',
and rabbit is a zero step. so strange to understand a 'the first piece' of."*

> **#4102 (2020-05-20 22:40): "answer is there"**

Detective Froz then asks (#4104): "Do you mean the answer to another door from the
1st piece?"

> **#4105 (2020-05-21, edited): "First or zero"**

Read together: he *endorses the solver's framing* — the rabbit is a "zero step"
and "first" is crypto-logic — and answers the door question with the same
disjunction. The doc previously carried #4105 alone; the endorsement of "rabbit =
zero step" in #4102 is the more informative half.

**2020-08-02 16:56 [S]** — "Really **nobody managed to find the extra door**, didn't
expect that after the earlier pace of cracking things." (Same day, #4589, on
whether the next thing is a new puzzle: "Or the same puzzle, or just not at all 🤷‍♀.")

**2020-08-12 [M]** — after a solver observes that everyone spent a year on the
binary path "and nobody see another route at the moment":
> **"Indeed remarkable with the hints stating the path pretty obvious..."** (#4688)

He then declines to confirm or deny hints hidden in the blockchain (#4689 — no
creator answer follows). Same day, #4694: "There's 1 club that passed but they are
stuck in the next phase."

**2020-10-01 [S]** — "I've just been notified that number 2 has made it to the next
stage." (#4771)

**2020-10-27 [S]** — the prize link, with "price is indeed still there" (#4912).

**2020-11-24 18:02 [M]** — "We have our reasons **halving the price money at every
bitcoin halving event** :-)." / "Who knows, maybe even in the same block."

---

## 2021 — primes, zeroing, and one joke that cost years

**2021-01-07 19:57 [S]** — "It'll be split on the next halving. We mentioned this at
the beginning, when the puzzle started."

**2021-01-18 [S]** — "I can solemnly promise you I'm not using any other accounts
besides my own." (#5672) — the creator is not an anonymous participant.

**2021-01-21 11:35 [M]** — "Not to give any hints but **a few might not require the
internet anymore**."

**2021-03-01 11:34 [M]** — "You are at **the prime part** already??? … Oh wait,
shouldn't have said that. That might have been a hint 🤔." Later the same day, on
the archaic spelling of FOURTY (#5960): **"Ancient spelling 😅. One of the many
many typos."**

**2021-03-05 [S]** — reached SalPhaseIon (#6243/#6491). On how he tracks progress
(#6497): "I don't check the website logs. There aren't any tracking scripts
either… I just read the chat and when I notice the address is empty I'll know."
#6509: "I gave an unforseen hint already 🤷‍♂" (the prime-part slip). #6541
(2021-03-19): "I know about 3 people/teams." #6712 (2021-03-22): "Nr 5 in salph."

### 2021-04-01 02:57 [X] (#6884, edited 2025-02-02) — an April Fools' joke, not a hint

> Hint: "another door might be found on {1 },{4} ,{21}"

The same thread settles it: at 08:06 a participant parodies it with
`Private key might be found on {30 },{2} ,{77}`; at 08:15 another asks "April
fool's? 😄"; at 08:34 the creator replies **"Good one V ;-)"** — to the parody; and
at 13:29 he posts `R=18 / A=1 / B=2 … Could also be 21 or 1812 bit 🧐`, which is
RAB + BIT = **RABBIT**. A participant completed it openly twenty minutes later.
On 2021-04-18 he asked, unprompted: *"Do you know what usually happens on the first
of april?"*

**This still matters:** `SALPHASEION_PREREGISTRATION.md:405` builds a "21-row
layout corresponding to `{1},{4},{21}`" on that line.

**2021-04-01 14:06 [S]** — a bare 👆 endorsing "Probably best to start at the
beginning to understand the mindset behind it".

**2021-04-03 [S]** — "I've been pretending to be one of the few creators for a while
now." (#7061) — first in-chat acknowledgement of a build team.

**2021-08-11 11:07 [S]** — "And the solver will find a way to 'decrypt' it."
Immediately before, #7832: asked whether the prize is "the one to be found by
solving the puzzle": **"The one to be found by solving the puzzle yes."**

**2021-12-03 03:41 [M]** — "There is / Another / D / O / O / R"
(then: *"Remind me when it's Christmas."*)

### 2021-12-26 20:18 [M] — the Christmas hint, opened with "A mini mini hint. Ready 🐰?"

> The previous "there is another door hint" is still a thing. We're not sure if
> anyone has found another door so far, and we can't check that... We've seen
> **prime numbers** being mentioned; well, that is definitely an aspect which is
> required to proceed. Furthermore, along the way, **some characters need to be
> 'zeroed out'**.

**2021-12-31 17:14 [M]** — "The only date I give away is the **expiry date of neo's
passport**." (`11-09-2001`)

---

## 2022 — quiet, but three real ones

**2022-12-02 [S]** — "It is meant to be solved." (#8301) / **"There might be a hint
coming but not too soon."** (#8307) / on how long the "theory" would take to
discover: "I'm not exactly sure how long it would take to discover that theory so
I can't really tell 🤔" (#8309 — the theory-of-everything path, pre-announced six
weeks before he named it).

**2022-12-11 15:30 [M]** — replying to a photo of the Time-Life *Cosmic Duality*
book cover: "…. **That is very specific**" / "If the puzzle is solved you'll see how
**scary specific** that is 😂"

---

## 2023 — Cosmic Duality, the seven phrases, and yinyang

**2023-01-09 04:52 [M]** — "@barrystyle, **provided a very specific hint already**."

**2023-01-09 10:10 [M]** — "At least **prime number is very important** to get any
further."

**2023-01-11 [S]** — "Rumour has it **a new hint is to be expected within 2 months**
from now." (#8342 — delivered 2023-02-23.)

**2023-01-12 11:09 [M]** — "Focussing on the **theory of everything** is also still
a valid path to reaching the private key."

**2023-01-12 16:05 [M]** — "**Every btc halving the price will half too.**"

**2023-01-12 [S]** — "I checked a certain GitHub yesterday, for whoever set that
up, nicely done. **You guys are really getting close.**" (#8352) And, in the same
session (#8360): "I'm aware it might appear unsolvable, **but it's not**. If you
find the answer now, the remaining 2.5 btc is well deserved... **Or 5, who
knows**." — the only statement hinting the full prize could re-consolidate.

### 2023-02-23 23:20 [M] — the seven phrases, posted as binary

He posted 1,288 bits directly in chat. **Decoded here from that message, not quoted
from a summary.** The encoding is two reversals: each byte is bit-reversed
(LSB-first), then the whole resulting string is reversed.

```
yellowblueprimes
matrixsumlist
lastwordsbeforearchichoice
yinyang
wewontgiveawaythepassword
itsinfrontofyoureyesbutyourenotseeingit
verylaststepisatruegiveawaypromised
```

**The order is creator-stated.** What each phrase operates on is not.

### 2023-06-10 [M] — three questions answered directly (#8569)

PoW puts three statements to him in one message: (1) *"phase 3.2 is not totally
solved, as the final block hasn't been decrypted"* (the terminal envelope,
quoted); (2) *"Maybe there [is] the hint for SalPhas[e]Ion everybody was asking
for"*; (3) *"in phase 2 the 'Norton's theorem' seems totally pointless in context
[and] X 2 S H 4 Y 0 Q B 15 doesn't seem usefull as well to go to phase 3."*

His answer, verbatim, three lines:

> **Correct.**
> **No.**
> **Can't say anything about this.**

So: **the terminal envelope is creator-confirmed unsolved**; it does **not**
contain the SalPhaseIon hint; and he declines to rule on Norton/X2SH. (Note the
tension with the dated 2021-02-12 "#…# wasn't used" screenshot in the reference
corpus — one of the two must be looser than it reads.)

**2023-04-14 17:41 [S]** — "It can be solved, albeit very difficult as **you have
to understand how to interpret all the hints**."

**2023-05-02 19:12 [M]** — "Still remarkable that scene. Especially the **expiration
date of his passport** 😁."

**2023-08-03 19:51 [S]** — "**Are you really looking for just the btc…?**" —
introduced by "Ok ok ok ok. **I can't hold this one any longer**" (#8773) and
followed by "Might be. **Wish I had said nothing though**" (#8787) and "**I saw
that you guys got really really far already**" (#8795).

**2023-08-03 20:34 [S]** — "Actually, **the hardest part is done**."

**2023-08-05 00:46 [M]** — what GSMG stands for: **"Globally supporting my
generation"**

**2023-08-06 12:09 [M]** — "Technically my friends and family can get to all my data
if they'd work together. In that scenario, **don't expect a halving of the price**."

### 2023-08-06 12:12 [M] — "Probably the last hint"

> Once you hit a **"ying yang"**, you'll be able to solve it the same day.

The safety-context messages around it, same session: "if I suddenly can't answer
you guys anymore, it was nice knowing you all ❤️" (#9550), "**be careful of what
you get yourselves into 🤐**" (#9551), "**The puzzle talks for me**" (#9554), and
"**Something was solved rather... remarkable**" (#9627).

**2023-08-06 12:19 [M]** — "**No need. You have all the info.**"

**2023-08-06 12:43 [S]** — "from here on, high likely no hints anymore… I hope not
to have to give another hint as **it would probably be a give away**." Expanded at
#9621: if unsolved "in the next few years… then I might feel the need to give an
additional hint, as I couldn't happily live with the idea that some would think
that this w[as never solvable]".

**2023-08-06 18:39 [M]** — "Correct. Well, technically, **you'll need the internet to
claim the prize** in the end 🤔."

### 2023-11-24 14:05 [M] — the offline confirmation

> There's a question multiple people have asked me. "Given the available knowledge,
> is internet still required to solve it?"
>
> **Nope**

---

## 2024 — dwindling, but two real ones

**2024-01-26 17:21 [M]** — asked what the prize key is: "**Regular Bitcoin Private
key**."

**2024-03-26 17:05 [M]** — "I prefer **superpositions** 😉."

**2024-03-26/27 [S]** — moderation-and-policy drop-in: "**I decided not to answer
any puzzle questions anymore. If there will be a hint (ever). It will be here.**"
(#23120). Asked what the phase-0 picture looks like: **"Sqaures and a rabbit?"**
(#23200) — his only in-chat description of the first puzzle piece.

**2024-04-20 00:15 [S]** — at the 2024 halving:
> "There are few prizes to win besides the banter in this chat. A private key, some
> **'obscure' intel**, or what I hope most of you have discovered by now, the most
> obvious reason to make sure you hold on to Bitcoin 😉." — and "see you in 4
> years!" (#24638).

**2024-09-19 07:20 [S]** — on Jacque Fresco: "I simply liked Jacque's ideas a lot. I
have techy friends building communities around that idea today."

**2024-11-29 09:59 [S]** — "**If wallet != empty, puzzle not solved.** (Most
likely)."

**2024-11-29 10:28 [S]** — "At this point, I don't know what to hint, without ruining
it… **If you guys got 1 microstep further, the puzzle will likely be solved the same
day.**"

**2024-11-29 10:47 [M]** — "I think I'll be going for **ASCII 127** myself. But not
overly dramatic."

**2024-11-29 11:06 [X]** — "You only need **the last number of pi** and it might get
you somewhere." (Pi has no last digit; this is a joke.) Same session: "if you guys
don't solve it anytime soon I'll have to try and **stay alive till the year 2145**"
(#32719), and — asked about the site's frontend — "it has been years and **we had a
few FE guys working on it**" (#32701; second acknowledgement of the build team).

---

## 2025–2026 — yinyang as the gate, and the drunken AMA (now first-hand)

### 2025-04-28 16:57 [M]

> Did anyone found **yingyang**? I don't think so, you guys are so smart, **when
> yingyang is reached, 2 hours max.**

**2025-04-28 17:01 [M]** — asked whether it comes after decrypting an AES ciphertext:
> "**It's the next phase**, but I await the day someone finally gets there."

**2025-04-28 17:02 [S]** — "Ok, the **'better half'** is hungry. Which means I'm off 🤗"

**2025-04-28 [S]** — "If I'd ever take the funds (**I won't**), I wouldn't even tell
the answer 😈" (#39219). Also #39208: "if you **understand the puzzle** you'll
discover that I'd suggest btc only, and don't gamble."

**2025-09-15 [X/lore]** — "Carrots were originally **purple, until the Dutch turned
them orange** in the 1600s to kiss up to their royal family." (#49176 — he is
Dutch; purple/orange/carrot/rabbit asides recur.)

**2026-01-01 03:20 [X]** — 616 bits of plain MSB-first ASCII:
> "Happy new year! Make the best of everything. Oh, and here's a "tiny hint" <3."
>
> The "tiny hint" is the message itself being trivially decodable — no payload.

**2026-03-04 01:17 [S]** — "**No hints, only free will.**"

**2026-03-04 01:19 [S]** — "**Jacque was quite an inspiring lad** I'd say."

**2026-03-04 01:30 [M]** — "**I only need to look at the address.** If any of you
reaches the next phase, the price is taken in no-time."

**2026-03-04 01:35 [M]** — "I'm going to rewatch **episode 3.5** with the **better
half**."

### 2026-07-12 — the drinking-night AMA (all first-hand; reply-context verified)

**20:17 [#66540, edited]** — "what if one day, some of you finally finds it... and
doesn't explain it publicly, while I've already passed away. How do I have to turn
myself around in my grave 🤔..."

**20:21 [#66542, edited]** — "In 2029, all btc on old addresses might be cracked
(cmiiw)." / "A nation state will at some point hack the currently lost coins, and
then keep OR sell it." (#66596)

**20:30–20:47 [M]** — on the puzzle's origin (#66559): "the **rickroll effect**
inspired me to make an actual puzzle, just to see if I could. It wasn't a PR stunt
until I realized it after I published it. **The others didnt fully understand/agree**"
(third team acknowledgement). On his method (#66561): "I get into a frenzy and zone
in with 800%. A day later I can hardly understand what I have done 🫤."

**20:47 [#66568, edited] [M]** — "Most of you know the puzzle WAAAY better than me
at this point. **I have a hidden laptop which I haven't touched in years. On that
thing... is the actual answer....**"

**20:49–20:52 [#66571/66573/66574] [M]** — "Some of you, can find me. Quite a few in
this chat, already met me." / "My close friends have the best chance of solving it
(a few tried). But **they don't have the skills some of you do**." / — 22 seconds
later — "**NOTE: that is a hint.**" The only message in seven years he labelled as
a hint.

**20:52–21:01** — bare answers whose questions are not recoverable from threading:
"Nope." (#66586), "Yes." (#66588). **Do not attribute these to specific questions.**

**20:55 [#66584, edited] [S]** — "I feel it a bit off knowing **the url (and thus
the original puzzle) is 'gone'**."

**21:03 [#66589, edited] [M]** — "And IIFF I'm somehow still wrong, which I'm most
likely not as I've verified many times back then after some sad rushed mistakes,
**it's all still solvable with a few stable qubits**." — the endgame is
ECDLP-shaped; the final answer is a private key.

**21:10–21:11 [#66592/66593/66595, edited] [M]** — "I held quite a secret in my head
which I seriously wanted to share with the planet" / "**The '5' btc was never the
actual prize. That was only a tiny fraction.**" / "(And yes, **the btc is still
available** before you fire any questions)."

**21:17 [#66600, edited] [M]** — replying to "nobody knows how to solve and much
less about this": **"Some already found it. And understood not to risk it... 🤐"**

### 2026-07-16 — the second night (context verified; three earlier readings deflate)

**18:19 [#66903, edited] [S]** — "Well, **it's hidden in a room with a hidden
door.**" — a direct reply to a member joking about spending the night looking for
his laptop: it describes the **laptop's room**, not a puzzle room.

**18:26 [#66909/66910]** — the BIP-360 ELI5 he asked AI for. "**ELI4.5 is meta**"
(#66913); "You have to be **in your prime** for that" (#66931, reply-context:
fractions).

**18:48–18:52 [#66962, edited] [S→downgraded]** — "Latetly, I'm working with many
**NOTES**." — a reply to a member "Waiting for the 'NOTE: that is a hint.' moment";
self-reference to his own hint-posts, **not a cipher lead**.

**18:50 [#66961, edited] [S — restored 2026-09-09]** — "Give yourself yourself
and yourself will be given yourself." — sits inside the psychedelic stretch,
but is a near-quote of the 3.2.1 plaintext's deliberate doubling ("…THE
EXTINCTION OF THE ENTIRENESS OF YOURSELF**SELF**…" — the film says it once).
Part of the recurring doubling signature: "YOU YOU" in the same speech, the
double space (0x20 0x20) in the 2026 "episode 3.5 with  the better half"
message, the twins, 479=479. Read as callback, not random philosophy.

### 2026-09-01 — the anniversary drop (new in this export)

**07:49 [#70307, edited]** — "Pfff. **Coincidence.**" (to an AI-hallucination joke.)

**08:01 [#70311, edited] [S]** — asked how he could afford it: "A. **I rushed
(t)it.** B. Yes, have quite some time for stupid stuff." The `(t)` is his own
callback to givetit.

**08:40 [#70336] [S]** — asked how long the puzzle took to create and whether he
worked alone: **"Couple hours, and no."** — *not alone*. Matches "one of the few
creators" (#7061, 2021), "a few FE guys" (#32701, 2024), "the others didn't fully
understand/agree" (#66559, 2026), and — loosely — "done before dawn" (#8038, 2021,
posted drunk; #70377 "Same same" equates the two claims).

**11:41 [#70377, edited]** — "Same same." (his last message in the export)

---

## The mechanical hints, condensed

Everything in tier **[M]** that names an operation or object, with what it is known
to have resolved to:

| hint | resolves to | status |
| --- | --- | --- |
| `giveit = givetit` | the phase 3 typo; live-patched on site ~2020-01 (#1726) | consumed |
| a piece outside the main puzzle | Decentraland parcel (−41, −17) | consumed |
| Yellow has a number and so does Blue | 24 markers on the first 24 primes → 479 | consumed |
| Go back to the first puzzle piece | the poster | **open** |
| the rabbit's nest contains more | a second door in the poster | **open, unfound since 2020** |
| Roses are White but often Red | the poster's colour pairing | **open** |
| "answer is there" → rabbit is a zero step (#4102) | endorses "first vs zero" framing of the rabbit grid | **open** |
| "First or zero" (#4105) | indexing instruction for the second door | **open** |
| the hints state the path "pretty obvious" (#4688) | the door hints point a direction nobody took | **open** |
| prime numbers are required | 479, and the `#fefefe` cell at prime spiral index 163 | partly consumed |
| some characters need to be 'zeroed out' | unidentified | **open** |
| expiry date of Neo's passport | `11-09-2001` | consumed |
| "7 parts right?" (#1465) | the seven-part phase-3 password | consumed |
| the seven phrases, in order | 5 of 7 have an object; **5 and 7 have none** | **open** |
| 3.2 final block undecrypted = "Correct" (#8569) | creator-confirmed open target; not the SalPhaseIon hint | **confirmed open** |
| `yinyang` | "the next phase", reached via a decryption, then 2 hours | **open — the gate** |
| Cosmic Duality is "scary specific" | the Time-Life book cover | **open** |
| no internet required | the answer is inside the puzzle | constraint |
| ASCII 127 | unidentified | **open** |
| superpositions | unidentified | **open** |
| hidden laptop / close friends / "find me" (#66568–74) | personal, low-skill-accessible — his only labelled hint | **open** |
| "solvable with a few stable qubits" (#66589) | endgame is a private key (ECDLP) | constraint |
| "the '5' btc was never the actual prize" (#66593) | unidentified larger prize | **open** |
| "some already found it… not to risk it" (#66600) | the door, found by some, undisclosed | **open** |

## Team and authorship (for the profile)

| date | statement |
| --- | --- |
| 2021-04-03 | "one of the few creators" (#7061) |
| 2024-11-29 | "a few FE guys working on it" (#32701) |
| 2026-07-12 | "The others didnt fully understand/agree" (#66559) |
| 2026-09-01 | "Couple hours, and no [not alone]" (#70336) |

Full quotes with surrounding context for the door thread are in
`DOOR_HINTS.md` (the verified edition: every ID, date and edit-status checked
against the 2026-09-09 export; #1837 "Only -41,-17 matters" — 2020-02-22,
never edited — recovered there with full context). Reproduction and
measurement of everything above is in
`analysis/FINDINGS.md` (Addenda 1–39). The full 492-message creator extract is
`D:\newest-puzzle-9.9.26\creator_all.txt`.
