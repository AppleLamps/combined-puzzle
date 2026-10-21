# Creator messages — hints not covered by the 10 Sep review

Export: `newest-telegram-export_2026-09-12/result.json` (61,669 messages, last 2026-09-12 15:12 UTC).
Creator: `user9815232` "Jrk Bgrt" (@SoWut). Scope: 492 direct messages, 18 service events, and 324 forwards (139 distinct texts).
The "Review hits" column counts mentions in `rabbit/CREATOR_AND_PLAINTEXT_REVIEW_2026-09-10.md`.

## 0. What changed since the 9 Sep export

**Nothing from the creator.** The creator has 0 new messages, 0 edits and 0 deletions, and the forward count is unchanged (324). The 251 new messages (ids 71331–71603) all come from other users. Diff: `_diff.txt`.

## 1. Leads the previous review did not pick up, ranked by signal

| # | Message | Why it matters | Review hits |
|---|---|---|---|
| 1 | **#60312 "Bingo"** | Chain: #60298 Jrk "Jacque was quite an inspiring lad" → #60304 Denis Golovkin: *Wasn't "it's in front of your eyes but you're not seeing it" a recommendation to read "Looking Forward"?* → #60309 Jrk "Looks at gnomad 👀" → #60310 gnomad "Looks at DG's comment…" → #60312 Jrk **"Bingo"**. This is the only direct creator confirmation of a referent for a line from the 2023 reversed-bit hint. *Looking Forward* (Jacque Fresco & Ken Keyes Jr, 1969) is a real text. It could supply the "text in front of your eyes", the "last words" source, or the Fresco-themed Architect message. Also #26875: "I simply liked Jacque's ideas a lot". | 0 |
| 2 | **#8569 "Correct. / No. / Can't say anything about this."** | This replies point by point to PoW's #8566–8568. (a) The phase 3.2 final block `U2FsdGVkX1+0Wl49gnWT…` (salt `b45a5e3d827593ca` = `1st_half.bin`) is not decrypted → **Correct**. (b) It holds the SalPhaseIon hint → **No**. (c) Norton's theorem and `# X 2 S H 4 Y 0 Q B 15 #` are pointless → **can't say**. So that envelope is a separate branch, not the gateway to SalPhaseIon, and it is still unsolved. The "can't say" also stops anyone from writing off the Norton line and the X/Y strip. | 0 |
| 3 | **Colour cluster**: #17891 "Have you tried the purple pill already?", #17893 "Candy flipping into 2024 ;-)", #49175 "Yes" (the rabbit has a carrot) and #49176 "Carrots were originally purple, until the Dutch turned them orange", and #6250 **"Infrared"** replying to *"xor black, white, yellow, blue? … or sum for red"* | Purple = red + blue and orange = red + yellow. These are *mixed* colours from the poem's colours ("Roses are White but often Red / Yellow has a number and so does Blue"). "Infrared" answers a question about how to combine the colours. "Candy flipping" is a combination of two substances, i.e. two things mixed. Together they suggest the colour channels are **combined** (a sum or overlay), not only read as separate markers. The review covers only separate yellow/blue marker models. | 0 |
| 4 | **#66564 "I don't know right now."** (to Jerry #66562) | Jerry's claim checks out exactly. DBBI (91) + FAED (570) = **661, and 661 is itself the 121st prime**. Taking the 1-indexed prime positions gives exactly 121 = 11×11 characters. There are 30 primes ≤ 121, and 121 − 30 = 91, the DBBI length. The creator neither confirms nor denies this, which is unusual for him (he normally says "coincidence" or "no"). | 0 |
| 5 | **#70307 "Pfff. Coincidence."** (to Diego #70303) | In YOUWON, positions {1,4,21} → VIC. The digits right of YOUWON number exactly **103**, equal to the length of the SalPhaseIon instruction string; the digit string is `2431611237214124471074211414221316122016161124131025122622123518414242545191121152243113224101217201971`. Diego replied #70318: "Yellow BLUE primes = DEL FE — Coincidence?" (no answer). "Pfff" reads as dismissive but is ambiguous. VIC is already covered; the 103-digit equality is not. | partial |
| 6 | **#7830 / #7832 / #7834** | The key is stored online ("Technically we do"), and "the solver will find a way to **'decrypt'** it". The quoted word suggests something other than a plain AES/openssl decrypt. | 0 |
| 7 | **Forward-only: "1 private key is hidden in there."** and **"Equivalent of 25 btc" / "Depends how you look at it."** | The first is a direct statement that a single raw private key is embedded somewhere, consistent with the 64-hex plaintext expectation (#69276). The second: the prize value "depends how you look at it". | 0 |
| 8 | **Forward-only: April 2026 farewell letter** | Names JRK, d0d, Darky, Bloctite and Greengras; Sydney 2017; MR. ROIbot; the first Poloniex order on 10 June ~08:30; the scammer "fuzzyhobbit"; "Globally Supporting My Generation" reused from an old friend's group name; the puzzle built in "two sloppy days". Read with #66573/#66574 ("My close friends have the best chance… **NOTE: that is a hint**"), this is the only published material that "close friends" would know. The review analysed the hint but not the letter. | 0 (Sydney/fuzzyhobbit) |

## 2. Lower-signal items worth keeping on the list

- #4589: the 2.5 BTC half is "Or the same puzzle, or just not at all". #5071: "maybe even in the same block". Both suggest the half and the better half share one container.
- #60324 "episode 3.5 with the better half": plausibly *Mr. Robot* `eps3.5_kill-process.inc` (the review declined to name the series).
- #32671 "You only need the last number of pi and it might get you somewhere" (sarcasm is likely).
- #4105 "First or zero": the index base question.
- #3342 "there are errors?": three artifact lines in the mp3.
- #66903: the laptop is "in a room with a hidden door".
- #66600: "Some already found it. And understood not to risk it".
- #53342 binary New Year "tiny hint" after the dot sequence `. .. ... .... .....` (triangular numbers 1–5 = 15).
- #8318 (barrystyle, after the Cosmic Duality cover): "-nopad suppresses any errors". This matches the IV/padding gate issue.
- Creator text has **no hidden formatting** (no text_link or spoiler entities).

## 3. Offline tests run on these leads (no network, gsmg.io untouched)

Targets were `1st_half.bin` (b45a…), `2nd_half_correct.bin` (SalPhaseIon, 3ab5…) and `cosmicblob.bin` (2d3f…). KDFs: EVP_BytesToKey with MD5, SHA-256 and SHA-1. Passwords were tried raw, as sha256hex (lower and upper) and as double sha256hex. The gate is IV-independent: the key-only final block must have valid padding, plus a 64-hex body or >90% printable text. It passes its self-test with a deliberately wrong IV.

| Script | Material | Decryptions | Result |
|---|---|---:|---|
| `scratch_gsmg/lead_test_0912.py` | *Looking Forward* / Fresco / Keyes / Venus Project phrases, colour words, Norton, farewell-letter names, Decentraland coords, "yourself", self-keyed blob/salt/ct/b64 material, and all ordered pairs | 235,620 | 0 hits |
| `scratch_gsmg/jerry11.py` | Jerry's 121 prime-position characters (index bases 0 and 1), both orders `abcdefghi` and `dbifhcega`, 11×11 row/column/diagonal sums, boustrophedon, 4 serialisations, ± instruction suffix | 22,176 | 0 hits |

These negatives rule out only the literal phrases. They do not rule out the leads: *Looking Forward* most likely acts as a **source text** (a selector for "last words" or a book cipher), which needs the book's text and is not a password in itself.

## 4. Suggested next moves

1. Get the text of *Looking Forward* (1969). Test it as the "last words before archi choice" source and as the book behind "in front of your eyes". Look for its chapter headings, its final words, and any passage on "choice".
2. Treat `1st_half.bin` as its own branch (#8569). Candidate inputs are the Norton / X-Y strip material the creator refused to dismiss.
3. Build colour-*mixing* models for the poster: red+blue = purple and red+yellow = orange, as channel sums, instead of separate yellow/blue markers.
4. Carry Jerry's 11×11 selection and the 103-digit YOUWON tail forward as matrix inputs (not passwords) into the `matrixsumlist` step.
