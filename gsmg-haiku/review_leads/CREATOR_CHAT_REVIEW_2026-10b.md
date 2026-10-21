# Creator chat review, second pass (2026-10-08)

Scope (corrected 2026-10-09): 819 selected entries: 492 direct creator-account messages and 327 forwards attributed to that account in the Telegram export (2019-04-20 to 2026-09-23), extracted to `scratchpad/creator_posts.tsv`. Rows 1–420 were read in the earlier pass; rows 421–819 (2024-11-22 to 2026-09-23) were read in this pass. Decodes were done locally in Python. The chat pass itself made no chain queries. Chain queries were run later the same day, read-only, and are recorded in section 6. No links from the chat were opened.

## Provenance correction (2026-10-09)

The 819 entries are not 819 distinct original creator messages. The recovered
`creator_posts.tsv` IDs were matched to the committed Telegram export: 492 have
`from = Jrk Bgrt` and no forward marker; 327 have `forwarded_from = Jrk Bgrt`.
The selected IDs and source-file hash are in `evidence/creator_selection_ids.json`.
Forward/repost timestamps date the copies, not new clues or new wording.

The source kit identified in the review at commit
`00bc7b003140399d6d9a85aa3f7c91ce70a80a7a` contains these earlier records in
`jrk_messages.txt`. Exact local excerpts and the local file hash are preserved in
[evidence/creator_provenance.txt](evidence/creator_provenance.txt); the local kit
is an unpacked archive, so its commit identity is supplied by the review.

| Original message | Message date | Latest recorded edit | Wording in export |
|---|---|---|---|
| #991 | 2019-05-31 | none shown | folks found a new piece |
| #1487 | 2019-09-26 | 2025-04-30 | piece outside the main puzzle |
| #6250 | 2021-03-05 | 2025-09-08 | Infrared |
| #6884 | 2021-04-01 | 2025-02-02 | another door ... {1},{4},{21} |

For edited messages, the original timestamp does not establish when the current
wording first appeared. No edit history is available. Recent forwards establish
neither fresh clue dates nor the existence of a still-undiscovered artifact.

The braces in #6884 plausibly denote the calendar date 1 April 2021 and/or an
April Fools joke. Nearby #6895 recognizes the solver's #6891 {30},{2},{77}
parody as a Cyberpunk joke. This is contextual support, not proof that #6884 has
no other meaning. The archived R/A/B screenshot does not contain the braces clue.

## 1. Decodes that were checked

| message (id, date) | encoding | result | status |
|---|---|---|---|
| 34003, 2024-12-12, a forward posted by nieods of creator message #8446 (2023-02-23; identical 1,288 bits) (also reposted 2024-12-26 and later) | 8-bit bytes, each byte bit-reversed, whole string reversed | `yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyangwewontgiveawaythepassworditsinfrontofyoureyesbutyourenotseeingitverylaststepisatruegiveawaypromised` | Reproduces. Same text is already in `naddiseo_readme.md` and `issues/puzzlehunt_106.md`. Not new. |
| 45917, 2025-07-23 ("Here is the GSMG Puzzle!") | 8-bit bytes, plain | `?TNIH_DN2_EHT_SI_C_REBMUN_EHT_DNA_TLUAFED_SI_31_FI_TAHW_DNA?SEGASSEM_SIH_DNES_RASEAC_DID_WOH|` followed by a Caesar-encoded line and a bit tail | Reversed, the first two parts read "HOW DID CAESAR SEND HIS MESSAGE?" and "AND WHAT IF 13 IS DEFAULT AND THE NUMBER C IS THE 2ND HINT?". |
| 45917 (Caesar line) | shift −3 | `removethecorrecthinttoproceedtothenextstage` | Instruction text, no new value. |
| 45917 (376-bit tail) | per-byte bit reversal, then string reversal, then base64 | Decodes to `youtube.com/watch?v=dQw4w9WgXcQ` | This is the standard rickroll link. Not opened. It matches the creator's own 2026-07-12 remark: "The rickroll effect inspired me to make an actual puzzle". Joke, not a route. |
| 50656 (2025-10-16) and 71627 (2026-09-12) | hex | `Surebutwewontgiveitaway` | Echoes the "we won't give away the password" line in 34003. No new value. |
| 53342 (2025-12-31) and 57106 (2026-01-14) | 8-bit ASCII | `Happy new year! Make the best of everything. Oh, and here's a "tiny hint" <3.` | Season greeting. The early-2020 hint wording appears in later forwards; their 2025 copy dates do not date the original promise. |

Key point: the "esrever ... use that hint on the 2nd binary code" post (2025-08-20, id 47269) means reverse. Applying that to the 2024-12-12 post gives the real hint text, and applying it to the 2025-07-23 post gives the rickroll link. So the "2nd binary code" chain ends in a joke.

## 2. Candidate clues: status after this pass

| # | clue (date, id) | what was checked | status |
|---|---|---|---|
| a | "another door might be found on {1},{4},{21}" (2021-04-01 02:57, id 6884; reposted 2025-10-15, id 50450) and "R=18 / A=1 / B=2 / Could also be 21 or 1812 bit" (2021-04-01 09:29 post; image `hints/2021-04-01-april fool.png`) | R=18, A=1, B=2 are the correct alphabet positions. Read 1-based, {1},{4},{21} give **A, D, U**. Read 0-based, they give B, E, V. Positional characters at 1, 4, 21 of `lastwordsbeforearchichoice` (l, t, c), `matrixsumlist` (m, r), `yellowblueprimes` (y, l), `yinyang` (y, y), `thispassword` (t, s), `ourfirsthintisyourlastcommand` (o, f, s), and of the poem read as words (Roses, but, piece) give no coherent reading. | **Unresolved.** Calendar/April Fools is plausible given #6884 and #6895; no proved exclusion follows. The positional readings did not identify a usable value. The April 1 image has the R/A/B line but not the {1},{4},{21} line. |
| b | "2nd door" / "price is in half" (2020-05-11; reposted 2024-12-08, 2026-01-09, 2026-05-21) | 2026-05-21 forward (#63497) of creator message #5069 (2020-11-24): "We have our reasons halving the price money at every bitcoin halving event". Corrected 2026-10-14: earlier text called this a 2026 creator post. | Already known. Schedule and framing only. |
| c | "nobody managed to find the extra door" (2024-12-08, 2026-01-22) and "one team managed to find something ... others haven't yet found (unless they didn't tell us)" (2026-01-14, id 57098, forwarded) | Forwarded group statement; the team and the something are not named. | Forwarded claim; original chronology must be checked before treating it as new. No route or undiscovered artifact is established. |
| d | Jacque Fresco (2024-09-19 post; 2026-03-03, id 60298: "Jacque was quite an inspiring lad") | Consistent with the existing Venus Project / phase 3.2 lead in `naddiseo_readme.md`. | No new content. |
| e | "I know a Matthew, and if he knows a Roberto ..." (2024-10-21) | Earlier rows; not re-checked in this pass. | Still open. |
| f | "Checked the script for you today. It's possible. ... I forgot the last details on how to solve it exactly" (2025-12-02, id 51939, forwarded) | The creator says he no longer remembers the solve path. | Consistent with the closing post (see 3). |
| g | "1 private key is hidden in there" / "Equivalent of 25 btc" (repeated 2025-04-21/22, 2025-08-05, 2026-07-13, 2026-08-12) | Repeated forwards, followed by canned-looking replies ("Hi there, welcome", "Si", "Correct", "Depends how you look at it"). | Repeat only. |
| h | Typos: "giveit = givetit" (2025-08-16, id 47145) and the creator's answer "No clues to be found in those typos" (id 47146); "A. I rushed (t)it." (2026-09-01, id 70311) | The creator says typos are not clues. | Closed. |
| i | "Infrared" (#6250, 2021-03-05; edited 2025-09-08; later copies 57229 and 61423) | Older source located; first appearance of edited wording unknown. | Interpretation and dataset remain unverified; recent forwards are not new clues. |
| j | "piece outside the main puzzle" (#1487, 2019-09-26; edited 2025-04-30) and "folks found a new piece" (#991, 2019-05-31) | Earlier source records located; 51282 and 49794 are later copies. | The referenced piece is unidentified here. These statements do not prove an undiscovered artifact or a new 2025 clue. |
| k | "Only -41,-17 matters" (2026-04-04, id 61269, forwarded) | Repeats the 2020-02-20 Decentraland hint (`naddiseo_readme.md:212`, linked notebook `decentraland.ipynb`). The notebook was not re-run here. | Repeat. Already covered in the project. |
| l | "1357 blocks to go" (2025-10-20, id 50752; 2026-05-04, id 62445) | Same number on two dates. Not matched to a block height in this pass. | Unexplained. Probably a repeated countdown. |

## 3. New context (not clues)

- **Closing post (2026-04-13, ids 61385–61386, forwarded from the GSMG group account):** the group says it is shutting down. The code is kept and may be open-sourced or sold. The puzzle is "still unsolved", the group will not give hints, and it hopes the puzzle stays "community-maintained, as the URL might vanish". The post also says the creator "might admit he forgot how to solve it himself" in 40 years. This is a group statement, not a creator-account message, so treat it as unverified.
- **2026-07-12 creator remarks:** "I held quite a secret in my head ... for those who can understand what I meant" (id 66592); "The '5' btc was never the actual prize" (ids 66593, 71913, 73195); "Some already found it. And understood not to risk it" (id 66600). These are statements of intent with no route attached.
- **2026-08-17 creator (forwarded, ids 68905–68906):** "my friends and family can get to all my data if they'd work together". Adds to the laptop thread in `HIDDEN_LAPTOP_DOOR_TRACE.md`; still no file, passphrase, or location.
- **2026-08-25 (forwarded, id 69872):** "I'll offer free hints in PM. (After you've paid me 5.1 btc)". Joke, but it matches the paid-hint scam pattern the project already warns about. Do not pay anyone for hints.
- **2026-06-18 Dutch replies (ids 65533–65535, forwarded, author not identified):** "there is actually a private key to be found" and "you have to come from good houses; it's not lying around". Community noise, not creator.
- **Mr. Robot references (2026-05-21, id 63499; 2026-03-03 and 2026-05-24 "episode 3.5"):** the creator's wish that "the last scene of mr. Robot becomes a reality". Not tested; no concrete pointer.
- **Repeated forwards** of the same hint blocks ("At least prime number...", "There is / Another / D / O / O / R", "Roses are White...", "Regular Bitcoin Private key", "a private key") do not change the timeline.

## 4. What this pass changes

- No new key, address, file, or dataset came out of rows 421–819.
- The 2025-07-23 "binary" post is a rickroll with a Caesar line. It is not a second route. Recorded so it is not re-opened.
- The 2024-12-12 binary post is confirmed to decode to the known creator hint text. It is not new.
- Interpretive questions (not evidence of new clues): (1) the "piece outside the main puzzle" line (j), whose older source is now located but referent remains uncertain; (2) "Infrared" (i), if a dataset is later named; (3) the {1},{4},{21} line (a), for which calendar/April Fools and positional readings remain possibilities; (4) the Matthew/Roberto line (e), from rows before 421, not re-checked here.

## 5. Not done

- No link from the chat was opened, including the rickroll link and the Hugging Face link (`CoruNethron/openssl-for-restless-souls`) from `CHECKPOINT_4F7A_VS_A5502.md`.
- Decentraland `-41,-17` was not re-run (`decentraland.ipynb`).
- No chain queries; the "1357 blocks" countdown is not matched to a height.

## 6. Chain work done the same day (added after this pass)

The chain checks below were run after the chat pass above. They are read-only. They do not change any finding in sections 1–4.

- **BSV history of the target address:** six transactions, with the 1 BSV at `7ea6eb76…` (block 968354) traced backward through a relay hub. Recovered local script evidence and the limits of the unlogged decoding-attempt claims are in [BSV_FUNDING_TRACE.md](BSV_FUNDING_TRACE.md). The May 2025 records contain `SLP\0` / `SEND` markers; protocol identification alone does not rule out a puzzle-related message.
- **Litecoin / BTC brainwallet scan:** partial. 257 of 2,176 addresses checked from 544 phrases. No match to the target. Four BTC addresses from common-word brainwallets (`BITCOIN`, `BTC`, `Bitcoin` x2) had history; none is linked to the target. Details in [LTC_SCAN_2026-10-08.md](LTC_SCAN_2026-10-08.md).
- **Relation to the chat:** no exclusive creator attribution follows. The BSV payment uses a publicly derivable checkpoint (verified in recovered local records). The numeric `9325` and `1133` tags correspond to Memo Send money and Like/tip, and the LTC scan phrases are creator hint words already decoded in the project (for example `yellow`, `blue`, `primes`, `matrixsumlist`, `archichoice`, `yinyang`, the "removethecorrecthinttoproceedtothenextstage" instruction, and the rickroll string) plus generic coin words (`btc`, `ltc`, `bitcoin`). No new creator text was used.
