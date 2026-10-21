# 02 — Creator hints (Jrk Bgrt, the puzzle creator)

**Sources**
- `PUZ` = `telegram/ChatExport_2026-09-13_result.json` ("GSMG Puzzle Solvers", 61,798 messages, 2019-04-20 → 2026-09-13).
- `COMM` = `telegram/CommunityGroup_2026-09-10_result.json` ("GSMG - Community & support group", 52,913 messages, 2018-04-17 → 2026-09-10).
- Full creator message lists are in `telegram/sourcebooks/CREATOR_MESSAGES.md` and `FORWARDED_CREATOR_POSTS.md`.

**Status tags**
- **[checked]**: the text was re-read in the export during this clean-up.
- **[digest]**: carried over from an earlier round's ledger and not re-read this time. The id is given so it can be looked up.

## Read this first: how far to trust hints

- **Edits.** 244 of 492 creator messages carry an `edited` timestamp. **Most late "edits" are not text edits:** Telegram bumps `edited` when reactions change. Of the 122 creator messages edited more than 30 days after posting, 84 have an edit time within 2 s of a reaction in the export (checked 2026-09-13). The other 38 mostly have no reaction data, so they are unexplained, not proven edits. Real text changes are known only where old copies exist (for example, #8446's forwards decode identically; #8000's wording is in an Aug 2023 screenshot [log]; #3384 says site typos were fixed). A full diff is still open lead 13.
- **Dates.** Dates are in the export's time zone, about 4 h behind UTC. Near midnight a message can fall on the neighbouring day.
- **Not the creator** (often mis-cited): #5241 (Saber), #6891 "{30},{2},{77}" (x7x7x7x6), #39233 (the yinyang question), #60352, #65924, #42477, #18782. See 06 §5.
- **Cite by id, not by count.** Counts shift between exports; ids are stable within a chat.
- **Policy changed.** Early on, "no hints" (#898 [digest]) was the rule. Many hints came later.
- **Contradictions exist.** See the end of this file.
- **Words he never wrote.** The creator never wrote "btcseed", "Bifid", "cosmic" or "duality". Any link from those words to him is a solver inference.

## 1. Envelope, format and "same software"

| id | date | text | notes |
|---|---|---|---|
| PUZ #225 | 2019-04-22 | Phase 1 hash `5ac40783…` | [checked] It confirmed the Phase 1 answer (see 01 §2). |
| PUZ #867 | 2019-05-17 (edited 2025-04-30) | "Here's the hint in order to bypass the mistake: giveit = givetit" | [checked] The current Phase 3.2 blob opens with **giveit** (see 01 §5). |
| PUZ #1465 | 2019-09-22 | "7 parts right?" | [checked] About the Phase 3 password (see 01 §4). |
| forward #33445 | 2024-12-01 | "You're going too fast now. Same software was used in every phase." | [checked] Forwarded by Jerry from Jrk Bgrt. This supports assuming the same envelope convention for the locked blobs; it does not prove it. |
| PUZ #20223 | 2024-01-26 | "Regular Bitcoin Private key" | [checked] |
| PUZ #24627 | 2024-04-19 | "A private key, some 'obscure' intel, or … hold on to Bitcoin" | [checked] |

## 2. Where the key is / what remains

| id | date | text | notes |
|---|---|---|---|
| PUZ #2910 | 2020-03-24 | "Answering that would be too much of a hint." | [checked] Reply to #2906: is the complete private key in the final chapter or in pieces? |
| PUZ #2918 | 2020-03-24 | "There must at least be something hidden in there." | [checked] Reply to #2911: "PK is in the last cipher of 3.2 decoded. Can you confirm?" He did **not** confirm a complete key. |
| COMM #28534 | 2019-04-19 | "1 private key is hidden in there." | [checked] |
| PUZ #7832 | 2021-08-11 | "The one to be found by solving the puzzle yes" | [checked] Reply to #7831: "encrypted private key stored online?" |
| PUZ #7834 | 2021-08-11 (edited 2026-01-06) | "And the solver will find a way to 'decrypt' it." | [checked] |
| PUZ #8796 | 2023-08-03 | "Actually, the hardest part is done." | [checked] |
| PUZ #9607 | 2023-08-06 | "No need. You have all the info." | [checked] Reply to #9605: is there another URL, or is it brute force? |
| PUZ #16624 | 2023-11-24 | '"Given the available knowledge, is internet still required to solve it?" Nope' | [checked] |
| PUZ #9639 | 2023-08-06 | "Correct. Well, technically, you'll need the internet to claim the prize in the end 🤔." | [checked] |
| PUZ #32579 | 2024-11-29 | "…If you guys got 1 microstep further, the puzzle will likely be solved the same day." | [checked] |
| PUZ #60314 | 2026-03-03 | "I only need to look at the address. If any of you reaches the next phase, the price is taken in no-time." | [checked] |
| PUZ #63957 | 2026-05-28 | "Ah, ofcourse. The puzzle is still valid!" | [checked] |

## 3. "yin yang" — the next phase

| id | date | text | notes |
|---|---|---|---|
| PUZ #9599 | 2023-08-06 | 'Probably the last hint: Once you hit a "ying yang", you'll be able to solve it the same day.' | [checked] |
| PUZ #39224 | 2025-04-28 | "Did anyone found yingyang?… when yingyang is reached, 2 hours max." | [checked] |
| PUZ #39237 | 2025-04-28 (edited same day) | "It's the next phase, but I await the day someone finally gets there." | [checked] Reply to #39233 (silver_anth, not the creator): "is yinyang found after decoding an AES ciphertext?" **Caveat:** #39233 shows edited 2025-08-26, which may be a reaction bump. |
| PUZ #23159 | 2024-03-26 | "I prefer superpositions 😉." | [checked] About "one or zero". |

## 4. Doors

| id | date | text | notes |
|---|---|---|---|
| PUZ #1487 | 2019-09-26 (edited 2025-04-30) | "There may indeed a piece be found outside the main puzzle." | [checked] |
| PUZ #1710 | 2020-01-14 (edited 2024-04-24) | "Roses are White but often Red. / Yellow has a number and so does Blue. / Go back to the first puzzle piece without further ado. / It might have shown you only one door, beware that the rabbits nest may contain a whole lot more. / Hush hush." | [checked] |
| PUZ #3923 | 2020-05-11 (edited 2024-12-23) | "…who knows what you'll find after opening the 2nd door. The price is in half, but what does it mean 🤔." | [checked] Posted on halving day, 30 min after #3922 complained about halving the prize. He uses "price" for *prize* (Dutch *prijs*: #5069, #7396, #9592, #60314). **Plain reading: the prize was halved** (cf. Dutch forward #65533). Reading it as "the key is in Half" is not the default (07 §2a). |
| PUZ #4105 | 2020-05-21 (edited 2025-12-23) | "First or zero" | [checked] Follows #4096 (points to the #1710 poem), #4101 "first piece is a zero piece? … rabbit is a zero step", #4102 "answer is there", #4104. It confirms that the "first puzzle piece" may be counted as piece 1 or piece 0; it is not a bit value (07 §2c). |
| PUZ #4590 | 2020-08-02 (never edited) | "Really nobody managed to find the extra door…" | [checked] |
| PUZ #6884 | 2021-04-01 (edited 2025-02-02) | 'Hint: "another door might be found on {1 },{4} ,{21}"' | [checked] **Likely an April Fools joke** (see #7529). Compare V, I, C at 1, 4, 21 in DBBI−VIC (01 §7). |
| PUZ #7529 | 2021-04-18 (edited 2026-07-22) | "Do you know what usually happens on the first of april?" | [checked] Reply to "is this an actual hint… April 1st". |
| PUZ #7914 | 2021-12-02 22:41 (never edited) | "There is / Another / D / O / O / R" | [checked] |
| PUZ #8000 | 2021-12-26 (edited 2026-02-15) | "The previous "there is another door hint" is still a thing. We're not sure if anyone has found another door so far, and we can't check that... We've seen prime numbers being mentioned; well, that is definitely an aspect which is required to proceed. Furthermore, along the way, some characters need to be 'zeroed out'.. Best of luck and happy holidays! 🥂" | [checked] "Previous door hint" more likely means #7914 than #6884. |
| PUZ #4096 | 2020-05-20 (edited 2025-12-23) | "This one 👆." | [checked] Reply to #1710, after #4076 "The January hint is missing on github" and #4094 "It is". Confirms #1710 is the January 2020 "final hint" announced in #881. |
| PUZ #66903 | 2026-07-16 | "Well, it's hidden in a room with a hidden door." | [checked] **Not a puzzle-door hint:** it replies to #66901 "I … spent the whole night looking for your laptop😂" (the laptop of #66568). |

## 5. Primes, zeroing, numbers

| id | date | text | notes |
|---|---|---|---|
| PUZ #1837 | 2020-02-22 (never edited) | "Only -41,-17 matters" | [checked] |
| PUZ #5966 | 2021-03-01 (edited 2025-09-08) | "You are at the prime part already???" | [checked] Reply to Janusz Baran #5963 "just say which primes 2,3,5,7 we need use", in a matrix thread (#5977 "matrix 14x15"). |
| PUZ #5969 | 2021-03-01 06:35 (never edited) | "Oh wait, shouldn't have said that. That might have been a hint 🤔." | [checked] The only accidental hint he labels as such before #6509, and so the likely "unforseen hint" for matrixsumlist [inference, strong; 09 §1]. |
| PUZ #6250 | 2021-03-05 (edited 2025-09-08) | "Infrared" | [checked] |
| PUZ #6913 | 2021-04-01 (edited 2025-08-09) | "R=18 A=1 B=2 Could also be 21 or 1812 bit 🧐…" | [checked] Posted on April 1st. |
| PUZ #8330 | 2023-01-09 (edited 2025-09-02) | "At least prime number is very important to get any further." | [checked] |
| PUZ #32613 | 2024-11-29 | "I think I'll be going for ASCII 127 myself. But not overly dramatic." | [checked] Reply to "which character would you imagine yourself as". |
| PUZ #32671 | 2024-11-29 | "You only need the last number of pi and it might get you somewhere." | [checked] Reply to "infinite key". |
| PUZ #70307 | 2026-09-01 | "Pfff. Coincidence." | [checked] No reply link. It follows Diego #70303: {1,4,21} → VIC in the YOUWON text, and the tail after YOUWON gives 103 A1Z26 digits (reproduced: L4 in `data/leads_reproduced.json`). It also follows Cereal Killer #70306 ("coincidence"). The referent is inferred, but only a few messages separate them. |

## 6. Theory of everything, Jacque Fresco, the address, "better half"

| id | date | text | notes |
|---|---|---|---|
| PUZ #8354 | 2023-01-12 (edited 2025-09-02) | "Focussing on the theory of everything is also still a valid path to reaching the private key." | [checked] |
| PUZ #60298 | 2026-03-03 | "Jacque was quite an inspiring lad I'd say." | [checked] |
| PUZ #60309 | 2026-03-03 | "Looks at gnomad. 👀" | [checked] |
| PUZ #60312 | 2026-03-03 | "Bingo" | [checked] **Caveat:** no reply link. The referent (often taken to be *Looking Forward*) is inferred. |
| PUZ #60324 | 2026-03-03 (edited 03-06) | "I'm going to rewatch episode 3.5 with  the better half." | [checked] **"The better half" is his partner** in #39241, COMM #42353 and #61385 / COMM #67741. The plain reading is watching (probably Mr. Robot eps3.5) with his partner, right after #60322 about unanswered DMs. The "Better Half" address (01 §9) is separate (07 §2b). |
| PUZ #8048 | 2021-12-31 | "The only date I give away is the expiry date of neo's passport." | [checked] Reply to joke questions. |

## 7. Barrystyle / Cosmic Duality / proof-of-work answers

| id | date | text | notes |
|---|---|---|---|
| PUZ #8311 | 2022-12-11 | ".... That is very specific" | [checked] Reply to barrystyle #8310 (the Cosmic Duality image post). |
| PUZ #8315 | 2022-12-11 (edited 2025-09-02) | "If the puzzle is solved you'll see how scary specific that is 😂" | [checked] |
| PUZ #8328 | 2023-01-08 | "@barrystyle, provided a very specific hint already." | [checked] |
| PUZ #8446 | 2023-02-23 | Binary message | [checked] Reversing the whole bitstream gives the 7 phrases: `yellowblueprimes matrixsumlist lastwordsbeforearchichoice yinyang wewontgiveawaythepassword itsinfrontofyoureyesbutyourenotseeingit verylaststepisatruegiveawaypromised`. The order puts "yellow blue primes" directly before "matrixsumlist" (09 §1). |
| PUZ #8483 | 2023-04-07 | "👆🤷‍♂" | [checked] Reply to #8448's decode. **Ambiguous.** |
| PUZ #8569 | 2023-06-10 | "Correct. / - / No. / - / Can't say anything about this." | [checked] Answers PoW questions #8566–8568. **Caveat:** the mapping assumes he answered in question order (see 01 §8). |

## 8. 2026: "the actual answer", close friends, NOTES

| id | date | text | notes |
|---|---|---|---|
| PUZ #66568 | 2026-07-12 | A hidden laptop: "On that thing... is the actual answer" | [checked] |
| PUZ #66573 | 2026-07-12 | "My close friends have the best chance of solving it (a few tried). But they don't have the skills some of you do." | [checked] |
| PUZ #66574 | 2026-07-12 (edited 2026-08-23) | "NOTE: that is a hint." | [checked] Follows #66571 "Quite a few in this chat, already met me" and #66573. He writes "Note:" habitually (#1703, #9621; COMM #16698, #43663). |
| PUZ #66588 | 2026-07-12 21:01 | "Yes" | [checked] No reply link; 3 minutes after #66587 "salphaseion is 100% solveable?". |
| PUZ #66589 | 2026-07-12 (edited 07-13) | "And IIFF I'm somehow still wrong, which I'm most likely not as I've verified many times back then after some sad rushed mistakes, it's all still solvable with a few stable qubits." | [checked] Followed by #66590 "But... Bip360 anyone. Thoughts?" |
| PUZ #66593 | 2026-07-12 | 'The "5" btc was never the actual prize. That was only a tiny fraction.' | [checked] |
| PUZ #66600 | 2026-07-12 | "Some already found it. And understood not to risk it... 🤐" | [checked] |
| PUZ #66962 | 2026-07-16 (edited 07-18) | "Latetly, I'm working with many NOTES." | [checked] **Reply to #66958** "Waiting for the 'NOTE: that is a hint.' moment", so it reads as a joke echo. This weakens the music-notes (*noten*) reading (07 §3). |
| PUZ #70311 | 2026-09-01 | "A. I rushed (t)it. / B. Yes, have quite some time for stupid stuff." | [checked] |
| PUZ #70336 | 2026-09-01 | "Couple hours, and no." | [checked] |
| PUZ #70377 | 2026-09-01 | "Same same" | [checked] Reply to "two sloppy days". This is the last creator message in the export. |
| PUZ #53342 | 2025-12-31 | Encoded message | [checked] It decodes to 'Happy new year! Make the best of everything. Oh, and here's a "tiny hint" <3.' The full sequence is in `sourcebooks/NEW_YEAR_SEQUENCE.md`. |
| PUZ #3338 | 2020-04-08 | "Those hints are the last hints. Although I can say that one team managed to find something..." | [checked] |
| PUZ #20224 | 2024-01-26 | "🤐" | [checked] Reply to "our first hint is your last command". |

## 8b. Added 2026-09-13 from the session-log review (all [checked] in the export)

| id | date | text | notes |
|---|---|---|---|
| PUZ #74 | 2019-04-20 | "Ok.. somebody has cracked the first code." | Timeline. |
| PUZ #325 | 2019-04-23 (edited 2025-04-30) | "Ewout managed to crack the april 1st puzzle. He was the first to solve it." | The April puzzle is a solved side puzzle. |
| PUZ #881 | 2019-05-18 (edited 2026-01-03) | "In case the private key hasn't been found in 2019 we'll release a tiny hint at the start of 2020, that will be the final hint. …" | That hint is #1710 (#4096). |
| PUZ #3384 | 2020-04-08 (never edited) | "Quite some typos have been changed already. The biggest blunder so far in the mainline of the puzzle was givetit instead of giveit 😩🔨" | Site text *was* edited for typos. |
| PUZ #4102 | 2020-05-20 | "answer is there" | Shortly before #4105 "First or zero". |
| PUZ #4624 | 2020-08-09 | "a private key" | Reply to "private key or seed phrase or phrase for brain wallet?" Earliest format answer. |
| PUZ #4688 | 2020-08-12 | "Indeed remarkable with the hints stating the path pretty obvious..." | |
| PUZ #6497 | 2021-03-14 (edited 2025-06-26) | "…When people progress in salphation it might be cracked pretty soon. Breaking salphation, should be giving the feeling of the phase's name. …" | A plaintext acceptance cue ("salvation"). |
| PUZ #6509 | 2021-03-14 | "I gave an unforseen hint already 🤷‍♂" | Reply to #6508 "time for a hint on matrixsumlist?". "Unforseen" = unplanned in his usage (#879; COMM #14307, #36509, #49547). Most likely referent: #5966/#5969 (09 §1). |
| PUZ #6514 | 2021-03-15 03:16 (edited 2025-03-27) | "Hush hush" | His next message after #6509. It follows #6512 'is salph related to hint about "roses are..."?'. The only other time he writes "hush" is the last line of #1710 [checked; nod to #1710 is inference]. |
| PUZ #3390 | 2020-04-08 (edited 2025-01-31) | "Humph. Hope, it is the quintessential human delusion, simultaneously the source of your greatest strength, and your greatest weakness." | Reply to Tracer #3389 "The door that leads to the source?". Word for word the **Scott Manning** Architect transcript (`rabbit/tools/arch_src2.md` l.109), i.e. the line right after the doors choice (09 §2). |
| PUZ #6712 | 2021-03-22 (edited 2026-05-06) | "Nr 5 in salph" | |
| PUZ #8516 | 2023-05-02 | "Still remarkable that scene. Especially the expiration date of his passport 😁." | |
| PUZ #9627 / #9629 | 2023-08-06 | "Something was solved rather... remarkable." / "Partly." | A private partial solve. |
| forward #11248 | 2023-08-22 (original date unknown) | "Follow the white rabbit" | Jerry's forward of Jrk Bgrt answering "what was the actual first hint" (#11247); #11249 "That was years ago". Candidate for "first hint is your last command" (06 §3). |
| PUZ #24071 | 2024-04-10 (edited 22 min later) | "1357 blocks to go" | ≈ 9.4 days before the 2024-04-20 halving: a halving countdown, not an operand (cf. #3903 "Happy halving!", 2020-05-11). |
| PUZ #70325 | 2026-09-01 | "🤐" | |

## 9. Other ids worth looking up [digest, not re-read]

**PUZ messages**
- #226, #866, #875, #881, #887
- #898 ("no hints")
- #1806 (typos)
- #2013 ("3.2 is a thing")
- #4096, #4694, #5069, #5717, #6491, #6497, #6514, #7418
- #7830 ("Technically we do")
- #8352, #8353
- #8385 ("42")
- #8516, #8773–8774, #9047, #9595, #9621
- #12653 ("Correct": the OP_RETURNs are not his)
- #17891 / #17893 (purple pill)
- #23120, #23200, #24071, #26875, #32535, #39219
- #49175–49176 (carrots)
- #60289, #60307, #66559, #66571, #66931, #66961

**Forwards**
- #14197: Decentraland coordinates; see `evidence/decentraland`
- #15781
- #24156: "forgot the last details"
- #28293: slack music
- #28300
- #50656: hex decoding to "Surebutwewontgiveitaway"
- #65533–65535: Dutch. Translated in 07 §4: the prize halves every halving; "there really is a private key to be found"; "you have to be seriously good, it isn't lying around". #65528 + photo_2244 is a scam-DM joke, not a hint.

**COMM**
- #28538: "Equivalent of 25 btc"
- #28526–28527: vanity address, "Only 4 chars"
- #28782–28784: about the Phase 1 format
- #25986 / #26143: April Fools

**Dutch-English.** He writes Dutch word order and word choices ("There may indeed a piece be found…", "high likely", "of" = or, "price" = prize). Read these plainly, not as code (07 §1).

## 10. Contradictions and tensions (do not paper over)

- **Internet.** #7830–7834 (an encrypted key is stored online) vs #9607 and #16624 (all the info is there; no internet needed). One reading: the key was online once and is now local to the puzzle. That reading is unproven.
- **Prize size.** #20223 ("regular Bitcoin private key") vs #66593 ("5 btc was never the actual prize") and COMM #28538 ("equivalent of 25 btc").
- **Personal knowledge.** #66573–66574 (close friends have the best chance; "NOTE: that is a hint") vs #9607 ("you have all the info"). #66962 (NOTES) is a joke echo of #66574 (07 §3).
- **{1},{4},{21}.** It looks like a hint, but #7529 points to April Fools. One solver dismissed as jokes: {1,4,21}, R=18, ASCII 127, superpositions, infrared, pi, and the New Year message. That is an opinion, not a finding.
- **Typos.** They are not clues (#1806, #5960), except giveit/givetit (#867).
