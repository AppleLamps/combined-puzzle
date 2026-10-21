# 01 — Proven chain (reproduced from originals)

Everything in this file is **re-verified** by `tools/verify_chain.py` from files in `originals/`.
Last run: 2026-09-13, result `ALL CHECKS PASSED` (log: `data/verify_log.txt`).

Anything that is *not* re-derived here is labeled `[source: …]` and was reproduced in an earlier round but is not re-run by this folder's scripts.

---

## 0. Encryption convention (proven on 3 envelopes)

| Item | Value |
|---|---|
| Container | OpenSSL `Salted__` + 8-byte salt + ciphertext (base64) |
| Password | `sha256(answer)` written as **64 lowercase hex ASCII** |
| KDF | legacy `EVP_BytesToKey`, **md = SHA-256**, 1 iteration (not MD5, not PBKDF2) |
| Cipher | AES-256-CBC, PKCS#7 padding |

- Equivalent command: `echo <b64> | openssl enc -d -aes-256-cbc -a -md sha256 -pass pass:<sha256hex>`
- Random wrong keys pass a PKCS#7 check about 1 time in 255 (mostly pad = 1). A pad-1 "success" is **not** evidence.
- A 5-block envelope (80 B ciphertext) holding exactly 64 B would end in 16 × `0x10`. Chance of that by accident is 2^-128. But the plaintext length is not known: anything from 64 to 79 B fits.

---

## 1. Poster → URL

- File: `originals/poster/puzzle.png`
  - sha256 `38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830`
  - 29,931 B, 1048×1556
  - Byte-identical to the Wayback 2020-11-12 capture and to the live `/puzzle` `[source: v2 Add.1, gemini]`
- Method:
  - Grid is 14×14 cells of 75 px, read as an **inward counter-clockwise spiral from the top-left** (down, right, up, left).
  - Black and blue cells = 1; white, yellow and the one `#fefefe` cell = 0.
  - Take 8 bits per character over the first 192 cells.
- Result: **`gsmg.io/theseedisplanted`** ✅
- Coloured cells in spiral order: `BBBBYBBBYYBBBBYBBYYBYYBY`, i.e. 15 blue and 9 yellow ✅
  - Every coloured cell sits on bit 7 of its character, so blue means the character's code is odd.
  - The low bits spell `F73D92`, which is redundant with the URL.
- Census: black 86, white 85, blue 15, yellow 9, off-white `#fefefe` 1 `[source: v2 Add.23]`
  - The `#fefefe` cell is at row 7, col 4 (0-based), which is **spiral index 163** (0-based).
  - It holds bit 3 of byte 20, the `n` of "planted". Flipping it gives `…pla~ted`.
- The 4 centre cells (spiral 192–195) are surplus: 196 − 192 = 4. The rabbit drawing covers 7 cells.
- The QR code is a stock encoding of `https://www.blockchain.com/btc/address/1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`.
  - All Reed-Solomon syndromes are 0.
  - No stego was found in the poster, the grid crop or the 8 rebus tiles `[source: v2 Add.22, gemini]`.

## 2. Phase 1 (seed page rebus)

- Page: `originals/pages/theseedisplanted.html`; rebus tiles are in `originals/rebus/`.
- Answer: **`theflowerblossomsthroughwhatseemstobeaconcretesurface`**
  - sha256 = `5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75` ✅
  - The creator posted this hash in Telegram (#225/#226, 2019-04-22: "just try hit your options against that hash").
- The site accepts it with a POST to `/phase1verification` and redirects to `/choiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecialdessertiwroteitmyself` `[source: gemini Add.40]`.

## 3. Phase 2

- Page: `originals/pages/phase2_choice.html`, textarea 1.
- Salt `06286612d43ed7ed`, 656 B ciphertext.
- Answer **`causality`**; password `eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf`.
- Plaintext: 648 B, CRLF, sha256 `e2f9dd65604a3231f8b3301724e8d713a88fffc4b6c7c4aeeb20f58a582b593a` ✅
  - Saved as `data/phase2_plaintext.bin`.
  - Contains the `# X 2 S H 4 Y 0 Q B 15 #` block and ends "Ok kid, on the highway, let put it in the worst gear."

## 4. Phase 3 (seven-part password)

- Page: `originals/pages/phase2_choice.html`, textarea 2.
- Salt `9fbc451d13d071f4`, 4,096 B ciphertext.
- The answer is the plain concatenation of 7 parts (`data/seven_part_phase3_answer.json`):
  1. `causality`
  2. `Safenet`
  3. `Luna`
  4. `HSM`
  5. `11110` (Executive Order 11110)
  6. `0x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854`
     - This is the Bitcoin genesis message, byte-reversed as in Satoshi's main.cpp line 1616.
     - It reverses to "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks" ✅
     - `0x` + 138 hex characters = 140 characters, the Architect text's "HUNDRED FOURTY" `[interpretation]`.
  7. `B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1`
     - The position **after** White's move. The page shows `…/6R1/… w - - 0 1`.
- Password = `1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5`.
- Plaintext: **4,090 B**, sha256 `c4ad94559a44a927c1032cc0e024515f9510a0806a2d14458dbf4a360af9865f` ✅ (`data/phase3_plaintext.bin`)
  - Layout: riddles (726 B), then the base64 Phase 3.2 envelope.

## 5. Phase 3.2

- The envelope is embedded in the Phase 3 plaintext.
- Salt `eefc4c5befc1656a`, 2,432 B ciphertext.
- Answer **`jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple`** (spelled `giveit`, not `givetit`)
  - Password `250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c`.
- Plaintext: **2,422 B**, pad 10, sha256 `b82afeb86f9e50848220f9b64b744b821400308aea273a1c949b9d2d0e408a34` ✅ (`data/phase3_2_plaintext.bin`)
- Only ~60% of it is printable (a strict 0x20–0x7E count in one run gave 29.11%; the definition differs). Any sweep that filters for "printable" plaintext would have thrown away this correct result.

Sections of the plaintext (byte offsets vary by ±4 between rounds, depending on whether the CRLFs are counted):

| Bytes | Content |
|---|---|
| 0–~446 | ASCII intro "I've been waiting for you…", including "Wake up, you… I've designed you a beautiful strategic position. **One for one, four for one.**" |
| 447–1985 | EBCDIC letters (see 5a) |
| 1990–2138 | 149 digits (see 5b) |
| ~2143–2291 | "Raising the stakes without extra chances of winning. A fubcd-king & oracle-queen, thingky mvps, on a sad board but as wide as the first one seen" |
| 2292–end | **Locked terminal envelope** (see §8) |

### 5a. Architect text
- Take bytes `[447:1986)`, read them as latin-1, re-encode to **cp273** (cp1141 is the same table plus the euro sign), then Beaufort-decrypt with key **`THEMATRIXHASYOU`**.
- Result: **1,539 letters**, a rewritten Matrix Reloaded Architect speech ✅ (`data/architect_letters_1539.txt`)
- Letters-only index **479** (0-based) starts `PRIVATEKEYYOUVEEARNEDITBUTPLEASE…` ✅
  - `PRIVATEKEY` occurs at [479, 1238].
  - Under the other compaction (whitespace-stripped, 1,544 characters, which keeps apostrophes and a hyphen), the same spot is index 480. Always use the letters-only form.
- `REINSERTINGTHEPRIMEBASICS` is one candidate referent for the words before the Architect's choice; the intended choice/referent is not proven (09 §2; 10).
- Changes compared with the film `[source: v2 Add.33, r1; corrected 2026-09-13 against the transcript]`:
  - "the One" → THE YOU; "the source" → THE SOURCE CODES; "the prime program" → THE PRIME **BASICS**.
  - "select from the matrix 23 individuals, 16 female 7 male" → SELECT FROM **OVER** TWENTY THREE **CIPHERS** SIXTEEN **ENCRYPTIONS AND/OR** SEVEN **INTERTWINED PASSWORDS**. The numbers 23 / 16 / 7 are the film's; the nouns are new.
  - Added: HOPEFULLY, ACTUAL PRIVATE KEY, BRUTE FORCING MIGHT BE REQUIRED, WISE MAN ABOVE … HUNDRED FOURTY, CIAO BELLA.
  - **Not** added: UNBALANCED EQUATION is in the film ("a remainder of an unbalanced equation") and is kept in the puzzle text.
  - Removed: the film says "choice" 5 times; the 1,539-letter puzzle text contains **no** `CHOICE`. So "last words before archi choice" cannot point to a literal CHOICE in this text (offset notes: 06 §6).
- The film transcript for diffing is `reference_texts/matrix_reloaded_architect_scene_transcript.txt`.

### 5b. Straddling checkerboard
- Digits: `15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112`
- Key `FUBCDORA.LETHINGKYMVPS/JQZXW`, with rows 1 and 4 left blank in the top line (straddles). The hint sentence spells it out: "fubcd-king & oracle-queen, thingky mvps".
  - The 149 digits never use cell 10 or cells 44–49, so the key tail `. / J Q Z X W` is **assumed**, not proven. Some copies have a dot instead of `/`; both decode identically.
- Result (91 letters) ✅: **`INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE`**

## 6. SalPhaseIon (side door from the poster)

- Instruction: `HASHTHETEXT`.
  - It is read from the spectrogram of the Decentraland parcel audio (−41,−17; `puzzlepiece.mp3` sha256 `ef17a96dce37b4dd7cbf79f210c5cbaf37fcae60e5faf8004de4e0832bd0dfee`). The signal is in the **left − right** channel difference; a mono mixdown cancels it.
  - It was read by eye, not by OCR `[source: rabbitv3 gsmg_hidden_research_2026_09_12; gemini dcl_audio_audit]`.
  - Creator pointer: #1837 "Only -41,-17 matters."
- `sha256("GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe")` = **`89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32`** ✅
  - The text hashed is the poster caption plus the prize address.
  - The digest is the page path and appears in the Wayback CDX (`originals/cdx_wayback_gsmg.json`).
  - It is **not** the AES password.
- Page: `originals/pages/salphaseion_phase3.html`. Textarea 1 is a 1,075-character letter stream (spaces removed, `data/salphaseion_compact_1075.txt`). Its layout, fully accounted for with no leftover characters:

| Range | Content | Decode |
|---|---|---|
| [0:91] | **DBBI** (`dbbi…abe`, letters a–i only) | **UNREAD** |
| [91:195] | a/b run | a=0, b=1, 8 bits → `matrixsumlist` ✅ |
| [195:765] | **FAED** (570 letters, a–i only) | **UNREAD** |
| 765 | `z` | separator |
| [766:829] | a–i/o | a..i=1..9, o=0 → decimal → integer → bytes → `lastwordsbeforearchichoice` ✅ |
| 829 | `z` | separator |
| [830:859] | a–i/o | same method → `thispassword` ✅ |
| 859 | `z` | separator |
| [860:895] | literal | `shabefourfirsthintisyourlastcommand` (splits as `shabef`+`our…` or as `shabefour`+`first…`; both have been tested) |
| [895:959] | base64 half 1 | **ends in `…rdrd9z`, and that `z` belongs to the ciphertext** |
| [959:999] | a/b run | `enter` ✅ |
| [999:1063] | base64 half 2 | |
| [1063:1075] | literal | `shabefanstoo` ("sha256 ans too") |

- Joining the two halves gives the **SalPhaseIon short envelope** (see §8). The widely circulated 127-character copy, which drops the `z`, can never decrypt.
- Textarea 2 is the **Cosmic Duality** envelope: one 1,792-character base64 blob containing `Salted__` once. Earlier notes calling it "14 blobs" are wrong.
- `matrixsumlist` candidate data (the poster's 1-bits) `[source: v2, gemini]`:
  - row sums `[6,10,8,7,6,6,5,4,9,9,7,8,7,9]`
  - column sums `[8,10,8,10,8,7,3,6,7,5,9,6,6,8]`
  - total 101

## 7. DBBI minus VIC (exact arithmetic; what it means is in 03)

- DBBI (91) minus the checkerboard plaintext (91), mod 26, A=0:
  `VOZIJBDTIQBRGVEOMZNBCYOUWONXCPKWGBNAXDGJGDUNNVMPABTAFPAAXMJYLZBUWERDNXYDESKUOBXCAMVDJLQTSGA` ✅
- `V`, `I`, `C` sit at positions 1, 4 and 21 (1-based), and `YOUWON` at positions 22–27.

## 8. Locked envelopes (exact bytes in `data/`)

| Name | File | Raw / ciphertext | Salt | sha256(raw) | First seen in chat |
|---|---|---|---|---|---|
| Terminal (end of 3.2) | `locked_terminal_phase3_2_end.*` | 96 / 80 B (5 blocks) | `b45a5e3d827593ca` | `291dfd6f3e759ec2e272b35a00c24907da70c3e7a9291b4c13605c7b0b4f3de9` | 2020-05-09 13:44 UTC |
| SalPhaseIon short | `locked_salphaseion_short.*` | 96 / 80 B (5 blocks) | `3ab585348552415d` | `9e2831e1b34b5f34796df47ccaf6530d48d371c61a6bff84d60db1064fa7a258` | stream 2021-04-16 |
| Cosmic Duality | `locked_cosmic_duality.*` | 1,344 / 1,328 B (83 blocks) | `2d3f6fe06dc950e6` | `b18950551a4dd0cb8a9378f0906ba18c03a15f0ee83eb98c6bc90165c5f79805` | 2021-04-16 |

- The terminal envelope was in chat about 30 hours before block 630000, so its key cannot come from the 2020 halving block.
- Creator #8569 (2023-06-10), answering in order:
  - "Correct." — the 3.2 terminal block has not been decrypted.
  - "No." — the terminal block is not where the SalPhaseIon hint is.
  - "Can't say anything about this." — about X2SH.
- **Not** puzzle material: an envelope with salt `74c974e3f92e64b5` ("urlblob"). It was requested as a gsmg.io hex path on 2026-01-05, most likely by a solver, and the site returned its generic shell page `[source: gemini digest]`.

## 9. On-chain facts `[source: v2 Add.24, gemini; raw tx re-verified in those rounds]`

| | Half | Better Half |
|---|---|---|
| Address | `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` | `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` |
| hash160 | `a9553269572a317e39f0f518cb87c1a0ee1dbae4` | `4bc468447fe1b048ad030a2f9a125478eabc4ed6` |
| Balance | 125,635,374 sat | 375,055,856 sat (never spent) |

- Total: 500,691,230 sat.
- Half's uncompressed public key (it has signed, so the key is exposed): `04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a4649c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559`
- History:
  - Funded 2019-04-13, block 571,497.
  - Moved 2.5 BTC to Better Half at block **630,001** (nLockTime 629,998, the halving).
  - Moved 1.25 BTC at block **840,725** (nLockTime 840,003).
  - If the pattern holds, the next move is around block 1,050,000 (~2028). This is a guess from the pattern.
- 6 signatures with 6 distinct r values, so there is no nonce reuse. All 105 OP_RETURN outputs are inbound spam from solvers (a count of 81 distinct messages vs 105 outputs has not been reconciled).
- More detail: `reference_texts/prize_address_dossier.txt`.
- **Marker addresses solved** (dust senders/recipients around the prize; re-derived 2026-09-13, details 06 §2):
  - `18CchrjA3U…` = key sha256(149-digit checkerboard string)
  - `1AD2wfwX…` = key sha256(Phase 1 answer)
  - `13HGhjkm…` = key = bit-reversed 192-bit integer of `gsmg.io/theseedisplanted`
  - `1GyT5W…` = key sha256(prize address)
  - `1NULY7…` is a kangaroo-tool tip address, not a puzzle key. The dossier still lists the first three and 1NULY7 as unknown.
- April 2026 inbounds from `1Kv59xv…` / `1KY3yqm…` use keys derived from the retracted fluke chain (05 §1), not from an opened envelope.

## 10. Site state

- Rounds disagree on whether the site is still up:
  - rabbit r1 and v2 said gsmg.io answered every path with a 9-byte `Hello :-)` 404 after 2026-07-01.
  - Round gemini (Add.40, 2026-09-09) found that **known paths still return 200**: `/theseedisplanted` (832 B), `/puzzle`, the phase 2/3 page (9,207 B), `/89727c…` (4,536 B). `Hello :-)` is just the site's normal 404 for unknown paths.
  - The gemini captures are `originals/pages/live_seed_capture.html` and `live_phase23_capture.html`.
  - Treat the site as **live** and "404 = unknown path". Also: Wayback captures made after July 2026 of made-up paths are placeholders, not doors.
- Qualification (06 §8): some non-puzzle paths served a parking template (2026-08-04), and a Wayback 2026-07-08 capture shows a domain-for-sale page. On 2026-09-12 the root page read "The lights are off. / Nine years of chaos ended. One mystery remains. / Follow the white rabbit →". `[log]`
- The live rebus page has a comment added later: `<!-- Nice to see you around! Good luck little bunny hunter ;) -->`.
