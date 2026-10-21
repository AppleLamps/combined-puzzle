# Constraints on the SalPhaseIon answer (3 October 2026)

**6 October 2026 interpretation notice.** This is a dated research record.
Its candidate counts and original logs are preserved, not freshly rerun.
Read [doc 118](../118-correctness-audit-remediation.md) for detector/coverage
limits and [doc 119](../119-current-evidence-ledger.md) for current findings.
A null applies only to its complete tested tuple.

Constraint grades for opened stages do not transfer to locked stages. The old slot-by-slot kill matrix, universal formatting, and compulsory lock order are superseded. This is not an exhaustive candidate census.

The method is constraint satisfaction. Step 1 lists every constraint on the SalPhaseIon password with its source and a strength grade. Step 2 looks for readings that satisfy all of them at once. Step 3 tests the survivors.

Sources: `jrk_messages.txt` (all 492 creator messages, re-read end to end for this), the dossier (sections 2, 3, 6, 7, 8, 10), docs 114 and 115, `../FAILED-ATTEMPTS-LOG.md`, `../critical-review-2026-10-03.md`, `../riddle-method/README.md` (R1 to R30), `../independent-model/README.md` and `../microstep/README.md`.

Strength grades:
- **P**: proven by computation on an opened stage.
- **D**: a deliberate creator statement, dated and unprompted, or an encoded hint.
- **R**: a reaction (an emoji, one word, or an answer to someone else's framing).
- **I**: an inference made by this project.

## Step 1. The constraint table

### A. Technical (the convention and the containers)

| # | constraint | source | grade | what it rules out |
|---|---|---|---|---|
| A1 | The password is `sha256(answer)` written as 64 lowercase hex characters. | phases 2, 3 and 3.2; the page says "sha256" twice | P for opened stages; I for locked stages | does not exclude a different locked-stage form |
| A2 | The KDF is EVP_BytesToKey with SHA-256 and 1 iteration (the OpenSSL 1.1.0+ default), and the cipher is AES-256-CBC. | phases 2, 3 and 3.2 (MD5 and SHA-1 fail phase 2) | P for the opened stages; I for SalPhaseIon, whose page names no cipher | no universal cipher/KDF exclusion; R15 covers only its stated matrix |
| A3 | Ciphertext lengths excluding headers are 80, 80 and 1,328 bytes, all divisible by 16. This is compatible with padded block encryption, but does not identify the mode or cipher. The 1/4,096 estimate assumes three independent, uniform length residues modulo 16; related short envelopes and structured plaintexts do not establish those assumptions. | sizes, dossier 6.5 | P for lengths; I for cipher hypothesis | no stream mode excluded; padding-based detectors leave those modes untested |
| A4 | Under the 16-byte CBC/ECB PKCS#7 hypothesis, 80 ciphertext bytes imply 64 to 79 plaintext bytes. A 64-hex key (64 B) or a 64-hex key plus `\n` (65 B) fits; a bare WIF or bare BIP38 does not. | dossier 6.5 | I for locked stages | WIF or BIP38 as the whole plaintext only under this padding hypothesis |
| A5 | The two base64 halves joined form one 96-byte container. `enter` sits exactly where `openssl -a` wraps at 64 characters. | dossier 6.1, 6.2 | P for the layout; exact short-envelope bytes also match the May 20, 2021 community README (doc 119) | b1 standalone (low prior, see section 4) |
| A6 | The final prize is "a private key" (#4624), a "Regular Bitcoin Private key" (#20223), "the encrypted private key stored online" which "the solver will find a way to 'decrypt'" (#7832, #7834). | creator | D | seed phrases and brain wallets as the final form; the win test still covers sha256 of every candidate |
| A7 | Known assemblies use stage-specific formatting. Phase 3 retains Safenet/Luna/HSM case, uppercase hex with lowercase 0x, and FEN spaces; the page uses aBa and connected not enf tags. SalPhaseIon has no such format tag. | dossier 3.3 and captured phase2_choice.html | P for exact accepted stage strings | no universal lowercase/no-space rule; locked-stage formatting remains open |

### B. Dated creator claims about the remaining steps

| # | date, id | claim | what solvers had then | grade | what it bounds |
|---|---|---|---|---|---|
| B1 | 2019-05-18 #881 | The key can be found without the Roses poem. | phase 3 | D | the poem is a help, not a required operand |
| B2 | 2021-01-21 #5717 | "a few might not require the internet anymore" | a few were at the side page | D | from the side page on, the material is enough |
| B3 | 2021-03-14 #6509 | An "unforseen hint" on `matrixsumlist` was already given; that is #5966 "You are at the prime part already???", which he flagged himself in #5969. | labels decoded; no dbbi parse | D | `matrixsumlist` comes after, or uses, the prime part |
| B4 | 2021-12-26 #8000 | "There is another door" still holds; primes are required to proceed; some characters must be "zeroed out" along the way. | labels decoded since April 2021 (#7360) | D | primes and a zero rule somewhere in the remaining path; both are already used once by the label decode (`o` = 0) and the dbbi walk |
| B5 | 2023-01-09 #8330 | "At least prime number is very important to get any further." | as above | D | same as B4 |
| B6 | 2023-01-12 #8352 | "I checked a certain GitHub ... You guys are really getting close." | a community repo we cannot see | D | the community framework of early 2023 was on track |
| B7 | 2023-02-23 #8446 | Order: yellowblueprimes, matrixsumlist, lastwordsbeforearchichoice, yinyang. "we wont give away the password its in front of your eyes but youre not seeing it very last step is a true giveaway promised". The whole message is bit-reversed. | labels | D (encoded, the promised hint) | the order of operations; "the password" is visible to solvers; the final step is trivial |
| B8 | 2023-08-03 #8796 | "Actually, the hardest part is done." | labels, #8446 | D | what remains should be easier than reaching and decoding the side page |
| B9 | 2023-08-06 #9599 | "Once you hit a 'ying yang', you'll be able to solve it the same day." | same | D | yinyang is the last hard step |
| B10 | 2023-08-06 #9607 | Another URL? "No need. You have all the info." | same | D | no further door or URL to find |
| B11 | 2023-11-24 #16624 | Given the available knowledge, is internet still needed? "Nope." | same | D | the referents are in held material or common knowledge |
| B12 | 2024-11-29 #32579 | "If you guys got 1 microstep further, the puzzle will likely be solved the same day." | every label; no dbbi parse | D | the creator described it as small; lack of a public parse does not prove independence from DBBI |
| B13 | 2025-04-28 #39224, #39237 | When yinyang is reached, "2 hours max". Yinyang is found after decoding an AES ciphertext: "It's the next phase." | same | D | a next-phase relation is stated; no named envelope, unique ordering, or both-label assembly is established |
| B14 | 2026-07-12 #66588, #66589 | SalPhaseIon is solvable: "Yes"; the puzzle was "verified many times back then after some sad rushed mistakes". | same | D | the containers and page are as intended |
| B15 | 2026-09-01 #70336, #70377 | "Couple hours" to make it; "Same same" to "two sloppy days". | dbbi parsed | D | each step is cheap to build |
| B16 | 3.2 plaintext (2019), creator-authored lines | "return to the source codes ... the code you hopefully carry, reinserting the prime basics, after which you will be required to select from over twenty three ciphers sixteen encryptions and/or seven intertwined passwords to find the actual private key. note that also brute forcing might be required." | in-artifact | D | after 3.2 there is a selection step, and the creator expected that some brute force might be needed |

### C. Reactions

| kind | id | to what | reading |
|---|---|---|---|
| dismissed | #5960 | the spelling "hundred fourty" | the spelling response endorses neither 104 nor a 140 binding; part 6 separately has 140 characters |
| dismissed | #6250, #6252 | his own "Infrared" | a joke, disowned in 19 seconds |
| dismissed | #7529 | the April 1 "{1},{4},{21}" | April Fools |
| dismissed | #1806 | typos | "No clues to be found in those typos" |
| dismissed | #12653, #60326, #32699 | OP_RETURN text, jrk.agency binary, the /PUZZLE page | not puzzle material |
| dismissed | #70307 | the YOUWON pivot | "Pfff. Coincidence." |
| joke | #32671, #32613, #8353 to #8356 | last digit of pi, ASCII 127, sqrt(-1) and the theory of everything | jokes in reply to jokes; #8354 continues the #8308 physics joke, so "42" (#8385) carries little weight |
| self-description | #66938 | "in a matrix cypher kinda way" | describes his life (Cypher chose the illusion); not a hint |
| silence | #20224 🤐 | "our first hint is your last command ... the 2nd to last piece" | not denied |
| silence | #32570 🤐, #60307 🤐, #66600 🤐 | "doesn't remember how to solve it", "just the btc?", "some already found it" | no puzzle content |
| silence | #70325 🤐 | dbbi and faed: decode or ingredient? | no direction |
| endorsed | #4096, #4102 | the Roses poem; "answer is there" | strongest planted hint; it maps onto the second door and the dbbi rule |
| endorsed | #7418 | "hash all the text you see" | the side page URL |
| endorsed | #2905 | the rabbit nest and the marked off-white cell | the cell, used by dbbi |
| endorsed | #3902 | "the half of prize went to better half" | the halving, not an operand |
| endorsed | #8311, #8315 | the Cosmic Duality cover | the yin-yang |
| endorsed | #8483 👆🤷‍♂ | the reversed #8446 decode | the decode is right |
| endorsed | #60312 Bingo | "in front of your eyes" as a pointer to *Looking Forward* | attribution uncertain (dossier 8.1); swept, null |

### D. The page itself

| # | constraint | grade |
|---|---|---|
| D1 | Order on the page: dbbi, `matrixsumlist`, faed, `lastwordsbeforearchichoice`, `thispassword`, "sha256 our first hint is your last command", the container (with `enter`), "sha256 [the] ans[wer] too". The literal reads `anstoo`, not `theanswertoo`. | P |
| D2 | The grammar of the opened pages is riddles, then a method line, then the container. Here the labels sit where riddles sat, and the "sha256 ..." line sits where the method line sat. | I, strong |
| D3 | `thispassword` follows the last label directly, and #8446 says "we wont give away the password" directly after its labels. So "the password" in #8446 is the one `thispassword` names, and it is "in front of your eyes". | I |
| D4 | "our" matches the creator's "A hash which **we** provided" (#257) for #225, his first hint. His first message that calls itself a hint is #867 `giveit = givetit`. | D (wording) |
| D5 | dbbi is a checksum of the poster colour program. A check only makes sense if what it checks is used next, which fits #6509: the prime part comes before `matrixsumlist`. | I |

### E. What the nulls rule out (by class, all with live controls)

| class | scale | where recorded |
|---|---|---|
| poster sum lists (91 list types x 17 encodings), alone, crossed with three last-words pools, with and without `thispassword` | 1.24 billion decrypts, plus 104,885 candidates and the 8.1 million joint passwords of doc 114 | dossier 10.8, 10.9 |
| dbbi with `b` as the merged zero | 4.03 billion | dossier 10.9 |
| every window of the Architect text, the 3.2 intro, the phase-2 plaintext and the checkerboard message as last words, alone and at list-named offsets | ~330,000 | dossier 10.6 to 10.8 |
| the film's door scene, the Hope line, the Merovingian, the six-dot CHOICE, as last words | 6,720 decrypts plus 3,331, and R2, R3, R7, R22, R23 | dossier 10.1, 10.6; ledger |
| riddle readings of every label (R1 to R30), alone, joined, sha-each-then-join, with the first-hint variants, newline forms and as-written forms | ~600 distinct candidates under 3 testers | ledger |
| "our first hint" candidates, the side-page hash as the first hint | 237 and 595 | dossier 10.5, 10.7 |
| the same answers under 14 ciphers x 5 KDFs | 443,520 | R15 |
| chain-order combinations of the chain atoms | 551 million | dossier 10.1 |

## Calibration: the creator's difficulty claims run optimistic

Several constraints in B are statements about how close or how small the remaining work is (B8, B9, B12, B13, B15). His own messages show those estimates are consistently off:

- #879 (2019): a team's progress was "unforseen as we expected it to take at least a !month!".
- #4590 (2020): "Really nobody managed to find the extra door, didn't expect that".
- #8796 (2023): "the hardest part is done", and the puzzle is still unsolved three years later.
- #32579 (2024): "1 microstep", and 22 months on nobody has taken it.

So these claims say what he finds obvious, not how much work is left. B12 reports the creator's perception of difficulty. It does not prove that the intended step needs no DBBI parse or that its route is uniquely determined.

## Step 2. Enumeration

Every reading has four slots: the referent of `matrixsumlist` (M), the referent of `lastwordsbeforearchichoice` (L), the assembly (f), and the form. B7, B13 and D1 motivated a joint M/L model, but do not fix its assembly, receiver or lock order.

### Slot M

| referent class | killed by |
|---|---|
| the poster grid, any sum list | E (1.24 billion, 1,558 lists x 17 encodings) |
| the dbbi colour program (5x5) | E (327 candidates; 82,710 three-slot crosses) |
| the film's "sum" sentence (`yourlife`), the 23/16/7 selection, `trace`, `theone`, `neo` | E (R1, R8, R11, R12, R14) |
| "this puzzle" sums to 101 | E (R19) |
| the chessboard, the phase-2 template | E (doc 102) |
| the textarea streams as matrices | E (7,480), and the row-plus-column theorem (dossier 10.5) |
| the checkerboard or the Beaufort key as "the matrix" | no reading names a unique list; fails "one candidate per reading" before testing |

The listed M configurations produced no validated result. This does not eliminate each referent independently of its partners, formatting and detector, or exhaust all uniquely stated rules.

### Slot L

| referent class | killed by |
|---|---|
| windows of the creator's Architect text, 3.2 intro, phase-2 plaintext, checkerboard message | E, alone and crossed with poster lists |
| the film's door speech as written in ledger R2 (`...nothingyoucandotostopit`) | E (R2) |
| "the problem is", "We won't", Hope | E (R3, R7, the Hope line) |
| the 3.2 intro before "One for one" | E (R20) |
| the faed tail before segment 1 (the "last words before" the label on the page) | E (textarea substrings 404,796; adjacent-operand pool) |

### Slot f

Historically tested assembly families included the following, but exact cross-product membership is not established for every M/L, and doc 118 identifies an omitted 144-form set: M+L, L+M, with or without `thispassword`, sha256 of each part then joined, the #225 hash, the phase-1 answer or `causality` as the last part, `giveit` in front, double hash, and newline suffixes.

### The survivor

The historical constraint exercise selected one unrecorded wording variant for S1; this was not proof that it was the only surviving possibility.

The Architect's last words before Neo's choice are the most natural reading of L. They satisfy B11 (common knowledge to Matrix fans), B7 and D3 ("in front of your eyes but you're not seeing it" echoes the line just before them, "an emotion that is already blinding you from the simple and obvious truth"), and the order constraints. The ledger ran them as `sheisgoingtodieandthereisnothingyoucandotostopit`. Transcripts disagree on one word. Two of the three I could read print "there is nothing **that** you can do to stop it". The historical argument used “inherent **to** the programming” to favor the leesmovieinfo transcript. Later comparison found that phrase is not a unique source fingerprint; the extra “that” varies across transcripts, and film audio was not verified. The phase-3.2 lesson (`giveit` against `givetit`) is that one missing word blocks a right answer, and round 2 found that remembered answers are wrong in their exact form about half the time. No file in this project contains `nothingthatyou` (grep over every ledger and tested list). The 6,720 film pre-door decrypts of doc 49 are not in the repo, so whether they used this wording cannot be checked.

**S1**: L = `sheisgoingtodieandthereisnothingthatyoucandotostopit`, plus its cuts (`nothingthatyoucandotostopit`, `thereisnothing...`), its longer form with "the simple and obvious truth", and its as-written forms, each alone and crossed with every M answer in the ledger (R1, R8, R11 to R14, R19, R6) under the nine assemblies above.

## Step 3. Results

`s1.txt`: 428 candidates.

| tester | decrypts | valid pads | flags | controls |
|---|---:|---:|---:|---|
| `rt.py` (convention, 4 forms, EVP SHA-256 and MD5, 6 containers) | 20,544 | 91 (~80.6 expected) | 0 | key 1; phases 2, 3 and 3.2 open and are recognised |
| `ms.py` (`\n`, `\r\n`, ` \r\n` suffixes) | 46,224 | 161 (~181) | 0 | three planted openssl containers with newline forms opened |
| `ct.py` (14 ciphers x 5 KDFs) | 359,520 | 1,408 (~1,410) | 0 | 11 planted containers recovered (7 made by the openssl CLI) |

Win test (single and double sha256 of every candidate, both point forms): 0 hits. **S1 is null.** Logs: `run_s1_rt.log`, `run_s1_ms.log`, `run_s1_ct.log`.

## Step 4. Historical interpretation of the S1 null

S1 returned no validated result in its tested configurations. The following historical diagnosis does not establish that all surviving mechanisms were excluded:

| constraint | evidence for it | what its failure would explain | verdict |
|---|---|---|---|
| A1, A2 convention | proven three times, page says sha256 twice | little: R15 re-ran every ledger answer under 70 cipher/KDF pairs | keep |
| A5 the archived bytes | exact short-envelope bytes have independent historical corroboration; layout matches an OpenSSL-style wrap | authenticity does not identify cipher, plaintext, order or mandatory use | byte identity supported; route and cipher remain hypotheses |
| B12 microstep / B8 hardest part done | dated and deliberate | nothing: they bound effort, not referents, and they run optimistic (calibration above) | weak as bounds; not the cause |
| **"one reading gives one candidate" (uniqueness)** | holds for every opened stage (chess, checkerboard, cp273, format tags, dbbi) | why the referent can be right and still fail: if the step has a small enumerable choice, one candidate per reading misses it | **most likely wrong for this stage** |

Why uniqueness is the one: it is the only pruning constraint the creator contradicts in his own words **for this stage**. B16 is the paragraph the dossier already reads as the manual for the post-3.2 path, and its added lines say the solver "will be required to select from" a numbered set and that "brute forcing might be required". The opened stages never said that. The critical review's rule (a reading must name one candidate before any decrypt) came from the opened stages. Applied here, it has a known blind spot: a right referent with a small stated choice left open.

Two limits on that conclusion:
1. "To find the actual private key" may place the brute force at the key itself (a speculative split reading of ownership/funding language), after the containers, not at the password. B16 does not say which.
2. Acting on it means a bounded enumeration. That is a coverage run, which Lamps has ruled out for now. So this README stops at naming it.

The historical enumeration records remain useful, but do not globally eliminate poster lists or Architect-text referents. Their candidate membership, partners, forms and detector define their scope.

## Side findings

- **A3 leaves a blind spot.** Stream-mode ciphers are not excluded by the lengths; padding-based tests do not comprehensively cover them. This agrees with doc 118.
- **#8354 and #8385 ("theory of everything", "42") are a joke thread** answering #8308, not a pointer at the phase-2 `H` slot.
- **D4.** The word "our" in "our first hint" matches #257's "a hash which **we** provided". That supports the dossier's reading (#225, the method) over #867.
- **Not done:** the community's early-2023 state (B6) and its "remarkable" partial solve (#9627) live in records outside this project.
