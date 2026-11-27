# 22 - How the creator thinks (OSINT profile, 2026-11-27)

**Purpose.** Move 2, workstream 1. A read of the creator's frame of mind, built to make the `yinyang` step recognizable. This is analysis only: no sweep, no candidate list, nothing run.

**Sources read for this note.**
- `PUZ` = `telegram/ChatExport_2026-09-13_result.json` (GSMG Puzzle Solvers). `COMM` = `telegram/CommunityGroup_2026-09-10_result.json` (GSMG community and support group). Creator = `user9815232`, display name "Jrk Bgrt", handle @SoWut. Ids are message ids.
- Saved puzzle pages in `gsmgio-5btc-puzzle-sept/assets/pages/` (theseedisplanted, choice-is-an-illusion, salphaseion-cosmic-duality).
- Live web, read 2026-11-27: gsmg.io home page; AirdropAlert's 2018 GSMG bot article; Medium reviews by an early Dutch user; Bittrex Global wind-down coverage (CoinDesk, CoinMarketCap); Internet Archive and resale listings for the Time-Life book *Cosmic Duality*; community GitHub repos and issues; bitcointalk topic 5151725.
- Builds on `5g-puzzle/analysis/CREATOR_PROFILE.md`, `02_CREATOR_HINTS.md` and `07_DUTCH_LENS_REVIEW.md`. Where this note repeats them, it re-read the export.

**Labels.** [quote] = his words, re-read in the source. [fact] = public record from a named source. [inference] = my reading. Confidence: high / medium / low.

**Unreachable or empty.** No creator X/Twitter account surfaced in search. The Steemit GSMG post needs JavaScript and did not load. The GSMG Intercom help centre returns 404. The barrystyle image (#8310) is not in the export ("File not included"). I did not find the source of the name "Witteveen" in anything I read; treat it as solver-supplied until someone cites it.

---

## A. Identity and origin

1. **Who.** "JRK" (Telegram "Jrk Bgrt", @SoWut) wrote the bot and the puzzle. GSMG was a small team: "JRK, d0d, Darky, Bloctite, and the remaining GSMG crew" (COMM #67742, farewell, 2026-04-13). [quote, high]
2. **Dutch.** "I'm in the Netherlands even" (COMM #41557); "Not everybody is Dutch but most of us are indeed" (COMM #52684); offers Dutch support in PM (COMM #5515, #42934). AirdropAlert (Aug 2018): "GSMG Trading bot is created by Dutch experts". [quote + fact, high]
3. **Background, in his team's own telling.** 2017, visiting Sydney "with the better half", he "locked himself in a living room for nine straight days. Zero high-end programming skills. Just Siemens PLC code, some HTML, Quake 3 scripting and a bit of Pascal. He built the entire bot from scratch as one single terrifying, never-ending script. No functions. No classes." First order hit Poloniex on 10 June (2017). First name of the script: "MR. ROIbot" (a Mr. Robot pun). (COMM #67741) [quote, high]
4. **What GSMG was.** A Dutch auto-trading bot that ran on users' Bittrex API keys from 2018 (later Binance and others), paid by commission on profitable trades plus prepaid "ETH fuel". [fact, high] I found **no formal Bittrex Global partnership** in press: the link is that the bot traded through Bittrex's API. Bittrex Global (Liechtenstein) stopped trading on 4 Dec 2023, and the creator later noted "since Bittrex is gone and Binance is not available for the Dutchies" (COMM #62394). [fact, medium on "no partnership", since absence is hard to prove]
5. **Why GSMG exists.** "JRK and d0d had just used another bot run by a scammer called fuzzyhobbit and thought nope... That disrespect for the old banking system? Still burns to this day. And that is literally where Globally Supporting My Generation came from. An old friend's group name was reused and suddenly became a mission. Give the power back to the little guy." (COMM #67741) [quote, high]
6. **Why the puzzle exists.** "JRK got inspired by other crypto puzzles and spent two sloppy days throwing one together. Full of grammatical mistakes and zero polish... In 40 years, he might admit he forgot how to solve it himself." (COMM #67741). The site now reads: "2017 - 2026. Nine years of chaos ended. One mystery remains." (gsmg.io, read 2026-11-27). [quote, high]
7. **Personal facts he volunteers** (already in CREATOR_PROFILE, re-checked): partner he calls "the better half", young children, travels (France, a Dutch Caribbean island in 2020, Ibiza), quantified-self health habits, open about psychedelics. Claims he has "seen some 'security' places" professionally. [quote, high]

## B. Worldview, as one thesis

**Money is a number someone types, and the people who hold the keyboard hold the power; his life's project is handing that keyboard to ordinary people.** Every item in his reference set says the same thing from a different angle. Fresco's Venus Project removes scarcity pricing. EO 11110, in the puzzle's own telling, is the president who "executed a specific order" against the money power and was killed for it ("never execute an order that revokes the highest power or you might suddenly get killed"). Mr. Robot's last scene erases consumer debt, and he wrote "Printing money is changing numbers with a keyboard, so is deleting money(debt)" (COMM #25493) and "I hope to witness the day that the last scene of mr. Robot becomes a reality" (PUZ #9592). The Matrix is a control system you can see through once you wake. The Merovingian line he used as a stage URL is "choice is an illusion created between those with power and those without". Bella Ciao is a partisan resistance song (and the anthem of a heist against a central bank in *Money Heist*). "Again, fiat is not to be trusted" (COMM #8062). "Wild thought: Im not sure there will even be money in 15 years" (COMM #67778). The duality that runs under all of it is **power versus the powerless**, and his stated wish is to dissolve it: "Give the power back to the little guy." [quotes high; the thesis is inference, high]

Corollary for the puzzle: he told the room three times that the coins are secondary ("Are you really looking for just the btc…?" #8774, #60307; "The '5' btc was never the actual prize" #66593; "I held quite a secret in my head which I seriously wanted to share with the planet" #66592). The finder he pictures is someone who shares this frame. [quote, high]

## C. Design style, with puzzle evidence

1. **Wordplay is the primitive.** HSM as "How so mate", "beautiful strategic position" to Beaufort, "one for one, four for one" to EBCDIC 1141, "shabef" to sha256, SalPhaseIon to salvation. He never asks for original mathematics. [fact from the solved chain, high]
2. **Hide in plain sight, and say so.** Phase 3 plaintext: "the keymaker's way of security by hiding, nearly unprotected, in plain sight". Master binary hint (#8446): "itsinfrontofyoureyesbutyourenotseeingit". The rabbit door was "hash the text" of the very first page. [quote, high]
3. **The phase name announces the plaintext.** "Breaking salphation, should be giving the feeling of the phase's name" (PUZ #6497). The stage heading is a content label. [quote, high] This is the single most useful rule in this note (see D).
4. **He has already composed complementary halves once, in an authenticated stage.** The theseedisplanted collage is eight tiles whose filenames split words between colours: `blue_lock_lo` + `red_crypto_gic` = LO+GIC, `black_banking-war` + `red_open_lock_n_ing` = WAR+NING, giving Logic's "The Warning". A word is cut in two across differently coloured tiles (LO blue and GIC red; WAR black and NING red), and you rejoin the halves. [fact from file names, high; reading the tiles as "halves to rejoin" is the accepted community solve]
5. **Colour carries data.** Phase 1 is yellow/blue/black/white cells; the poem says "Roses are White but often Red. / Yellow has a number and so does Blue." Pairs of colours recur as the carrier of a split value. [quote, high]
6. **He hints at the hard step, late, and calls it "obvious" afterwards.** "It's hinted where it would be impossible to solve but you're not there yet" (COMM #28784); "Indeed remarkable with the hints stating the path pretty obvious..." (PUZ #4688). [quote, high]
7. **He builds like a PLC engineer.** Self-taught on Siemens PLC logic, Quake 3 scripts and Pascal, wrote one linear script with no functions, and the puzzle uses only command-line tools (OpenSSL, sha256, simple encodings: "Same software was used in every phase", forward #33445). [quote high; inference about the final step, medium] Expect the last step to be a short, tool-level operation on named objects (join, hash, open), done once, with no search.
8. **Sloppy and rushed.** "spent two sloppy days throwing one together"; typos are not clues except giveit/givetit (#867, #1806, #3384). Irregularities carry no meaning by default. [quote, high]

## D. What he has said about yinyang, duality and two halves

Exact words, with location. I found **no statement in which he describes combining two halves into one key.** Everything below is the full set of related creator text.

| where | exact words | reading |
|---|---|---|
| gsmg.io SalPhaseIon page, second `<h1>` | "Cosmic Duality" (heading over the second textarea; first heading is "SalPhaseIon") | **Creator-authored**. He never wrote "cosmic" or "duality" in chat, but he did write it on the site. [fact, high] |
| PUZ #8446, 2023-02-23 (binary, reversed) | "yellowblueprimes matrixsumlist lastwordsbeforearchichoice **yinyang** wewontgiveawaythepassword itsinfrontofyoureyesbutyourenotseeingit verylaststepisatruegiveawaypromised" | yinyang is a named waypoint in his own roadmap. [quote, high] |
| PUZ #8311, #8315, 2022-12-11 | ".... That is very specific" / "If the puzzle is solved you'll see how scary specific that is 😂" | Reply to barrystyle #8310, who said he "googled a phrase which would be assumed to be part of a hint". The image is not in the export; the sibling repo records it as the Time-Life *Cosmic Duality* cover. That book is *Mysteries of the Unknown: Cosmic Duality* (1991, ISBN 0809465175, subjects "Polarity; Dualism") with a cosmic yin-yang on the cover (archive.org record; two resale listings). [quote high; image identity medium] |
| PUZ #8328, 2023-01-08 | "@barrystyle, provided a very specific hint already." | He re-pointed the room at that image a month later. [quote, high] |
| PUZ #9599, 2023-08-06 | "Probably the last hint: Once you hit a \"ying yang\", you'll be able to solve it the same day." | [quote, high] |
| PUZ #39224, 2025-04-28 | "Did anyone found yingyang? I don't think so, you guys are so smart, when yingyang is reached, 2 hours max." | [quote, high] |
| PUZ #39237, 2025-04-28 | "It's the next phase, but I await the day someone finally gets there." | Reply to a solver asking if yinyang comes after decoding an AES ciphertext. [quote, high] |
| VIC plaintext (phase 3.2.2) | "IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF AND THEY ALSO NEED FUNDS TO LIVE" | Puzzle text, his. "Better half" is also what he calls his partner (#39241, COMM #42353, #67741). [quote, high] |
| PUZ #3923, 2020-05-11 | "...who knows what you'll find after opening the 2nd door. The price is in half, but what does it mean 🤔." | Halving-day post; "price" = Dutch *prijs*, prize. Plain reading: prize halved. [quote high; any key reading low] |
| PUZ #23159, 2024-03-26 | "I prefer superpositions 😉." | Reply to "Are you a one or a zero?... a black rose... the red rose". Asked to pick a side, he picks both. [quote, high] |
| PUZ #17891/#17893, 2023-12-26 | "Have you tried the purple pill already?" / "Candy flipping into 2024 ;-)" | Red + blue = purple, but the second line makes it a drug joke (LSD+MDMA). Same instinct (take both), weak as a hint. [quote high; hint value low] |
| PUZ #4105, 2020-05-21 | "First or zero" | Counting ambiguity for "the first puzzle piece". [quote, high] |
| PUZ #9595, 2023-08-06 | "Technically my friends and family can get to all my data if they'd work together." | Knowledge held in parts by different people, which yields everything when combined. [quote high; relevance medium] |
| PUZ #66573/#66574, 2026-07-12 | "My close friends have the best chance of solving it (a few tried). But they don't have the skills some of you do." / "NOTE: that is a hint." | His only self-labelled hint. [quote, high] |

**What D implies [inference, medium-high].** By his own naming rule (C3), a phase heading tells you how its plaintext feels: SalPhaseIon reads as salvation. He headed the second textarea "Cosmic Duality", and when a solver googled that phrase and posted a yin-yang book cover, he called it "very specific" and "scary specific" and pointed at it again a month later. So **the yinyang phase and the Cosmic Duality textarea are the same thing**, named twice by him, once in English and once as a symbol. Reaching yinyang then means producing the true Cosmic Duality plaintext (the retracted 7-XOR "decrypt" `4f7a1e4e...` is a pad-1 fluke and does not count). Once that is open, he says the rest takes hours.

How he would expect a friend to see the step: a yin-yang is two halves, each carrying a dot of the other, that only make a circle together. His one authenticated precedent for a halves operation is theseedisplanted, where two coloured half-words are rejoined into one word. His reflex when offered a binary is to take both (superpositions, purple pill). The puzzle's own pairs on that page are SalPhaseIon and Cosmic Duality, side by side. This points at **the two textareas of that page belonging together as one object**, where earlier work treated each as a separate lock. That is a framing to reason from, and I am not proposing a sweep of joins.

## E. In-jokes and Dutch references a friend would catch

| item | source | plain meaning |
|---|---|---|
| "the better half" | #39241, COMM #42353, #67741 | his partner; the puzzle reuses it for the key holders |
| "price" | #3923, #5069, #9592, #60314 | Dutch *prijs* = prize |
| "proefkonijn" | COMM #45523 | "test rabbit" (guinea pig); GSMG beta testers were "bunnies"; "Boat rides with the first bunnies" (#67741) |
| "And Oen" | PUZ #3404 | reply to "Neo is an anagram of One"; *oen* = dimwit in Dutch |
| purple carrots | PUZ #49176 | "Carrots were originally purple, until the Dutch turned them orange in the 1600s to kiss up to their royal family" (House of Orange) |
| "geestverruimend" | PUZ #66976 | "mind-widening", about psychedelics |
| "Iets is het tegenovergestelde van niets" | COMM #41268 | "Something is the opposite of nothing", a line from the Dutch Wikipedia disambiguation page for *iets*, pasted as a joke answer. A small sign he reaches for opposites by default |
| MR. ROIbot | COMM #67741 | first name of the bot: Mr. Robot + ROI |
| 10 June 2017 | COMM #67741, #47838 | first live order, GSMG's birthday |
| Sydney, nine days | COMM #67741 | where and how the bot was written, with the better half present |
| "Globally supporting my generation" | PUZ #9047, COMM #10560 | the GSMG acronym; a friend group's name reused as a mission |
| Dutch island without Corona, Albert Heijn and Jumbo | COMM #41572, #42511 | spring 2020 on a Dutch Caribbean island |
| "Hush hush" | PUZ #1710, #6514 | his sign-off when he has just hinted |

## What changes for the frontier

1. Coordinator note correction: the creator **did** write "Cosmic Duality" (as the site heading). He never wrote it in chat. The Cosmic Duality link to yinyang therefore rests on his heading plus his endorsement of the yin-yang cover, which is stronger than "solver inference".
2. "Bittrex Global partnership" should read "bot that traded through Bittrex's API". No partnership record found.
3. "Witteveen" has no source in what I read. Drop it from the reference set until cited.
4. The lens for yinyang: one page, two textareas, a heading that names their relationship, a creator who rejoins halves and refuses to pick a side. The open question is conceptual: **what object does the Cosmic Duality textarea become when read together with SalPhaseIon instead of alone**, and answering it takes reasoning about his frame. More compute will not supply it.
