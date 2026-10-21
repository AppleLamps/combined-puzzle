# 02 — Reader: solved-chain literalness and open-label candidates

Sources only: `uploads/GSMG-handoff.md`, `ledger/01-archivist.md`. No decrypts in this file.

---

## 1. Section 4 solved stages — clue → source → literalness

Reader method: treat **[V]** as mechanical reproduction; treat **[R]** as hypothesis required to reach the answer string; ask whether a first-principles solver who only trusts on-page labels and byte checks would derive the same password without community lore or post-hoc fit.

### 4.1 Encryption convention

| | |
|---|---|
| **Clue** | Phase pages label containers as AES-256-CBC, base64, password = SHA-256 digest of the answer (§3.3 phase 2/3 `<p>`, §4.1). |
| **Answer source** | Convention inferred because it decrypts §4.2–§4.4 to exact plaintexts [V]; EVP SHA-256, one iteration, password passed as **lowercase hex** of `sha256(answer)` (§4.1). |
| **Literalness** | **High for the mechanism** once any answer string is known; **not** a stage password. Locked containers are **not** proven to use the same scheme (§4.1 last paragraph, §9). |

### 4.2 Phase 2 — `causality`

| | |
|---|---|
| **Clue** | Poster spiral → URL `gsmg.io/theseedisplanted` (§3.1 [V]); phase 2 lives at path derived from Merovingian / *Matrix* “choice” line (§3.3 URL). Phase 2 plaintext is thematic (keymakers, Merovingian, `# X 2 S H 4 Y 0 Q B 15 #`) (§4.2). |
| **Answer source** | Single-word answer `causality` opens the phase 2 container [V, §4.2, archivist #32–34]. **[R]** coordinate/SafeNet reading in §4.2 does not supply the decrypt password. |
| **Literalness** | **Low–medium.** Spiral + URL are literal [V]; the word `causality` is **not** printed as the phase 2 password—you need *Matrix* / URL thematic association or search under §4.1. A strict “labels only” reader would **not** produce `causality` without external cultural mapping or brute force. |

### 4.3 Phase 3 — seven-part concatenation

| | |
|---|---|
| **Clue** | Phase 3 page: “parts 1..7 → sha-256 → dgst is the password” (§3.3 HTML). Phase 2 plaintext embeds numbered hooks (2name, 3Moon, 4How, 5binary, genesis “row 1616”, chess diagram) (§3.3, §4.3 **[R]** table). |
| **Answer source** | Plain concatenation of the seven strings in §4.3 (no separators) decrypts phase 3 [V, archivist #35–37]. Part 1 reuses `causality`; parts 2–7 per §4.3 **[R]** readings (Safenet, Luna, HSM, `11110`, reversed genesis hex, corrected FEN). |
| **Literalness** | **Medium.** “Seven parts + SHA-256” is **literal on the page**; **each part’s content is mostly [R]** (Rotterdam office, EO 11110, file row 1616, chess move from diagram). A label-only reader gets the **shape** (7-tuple, concat, hash) but **not** the tuple without the handoff’s interpretive chain. Would **not** reliably produce all seven strings from pages alone. |

### 4.4 Phase 3.2 — `jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple`

| | |
|---|---|
| **Clue** | Phase 3 plaintext: thinker’s name, “add **giveit** in front of the answer” for keyhole riddle, Heisenberg limit sentence; “Phase 3.2 is ciphered…” (§4.3 plaintext block). |
| **Answer source** | Three riddle solutions joined **with no separators**: Jacque Fresco → `jacquefresco`, Cheshire “how long” → `giveitjustonesecond`, uncertainty → `heisenbergsuncertaintyprinciple` [V decryption, §4.4]. |
| **Literalness** | **Medium–high** for *which three answers* (they are in the decrypted phase 3 text); **medium** for exact join (no delimiter stated; spelling `jacquefresco`; “giveit” as prefix not separator). A careful reader of phase 3 plaintext could reach this; Beaufort/checkerboard/terminal tail are **downstream [V] structure**, not password literals. |

### Summary literalness (requested targets)

| Target | Would strict reader method produce it? |
|---|---|
| `causality` | **Unlikely** without *Matrix*/URL theme or guessing. |
| 7-part phase 3 password | **Partially** — procedure yes, part strings mostly **no** without §4.3 [R]. |
| Phase 3.2 password | **Likely** with plaintext study; exact concatenation/spelling still judgment calls. |

---

## 2. Open labels — candidate readings

Each row: **exact string or operation** + one-sentence citation (handoff section or creator `#`, with reply-to when given).

**Open label count: 16** (`matrixsumlist`, `enter`, `lastwordsbeforearchichoice`, `thispassword`, `yinyang`, `yellowblueprimes`, `sha256 hints`, `Cosmic Duality`, `container order`, `New Year dots`, `#8446`, `another door`, `off-white`, `SELECT/Architect`, `dbbi fillers`, `faed after btcseed`).

---

### `matrixsumlist`

1. **Operation:** For each of many poster-derived lists (rows, columns, diagonals, blocks, prime indices, spiral order), encode cells as digits/letters, **sum** list elements, emit decimal or ASCII string → candidate password (before/after sha256 per §4.1). — Handoff §8 [T] (~1.55B poster-sum decrypts).
2. **Literal label only:** `matrixsumlist` is the ab-decode of SalPhaseIon span [91,195) (a=0, b=1, 8 bits/char) [V, §6.2]; names a step, not an operand on the page. — §6.3, §9.
3. **Recipe position:** First verb in #8446 token order after `yellowblueprimes` (reverse-bit roadmap). — §7.1 [V decode], string order in §7.1.
4. **Meta-hint:** Creator #6509 → replying to #6508 (“hint on matrixsumlist?”): “I gave an unforseen hint already.” — Appendix A #6509.

---

### `enter`

1. **Literal decode:** Span [959,999) → string `enter` (same ab rules as `matrixsumlist`) [V]. — §6.2.
2. **Pipeline verb:** Insert `enter` between named steps (e.g. after sum list, before lastwords output) in the SalPhaseIon “recipe” [R]. — §6.3 (“read as a recipe”), §9.
3. **Encrypt step:** `enter` = apply §4.1 decrypt with `pass:sha256hex(candidate)` to the next named container. — §4.1, §9 (which container per step open).
4. **False concat (retracted):** `matrixsumlistenterlastwordsbeforearchichoicethispasswordmatrixsumlist` as raw password — padding artifact only [V]; retracted #76033–#76034 per §8.1.

---

### `lastwordsbeforearchichoice`

1. **Literal label:** Decimal run [766,829) → `lastwordsbeforearchichoice` (a..i=1..9, o=0 → int → hex → ASCII) [V]. — §6.2.
2. **Operation on Architect text:** Last token(s) before each “choice” in the Beaufort Architect speech (phase 3.2 bytes 447–1985) or film script — hundreds of windowed candidates [T]. — §8, §4.4 speech [V].
3. **Phase URL anchor:** “Choice” from phase 2/3 URL `choiceisanillusion…` as the “archi choice” event [R]. — §3.3.
4. **#8446 ordering:** Token sits after `matrixsumlist` in reversed-bit string — defines step order, not operand [V]. — §7.1.

---

### `thispassword`

1. **Literal label:** Span [830,859) decodes to `thispassword` [V]. — §6.2.
2. **Recipe output slot:** Result of prior steps is “this password” fed to sha256 + container [R]. — §6.3, §9.
3. **Creator tease:** #8446 fragment “…wewontgiveawaythepassworditsinfrontofyoureyes…” — password material visible in primary artifacts, not spoken [V decode]. — §7.1.

---

### `yinyang`

1. **Roadmap token:** Appears in #8446 reversed-bit plaintext after `lastwordsbeforearchichoice` [V]. — §7.1.
2. **Next phase name:** Creator #39237 → replying to #39233 (“is yinyang found after decoding an AES ciphertext?”): “It’s the next phase, but I await the day someone finally gets there.” — Appendix A #39237.
3. **Duality pair:** Complement to “Cosmic Duality” / checkerboard “half and better half” [R]. — §4.4 decoded digits, §5 Cosmic heading.

---

### `yellowblueprimes`

1. **dbbi parse name:** Poster yellow/blue cells at **prime** walk positions with filler between [V parse, open meaning]. — §6.3 [R intro], archivist §6.3 #68–82.
2. **#8446 prefix:** First token in reversed-bit string — orders recipe before `matrixsumlist` [V]. — §7.1.
3. **Roses poem:** #1710 “Yellow has a number and so does Blue”; #4096/#4102 point back [R]. — §7.2, Appendix #1710.

---

### `sha256 hints` (`shabef…`)

1. **Expand `shabef` → `sha256`:** Plaintext blocks read “sha256 our first hint is your last command” and “sha256 ans too” (b=2,e=5,f=6) [R]. — §6.3.
2. **First hint = #225 hash:** Phase 1 answer verified via posted digest `5ac40783…6f75` (#225), “hit your options against that hash” (#226). — §3.2, Appendix #225–#226.
3. **Last command = spiral URL:** `theseedisplanted` / `gsmg.io/theseedisplanted` as terminal command in Neo/Matrix line family [R]. — §8 (Neo lines, `theseedisplanted` tests [T]).
4. **Double-hash variant:** `sha256(sha256(answer))` or raw digest as password in container sweeps [T]. — §8 convention paragraph.

---

### `Cosmic Duality`

1. **Locked container:** Textarea 2 on SalPhaseIon side page; 1328-byte ciphertext, salt `2d3f6fe06dc950e6` [V]. — §5, §3.4.
2. **Book title lock-in:** #8311 → replying to #8310 (Time-Life cover image): “…. That is very specific”; #8315: solved puzzle will show how specific. — §7.2, Appendix #8311/#8315.
3. **Post-yinyang stage:** Pair with #39237 “next phase” after SalPhaseIon AES stages [R]. — Appendix #39237, §9.

---

### `container order`

1. **Discovery order in narrative:** Terminal at end of phase 3.2 plaintext → SalPhaseIon short inside textarea 1 → Cosmic on same side page [V locations]. — §5, §6.1.
2. **#8446 recipe order:** `yellowblueprimes` → `matrixsumlist` → `lastwordsbeforearchichoice` → `yinyang` → … (not three container names) [V]. — §7.1.
3. **SalPhaseIon before Cosmic on page:** Layout [0,1075) then separate textarea 2 [V]. — §6.1, §3.4.
4. **Open:** §9 “Are the three locked containers all needed, and in what order?” — no creator order proof in handoff.

---

### `New Year dots`

1. **Count 1–5 then binary:** #53335–#53341 single- to five-dot messages; #53342 binary → ASCII `Happy new year! … "tiny hint" <3.` [V in §7.2]. — §7.2, Appendix #53335–#53342.
2. **Dot lengths as separate code:** Five dot-count messages may encode an index/key independent of #53342 binary [R, not decoded in handoff].
3. **Tiny-hint arc:** #881 promised a final tiny hint at start of 2020; New Year 2025–26 message claims another “tiny hint” [R linkage]. — §7.2 #881, #53342 text.

---

### `#8446`

1. **Decode op:** Reverse **entire** 1288-bit string (161×8), then 8 bits/char → roadmap string [V]. — §7.1, archivist #104–106.
2. **Literal payload:** `yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyangwewontgiveawaythepassworditsinfrontofyoureyesbutyourenotseeingitverylaststepisatruegiveawaypromised` — §7.1.
3. **Confirmation:** #8483 → replying to #8448 (solver “reversed binary: yellowblueprimes…”): “👆🤷‍♂”. — Appendix #8483.

---

### `another door`

1. **Spelled hint:** #7914 → replying to #7913: vertical “There is / Another / D / O / O / R” [V]. — §7.2, Appendix #7914.
2. **Still active + primes + zeroing:** #8000 (mini hint): prior door hint “still a thing”; primes required; characters must be “zeroed out” [V]. — Appendix #8000.
3. **Coordinate joke:** #6884 Hint `another door might be found on {1 },{4} ,{21}`; #6913 R=18,A=1,B=2 “Could also be 21 or 1812 bit”; #7529 April 1 caveat [R]. — Appendix #6884, #6913, #7528–#7529.
4. **No new URL:** #9607 → replying to #9605: “No need. You have all the info.” — Appendix #9607.

---

### `off-white`

1. **Poster cell:** Single `#FEFEFE` (254,254,254) at row 7 col 4; spiral index 163, bit 0 in `n` of “planted” [V]. — §3.1, archivist #19–24.
2. **dbbi 25th colour:** Splice `F` into 25-symbol colour sequence; treat F like blue (bit-insert at URL position 21) [V bit match, open intent]. — §6.3, archivist #77–78.
3. **Not 255:** Colour-weight numerology using 255 fails; off-white is 254 [V]. — §8.1.
4. **Chat noise:** #5960 → replying to #5952 (fefefe / 104 banter): “Ancient spelling… typos” — weak poster link [R]. — Appendix #5960.

---

### `SELECT` / `Architect`

1. **Speech constraint list:** Beaufort plaintext includes `…SELECTFROMOVERTWENTYTHREECIPHERSSIXTEENENCRYPTIONSANDORSEVENINTERTWINEDPASSWORDS…` [V]. — §4.4.
2. **`lastwordsbeforearchichoice`:** Label points to words before “choice” in this speech or film [R]. — §6.2 label, §8.
3. **Parallel counts [R]:** 23 dbbi hosts, 16 encryptions, 7 rabbit cells / seven phase-3 parts — numerological alignment only. — §6.3, §4.3, §3.1.

---

### `dbbi fillers`

1. **Fixed 60-letter string:** `difhccgihaeeihggegebgehhehhfafdhffcdbfcccgfeggecdcifffgigeea` at non-prime walk positions [V]. — §6.3, archivist #74.
2. **Hidden-zero masks:** Choose subsets of letter occurrences to zero → decimal→bytes→password variants [T, ~16.8M + 4B dbbi tests]. — §8.
3. **Split lengths 19|16|23:** Two filler `b` partition host segments [V count]; tie to 23/16/7 Architect numbers [R]. — §6.3.
4. **Deletion:** §9: deletion not tried; zeroing exhausted without container hit.

---

### `faed after btcseed`

1. **Bifid period 570:** Square `dbifhcegaklmnopqrstuvwxyz`; full-period decrypt → prefix `btcseedd…`, sha256(output)=`15d62c8228c1a30f3f6280fcdce2251fe616135e9de291b0c7b8a792dd8d0507` [V]. — §6.3, archivist #88–90.
2. **Tail after prefix:** Bytes after `btcseed` not readable; even indices only use {b,c,d,e} [V]. — §6.3.
3. **Whole-block decimal:** faed as one integer (a=1..9) → 237 bytes, head `1bd5951d`, tail `c7bbc075` [V]; g/e zeroing cannot make full decode printable [V]. — §6.3, archivist #95–99.
4. **Structured zero tail:** Zero positions {551,557,561,563} → last four bytes ASCII `szqu` [V search finding, not checksum]. — §6.3, archivist #101–102.
5. **Not forced:** 8/362880 square orderings give `btcseed`; 5/6561 continuations from `faed` [V calibration]. — §6.3, §8.1.

---

## 3. Top 3 untested (or under-tested) readings worth priority

1. **Letter deletion (not zeroing) on dbbi, faed, and/or the 60 filler letters** — output fed through §4.1 or as raw key material. Handoff §9 and §8: exhaustive zeroing failed; “Deletion has not been tried.”
2. **New Year dot counts (#53335–#53341) as an encoding separate from the #53342 binary plaintext** — only the binary tail is recorded [V] in §7.2; dot-length sequence 1,2,3,4,5 is not interpreted in handoff.
3. **`another door` coordinate reading {1},{4},{21} with #6913 A=1,R=18,B=2** — #8000 says the door hint “still a thing” alongside primes and zeroing; #6884/#6913 April 1 framing is ambiguous (#7529), so this path is cited but not closed [R].

---

## 4. Cross-check

Archivist reproduces all [V] decodes cited above (106/106). This reader file proposes no passwords and performs no decrypts.
