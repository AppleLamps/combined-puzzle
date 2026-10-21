# Status as of 2026-10-15 UTC

**The puzzle is unsolved.** The private key of `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` is unknown. Three encrypted containers remain unopened. No experiment in this repo has produced a structured decrypt or a key that matches the target.

How to read this file:
- The earlier status audit was checked on 2026-10-14. The cryptanalysis update below was reproduced on 2026-10-15 UTC; older claims retain their original scope.
- **[local]** means it was checked against a saved local file or recomputed here.
- **[not checked]** means it depends on a live chain query, the source kit, or output that is not in the repo.
- Chat times are UTC, taken from `date_unixtime` in `ChatExport_2026-10-08/result.json`. That export's `date` field is local time (UTC-4) and runs to 2026-10-09 00:30 UTC.

## Latest result: coordinate structure reproduced, next operation unresolved

See [the full investigation](review_leads/cryptanalysis_2026_10_15/README.md) and its source/experiment receipts. The known phase-3.2 decrypt and the live SalPhaseIon fields were checked independently. The following results are conditional on the stated decoding models, not proof that the author intended every inferred step:

- The 91-character DBBI prime grammar has both 83- and 84-cell parses. The 84-cell branch gives 23 prime tokens split 16/7 and, under the signed 7×12 column-sum construction, `HILLFEXMGSGQ`. Poster correspondence still needs an additional selection rule to choose that branch uniquely.
- Full-period Bifid with square `dbifhcegaklmnopqrstuvwxyz` reproduces `BTCSEED`; the proposed mod-25 Hill stage gives `IFINDO` followed by unexplained output. Both alternating streams are retained. The four-symbol companion alphabet follows mechanically from the nine-symbol source alphabet.
- Exactly 58 row bits are forced zeros. Removing them leaves 512 bits **including eight header bits**; the post-header row payload is 504 bits. Both representations reconstruct the original source when the column stream and header are retained.
- The unchanged carrier cannot be an output of any of the four singular mod-26 Hill matrices satisfying the proposed FEXM→GSGQ example. A linear 3×3 natural25 A=0 Hill decoder also cannot extend the prefix to IFINDOUBT, by a mod-5 invariant. Affine/field alternatives were tested separately and produced no coherent complete continuation.
- The documented 64/63-byte key and HD-seed tests made 37,952 exact public-point comparisons and 1,536 OpenSSL-format container attempts, with no prize match or coherent decrypt. Official BIP32 controls passed. Paths, transforms and padding-only outputs are retained; arbitrary paths or derivations are not excluded.

**Unsolved interface:** the operation on the 282-letter post-header carrier and 281 remaining companion symbols. No rule yet fixes its key, ordering, representation, or combination into a complete instruction or verified object. The literal decoded labels are not established passwords.

## 1. Stages

| Stage | State | Where |
|---|---|---|
| Poster, Phase 1, Phase 2, Phase 3, Phase 3.2 | solved | `STEPS.md` steps 0-4 |
| SalPhaseIon page, both textareas | decoded as far as the a/b and a-i,o runs go (`matrixsumlist`, `lastwordsbeforearchichoice`, `thispassword`, `enter`) | `STEPS.md` step 5 |
| SalPhaseIon a-i runs r1 (`[0:91]`) and r2 (`[195:765]`) | partial prime/coordinate constructions reproduced; no complete instruction | `STEPS.md` step 5a and the latest investigation |
| Terminal container | **not decrypted** | `files/terminal.b64` |
| SalPhaseIon short container | **not decrypted** | `files/salphaseion-short.b64` |
| Cosmic Duality container | **not decrypted** | `files/cosmic-duality.b64` |

The three open containers [local]:
- **Terminal** and **SalPhaseIon short:** `Salted__` + salt + 80 ciphertext bytes each. Under AES-CBC/PKCS#7 the plaintext is 64-79 bytes. A 64-character hex private key fits. A raw 32-byte key or a 51/52-character WIF alone does not fit (`review_leads/REVIEW.md:151`).
- **Cosmic Duality:** 1,328 ciphertext bytes, so the plaintext is 1,312-1,327 bytes.

The working convention, used by every solved stage:
- password = `sha256(answer)` as lowercase hex
- key derivation: OpenSSL `EVP_BytesToKey`, SHA-256, 1 iteration
- cipher: AES-256-CBC

## 2. Target

- **Address and public key** [local]: hash160 `a9553269572a317e39f0f518cb87c1a0ee1dbae4`, P2PKH of the **uncompressed** public key. The base58 check passes.
- **Public key exposure** [local]: the full public key is on-chain, visible in the input scripts of the 2024 spend `88cdb3cd`. That transaction is saved inside chat message #24824. No one has assessed whether an attack using the exposed key is feasible (`review_leads/TELEGRAM_REVIEW_2026-10.md:41`).
- **Balance:** 1.25636967 BTC on 2026-09-29 (`README.md:25`) [not checked]. The creator said on 2026-07-13 UTC that the BTC is still available (#66595, edited 2026-07-26) [local].

## 3. Creator hints

Sources: the Telegram export, `mywork2/web/hints/*.png`, and `mywork2/web/naddiseo_readme.md`. All entries are from the creator account "Jrk Bgrt". Most were edited after posting, so the wording may be later than the date.

| UTC date | Msg | Wording (exact) | Note |
|---|---|---|---|
| 2020-01-14 | #1710 | "Roses are White but often Red. Yellow has a number and so does Blue. Go back to the first puzzle piece without further ado. It might have shown you only one door, beware that the rabbits nest may contain a whole lot more. Hush hush." | edited 2024-04-24 |
| 2021-03-01 | #5966 | "You are at the prime part already???" then "Oh wait, shouldn't have said that. That might have been a hint" | reply to a solver |
| 2021-12-03 | #7914 | "There is / Another / D / O / O / R" | 2021-12-02 in local time |
| 2021-12-26 | #8000 | "...prime numbers ... definitely an aspect which is required to proceed. Furthermore, along the way, some characters need to be 'zeroed out'.." | the image file is named 12-25; edited 2026-02-15 |
| 2023-01-09 | #8330 | "At least prime number is very important to get any further." | |
| 2023-01-12 | #8354 | "Focussing on the theory of everything is also still a valid path to reaching the private key." | |
| 2023-02-23 | #8446 | 1,288 bits. Reversing the whole bit stream and reading it as ASCII gives `yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyangwewontgiveawaythepassworditsinfrontofyoureyesbutyourenotseeingitverylaststepisatruegiveawaypromised` | decoded here from the export [local]; the original has no spaces |
| 2023-08-06 | #9599 | "Probably the last hint: Once you hit a \"ying yang\", you'll be able to solve it the same day." | spelled "ying" |
| 2024-04-10 18:21 | #24071 | "1357 blocks to go" | Block 838,643 = 840,000 - 1,357 was mined at 18:08:53 UTC that day (`review_leads/REVIEW.md:157`), 13 minutes earlier. This points strongly to a halving countdown. |
| 2026-01-01 03:20 | #53342 | binary: "Happy new year! Make the best of everything. Oh, and here's a \"tiny hint\" <3." | 2025-12-31 in local time |
| 2026-07-13 00:47 | #66568 | "I have a hidden laptop which I haven't touched in years. On that thing... is the actual answer...." | edited |
| 2026-07-13 00:51 | #66573/4 | "My close friends have the best chance of solving it (a few tried). But they don't have the skills some of you do." / "NOTE: that is a hint." | NOTE edited 2026-08-23 |
| 2026-07-13 01:10 | #66593 | "The \"5\" btc was never the actual prize. That was only a tiny fraction." | |
| 2026-07-16 22:19 | #66903 | "Well, it's hidden in a room with a hidden door." | reply to a joke |
| 2026-07-16 22:25 | #66909 | BIP 360 "piggy bank" explanation | also #66555 and #66590 |

The last direct creator message in the export is #70377 ("Same same", 2026-09-01 15:41 UTC). The last forward attributed to the creator is #73195 on 2026-09-23, a copy of #66593.

The 2023-02-23 decoded hint presents these labels in order; their separation into operations remains an interpretation:
1. yellow/blue
2. primes
3. matrix sum list
4. last words before the Architect's choice
5. yin-yang

Labels 3 and 4 match the decoded SalPhaseIon fields. The latest investigation supplies reproducible prime-position and signed-sum constructions, with explicit assumptions; their intended downstream role and the yin-yang operation remain unresolved.

## 4. What has been tried (bounded negatives)

"No hit" means no decrypt that was both padding-valid and structured, and no scalar matching the target. **Each result covers only its own candidate set and transforms.** The counts were checked against the saved result files [local] unless the table says otherwise.

| Experiment | Scope | Result | Source |
|---|---|---|---|
| Pool sweep | 40,114 strings (n-grams of page text, decodes, known answers) x 9 password transforms x 3 containers, with Phase 3.2 as a control (recovered) | no hit | `mywork/LOG.md:7-11`, `mywork/pool_out.txt` |
| Binary envelopes | same pool, 361,002 passwords, 722,004 trials, terminal + short containers, structural detectors | no structure | `review_leads/BINARY_FOLLOWUP_REPORT.md` |
| HD wallet | 834 materials, 572,164 derivations over 295 paths | no match | same |
| Double CBC | 816 passwords, 3,995,136 pair trials | no hit | same |
| Hash scope (8 families: partitions, subsets, selective hashing, decrypt-then-hash, command outputs, ...) | 707,730 AES trials, 450,344 scalars | no hit | `review_leads/HASH_SCOPE_REPORT.md` |
| Columnar transposition before checkerboard | 32 cases, 414 trials, 478 scalar checks | no hit | `review_leads/TRANSPOSE_REPORT.md` |
| Alternative digit maps and 10-column boards | 1,642,254 trials, 1,040,383 scalar checks, 4-gram language ranking | no hit, no grammatical text | `review_leads/MAPPING_BOARDS_REPORT.md` |
| Prime-weighted poster sums | 4,308 answers, 12,924 trials | no hit | `review_leads/REVIEW.md` test 5 |
| r1 as a keystream for r2 | 17,352 answers, 52,056 trials | no hit | `review_leads/REVIEW.md` test 6 |
| Vanity offset | target = +/-seed + delta, delta in [-2^31, 2^31), 10 seeds | no match | `review_leads/vanity-offset-32.json` |
| QR residual | 16 QR candidates | v4-L, mask 2, ECI 26 matches all 1,089 modules, so no hidden module changes | `review_leads/qr-results.json` |
| Genesis-block slices | 407,712 trials, 293,580 scalar checks | no hit | `review_leads/GENESIS_SLICES_REPORT.md` |
| Brainwallets | 499 phrases x (sha256, double sha256) x (compressed, uncompressed) | 0 hits (recomputed here) | `review_leads/BRAINWALLET_CANDIDATES.md` |
| LTC/BTC brainwallet scan | **partial: 257 of 2,176 addresses** looked up, covering 66 of 544 phrases | no match among those checked | `review_leads/LTC_SCAN_2026-10-08.md` |
| Zeros hidden as g/i/e, deleted zeros, other encodings | beam/DFS decoders with language models; controls recovered | no complete decode of r1 or r2. Three DFS runs hit the 300,000-node cap and were truncated, not exhausted | `mywork/LOG.md`, `mywork2/zero_*.out` |
| Checkerboard substitution solve of r1 (b/e selectors) | annealing, 150 restarts, cribs | best scores fall inside the shuffled-null range, no crib fits | `mywork/LOG.md` 12b-13, `mywork2/subsolve_*.out` |
| Prime/position zeroing masks on r1 and r2 (rerun of LOG entry 5, with Y=9/B=15 classes) | 113 position classes x 511 letter subsets x zero/remove, 6 run orders, 487,725 masked strings, 3 decoders; planted controls recovered at rank 1 | best scores equal the shuffled null; 0 hits on 1,412 container answers | `mywork/LOG.md` 16, `mywork2/prime_zero.out` |
| Poster/DBBI structural audit, independently rerun | All 300 selections of 23 out of 25 events, with off-white identified as blue | Five exact parses: three of length 83, two of length 84; branch-selection assumptions retained | `review_leads/cryptanalysis_2026_10_15/poster_check.py` and `.json` |
| Coordinate/Hill and row-bit investigation | Exact algebraic exclusions, forward-controlled cipher tests, 64/63-byte derivations, 295 documented HD paths | No complete instruction or unlock; 512-bit extraction corrected to 504 post-header payload bits | `review_leads/cryptanalysis_2026_10_15/README.md` |

**Claimed but not checkable** (no script or output in the repo) [not checked]:
- `mywork/LOG.md` entries 3, 4, 5, 6, 7, 11c, 11d, 14 (entry 5 was rerun reproducibly as entry 16 on 2026-10-14)
- the 720 `try_sub.py` trials
- `pool2.py` and `cb_solve.py`, which have no saved result at all
- the 31 block-scan brainwallet additions

**A false lead to set aside:** the "1327-byte plaintext" of Cosmic Duality under the 4f7a key ends in a single 0x01 pad byte. A wrong key produces that about once in 256 tries. The output has 7.87 bits/byte of entropy and does not compress. It is consistent with a wrong key (`review_leads/CHECKPOINT_4F7A_VS_A5502.md`).

## 5. Open leads and unresolved operations

1. **Resolve the operation after the coordinate split.** Explain the complete 282-letter carrier and 281-symbol companion, including the seven-character interleaved header boundary. The new report separates exact prime/Hill constructions from unproved interpretations. The meanings of `matrixsumlist`, `lastwordsbeforearchichoice`, "zeroed out," and "yin-yang" remain unbound to a verified next operation.
2. **Mapping + board + transposition combined.** Never tested (`review_leads/MAPPING_BOARDS_REPORT.md:86`). The fixed-board r1 digit counts suggest the board itself may be wrong (`review_leads/TRANSPOSE_REPORT.md:35`).
3. **Opaque 78/79-byte plaintexts.** This covers unpadded 80-byte payloads, raw-block nesting without headers, and other cipher compositions (`review_leads/BINARY_FOLLOWUP_REPORT.md:136`, `review_leads/HASH_SCOPE_REPORT.md:102-110`).
4. **Finish the LTC/BTC scan:** 1,919 addresses remain. The script restarts from zero and overwrites its output, so add a resume step first.
5. **Vanity offset `--bits 36`** (about 5.5M point additions). Low priority (`review_leads/REVIEW.md:107`).
6. **Unexplained clues:**
   - the sign of H in Phase 2 (`review_leads/REVIEW.md:154`);
   - {1},{4},{21}, "Infrared", and "a piece outside the main puzzle" (`review_leads/CREATOR_CHAT_REVIEW_2026-10b.md`);
   - the meaning and authorship of the BSV blob (`review_leads/BSV_FUNDING_TRACE.md`).
7. **Chain-history gaps**, all needing live queries:
   - funding-wallet pagination;
   - sink and deposit inputs;
   - the method behind a5502d09.

## 6. Errors corrected in other documents

Each of these was confirmed on 2026-10-14 against the Telegram export, saved outputs or evidence files, and **corrected in place the same day**. Line numbers refer to the text before the correction. The "Says" column is the old wording.

| File:line | Says | Correct |
|---|---|---|
| `review_leads/HIDDEN_LAPTOP_DOOR_TRACE.md:9,15` | message ids 1047189 and ~1044357 | those ids do not exist (the export's maximum is 76044); the right ids are #67037 and #66909 |
| `review_leads/HIDDEN_LAPTOP_DOOR_TRACE.md:9,13`, `review_leads/TELEGRAM_REVIEW_2026-10.md:11-13` | times labeled UTC | those are local times (UTC-4); for example, #66903 is 22:19 UTC, not 18:19, and the "2026-07-12" creator posts are 2026-07-13 UTC |
| `review_leads/HIDDEN_LAPTOP_DOOR_TRACE.md:26` | "Obviously pretending" is attributed to the creator | written by F1f7h, #68902, 2026-08-17 |
| `review_leads/CREATOR_CHAT_REVIEW_2026-10b.md:53` | a "2026-05-21 creator post" about the halving | #63497 is a forward of creator message #5069 from 2020-11-24 |
| `review_leads/CREATOR_CHAT_REVIEW_2026-10b.md:39` | #34003 is a creator post | a forward posted by nieods; the decode itself reproduces |
| `review_leads/CHECKPOINT_4F7A_VS_A5502.md:34-35` | #71309/#71310 at 11:29 / 11:38 UTC | 15:29 / 15:38 UTC |
| `review_leads/BSV_FUNDING_TRACE.md:50` | block 968354 is from 2026-09-24 | blocktime 2026-09-25 19:35 UTC |
| `review_leads/LTC_SCAN_2026-10-08.md:53` | 241 results | 257 |
| `review_leads/LTC_SCAN_2026-10-08.md:9` | base-token list | omits `yellowblueprimes`, which `ltc_scan2.py:38` includes |
| `mywork/LOG.md:59` | no zero branch survives more than 1-3 lowercase bytes | r1-reversed reached 7 bytes, `'uoijgch'` (`mywork2/zero_tail.out:69`) |
| `mywork/LOG.md:68` | quoted beam string | it appears nowhere in the saved outputs; `zero_insert.out` may be from a rerun |
| `review_leads/REVIEW.md:7-83` | tests 1-3 are listed as "ranked next tests" with their planned costs | all three ran (only line 5 says so). Test 1 used 414 trials, not "at most 480". The filtered digit-map variant never ran and was superseded by the mapping-boards run |
| `scratchpad_grid.txt` | poster grid | 2 cells differed from `files/puzzle.png` (row 6 col 7, row 7 col 4, zero-based); now matches `STEPS.md` |

The `zero_enc.py` and `subsolve.py` control sentences, such as "Well done, you found the hidden zeros...", are invented test plaintexts. They are not decodes.

## 7. How this was checked

- Container sizes, salts and hashes were recomputed from `files/*.b64`.
- All eight checkpoint addresses in `STEPS.md:366-378` were recomputed with coincurve.
- Chat claims were checked against `result.json` by message id.
- Experiment counts were read from each experiment's results JSON and padding JSONL.
- `python -m unittest discover -s tests -v` passes 15/15 with `requirements.txt` installed.


The 2026-10-15 update passed its dedicated `audit.py`, exact source round trips, BIP32 test vectors, and recorded forward controls. The older 15-test regression result above is historical; the new research folder is self-contained and does not change existing solver code.
