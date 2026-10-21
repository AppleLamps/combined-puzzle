# GSMG.io puzzle: what everyone (including us) is doing wrong

**6 October 2026 interpretation notice.** This is a dated research record.
Its candidate counts and original logs are preserved, not freshly rerun.
Read [doc 118](118-correctness-audit-remediation.md) for detector/coverage
limits and [doc 119](119-current-evidence-ledger.md) for current findings.
A null applies only to its complete tested tuple.

The unique-design and one-candidate claims below were methodological hypotheses, not theorems. DBBI uniqueness is grammar-scoped; FAED purpose is unproved and known assembly preserves mixed case/FEN spaces.

Critical review, 3 October 2026. Sources: the repo kit (dossier, docs 114 and 115, `jrk_messages.txt`, the captured pages), `gsmg/FAILED-ATTEMPTS-LOG.md` and its index, and project memory. No sweeps were run for this; the only computation was a few greps and counts, quoted where used. Statements marked INFERRED are my reading, not a measurement.

## Bottom line

1. **Wrong kind of search.** Every password that has ever opened a gate was the answer to a riddle, looked up from outside knowledge (a song, a film, trivia) and concatenated. None was the output of arithmetic on puzzle data. The open containers are being attacked almost entirely with arithmetic on puzzle data.
2. **Wide pools are the symptom.** The creator builds every step so the right reading leaves one candidate. When a reading leaves thousands (17 encodings x 91 list types x forms x crosses), the riddle has not been solved, and crossing two such pools multiplies two small priors.
3. **The acceptance bar rules out the answer type that has always worked.** "Exact structural fit against a shuffle null" fits data operations like the dbbi parse. `causality` or `jacquefresco...` would fail it.
4. **Hints are being reused and over-read.** The Roses poem maps line by line onto the stage it was posted for (the second door and the dbbi colour rule), which is solved. Its imported "primes {2, 5, 7}" then drove the largest operand runs.
5. **The scale contradicts the creator.** "Couple hours" to build it, "1 microstep" away in November 2024 (before dbbi was even parsed), "same day" once yinyang is hit. A 7.3-billion-decrypt search space is the wrong shape for that puzzle.
6. **Compute follows what is enumerable, not what is likely.** More than half of doc 115 went into an object the dossier had already classified as consumed.

The project's controls, recogniser and data hygiene are excellent and should stay. The problem is upstream of them: what gets fed in.

---

## 1. How the opened gates were actually solved

| gate | clue on the page | reasoning step that cracked it | where the answer came from | answer on the page? |
|---|---|---|---|---|
| poster | 14x14 two-colour grid | recognise a medium (spiral, 8-bit ASCII) | the image | yes, as bits |
| phase 1 | rebus: WARNING, LOGIC, CAN YOU DIG IT | identify the song, quote its phase-two opening to the comma | outside: the song | no |
| phase 2 | "1... are you looking for the private keymaker?" | Matrix Reloaded, the Merovingian | outside: the film | no |
| phase 3 | seven numbered riddles plus format tags | seven trivia lookups (SafeNet, Luna, HSM, EO 11110 via a multi-hop chain, genesis bytes reversed, the one non-mating chess move), concatenated in numbered order | outside: trivia | no |
| phase 3.2 | three riddles | Fresco's *The Choice Is Ours*, the Cheshire Cat's "just one second", Heisenberg | outside: film, book, physics | no |
| Architect text | intro names the cipher (Beaufort, 1141) | decode as stated | in the artifact | produced a message |
| checkerboard | riddle spells the key | decode as stated | in the artifact | produced a message |
| dbbi | label `yellowblueprimes` | colour program walked at primes | in the artifact | produced a check (91/91), no password |

Checked by grep on the captured pages (`phase2_choice.html`, `theseedisplanted.html`, `salphaseion_phase3.html`): none of `causality`, `safenet`, `luna`, `11110`, `fresco`, `heisenberg`, `uncertainty`, `giveit`, `flower`, `concrete` occurs on any of them.

Two patterns hold without exception:

- **Data decodes produce messages or checks. Riddles produce passwords.** The Architect text, the checkerboard and dbbi were all decoded by computation, and none of them yielded a password. Every password came from a riddle answered with outside knowledge.
- **Where a transformation is part of a password, the clue states it exactly and the result is unique** (raw genesis data "after 4 on row 1616"; "the next situation" after the only non-mating move). There is never a free parameter for the solver to search.

## 2. Finding: the search is aimed at the wrong class of answer

The dossier's model (section 9) reads `matrixsumlist` as an arithmetic operation on the 14x14 poster and `lastwordsbeforearchichoice` as a window cut from the Architect text at some offset. Both are data-arithmetic readings, the class that has never produced a password in this puzzle.

Where the budget went (dossier 10.9, doc 115): 7.29 billion decrypt tests, of which about 4.03 billion were dbbi with `b` as a merged zero, about 1.24 billion were poster sum lists crossed with Architect windows, and about 2.0 billion were "operand families, decrypts only" (remainders, RGB values, walk numbers, substrings, card pips). Essentially all of it is arithmetic or windowing over puzzle data. By contrast the runs that treated the labels as riddles (doc 98's riddle readings, docs 103 and 104, the Fresco concepts) total under a million candidates, and even those were crossed combinatorially rather than solved.

**Retrodiction test (INFERRED, but easy to see).** Run the current pipeline against phase 2, 3 or 3.2 as if they were still locked. The pools are built from puzzle objects; none of the answers is in a puzzle object. Recall on the creator's demonstrated password class is zero. A method that could not have opened any of the four solved gates should not get the CPUs for the fifth.

## 3. Finding: wide candidate pools mean the riddle is unsolved

The creator designs for uniqueness, and the project already has the evidence:

- chess: 14 legal moves, 13 mate at once, one does not (doc 42)
- checkerboard: 45 blank pairs, exactly one reproduces the plaintext
- Architect: only cp273 turns all 1,539 bytes into letters
- format tags: six for six, the single negation on the single spaced part
- dbbi: one colour program parses 91 of 91

Phase 3 needed seven parts with no per-part check, and solvers still got it, because each riddle had one confident answer. That is the design: no partial oracle is needed when every piece is forced.

The project's open-problem inputs look nothing like that. `msl_new` 4,218 and `msl_old` 6,459 strings, `lw_loc` 6,613, 2,500 x 1,620 joint passwords (doc 114), 1,547 lists in 17 encodings crossed with three last-words pools (doc 115). A reading that needs a pool of thousands has not found the reading. Crossing two such pools does not help: if each pool has, say, a 1% chance of containing the right element, the cross has 0.01%, whatever its size.

**Practical rule:** a reading of a label is only ready to test when it names one candidate, or a handful that differ only in case or spacing, and the justification can be written down in a sentence before any decrypt runs.

## 4. Finding: the acceptance bar filters out the likely answer

Doc 115 section 7 requires a derivation to name an object, a length, a rule, and "a count that a shuffled object does not reach". That standard is right for data operations (it is exactly how dbbi was validated) and it protects against apophenia. But apply it to the solved passwords: `causality` has no shuffle-null statistic, nor does `Safenet`, `Luna` or `jacquefresco`. The bar can only ever pass a data-arithmetic derivation, so it quietly steers all work toward the class in section 2.

For a riddle answer the decrypt itself is the test. It is exact, free and silent, and a single candidate costs microseconds. Semantic candidates do not need a fit statistic; they need a reason.

## 5. Finding: hints are double-spent and over-read

**The Roses poem (#1710, January 2020) belongs to a solved stage.** Line by line (INFERRED, but each line has a match):

| poem | the stage it was posted for |
|---|---|
| "Go back to the first puzzle piece" | the poster |
| "It might have shown you only one door" | the poster's URL, `theseedisplanted` |
| "the rabbits nest may contain a whole lot more" | the second door, the side page reached by hashing the poster's text (dossier 4.5; #7418 "Good point") |
| "Yellow has a number and so does Blue" | the dbbi walk rule: blue consumes 1, yellow consumes 2 (dossier 6.3) |
| "Roses are White but often Red" | the one white cell that must be painted to count as coloured, `#FEFEFE` (dossier 4.3) |

In January to May 2020 ("This one", "answer is there", #4096 and #4102) solvers were stuck reaching and reading the side page. That stage is now solved. The dossier instead takes the *Alice* Ch. VIII reading, imports the gardeners' primes {2, 5, 7}, and assigns them to `matrixsumlist`: 1,558 lists and 104,885 candidates (doc 111), the 1.24-billion cross (doc 115), and 112 million decrypts of card pips (doc 115) all rest on that import. The *Alice* reading may well be a second layer (the creator does say things twice), but nothing in the poem points it at the next operation.

**Chat hints are a weak, noisy channel, and they set the agenda anyway.** The creator labels his own lines "not a hint btw, just fooling around" (#3391), ran an April Fools hint (#7529), said "No hints after stage 2" (#898) and "No hints, only free will" (#60289) and broke both, and said in November 2024 "I could come up with some empty cryptic bs hint" (#32579). Sweeps seeded from chat lines (the *Cosmic Duality* book 1.89M, *Looking Forward* 1.31M plus 9,800, the dots, the card pips, Neo's passport, "Infrared", purple pill, ASCII 127) are all null. The in-artifact text, which produced every solved step, gets read less carefully than the chat: the song that built two gates was missing from the dossier for about 75 docs (methodology item 15).

**Rule worth adopting:** tag every hint with the stage solvers were stuck on when it was posted, and mark it consumed when that stage is solved.

## 6. Finding: the search scale contradicts the creator's own account

- "Couple hours, and no" (#70336, 1 September 2026), asked how long the puzzle took to make and whether he worked alone.
- "If you guys got 1 microstep further, the puzzle will likely be solved the same day" (#32579, November 2024). At that date dbbi had not been parsed (Ugur Keser, #72215, September 2026), so the microstep was reachable from the material solvers already had: the decoded labels.
- "Fyi. Another person (or team) made it to salph" and "Nr 5 in salph" (#6491, #6712, March 2021). Five teams have stood at this exact wall for five and a half years.
- "you have to understand how to interpret all the hints" (#8491); "Once you hit a 'ying yang', you'll be able to solve it the same day" (#9599).

A puzzle built in a couple of hours, whose next step was a microstep from the decoded labels, does not hide its key behind one of 1,547 sum lists in 17 encodings. When many independent teams fail for years with very different search methods, the shared assumption is the likely fault, not the coverage.

## 7. Finding: compute goes where enumeration is possible

- Doc 115's largest run (4.03 billion, 55% of the session) was dbbi with `b` as a merged zero, after dossier 6.3 had concluded dbbi is "a verification object ... and carries no payload beyond that". It ran because 2^25 is enumerable.
- About 2.0 billion more were "operand families, decrypts only", with no fit test, after the dossier's own methodology item 14 ("A new word source is not a lead").
- The current proposal list (`gsmg/status.md`, thread 1) and the off-repo gap list (log section 8) both lead with closing coverage gaps: double-hash forms in the crosses, the second password order, the 38.6M odd-size XOR universe, the 170,295-form residue. Closing a gap matters only in proportion to the prior of the family it belongs to. Probability of a win is roughly P(the family is right) x P(the pool holds the answer) x P(the form is right), and gap-closing improves only the last factor while the first two are tiny.

## 8. Finding: the "two operations feed one password" model is a framing choice, not a result

The joint model comes from textarea adjacency (`lastwordsbeforearchichoice` then `thispassword`) and from #8446 listing the labels in a row. It is what justified the largest crosses (8.1M joint passwords in doc 114, the 1.24B cross in doc 115). Other readings fit the same evidence at least as well (INFERRED):

- **Labels as stage names.** #8446 lists four labels in order; one is solved (`yellowblueprimes`, the dbbi check), and three labels remain against three locked containers, with `yinyang` already tied to Cosmic Duality (#39237, #8310). Under this reading each label is its own riddle for its own lock, as the riddles of phases 2 to 3.2 were.
- **Labels as the riddle sheet.** Every opened container had its riddles beside it. The SalPhaseIon textarea's only live content is labels and two `sha256` instructions (dossier 9). Read in the creator's grammar, the labels are the riddles and `thispassword` / "sha256 the answer too" are the assembly instructions, like "parts 1..7 --> sha-256" on the phase-2 page.

Individual pool items were tested alone against all containers, so these models were not ignored. But they were only fed the same data-arithmetic pools, so the model question itself is still open.

**A consistency check the project fails.** It reads "archi" through the film (the Architect's speech) but "matrix" through the poster grid. Everywhere else in the creator's material "matrix" means the film: the Beaufort key `THEMATRIXHASYOU`, the Architect, the Merovingian, the keymaker, the white rabbit, "in a matrix cypher kinda way" (#66938). The one "sum" sentence in the chain texts is the Architect text's opening line. In the film it ends "inherent to the programming of the matrix"; the creator swapped "the matrix" for "this puzzle". I am not claiming that is the answer; doc 102 tested the phase-2 template sums it suggested. It is an example of the kind of reading (one referent, one sentence, few candidates) that section 3's rule asks for, and that the poster-grid reading cannot produce.

## 9. Finding: errors specific to the wider community and to the off-repo work

From the failed-attempts log (sections 2, 6 and 8) and its index:

- **Pad-1 "solves".** The community Cosmic Duality "solve" (C1), `enter484` (S8), the 79-byte MD5 output and its WIF (S9), the "gnosis" and WhoAmI claims: all pad-1 events, which a wrong key gives about 1 time in 250. None came with authenticated plaintext.
- **Validators that void their own negatives.** ASCII gates, unpad-before-check, MD5-default harnesses, a Terminal loader truncated to 48 bytes, a Base58Check bug, CRLF-stripped plaintexts, a mis-transcribed phase-3 salt. A large share of pre-September negatives are weaker than their counts suggest.
- **Data errors from retyping and misreading.** `CRYPTOLOGIC` (the tile reads `crypto/gic`) underlies a 13,264-candidate run; the rabbit was analysed facing the wrong way; `matrix.json` carried a wrong cell for twelve days.
- **Fragmented records.** Separate workspaces (`D:\5btc`, astra-puz, GSMG-CLEAN, 8.7-fresh-start and others) reached contradictory verdicts: Cosmic Duality "opened" in one register and locked in the rest; `YOUWON` "authenticated" in one and "Pfff. Coincidence." (#70307) in the repo. Several runs have no saved output (about 13.6M and 69.7M candidates), so their coverage is unverified.
- **LLM-generated leads, ours included.** The log records superseded GPT consults and retracted Gemini additions. The repo's own 115 docs, many written by Claude sessions, follow the same loop: propose a reading, build a pool, sweep, publish a null, propose the next reading. That loop is good at closing doors and bad at finding the one the creator meant, because it rewards whatever can be generated and tested at scale.

## 10. What to do differently

1. **Run a retrodiction check before any new method.** Would it have opened phase 2, 3 or 3.2 from the page text alone? If not, it does not get CPU time.
2. **Solve each label as a riddle, to one answer.** Write the reading, its referent and its single candidate (with case and spacing variants) in a sentence before decrypting. Readings that leave more than a handful of candidates are unfinished, not ready to sweep.
3. **Test semantic candidates directly, a few at a time.** The decrypt and the win test are exact and free; no shuffle null is needed for an answer that has a reason.
4. **Stop gap-closing on low-prior families** until a family earns a prior from a reading. This includes the sweep currently running if it is coverage work.
5. **Re-audit hint assignments by date.** For each creator hint, record what solvers were stuck on when it was posted. Retire hints whose stage is solved, starting with the Roses poem.
6. **Keep what works:** planted controls, the structure-agnostic recogniser, lock chaining, generated data blocks, and the standing rules.

## Caveats

- The readings in sections 5 and 8 are INFERRED and untested as framings; the point is the method, not those specific readings.
- Budget shares are taken from dossier 10.9 and doc 115 as reported, not recomputed.
- I checked whether the "edited" stamps on 244 of the creator's 492 messages could mean hints were rewritten later. Every message with reactions carries an edit stamp, and many stamped messages are a lone emoji, so the stamps are mostly reaction artifacts. That is not a finding.
