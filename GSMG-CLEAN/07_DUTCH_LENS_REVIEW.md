# 07 — Dutch-lens reading of the creator's messages (2026-09-13)

**What this is.** A reading pass, not a search run. Every message by the creator (Telegram `user9815232`, Jrk Bgrt / "SoWut") and every forward attributed to him was read with one question: *does knowing he is Dutch change what this message means?*

**Scope**
- Puzzle Solvers export (`telegram/ChatExport_2026-09-13_result.json`): all 817 creator messages and forwards were read in full.
- Community group export (`telegram/CommunityGroup_2026-09-10_result.json`): 5,424 creator messages. These are almost all trading-bot support. I read every message flagged as Dutch (18 clear, 51 possible) and every message matching puzzle words (puzzle, rabbit, phase, hint, prime, zero, half, price/prize, note, terminal, Dutch). I did **not** read the rest line by line.
- The dump was made with a throwaway script (scratchpad, not kept here). It selects `from_id == "user9815232"` or `forwarded_from == "Jrk Bgrt"` and flags Dutch stop-words. Context for each item below was then read in the export itself.

**Labels.** [checked] = read in the export with its surrounding messages. [inference] = my reading; it is not proven.

## Bottom line

1. **No hidden Dutch puzzle key turned up.** No Dutch word, pun or Dutch-only reading gives a new instruction, answer or password.
2. **The Dutch lens mostly *removes* false clues.** Several messages that were being read as cryptic are ordinary Dutch-English with a plain meaning (§2). The biggest ones: "price" means *prize*, and "the better half" is his partner.
3. **The NOTES / music-notes idea is weakened.** I suggested it earlier. He writes "Note:" out of habit, and #66962 "NOTES" was a joke reply (§3).
4. **Neo's passport:** day-first date formats were **already covered** by rabbitv4 F (§5). Nothing to re-run there.
5. **photo_2244 is not a hint.** It is a screenshot of a scam DM (§4).

## 1. How to read his English

He writes Dutch word order and Dutch word choices in English. These are his normal style, so **they should not be treated as deliberate oddities**. [checked]

| id | text | Dutch source | plain meaning |
|---|---|---|---|
| PUZ #874 | "3th phase" | *3de fase* | third phase |
| PUZ #887 | "consist out of" | *bestaan uit* | consists of |
| PUZ #1487 | "There may indeed a piece be found outside the main puzzle." | verb-final order (*er kan inderdaad een stuk gevonden worden*) | a piece may be found outside the main puzzle. The word order is not a code. |
| PUZ #3373, COMM #35284 | "typo's" | Dutch plural apostrophe | typos |
| PUZ #3905, #9621 | "high likely" | *hoogstwaarschijnlijk* | highly likely |
| PUZ #4307 | "dosis" | *dosis* | dose |
| PUZ #6541 | "If know about" | *ik* → "I" dropped/typo | if I know about |
| PUZ #6712 | "Nr 5 in salph" | *nr.* | more likely "the 5th person/team is in SalPhaseIon" (cf. #6491 "Another person (or team) made it to salph"); see 08 §4 |
| PUZ #8034, #39224 | "did … found" | past-tense mix-up | did … find |
| PUZ #9632 | "obstacle parc here on France" | *parc*, *op* | obstacle park here in France |
| PUZ #24491 | "out of the drawer of either slap" | *of* = "or" | either … or |
| PUZ #66540 | "turn myself around in my grave" | *zich omdraaien in zijn graf* | turn in my grave |
| PUZ #66976 | 'in Dutch its called "geestveruimend"' | mind-expanding (about psychedelics) | not puzzle material |
| COMM #25644 | "The dutch law doesn't even a legal framework" | dropped verb | — |

**Consequence.** Solvers should not squeeze meaning out of odd grammar, word order or spelling in his messages. The one exception he confirmed himself is giveit / givetit (#867, #3384, COMM #35284).

## 2. Readings that change

### 2a. "price" = *prijs* = **prize** [checked]

Dutch *prijs* means both "price" and "prize". He uses "price" for the prize again and again:
- #5069 "price money"
- #7396 "gets the price"
- #9592 "the 'main price'" (*hoofdprijs*)
- #9595
- #60314 "the price is taken"
- #8364 "Every btc halving the price will half too"
- COMM #35310 "we'll be halving the price at next btc halving"

**#3923** (2020-05-11 16:31, edited 2024-12-23): "Let's see what bitcoin is worth the next halving and who knows what you'll find after opening the 2nd door. The price is in half, but what does it mean 🤔."
- It was posted on halving day. That was 30 minutes after #3922 complained that halving the prize kills the incentive, and 1 hour after "Happy halving!" (#3903).
- Dutch forward #65533 says the same thing plainly: *"Iedere btc halving wordt de prijs overigens gehalveerd"* ("every BTC halving the prize gets halved, by the way").
- **Plain meaning:** the prize has been halved. "What you'll find after the 2nd door" hints that the reward is more than the visible BTC (cf. #66593 "The '5' btc was never the actual prize").
- [inference] The 🤔 still leaves room for a second meaning, because solved marker addresses are named Half / Better Half (01 §9). But **"the key is inside 'Half'" is not the default reading** of this message.

### 2b. "the better half" = his partner [checked]

- PUZ #39241 (2025-04-28): "Ok, the 'better half' is hungry. Which means I'm off."
- COMM #42353 (2020-04-22): "I'm collecting my better half from work with the little one in the back."
- #61385 forward and COMM #67741 (GSMG farewell, 2026-04-13): "JRK was visiting Sydney with the better half."
- So **#60324** "I'm going to rewatch episode 3.5 with the better half" plainly means *watching (probably Mr. Robot eps3.5) with his partner*. It came right after he apologised for not answering DMs (#60322).
- [inference] The "Better Half" marker address is still real (01 §9), and he may enjoy the double meaning. But this message is **not** evidence that episode 3.5 is a key to the Better Half address.

### 2c. "First or zero" (#4105) [checked]

The thread, in order:
- #4096 "This one 👆" (a reply to the #1710 poem: "Go back to the first puzzle piece…")
- #4101 (a solver): "first piece is a zero piece? … rabbit is a zero step"
- #4102 "answer is there"
- #4104: "Do you mean the answer to another door from the 1st piece?"
- #4105 "First or zero"

**Plain meaning:** the "first puzzle piece" in #1710 may be counted as piece 1 or as piece 0 (the rabbit / poster step). He is confirming the solver's ambiguity, not stating a bit value. Dutch adds nothing distinctive here. The earlier "poster vs rebus" note in 02 fits this thread.

### 2d. "bunny" = *proefkonijn* (test rabbit) [checked]

- COMM #45520–45525: a user asks "What bunny means / Beta tester?"
  - Creator: "Yes" / '"proefkonijn" in dutch.'
  - *Proefkonijn* is literally "test rabbit" (English "guinea pig").
- GSMG's bot tiers and phases use this word: COMM #31282 "In bunny phase at the moment" (feature testing, explicitly "it's not a puzzle"); COMM #65800 "way passed bunny status".
- [inference] In his own vocabulary, rabbit/bunny carries the sense "test subject / first trial". This is background for "follow the white rabbit" and "the rabbit's nest", **not** a decoded instruction. Nothing here was tested and no test is proposed.

### 2e. "And Oen" (#3404) [checked]

- A solver wrote "Neo is anagram for One" (#3403). He replied "And Oen".
- *Oen* is Dutch for "dimwit".
- [inference] This is a Dutch joke riding on the anagram. It carries no puzzle content.

## 3. NOTE / NOTES: the music-notes idea is weakened [checked]

- He writes "Note:" as an ordinary aside all the time:
  - PUZ #1659, #1703 ("Note: not trolling with scripted cake this time"), #9621, #11989
  - COMM #16698, #35129, #37825, #43663, #43934
- **#66574** "NOTE: that is a hint." (2026-07-12) follows #66571 "Some of you, can find me. Quite a few in this chat, already met me" and #66573 "My close friends have the best chance of solving it". Just before this, Zil asked him to "stop drinking/hinting" (#66569).
- **#66962** "Latetly, I'm working with many NOTES." (2026-07-16) is a **reply to #66958** "Waiting for the 'NOTE: that is a hint.' moment". The capitals echo his own earlier "NOTE:". It reads as a joke.
- Dutch *noten* does mean musical notes (and also nuts). He does talk about music:
  - forward #28293: "tiny hint in the music channel on slack for the rabbit phase"
  - COMM #28961: the same claim in 2019
  - COMM #66598: a track suggestion, "My habitat - J ribbon"

  But nothing in the NOTES messages themselves points to music.
- **Change to 03 §16:** "musical notes" drops from a named reading to an unsupported one. The personal-knowledge reading of #66573–66574 remains. The **Slack music-channel hint for the rabbit phase** (#28293, COMM #28961) is a separate, older and firmer claim. The rabbit phase is solved, so it matters only as a method precedent.

## 4. The Dutch forwards and photo_2244 [checked]

All are forwarded by "sol" on 2026-06-18 and attributed to Jrk Bgrt. Their original date is unknown.

| id | Dutch | translation | reading |
|---|---|---|---|
| #65528 + `photo_2244@18-06-2026_12-19-18.jpg` | "Is deze digitale vlegel de laan al uitgestuurd?" | "Has this digital lout been sent packing yet?" | The photo is a Telegram DM from "Denn yy" pitching a bitsgamex.com jackpot scam. The creator's replies: "My robot does this for me." and "Please send 0.1 BTC to my address. 183hmJGRuTEi2YDCWy5iozY8rZtFwVgahM and I might look into it." **A scam joke, not a hint.** sol then reposted that address (#65531, "=)))"). Whether "Denn yy" is the chat member Denis Golovkin (#65525, same minutes) is [inference] only. |
| #65533 | "Hehe, leuk. Iedere btc halving wordt de prijs overigens gehalveerd. Die puzzelaars moeten gewoon opschieten. Ligt niet aan ons dat het zo lang duurt. … Het welkomst puzzeltje was binnen 2 uur opgelost. We hadden geschat dat dat minimaal een week ging duren.." | "Hehe, nice. Every BTC halving the prize gets halved, by the way. Those puzzlers just need to hurry. Not our fault it takes so long. It's fun to watch from the sidelines: teams of hackers who sink their teeth in and race through the puzzle until they get stuck again. The welcome puzzle was solved within 2 hours. We had estimated it would take at least a week.." | The "welcome puzzle" / 2 hours points to the April 2019 start (COMM #26065–26141). Confirms 2a. |
| #65534 | "Zo lame zijn we niet, er is daadwerkelijk een private key te vinden." | "We're not that lame; there really is a private key to be found." | Plain. |
| #65535 | "Moet je wel van goede huizen komen, hij ligt niet voor het oprapen." | "But you have to be seriously good (*van goeden huize komen*); it isn't lying around for the taking (*niet voor het oprapen*)." | Plain difficulty statement. It is not "good houses" or a location. |

## 5. Neo's passport and day-first dates [checked]

- `E:\rabbit-combined\rabbitv4\rabbit\analysis\leads_2026_09_12\f_neo_passport.py` `date_forms()` (read only) already generates:
  - dd-mm-yyyy, mm-dd-yyyy and yyyy-mm-dd, with yyyy and yy, with separators "" / "/" / "-" / "." / " ", and with month "09" and "9"
  - lowercase "11 september 2001"
  - Unix times, day-of-year and Julian day
- So "11-09-2001", "11092001", "11.09.01" and similar were all in the 1,861,464-trial null (04 §E, F).
- **Dutch-only gaps** (not tested, very small): "elf september 2001", "11 sept. 2001" (with a dot), "elfseptember".
- Context: #8048 was a refusal to give his own birth date (rabbitv4 RESULTS). I do not recommend spending a run on these gaps.
- Checked on the side: "elf" (Dutch for eleven) appears as "U said elf hint)" at PUZ #1706/#1708. That is a solver (0xColombo), probably a typo for "self". It is not the creator.

## 6. English messages worth re-reading (found during this pass) [checked]

These are not Dutch, but they bear on the diagnosis in the session.

| id | date | text | why it matters |
|---|---|---|---|
| COMM #29123 | 2019-04-22 | "Success detection of unlocking phase 3 is the same as you'd crack any other hash." | Phase 3's check was a hash comparison. This supports the self-verifying-intermediate point: a correct step gives an unambiguous check. |
| COMM #29132 | 2019-04-22 | "Nope, no hints after reaching stage 2. Hash won't help you anyhow." | — |
| COMM #28784 | 2019-04-21 | "It's hinted where it would be impossible to solve but you're not there yet." | The hints sit at the hard step itself. |
| COMM #32043 | 2019-05-18 | "…The 'last' part of the puzzle will ensure that there's quite some time for you guys to catch up…" | The last part was designed as the slow part. |
| COMM #65880 | 2025-10-21 | "Creating it is way easier than solving it; those who got so far are the true genies." | — |
| COMM #63031 | 2025-01-26 | "I'll just refrain from making a joke about being in your prime on this one." | A pun on "prime" (reply to "no, it is not a prime" about 69). Not a hint. |
| COMM #69023 | 2026-08-15 | "As we stopped trading services. I wont be mad at puzzle talk here anymore ;-)." | The community group may now carry puzzle talk after 2026-08-15. The 2026-09-10 export has almost none of it. |
| COMM #67787 | 2026-04-14 | '"The world is a business".' | A film quote (Network, 1976) in a chat about the future. Not a hint. |

## 7. What this changes, and what it does not

**Changes (applied to 02 and 03):**
- #3923: plain reading = prize halved.
- #60324: better half = partner.
- #66962: a joke echo of "NOTE:".
- #4105: the thread context.
- The Dutch forwards are translated.

**Does not change:**
- No lead in 03 gains or loses tested status.
- No null in 04 is voided.
- The "Half" / "Better Half" marker addresses stay solved facts (01 §9).

**Still open, and only a human who knows him could close it:**
- the "close friends" / personal-knowledge reading of #66573–66574
- the Slack music-channel hint (the Slack workspace is gone)
