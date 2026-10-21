# 117 - Riddle rounds R1 to R35, the per-container verdicts, and the pair ledger (all null)

**6 October 2026 interpretation notice.** This is a dated research record.
Its candidate counts and original logs are preserved, not freshly rerun.
Read [doc 118](118-correctness-audit-remediation.md) for detector/coverage
limits and [doc 119](119-current-evidence-ledger.md) for current findings.
A null applies only to its complete tested tuple.

Uniqueness, consumed instructions, mandatory lock order, and unique creator use of v0.3.10 were overstatements. The dated section-8 authorization/block is not an active queued task.

Dates: 3 to 4 October 2026. This doc collects the project work done after doc 116. Each workstream has its own folder under `claude/` with its write-up, scripts, candidate lists and run logs; this doc says what each one found and where it leaves the frontier. Statements marked INFERRED are readings, not measurements.

Result in one line: about 2,500 hand-justified candidate strings (counting re-runs under new forms and ciphers) and 1.68 million decrypts across ledger rows R1 to R35 and the cross-camp block, plus 11,397 structural key tests, all null with live controls. The most important output is not a null but a method correction (section 11): a joint-password null kills a **pair** of readings, never a single label's reading.

## 1. Why the method changed

`claude/critical-review-2026-10-03.md`, requested by the owner. Every password that ever opened a gate was a riddle answered from outside knowledge (the song, the film, trivia) and concatenated in the stated order; no answer word appears on any captured page. Decoded data (Architect text, checkerboard, dbbi) only ever produced messages or checks. Yet nearly all of doc 115's 7.29 billion decrypts were data arithmetic. Wide candidate pools mean a riddle is unsolved, because the creator makes each step unique.

Direction set by the owner on 3 October 2026, and still in force:

- No new method gets CPU unless it retrodicts the phase 2, 3 and 3.2 answers (`riddle-method/retro.py`, which must compare the decrypted plaintext hash, not just a valid pad).
- Work each label as a riddle with one answer that can be justified in one sentence; test a few at a time.
- No more coverage sweeps. One bounded enumeration shaped by the creator's own "23 ciphers / 16 encryptions / 7 intertwined passwords, brute forcing might be required" line was approved (section 8), with its size stated first.
- Never propose anything that needs another person (no human blind solver, no community, no creator). When readings run out, find a new angle.

## 2. Testers and controls

| tester | what it runs | controls |
|---|---|---|
| `riddle-method/rt.py` | all six containers, password forms raw / hex sha256 / double hash / hex of hex, EVP SHA-256 and MD5, structure check on every valid pad, win test (single and double hash) on the candidate and every 32-byte window of a flagged output | key 1; phase 2, 3 and 3.2 open and are recognised |
| `microstep/ms.py` | the same with `\n`, `\r\n` and ` \r\n` appended before hashing (`echo ANSWER \| sha256sum` on Linux and Windows) | three planted openssl containers keyed with newline forms |
| `independent-model/ct.py` | 4 forms x 5 KDFs (EVP MD5, SHA-1, SHA-256, SHA-512, PBKDF2-HMAC-SHA256 10,000) x 14 ciphers (AES-128/192/256 CBC and ECB, Camellia-128/192/256, SEED, SM4, 3DES, Blowfish, CAST5) | 11 planted containers, 7 made by the openssl 3.0.13 CLI |
| `riddle-method/retro.py` | retrodiction gate: does a method, fed only what a solver could see, reopen phase 2, 3 and 3.2 with the known plaintext | text windows (61,655 to 98,118 per stage) open nothing; the hardcoded known-answer fixture opens all three (regression verification, not independent validation) |

The scripts default to the repository root for the kit files; set `GSMG_KIT` to point elsewhere. Every null below had its controls fire in the same run.

## 3. The riddle ledger (`riddle-method/README.md`)

| rows | readings | candidates | decrypts | result |
|---|---|---:|---:|---|
| R1 to R10 | 23/16/7 as `twentythreesixteenseven`/`231607`; the door line, `theproblemis`, `wewont`; #225 as the first hint; yinyang as Smith; `neo`; sha256-each-then-join | 78 | 3,744 | null (14 pads, ~14.7 expected) |
| R11 to R14 | the film's sum sentence: `yourlife`, `trace`, `infrared`, `theone`/`anomaly`, crossed with film last words | 125 | 6,000 | null |
| R15 to R21 | every earlier answer under 13 more ciphers and PBKDF2; #867 `giveit = givetit` as the first hint; `giveit` in front; key stretching; `101`; the 3.2 blank choice; self-reference | 528 | 443,520 | null (1,702 pads, ~1,740) |
| R22 to R27 | per-lock split: Terminal = left door (Architect's last words before the doors, `trinity`); short = right door (`thesource`, `salvation`, `zion`); Cosmic = the pair | 25 | 22,200 | null |
| R28 to R30 | line-ending forms on every ledger answer; answers typed as written; `causality` as the last part | 599 | 106,428 | null |
| R31 | the canonical last-words line in the creator's transcript wording ("nothing **that** you can do") | 428 | 426,288 | null |
| R32 | shell history: `!!`, `!1` and variants | 6 | 288 | null (0 pads, ~1.1) |
| R33 | the remainder of the poster program: centre cells `0000`, `zero`, leftover B, Y as `3` | 198 | 175,824 | null |
| R34 | "return to the source codes": the genesis comment block in Satoshi's `main.cpp` | 21 | 18,648 | null |
| R35 | the rest of the v0.3.10 genesis construction (raw coinbase, pubkey un-reversed, hash160, address, row 1616 whole) | 27 + 2 | 23,976 | null |

Valid pads matched expectation in every run; 0 flags beyond the planted controls; 0 win-test hits.

Round 2 also tried a blind retrodiction with a fresh model given only the pre-phase text. It recognised the puzzle and recalled the published answers, so the test was contaminated. Its remembered phase-3 answer was wrong in form (the FEN after Rg6-c6 was not applied), which shows that remembered answers must be tested, never assumed.

Round 4 read every line the creator inserted into his Architect text as a literal operation ("return to the source codes", "reinserting the prime basics", #8000 "zeroed out", "select from over twenty three ciphers sixteen encryptions and/or seven intertwined passwords", "worth hundred fourty"). Each had already been executed, most exhaustively (dossier 10, docs 75, 97, 106, 114, 115; failed-attempts log T24, T44). Only faed with arbitrary `g` (2^107) is open, and it is not enumerable.

## 4. Independent re-derivation (`independent-model/README.md`)

A model built from the primary files alone, then compared with the dossier. Main divergences: the textarea reads as a terminal transcript (`enter` sits where `openssl -a` breaks base64 at 64 characters); the creator's first self-described hint is #867, not #225; dbbi's hosts write blue as `b` (2) and yellow as `be` (25), so the leftover program symbols spell `BY` (no password); `thispassword` may serve the Terminal, which would make the Terminal and short container separate locks (INFERRED). Every testable divergence ran as R15 to R27 and is null.

## 5. The two dated creator claims (`microstep/README.md`)

- #6509 (14 Mar 2021) "unforeseen hint" is the prime slip #5966 ("You are at the prime part already???"), self-flagged in #5969. It is consumed by the dbbi parse and gives no new string. "Infrared" (#6250) was deliberate and disowned.
- #32579 (29 Nov 2024) "1 microstep": at that date the community held every label but not the dbbi parse. "Our first hint is your last command" drew a zipped-mouth reaction (#20224), not a denial. A microstep read as a change of form gave R28 to R30, null.

## 6. Constraint table (`constraints/README.md`)

Every constraint (convention, container sizes, dated creator claims, reactions, page structure, nulls by class) was pooled and the readings intersected.

- Ciphertext lengths are multiples of 16, compatible with padded block encryption. This does not exclude stream modes. The 1/4,096 estimate requires independent uniform residues modulo 16, which are not established.
- The creator's difficulty claims run optimistic (#879, #4590, #8796, #32579), so they are weak bounds.
- #8354 and #8385 (theory of everything, 42) are a joke thread off #8308, not a pointer.
- Only R31 survived the intersection, and it is null. Verdict: nothing satisfies every constraint. The constraint most likely wrong is "one reading gives one candidate", which the creator's own Architect additions contradict.

The kill matrix in that file was built slot by slot and is superseded by the pair ledger (section 11).

## 7. Are the containers rabbit holes? (`rabbit-holes/README.md`)

- No bypass exists. The creator says the key is stored online encrypted, "to be found by solving" (#7830 to #7834); no other URL is needed (#9607); no internet is needed (#16624); the containers are "still valid" with sites down (#63957).
- SalPhaseIon short: on the path (the second route, #4694 to #4696). Target it first. Cosmic Duality: on the path as a message (yinyang, #39237, #9599), not a key holder. Terminal: the only rabbit-hole candidate (no riddle, no "ciphered with" line; #2017, #2026).
- Leak test (`leak.py`): randomness tests cannot identify AES; historical 64-byte random controls mismatched the 80-byte short/Terminal ciphertexts. Under the 16-byte PKCS#7 hypothesis, short and Terminal hold 64 to 79 bytes, one sha256-hex password or hex key; Cosmic holds 1,312 to 1,327 bytes, a message or nested envelope.
- Structural checks (`structural.py`), 11,397 tests, null: EVP keys and IVs of the solved gates as scalars, raw-ASCII atoms (control: the poster URL reproduces the `148XH2YBmL` checkpoint), every 32-byte and 64-hex window of every text and blob, poster grid integers, the 149 digits and genesis-140 as integers. No WIF or BIP38 string anywhere.
- One-password model (follow-up 2): read in order, the textarea says operations, then `thispassword`, sha256, the short container, then "sha256 the answer too". Only the short password is unknown; the rest follows by hashing (INFERRED).

## 8. The approved bounded enumeration, blocked (`selection/`)

The owner approved one bounded enumeration on 3 October 2026 ("yes bounded"): ordered selections k = 1 to 7 of the 23 chain atoms in `selection/atoms.txt`, plain concatenation, canonical convention, about 1.31 billion candidates, with phase 2, 3 and 3.2 reopening at k = 1, 7 and 3 as retrodiction controls. `selection/sel.c` is the generator. Two attempts were stopped by an automated safety check while the harness was being written or launched. **Nothing was run against the containers.** The space is untested, not null.

## 9. Source pointer and the genesis code (`source-pointer/`, `genesis-main-cpp/`)

- The failed-attempts log's 1008/868 pointer cannot be rebuilt from any recorded object. 140 = 2 x 1008 - total, so it is one event, and a random index lands on a word start in the instruction paragraph 4.0% of the time (61/1,539). Chance-level, like the 479 pointer.
- Row 1616 identifies the file: of every `bitcoin/bitcoin` release tag from v0.1.5 to v0.4.0, only **v0.3.10** has the scriptSig comment on row 1616. Retrodiction passes: the text after " 4 " on that row rebuilds the phase-3 password by script. Both `main.cpp` versions are kept in `genesis-main-cpp/` (MIT licence).
- R34 and R35 exhaust the genesis construction as standalone answers. Its values could still be atoms in the blocked 23/16/7 selection.

## 10. The poster photo (`photo-analysis/`)

`puzzle.png` (sha256 `38125bbd...`, matching the 2020 Wayback capture) re-checked with planted controls: chunks, trailing bytes, alpha, a hidden-mark scan of the lower panel, the logo's LSB plane, the QR at codeword level (version 4-L, mask 2, ECI 26, standard pad `EC 11 EC`, Reed-Solomon parity matches) and font-glyph determinism. Nothing hidden. The photo has no spare channel.

## 11. The shared flaw and the pair ledger (`common-flaw/README.md`)

`matrixsumlist` and `lastwordsbeforearchichoice` may feed one password; under that hypothesis, a null kills only the tested pair. The record nonetheless struck readings off per label (the constraint kill matrix, "spent" verdicts on R2, R3, R7, S1, R1, R8, R11 to R14, R19 and on the 1,558 poster lists as M). Each camp also paired only within itself:

- The data camp (docs 114, 115): poster sum lists x windows of the creator's Architect text. No film line in any L pool.
- The riddle camp (R1 to R35): film lines x riddle M answers. Poster lists were excluded by the review's rule, so they never met a film line.

Phase 3 itself mixed source classes in one password (trivia, a string copied from source code, a computed chess position). The page points M inside (dbbi, the poster check, sits right before `matrixsumlist`) and L outside (the creator deleted the door scene from his Architect text), so the most literal pair is poster-derived M with film-derived L (INFERRED), the pair neither camp formed.

**Block (a) tested:** the poster's row and column sums (off-white cell as 0 and as 1) in digit, comma, comma-space, space, Python-list and JSON forms (24 M strings) x film L (S1 wording and cuts, R2, `wewont`, `theproblemis`), M+L, L+M and M+L+thispassword only. 456 historical candidates; L+M+thispassword was omitted. The corrected `common-flaw/cross.txt` has 600 candidates and has not been searched.

| tester | decrypts | valid pads | flags |
|---|---:|---:|---:|
| `rt.py` | 21,888 | 87 (~85.8 expected) | 0 |
| `ms.py` | 49,248 | 223 (~193) | 0 |
| `ct.py` | 383,040 | 1,463 (~1,502) | 0 |

Win test 0 hits. Controls fired in all three. Null.

**Block (b) untested:** riddle M answers (about 10) x the 175 `lw_core` Architect-text windows, both orders, about 3,500 candidates. It is a pool cross, so it was not run under the no-sweep rule; it is the owner's call.

What stands and what does not:

| item | status |
|---|---|
| every decrypt null as a fact about the strings tested | stands |
| single-label-alone nulls | stand (they test one-label-per-lock models) |
| convention, container sizes, cipher class, faed statistics, dbbi parse, photo | untouched |
| doc 114/115 crosses as a complete block | stand |
| per-label "spent" verdicts on L and M readings | **invalid as stated**: each is dead only with the partners it was tested against |
| the constraint table's slot-by-slot kill matrix | **invalid**; redo as pairs |
| "the operands lie outside the page" (dossier 9) | not shown by the nulls; it rests on faed being filler |

Going forward: keep a pair ledger, not per-label kill lists, and prefer one idea that explains both labels at once (the way one song explained the URL, the rebus and the phase-1 password).

## 12. Files

| folder | contents |
|---|---|
| `critical-review-2026-10-03.md` | the methodology critique |
| `riddle-method/` | `rt.py`, `retro.py`, generators, `riddles*.txt`, the R1 to R35 ledger |
| `independent-model/` | model, divergences, `ct.py`, candidate files, logs |
| `microstep/` | #6509 and #32579 timelines, `ms.py`, ledger, logs |
| `constraints/` | constraint table, R31 candidates, logs |
| `rabbit-holes/` | per-container verdict, `leak.py`, `structural.py`, logs |
| `selection/` | atoms and generator for the approved, unrun 23/16/7 enumeration |
| `source-pointer/`, `genesis-main-cpp/` | R34, R35, both `main.cpp` versions |
| `photo-analysis/` | `photo_checks.py`, run log |
| `common-flaw/` | the pair-ledger argument, `gen.py`, `cross.txt`, logs |
| `doc116-runs/` | doc 116 run logs: flags and stderr per pool and part, `rungaps.sh`, controls and win-test logs |
| `status.md` | one-page status |

Correctness audit (5 October 2026): historical counts/logs above are unchanged. Block (a) tested 456 strings, omitting 144 L+M+thispassword assemblies; the corrected 600-string set has not been searched. Historical detectors could suppress unranked padding-1/2 binary outputs, so zero flags do not exclude all valid plaintexts. See doc 118 for the full hypothesis tuple and verification limits.
