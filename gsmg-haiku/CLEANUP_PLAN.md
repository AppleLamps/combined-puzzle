# Cleanup plan: redundant scripts

Status: **applied** on branch `cleanup/redundant-scripts` (2 files removed, 1 reference updated).

Scope: all 108 tracked `.py`/`.ipynb` scripts in `work/`, `mywork/`, `mywork2/` and `review_leads/`. There are no scripts at the repo root. `review_leads/vendor/qrcodegen.py` is a vendored library and was not considered. The following were left alone: `files/`, `derived/`, `ChatExport_*`, data and result files, and the untracked `review_leads/poster_dbbi_audit_2026-10-09/`.

## Method

1. **Purpose inventory** of every script (Appendix A). It was built by reading each file in full and running DigUp `search_code` with plain-language purpose queries:
   - sha256 of candidate phrases as AES password on the Salted__ containers
   - raw bytes as AES key/IV
   - a/b binary decode
   - matrix row/column sums
   - poster spiral walk
   - straddling checkerboard
   - private key to target hash160
   - zero insertion/replacement decode
   - substitution hill-climb
   - Architect transcript measurement

   I read the hits to confirm them.
2. **Embedding similarity.** I opened `C:\Users\lucas\.claude\digup-index\gsmg-puzzle-clean-441d54a4\code.sqlite` read-only (`mode=ro`), averaged the segment vectors per file, and listed pairs with cosine >= 0.93. There were 65 pairs (Appendix B). These were used only as leads. Most high-scoring pairs turned out to test different candidates.
3. **Same-purpose check.** For every candidate group I diffed the candidate lists, containers, modes and outputs. I only call a script redundant when the keeper covers everything it does, or when every difference is recorded below.
4. **Reference check.** I ran `git grep --untracked` for each script's file name and import name across `tests/`, every `*.md`, the reports and the other scripts.

Result: **2 scripts are redundant.** Most similar-looking scripts each test at least one candidate, mode or container that no other script tests, so they stay.

---

## Group 1: poster spiral walk (`mywork/`)

- **Keeper:** `mywork/inspect_poster_grid.py`
- **Remove:** `mywork/test_spiral.py`

**What both do.** Both take the same hard-coded 14x14 poster grid:
- `test_spiral.py:1-14`
- `inspect_poster_grid.py:1-16`

The rows are identical. Both walk the same spiral: start at (0,0), directions down, right, up, left, and turn when blocked. The code is `test_spiral.py:16-32` and `inspect_poster_grid.py:51-66`. Both report where the F, Y and B cells fall along that path.

**What the removed script did differently.**
- It printed the indices grouped by cell type (`test_spiral.py:34-45`).
- The keeper prints one line per special cell, with its index, coordinates and value (`inspect_poster_grid.py:68-72`).
- The keeper also prints the B/Y/F coordinates (`inspect_poster_grid.py:20-29`).

I ran both scripts and parsed their output. The per-type index lists are identical: F=1, Y=9, B=15 cells. So the keeper's output contains all of `test_spiral.py`'s output.

**References.** There is one reference, at `mywork/report.md:7`: "(Checked via `test_spiral.py`)". I will update it to "(Checked via `inspect_poster_grid.py`)". Nothing imports either script.

---

## Group 2: second base64 block as a raw AES key/IV (`work/`)

- **Keepers:** `work/test_raw_key_iv.py` for the raw key/IV stage, and `work/test_raw_keyiv2.py` for the password stage.
- **Remove:** `work/test_raw_keyiv.py`

**Raw key/IV stage.**
- `test_raw_keyiv.py:81-84` takes `textarea[999:1063]`, decodes it, and sets key = bytes 0-31 and IV = bytes 32-47. It then decrypts `[16:]` of terminal, salphaseion-short and cosmic-duality with AES-256-CBC (`:94-118`).
- `test_raw_key_iv.py` runs that exact case (`:51-52`, `:93`). It hardcodes the same block at `:31`; I checked that `textarea[999:1063]` equals that string. It also tries key 16-47 with IV 0-15 (`:59-60`, `:104`) and 9 AES-128 key/IV combinations (`:110-123`), on the same three containers (`:24-28`).
- `test_raw_keyiv2.py:83-105` repeats the same single case.

I ran both scripts. `test_raw_keyiv.py` reports padding failure on all three containers. `test_raw_key_iv.py` reports no success for any of its 11 combinations.

**Password stage.**
- `test_raw_keyiv.py:323` calls `decrypt_with_password`, which is never defined. When run, the first candidate raises `NameError: name 'decrypt_with_password' is not defined` at line 323, called from line 365. **No password candidate was ever tested by this script.**
- Its intended list is at `:332-361`. `test_raw_keyiv2.py:118-154` contains every entry except one, and `test_raw_keyiv2.py` also tests all three containers, not only salphaseion-short.

**What the removed script did differently, recorded here so nothing is lost:**
- **Intended but never-executed candidate `'enter' + 'matrixsumlist'`** (`test_raw_keyiv.py:341`). No other script in the repo tests this string; the only grep hit is that line. It is recorded here as **untested**. It is not disproven.
- `candidates_from_sum` (`:272-290`) holds the str/hex forms of the 149-digit sum (504) and the 570-run digit sum (3079). The list is built but never tested.
  - `test_instruction_patterns.py:133-140` prints both sums.
  - `test_instruction_patterns.py:197` tests `str(504)` as a password.
  - The hex forms and `str(3079)` are untested anywhere. They were never tested here either.
- `candidates_from_words` (`:298-305`) and `decode_ai_run_as_digits` / `decode_ai_run_paired_hex` (`:163-188`) are defined but never used.
- The printed digit sums (504 and 3079) are also printed by `test_instruction_patterns.py:134,140`.
- The long block of speculative prose (`:204-250`) is not a test.

**References.** None: no `.md`, test or script names `test_raw_keyiv.py`. `test_raw_keyiv2.py` and `test_raw_key_iv.py` do not import it.

---

## Groups examined and kept

Each of these groups has the same broad purpose, but every member tests something the others do not.

| Group | Why it stays (key differences, file:line) |
|---|---|
| `mywork2/zero_mixed.py`, `zero_mixed_ins.py`, `zero_longctl.py` (cosine 0.98-0.99) | Lines 1-70 are identical, but the drivers differ. **zero_mixed** is the only one that runs replace-gie on r1/r1rev/r2/r2rev (`zero_mixed.py:76`). **zero_mixed_ins** runs insert at beam 20000, where zero_mixed uses 3000 (`zero_mixed_ins.py:72-78`). **zero_longctl** is the only one with the 568-digit control (`zero_longctl.py:71-74`). `mywork2/dbg.py:1-4` execs zero_mixed's source text. All are referenced in `mywork/LOG.md`. |
| `mywork2/zero_insert.py` vs `zero_mixed_ins.py` | zero_insert uses an a-z-only output alphabet, a binomial zero prior (`:14-15`), a different model, and both z-section controls. Beam search is not monotone, so the larger space in zero_mixed_ins does not guarantee coverage. |
| `mywork2/zero_enc.py`, `zero_codes.py`, `zero_tail.py`, `zero_bases.py` | They test different number encodings: LE/EBCDIC/7-bit, per-character codes, exhaustive DFS without a model, and base conversion with all 8 g/i/e subsets plus the r1+r2 stream. |
| `work/test_raw_keyiv2.py` vs `work/test_raw_key_iv.py` (0.968) | Disjoint password lists. keyiv2 has the +LF variants, `[0:447]` text, HALF/BETTERHALF, 149 digits and checkerboard plaintext. key_iv has 24 permutations, upper-case words, causality and the 10 "one for one" variants. |
| `mywork/test_lead1.py`, `test_lead1_ops.py`, `test_matrixsum.py` (0.94-0.97) | 8 of test_lead1's 20 candidates are in test_lead1_ops. **12 are unique**: idx1-idx4 with fallbacks (`test_lead1.py:57-80`). test_lead1_ops adds idx_0based, word_lens, sum_lens and xor. test_matrixsum adds sum_1/3/4. |
| `mywork/run_targeted_tests.py` vs `test_specific_targets.py` (0.964) | 201 vs 99 candidates, 38 shared. run_targeted adds **raw mode** (`:96-99`) and the +matrixsumlist variants. test_specific has 61 strings in neither run_targeted nor test_transcript, e.g. the cumulative L24 prefixes. |
| `work/systematic_explore.py`, `deep_analysis.py`, `analyze_salphaseion.py`, `complete_salphaseion_decode.py` | Different decodes and different candidate lists. See "Observations" for the two that crash. |
| `work/test_candidates_robust.py`, `try_passwords.py`, `try_chess_and_3a.py` | try_passwords adds `justonesecond` and `ciaobella`, a plaintext classifier, and `btc_check` private-key checks. robust stops at the first container that passes padding (`:295`). try_chess_and_3a is almost disjoint from both. |
| `work/analyze_enter_instruction.py` vs `analyze_instructions.py` (0.958) | Only analyze_enter_instruction verifies the correct join `[895:959]+[999:1063]`. Only analyze_instructions actually decodes the a/b run to `enter`. |
| `work/verify_false_positive.py` vs `reproduce_decrypts.py` | One retests `[0:447]` variants on the unopened containers. The other reproduces the Phase 2, 3 and 3.2 decrypts. |
| `review_leads/hash_scope.py` vs `hash_scope_followup.py` (0.957) | The follow-up adds decrypt-then-hash and command-output byte layouts. Both are cited in `HASH_SCOPE_REPORT.md`. |
| `review_leads/next_tests.py` vs `run_new_leads.py` (0.938) | Different candidate sources. Both are imported by other modules, and next_tests by `tests/test_review_regressions.py:146`. |
| `mywork2/subsolve.py` vs `cb_solve.py` (0.949) | Different streams: r1 with selector `be` vs r2 and r1+r2 with all 129 selectors. Different models, nulls and cribs. |
| `mywork2/stats.py` vs `mywork/explore1.py` (0.948) | Different statistics: base-9 conversions vs decimal-to-hex conversion. |
| `mywork/align_arch.py` vs `align_architect.py` (0.943) | Prefix positions vs whole-line/LCS matching. Each reports results the other does not. |

---

## Not sure: not removing these

1. **`mywork/check_lines.py`.** Its output, three container lengths plus transcript lines 11, 14 and 24, is fully reproduced by `compare_containers.py:8,14,20` plus `print_transcript.py`. But no single script covers it, and it is a filtered "find the choice lines" view.
2. **`mywork/breakdown_arch.py`.** The six slices it prints concatenate to the full Architect text, which `check_arch.py:10` also prints. Its section labels, e.g. "matches Line 4" and "PUZZLE AUTHOR CUSTOM TEXT" (`:7-22`), are an interpretation that no other script records.
3. **`mywork/measure_speeches.py` vs `measure_dialogue_only.py`** (0.937). Same loop, but speeches measures the line with the "Speaker:" prefix and dialogue_only measures without it. The numbers differ.
4. **The `zero_mixed*` drivers.** These could be folded into one script with CLI flags, but that is a refactor, not a removal, and `dbg.py` depends on zero_mixed's text.
5. **`next_tests.py` digit-map mode.** It was never run, and `mapping_boards.py` digit-map mode is a strict superset (same 5040 maps, no printable filter). This is a mode inside a script that tests import, so there is nothing to remove.

---

## Observations (out of scope, no action proposed)

These are not redundancies. They came out of the inventory and may matter for interpreting old results. **Verified** means I checked it myself. The rest was found by reading the code and was not run.

- **Verified:** `work/systematic_explore.py:34` imports `decrypt_container`, which `work/openssl_decrypt.py` does not define (it only has `derive_key_and_iv`, `decrypt_openssl_aes256cbc` and `decrypt_b64_file`).
- **Verified:** `work/decode_large_ai_runs.py` reads `files/salphaseion-page.txt` and `derived/salphaseion-digits.txt`. Neither file exists.
- **Verified:** `derived/phase3.2-plaintext.bin` is 2411 bytes with LF line endings. Several `work/` scripts slice it at the CRLF offsets in STEPS.md (`[0:447]`, `[1990:2139]`, `[2143:2292]`), so their "last words before archi" candidates carry trailing Architect bytes.
- **Not verified:**
  - `analyze_salphaseion.py:145` will crash on the first bad padding, because `decrypt_openssl_aes256cbc` raises.
  - `analyze_matrixsumlist.py:240` tests no candidates on the LF file.
  - `reproduce_decrypts.py:150` will report a Phase 3.2 mismatch.
  - Five scripts parse `[127:447]` as a chess board, but those bytes are English prose.

---

## Phase 3 steps (after approval)

1. Run `python -m unittest discover -s tests -v` (the command in `review_leads/REVIEW_CORRECTIONS.md:94`) and record the result.
2. `git switch -c cleanup/redundant-scripts`
3. `git rm mywork/test_spiral.py work/test_raw_keyiv.py`
4. Edit `mywork/report.md:7`: change `test_spiral.py` to `inspect_poster_grid.py`.
5. Re-run the same test command.
6. Commit with a message listing both groups. Do not push.

Files removed: **2**. References updated: **1**.

---

## Appendix A: purpose inventory

Abbreviations:
- **STD** = password `sha256(answer).hexdigest()`, EVP_BytesToKey SHA-256 with 1 iteration, AES-256-CBC.
- **3C** = terminal, salphaseion-short and cosmic-duality containers.
- **r1** = `textarea[0:91]`; **r2** = `textarea[195:765]`.

### work/
| Script | Input, operation, output |
|---|---|
| analyze_149_digits.py | 149 digits and textarea runs: repeat search, a-i,o decodes, 18Cchrj decode tries. Prints only. |
| analyze_embedded_container.py | STD on an assumed embedded container plus 3C. About 70 candidates: instruction words, checkerboard words, 24 permutations. |
| analyze_enter_instruction.py | Verifies that the base64 halves around the `enter` run join to salphaseion-short. No crypto. |
| analyze_half_betterhalf.py | STD on 3C with 149-digit splits at 78/98 (actual "149" positions are 80/100), HALF/BETTERHALF and lastwords combinations. |
| analyze_instructions.py | Regex-locates and decodes the a/b instruction runs, prints the STEPS section. No crypto. |
| analyze_matrixsumlist.py | STD on 3C with 149-digit prefix/suffix/sum candidates (gated by an isdigit check). Also "3a/3b" decode. |
| analyze_salphaseion.py | Run decodes, then STD on 3C with about 60 candidates (instruction words, architect words, fubcd family, generic passwords). |
| btc_check.py | Private-key integer to compressed/uncompressed hash160 vs target. Library and CLI, imported by try_passwords. |
| complete_salphaseion_decode.py | Walks every textarea part in order and decodes each. No crypto. |
| debug_ab_decode.py | 7 a/b bit conventions on `[91:195]` vs `matrixsumlist`. |
| decode_570char_run.py | 570 run as bigint/hex and decimal pairs, base64 block dissection. No crypto. |
| decode_before_archi.py | Prints `[0:447]`, digit repeats of length 6-29, STEPS grep. No crypto. |
| decode_chess_properly.py | Prints `[0:127]`, `[127:447]` as 64 piece+int32 squares, architect slice. No crypto. |
| decode_large_ai_runs.py | a/b and a-o runs from page files, checkerboard-hex candidates, STD on 3C. |
| deep_analysis.py | Run-type map, a-i bigints, checkerboard encoder/decoder, keyword search. No crypto. |
| find_missing_words.py | Finds instruction words and base64-like blocks, salt comparison. No crypto. |
| lastwords_before_archi.py | STD on 3C with `[0:447]` variants, quote phrases, fubcd family, digit sum. |
| openssl_decrypt.py | EVP/AES library and CLI. Imported by 5 work/ and 5 mywork/ scripts. |
| reproduce_decrypts.py | Reproduces the Phase 2, 3 and 3.2 decrypts and prints their structure. |
| systematic_explore.py | Digit sums, checkerboard verify, "chess" sums, then STD on 3C (chess sums, mlte, interleave, architect words). |
| test_candidates_robust.py | STD sweep on 3C, about 75 candidates, stops at the first container that passes. Writes FOUND_* on a hit. |
| test_instruction_patterns.py | STD on 3C: instructions with LF, 24 permutations x 3 joins, `[0:447]` variants, digit forms. |
| test_raw_key_iv.py | Raw key/IV of the second block, 11 combinations on 3C, then STD with about 50 candidates (permutations, "one for one"). |
| test_raw_keyiv.py | **Remove.** Raw key 0-31 / IV 32-47 on 3C, then crashes before any password. |
| test_raw_keyiv2.py | Raw key 0-31 / IV 32-47 on 3C, STD with 17 instruction/text candidates, join check. |
| try_chess_and_3a.py | STD on 3C: chess sums, 3a hex/sum, jacq/250f, 24 permutations, interleave, 149 splits at 70-79. |
| try_passwords.py | STD on 3C with 19 candidates plus a plaintext classifier. 149-digit slices as private keys. |
| verify_container_join.py | Base64 run joins with padding variants. No crypto. |
| verify_false_positive.py | STD on 3C with `[0:447]`, 3a and 3b variants. Phase 3.2 length check. |
| verify_sp_short.py | STD on salphaseion-short with 15 byte variants of `[0:447]`. |

### mywork/
| Script | Input, operation, output |
|---|---|
| align_arch.py | Finds each transcript line's 30-letter prefix in the architect text and prints positions. |
| align_architect.py | Whole-line or longest-common-substring match of transcript lines in the architect text. |
| analyze_poster_bits.py | 24 B/Y cells (hardcoded spiral order) to bits, ASCII and hex. |
| breakdown_arch.py | Prints 6 labelled slices of the architect text. (Not sure, kept.) |
| candidate_pool.py | Builds the 40k password pool and 9 transforms. Imported by pool_search, binary_envelopes and tests. |
| check_14.py | Lengths of the checkerboard, architect and runs, and divisibility by 14/7. |
| check_arch.py | Architect length, keyword offsets, full text. |
| check_l24.py | L24 prefix up to "the problem is" and its lengths. |
| check_lines.py | Container lengths and the transcript lines with "choice"/"truth"/"quintessential". (Not sure, kept.) |
| check_quirks.py | Which quirk words occur in the transcript and architect text. |
| compare_containers.py | 3C lengths, salts and ciphertext hex. |
| do_it.py | 583 candidates from 4 hypotheses: matrix sums, permutations, 14-wide reads, clauses. sha/raw on 3C plus key checks. |
| explore1.py | r1 and r2 as decimal to hex to bytes, digit counts. |
| extract_quotes.py | Strips an external wikiquote HTML into `wikiquote_reloaded.txt`. |
| inspect_32_head.py | Prints phase3.2 bytes 0-446. |
| inspect_html.py | HTML comments, scripts and hidden inputs in `files/*.html`. |
| inspect_poster_grid.py | **Keeper, Group 1.** Poster B/Y/F coordinates and their spiral indices. |
| inspect_rabbit.py | Rabbit PNG format and colour histogram. |
| inspect_sentences.py | Per-sentence lengths of each transcript line. |
| inspect_sp.py | Textarea segment boundaries, prints p5/p7/p9/p10/p12/p13. |
| lead1_sum.py | 12 mod-26 combos of digit runs with texts, scored on English n-grams, plus IC and periodicity. No crypto. |
| lib.py | EVP/AES helpers and secp256k1 hash160 check. Imported by 20 scripts. |
| map_cb_digits.py | Decodes the 149 digits with the fixed board, letter-by-letter. |
| matrix_exp.py | Row/column sums of r1/r2 for every divisor shape, printed. |
| measure_dialogue_only.py | Raw/alpha length of each line's dialogue without the speaker prefix. |
| measure_speeches.py | Raw/alpha length of each whole line, with the prefix. (Not sure, kept.) |
| parse_png.py | PNG chunk list, IHDR and tEXt. |
| pool_search.py | Pool x 9 transforms on 3C plus control. Imported by tests. |
| print_transcript.py | Prints every transcript line numbered. |
| probe_script.py | Keyword windows from an external antigravity file. |
| read_last_turns.py | Prints turns from an external antigravity transcript. |
| run_targeted_tests.py | 201 L24/L26/L10 clause candidates, sha and raw, on 3C. |
| test_checkerboard.py | r1 parsed with 2/5 selectors and a hypothetical alphabet (3 distinct decodes), STD. |
| test_decode.py | Decimal-hex decode of the two z-section controls. |
| test_elementwise.py | Prints checkerboard +/- r1 three ways. |
| test_lead1.py | 20 candidates from r1 indexing into Line 20 words and checkerboard shifts, STD. |
| test_lead1_ops.py | 24 candidates: indexing, word lengths, sums, shifts, xor. STD. |
| test_matrix_sums.py | Prints r1 and checkerboard-ASCII 7x13/13x7 sums. |
| test_matrixsum.py | 48 element-wise sum candidates, STD. |
| test_specific_targets.py | 99 L24/L26/L10 sub-clause candidates, sha only, on 3C. |
| test_spiral.py | **Remove.** Spiral indices of the F/Y/B poster cells. |
| test_term_cb.py | 21 checkerboard/clue phrases, sha/raw, terminal only. |
| test_transcript.py | 128,667 transcript-derived candidates x 3 modes on 3C plus control. |
| test_transposition.py | 5 keyed columnar transpositions of the checkerboard, STD. |
| verify.py | Hash160 sanity check, README pubkey vs targets, 3 control decrypts. |
| verify_91.py | Prints checkerboard and r1 (both 91 long). |
| view_chunk.py | Prints phase3.2 bytes 2100-2299. |

### mywork2/
| Script | Input, operation, output |
|---|---|
| block765.py | Masked row/column sums of digit blocks, 4 decodings, scored by dictionary. |
| cb_solve.py | r2 and r1+r2 checkerboard parses (129 selectors), quadgram substitution annealing. |
| dbg.py | Debugs the zero_mixed insert-control failure (execs zero_mixed text). |
| pool2.py | Architect/checkerboard substrings and transcript n-grams x 4 transforms x 4 KDF digests on 3C. |
| r1_ic.py | IC of r1 checkerboard parses vs shuffles. |
| stats.py | r1/r2 counts, digrams, base-9 conversions. |
| subsolve.py | Anneals the 63-symbol r1 `be` parse as substitution, with nulls and cribs. Writes subsolve_*.out. |
| try_sub.py | subsolve plaintexts as passwords, 3 transforms x md5/sha256, on 3C. |
| zero_bases.py | Whole-number base conversion with g/i/e set to 0, dictionary scoring. |
| zero_codes.py | Per-character decimal codes with zero insert/replace, 4 tables. |
| zero_enc.py | zero_mixed engine under LE/EBCDIC/7-bit encodings. |
| zero_insert.py | Zero re-insertion beam search, a-z output, binomial prior. |
| zero_longctl.py | 568-digit control for the zero_mixed engine. |
| zero_mixed.py | Zero replace and insert beam search, printable output, mixed-case 4-gram model. |
| zero_mixed_ins.py | Same engine, insert only, beam 20000. |
| zero_tail.py | Exhaustive DFS with zeros hidden as g/i/e, no model. |
| web/salphaseion.ipynb | Notebook decoding the a/b runs and z-sections. |

### review_leads/
| Script | Input, operation, output |
|---|---|
| binary_envelopes.py | Old pool re-tested on terminal and short with structural detectors and 4 padding modes. |
| binary_hd.py | 64-byte materials as BIP32 seeds and key/chain pairs, 295 paths vs target. |
| double_cbc.py | Two-layer CBC with inner salt variants, 816 passwords. |
| genesis_slices.py | Genesis-block slices as scalars, passwords and key+IV windows. |
| hash_scope.py | Which parts get hashed: 5 families as passwords and scalars on 3C. |
| hash_scope_followup.py | Decrypt-then-hash and sha256sum/openssl output layouts. |
| inspect_transpose.py | Offline structure and scalar checks of next_tests transposition outputs. |
| ltc_scan2/ltc_scan2.py | Brainwallet phrases as BTC/LTC addresses via network lookups (partial run). |
| mapping_boards.py | Exhaustive digit maps and checkerboard boards on r1/r2 as passwords. |
| next_tests.py | Transposition, partitions and digit-map modes. Imported by tests. |
| qr_residual.py | Re-encodes the QR to check for residual modules. |
| rank_mapping_text.py | Ranks mapping_boards text by the subsolve language model. |
| run_new_leads.py | Poster prime weights and numeric-key combinations of r1/r2 as passwords. |
| vanity_offset.py | Baby-step giant-step search for small offsets from seed keys. |

## Appendix B: file pairs with cosine >= 0.93 (65)

Top pairs and their verdicts. Every other pair is between scripts listed under "kept" or between scripts with plainly different candidates (see Appendix A).

| Cosine | Pair | Verdict |
|---|---|---|
| 0.994 | zero_mixed_ins / zero_mixed | kept (different driver runs) |
| 0.982 | zero_longctl / zero_mixed | kept (unique control) |
| 0.975 | zero_mixed_ins / zero_insert | kept |
| 0.975 | test_raw_keyiv2 / test_raw_keyiv | **test_raw_keyiv removed** (Group 2) |
| 0.970 | test_raw_keyiv / test_raw_key_iv | **test_raw_keyiv removed** (Group 2) |
| 0.969 | test_lead1_ops / test_lead1 | kept (12 unique candidates) |
| 0.968 | test_raw_keyiv2 / test_raw_key_iv | kept (disjoint lists) |
| 0.964 | run_targeted_tests / test_specific_targets | kept |
| 0.959 | systematic_explore / deep_analysis | kept |
| 0.958 | analyze_enter_instruction / analyze_instructions | kept |
| 0.957 | hash_scope_followup / hash_scope | kept |

`test_spiral.py` / `inspect_poster_grid.py` did not reach 0.93, because the keeper also has dead code and coordinate printing. The pair was found by the DigUp purpose query "walk the poster grid in a spiral".
