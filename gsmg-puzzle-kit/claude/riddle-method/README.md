# Riddle method: retrodiction check and first riddle answers (3 October 2026)

**6 October 2026 interpretation notice.** This is a dated research record.
Its candidate counts and original logs are preserved, not freshly rerun.
Read [doc 118](../118-correctness-audit-remediation.md) for detector/coverage
limits and [doc 119](../119-current-evidence-ledger.md) for current findings.
A null applies only to its complete tested tuple.

Statements that every operation was executed or that 140 is consumed by genesis are superseded. Prime reinsertion may already be DBBI; the carried-code/genesis identification is a solver hypothesis. Formatting and film wording remain stage/source-specific.

Follows `../critical-review-2026-10-03.md`. Everything here ran on one core in under a second per run.

## Files

| file | does |
|---|---|
| `retro.py 'CMD'` | Retrodiction check. Feeds `CMD` the text a solver could see before phase 2, phase 3 and phase 3.2, and counts a stage as passed only if a candidate decrypts to the **known plaintext** (sha256 match), not just to a valid pad. |
| `gen_windows.py` | A stand-in for the data-derived pools (`lw_words`, `subs`, book sweeps): every 1 to 12 word run and every 4 to 40 letter substring of the visible text. |
| `gen_riddle.py` | The riddle method written out: one named outside referent per riddle, joined in the stated order. Its answer table is filled from the known solutions, so it passes by construction and is **not** a blind test. It is regression verification of known answers and marker dispatch, not independent generative validation. |
| `rt.py FILE...` | Small-batch tester for riddle answers. Runs controls first (key 1; phase 2, 3 and 3.2 open and are recognised), then tries each candidate on all six containers under hex sha256, double-hash and raw forms, EVP SHA-256 and MD5, with a structure check on every valid pad and the win test (single and double hash) on the candidate and on every 32-byte window of any flagged output. |
| `riddles.txt`, `riddles2.txt` | The candidates tested, with the reading and its justification as `#` comments. |

`GSMG_KIT` sets the path to the kit's `*.b64` files and `phase2_choice.html` (default: the repository root, two levels above this folder).

## Retrodiction result

| method | phase 2 | phase 3 | phase 3.2 |
|---|---|---|---|
| text windows (`gen_windows.py`), 61,655 to 98,118 candidates per stage | not opened | not opened | not opened |
| known-answer regression fixture (`gen_riddle.py`), 2 to 3 candidates per stage | opened | opened | opened |

On a first pass the check counted any valid pad as "opened", so the text windows appeared to pass 3/3 on random pad-1 events. Comparing the decrypted body with the known plaintext hash fixed it. Any future check needs the same guard.

## Riddle answers tested

Lowercase, joined with nothing between them, as the 3.2 riddles were (`aa, connected`).

| label | reading | answer |
|---|---|---|
| `matrixsumlist` | The Architect's only line that selects "from the matrix" a list whose numbers make a sum: "23 individuals, 16 female, 7 male" (16 + 7 = 23). The creator kept the numbers and cut "the matrix" from that line. | `twentythreesixteenseven` (also written `231607`) |
| `lastwordsbeforearchichoice`, reading 1 | The Architect's last words before Neo picks a door. The creator's Architect text deletes the whole door scene. | `sheisgoingtodieandthereisnothingyoucandotostopit` (also cut to `stopit`) |
| `lastwordsbeforearchichoice`, reading 2 | Taken literally: the words the Architect says just before he says "choice" ("the problem is choice"). | `theproblemis` |
| `thispassword` / "our first hint is your last command" | Join the answers in label order. Variants: the first hint (#225's hash, or the phase-1 answer) as the last part, the reverse order, and `enter` or a newline between the two. | assemblies in the files |

36 candidates in total, each alone and assembled, 1,728 decrypts. Result: **null**. 6 valid pads against about 6.8 expected, all pad 1 or 2 with no structure, and no win-test hit.

Before this, the selection line had only been used as a selection rule over atoms (doc 114). The door line and `theproblemis` had only been run under PBKDF2 (failed-attempts log T47), in the 21-string Cosmic reader, and probably in the 6,720 film pre-door decrypts. These two answers had never been joined into one password before.

## What the null means

The answers above are wrong, or the assembly is. It does **not** argue for widening the readings into pools. The next step is another reading, each one justified in a sentence and tested the same way.

## Round 2 (3 October 2026, evening)

### Blind retrodiction attempt: contaminated, so not a valid test

A fresh subagent got only the text a solver could see before phase 2, 3 and 3.2, with no tools, and was asked for one answer per riddle with a one-sentence justification. It **recognised the puzzle and said it remembered the published solutions**, so the test is not blind. Any current LLM will probably have the same problem, because the solutions are public. Its results, checked with `retro.opens` against the known plaintexts:

| stage | its answer | opens? |
|---|---|---|
| phase 2 | `causality` | yes |
| phase 3 | seven parts, with the FEN's side-to-move flipped to `b` but the move Rg6-c6 never played (`6R1` kept in rank 3) | **no**, primary and alternative both fail |
| phase 3.2 | `jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple` | yes |

Two things to take from it. The derivation of part 5, which it reasoned from the text (Norton's theorem, then McAfee, Belize, presidents named John, JFK, EO 11110), is a fair example of the reasoning depth these riddles need. And a remembered answer is wrong in its exact form as often as not, so every answer has to be tested, never assumed. A clean blind test would need a human who does not know the solutions.

### Ledger

Every row ran through `rt.py`: controls first, all six containers, four password forms, both EVP digests, the structure check and the win test.

| id | label | reading (one sentence) | answer(s) | result |
|---|---|---|---|---|
| R1 | matrixsumlist | The Architect's only line that selects a list "from the matrix" whose numbers sum (23 = 16 + 7); the creator kept the numbers and cut "the matrix". | `twentythreesixteenseven`, `231607` | null |
| R2 | lastwordsbeforearchichoice | The Architect's last line before Neo picks a door; the creator's version deletes the door scene. | `sheisgoingtodieandthereisnothingyoucandotostopit`, `stopit` | null |
| R3 | lastwordsbeforearchichoice | Literal: the words the Architect says just before "choice". | `theproblemis` | null |
| R4 | thispassword / "our first hint is your last command" | Join the answers in label order, with the first hint as the last part. | R1 x R2/R3 assemblies (`riddles.txt`, `riddles2.txt`) | null |
| R5 | thispassword + "sha256 our first hint is your last command" | This page's password is the first hint itself (#225, the sha256 of the phase-1 answer). | the #225 hex, the phase-1 answer (with double-hash forms) | null |
| R6 | yinyang | Neo's opposite, "the equation trying to balance itself out" (the Oracle, Revolutions), which is Smith. | `smith`, `agentsmith` | null |
| R7 | lastwordsbeforearchichoice | The Architect's literal last words in the scene, "We won't."; #8446 puts `wewont` right after the labels. | `wewont` | null |
| R8 | matrixsumlist | "Your life is the sum of a remainder ... of the matrix", so the sum is Neo. | `neo` | null |
| R9 | "sha256 the answer too" | Hash each answer, join the hex digests, then the usual sha256; also plain joins and `+yinyang`. | {R1, R8} x {R2, R3, R7} (`riddles3.txt`) | null |
| R10 | enter | The line break `openssl -a` puts between the two 64-character base64 lines; already consumed (dossier 6.2). As a joiner it is covered in R4. | n/a | consumed |

Totals for rounds 1 and 2: 78 candidates, 3,744 decrypts, 14 valid pads against about 14.7 expected, 0 flags, 0 win-test hits.

### Status

These are all the readings I can justify in one sentence from in-artifact text and the film. Others I considered (the Architect text before `SELECT`, the Hope line, Oen/One/Neo, the 23/16/7 selection) already appear as nulls in the dossier. The next reading needs a new referent, not a variant of these.

## Round 3 (3 October 2026, late)

### The review's section 5 and 8 readings

- **Section 5** re-dates the Roses poem to the solved second-door and dbbi stage. It retires a hint; it names no password, so there is nothing to decrypt.
- **Section 8** gives three framings. "Labels as stage names" (each label is its own riddle for its own lock) was already exercised: `rt.py` tries every candidate alone against every container, so R1 to R8 ran under it. "Labels as the riddle sheet" (answers joined in label order, `sha256 the answer too`) is R4 and R9. "Matrix means the film" is R1 and R8.
- What section 8 still left open was its own example: the sum sentence read through the film. That is R11 and R14 below.

### Ledger

`riddles4.txt`. Each matrixsumlist reading is tried alone and joined with the four film lastwords answers (R2 in full and cut, R3, R7) under six joins: M+L, L+M, sha256 each then join, M+L+the #225 hex, M+L+the phase-1 answer, M+L+`yinyang`. The film lastwords answers come from outside every captured text, so no earlier windowed pool held them.

| id | label | reading (one sentence) | answer | result |
|---|---|---|---|---|
| R11 | matrixsumlist | The film's only "sum" sentence is "Your life is the sum of a remainder ... of the matrix", so the matrix's sum is your life. | `yourlife` | null |
| R12 | matrixsumlist | The standard sum of a matrix is its trace, and "Trace program: running" is the first text on screen in *The Matrix*. | `trace` | null |
| R13 | matrixsumlist | #6509 (14 March 2021) says an unforeseen matrixsumlist hint was already out; the only unprompted one-word clue in the fortnight before is "Infrared" (#6250), disowned at once. Never tried inside a longer passphrase (log section 8, gap 5). | `infrared` | null |
| R14 | matrixsumlist | The sum line continues "You are the eventuality of an anomaly": the remainder is the One (the creator wrote THE YOU). | `theone`, `anomaly` | null |

125 candidates, 6,000 decrypts, controls fired, 26 valid pads against about 23.5 expected, 0 flags, 0 win-test hits.

Running total, rounds 1 to 3: 203 candidates, 9,744 decrypts, 0 flags.

### Where this leaves the method

The creator's 492 messages were re-read end to end for statements about command order or what the labels refer to. Beyond what the dossier already records (#8446's order, #6509, #20224, #39237), there are none. The song is spent as text (dossier 3.A) and is not in the project. So the readings an AI can justify in one sentence from available material are used up, and the blind retrodiction test (round 2) showed that an AI cannot tell its own reasoning from its memory of published answers.

One part of the review's reasoning is too strong. It says data operations never produce passwords. But the creator's own additions to the Architect text describe this exact stage as a procedure ("reinserting the prime basics, after which you will be required to select from over twenty three ciphers sixteen encryptions and/or seven intertwined passwords ... note that also brute forcing might be required"). #8000 says primes are required and characters must be "zeroed out", and phase 3 included two exact transformations (reversed genesis hex, the FEN after a move). The fair reading is that every label is a riddle *whose answer may be an operation*, stated exactly, with no free parameter. That keeps the review's rule (one reading, one candidate) without ruling out a stated operation.

## Round 4: the creator's inserted Architect lines as stated operations (3 October 2026)

Each creator-authored addition to the Architect text, read as one exact operation on one named object, checked against the dossier, docs 114/115 and the failed-attempts log. No new run was made in that round. The table records earlier interpretations and tests; it does not show every literal reading was exhausted.

| inserted line | literal operation | executed? |
|---|---|---|
| "return to the source codes" | read the page source | yes: textarea decoded (dossier 6); every archived HTML string, 1,670 (10.5); log's 1008 pointer to `TORETURNTOTHESOURCECODES` |
| "reinserting the prime basics" ("prime program" in the film) | put back what sits at prime positions | yes: dbbi prime walk (solved); zero reinsertion into dbbi and faed to k=18, 18.8B nodes (doc 75); 15 prime-basic cells reinserted, 576 (log T24); prime masks over known answers, 220 (T44) |
| #8000 "characters need to be zeroed out" | replace characters with 0 | yes: merged-zero dbbi 2^25, 4.03B (doc 115); faed zero-substitution exhaustive under rule 2 (10.6); prime-position zeroing of published text (10.5); zeroed poster text, 857 variants (doc 106). Only faed with arbitrary `g` (2^107) is open, not enumerable |
| "select from over twenty three ciphers sixteen encryptions and/or seven intertwined passwords" | select 23 / 16 / 7 items and intertwine them | yes: 22,221 selections and interleaves over the 23 chain atoms (doc 114); L=84 23/16/7 host sets as selectors into nine texts (doc 97); R1 as a word. The numbers are the film's own (doc 45) |
| "brute forcing might be required" | an instruction, not an operation | n/a |
| "what a wise man above hinted at is worth hundred fourty of the investment" | 140 | part 6 separately has 140 characters; a binding or consumed role is not established (doc 119) |
| "the code you hopefully carry", "help us build it", "take the private key", "CIAO BELLA O", doubled SELF | no stated operation | n/a (the last two sit in the surplus list) |

Corrected conclusion: the listed interpretations have historical tests, but receiver, selection, assembly and exact numerical binding remain unknown; no exhaustive instruction-level exclusion follows. Outside input is off the table under Lamps's rule (3 Oct 2026: nothing that requires another person). The next input must be a new angle from Claude.

## Round 5: independent re-derivation and the convention matrix (3 October 2026)

Model, divergences and tooling in `../independent-model/README.md`; tester `../independent-model/ct.py` (4 forms x 5 KDFs incl. PBKDF2-SHA256 10,000 x 14 ciphers; 11 planted controls, 7 made by the openssl CLI, all recovered).

| id | label | reading (one sentence) | answer(s) | result |
|---|---|---|---|---|
| R15 | convention | None of the three locked containers names its cipher or KDF (phases 2, 3 and 3.2 did), so every ledger answer R1-R14 is re-run under 13 more ciphers and PBKDF2. | R1-R14 assemblies | null |
| R16 | "our first hint" | The creator's first message that calls itself a hint is #867 "giveit = givetit" (#225 was "a hash which we provided"). | `giveit = givetit` and variants | null |
| R17 | "is your last command" | #8446 "in front of your eyes" / "true giveaway" echo phase 3's "add giveit in front of the answer". | `giveit` + R1-R14 answers and labels | null |
| R18 | "Raising the stakes without extra chances of winning" | Key stretching (`openssl -pbkdf2`) raises an attacker's cost without changing the odds; the sentence sits right above the Terminal. | PBKDF2-SHA256 10,000 on every candidate in this round | null |
| R19 | matrixsumlist | The creator swaps "the matrix" for "this puzzle"; the puzzle's matrix sums to 101 set cells, which is Neo's room number. | `101`, `onehundredone`, ... alone and joined | null |
| R20 | lastwordsbeforearchichoice | The only choice the 3.2 Architect makes is the blank pair "One for one, four for one"; the words before it. | `abeautifulstrategicposition`, `strategicposition`, ... | null |
| R21 | thispassword | Self-reference: the encoded form on the page is the password. | segment strings, their digits, the binary runs | null |

528 candidates, 443,520 decrypts, 1,702 valid pads against about 1,740 expected, 0 flags, 0 win-test hits. R15 re-runs the 211 earlier ledger candidates; 317 candidates are new. Running total of distinct candidates, rounds 1 to 5: about 520.

## Round 6: per-lock split (3 October 2026)

Assignment table, rejected alternatives and already-null locks: `../independent-model/README.md`, round 6. Frame: SalPhaseIon = salvation = the film's right door ("the Source, and the salvation of Zion"); the Terminal = the left door ("back to the Matrix, to her").

| id | lock | reading (one sentence) | answer(s) | result |
|---|---|---|---|---|
| R22 | Terminal | `lastwordsbeforearchichoice` + `thispassword` serve the only lock with no riddle: the Architect's last words before he presents the doors. | `theanomalyrevealedasbothbeginningandend` and cuts | null |
| R23 | Terminal | Same label, literal: his words before his own word "choice". | `asyouadequatelyputtheproblemis`, `asyouadequatelyput` | null |
| R24 | Terminal | The left door leads "to her", the better half of the 3.2 checkerboard. | `trinity`, `her`, `backtothematrix` | null |
| R25 | short | The right door leads to the Source; the creator added "return to the source codes". | `thesource`, `source`, `thesourcecodes` | null |
| R26 | short | The phase's name, decoded per #6497. | `salvation`, `thesalvationofzion`, `zion` | null |
| R27 | Cosmic | The duality is the pair of doors, or Neo and Trinity. | `therearetwodoors`, `neoandtrinity` ... | null |
| -- | short | `matrixsumlist` alone | R1, R8, R11-R14, R19 | already null, not rerun |
| -- | Cosmic | sha256 of the short plaintext | n/a | untestable until short opens |

25 candidates: 1,200 decrypts under the convention (3 pads, ~4.7 expected) and 21,000 under the 14-cipher tester (81 pads, ~82 expected), 0 flags, 0 win-test hits, controls fired.

## Round 7: the two dated creator claims (3 October 2026)

Timeline and derivation: `../microstep/README.md`. #6509's "unforeseen hint" is the prime slip #5966 (self-declared in #5969), already consumed by the dbbi parse, so it gives no new string. At #32579 the community held every label but not the dbbi parse; a "microstep" is read as a change of form.

| id | label | reading (one sentence) | answer(s) | result |
|---|---|---|---|---|
| R28 | form | The page is a terminal transcript and the creator wrote on Windows, so `echo ANSWER \| sha256sum` adds `\n`, `\r\n` or ` \r\n` to the hashed answer. | every ledger answer R1-R27 and R29-R30, three suffixes, `ms.py` | null |
| R29 | form | The SalPhaseIon page alone has no `/(...)` format tag, so the answer is typed as written, with its case, spaces and punctuation. | film lines and sum readings as written (`natural.txt`) | null |
| R30 | thispassword / "our first hint is your last command" | The gif in the #32579 sitting is causality, and the puzzle's first numbered hint ("1...") "will grant the first part"; mirrored, its answer goes last. | lastwords and matrixsumlist answers + `causality` (`causality_last.txt`) | null |

599 candidates, 64,692 decrypts under M1's forms (240 pads, ~254 expected), 2,256 under the convention and 39,480 under the 14-cipher tester, 0 flags beyond the phase-2 control, 0 win-test hits. Controls fired in all three runs, including three planted openssl containers keyed with newline forms.

## Round 8: constraint table (3 October 2026)

Table, enumeration and verdict: `../constraints/README.md`. Every constraint (convention, dated creator claims, reactions, page structure, nulls) was pooled and the readings intersected. One cell survived: the canonical last-words answer in the exact wording of the transcript the creator copied (his Architect text reads "inherent to", which pins a transcript printing "nothing **that** you can do"; R2 had used "nothing you can do").

| id | label | reading (one sentence) | answer(s) | result |
|---|---|---|---|---|
| R31 | lastwordsbeforearchichoice | The Architect's last words before Neo's choice, in the wording of the creator's own transcript source. | `sheisgoingtodieandthereisnothingthatyoucandotostopit`, cuts, as-written forms; alone and x every ledger M answer x 9 assemblies (`../constraints/s1.txt`) | null |

428 candidates: rt.py 20,544 decrypts (91 pads, ~81 expected), ms.py 46,224 (161, ~181), ct.py 359,520 (1,408, ~1,410), 0 flags, 0 win hits, controls fired in all three. Verdict: no reading satisfies every constraint; the constraint most likely wrong for this stage is "one reading gives one candidate", which the creator's own Architect additions contradict ("select from ... brute forcing might be required").

## Round 9: terminal history (3 October 2026)

| id | label | reading (one sentence) | answer(s) | result |
|---|---|---|---|---|
| R32 | "our first hint is your last command" | The page is a terminal transcript, and in a shell your last command is literally `!!` and the first history entry `!1`. | `!!`, `!1`, `!-1`, `!1!!`, `!!!1`, `sudo !!` (`riddles5.txt`) | null |

6 candidates, 288 decrypts, 0 valid pads (about 1.1 expected), 0 flags, 0 win-test hits, controls fired. Context and the one-password model: `../rabbit-holes/README.md`, follow-up 2.
| R33 | matrixsumlist | The creator's own sum sentence says "your life is the sum of a remainder of an unbalanced equation inherent to the programming of this puzzle"; the poster program spends 192 of 196 cells, the remainder is the four centre cells (`0000`), whose sum is zero (#8000 "zeroed out"); also the dbbi leftover B, Y as 1 + 2 = 3. | `zero`, `0`, `0000`, `fourzeros`, `three`, `3`; alone and with 8 top L answers as M+L, L+M, M+L+`thispassword`, sha256-each-joined (`riddles6.txt`) | null |

R33: 198 candidates; rt.py 9,504 decrypts, 38 valid pads (about 37.3 expected); ct.py 166,320 decrypts, 635 pads (about 652 expected); 0 flags, 0 win-test hits; controls fired in both.

## Round 10: "return to the source codes" as Satoshi's genesis comment block (4 October 2026)

Write-up: `../source-pointer/README.md`. The log's 1008/868 pointer cannot be rebuilt from any recorded object and is chance-level (a random index lands on a word start in the instruction paragraph 4.0% of the time; the 140 difference follows from the total). The sentence it lands on was read literally: phase 3 part 6 came from `main.cpp`'s genesis comment block, so "the source codes" are that block's other values.

| id | label | reading (one sentence) | answer(s) | result |
|---|---|---|---|---|
| R34 | any lock | "Return to the source codes ... the code you hopefully carry": go back to the genesis comment block in Satoshi's `main.cpp` that part 6 (140 chars) came from and use its sibling codes. | genesis scriptPubKey (reversed hex), genesis hash, merkle root, the full scriptSig line, nValue/nTime/nBits/nNonce, the decoded headline, the block joined; as written, lowercase, no `0x` (`../source-pointer/cands.txt`) | null |

R34: 21 candidates; rt.py 1,008 decrypts, 5 valid pads (about 4.0 expected); ct.py 17,640 decrypts, 78 pads (about 69 expected); 0 flags, 0 win-test hits (also hash and merkle root as raw scalars); controls fired in both.

## Round 10 (4 October 2026): genesis construction, second pass

Write-up: `../genesis-main-cpp/README.md`. Row 1616 is now pinned: of every `bitcoin/bitcoin` release tag from v0.1.5 to v0.4.0, only **v0.3.10** has the scriptSig comment on row 1616 (v0.3.12 onward drops that comment line). Retrodiction passes: row 1616 of v0.3.10, text after " 4 ", rebuilds the phase-3 password by script.

| id | label | reading (one sentence) | answer(s) | result |
|---|---|---|---|---|
| R35 | any lock | The parts of the v0.3.10 genesis construction R34 left out: the raw coinbase bytes the dump prints, "after 4" read on those raw bytes, the public key un-reversed with its hash160 and address, the release name, the temporary debug print, the dump's own output, and row 1616 as a whole row. | coinbase hex, `455468...`/`5468...` headline hex, `04678afd...`, `62e907b1...`, `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`, `v0.3.10` forms, `debugprint`/`debug print, delete this later`, CBlock line, dump rows, row 1616 (`../genesis-main-cpp/cands.txt`) | null |

R35: 27 candidates + 2 newline forms; rt.py 1,296 decrypts, 5 valid pads (about 5.1 expected); ct.py 22,680 decrypts, 100 pads (about 89 expected); 0 flags, 0 win-test hits; controls fired in both, plus an openssl-made container keyed by a candidate drawn from this file.

Non-candidate check, 4 Oct 2026: the poster photo itself re-examined directly (chunks, alpha, hidden-mark scan, logo LSB, QR at codeword level with RS check, glyph determinism), every check with a planted control that fired. Nothing hidden; the QR is standards-clean (ECI 26, standard pad EC 11 EC, parity matches). Write-up: `../photo-analysis/README.md`. No candidates added.
