# Doc 117: the Telegram export mined

26 September 2026. Doc 116 put the export in the repository and verified the dossier
against it. This session mines it: every field the export carries that earlier
sessions did not use, every string it contains against the win test and the three
locks, and the on-chain record the chat keeps pointing at. Harness: doc 115's
(`claude/scripts/115/`), seeded planted controls on every run, both fired every time.

Result: **null throughout.** No key, no container, no new creator statement that
changes sections 9 to 12 of the dossier. What the session settles is listed in
section 5 so it is not re-proposed.

## 1. Fields the export carries that no session had used

**Reactions.** The export records emoji reactions, with the last three reactors per
emoji. The creator (`user9815232`) appears as a reactor 29 times (a lower bound,
since only the three most recent reactors are listed). Every one is social: laughing
at "my entire city lost power" (#17792), a thumbs-up to "let jrk be alone" (#23612),
❤ to a thank-you (#29002), 😁 to "42" thrown into a darts joke (#66468), 🥴 to "the
hole..." said about drugs (#66607), 🌚 to a question about neural networks versus the
2028 halving (#66915). None sits on a puzzle claim. The endorsement method in section
8.1 of the dossier (reply link, else nearest preceding message) is not extended by
reactions.

**The "edited" stamps are reaction artifacts.** 123 creator messages carry an edit
date years after posting, in monotone runs (dozens of 2019 to 2020 messages stamped
2025-04-30 18:44 to 19:12 in id order). Across the whole export, 343 of the late
stamps equal a listed reaction's timestamp to the second, 39 are within a second or
reflect a reaction since removed, and the rest have no surviving reaction. Telegram
Desktop writes a reaction as an edit. **The creator has not retro-edited his
messages**; #1710 (the Roses poem, "edited 2024-04-24") and #8446 ("edited
2023-12-02") are reactions, not text changes.

**Media.** The creator posted 18 media items: one photo of a dessert (#1647), one
screenshot with 😎 (#1743, 1280 x 749), one photo captioned "Nice" (#66964), two
stickers, and 13 GIFs whose file names are the only content the export keeps:
`giphy.mp4` (the halving day, #3860), `who-wants-to-be-a-millionaire-wwtbam.mp4`,
`confront-interrogate.mp4` and `what-if-i-told-you-what-if.mp4` (#8792, #8793, the
"Are you really looking for just the btc...?" exchange), `tumbleweed.mp4`,
`the-train.mp4`, `matrix-merowinger-aktion-reaktion.mp4` (#32561, the Merovingian's
causality scene), `forrest-gump-wave.mp4`, `happy-carrot.mp4` (#49172, then "Carrots
were originally purple"). The files themselves are not in the export. No forwards,
no polls, no pinned messages, five links (a sha256 generator, `Gsmg.io/puzzle`, the
prize address on blockchain.com, two halving countdowns).

**Timing.** 65 of the 492 creator messages land in seconds :00 to :05 of a minute
against 49 expected. Both binary hints were posted at hh:20:03 (#8446 at 18:20:03,
#53342 at 22:20:03) and the five dot messages before #53342 at 22:15:02, 22:16:15,
22:17:05, 22:18:07, 22:19:05, which is what scheduled sends look like. He schedules
his hints; the seconds carry nothing.

## 2. Creator lines the hint catalogue does not carry

Found by listing every short creator endorsement with its parent (section 8.1's
method, run over all 492 messages). None changes a reading; recorded so they need
not be re-found.

| id | creator | parent | note |
|---|---|---|---|
| #3615 👆 | reply to #3613 "let me guess: because it's unknown?" | #3612 (Legik, joking): "you'll never finish the last task" | agreeing that the last task is unknown to everyone; not a hint |
| #6944 👆 | reply to #6943 "Probably best to start at the beginning to understand the mindset behind it" | a newcomer's question | endorses reading the chain from the start |
| #8352 | "I checked a certain GitHub yesterday, for whoever set that up, nicely done. You guys are really getting close." (12 Jan 2023) | | the puzzlehunt GitHub; "close" before #8446 |
| #8368 👆 | reply to #8367 "Who knows..." | #8365 on whether the remaining 2.5 BTC is the prize | |
| #8569 | "Correct. / - / No. / - / Can't say anything about this." | #8566 (3.2 not totally solved, the Terminal undecrypted), #8567 (maybe the SalPhaseIon hint is in there), #8568 (Norton's theorem pointless; the phase-2 `# X 2 S H 4 Y 0 Q B 15 #` line not useful) | the dossier reads the third part as answering the header (section 3.2); the three answers map to the three messages in order: the Terminal is undecrypted (Correct), the SalPhaseIon hint is not in it (No), the phase-2 line (can't say) |
| #9551 | "Oh, and be careful of what you get yourselves into. 🤐" (6 Aug 2023) | follows "This may sound a little dramatic but if I suddenly can't answer you guys anymore" (#9550) | the 2023 "obscure intel" thread, section 8.4 |
| #17893 | "Candy flipping into 2024 ;-)" | | doc 116 correction |
| #32715 | "Blueprint is sort of the leading list at this point." | #32714 "Maybe qbsh is actually a list of supplements!" | Bryan Johnson's supplement list; a joke |

The #8569 mapping is new: if the three dashes answer #8566, #8567 and #8568 in order,
"No" says the SalPhaseIon hint is **not** hidden in the Terminal, which sits beside
#2918 ("There must at least be something hidden in there") without contradiction: the
Terminal holds something, and that something is not the SalPhaseIon hint.

## 3. The on-chain record, fetched and closed

The chat returns to the chain every few months. The prize address's full history was
paged from mempool.space (about 125 transactions) so the question is answered from
the record rather than from chat claims.

- **Funding.** 2019-04-13, block 571,497, 5 BTC from `1EtbTvVB8QTGN4mduSdy7n4cZQm4iYTpQ1`
  (seven inputs, nLockTime 571,496). The creator's funding wallet; nothing else from it
  touches the puzzle.
- **The two halving spends** are as the dossier records them (blocks 630,001 and
  840,725, nLockTime 629,998 and 840,003).
- **`3GSMG24TujqfMJG1kQoBX18DzJHQLeJYMK`.** A P2SH vanity address that paid 700 sat to
  the prize address with `OP_RETURN "Halving"` in block 630,001, the same block as
  the first halving spend (nLockTime 0, so broadcast on seeing the spend). It later
  dusted the secp256k1 "neighbours" of the prize point (the point halved, doubled,
  plus and minus one; #52598, #63358), which anyone can compute from the exposed
  public key. The creator said it is not his (#36205, #63360); a chat member recovered
  private keys to some of its brain-wallet targets (#36204). **Fan fiction, as the
  chat concluded.** Not a creator channel.
- **Third-party OP_RETURN dust, 2025 to 2026**, all from unrelated wallets: "Turing
  Complete.", "Causality Transcended", "From Neo", "The answer is women", "If I were
  you, I'd hope we dont meet again.", "EW There is no spoon", "Happy late mothers
  day!", "HALVING", "#SOLUTION", `false || echo "5 BTC"`, "happy xmas! :P Everything
  That Has A Beginnin Has An End", `FromN0EHalfABetterHalfBuiltItBellaCiao1_1Pi36y7...`
  (from a vanity `1Pi36y7...`), `844e86a69a04eea672049e0e0e8612`, a symbol string
  from `3JC6NJz2vXZ8...`, and the two dust bots' batches of 24 February 2026
  (`SalPhaseIon`, `ALPHANOISES`, `THEMATRIXHASYOU`, `There is no spoon`, `iamtheone`,
  `entertherabbithole`, `redpill`, `fanstoo`, `leavethematrix`, `yourlastcommand`,
  `secondanswer`, `isolveditwithanabacus`, `hereismysecret`,
  `fourfirsthintisyourlastcommand`, `matrixsumlistenterlastwordsbeforearchichoicethispassword`,
  the Saint-Exupery line in three cuts, and a `bc1q...` address), plus
  `GSMG WITNESS BLK 949653 TX 808f812f` (May 2026). The full table (81 OP_RETURN
  outputs across the address's 127 transactions, with txid, script and data hex) is
  checked in as `claude/scripts/telegram/opret.tsv`, and the sweep builds its string
  list from that file rather than from a typed list (added after review: the typed list
  had missed eight strings, among them the three `...bc1q...` concatenations and the
  2025 lines "EW There is no spoon", "Happy late mothers day!" and "If I were you, I'd
  hope we dont meet again."). Every string, every case and spacing form, and every
  ordered pair, self-pairs included: **13,797 candidates, null.**
- The "Good job Neo" transactions a 2020 message asks about (#4652) are not on the
  prize address; the only pre-halving inbound besides the funding is 666 sat in block
  622,713 with no OP_RETURN.

## 4. Every string in the chat against the locks

`claude/scripts/telegram/sweep.py` and `sweep_extra.py`. Harness as doc 115: win test
on both point forms plus the double-hash paths, all three containers under four
password profiles (sha256 hex, raw, double sha256 hex, sha256 of the hex) and both EVP
digests, padding then the structure-agnostic recogniser. One planted container and one
planted key target per family, seeded; every control fired.

| family | what | candidates | decrypts | valid pads (expected) | result |
|---|---|---:|---:|---:|---|
| scalars | every 64-hex string (192) and every WIF (47) posted in chat, as a raw private key | 239 | | | 0 (control fired) |
| keyish | every 32+ hex, base64-ish, URL and address token as password text | 2,750 | 88,000 | 374 (344) | 0 |
| tokens | every whitespace token, original and lowercase, punctuation-stripped | 82,691 | 2,646,112 | 10,408 (10,336) | 0 |
| lines | every line and every whole message, original and lowercase | 125,368 | 4,011,776 | 15,925 (15,671) | 0 |
| ngrams | every 2-, 3- and 4-gram inside a message, spaced and joined, both cases | 3,501,970 | 112,063,040 | 439,440 (437,746) | 11 flags, all chance (below) |
| cjoins | 2- to 6-grams across runs of consecutive creator messages within 15 minutes, and each run joined | 56,949 | 1,822,368 | 7,148 (7,119) | 0 |
| pairs | each short creator endorsement's parent text, alone and joined with the reply | 2,539 | 81,248 | 327 (317) | 0 |
| opret | every OP_RETURN string on the prize address (`opret.tsv`) plus the reader's cuts, alone and in ordered pairs, self-pairs included | 13,797 | 441,504 | 1,815 (1,725) | 0 |

Valid-pad counts sit at the 1-in-256 chance rate in every family, which is the
liveness check. The only flags outside the planted controls are the n-gram family's
11, and each was re-derived and read: seven pad-3 events (6.7 expected at 1 in 2^24
per decrypt), three plaintexts opening with the gzip magic `1f 8b` that gzip refuses
("Unknown compression method"; 6.7 expected over 439,440 valid pads), and one
distinct-byte-count flag on Cosmic Duality. All eleven are 34% to 42% printable
random bytes, the noise floor. No key window, no readable plaintext, no EBCDIC, no
bit bias.

The 47 WIFs are keys other people posted (their own, or brute-force finds of
brain wallets); none controls the prize or the sentinel. The 192 hex strings are
mostly sha256 digests of chain answers (`causality` 25 times, the phase-1 hash 33
times) and transaction ids.

## 5. Settled by this session

- The export's reactions, edits, media, forwards, links, pins and timestamps carry no
  puzzle content beyond the text already catalogued.
- Nothing typed into the chat in seven years, alone or in any 2- to 4-word window,
  opens a lock or is the key. If the password was ever posted, it was not posted as a
  contiguous string of up to four tokens or as a whole line.
- The on-chain record contains no creator message. `3GSMG...` is a third party.
- Four creator lines were uncatalogued (#3615, #6944, #8352, #9551); none is a hint.
  #8569's three answers map to three messages; "No" says the SalPhaseIon hint is not
  in the Terminal.

The wall stands where doc 114 left it: `matrixsumlist` and
`lastwordsbeforearchichoice` are operations whose operands lie outside every text the
project holds, the chat included.
