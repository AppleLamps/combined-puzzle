# Two dated creator claims, and what they bound (3 October 2026)

**6 October 2026 interpretation notice.** This is a dated research record.
Its candidate counts and original logs are preserved, not freshly rerun.
Read [doc 118](../118-correctness-audit-remediation.md) for detector/coverage
limits and [doc 119](../119-current-evidence-ledger.md) for current findings.
A null applies only to its complete tested tuple.

A small-step claim made before the public DBBI parse does not prove the intended next step is independent of that parse. Hint consumption and input/output order remain interpretations.

Source: `jrk_messages.txt` (492 creator messages with reply headers), read end to end; community
messages appear only where a reply header quotes them (first ~150 characters) or where the dossier
quotes them from the full export (dossier 8.1, 6.3). Nothing else about the community is visible, so
every statement about "what the community held" below is either a quoted header or an inference
marked as such.

## 1. The moment of #6509 (14 March 2021)

### Timeline, 1 January to 14 March 2021

| id | date | who | text | reading |
|---|---|---|---|---|
| #5717 | 01-21 | Jrk | "Not to give any hints but a few might not require the internet anymore." | someone was past the online steps |
| #5952 | 03-01 | Janusz (quoted in #5960) | "this is old talk, now is FORTY but hundred FOUR = 104 is the fefefe square fefefe is 101 010" | working on the Architect's "hundred fourty", the off-white cell, and `fefefe` read as bits (f=1, e=0 gives 101010) |
| #5958 | 03-01 | Janusz (dossier 8.1) | "AND OR logic gates" | combining bit strings |
| #5960 | 03-01 | Jrk, reply to #5952 | "Ancient spelling. One of the many many typos." | dismisses the **spelling** "fourty", not the 104 or the cell |
| #5963 | 03-01 | Janusz (dossier 8.1) | "just say which primes 2,3,5,7 we need use" | |
| #5966 | 03-01 | Jrk | "You are at the prime part already???" | 3 minutes after #5963 |
| #5969 | 03-01 | Jrk | "Oh wait, shouldn't have said that. That might have been a hint." | **self-declared accidental hint** |
| #6201 | 03-05 | Alex (quoted) | "Author just wasted a huge amount of time of people" | |
| #6250, #6252 | 03-05 | Jrk | "Infrared" / "No hints 🤡" | posted on purpose, disowned at once as a joke |
| #6491, #6495 | 03-14 | Jrk | another person or team "made it to salph"; "Nope" (not trolling) | |
| #6497 | 03-14 | Jrk, reply to #6496 | "...Breaking salphation, should be giving the feeling of the phase's name..." | deliberate, general |
| #6508 | 03-14 | anon (quoted) | "So don't you think it's time for a hint on matrixsumlist?" | |
| #6509 | 03-14 | Jrk, reply | "I gave an unforseen hint already" | |

### State of the community at #6509

- Main route solved to the end of phase 3.2 since 2019; the Terminal envelope pasted in chat by May 2020 (#3806).
- The SalPhaseIon page reached by at least four or five people or teams (#6491, #6541, #6543, #6712), by hashing the poster text (#7416, endorsed later).
- The `matrixsumlist` a/b run decoded: the asker names the label. The other labels and the segmentation were posted later (#7360, April 2021), so whether `lastwordsbeforearchichoice` and `thispassword` were decoded on this date is not visible.
- `yellowblueprimes` did not exist as a label (it comes from #8446, February 2023), and dbbi was unparsed (until #72215, September 2026).
- Open discussion: the poster's off-white `#FEFEFE` cell, bit readings of it, logic gates, and which primes to use.

### What "unforeseen hint" refers to

**Conclusion: #5966 "You are at the prime part already???".** It is the only creator message in the window that he himself called an accidental hint (#5969), and "unforseen" is his word for "not expected" (#879).
Rejected: "Infrared" (#6250) was intentional and disowned as a joke within 19 seconds; #6497 was deliberate and names no label.

What the hint says, read against the state above: a solver discussing the `#FEFEFE` cell, bits and "which primes" was told he had reached "the prime part" early. With what is known now, that part is the dbbi walk (the `#FEFEFE` cell is color-event 21 of the spliced program, assigned to logical prime 73 under the fixed-prefix model; 21 is not a prime position, dossier 6.3). So the answer to "a hint on matrixsumlist" was: the prime part comes first and feeds it. The creator's own order in #8446 (yellowblueprimes, then matrixsumlist) says the same.
This yields **no new string**. "matrixsumlist is a prime operation" is already the dossier's reading (8.1), the gardeners' {2, 5, 7} answer to "which primes" is already swept (doc 104, doc 115: 13,319 card and gardener strings), and the dbbi output as the matrixsumlist operand is closed (dossier 10.9, 327 candidates). The 104 in Janusz's message equals the length of the `matrixsumlist` a/b run (dossier 6.1), but the creator answered only its spelling, so I take nothing from it.

## 2. The moment of #32579 (29 November 2024)

### Timeline, August 2023 to 29 November 2024 (what the community was told and asked)

| id | date | parent (quoted) | creator | reading |
|---|---|---|---|---|
| #8483 | 2023-04-07 | #8448 the reversed #8446 decode: yellowblueprimes, matrixsumlist, lastwordsbeforearchichoice, yinyang | 👆🤷‍♂ | four labels known to all |
| #8795, #8796 | 2023-08-03 | #8791 "is there a 3rd door yet to be found?" | "I saw that you guys got really really far already." / "Actually, the hardest part is done." | |
| #9599 | 2023-08-06 | | "Once you hit a 'ying yang', you'll be able to solve it the same day." | |
| #9607 | 2023-08-06 | #9605 "another URL to find?" | "No need. You have all the info." | |
| #9627, #9629 | 2023-08-06 | #9626 "unless Jrk thinks we already know something, which we do not" | "Something was solved rather... remarkable." / "Partly." | |
| #16624 | 2023-11-24 | | internet no longer required: "Nope" | |
| #20224 | 2024-01-26 | #20222 "...an inability to solve 'our first hint is your last command'. That seems to be the 2nd to last piece we need to..." | 🤐 | **not dismissed**; the community's own framing of the open step |
| #23151 | 2024-03-26 | #23148 "which hints are no longer relevant" | "Technically yes but Nope." | |
| #32557 | 2024-11-29 05:15 | | "Haven't interacted with a terminal in a while." | |
| #32560, #32561 | 05:17 | #32556 "Ok but hint? At least in where to focus on salph or in the puzzle" | "Hint? Hint? ... There is no hint." + Merovingian "action, reaction" gif | the gif is the phase-2 riddle's character and its word, causality |
| #32570 | 05:20 | #32568 "jrk probably doesn't even remember how to solve it" | 🤐 | |
| **#32579** | 05:28 | (no parent) | "If you guys got 1 microstep further, the puzzle will likely be solved the same day." | |
| #32613 | 05:47 | #32600 "What character do I have to imagine myself as?" | "ASCII 127" | DEL; already screened |
| #32671 | 06:06 | #32666 "It's an infinite key" | "You only need the last number of pi" | a joke (impossible) |
| #32699 | 06:23 | #32696 /PUZZLE vs /puzzle | doesn't affect the puzzle | dismissed |

### State of the community at #32579

- Held: every label (`matrixsumlist`, `lastwordsbeforearchichoice`, `thispassword`, `enter`, the two `sha256` lines, and from #8446 `yellowblueprimes` and `yinyang`), the short container, the Terminal, Cosmic Duality, and the order of #8446.
- Not held: the dbbi parse (September 2026). So the microstep did not need it, or the microstep **was** it. The second is now tested by events: the parse has been public since 18 September 2026 with no solve, and dbbi turned out to be a checksum. I take the first.
- The live question, in the community's own words, was "our first hint is your last command", which the creator met with 🤐, not a denial. Asked where to focus, he answered with causality (the gif).
- "Same day" matches #9599 (from yinyang) and #39224 ("2 hours max"), so the microstep is what opens the short container. Everything after it is fast.

### What "1 microstep" can be

A microstep is a change of **form**, not of content: the creator's one documented blocker of this size was a single character (`givetit`, #866: "nearly impossible to solve unless you'd know where to add 1 extra character"), and he tested his own puzzle three times with the typo in it (#871). So the smallest single changes to what the community held are:

| id | microstep | one-sentence justification |
|---|---|---|
| M1 | the line ending | The SalPhaseIon page is a terminal transcript (it prints `enter` where Enter was pressed), he wrote "Haven't interacted with a terminal in a while" in the same sitting, and his plaintexts carry CRLF, so `echo ANSWER \| sha256sum` (or the Windows `echo`) would hash the answer plus `\n`, `\r\n` or ` \r\n`: one byte or two that no one adds. |
| M2 | case and spaces | The SalPhaseIon textarea is the only password page with no `/(...)` format tag, so nothing enforces lowercase-connected, and an untagged answer is typed as written. |
| M3 | causality as the last part | The gif in the same sitting is causality; the puzzle's first numbered hint ("1... are you looking for the private keymaker?") says its answer "will grant the first part", and SalPhaseIon mirrors that with "our first hint is your last command". |

M1 contradicts the convention that opened phases 2, 3 and 3.2 (no line ending), so it can only hold if the SalPhaseIon password was made differently; that is the cost of the reading and is stated, not hidden.

## 3. Tests (round 7)

All under the proven convention first (`rt.py`: controls key 1 and phases 2, 3, 3.2 open and are recognised), then M1 under its own forms (`ms.py`), then the 14-cipher matrix (`ct.py`, 11 planted containers recovered).

| run | file | candidates | decrypts | valid pads | flags |
|---|---|---:|---:|---:|---:|
| M2 + M3, convention | `natural.txt`, `causality_last.txt` | 47 | 2,256 | 4 (~8.8 expected) | 1, the phase-2 control (`causality` opens phase 2) |
| M2 + M3, 14 ciphers x 5 KDFs | same | 47 | 39,480 | 173 (~155) | 0 |
| M1 on every ledger answer and on M2/M3 | `ledger.txt` (553 distinct ledger candidates, rounds 1 to 6) + the two files above | 599 | 64,692 | 240 (~254) | 0 |

`ms.py` controls: key 1, phases 2/3/3.2, and three planted containers made by the openssl 3.0.13 CLI with passwords `sha256('plantedmicrostep' + suffix)` for each suffix, all opened. Win test on every candidate with each suffix: 0 hits.

Logs: `run_rt.log`, `run_ct.log`, `run_ms.log`.

## 4. What this leaves

- #6509's hint is the prime slip, and it is already consumed by the dbbi parse; it narrows `matrixsumlist` to "after the prime part", which the dossier already holds.
- At #32579 the community held the labels and nothing more; none of the three form-level microsteps (line ending, as-written case and spaces, causality last) opens anything with any answer in the ledger.
- If the microstep is a form change, it is not one of these three applied to these answers. If it is a content change, the timeline says only that it was reachable from the labels without the dbbi parse, and that "our first hint is your last command" was the step the creator would not discuss.
