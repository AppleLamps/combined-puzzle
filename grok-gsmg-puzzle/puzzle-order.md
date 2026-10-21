# Puzzle order

Step-by-step path through the GSMG.io 5 BTC puzzle, in the order a solver meets the material. Facts marked **[V]** are reproduced in this repo (`python3 src/archivist_check2.py`, 106/106). Strings marked **[R]** are the accepted readings that decrypt the solved stages; they are not printed as passwords on the pages. **Locked** means no password in this repo opens that container.

Source pack: `uploads/GSMG-handoff.md`. Status log: `ledger/00-lead.md`.

Win test: a 32-byte private key is correct only when the uncompressed public key hashes to `a9553269572a317e39f0f518cb87c1a0ee1dbae4` (address `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`).

Solved containers use OpenSSL `Salted__`, AES-256-CBC, EVP SHA-256, one iteration. The password bytes are the **lowercase hex** of `sha256(answer)`, not the answer itself. That convention is **not** proven for the three locked containers.

---

## 1. Poster

Image: `data/puzzle.png`.

A 14×14 colour grid, title `GSMG.IO 5 BTC PUZZLE CHALLENGE`, a QR code to the prize address, and seven rabbit cells.

**[V]** Black and blue = 1, white, yellow, and off-white = 0. Read inward, counter-clockwise, from the top-left, down first. The first 192 bits are the URL:

`gsmg.io/theseedisplanted`

The last four bits (centre) are `0000`. Every blue or yellow cell sits on bit 7 of a character (the low bit): blue on 1, yellow on 0. One off-white cell (`#FEFEFE`) is spiral index 163, counting from 0, a 0 in the `n` of `planted`.

Two routes leave the poster. The spiral URL is phase 1 (step 2). Hashing the title text plus the address is the SalPhaseIon page (step 6). That page does not depend on solving phases 2–3.2.

## 2. Phase 1 — the seed page

Page: `gsmg.io/theseedisplanted`. Eight rebus tiles.

**[R]** The tiles read CAN YOU / DIG IT / LOGIC / WARNING, from Logic’s song “The Warning”.

**[V]** The form accepts:

`theflowerblossomsthroughwhatseemstobeaconcretesurface`

The creator posted that string’s sha256 as chat #225: `5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75`. Submitting it (do not; this repo stays offline) redirects to phase 2.

## 3. Phase 2 — causality

Page path (the Merovingian “choice” line):

`gsmg.io/choiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecialdessertiwroteitmyself`

Textarea 1 is the phase 2 container.

**[V]** Answer `causality` decrypts 648 bytes. The plaintext names keymakers, “2name”, “3Moon”, “4How so mate”, and the coordinate template `# X 2 S H 4 Y 0 Q B 15 #`.

**[R]** That template resolves to the former SafeNet office in Rotterdam-Pernis (51°52'28.0" N, 4°24'23.2" E). The numerals 2, 3, 4 index later password parts. `causality` itself is not printed on the page.

## 4. Phase 3 — seven parts

Same page, textarea 2. The page says parts 1..7 are hashed and the digest is the password.

**[V]** Concatenate these seven strings with **no separators**. That password decrypts 4090 bytes (`artifacts/phase3.txt`). The page text is `parts 1..7 --> sha-256 -> dgst is the password`. In this repo, lowercase `safenet`, `EO11110`, the genesis hex without `0x`, the other side to move, and a trailing space on `Luna` do not decrypt it.

| # | String | Reading **[R]** |
|---|--------|-----------------|
| 1 | `causality` | Phase 2 answer reused |
| 2 | `Safenet` | “2name” |
| 3 | `Luna` | “3Moon” |
| 4 | `HSM` | “4How so mate” |
| 5 | `11110` | Executive Order 11110 (“5binary”) |
| 6 | `0x736B6E61…656854` | Genesis-block newspaper headline, reversed hex (“row 1616”) |
| 7 | `B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1` | Chess position after the move the page asks for |

The plaintext ends with the phase 3.2 container.

## 5. Phase 3.2 — three riddles, then five regions

**[V]** Join these three answers with no separators:

`jacquefresco` + `giveitjustonesecond` + `heisenbergsuncertaintyprinciple`

They come from the phase 3 plaintext (Jacque Fresco; “add giveit in front of” the Cheshire keyhole answer; Heisenberg’s uncertainty principle). The decrypt is 2422 bytes (`artifacts/phase32.bin`). Ranges below are inclusive. `CRLF CRLF` sits between the regions.

1. **Bytes 0–446.** ASCII. Ends “One for one, four for one.”
2. **Bytes 447–1985.** 1,539 bytes. Read as cp273, letters a = 0, then reciprocal Beaufort (`P = K − C mod 26`) with key `THEMATRIXHASYOU`. Result is a rewritten Architect speech: select from over twenty-three ciphers, sixteen encryptions, and/or seven intertwined passwords; brute force might be required.
3. **Bytes 1990–2138.** 149 digits. Straddling checkerboard with alphabet `FUBCDORA.LETHINGKYMVPS/JQZXW` and digits 1 and 4 as the top-row blanks. **[V]** decode: `INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE`. **[V]** Of the 90 ordered blank pairs, 72 parse all 149 digits and only (1, 4) gives text containing the plaintext's cribs (`python3 src/checkerboard_pairs.py`).
4. **Bytes 2143–2291.** The riddle that supplies that checkerboard alphabet: “Raising the stakes without extra chances of winning…”
5. **Bytes 2292–end.** Locked **Terminal** container (80-byte ciphertext, salt `b45a5e3d827593ca`). The raw blob is 96 bytes: `Salted__`, 8-byte salt, 80-byte ciphertext.

## 6. Side page — hash the poster text

This page is the other exit from step 1. It is not unlocked by phase 3.2.

**[V]** Path is sha256 of `GSMGIO5BTCPUZZLECHALLENGE` plus the prize address:

`gsmg.io/89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32`

**[R]** Solvers reached that instruction via `HASHTHETEXT` (a Decentraland audio clip) and creator hint #7416 (“hash all the text you see” on the poster).

The page has two headings:

- **SalPhaseIon** — 1,075 characters. On the page each character except the last is followed by one space (1,074 spaces).
- **Cosmic Duality** — locked container, 1,328-byte ciphertext, salt `2d3f6fe06dc950e6`. Raw blob is 1,344 bytes.

## 7. SalPhaseIon text, in the order it is written

Remove the spaces. Blocks change when the alphabet changes. Spans are half-open, as in the handoff. Decodes below are **[V]**.

| Order | Span | What it is |
|------:|------|------------|
| 1 | [0, 91) | `dbbi` — 91 letters `a`–`i` |
| 2 | [91, 195) | `a`/`b` bits → `matrixsumlist` |
| 3 | [195, 765) | `faed` — 570 letters `a`–`i` |
| 4 | [765, 766) | a single `z` |
| 5 | [766, 829) | decimal, `o` = 0 → `lastwordsbeforearchichoice` |
| 6 | [829, 830) | `z` |
| 7 | [830, 859) | same decimal decode → `thispassword` |
| 8 | [859, 860) | `z` |
| 9 | [860, 895) | `shabefourfirsthintisyourlastcommand` |
| 10 | [895, 959) | base64, first half of a container |
| 11 | [959, 999) | `a`/`b` bits → `enter` |
| 12 | [999, 1063) | base64, second half |
| 13 | [1063, 1075) | `shabefanstoo` |

Joining the two base64 halves **is** the SalPhaseIon-short container (80-byte ciphertext, salt `3ab585348552415d`). `enter` sits between the halves on the page.

**[R]** `shabef` expands with b=2, e=5, f=6 to “sha256 our first hint is your last command” and “sha256 the answer too”. The creator’s first hash hint is #225. “Last command” has been read as `theseedisplanted` or the ciphertext that follows the phrase. Neither reading has opened a locked container here.

**[V]** `dbbi` parses against the poster’s spiral colours, with the off-white cell spliced in as a 25th symbol. At prime positions take the next colour (`b` for blue or off-white, `be` for yellow). At non-prime positions take one filler letter. The 91 letters are used up at position 83. The 23 host bits (blue = 1, yellow = 0) equal the URL’s 24 low bits after a 1 is inserted at position 21 and the first 23 bits are kept (`10` left over). That is the same splice as treating off-white as blue. The 60 filler letters are unexplained. Continuing past position 83, the 24th colour (blue) lands on `b`; the 25th (yellow, which needs `be`) lands on `aa` and the walk fails.

**[V]** Full-period Bifid of `faed` on square `dbifhcegaklmnopqrstuvwxyz` starts `btcseedd`. Eight of 362,880 orderings of the nine `dbbi` letters do the same. Nothing after `btcseed` is readable. This is not a unique checksum.

## 8. Creator roadmap (after the pages)

**[V]** Chat #8446: reverse the whole bit string, then read 8 bits per byte. The text is `yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyang` followed by `wewontgiveawaythepassworditsinfrontofyoureyesbutyourenotseeingitverylaststepisatruegiveawaypromised`.

That names an order. It does not give the inputs of `matrixsumlist` or `lastwordsbeforearchichoice`.

Other creator lines that point at the unsolved part, not at a finished password:

- #7914 — “There is / Another / D O O R”, written vertically.
- #8000 — that door hint is still live; primes are required; some characters must be zeroed out.
- #6884 — `another door might be found on {1 },{4} ,{21}` (posted 1 April).
- #6913 — `R=18`, `A=1`, `B=2`; “Could also be 21 or 1812 bit”.
- #6509 — an unforeseen hint on `matrixsumlist` was already given.
- #39237, replying to whether yinyang comes from decrypting AES — “It’s the next phase.”
- #8310–#8315 — a solver posted the cover of the Time-Life book *Mysteries of the Unknown: Cosmic Duality*. The creator called it “very specific” and said the solved puzzle would show how specific.
- #9607, asked if another URL must be found — “No need. You have all the info.”

## 9. Where the path stops

Three `Salted__` containers remain closed:

| Container | Where it sits | Ciphertext |
|-----------|----------------|------------|
| Terminal | End of the phase 3.2 plaintext | 80 bytes (raw 96) |
| SalPhaseIon short | The two base64 halves around `enter` | 80 bytes (raw 96) |
| Cosmic Duality | Second textarea on the side page | 1,328 bytes (raw 1,344) |

Everything after phase 3.2 is operands without an agreed operation: what `matrixsumlist` sums, what text is `lastwordsbeforearchichoice`, what `enter` does, which container each step opens, and whether those containers use the solved AES convention.

Rounds 2–14 in `ledger/` tried those labels, poster sums, deletion and zeroing, chained pipelines, and the structural readings in steps 7–8. None produced structured plaintext or the prize hash160. Current status: `ledger/00-lead.md`. Latest round: `ledger/22-round14.md`.
