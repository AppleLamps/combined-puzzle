# 67. Document index and errata

## Current reading layer: 6 October 2026

Start with [status](status.md), [doc 119](119-current-evidence-ledger.md),
[doc 118](118-correctness-audit-remediation.md), then the dossier. The historical
tables below include files absent from this checkout. They do not establish
that the complete original candidate pools or receipts are available.

Doc 119 supersedes these earlier errata wherever they assert:
- global L84 rejection or uniqueness without a fixed correspondence;
- FAED/residue filler certainty, a shared generator, or no other payload;
- a necessary short-first route or Cosmic message-only content;
- that 140 explains the Architect's number or uniquely identifies v0.3.10;
- that all operations/assemblies were exhausted or all old detector nulls stand;
- a mandatory split, outside-page operands, or a category-bound 23/16/7 corpus.

### Documentation inventory for this reconciliation

All 28 pre-existing Markdown documents/START-HERE files were inspected at base
`1a71de4a62a42b0e0f27d26a1d562d67dca6e55b`; doc 119 is newly added.

| role | files |
|---|---|
| current entry points | root README, START-HERE, CLAUDE; `status`; doc 119 |
| detailed evidence/reference | dossier; ARTIFACTS; 04-key-material; 07-onchain-facts; doc 21 |
| tooling and validation | tools/README-tools; doc 118 |
| historical index and crosswalk | doc 67; FAILED-ATTEMPTS-INDEX; FAILED-ATTEMPTS-LOG |
| dated experiments/reviews | docs 114–117; critical-review; the nine workstream READMEs |

Primary artifacts, code, candidate files and raw run output are unchanged.
Historical run titles and original conclusions are retained with explicit
supersession notices; they do not authorize resuming old work.

## Historical catalog and errata


Historical catalog as of 29 September 2026, with later additions noted. This file is the map of the project: what to read, what each surviving log doc is worth, which sentences inside them are stale, and where the content of every retired doc went.

Docs in the analysis log were written one session at a time, and later sessions overturned parts of earlier ones. Rewriting a finished negative result risks introducing new error, so the logs are kept as written and their stale sentences are listed in section 5.

## 1. Reading order

1. Read docs 119 and 118, then `claude/GSMG-PUZZLE-DOSSIER.md` for detailed evidence.
2. `README.md`: the state in brief and the file table.
3. This file, for the status of any log doc before relying on it.
4. `04-key-material.md`, `07-onchain-facts.md` and `claude/21` for addresses and the on-chain oracle. `claude/113` is the audit behind them.
5. Doc 118 for current detector/source limits; references to doc 110 describe the historical recognizer, not a newly verified runtime.

## 2. Top-level files

The following records describe the 29 September edition, not live balances or current validation. Rewritten then: `README.md`, `04-key-material.md`, `07-onchain-facts.md`, `ARTIFACTS.md`, `keys.json`, `message-sequence.json` (regenerated from the chain), `matrix.json` (cell (7, 6) corrected to white) and `claude/21`. The data files were checked against the artifacts they derive from (dossier section 13). `README.md` lists each file. The scripts behind docs 107 to 115 are under `tools/` (entry point `tools/README-tools.md`); doc 115 section 8 lists which script does what.

Added 3 to 5 October 2026: `claude/status.md` (one-page status), `claude/116` (doc 115 coverage gaps, logs in `claude/doc116-runs/`), `claude/117` (riddle rounds R1 to R35 and the pair ledger, with one folder per workstream listed in its section 12), and `claude/critical-review-2026-10-03.md`. Doc 117 section 11 qualifies every per-label "spent" verdict in the log docs and the dossier: a joint-password null kills only the pair tested.

`claude/FAILED-ATTEMPTS-LOG.md` (added 3 October 2026) is a do-not-repeat register for the three locked containers, compiled from runs kept outside this repo. `claude/FAILED-ATTEMPTS-INDEX.md` says which of its rows are new, which the dossier already carries, and where the two disagree.

## 3. Retired docs and where their content went

The docs below were folded into the dossier and deleted. A pointer to one of them from a kept doc ("see claude/56", "claude/20 Part 7") resolves through this table. Per-run details that no later doc used (individual candidate lists, harness code) were dropped with them.

| retired | subject | now in dossier section |
|---|---|---|
| `01-overview.md` | what the puzzle is, its stages, the prize, where it stands | 1, 9, 12 |
| `02-verified-chain.md` | the solved stages: decrypt commands and derived outputs | 2, 3 |
| `03-unsolved-material.md` | the unsolved ciphertexts and their structure | 6 |
| `05-hints.md` | creator hint excerpts and decoded artifacts | 7, 8 |
| `06-first-image.md` | the poster: matrix, spiral, colours | 4 |
| `claude/10` | the creator's mindset and a four-slot concatenation plan | 9, 10.1 |
| `claude/11` | that plan run (2.7M and 5.5M phrases, 0 hits) | 10.1 |
| `claude/19` | `#FEFEFE` as a bit-level prime pointer (748 transforms) | 4.3, 10.4 |
| `claude/20` | the chain and the hint catalogue | 3, 8 |
| `claude/27` | the container phrase oracle, first powered negative | 10.1 |
| `claude/28` | imported prior-work findings | 8.1, 9 |
| `claude/31` | the 83-cell dbbi parse reproduced | 6.3 |
| `claude/32` | audit of a keyed-faed script | 6.4, 10.2 |
| `claude/34` | the answer distributed across null decodes | 10.5 |
| `claude/36` | how the creator builds a stage | 9 |
| `claude/37` | frames for "last words" and "our first hint" | 10.1 |
| `claude/44` | `matrixsumlist` as a key operation, with the row-plus-column-sum theorem | 9, 10.5 |
| `claude/46` | the 18 September state of play | 11 |
| `claude/47` | acceptance test for raw binary keys (215,550 configurations) | 2, 10.1 |
| `claude/49` | the film's pre-door lines as "last words" | 10.1, 10.5 |
| `claude/51` | the last page read as a poster | 4.6, 9 |
| `claude/52` | 481 hand-visited door paths | 10.5 |
| `claude/54` | the live site as evidence | 1, 11 |
| `claude/56` | the complete walkthrough | 3 |
| `claude/57` | the phase-2 header and tags | 3.2, 3.3 |
| `claude/61` | the SafeNet and Luna vocabulary sweep | 10.1 |
| `claude/62` | the verifier submission plan | 1 |
| `claude/74` | the creator dump mined; the prime rider | 8 |
| `claude/79` | segmentation confirmed; faed spent | 6.1, 6.4 |
| `claude/80` | the dbbi parse verified; the residue | 6.3 |
| `claude/83` | the poster program is dbbi-specific | 4.2, 6.3 |
| `claude/84` | doc 79b executed; passphrase screen | 10.3 |
| `claude/85` | poster closed; yinyang is not in it | 10.4, 12 |
| `claude/88` | homophonic substitution closed; faed is filler | 6.4, 10.2 |
| `claude/89` | the rebus colour channel read | 5, 10.4 |
| `claude/92` | the seed of the opposite tested | 10.6 |
| `claude/93` | reassessment, endorsement audit and plan | 8.1, 12 |
| `claude/94` | dossier rebuild; `matrixsumlist` and last words worked | 10.6 |
| `claude/GSMG-DOSSIER-ADDENDUM-2026-09-23.md` | the 23 September addendum (docs 94 to 110) | 10.6, 10.7 |
| `cosmic-duality.txt` | duplicate of `cosmic-duality.b64` (the same base64 without the trailing newline) | 6.5 |

Two files carry the number 81: `claude/81-chat-mined-and-a-mechanism-that-acts-on-faed.md` (listed below as 81a) and `claude/81-parse-reproduced-cold-and-four-branches-closed.md` (81b). Both were written in the same session and both are kept.

## 4. The surviving analysis log

Status legend:

- **CANONICAL**: current as written.
- **CANONICAL WITH ERRATA**: the result stands and section 5 lists stale sentences.
- **NEGATIVE RESULT**: a swept null kept so the space is not covered twice. The control and the count are in the doc.
- **NEGATIVE RESULT WITH ERRATA**: the same, with stale sentences listed in section 5.
- **HISTORICAL**: a working log whose conclusions were overtaken. Read for history only.
- **SUPERSEDED**, **RETRACTION**: as stated in the row.

"Carried in" names the dossier sections that hold the doc's result.

| doc | headline | status | carried in |
|---|---|---|---|
| `09` | Exhaustive sweeps of digit keys, zero rules, grid sum lists and Architect-number readings against three containers and 11 addresses. All null. | NEGATIVE RESULT WITH ERRATA | 10.1, 10.2, 10.3, 10.5, 3.4a, 6.3, 6.4 |
| `12` | Dictionary segmentation of the 1,539-letter Architect text into 333 words, a reading aid with notes on segmenter artefacts. | CANONICAL WITH ERRATA | 3.4a |
| `13` | Read 492 creator messages: found the unforeseen matrixsumlist hint (#5966), dismissed the April Fools and on-chain hints, and located the Cosmic Duality container. | CANONICAL WITH ERRATA | 8.1, 8.2, 8.3, 8.5, 7.4 |
| `14` | Audited the poster at six levels (file, QR, grid, traversal, colour, encoding); it yields only gsmg.io/theseedisplanted, so no second door comes from the image alone. | NEGATIVE RESULT WITH ERRATA | 4.1, 4.3, 4.5, 4.6, 10.4 |
| `15` | Transcribed the eight rebus tiles and audited all nine images at file level; follow_the_white_rabbit.png is a pixel-identical 3x reduction of the poster grid. | CANONICAL WITH ERRATA | 5, 4.1, 4.5 |
| `16` | Chi-squared and exhaustive search show dbbi and faed are not rule-2 numbers under any letter mapping; faed's excess symbol g sits at +5.8 sigma. | NEGATIVE RESULT WITH ERRATA | 6.4, 10.2 |
| `17` | Door searches on the rebuilt live site (about 8,500 probes) found nothing beyond known pages; confirmed all nine project images byte-identical to the server's. | NEGATIVE RESULT WITH ERRATA | 1, 4.5, 10.5 |
| `18` | Session index and reusable tool code (address oracle, rule-2 search, checkerboard, Architect decode, poster grid) from the 14 to 20 round; index role superseded. | SUPERSEDED by the dossier (win test in section 1, recogniser in 2, decodes in 3.4a and 3.4b) and this index; the tool code is kept | 1, 2, 3.4a, 3.4b, 11 |
| `21` | Rewritten 29 September: the checkpoint filter, its controls, the six checkpoints, the signed set through 2021-07-18, and a tested paging checker. | CANONICAL | 1 |
| `22` | Recovered the Phase 1 mechanism from the Telegram export: the rebus spells Logic's song The Warning, and the creator's posted hash verifies the answer. | CANONICAL WITH ERRATA | 3.A, 3.1, 5 |
| `23` | Mined solver-side chat: /(aa) and /(aBa) tags are normalisation instructions; double-hash reading of Hush hush is null; a Cosmic Duality checkpoint hash is unreproducible. | CANONICAL WITH ERRATA | 3.3, 8.1, 10.5 |
| `24` | Mined 492 creator messages and export media: closed #8310, catalogued new hints, ran null sweeps (KEYNOTE, zero reinsertion, seeded checkerboards), analysed the FEN. | CANONICAL WITH ERRATA | 7.4, 8.2, 8.4, 10.2, 11 |
| `25` | Audited six score-based claims against shuffled nulls: entropy evidence for ciphertext fails, octal printability is noise, no elimination overturned. | CANONICAL WITH ERRATA | 11 |
| `26` | Matched the poster to a 2020 Wayback capture and SalPhaseIon blocks to a 2023 capture; showed the two 96-byte containers are independent encryptions. | CANONICAL WITH ERRATA | 3.0, 6.5 |
| `29` | Swept 4,153 vocabulary candidates over EVP and PBKDF2, CBC and ECB, five password forms, against both 80-byte containers: 0 hits, controls fired. | NEGATIVE RESULT WITH ERRATA | 2, 6.5, 10.1 |
| `33` | Rebuilt the keyed-faed harness with a power control; zero-free arithmetic rules out keyed rule-2 decoding; 1,336 running keys under mod-9 operations were null. | NEGATIVE RESULT | 10.2, 11 |
| `35` | Audit: #8446 reread as a stage list, film text separated from creator edits, new nulls (issue 69 claim, 7.14M cipher variants), next steps listed. | CANONICAL WITH ERRATA | 3.4a, 6.3, 7.1, 10.1, 11 |
| `39` | Read 2020 chat: the extra door was the SalPhaseIon page reached by hashing poster text; "First or zero" teased which piece is first. | CANONICAL WITH ERRATA | 4.5, 7.2, 8.1, 11 |
| `40` | Read the December 2021 Another DOOR sequence: #8000's prime and zeroing hint follows solver posts on dbbi primes; a zeroed-marker decode was null. | HISTORICAL | 8.2 |
| `42` | Remeasured the artifacts: 13 of 14 White moves mate and Rg6-c6 alone does not, checkerboard input is 149 digits, tail bits are 0000. | CANONICAL WITH ERRATA | 3.0, 3.3, 3.4b, 4.4, 5, 6.5 |
| `43` | Placed unconsumed pieces: rabbit gaze points to the off-white cell, marker 21 of dbbi's program; field split, container roles and order inferred. | CANONICAL WITH ERRATA | 4.3, 4.4, 6.3, 6.5, 9 |
| `45` | Aligns the 1,539-letter Architect text against the film monologue: 22 edits, 46% creator-authored. Shows 23/16/7 and 'reinserting the prime' come from the film. | CANONICAL WITH ERRATA | 3.4a |
| `48` | Reviews an external lab's atlas: FAED tests as filler, the codec-pool sweep is null, and an L=84 parse with 23/16/7 is proposed (later rejected). | HISTORICAL | 6.3, 6.4, 8.3, 8.4, 10.1 |
| `50` | Builds a 384-string generator of the creator's world and runs it, plus 13,692 interleaved operand permutations, against the three containers: 475,808 decrypts, all null. | NEGATIVE RESULT WITH ERRATA | 10.1, 12 |
| `53` | Sweeps robots.txt, page source, headers, favicon and poster pixels: five-colour grid proves the off-white cell deliberate; the rabbit robots.txt post-dates March 2022. | NEGATIVE RESULT WITH ERRATA | 1, 4.1, 4.3 |
| `55` | Verifies recovered 2020-2023 archives: puzzle.png is the original with the off-white cell, the SalPhaseIon textarea is byte-identical, and phase 2 was unedited to 2022. | CANONICAL WITH ERRATA | 1, 3.0, 4.1, 6, 13 |
| `58` | Tests three readings of the 'Infrared' hint (invisible pixels, inversion, under the red line) and the word as a passphrase: all null, hint unexplained. | NEGATIVE RESULT WITH ERRATA | 10.5, 4.1, 4.5 |
| `59` | Builds a prize-key acceptance test, bounds 80-byte container plaintexts to 64-79 bytes, shows Terminal ends the 3.2 file; 96,138 real decrypts null. | CANONICAL WITH ERRATA | 2, 3.4b, 6.5, 10.1 |
| `60` | Reads phase 2 for meaning: Luna HSM key-ceremony and split-volume readings, plus a null test of the tag alphabet under two SalPhaseIon codecs. | HISTORICAL | 3.2, 3.3, 5, 10.1 |
| `63` | Executes the verifier run: the /phase1verification form is live, accepts only the phase-1 answer, and rejects causality, the 227-character and 62-byte answers. Ten submissions. | CANONICAL WITH ERRATA | 1, 3.2 |
| `64` | Checks 23 message citations from an outside analysis against the export (all verbatim), corrects three of its claims, and closes the #9505 192-byte discrepancy. | CANONICAL WITH ERRATA | 8.3, 8.4, 8.5, 6.1, 6.5 |
| `65` | Checks the KDF and eight ciphers against Cosmic Duality: SHA-256 KDF confirmed, 7.16M decrypts null bar one noise hit, keyless faed encodings null. | NEGATIVE RESULT WITH ERRATA | 2, 10.1, 11, 6.5 |
| `66` | Sweeps 551.7M concatenations of 29 decrypted objects against Cosmic Duality: 123 block-1 survivors versus 117 expected from noise, zero confirmations. | NEGATIVE RESULT WITH ERRATA | 10.1, 12, 11 |
| `68` | Mines the 403-URL Wayback CDX record: the original site answered 200 to every path, voiding door-probe nulls; sitemap lead closed; 845,040 archived-name decrypts null. | CANONICAL WITH ERRATA | 1, 10.5, 11 |
| `69` | Authenticates the phase-2/3 page against a 12 Nov 2020 capture, confirms the tag inventory, limits the numerals to five parts, finds underscore emphasis. | CANONICAL WITH ERRATA | 3, 3.2, 3.3 |
| `70` | Answers an eight-point critique: greenback, DEL and faed-selection nulls, OpenSSL -md fix, and a poster-based case for L=84 that doc 71 reversed. | NEGATIVE RESULT WITH ERRATA | 2, 3.3, 10.5, 6.3 |
| `71` | Corrects doc 70: the 83-cell parse matches the poster 23 of 23 with the off-white cell. Screens 2^30 subsets on all containers: null. | CANONICAL WITH ERRATA | 6.3, 4.3, 3.3, 3.2, 10.1, 10.5 |
| `72` | Records two parallel null sweeps against the three shut containers (7.7M passphrases; ten dbbi/faed transform families) and proposes the live hash-path site as a verifier. | NEGATIVE RESULT WITH ERRATA | 10.3, 10.2, 4.2 |
| `73` | Runs the live hash-path oracle in a browser: 391 probes hit only the known SalPhaseIon page. Rule 2 re-verifies the two soup segments. | NEGATIVE RESULT WITH ERRATA | 6.1 and 6.2, 4.5, 10.5, 1 |
| `75` | Exhaustive search for zero reinsertion into dbbi and faed under rule 2, calibrated on planted controls: no survivors to k=18 (18.8 billion nodes). | NEGATIVE RESULT | 10.2, 6.4 |
| `76` | Works the two riders: primes-as-zero-positions contradicted by the creator's own checkerboard, yellowblueprimes decomposed, anomaly-cell rotation tested, board-1 rule recovered, clause-2 boards null. | NEGATIVE RESULT WITH ERRATA | 3.4b, 4.2, 4.3, 10.2, 10.5 |
| `77` | Two solvers validated on the checkerboard control find no English in dbbi or faed under any escape set; 10.2M direct key checks are null. | NEGATIVE RESULT WITH ERRATA | 6.4, 10.2, 10.3 |
| `78` | Joint dbbi and faed combination sweep null; chi-square rules out additive shares. Withdraws doc 77's key sweep; casts faed as the payload, later overturned. | NEGATIVE RESULT WITH ERRATA | 1, 6.4, 10.2 |
| `81a` | Mined chat claims: A1 faed prime-row read (retracted by doc 82), A3 dbbi rail derivation bit-identical, A2 YOUWON suggestive, two solver claims unreproduced. | HISTORICAL. Holds material the dossier does not carry: the A3 dbbi rail derivation and the Worldmaker and Doober checks | 10.5, 11 |
| `81b` | Cold reproduction of the dbbi parse (23 hosts, 91 of 91, same residue). Four reuse tests on faed and the residue are null. | NEGATIVE RESULT WITH ERRATA | 6.3, 10.4, 10.6 |
| `82` | Retracts doc 81's 'key eyes' read of faed: the null pinned the answer, the output alphabet is forced, and real faed underperforms shuffles (P=0.93). | RETRACTION | 11, 6.4, 10.4 |
| `86` | faed is one homogeneous object; doc 03's drift result comes entirely from the last 32 characters (tail P=0.0201); the 538-character head shows none. | CANONICAL WITH ERRATA | 6.4, 11 |
| `87` | Running-key, checkerboard, columnar and digram tests close the fixed-key class for faed; faed measures as significantly non-uniform, memoryless machine filler (p=1.3e-8). | NEGATIVE RESULT WITH ERRATA | 6.4, 10.2 |
| `90` | Review of dossier regressions (since restored), the dot-elision convention, an exhaustive zero-substitution search (zero solutions) and 22,394 new candidates, all null. | NEGATIVE RESULT WITH ERRATA | 6.4, 7.3, 10.6, 3.2, 3.3, 8.4 |
| `91` | Verifies the #8310 image as the Cosmic Duality cover, recovers the #8311 to #8330 thread, screens 1.89M book phrases and closes phase3.1_old.aes; all null. | NEGATIVE RESULT WITH ERRATA | 7.4, 10.6, 3.4 |
| `95` | Five structural derivations (label concatenations, residue as key, matrix sum on the Architect text, matrixsumlist as selector, #8446 chain hash) tested; all null. | NEGATIVE RESULT | 10.6, 12 |
| `96` | Ran about 285,000 sha-before-combine, newline-join, XOR, ordering and filler-sum screens, all null; reviewed possible gaps, including whether the Architect text argues for the L=84 parse. | NEGATIVE RESULT WITH ERRATA | 10.7, 10.2, 3.4a, 6.5 |
| `97` | Used L=83 and L=84 host prime and offset sets as indices into nine texts, and screened poster-text hashes as 'our first hint'. Both null. | NEGATIVE RESULT | 10.7, 3.4a, 6.3 |
| `98` | Recovered the song 'The Warning' as the puzzle's backbone (restored as dossier 3.A) and ran about 880,000 riddle, double-hash and song screens, all null. | CANONICAL WITH ERRATA | 3.A, 9, 10.7, 11 |
| `99` | Tested every word span, line and clause of 'The Warning' as password text, raw, double-hashed and crossed with labels: about 79,000 candidates, all null. | NEGATIVE RESULT WITH ERRATA | 3.A, 10.7, 12 |
| `100` | Song phase three consumed two surplus items: the black war tile and the #FEFEFE cell forced to blue, which fixes L=83; text screens null. | CANONICAL WITH ERRATA | 3.A, 4.3, 5, 6.3, 10.7 |
| `101` | Showed the 60-symbol dbbi residue matches faed's letter distribution (G-test p = 0.26), so dbbi is the poster program plus filler; checkerboard reuse null. | CANONICAL WITH ERRATA | 6.3, 6.4, 9, 10.7 |
| `102` | Tried chessboard piece-value sums and phase-2 template sums (with H as -42, 42, 24, -24) as the matrixsumlist operand: 4,780 candidates, all null. | NEGATIVE RESULT WITH ERRATA | 3.2, 9, 10.7 |
| `103` | Re-read all 492 creator messages against their parents: #881 marks the Roses poem as the planned final hint; 7,368 screens of readings, all null. | CANONICAL WITH ERRATA | 8.6, 7.2, 6.5, 10.7 |
| `104` | Identified the Roses poem as Alice in Wonderland Chapter VIII, naming the primes {2, 5, 7} through the gardeners; gardener and vocabulary screens null. | CANONICAL | 7.2, 8.2, 10.4, 10.7 |
| `105` | The #FEFEFE cell has 14 equivalent positions; only 163 is prime by both counts (post hoc, about 1 in 5). Nest pixels carry no data. | CANONICAL | 4.3, 4.4, 7.2, 10.4 |
| `106` | Screened 857 zeroed poster-text variants (3,428 screens) as second-door candidates; two archived gsmg.io pages are the web app shell. No door found. | NEGATIVE RESULT WITH ERRATA | 1, 7.2, 10.7, 14 |
| `107` | Tested three untried methods: whole decrypted stages as passwords, poster sums as a raw scalar, XOR/interleave of the two short containers. All null. | NEGATIVE RESULT | 10.7, 6.5, 9, 14 |
| `108` | Audited the August 2026 farewell page and hidden terminal grid; 12,645 decrypts of its strings against three locks gave 54 valid pads, none readable. | NEGATIVE RESULT | 1, 4.3, 10.7, 11, 14 |
| `109` | Tested the merged-zero digit reading of the filler (residue, faed, dbbi) as binary payloads against the locks: about 16.8 million decryptions, all null. | NEGATIVE RESULT WITH ERRATA | 6.4, 10.2, 10.7, 14 |
| `110` | Defines a structure-agnostic recogniser (bias, headers, EBCDIC, UTF-16) and lock-to-lock chaining, then reruns earlier candidates: about 28 million decrypts, one random pad-3 flag. | CANONICAL | 2, 10.7, 11, 14 |
| `111` | Worked five leads: 1,558 poster sum lists tested for exact fit against shuffled posters, located last words, halves, dots, Fresco. 466,441 candidates, all null. | NEGATIVE RESULT WITH ERRATA | 10.8, 7.3, 8.1, 12, 14 |
| `112` | Checked the dot hints against 492 creator messages: no 1-to-5 word-length run; four-dot replies read as ordinary ellipses; 'tiny hint' in #53342 cites #881. | CANONICAL | 7.3, 11, 12, 14 |
| `113` | Classified the oracle's 30 transactions (14 signed, 16 inbound). Neo addresses are poster checkpoints, 1NULY is a kangaroo-tool tip address, creator authorship unproven. | CANONICAL | 1, 10.8, 11, 14 |
| `114` | Tested the joint #8446 password (8.1 million operand pairs), halves, and the 23/16/7 selection space (22,221 candidates). All null. | NEGATIVE RESULT WITH ERRATA | 10.8, 12, 9, 14 |
| `115` | Worked the 29 September queue: dbbi with `b` as the zero (all 2^25 subsets), letter and mod-10 sum-list forms crossed with the last-words pools, and eight operand families with shuffle-null fit tests. 7.29 billion decrypts, all null; no derivation names the operand. | NEGATIVE RESULT | 6.4, 7.3, 10.9, 12, 14 |

Docs 94 to 115 are also listed with their outcomes in dossier section 14.

## 5. Errata: stale sentences that survive in kept docs

### Errors that recur across docs

- **Pointers to retired docs.** Resolve them through section 3. Doc 71 section 6 was the correction of record for retired docs 56, 57 and 31 and for doc 70 section 2; the dossier carries the decided versions.
- **Container sizes.** "80-byte" containers means the ciphertext without the 16-byte header. The files are 96 bytes (Terminal, SalPhaseIon short), and Cosmic Duality is 1,328 bytes of ciphertext in a 1,344-byte file (`ARTIFACTS.md`).
- **Checkpoint dates.** The six `GSMG.io:` checkpoints were paid on 2020-03-24 (blocks 622762 to 622774). Statements that place them in April 2020, or that say the oracle's trail ends there, are stale: the oracle signed messages until block 691563 (2021-07-18) and everything later is inbound (`07-onchain-facts.md`).
- **"Cosmic Duality is the anchor."** Retracted. The threaded reply #39237 puts yinyang after an AES decode, so if yinyang is Cosmic Duality's plaintext, SalPhaseIon short is the gate. Screen all three containers on every candidate (dossier 6.5 and 11). The caveat that older indexes attached to doc 59, that its nulls say nothing about the known vocabulary, is withdrawn on the same grounds.
- **dbbi, its residue and faed as open questions.** Any sentence that calls them unread, live, key material or payload is superseded: dbbi is the poster's colour program written as prime-position hosts plus filler, and faed is filler (dossier 6.3 and 6.4).
- **"The personal census is the remaining generative line."** Closed. The census was built (384 strings, 475,808 decrypts) and is null (dossier 10.1 and 12).

### Errata by doc

Each quoted sentence is stale, and the correction follows it.

| doc | stale sentence | correction |
|---|---|---|
| `09` | "`POST /phase1verification` now returns 404." (5. Live domain facts (fetched 2026-09-17)) | The verifier is live. It needs the CSRF token from the page's meta tag; a bare POST gets 413. It validates only the phase-1 answer and rejects causality, the 227-character answer and the 62-byte answer. Do not submit more. |
| `09` | "they describe the internal segmentation of the creator-validated 227-character Phase 3 answer" (11.4 Standing conclusion (same claim in 11.2, 12.4 and 14.3)) | Twenty-three, sixteen and seven are the film's own numbers, sitting in an unchanged run of Architect dialogue. Only 140 is a fact about the Phase 3 answer (part 6 is 140 characters). |
| `09` | "What remains unexplained is unchanged since section 3: `faed` and `dbbi` resist every decoding with an oracle" (13.5 Position after section 13) | dbbi is decoded: the L=83 prime-host parse consumes 91 of 91 and gives the poster colour program plus filler. faed is filler from a biased generator, so no decoding remains to find. |
| `09` | "That archive is the only body of creator-authored words known to exist and not available here." (13.6 The one piece of creator-authored material not in hand) | The creator message export (jrk_messages.txt, 492 messages) and the full Telegram export are in the project and have been mined (docs 13, 22, 23, 103; dossier section 8). |
| `09` | "it confirms the seven-part object as a unit the creator himself counts" (10.1 The 227 constraint validates, exactly) | The checkpoint message comes from the 3GSMG24 oracle, which reads as an early solver's ledger; creator authorship is unproven and he denied on-chain messages (#12653). 227 remains the verified length of the answer. |
| `12` | "The Phase 3.2.1 decryption yields 1,539 unbroken uppercase letters." (Opening paragraph) | The cp273 plus reciprocal Beaufort decode emits 1,539 lowercase letters. The canonical form is unbroken lowercase; uppercase is display only. |
| `13` | "the password for a 1,344-byte AES container with salt `2d3f6fe06dc950e6`" (7. The Cosmic Duality question: 'The live problem is therefore exactly one thing') | There are three locked containers: Terminal and SalPhaseIon short (96 bytes each) and Cosmic Duality (1344 bytes). Per #39237, yinyang is Cosmic Duality's plaintext reached after an AES decode, which makes SalPhaseIon short the gate. |
| `13` | "belongs to a separate, parallel route out of the first image" (8. Chronology correction: 'another door' is not the SalPhaseIon page) | The primes and the #FEFEFE cell are consumed by the dbbi parse on the SalPhaseIon textarea (4.3, 6.3), and the poster has no spare capacity (4.6). The 2020 second door is the 89727c... side page (4.5). |
| `13` | ""First or zero" is the indexing convention, and it resolves to **first**." (1. Why this matters, checked against the image) | "First or zero" (#4105) answered which puzzle piece is the first (rabbit poster = piece zero, rebus = piece one). It applies to that one question (7.2, doc 39). |
| `13` | "Obtaining message #8310's image is now the highest-value missing item" (6. The artifact still missing (and 9: 'not verified to be message #8310')) | The image was retrieved: it is the cover of Time-Life Mysteries of the Unknown: Cosmic Duality, from the export file for #8310 (7.4). The section 9 doubt about the identification is also superseded. |
| `14` | "`https://gsmg.io/<path>` returns **200** for a real page and **404** otherwise." (New validator: the site itself) | The 2026 site is a static rebuild and the original answered 200 to every path, so 404 never discriminated. Every URL-probe negative in this doc is void and carries no evidence either way (dossier 10.5, doc 68). |
| `14` | "That is a pointer at bit-level surgery on the 192 bits, which is the only reading under which" (Standing conclusion on the first image, first live lead) | The #FEFEFE cell is the gardeners' painted rose, forced to blue, consumed by the dbbi parse at program position 21 (4.3, 6.3). The bit-level prime pointer was tested (748 transforms) and is null (10.4). |
| `14` | "is the operative meaning of `yellowblue` in the message-8446 checklist" (Standing conclusion on the first image, second live lead) | yellowblueprimes names the dbbi parse: the poster colour program walked at prime positions, consuming 91 of 91 (6.3). The resistor code (yellow 4, blue 6) is a null observation (4.4, 10.4). |
| `14` | "the puzzle uses EBCDIC cp1141 at Phase 3.2.1, so this family was worth testing" (Format-level item 7, alternative character encodings) | The Phase 3.2.1 codec is cp273 (cp1141 is not a Python codec and no euro occurs in the data), with reciprocal Beaufort and key THEMATRIXHASYOU (3.4a). |
| `14` | "it is a legitimate oracle for a small number of well-motivated guesses" (Next surface: the rebus tiles, note on the form) | The verifier validates only the phase-1 answer and rejects everything later. Ten submissions characterised it fully. Do not submit more (dossier 1). |
| `14` | "the four tail spiral bits recorded as ambiguous, not as 0100" (poster audit, tail bits) | The four tail bits are 0000, measured (dossier 4.4 and 12). |
| `15` | "this is the string an earlier run used for slot 1, not an independently verified Phase 1 answer" (The Phase 1 answer: gap found, then closed) | Verified. The sha256 of the phrase equals the hash the creator posted (#225/#226, 2019-04-22). It is the song's phase-two opening up to its comma (3.1, 3.A). |
| `15` | "The one partial assembly that is unforced: `crypto` + `lo` + `gic` = **cryptologic**" (Tile contents, transcribed) | lo + gic spell LOGIC, the artist, and crypto is a separate token (dossier 5, doc 22). |
| `15` | "Three red, three blue, one black, one that is both (the open-padlock tile is red)." (Tile contents, transcribed, paragraph after the table) | Four tiles are red (t, crypto_gic, n_you, open_lock_n_ing), three are blue and one is black (dossier 5). |
| `16` | "It needs a **key**, and the key is the actual missing object." (What survives) | faed is filler: a machine-generated draw from a fixed biased distribution over nine symbols, homogeneous with dbbi's filler. It needs no key (6.4, 10.2). |
| `16` | "that is the profile of ciphertext or compressed data" (What survives, faed's payload is high-entropy) | The 6.89 bits per byte measures a filler draw over nine symbols. faed is filler (6.4). |
| `16` | "Under that reading `g` is framing rather than content" (What survives, last paragraph) | The g excess is a property of faed's filler generator; the dbbi residue shows the same excess (6.3, 6.4). |
| `17` | "Six checkpoints, all April 2020, **all with known preimages**, nothing after" (The two oracles, as they actually stand: Offline checkpoints) | The six GSMG.io: checkpoints were paid on 2020-03-24 (blocks 622762 to 622774). The oracle 3GSMG24 kept signing until block 691563 (2021-07-18); later messages are inbound from other keys (dossier 1). |
| `17` | "Read as suggestive only." (Phrase doors from the puzzle's own plaintexts, after the sweep table) | Void: the original site answered 200 to every path and the live site is a 2026 rebuild, so these probes carry no evidence either way (dossier 10.5, doc 68). |
| `18` | "so it is not a fixed-key cipher of a fixed text" (What this session established, item 5 (faed is high-entropy)) | faed is filler, homogeneous with dbbi's filler; its drift is 32 of 570 characters (P = 0.0201). The measurements support filler (dossier 6.4). |
| `18` | "the right sweep anchor, and the #39233 → #39237 threaded exchange supports it being the container the available material should open" (Where this doc left the problem, last paragraph) | #39237 implies yinyang (Cosmic Duality's plaintext) is reached after an AES decode, so SalPhaseIon short is the gate. Treating Cosmic Duality as the anchor inverted it (dossier 6.5, 11). |
| `22` | "Negative, but the lead is **not** exhausted" (3. The song's three parts map onto the puzzle, Tested here, null) | The song as text is closed: every 1 to 40 word span, line and clause, raw and double-hashed, is null (doc 99, about 79,000 candidates). The song acts as structure (3.A). |
| `22` | "it reads as an instruction that where the song says *black*, the poster says *white*" (4. A reinterpretation of the January 2020 poem) | The Roses poem is Alice in Wonderland Ch. VIII: a white rose painted red, with gardeners Two, Five and Seven naming the primes {2, 5, 7} (7.2). The song's rose line explains the war tile and the off-white cell (3.A). |
| `23` | "there are exactly **five** cases where the creator replies to a specific message with an affirmation" (5. Creator affirmations are rarer than assumed) | The endorsements are more numerous: also #60312 Bingo (Looking Forward), #4696 Correct, #4096 This one, #2905 Interesting, #8311 and #8483 (dossier 8.1). Check any claim against 8.1. |
| `23` | "Two independent derivations agreeing raises confidence that this is the intended referent" (3. Convergent derivation of lastwordsbeforearchichoice) | The referent of lastwordsbeforearchichoice is unidentified. The film's pre-door lines, the Hope line and Architect choice-point text are all null as literal text (dossier 9, 10.6, 10.8). |
| `23` | "The /(...) markers that appear throughout the Phase 2 and Phase 3 plaintexts" (tag discussion) | The phase-2 plaintext holds no tag. Three tags sit in the page HTML and three in the phase-3 plaintext, and all six are format specifications (dossier 3.3). |
| `24` | "Nothing lands on 479 or 484." (sec. 7, Correction: the 479 figure is NOT reproduced) | The canonical spiral traversal yields yellow 479 and blue 484 (563 and 497 with #FEFEFE as the 25th cell). Reproduced, and spent as a pointer: 1.88 loaded-phrase hits expected against 1 observed (dossier 12). |
| `24` | "Five mates in one is, by the conventions of composition, a broken problem." (sec. 10.2, Why this matters, and why it also cuts against itself) | In the posed position White has 14 moves, 13 mate, and only Rg6-c6 does not, so the key is unique. The five mates come after Black's forced reply (doc 42, dossier 3.3). |
| `24` | "The Architect text's own verb is **REINSERTING**" (sec. 6, REINSERTING THE PRIME BASICS tested as literal zero-reinsertion) | REINSERTING and PRIME are the film's words; the creator changed 'prime program' to 'prime basics' (dossier 3.4a, doc 35 sec. 3). The zero-reinsertion null stands (dossier 10.2). |
| `24` | "The "tiny hint" is the dot sequence itself." (sec. 3.4, table row for #53335 to #53342) | The quotation marks cite #881: the tiny hint is the Roses poem, and #53342 re-points to it. The dot messages themselves yield no value; the locator is null (dossier 7.3). |
| `24` | "in the same register as `givetit`. Untested." (sec. 3.2, #66961) | #66961 was tested as each container keyed by itself and is null (dossier 8.4, doc 103). |
| `25` | "It does *not* overturn `claude/16`'s conclusion that faed needs a key" (sec. 2, 6.89 bits per byte, 129 distinct of 173: FAILS as independent evidence) | faed is filler from a biased generator (dossier 6.4, doc 101), so it needs no key. The uniformity result stands as a description of that filler. |
| `26` | "The two structurally-motivated couplings that remain open" (sec. 2, The two 96-byte containers are NOT one split object) | Both were tested and are null: halves at string and password level (docs 111, 114) and lock chaining of every valid-padding output into the other locks (doc 110). See dossier 9, 10.7, 10.8. |
| `29` | "So the intended final plaintext is most likely `gsmg.io/<64 hex>`" (The insight) | Padding is fixed by length: 80 bytes of ciphertext admits 64 to 79 bytes of plaintext (bare hex key, gsmg.io/ plus hex, gsmg.io/ plus BIP38). The pad-habit argument fails (dossier 6.5, doc 59 sec. 5a). |
| `29` | "the acceptance test for any key/password search upgrades from" (The insight (recogniser upgrade)) | A recogniser limited to printable text and hex keys is blind to EBCDIC, UTF-16, binary and compressed plaintexts. The structure-agnostic recogniser with lock chaining replaced it (doc 110, dossier 2). |
| `35` | "both satisfied by the DBBI stage: strip the prime cells, keep the 60-symbol residue" (sec. 2, item 2 (primes and zeroing hints)) | The residue is filler (dossier 6.3), so stripping prime cells satisfies neither hint. The dossier keeps primes {2, 5, 7} and matrixsumlist as a prime operation with an operand outside the page (7.2, 9). |
| `35` | "The live stage is number two: the 60-symbol residue, the label `matrixsumlist`, and FAED" (sec. 7, item 2 (work the chain in page order)) | The residue and faed are filler (dossier 6.3, 6.4). The live problem is the operand of matrixsumlist and lastwordsbeforearchichoice, which lies outside the SalPhaseIon page (9, 12). No prime-walk layer was found in faed (10.6). |
| `39` | "so "our first hint" on it cannot refer to anything said in chat." (What this changes, item 2) | "Our first hint" is the creator's #225 chat post (the bare phase-1 sha256, "just try hit your options against that hash"), described in #257 as a hash which we provided. It states a method and names no operand (dossier 6.2). |
| `39` | "Solvers tie the Phase 2 line `# X 2 S H 4 Y 0 Q B 15 #` to those X,Y coordinates" (Timeline row 02-20 (Decentraland parcel)) | The template resolves fully to 51 deg 52' 28.0" N, 4 deg 24' 23.2" E, with X and Y as the two hemisphere positions (dossier 3.2). It gives no support for an April 2019 side-page plan. |
| `40` | "So "Another DOOR" is inside SalPhaseIon and DBBI is on the way to it." (What this establishes, item 2) | The door's location is open. dbbi is the poster's colour program plus filler with no payload (dossier 6.3); the dossier reads the nest hint as the site's door structure (7.2), and #9607 says any door derives from held information. |
| `42` | "**off-white cell** \| **unconsumed**" (Inventory table (also the residue and faed rows)) | The off-white cell is consumed: forced blue, it is the 21st program symbol of the dbbi parse (dossier 4.3, 6.3). The 60-symbol residue and faed are filler (6.3, 6.4), so nothing remains to consume in them. |
| `42` | "The whole line is consumed." (Stage 2, on "Raising the stakes without extra chances of winning") | The fubcd riddle seeds the checkerboard key (dossier 3.4b). "As wide as the first one seen" stays unconsumed surplus (12), and "raising the stakes" may concern the Terminal (6.5). |
| `42` | "The grid is cropped 3 px on the right" (Stage 0, pixel audit) | 1048 minus 13 x 75 leaves 73 px, so the last column is clipped by 2 px, and a 1-pixel white column sits at the image edge (dossier 4.1). |
| `43` | "Cosmic Duality is what the ingredient chain builds toward, so it opens first." (sec. 6, Order) | #39237 calls yinyang "the next phase" after an AES decode. If yinyang is Cosmic Duality's plaintext, Cosmic Duality opens after an AES decode, so SalPhaseIon short is the gate (dossier 6.5, 11). |
| `43` | "field 1  =  [ dbbi: key material ] [ matrixsumlist: the operation ] [ faed: the payload ]" (sec. 4-5, The z characters are field separators) | dbbi is the poster's colour program as b/be hosts plus filler, a verification object; faed is filler from the same generator (dossier 6.3, 6.4). Neither is key or payload. |
| `43` | "pad 8 matches the creator's habit (the three solved containers pad 8, 6 and 10, never 16)" (sec. 6, The three containers) | Padding is fixed by plaintext length, so no argument from an author's pad habit holds (dossier 6.5, doc 59 sec. 5a). Plaintexts of 64 to 79 bytes are all admitted. |
| `43` | "the operation that turns the 60-symbol residue into a key for faed" (The resulting map, closing paragraph) | The residue and faed are filler. The unplaced item is the operand of matrixsumlist and lastwordsbeforearchichoice, which lies outside the SalPhaseIon page (dossier 9, 12). |
| `45` | "and he dismissed it in chat as a typo" (What this kills, paragraph on 'Hundred fourty') | He dismissed only the spelling 'fourty' as an ancient-spelling typo (#5960). The number stands: part 6 of the phase-3 answer is exactly 140 characters, matching HUNDRED FOURTY (dossier 3.3). |
| `45` | "`SELF` is the only voice whose speech is entirely his own." (The three speaker-labelled voices) | The dossier (3.4a) records two speaker labels, YOU at offset 341 and ME at 371. The SELF at 1483 is a doubled word before the sign-off and sits in the surplus list; a third voice is unestablished. |
| `48` | "The 23 / 16 / 7 line should be treated as a binding count over a built object, not as film residue." (1. Correction: DBBI admits a second complete prime-host parse) | L=84 is rejected and L=83 decided: the spliced program's 23rd symbol is yellow and forced-blue selects L=83. The 23/16/7 numbers are the film's own, and every L=84 selection is null (dossier 6.3, doc 97). |
| `48` | "Adopt the L=84 parse alongside L=83 and stop treating 23 / 16 / 7 as film residue." (6. What to do with it, item 1) | Do not adopt L=84. L=83 is the parse (91 of 91, 23 hosts, 8 of them be). The Architect's 23/16/7 comes from the film (dossier 3.4a, 6.3). |
| `48` | "concludes it is hand-typed filler rather than a cipher of any text" (2. FAED: the statistical verdict, reproduced) | faed is homogeneous (P = 0.45) once its last 32 characters are set aside. The drift is those 32 of 570 characters (tail P = 0.0201); 0.0040 is the change-point figure. faed is machine-generated filler (dossier 6.4, 10.2). |
| `48` | "re-encoding through **EBCDIC cp1141**" (7.1 The codec pool (their E0083)) | The codec is cp273: latin-1 decode, encode to cp273, read the bytes as lowercase letters, then reciprocal Beaufort with key THEMATRIXHASYOU. 1141 is the puzzle's pun and adds only a euro sign (dossier 3.4a). |
| `48` | "Selection A is the 84-parse variant in which the 23 hosts represent URL bytes 1 to 23 exactly once each" (7.2 The coordinate serialisation of selection A) | Selection A rests on the rejected L=84 parse. L=83 with the off-white cell forced blue is the parse, and every L=84 selection is null (dossier 6.3, doc 97). The 'live' test has no valid basis. |
| `48` | "the next opening is a container password, and the candidate generator is his world, not the streams." (6. What to do with it, item 3) | The creator's-world census was built (384 strings) and swept with 475,808 decrypts: null, closed. The missing piece is the operand of matrixsumlist and lastwordsbeforearchichoice (dossier 10.1, 12). |
| `50` | "The remaining one is the coordinate serialisation of selection A." (The atlas's third unexecuted test, also closed) | Selection A depends on the L=84 parse, which is rejected (L=83 decided, dossier 6.3). Every L=84 selection is null (doc 97). No atlas test remains open on that basis. |
| `50` | "The deliverable is `gsmg_census.py`, a standalone generator plus oracle that anyone can extend by adding strings." (What was built) | No gsmg_census.py is in the Project file list, which is flat and holds no scripts. Rebuild from this doc's description. The result is carried in dossier 10.1 (384 strings, 475,808 decrypts, null). |
| `53` | "Every file on the site carries the same `Last-Modified`" (3. Server facts) | The site was restored in three steps: /theseedisplanted and /puzzle on 2026-08-15, robots.txt on 2026-08-16, the farewell page at / on 2026-08-17 (dossier 1). The live site is a rebuild, so it is no primary source. |
| `53` | "the last page is where his habits stop" (2. The three pages at source) | The bunny-hunter HTML comments are rebuild additions, absent from the archived captures of both pages (dossier 5, doc 55). They carry no information about the creator's habits. |
| `55` | "Unlike a probe, it is authoritative: it names routes the application itself considered real." (5. The one genuinely new lead (sitemap.xml)) | The 2022-08-21 sitemap.xml capture is text/html at 10,435 bytes, the catch-all SPA shell. No sitemap ever existed and the lead is closed (doc 68 section 2). |
| `58` | "The door oracle was not available (the live site is down; see `claude/54`)." (5. The word as a passphrase) | The live verifier at /phase1verification works. It validates only the phase-1 answer and needs the CSRF token from the page's meta tag (dossier 1, doc 63). It is no general door oracle. |
| `59` | "(`dbbi` / `matrixsumlist` / `faed`, still unread)" (7b. What that eliminates) | dbbi is solved (L=83 prime-host parse of the poster colour program, plus filler) and faed is filler. yellowblueprimes names that parse. Only the operands of matrixsumlist and lastwordsbeforearchichoice are missing (dossier 6.3, 6.4, 9). |
| `59` | "Keep the recognizer; scale by compute, not by loosening." (8. What I would do next, item 2) | Use the structure-agnostic recogniser with lock chaining (bit bias, distinct-byte deficit, magic headers, EBCDIC, UTF-16). The seven-class text recogniser is blind to non-text plaintexts (dossier 2, doc 110). |
| `59` | "something is counting a different object" (5d. Container sizes, for the record) | #9505 is silver_anth pasting two transcriptions of the SalPhaseIon-short blob side by side, differing by a stray z. 192 counts both pastes; the container is 96 bytes (doc 64 section 4). |
| `59` | "offset ~2292  "Raising the stakes without extra chances of winning." (2a. The decisive fact is positional (offset dump)) | The 149 digits occupy bytes 1990 to 2138 and the checkerboard riddle bytes 2143 to 2291. The Terminal starts at 2292 and the plaintext ends at 2422 (dossier 3.4). |
| `59` | "not independently confirmed in this project's bundled `jrk_messages.txt`" (5b. The decisive chat evidence is #4624; also table in section 9) | #4624 (2020-08-09, seed phrase or private key, answered 'a private key') was checked against jrk_messages.txt and is carried in dossier 1 and 8.3. |
| `60` | "open, `claude/57` §3; the `a`/`B` alphabet is unread" (3. The unconsumed inventory of phase 2 (table, first row); also 5 item 3) | Closed: the six tags are format specifications (aa/aaa lowercase, aBa mixed case, connected no spaces, enf enforced, one 'not enf' on the FEN). Six of six fit (dossier 3.3, doc 71 section 2). |
| `60` | "unexplained; `claude/57` uses only "worst gear" as the reversal instruction" (3. The unconsumed inventory of phase 2 (table, 'on the highway' row)) | Consumed: the coordinate is SafeNet's Rotterdam site (Seattleweg 5, Pernis) beside the A15 motorway (dossier 3.2, doc 71 section 3). |
| `60` | "and nobody has enumerated it." (1. The omission, stated exactly; repeated in 4 and 5) | The SafeNet/Luna vocabulary was enumerated and swept: 12,395 candidates against all three containers, null (dossier 10.1, doc 61). |
| `60` | "Nobody has checked whether the tile colouring carries a second, HSM-flavoured reading." (2.2 The Luna PED key ceremony) | Each tile's colour prefix marks which half of a rebus word it is (blue and black left, red right, confirmed by the padding). The colour layer has essentially zero capacity and no second channel (dossier 5). |
| `60` | "the missing object is a recognition from the creator's world" (6. Honest weight) | The missing piece is the operand of the two operations matrixsumlist and lastwordsbeforearchichoice. The creator's-world census (384 strings) and the Luna vocabulary are swept and null (dossier 12, 10.1). |
| `60` | "three ciphertexts in a public textarea, no JavaScript, no form, no verifier" (2.1 'security by hiding, nearly unprotected, in plain sight') | The SalPhaseIon page holds two containers in two textareas (SalPhaseIon short and Cosmic Duality). Terminal sits at the end of the phase-3.2 plaintext (dossier 6.5). |
| `63` | "The on-chain checkpoints (closed since April 2020" (3. The decisive test: the route validates ONLY phase 1) | The six GSMG.io: checkpoints were paid on 2020-03-24 (blocks 622762 to 622774). The oracle's own signed messages run to block 691563 (2021-07-18). Both oracles are closed (dossier 1, doc 113). |
| `63` | "This project does not hold that census at all" (6. Where this leaves the board) | The census was built in doc 50 (33 groups, 384 strings) and swept with 475,808 decrypts: null. The personal census is closed (dossier 10.1, 12). |
| `63` | "The candidate stream is the only work left that is generative." (6. Where this leaves the board) | The missing piece is the operand of matrixsumlist and lastwordsbeforearchichoice. Candidate streams from public and personal sources are swept and null (dossier 12, 'What remains'). |
| `63` | "`claude/60` §2.2's audit of the phase-1 tile colours and padlock states" (6. Where this leaves the board, third item) | Tile colours mark the left or right half of each rebus word and carry no second channel (dossier 5). Nothing remains to audit under a custody reading. |
| `63` | "re-run the existing FAED and `matrixsumlist` key families" (6. Where this leaves the board, second item) | Done: acceptance test for raw binary keys, 215,550 configurations, 0 hits (dossier 10.1). faed is filler, so key families over it are closed (dossier 10.2). |
| `64` | "FAED is not a cipher of anything; it reads as hand-typed filler." (2a. The dbbi/faed claim) | faed is machine-generated filler from a fixed biased distribution, homogeneous with dbbi's filler once its last 32 characters are set aside. The p = 0.004 'wandering marginals' figure is the change-point test (dossier 6.4). |
| `64` | "DBBI is unread, FAED is measured as non-cipher" (6. The question it ends on) | dbbi is solved: the L=83 prime-host parse consumes 91 of 91 and equals the poster colour program plus filler. yellowblueprimes names that parse. faed is filler (dossier 6.3, 6.4). |
| `64` | "was true in April 2025 and is still true here" (6. The question it ends on (X's #39225)) | The prime walk is solved: dbbi's 23 hosts sit at the primes up to 83 (dossier 6.3). The prime set {2, 5, 7} comes from the Roses poem (dossier 7.2). |
| `64` | "DBBI is a different object and the claim survives for it" (2a. The dbbi/faed claim) | dbbi carries no payload beyond the colour-program check and filler. L=84 is rejected and L=83 decided (dossier 6.3). The idea that the missing word is written in dbbi is closed. |
| `64` | "All from `telegram/ChatExport_2026-09-13_result.json`, 69,023 messages indexed." (1. Citations verified) | The full Telegram export is absent from the Project. Only jrk_messages.txt (492 creator messages with reply headers) is bundled, and non-creator parents are known only from those excerpts (dossier 13). |
| `65` | "Cosmic Duality is the anchor for all future sweeps." (Section 2, 'Operational consequence, adopted') | Inverted. The threaded reply #39237 puts yinyang after an AES decode, so if yinyang is Cosmic Duality's plaintext, SalPhaseIon short is the gate. Screen all three containers on every candidate (dossier 6.5, 11). |
| `65` | "sharper than a padding check, and the ordering argument (#39233 → #39237, threaded) says it is the" (Section 8, standing rule 1 (continues 'container that should open with material already in hand')) | The ordering argument runs the other way: Cosmic Duality opens after an AES decode, so it is not the container that opens first with material already in hand (dossier 6.5). |
| `65` | "`claude/59`'s three runs are the project's most careful container work and under this model they" (Section 2, table and text ('carry no information about the known vocabulary')) | Under the corrected ordering the 80-byte containers are the likely first gate, so the doc 59 nulls stay informative about the known vocabulary. All three containers are screened together (dossier 10.1). |
| `65` | "DBBI remains the live half, as agreed." (Section 5, 'Net') | dbbi is solved (L=83 prime-host parse, 91 of 91, poster colour program plus filler) and faed is filler. Neither half is live (dossier 6.3, 6.4). |
| `65` | "FAED is not a **fixed-key cipher of a fixed text**." (Section 5, the correction to docs 47, 48 and 56) | faed is machine-generated filler from a fixed biased distribution, homogeneous with dbbi's filler. The open question about its nature is closed (dossier 6.4). |
| `66` | "under the ordering argument their passwords come from CD's plaintext" (Section 5, limit 5 (also section 1, 'Cosmic Duality is the stage-1 target')) | Inverted ordering. #39237 makes SalPhaseIon short the gate and Cosmic Duality the later container, so the 80-byte blobs are the containers to screen first (dossier 6.5). |
| `66` | "The two 80-byte blobs were only screened at stage 2." (Section 5, limit 5) | Doc 71 section 5 screened all 2^30 chain-order subsets and 17.8M orderings directly against Terminal and SalPhaseIon short, with in-space controls: 0 hits (dossier 10.1). |
| `66` | "The missing token is external." (Section 6, 'The honest reading') | Withdrawn in doc 70 section 6: the sweep bounds arrangements of decoded objects only. The gap is the operand of matrixsumlist and lastwordsbeforearchichoice, outside the page and every decoded object (dossier 12). |
| `66` | "\| 16 \| cp1141 \| 4 \| `1141` \|" (Section 1, atoms table, atom 16) | Atom 16 is the hint string 1141 from the Architect intro. The decode codec is cp273 (CP1141 only adds the euro sign, absent from the data; dossier 3.4a). |
| `68` | "it is external to everything the puzzle has produced" (Section 6, 'Honest weight', last sentence) | Withdrawn in doc 70 section 6. The sweeps bound arrangements of decoded objects only. Derivations and the operands of matrixsumlist and lastwordsbeforearchichoice stay open (dossier 12). |
| `68` | "Two small pulls that remain unexecuted" (Section 5 heading) | Attempted in doc 69 (nothing returned), then retrieved in doc 106: both captures are the GSMG web application shell with no door (dossier 1, #32699, #32701). |
| `69` | "It sits with "on the highway" (`claude/57` §1) and the `a`/`B` tag" (Section 5, 'Status: observed, unconsumed') | "On the highway" is consumed (SafeNet Rotterdam beside the A15, doc 71 section 3) and the /(...) tags are format specs (doc 71 section 2, dossier 3.3). Only the underscore emphasis stays unconsumed. |
| `69` | "Both are closed as unavailable rather than as negative." (Section 1, result of the two pulls) | Both were later retrieved (doc 106): the archived /Puzzle and /phase1verification captures are the GSMG web application shell with no door (dossier 1). |
| `70` | "On positional fit, 84 is the better match, not 83." (Section 2, item 3 of 'Three facts follow' (and Net: 'The poster no longer supports the 83-cell parse')) | With the off-white #FEFEFE cell in the 25-entry schedule, L=83 matches the poster 23 of 23 and L=84 misses one. L=83 is settled (doc 71 section 1, dossier 6.3). |
| `70` | "60 and 61, and neither is privileged" (Section 2, Consequences, 'Both residues are live again') | The 60-symbol residue is filler from faed's generator and L=83 is settled. The 61-symbol L=84 residue is rejected (dossier 6.3). |
| `70` | "That is the first non-aesthetic reason to prefer 83 this project has had." (Section 4, DEL as an operation selecting 83) | The poster's 25-symbol colour program selects L=83 exactly (23 of 23, off-white cell forced blue). DEL-as-operation is not needed for the parse (dossier 6.3, 4.3). |
| `70` | "The personal-census theory stays on the table." (Section 6, last paragraph) | The personal census is closed. The remaining gap is the operand of matrixsumlist and lastwordsbeforearchichoice (dossier 12). |
| `70` | "that pipeline has twice the input space it had this morning" (Section 7, matrixsumlist 'bounded, not closed') | Only the 60-symbol residue is live, and it is filler. The input space did not double (dossier 6.3). |
| `70` | ""FAED as an index reservoir" as a category" (Section 5, closing paragraph) | faed is filler from a fixed biased generator (dossier 6.4, 10.2). An index-reservoir reading has no support. |
| `71` | "The payload is 60 symbols, fixed." (Section 8 (also section 1, 'The 60-residue is the payload')) | The 60-symbol residue is filler from faed's generator (doc 101, dossier 6.3). The missing piece is the operand of matrixsumlist and lastwordsbeforearchichoice. |
| `71` | "Standing rule 5 (anchor every sweep on CD) rests on that identification," (Section 4, 'yinyang = Cosmic Duality is an assumption') | The anchor rule is retracted (dossier 6.5, 11). The threaded reply #39237 puts yinyang after an AES decode, so SalPhaseIon short is the gate. Screen all three containers on every candidate. |
| `71` | "#8569 answered the two neighbouring questions plainly and this one with "Can't say anything about this."" (Section 3, 'What stays open') | #8569 is one three-line message: Correct. / No. / Can't say anything about this. Which line answers which question, and what #8568 asked, is open (dossier 3.2). |
| `72` | "yes/no, and it is the only change that alters the economics of the whole search." (Section 'The pivot: get a verifier') | Doc 73 executed it: the live hash-path oracle confirms only the known SalPhaseIon side-page URL (391 probes, 1 hit, the known page). It is no general answer verifier. |
| `72` | "Four second-address paths have never been requested" (Section 'The pivot: get a verifier') | Requested in doc 73: all four and 21 other recorded hashes return 404 (25 probes, 0 hits). The second-address hypothesis is dead. |
| `73` | "dbbi (91) and faed (570) are the only material in hand that has never read" (Section 'Honest state at end of session' (also 'dbbi and faed are the only unconsumed objects in it' under Block [765,860))) | dbbi is consumed (poster colour program written as b/be hosts at prime positions, plus filler) and faed is filler. SalPhaseIon's a..i content is fully accounted for (dossier 6.3, 6.4, 9). |
| `73` | "not a gate a solver walks through by solving something." (Section 'But it is a one-off, not a general answer verifier', preimage paragraph) | The side-page URL is the 2020 second door, reached by HASHTHETEXT from the Decentraland audio side quest and the poster text. Its preimage holds no answer, and solvers reach it (dossier 4.5). |
| `76` | "Yellow and blue are spent. Only "primes" is unspent." (Section 2, 'yellowblueprimes decomposes') | yellowblueprimes is solved: the dbbi prime walk applies the poster's colour program at prime positions, L=83, 91 of 91 consumed (dossier 6.3, 7.1). The colour layer is read by that walk. |
| `76` | "What is left standing is narrow and specific: a second straddling board whose" (State section, last paragraph) | dbbi is the poster's colour program plus filler and faed is filler from a fixed nine-symbol generator, so no second board decodes them (dossier 6.3, 6.4, 10.2). |
| `76` | "the one place where a hand-placed prime index and a deliberate single-cell" (Section 3, 'The anomaly cell as a pointer') | Fourteen spiral positions (152 to 158, 160 to 166) give the walk the same program. Cell 163 is prime by both counts but was chosen post hoc, at a fair price of about 1 in 5 (dossier 4.3). |
| `77` | "dbbi and faed are high-entropy data rendered in base 9" (Section 'The independent evidence', Conclusion) | dbbi is the poster colour program as b/be hosts at prime positions plus filler; faed is filler from a biased generator, non-uniform at p=1e-8. Neither is a key, hash or compressed bytes. |
| `77` | "They are 91 and 570 base-9 symbols of high-entropy data" (Section 'State') | The question of what they encode is answered: dbbi re-encodes the poster colour program plus filler (dossier 6.3) and faed is filler (6.4). Neither is treated as an encoded 36 or 226 byte payload. |
| `78` | "faed is large and near-uniform" (Section 'The correction to doc 77', asymmetric reading (dbbi a key or instruction, faed the payload)) | faed is filler from a fixed biased generator and carries no payload. dbbi is the poster colour program as hosts plus filler, a verification object with no key or instruction (dossier 6.3, 6.4). |
| `78` | "faed is essentially maximal-entropy base-9" (Section 'The correction to doc 77', frequency table) | Entropy is near maximal but the symbol chi-square is significantly non-uniform (chi2 43.7, p=6e-7), which excludes modern ciphertext, a key or a hash (doc 87). faed is filler. |
| `78` | "April 2020, all with known preimages, nothing after" (Correction 2 (repeats 'all paid in April 2020' from Correction 1)) | Checkpoints were paid 2020-03-24 (blocks 622762 to 622774). 3GSMG24 has 30 transactions, 14 signed by its key up to block 691563 (2021-07-18); the neighbours payment supplies four near-miss targets. |
| `78` | "address = P2PKH of the COMPRESSED pubkey" (Section 'A better screen, verified') | True for the checkpoints. The prize hash160 a9553269... is of the uncompressed pubkey, so the win test must check both point forms (dossier section 1). |
| `81a` | "This is the only mechanism found that acts on faed, has a null in the 1e-5 range," (A1 section, closing paragraph (also the intro and the 10 / 200,000 = 5e-5 figure)) | Retracted in doc 82. The null held the first word fixed. The honest price is about 1 in 481, real faed yields fewer readable variants than shuffles (P=0.93), and the method generalises to nothing. faed is filler. |
| `81a` | "The creator's marker set is {1},{4},{21}." (Section 'The recurrence of 21' (also in A2)) | The 1 April 2021 {1},{4},{21} post was an April Fools joke (#7529, dossier 8.5), so it is no creator marker set. |
| `81a` | "Four independent objects point at the same index." (Section 'The recurrence of 21') | Prime row 21 comes from the retracted A1 read, YOUWON at 21 is p=0.088 under a generic null, and the marker set is a joke. Only the FEFEFE position is solid. The recurrence is no evidence. |
| `81a` | "VERIFIED, with a caveat that matters." (Heading of A2) | The creator answered 'Pfff. Coincidence.' (#70307). The pivot cannot coexist with the prime grammar; treat it as coincidence (dossier 10.5). |
| `81a` | "four leftover bits are `0100`" (Worldmaker paragraph, readings that fail (also 'bit balance is 102/94')) | The four leftover bits are 0000 (measured). The poster has 101 set and 95 unset cells. The 0100 and 102/94 came from a wrong matrix.json centre cell (7,6), fixed 29 September. |
| `81a` | "Three things remain untested and are where I would go" (Section 'Next') | All three were screened in doc 82 (about 110,000 exact screens on the 133 characters, the 437 discarded characters and the row index set): zero hits. The prime walk is dbbi-specific. |
| `81b` | "the only branch with a live rationale behind it" (Section 3, closing paragraph (residue as key material against faed, 'doc 79 step (b)')) | Closed: the residue and faed are filler from one generator (doc 101; dossier 6.3, 6.4), and keystream, running-key and passphrase screens over both are null (dossier 10.2, 10.3). No live branch remains in this family. |
| `81b` | "uniform under every reading tried" (Section 3, sizes of the residue (~190 bits) and faed (~1806 bits)) | faed is significantly non-uniform (chi2 43.7, p=6e-7) and the residue fits faed's biased distribution (G=10.40, p=0.26). Both are filler, so the bit counts carry no payload. |
| `86` | "a fixed key over a fixed text is **not excluded**" (Section 'The correction to doc 03' (and Verdict: fixed-key class open again for faed[0:538])) | Doc 87 worked the class and closed it: 1,132,326 running-key candidates, all 45 escape sets, columnar widths and homophonic partitions are null. faed is filler (dossier 6.4, 10.2). |
| `87` | "Classical homophonic substitution qualifies in principle" (Section 6, What would overturn this) | Homophonic substitution was run afterwards (doc 88): all 21,145 set partitions, P=0.2233 and 0.4300, null (dossier 10.2). faed is settled as filler. |
| `90` | "Cosmic Duality image opens with a four-letter elision" (Section 2 (also the #8311 table row and Section 5 item 2)) | #8311's four dots are an ordinary ellipsis (doc 112); the creator writes four dots that way in #990 and #66568. No word is elided (dossier 7.3, 7.4). The image was recovered in doc 91. |
| `90` | "Never interpreted" (Section 1 regressions table, New Year tiny hint row) | Docs 111 and 112 read it: the quotation marks around tiny hint cite #881, the Roses poem, so #53342 re-points to that poem. The dots still yield no value (dossier 7.3). |
| `90` | "These four items make that rule actively harmful until they are restored." (Section 1 (and Section 5 item 1, restore sections 1 to 2 into the dossier)) | Restored on 22 September: tag alphabet in 3.3, on the highway in 3.2, tiny hint in 7.3, and #66898, #66961 and #66962 in 8.4. Section 5 item 1 is done. |
| `91` | "Poster-level symmetry tests (dossier 10.4) did not test that operation specifically." (Section 6, closing paragraph) | Seed-of-the-opposite was then tested on the poster and every textarea block (doc 92; dossier 10.6: 945 transforms plus hex, null). The yinyang operation reading is closed (dossier 9, 12). |
| `91` | "The dossier's one unexplained property of `#FEFEFE` has the same shape" (Section 3, book passages) | The mismatch is consumed: the song's red-or-black rule (line 9) forces the in-between cell to one side, only blue parses dbbi, and Alice Ch. VIII gives the painted rose (dossier 3.A, 4.3). |
| `96` | "The Architect text may be the SalPhaseIon manual, and that argues for L=84." (Review: what the record suggests has been missed, item 1) | L=84 is rejected. The L=83 prime-host parse is decided: F forced to blue gives the only exact fit (91/91, all hosts start b, 8 be), and L=84 contradicts the spliced program's 23rd symbol (doc 100). |
| `96` | "rests on the `#FEFEFE` splice, which the dossier itself prices as a 1-in-12 positional inference." (Review, item 1 (basis for L=83)) | The painted-cell count is 14 (doc 105); the identity is priced about 1 in 5, post hoc. L=83 is settled by the forced-blue exact fit of 91/91 (doc 100). |
| `98` | "`GSMG-PUZZLE-DOSSIER.md` never mentions the song." (1. The dossier is missing the puzzle's backbone) | The dossier carries the song as section 3.A, restored on 23 September (docs 98 to 100). Its full text is kept out of the project. Section 11 records the omission as a correction. |
| `98` | "The full lyric text of "The Warning" is needed to test the unused lines" (3. What is blocked, and the next step) | The full 13-line text was supplied by the user and tested in doc 99 (null as text). It is deliberately kept out of the project (dossier 3.A, 13). |
| `99` | "The dossier still needs a section on the song; it was dropped after doc 22." (Status) | Restored as dossier section 3.A on 23 September; no further section is needed. The song text stays out of the project (dossier 3.A, 13). |
| `100` | "With these two consumed, the remaining surplus is: the 60-character" (Status (surplus list)) | The residue is filler from faed's generator (doc 101), so it leaves the surplus. The dropped H sign was read in doc 102 with no value. Current surplus: dossier 12. |
| `100` | "four-dot reply (#8311)." (Status (end of surplus list)) | The four-dot reply #8311 is an ordinary ellipsis and left the surplus list (doc 112; dossier 7.3, 12). |
| `101` | "the dropped `H` sign, the four-dot reply (#8311)." (3. What this means, final paragraph (surplus list)) | The four-dot reply #8311 is an ordinary ellipsis (doc 112). The dropped H sign was read in doc 102 with no value. Both left the surplus list (dossier 12). |
| `102` | "the four-dot reply (#8311)." (Status (remaining unconsumed items)) | The four-dot reply #8311 is an ordinary ellipsis and left the surplus list (doc 112; dossier 7.3, 12). |
| `103` | "part of the poster whose content, the rabbit ink, has only ever been tested as a number string." (3. What the re-read supports) | The nest was also read as a bitmap and at sub-pixel level in every order (docs 14, 105): best 0.64 printable, no hits. Its pixels are the drawing and carry no data (dossier 4.4, 10.4). |
| `103` | "and #2918 puts something in the Terminal container." (3. What the re-read supports (and table row #2918)) | Hedged in dossier 6.5: the question relays a third-hand claim, the Terminal blob first appeared in chat at #3806 (2020-05-09), and #2910 declined to localise the key. Not proof the Terminal holds it. |
| `106` | "The site is down, so the hashes could only be screened as passwords and keys, not visited as doors." (Zeroed poster text, closing parenthesis of the test paragraph) | gsmg.io has been live since the August 2026 relaunch (dossier section 1, doc 108). It serves only /theseedisplanted, /puzzle, / and robots.txt and returns 404 elsewhere, so a hashed door path can be checked live. |
| `109` | "Still open by size alone: faed with arbitrary `g` choices (2^107), and dbbi with `b` as the zero (2^25, low prior because `b` marks the hosts)." (Status) | Doc 115 ran all 2^25 subsets of dbbi's `b` as the zero, in numeric and string forms, forward and reversed (4.03 billion decrypt tests): null. Only faed with arbitrary `g` choices (2^107) stays open (dossier 6.4). |
| `111` | "The creator messages were not scanned this session (export not staged)." (Lead 4: the dots, Locator bullet) | Doc 112 scanned all 492 creator messages from the Telegram export: no run of five words with lengths 1 to 5 (or 5 to 1). Null; closes the item. |
| `114` | "letter and mod-10 forms were not crossed (that would be ~3x more and is the obvious extension if a reason appears)." (1. The literal #8446 joint password) | Doc 115 crossed the letter and mod-10 forms with the last-words pools (1.24 billion decrypt tests, null), and the other operand families as well. |
