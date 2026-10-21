# Are the three locked containers rabbit holes? (3 October 2026)

**6 October 2026 interpretation notice.** This is a dated research record.
Its candidate counts and original logs are preserved, not freshly rerun.
Read [doc 118](../118-correctness-audit-remediation.md) for detector/coverage
limits and [doc 119](../119-current-evidence-ledger.md) for current findings.
A null applies only to its complete tested tuple.

The categorical route verdicts below are historical hypotheses: artifact provenance does not establish mandatory use, short-first order, Terminal-only rabbit-hole status, Cosmic message-only content, or exactly one remaining password. A short surplus can encode selectors/instructions, not only passwords.

Question from Lamps: is one, or all, of the three remaining containers a rabbit hole, with the real route to the prize never found?

Sources: `jrk_messages.txt` (all 492 creator messages, read with their reply parents), dossier sections 1, 3.4, 4.5, 6.5, 7, 8, 9, 10 and 12, `21-checkpoint-oracle.md`, the critical review, the riddle ledger (rounds 1 to 7) and the failed-attempts log. Compute: one script, `structural.py`, under a second on one core; output in `structural.log`. Statements marked INFERRED are readings, not measurements.

## Verdict

| container | verdict | one-line reason |
|---|---|---|
| SalPhaseIon short (80 B) | **on-path** | It is the lock of the "second route" the creator confirmed (#4695 "Correct"); his page labels sit beside it; asked with the sites down whether "Salp or Cosmic" still work, he said "The puzzle is still valid!" (#63957) |
| Cosmic Duality (1,328 B) | **on-path, but as a message, not the key holder** | 1,312 to 1,327 bytes of plaintext; "yinyang" is "the next phase" after an AES decode (#39237) and "once you hit a ying yang, you'll be able to solve it the same day" (#9599); the cover is "scary specific" once solved (#8315). It may also be the "'obscure' intel" prize of #24627 |
| Terminal (80 B) | **unknown; the only real rabbit-hole candidate** | No riddle beside it and no "ciphered with ..." line (every other mainline envelope had one); when solvers sat at it with "no clear direction" the creator said "Or nobody found the direction" and "most see 3.2 as the last part" (#2017, #2026); he refused to say where the key is (#2910) and gave only "There must at least be something hidden in there" (#2918) |

**On the bigger question (a route nobody has found):** the creator's own statements rule out a route that bypasses the containers. In August 2021 he said the private key is technically stored online, encrypted, "the one to be found by solving the puzzle", and "the solver will find a way to 'decrypt' it" (#7830, #7832, #7834). The only encrypted objects published online are these containers (the three solved ones are open and hold no key; section 3 below re-checks that). He also said no further URL is needed ("No need. You have all the info.", #9607), no internet is needed (#16624), and the puzzle is "still valid" with the sites gone (#63957). A hidden route that needs a URL, the live site or anything outside the published material contradicts all four. So the "real way" runs through the containers; what may still be unfound is the **order and the third door**, not a different vault.

## Part 1: evidence per container

### SalPhaseIon short

For:
- Route structure. The poster showed "only one door" (Roses poem, Jan 2020); the second door is the side page, reached by HASHTHETEXT (dossier 4.5). "Who knows what you'll find after opening the 2nd door" (#3923, May 2020); "There's 1 club that passed but they are stuck in the next phase" then "Correct" to "Is it the next stage of the second route?" (#4694 to #4696, Aug 2020); "Another person (or team) made it to salph", "Nr 5 in salph" (#6491, #6712).
- "Breaking salphation, should be giving the feeling of the phase's name" (#6497): breaking salph is a named, intended step.
- "salphaseion is 100% solveable?" then "Yes" (#66587, #66588; adjacent, no reply link).
- #63957: asked whether the sites going down affects "resolve Salp or Cosmic", he answered "Ah, ofcourse. The puzzle is still valid!"
- The textarea's live content is labels and `sha256` instructions placed around this ciphertext (dossier 9), the creator's usual riddle-beside-the-lock grammar.
- The Architect text tells the mainline solver to "return to the source codes", which is this page's source.

Against: nothing found.

### Cosmic Duality

For:
- #39237: "is yinyang found after decoding an AES ciphertext?" answered "It's the next phase". #9599 "Once you hit a 'ying yang', you'll be able to solve it the same day." #39224 "when yingyang is reached, 2 hours max."
- #8311/#8315 on the book cover: "That is very specific" and "If the puzzle is solved you'll see how scary specific that is". The title matters to the solution.
- Named in the #63957 question, answered "still valid".

Against (as a key holder, not as a step):
- Size: 1,312 to 1,327 bytes of plaintext. A private key needs 64 hex characters. Dossier 6.5 already calls it a message.
- #24627 lists three prizes: "A private key, some 'obscure' intel, or ... the most obvious reason to make sure you hold on to Bitcoin." A 1.3 KB message fits "obscure intel" better than a key (INFERRED).

### Terminal

For:
- It is the last object of the mainline, and the checkerboard message immediately before it reads "In case you manage to crack this, the private keys belong to half and better half ..." (dossier 3.4b).
- #2918 "There must at least be something hidden in there" (hedged in dossier 6.5: third-hand question; #2910 declined to localise the key).
- An 80-byte container holds exactly one 64-character hex string with a full pad block, the shape of both a private key and a next password (INFERRED from the length bounds in dossier 6.5).
- Formatting: `\r\n` line breaks at 64 characters inside the 3.2 plaintext, the same workflow that made the solved envelopes. Not a hand-made fake.

Against:
- No riddle beside it, and no "Phase X is ciphered with aes-256-cbc base64 and a sha256 pw" line, which preceded every solved envelope (checked in the phase-3 plaintext: "Phase 3.2 is ciphered with aes-256-cbc base64 and a sha256 pw, yet again.").
- Feb 2020, solvers stuck exactly here: #2016 "There's no clear direction on what to do next, and probably invokes time consuming brute force" answered "Or nobody found the direction" (#2017), then "Don't know but most see 3.2 as the last part" (#2026). The creator steered people away from attacking the Terminal and toward a direction they had not found (the side page, found later that year).
- The Architect text sends the reader away from the mainline ("return to the source codes").
- The riddle above it opens "Raising the stakes without extra chances of winning." It spells the checkerboard key, but read as a label for the next object it describes a gamble that costs more and wins nothing, which is what a decoy is (INFERRED; R18 already ran the key-stretching reading of the same sentence).
- The #63942 question that drew "still valid" named "Salp or Cosmic", not the Terminal.

Rating: unknown. The evidence supports "not the next step" strongly and "not needed at all" only weakly. Two readings survive: the Terminal is the final vault, opened with what SalPhaseIon yields (the checkerboard's "crack this" plus #2918), or it is the mainline's dead end, kept to absorb brute force (#2017, #2026, the missing cipher line).

### The "another door"

- #7914 (Dec 2021) "There is Another DOOR", #8000 "still a thing. We're not sure if anyone has found another door so far ... prime numbers ... some characters need to be 'zeroed out'". By then five teams were in salph, so this door is past the second one.
- #8795/#8796 (Aug 2023), to "can you confirm there is indeed a 3rd door yet to be found?": "I saw that you guys got really really far already. Actually, the hardest part is done." Not a denial.
- #9607 the same week: no other URL is needed.

Reading (INFERRED): the third door is opened with information already held (prime walk, zeroing), so it is a password, not a page. The prime part is dbbi (solved Sep 2026). That leaves the third door most plausibly being SalPhaseIon short itself.

## Part 2: if the key does not come from a container

Every object that could carry or point at a 256-bit key, the single operation that would yield it, and its status.

| object | single operation | status |
|---|---|---|
| Architect text (1,539 letters) | sha256 of the text; any 32-byte or 64-hex window; "TAKETHEPRIVATEKEY" pointer (479) | null (doc 107; S3 below; 479 pointer spent, dossier 12) |
| Checkerboard message "private keys belong to half and better half" | sha256 of the 91 letters; the halves as two scalars | null (doc 107, doc 111/114). It names owners, no value |
| Checkerboard 149 digits | sha256 (on-chain checkpoint "part of the cipher"); the number itself mod n | sha256 is a known checkpoint, not the prize; integer null (S6) |
| dbbi residue | as key material, base-9, decimal | null (doc 95) |
| Poster grid (196 bits) | the 192-bit spiral as a raw key ("Good job, Neo!" checkpoint, not the prize); the full grid row-major, column-major, spiral, reversed, inverted | null (S5) |
| Phase plaintexts (2, 3, 3.2) | sha256 of each; every 32-byte and 64-hex window | null (doc 107; S3, S7) |
| Phase-3 part 6, the 140-character genesis code | as an integer, both byte orders | null (S6) |
| Solved passwords (sha256 of each answer) | the password is itself a 256-bit scalar | this is exactly the win test of the answer; null (S7) |
| AES key and IV each solved gate derived | raw scalar, sha256 | null (S1, new) |
| Chain atoms up to 32 bytes | raw ASCII as a big-endian scalar, as the poster URL was | null (S2, new) |
| Any text, for a WIF or BIP38 string | base58 run of 51, 52 or 58 characters | none exists (S4) |
| Unconsumed surplus: centre `0000`, leftover `B` and `Y`, trailing `O`, doubled `SELF`, "And Oen", "as wide as the first one seen", the New Year dots | none of them is 256 bits or names a 256-bit object; each is at most a few characters or a pointer | no key-producing operation exists; they can only be parts of a password |

Conclusion of part 2: no decoded object carries the key, and the surplus is too small to be one. Anything that is not a container can only supply a **password**, which brings the route back to a container.

## Part 3: does any solved artifact, under the proven convention, act as the key?

`structural.py`, controls first: key 1 gives `751e76e8...`; phases 2, 3 and 3.2 open and the 3.2 plaintext hashes to `b82afeb8...`; the raw-ASCII form reproduces the real on-chain poster checkpoint `148XH2YBmL...` from `gsmg.io/theseedisplanted`; a planted key inside a random buffer is found by both window scanners. Targets: prize (both point forms), sentinel, and the four EC neighbours, so a scalar off by one step, half or double would also show.

| id | family (one sentence each) | tests | result |
|---|---|---:|---|
| S1 | The AES key, IV and salt each solved gate derived are 256-bit (or shorter) secrets the solver holds and the win test never saw. | 24 | null |
| S2 | Chain atoms up to 32 bytes as raw big-endian ASCII, the construction the poster checkpoint used. | 128 | null |
| S3 | Every 32-byte window and every 64-hex window of the three solved plaintexts, the textarea, the three locked blobs and the Architect letters. | 11,200 | null |
| S4 | Base58 runs that could be a WIF or BIP38 key in any of those texts. | scan | none (only the 149 digits, the a..i soup and a base64 fragment) |
| S5 | The 196-bit poster grid as one integer, six readings each inverted. | 18 | null |
| S6 | The 149 checkerboard digits and the 140-character genesis code as integers. | 8 | null |
| S7 | Confirmation of doc 107: each answer, password and plaintext (with line-ending variants, and 3.2 split at the Terminal) through the win test. | 19 | null |

11,397 tests, 0 hits. The solved chain is not the key under any single structural reading.

## What this changes

1. The rabbit-hole hypothesis for **all three** is refuted by #7830 to #7834, #9607, #16624 and #63957: the key is an encrypted object already published, and nothing outside the published material is needed.
2. The hypothesis survives for **the Terminal only**. Practical consequence: no further work should treat the Terminal as the next lock. Every candidate is still screened against it for free (the harness does that), but derivations should target SalPhaseIon short first (dossier 6.5 already prioritises it; this adds the Feb 2020 evidence).
3. Cosmic Duality should be modelled as a message reached after SalPhaseIon (yinyang), not as a key holder; trying to open it before SalPhaseIon is likely the wrong order.
4. The "another door" of Dec 2021 is best read as a password door opened with primes and zeroing, which lands on SalPhaseIon short; no separate unexplored route is indicated.

Nothing here required outside people or the creator. No sweep was run.

## Follow-up: what Cosmic Duality and SalPhaseIon short give away without a password (3 Oct 2026)

Lamps asked for a stress test of both for any leak about what they are. Script `leak.py`, output `leak.log`, under a second.

**1. Historical statistics did not detect the planted crude patterns; they cannot establish AES.** Byte histogram, bit balance, compressibility, repeated 16-byte blocks (the ECB tell), serial correlation and periodicity at shifts 1 to 64. Controls: the three solved containers (real AES-CBC) all read random; four planted fakes (text XOR a repeating key, a byte-shift Vigenere, AES-ECB of repetitive text, text XOR a 32-byte key) are all caught. Cosmic Duality, SalPhaseIon short and the Terminal read random on every test. The historical `leak.py` generated 64-byte random controls for the 80-byte short/Terminal ciphertexts, despite `leak.log` describing 80-byte controls. The old flag rates and percentiles have mismatched or uncertain provenance and are not calibrated evidence. The revised script uses matched ciphertext lengths, the same unrounded statistics and a recorded seed/runtime. It has not been rerun; `leak.log` is preserved unchanged. Random-looking bytes cannot distinguish AES from other encryption or random data.

**2. These length bounds assume 16-byte CBC/ECB with PKCS#7.**
- SalPhaseIon short (and the Terminal): plaintext 64 to 79 bytes. That is exactly one 64-character hex string with a full pad block, which is the shape of the creator's own passwords (sha256 hex) and of a hex private key; also `gsmg.io/` + 64 hex (72), or one 64-character base64 line, which would be a nested 48-byte envelope holding 16 to 31 bytes. WIF (51/52) and bare BIP38 (58) do not fit.
- Cosmic Duality: plaintext 1,312 to 1,327 bytes, 83 blocks. A message, or a nested envelope in base64 (inner envelope 960 to 992 bytes, inner plaintext about 928 to 975), or hex of a 656-byte envelope. Not a bare key.
- Reading (INFERRED): short's size is exactly "one password", which fits short holding the password that opens Cosmic Duality (yinyang "after an AES decode", #39237). The harness's lock chaining already tries every short-like output on Cosmic.

**3. Page presentation.**
- On the phase-2 page every lock has a riddle and a "Ciphered with aes-256-cbc /w base64 sha-256(password)" line. Cosmic Duality has neither: its only clue is its heading. SalPhaseIon short has the label soup around it.
- Cosmic's base64 is plain `openssl enc -a` output: 28 lines of exactly 64 characters, no trailing newline. Same textarea style as the phase-2 page. Trailing newlines vary on the creator's own phase-2 page, so that carries no signal. No capture has carriage returns at all, so line endings say nothing about the machine.
- The heading tags differ: the creator's phase-2 page uses `<H1>...</H1>`; the side page has `<h1> SalPhaseIon </H1>` (his uppercase close) but `<h1> Cosmic Duality </h1>` (all lowercase). Weak sign that the Cosmic block was typed separately from the SalPhaseIon block, possibly at a different time (INFERRED).
- When each block first appeared would say whether Cosmic was added later, but the Wayback API is blocked from this container (proxy 403), so that stays open.

**What it adds.** Nothing about either plaintext beyond size. The useful constraints: short holds something password-sized, Cosmic holds a message-sized object, and Cosmic is the one lock on the site published with no riddle text or cipher line, only a title.

## Follow-up 2: solve order and number of passwords, from lengths and the page's own order (3 Oct 2026)

Read the SalPhaseIon textarea top to bottom as an instruction list (offsets from dossier 6.1), with the container lengths from `leak.py`:

| step | page content | role |
|---|---|---|
| 1 | dbbi = `yellowblueprimes` | a check that you are on the right poster (solved, 91/91) |
| 2 | `matrixsumlist` | operation 1 |
| 3 | faed | filler |
| 4 | `lastwordsbeforearchichoice` | operation 2 |
| 5 | `thispassword` | "these two make this password" |
| 6 | `sha256 our first hint is your last command` | hash it: the first hint (#225) was a sha256, and so is the last command |
| 7 | short envelope (with `enter` between its two 64-char lines) | opens to 64 to 79 bytes |
| 8 | `sha256 the answer too` | hash what comes out as well |

Model (INFERRED, but every step is on the page and the sizes agree): **one unknown password remains**, the one for short. Short's plaintext is "the answer", 64 to 79 bytes. Step 8 then says to sha256 it: that gives either the private key itself (sha256 of a phrase is exactly the win test, and the creator's checkpoints used that construction) or the password for Cosmic Duality, whose 1.3 KB message is the "yinyang" after which the solve is "the same day" (#9599). #8446's "very last step is a true giveaway, promised" fits step 8. The Terminal would then open with something from that message, or not be needed.

Consequences:
- No second unknown password is implied for Cosmic or the Terminal; they follow by hashing. The harness already chains a short-like output into Cosmic and runs the win test on every decrypt, so nothing extra needs building.
- All remaining effort belongs on the short password (steps 2 to 6). That is the Constraint synthesis thread's table; this thread adds no candidate pool to it.

One literal reading the transcript framing suggested and the ledger lacked, R32: in a shell "your last command" is `!!` and the first history entry is `!1`. Six forms (`!!`, `!1`, `!-1`, `!1!!`, `!!!1`, `sudo !!`) through `riddle-method/rt.py` (controls fired; 288 decrypts, 0 valid pads against about 1.1 expected, 0 flags, 0 win-test hits). Null.
