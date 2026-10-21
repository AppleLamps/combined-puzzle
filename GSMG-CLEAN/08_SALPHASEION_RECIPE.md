# 08 — SalPhaseIon labels read as a recipe (2026-09-13)

**Context-audit qualification (10):** this is one unproven recipe, not an established algorithm. L5 is an optional, separate hypothesis. The creator's “feeling of the phase's name” describes progress and must not be used as a required plaintext-content filter. `enter` and the common `shabef` prefix have strong explanations; the full semantics of `anstoo` and field roles remain unproven. The 755 pad-valid referent outputs are retained as unresolved, with no authenticated result found.

**Why this file exists.** In the session diagnosis I argued that every solved GSMG step handed the solver a self-check: a URL, readable text, a hash to match (#225), or a decode that obviously worked. Nulls from the pad-byte envelope oracle carry almost no information. The SalPhaseIon page is the one place where the creator wrote labels right next to the unread material. This file reads those labels in stream order, as instructions. For each step it records:
- what is **exact**
- what the creator said
- what was **already tested**
- what a **self-checking** result would look like

This is a reading and bookkeeping pass. **No new decrypts were run.** Labels: [checked] = verified in files here; [log] = from a prior ledger, not re-run; [inference] = my reading.

## 0. Three facts that shape every reading

1. **The page uses three encodings, and all three are decoded.** [checked, 01 §6]
   - **a/b binary** (a=0, b=1, 8 bits): `matrixsumlist`, `enter`
   - **a–i/o decimal** (a..i=1..9, o=0 → decimal → integer → bytes): `lastwordsbeforearchichoice`, `thispassword`
   - **plain letters with letter-digits**: `sha` + **b=2, e=5, f=6** = **sha256**. So `shabefourfirsthintisyourlastcommand` = "sha256 our first hint is your last command", and `shabefanstoo` = "sha256 ans too" (round 1, `rabbit_r1/FINDINGS_round1.md:598`).
   - DBBI and FAED use **only a–i**. That is the decimal alphabet **minus `o`** (no zeros).
2. **`enter` is where OpenSSL breaks the line.** [checked 2026-09-13]
   - `openssl enc -a` wraps base64 at 64 characters.
   - The SalPhaseIon envelope is exactly 64 characters `[895:959]`, then `enter` `[959:999]`, then 64 characters `[999:1063]`.
   - The same wrap shows up elsewhere by the same author:
     - the Terminal envelope inside the Phase 3.2 plaintext is a 64-character line, CRLF, then the rest (`data/phase3_2_plaintext.bin`, from byte 2292)
     - the Cosmic textarea on the page is 28 lines of 64 (27 newlines, `originals/pages/salphaseion_phase3.html`)
   - So `enter` most simply records the newline in the creator's own `openssl -a` output. It carries no key material. This fits the finding that adding CR/LF gives the same 96-byte envelope (06 §4).
3. **The shared prefix fixes the parse.** [inference, strong]
   - Both literals begin `shabef` = sha256.
   - So the long literal parses as **`shabef` | `ourfirsthintisyourlastcommand`**, not `shabefour` | `firsthint…`.
   - It reads "sha256: our first hint is your last command", in the same shape as "sha256: ans too".

## 1. The recipe table (stream order)

| # | Range | Text (decoded) | Recipe reading | Creator evidence | Already tested | A self-checking result would be… | Status |
|---|---|---|---|---|---|---|---|
| 1 | [0:91] | **DBBI** (91 × a–i) | Material. 91 = 7 × 13. | Primes are required, some characters get "zeroed out" (#8000, #8330). The `b` positions start 2, 3, 5, 7, 11 (L6). | Very many classical, prime and zero attacks (04 §A, B, E-H/I, J). **Exhaustive:** DBBI is *not* the sibling decimal code with digits zeroed or removed (rabbitv4 H). | (a) DBBI's `bg` tokenisation (64 tokens / 16 codes) equals the repeat pattern of sha256 of some answer (L5; chance ≈ 2⁻¹⁰⁰); or (b) a transform after which the page's own decimal or binary decode gives ASCII. | **Unread.** The L5 hash-pattern check is the strongest self-check on the whole page. |
| 2 | [91:195] | `matrixsumlist` (a/b, 13 chars = 104 bits) | A label between DBBI and FAED: "a list of sums of a matrix". 13 letters, the same as DBBI's 13 columns [inference]. | #6509 (2021-03-14): "I gave an unforseen hint already 🤷‍♂" in reply to "time for a hint on matrixsumlist?" | ~160k matrix-sum constructions (04 §B). Poster row/column sums (01 §6) as candidates. L2 DBBI 7×12 column sums → `hillfexmgsgq`. ZERO 24-cell total 104 = this field's length [log]; ZERO envelope run null. | A sum list that (a) decodes under one of the page's three encodings to text, (b) matches DBBI's L5 pattern after sha256, or (c) reproduces part of DBBI or FAED exactly. | **Open.** The "unforeseen hint" is now identified with good confidence as #5966/#5969 "You are at the prime part already???" / "…That might have been a hint 🤔." (2021-03-01), with #6514 "Hush hush" pointing back to #1710 (09 §1). The operation itself is still unknown; L1/L2 sum lists and their string forms gave an L5/envelope null (09 §3). The direct pipeline (colour primes → 552 row/column sum lists → page decodes or index decodes, 400 shuffle controls) was also null (09 §5). |
| 3 | [195:765] | **FAED** (570 × a–i) | Material. 570 = 2·3·5·19. | Same as DBBI. | Bifid families (L3; seven-key null), 3×3 Bifid 206M, Morbit and Pollux, row selectors (34,272), rabbitv4 H exhaustive zero search. | As for DBBI; a readable plaintext or a decode that fits the page's encodings. | **Unread.** |
| 4 | [766:829] | `lastwordsbeforearchichoice` (a–i/o) | "The last words before the Architect's choice". A pointer to a text. | The 1,539-letter puzzle text contains **no** `CHOICE`. Every choice line and the doors scene are cut; it ends "…ciao bella O" where the film's doors choice would begin (rabbitv4 ARCHITECT_DIFF A4, A12). "Reinserting the prime **basics**" was changed from "program" (A9). | Film and puzzle referents as literal answers: rabbitv3 `salphaseion_focus_2026_09_10.py` (film "the problem is", "beginning, and end", the Hope speech, REINSERTINGTHEPRIMEBASICS…); round 1 `matrix_quotes.py` / `sweep2.py` (incl. "…salvation of zion…"; **round-1 oracles were raw-only**, 04 §G); gemini document literals incl. CIAO BELLA O (186, null); r1 lastw 78,984; v2 lastwords 5,800. | The words, sha256'd, give an L5 DBBI pattern match; or an envelope opens with a readable plaintext. | **Heavily tested as a literal answer.** The structural referents P1–P5 are pinned in 09 §2: P1 is primary, the Scott Manning transcript that the creator quotes in #3390, whose line 105 comes just before _Neo walks to the door on his left_. All suffixes, sentences and clauses of P1–P5 gave an L5 and envelope null (09 §3). |
| 5 | [830:859] | `thispassword` (a–i/o) | With #4: "[the last words before archi choice] = this password". | — | Together with #4 (above). | Same as #4. | Same as #4. |
| 6 | [860:895] | `shabef` + `ourfirsthintisyourlastcommand` (literal) | "sha256 (our first hint) is your last command": the final action is hashing. | #20224 🤐 in reply to a request for a hint on exactly this line. Forward #11248: the "actual first hint" was "Follow the white rabbit". #867 "giveit = givetit" is the first thing the team *called* a hint. #225 posted a sha256 to check answers against. | firsthint SHA×1–8 (8,004); G2 first-hint candidates × plain/reversed/ROT13/Caesar/+Enter/double-sha (15,060); wrapper 7,265; "follow the white rabbit" literal 540. | Under the procedural reading (rabbitv4 §2) this line **is the verification step itself**: sha256 of the right answer is what you compare against, and that is the self-check. The thing it could be compared against on this page is **DBBI's hex-digest shape (L5)**. | **Open.** The procedural reading and the L5 check point the same way [inference]. |
| 7 | [895:959] | envelope, line 1 (64 b64) | Ciphertext. | — | — | — | — |
| 8 | [959:999] | `enter` (a/b, 40 bits) | **The OpenSSL line break** (§0.2). | Round 1 and Diego's "enter = 13224" (EO 13224) reading. | CR/LF variants; "+Enter" on first-hint candidates (G2); EO 13224 text (E2, 821,784). | None needed: the reading is already mechanically complete. | **Explained** [inference, strong]. No key material. |
| 9 | [999:1063] | envelope, line 2 (64 b64) | Ciphertext. SalPhaseIon short, salt `3ab5…`, 80 B, so the plaintext is 64–79 B. | #6497: breaking it "should be giving the feeling of the phase's name" (salvation). #66588 "Yes" (100% solvable). | All envelope sweeps (04). | A plaintext that *reads as salvation* (#6497), not merely pad-valid. | Locked. |
| 10 | [1063:1075] | `shabefanstoo` (literal) | "sha256 answers too": answers are hashed before use. | Matches the **proven** envelope convention: password = sha256(answer) hex (01 §0). | — | Already self-checked: it describes the convention that opened Phase 2, 3 and 3.2. | **Explained** [checked by the proven convention]. |

## 2. What the whole line says, read straight

> [DBBI] **matrix sum list** [FAED] · **last words before archi choice** · **this password** · **sha256: our first hint is your last command** · [cipher line 1] **⏎** [cipher line 2] · **sha256: answers too**

This is the plainest reading [inference]:
- **The bottom half is a user manual for the envelope.** Take the answer, hash it with sha256 (items 6 and 10), paste the two base64 lines (item 8 is the newline), decrypt. Items 8 and 10 are fully explained. Item 6 is a procedure, not a password (see also rabbitv4 ARCHITECT_DIFF §2).
- **The answer is "the last words before archi choice", and that is "this password"** (items 4–5).
- **The top half holds the material and its operation:** DBBI and FAED with "matrix sum list" between them. The recipe reading is that the last words (or the key to finding them) come out of DBBI/FAED through a matrix-sum operation. Nobody has found that operation, and the creator says a hint to it was already given by accident (#6509).
- **L5 fits this reading.** DBBI's `bg` tokenisation has exactly the shape of a sha256 hex digest. If the recipe is "hash the answer", DBBI may *be* that hash, substituted. Then the correct answer checks itself against DBBI with no envelope needed, at a chance of about 2⁻¹⁰⁰. `tools/check_candidate.py` already runs this check on every candidate.

**What this reading predicts, and what would falsify it**
- The broad recipe may yield an answer from items 4–5. Only the additional DBBI-as-substituted-digest hypothesis predicts an L5 match.
- No L5 match rejects that candidate under the additional digest model; it does **not** falsify the broad recipe or reject the candidate as an envelope answer.
- **Weakness:** the L5 shape is post-hoc. About 0.3–1% of shuffles give 64/16 for *some* letter pair (03 §2).

## 3. Next steps (reading and decisive checks only, no pad-oracle sweeps)

1. **L5 back-check over every string already tried.** [done 2026-09-13, null; stopped at 4,443/4,444 jobs, see `runs/2026-09-13_l5_backcheck/REPORT.md`: 16.8 M strings, 1.1 × 10^9 digest checks, 0 hashed-string matches, 8/8 controls]
   - Earlier rounds tested hundreds of thousands of literal answers against envelopes but **never against the DBBI hash pattern**. The L5 check was only built into this folder on 2026-09-13; the dbbi_hex ledger says only an unquantified set was checked.
   - The check is one sha256 plus a pattern comparison per string, with a decisive gate (exact chance 16!/16^64 = 2^-211.7 per digest; older text said ≈ 2⁻¹⁰⁰).
   - Material: the candidate lists that still exist on disk (round 1 `rabbit/tools/*`, rabbitv3 `salphaseion_focus`, rabbitv4 `f_*`/`g_*` materials, gemini literal lists).
   - Unlike a pad-byte sweep, a null here means something for exactly those strings, and a hit would be proof.
2. **Find the "unforeseen hint" for matrixsumlist (#6509).** [done 2026-09-13, see 09 §1: #5966/#5969 "prime part", plus #6514 "Hush hush" → #1710; its sum lists gave an L5/envelope null, 09 §3] Read the creator's messages from the start up to 2021-03-14 (PUZ #1–#6509, plus COMM up to that date) for anything he could later see as an accidental pointer to a matrix sum. Candidates to weigh:
   - #1710 "Yellow has a number and so does Blue" (colour sums → L1 479/484)
   - the poster row and column sums
   - #1837 "Only -41,-17 matters" (41/17 = prime-ordinal sums, 06 §3 item 5)
   - This is a reading task. Its output is a short list of specific sum lists, and each one goes through check 1.
3. **Pin down "last words before archi choice" as a referent, not a sweep.** [done 2026-09-13, see 09 §2–3: referents P1–P5, 15,676 strings, 0 L5 matches, 0 notable envelope results; `runs/2026-09-13_last_words_referents/`] The cut point is known exactly: the puzzle text stops where the doors choice begins (A12), and the Neo "choice" lines were replaced by the creator's own paragraph (A4). Write down the handful of referents this *structure* allows (the last sentence before each cut; the last words of the whole text), then run check 1 on them. Most were already envelope-tested, but not L5-tested.
4. **Do not spend effort on `enter` or `shabefanstoo`.** They are explained (§0.2, item 10).

## 4. Corrections this pass makes elsewhere

- **03 §6** said the parse `shabef`+`our…` vs `shabefour`+`first…` was open. The shared `shabef` = sha256 prefix settles it in favour of `shabef` [inference, strong]. Both parses were tested anyway.
- **07 §1** listed #6712 "Nr 5 in salph" as "number 5 in SalPhaseIon". Read in context it is more likely a head count. A week earlier the creator posted #6491, "Another person (or team) made it to salph", and #6712 sits in a thread about the Decentraland MP3, not about a numbered item. So it plausibly means "the fifth person or team has reached SalPhaseIon" [inference]. It is **not** a pointer to a fifth element.
