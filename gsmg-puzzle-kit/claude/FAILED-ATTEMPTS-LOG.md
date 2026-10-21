# GSMG.io 5 BTC Puzzle: Failed-Attempts Log for the 3 Locked Containers

**6 October 2026 supersession note (original record below retained).**
Read [doc 118](118-correctness-audit-remediation.md) for detector/coverage limits
and [doc 119](119-current-evidence-ledger.md) for current findings. In particular:
CBC plaintext bounds are conditional; filler/no-payload and global L84 exclusions
are unproved; 140 does not authenticate the 1008/868 pointer; a claimed FAED
last-60 no-g premise is false (six g's); continuation must not double-count event
24 on L84. Historical Atlas-derived leads are not active work. No old test output
has been edited to imply a rerun, and no listed gap is automatically a queued task.

Prize address: `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`
Compiled: 2026-10-03 from Desktop, D: and E: (E: contained no GSMG work; its keyword hits were false positives in unrelated notebooks and JSON files).
Purpose: a "do not repeat" register. **No source on any drive shows an authenticated opening of any of the three containers.**

> Read every row as "ruled out for that candidate set, KDF, password form and validator only". It does not mean the container is closed to the whole idea.
> Counts overlap between sources and **must not be added together** as unique attempts. Several totals below are reconstructed from script code, not from saved logs. Those are flagged.

---------------------------------------------------------------------
## 1. The three containers

| ID | Name in sources | Salt | Size | Where it sits | Plaintext bound |
|---|---|---|---|---|---|
| **T** | Architect-128 / "Terminal" / "P3.2 end" | `b45a5e3d827593ca` | 128 b64 chars = 96 B file, 80 B ciphertext | last two 64-char lines of the phase-3.2 page | 64-79 B |
| **S** | b1, or b1+b2 / "SalPhaseIon short" | `3ab585348552415d` | b1 = 48 B (header + salt + 32 B); b2 = 48 B **with no header**; b1+b2 = 96 B / 80 B ciphertext | two 64-char base64 halves on the SalPhaseIon page, with the 40-bit `enter` field between them | b1 alone 16-31 B; b1+b2 64-79 B |
| **C** | Cosmic Duality | `2d3f6fe06dc950e6` | 1792 b64 chars = 1344 B file, 1328 B ciphertext | side page "Cosmic Duality" | 1312-1327 B |

**Caveats on this mapping (inferred, not stated by the sources):**
- No file on disk uses exactly the label "Architect-128" together with "b1/b2" and the dossier names. The mapping is built from salts and sizes.
- **Sources disagree on the third container.** The astra-puz dossier and GSMG-CLEAN treat Cosmic Duality as the third locked blob. The `D:\5btc` verification register treats Cosmic as an "opened, reproducible but unconfirmed candidate" (the XOR/MD5 1327-byte output, pad 1). That output is statistically noise (see section 6), so I list Cosmic as still locked.
- In the `D:\5btc\verify-work` probe scripts, the "three envelopes" are Architect-128, b1+b2 and b1 standalone.
- `D:\5btc` finds no distinct "final prize envelope". E3 (570 a-i letters) is undecoded data, not an AES container.

**Proven recipe for the three *solved* page blobs (phase 2, 3, 3.2 only; unproven for T/S/C):**
password = lowercase hex SHA-256 of the answer phrase (64 ASCII chars); KDF = OpenSSL `EVP_BytesToKey`, SHA-256, 1 iteration; AES-256-CBC; PKCS#7.

**Success oracle to use:**
- Do not treat PKCS#7 pad=1 as success. It occurs about 1 in 250 for any wrong key.
- Do not use printable-text filters. The correct phase-3.2 plaintext is only 58.9-59.8% printable.
- Check any 32-byte window (BE/LE), or SHA-256 of the output, or WIF or base64 of the output, against the prize hash160 `a9553269572a317e39f0f518cb87c1a0ee1dbae4`. Check against `4bc468447fe1b048ad030a2f9a125478eabc4ed6` (17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa) as well.

---------------------------------------------------------------------
## 2. Validator defects that void or weaken older negatives

| Defect | Affects |
|---|---|
| Session 12: >90% ASCII gate | dropped 2 padding-valid binary outputs (388 trials) |
| Session 13 (`session13_b1_architect.py`): unpads before the full-pad check, logs only pad<=2, drops non-printable bodies with pad 3-16 | 781,312 Architect trials; b1 tier (8,190); T3/T4 |
| Session 13b: fixed pad check but skipped the 24-token core and tried odd sizes only | 37.8M Architect trials. Not a full universe |
| Early scripts: printable-ratio gates 0.7-0.9, mostly SHA-256 KDF only | sessions 2-8, `architect_attack.py`, `crossphrase.py`, `revised_attack.py`, etc. |
| Base58Check bug | any literal-key comparison before 2026-09-12 |
| Harness defaulted to MD5 EVP, or printable-only filter | `oracle.py` MD5 branch (349M/437M runs, wrong target); GitHub issue #106 (~2.5B tests) |
| Terminal loader truncated to 48 B (`E:\testing-btc-p\fresh-start`); Half-only target (`Desktop\idk-btc`, fastoracle); raw-only oracles | those runs |
| b1 half-blob bug: dropping the `z` at b64 position 64 of half 1 gives a bad 95 B blob | any b1/b2 run built from that parse |
| Phase-3 salt mis-transcribed as `35f64511d3d11f4c` (true: `9fbc451d13d071f4`) | `D:\5btc\known-real\verified\aes-envelope-recipe-and-decryptions.txt:27` |
| Cached `GSMG-CLEAN-main/data/phase*_plaintext.bin` has CRLF changed to LF (642/4032/2411 B instead of 648/4090/2422) | byte-offset work on those files. Use `astra-puz\qr_analysis\exact_plaintexts\` |
| Community scripts bail on non-printable first block or require 100% printable | community results, unverified |

Reliable (fixed-validator) coverage:
- **Session 15:** `session15_recovery.py` re-ran the 24-token universe at sizes 1-7 against T (1,072,308 trials) and b1+b2 (1,072,308). It also ran the 40-token universe at even sizes 2/4/6 against T (7,570,104). Total 9,714,720 by the output file; the README says "9.88M".
- **Not re-run with the fixed validator:** the 40-token odd-size universe (~38.6M) and any b1-standalone tiers.
- `astra-puz` REEX and the `zero_loss_validator.py` scripts are also valid.

---------------------------------------------------------------------
## 3. Container T: Architect-128 (`b45a5e3d827593ca`)

### 3.1 Password and phrase sets (D:\5btc\verify-work, sessions 2-18)
| # | Attempt | Scale | Result | Status | Source |
|---|---|---|---|---|---|
| T1 | 227-char phase-3 string; raw and sha256hex; EBK MD5/SHA1/SHA256 and PBKDF2 | n/a | 0 | closed (also fails vs Cosmic and blob A; it opens the phase-3 blob only) | `architect_attack.py`, session 2 and 6 notes |
| T2 | `architect_attack.py`: stripped block, alnum, digit string, chess line, onefor/fourforone, wakeup, wakeneo, fubcd, oraclequeen, thingkymvps, sadboard, architect, givemetheenvelope, A1Z26 of digits | n/a | 0 | PARTIAL (ASCII-ratio gate) | `architect_attack.py` |
| T3 | `sweep32.py`/`decrypt32_full.py`: jacquefresco riddle, "givetit" typo, challenge string; 3 EBK digests + PBKDF2 (sha1/256/md5; 1 and 10000 iterations) | n/a | 0 | calibration sweeps | `sweep32.py` |
| T4 | `sweep2.py`: sha256hex of speech substring windows 6-45 chars; all 12-30 windows; chess words under Beaufort/Vigenere/autokey with `thematrixhasyou` at all 15 phases | ~240k+ | 0 | PARTIAL (SHA-256 KDF only, printable gate) | `sweep2.py`, session 3 |
| T5 | `speech_attack.py`: specials, word n-grams 1-6 around keywords, tail grams, book-cipher parses of digits (up to 300k) | n/a | 0 | PARTIAL | `speech_attack.py` |
| T6 | `crossphrase.py`: enter, firsthint variants, shabefour, shabefanstoo, matrixsumlist, phase-1 password/hash, matrix-sum renderings (widths 7/9/13/19/26/29/57/58) | n/a | 0 | PARTIAL (ratio >0.8) | `crossphrase.py` |
| T7 | `revised_attack.py`: ~120 thematic strings (yinyang, cosmicduality, Matrix, film quotes, 3024/149/75/558/91/570/765, Decentraland coordinates) | n/a | 0 | PARTIAL | `revised_attack.py` |
| T8 | `test_four_for_one.py`: 21 concatenations of the four phase passwords x {sha256hex, raw} x {SHA-256, MD5} | 84 | 0 | closed | `test_four_for_one.py` |
| T9 | Session 6: 227-char variants (raw, sha256hex, live-FEN, no-0x, UPPER-hex, parts-only) x EBK SHA-256/MD5 | n/a | 0 | closed | session 6 notes |
| T10 | Sessions 7-8: z-phrases (both orders), film-choice candidates, 12,296 tail-window candidates, 75-group sum partition (falsified) | 12,296+ | 0 | closed | sessions 7-8 notes |
| T11 | Session 11/12: Cosmic XOR password `a795de11...e50735` and the two 32-byte halves (raw/hex, MD5/SHA-256) | small | 0 | closed | session 11 |
| T12 | Session 12: 388 AES trials (Cosmic material 134; three 7-token XOR/concat lists 42; choice phrases 212). Also 12 prize-key algebra combos (no AES) | 388 + 12 | 0; 2 pad-1 noise | PARTIAL (ASCII gate) | `session12_architect.py`, `session12-report.json` |
| T13 | Session 13 T3/T4: 12 extraction phrases x {literal, sha256hex, sha256raw} x 2 KDFs; 9 whole objects (speech, VIC message, chess sentence, 227-char, select-clause, final sentence) | not logged | 0 | PARTIAL (defective validator) | `session13_b1_architect.py`, `session13-log.txt` |
| T14 | Session 13 T5: XOR of odd-sized subsets (k=1/3/5/7) of 24 tokens | 781,312 | 0 (3,073 pad-only) | PARTIAL, but **superseded by session 15 Tier A** | `session13-log.txt` |
| T15 | Session 13b: 40-token vocab, odd k=1/3/5/7, subsets with at least 1 new token | 37,841,664 | 0 (148,348 pad-only) | PARTIAL (odd sizes only, skipped core) | `session13b_expansion.py` |
| T16 | **Session 15 Tier A**: 24 tokens, sizes 1-7, fixed validator, 64-B scalar-pair vs both hash160s, SEC1-65, BIP32-78 | 1,072,308 | 0 retained | **VALID** | `session15_recovery.py` |
| T17 | **Session 15 Tier B**: 40 tokens, even sizes 2/4/6, at least 1 new token | 7,570,104 | 0 retained | **VALID** | same |
| T18 | `crack_v24_zero_loss.py`: V24 list, sizes 1-7, raw and hex, MD5/SHA-256, zero_loss | no saved output | none recorded | overlaps T16; its V24 list differs slightly; only the first ~199 lines were inspected | `crack_v24_zero_loss.py` |
| T19 | `crack_seven_concatenations.py`: 7 semantic slots, at least 3 non-empty, concat -> sha256hex/raw, MD5/SHA-256 (bound ~220,500 combos before filter) | not persisted | none recorded | valid validator; only the first ~170 lines were inspected | `crack_seven_concatenations.py` |
| T20 | `test_seven_intertwined.py`: 576 assemblies | 576 | 0 | closed | `test_seven_intertwined.py` |
| T21 | `test_choice_phrases.py` (13 speech tails + film phrases); `test_last_words.py` (~70 phrases) | ~1.1k | 0 | closed | scripts |
| T22 | `sweep_unified_envelopes.py` (run91 7x13/13x7, run570 factorizations, rabbit centre cells, checkerboard codes 10/44-49, command tokens) | 1,872 (19 pad-valid) | 0 | closed | `zero_loss_sweep_results.json` |
| T23 | `sweep_hint_compilation.py`: ~150 hint tokens + case/space variants | 3,472 (18 pad-valid) | 0 | closed | `hint_compilation_sweep_results.json` |
| T24 | Session 17 probes: `probe_s64_reinsert.py` (576), `probe_matrixsumlist_15.py` (666), `probe_e3_prime_mask.py` (1,440), `probe_youwon_payload.py` and `probe_seven_trigrams.py` (outputs not saved) | 2,682 counted | 0; pad-1 noise only | closed (bounded) | `verify-work\probe_*.py` |
| T25 | Session 18: yin-yang on H1/H2 (73 candidates = 2,658 trials, 18 pad-1); E3 under named instructions (258 trials, 1 pad-1) | 2,916 | 0 | closed (bounded) | `probe_poem_yinyang_e3_results.json` |
| T26 | Bounded b2-as-key/IV layouts: `(B[:32],B[32:48])` and `(B[16:48],B[:16])` on b1, b1+b2 and Architect | 6 layouts | all fail PKCS#7 | **closed, do not re-recommend** | `adversarial-review/bounded_tests.py` |

### 3.2 Large-scale and clean-room runs (astra-puz, GSMG-CLEAN, 8.7-fresh-start, D:\GSMG-PUZZLE-DOSSIER.md)
| # | Attempt | Scale | Result | Source |
|---|---|---|---|---|
| T27 | `pipeline_enum`: yellowblueprimes -> matrixsumlist -> lastwordsbeforearchichoice pipeline, AES-256-CBC + EVP SHA-256 | 44,979 paths / 17,905 unique pw | 62 pad hits vs ~70 expected; 0 structural | `8.7-fresh-start\pipeline_enum.py` |
| T28 | `zero_envelopes` | 194,382 AES (+139,288 full T) | null | GSMG-CLEAN 04 §J |
| T29 | `seven_key_bifid` | 1,079,568 AES | null (28 pad vs 25 expected) | GSMG-CLEAN 04 §J |
| T30 | `l5_backcheck` (DBBI as substituted SHA-256) | 1,117,326,681 digest checks | 0 | GSMG-CLEAN 04, 03 |
| T31 | `last_words_referents`; `matrixsum_pipeline` | 188,112 + 188,112; 110,832 + 110,832 | null | GSMG-CLEAN 04 |
| T32 | Moves 0-6 (2026-09-14): pointer_selectors, board_shape_sums, colour_selectors, keyed_faed, tail_cipher, m4_zeroing_oracles, structural_key_formats (463,290 scalars), architect_differential (728), matrixsum_lastwords (34,860 vs 557,760 controls) | as listed | 0 | GSMG-CLEAN README, 10/11 |
| T33 | Colour-primes 479 -> PRIVATEKEY "M4 zeroing" (Architect plaintext = 1,539 letters, Beaufort key THEMATRIXHASYOU, PRIVATEKEY at 0-based offset 479) | 476 outputs | null | GSMG-CLEAN 03 |
| T34 | Recovery tests (lossy Hill models etc.) | 2,519,424 constructions / 245,184 full comparisons | null | GSMG-CLEAN 13 |
| T35 | Classical attacks on DBBI(91)/FAED(570): affine MITM 11,560,320; hex strings 155,520 (2,799,360 decrypts); FAED 3x3 Bifid 206,841,600; Morbit/Pollux 211M/11M | as listed | null | GSMG-CLEAN 04 §A |
| T36 | Brute masks 7.98M; 1.64B / 9.87B / 470M; 72.8M / 145.3M / 47.4M | as listed | null | GSMG-CLEAN 04 §C |
| T37 | Round 1: allwin 11.8M; arch1-4 664k / 3.16M / 22.2M / 11.96M; kdfsweep 325,440; h140 5.24M | as listed | null | GSMG-CLEAN 04 §G |
| T38 | Looking Forward / Norton / Executive Order / Neo's passport workstreams | see source | null | GSMG-CLEAN 04 §E |
| T39 | 551,714,300 chain-order combinations (judged on block-1 printable only) | 551M | 123 survivors vs 117 expected = noise | astra-puz DOSSIER §10.1 |
| T40 | All 2^30 corpus subsets with dbbi residue and header coordinate as atoms | 2^30 | null | DOSSIER §10.1 |
| T41 | Solved vocab + single-character corruptions under 8 ciphers (AES-256, ARIA, Camellia, SM4, SEED, 3DES, Blowfish, CAST5) x 2 KDFs | 7,163,600 | 1 noise hit | DOSSIER §10.1 (**only non-AES-256 coverage**) |
| T42 | SafeNet/Luna vocab (550,660); "creator's world" generator (475,808); creator vocabulary of 236 tokens incl. all pairs and 40-token triples (732,336); "last words" frames (1,808,960); four-slot concat (2.7M + 5.5M); raw-key acceptance (215,550) | as listed | null | DOSSIER §10.1 |
| T43 | Creator-corpus win-test: tokens 3-20 chars and whole messages up to 6 words | 8,812 strings | 0 | DOSSIER §10.1 |
| T44 | Prime masks over known answers (220); Neo passport date (307); Mr Robot / episode strings (1,586); 2026 OP_RETURN payloads (379); `infrared` (384); film pre-door lines (6,720) | as listed | null | DOSSIER §10.1 |
| T45 | **REEX 2026-09-21**: six runs, 141,846 distinct base candidates, 5 password forms (raw, SHA-256 lower hex, SHA-256 upper hex, raw digest, SHA-256 of the hex string), SHA-256 and MD5 EVP, AES-256-CBC, all containers | **4,467,816 decrypts** | 0 authenticated plaintexts. 17,412 pad-valid (17,339 pad-1, 72 pad-2, 1 pad-3 on Cosmic = noise). 446,315 scalars vs prize pubkey: no match | `astra-puz\REEXAMINATION_2026-09-21.md` |
| T46 | DOSSIER §10.7: sha-before-combine 154,784; 4-part orderings 131,040; riddle readings 726,067; Architect text before choice points 163,904; August 2026 farewell page 12,645; merged-zero payloads ~16.8M; structure-agnostic recogniser ~28M + ~3M chain decrypts | as listed | null (random pad-3/flags only) | `D:\GSMG-PUZZLE-DOSSIER.md` §10.7 |
| T47 | PBKDF2-HMAC-SHA256 (10,000 and 600,000 iterations) on all three: stopit, sheisgoingtodieandthereisnothingyoucandotostopit, therearetwodoors, theproblemis, theflowerblossoms..., followthewhiterabbit, gsmgio5btcpuzzlechallenge, yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyang, incaseyoumanage... | 90 | all failed padding | DOSSIER §10.8 (record 122) |
| T48 | Salts as passwords (hex/UPPER/0x/latin-1/sha256/md5/decimal; 2- and 3-permutations; XOR of 2/3 salts) | script only | no hit recorded | `astra-puz\salt_probe.py`; DOSSIER also notes no salt is a prefix/suffix of any hash of the chain answers |

---------------------------------------------------------------------
## 4. Container S: b1 / b1+b2 (`3ab585348552415d`)

| # | Attempt | Scale | Result | Status | Source |
|---|---|---|---|---|---|
| S1 | All of T1-T25 and T27-T48 above also targeted b1+b2 (and often b1). Same candidate sets, same nulls | see section 3 | 0 | as in section 3 | various |
| S2 | Session 13 T1: XOR of all 4,095 non-empty subsets of 12 tokens (matrixsumlist, enter, lastwordsbeforearchichoice, thispassword, yourlastcommand, secondanswer, shabefour, shabefanstoo, shabefourfirsthintisyourlastcommand, ourfirsthintisyourlastcommand, hashthetext, b2 base64 text) x 2 KDFs | 8,190 | 0 (44 pad-only) | **PARTIAL (defective validator)** | `session13_b1_architect.py` |
| S3 | Session 13 T2: b1 literal and sha256hex of the 12 tokens; b2 as ASCII/hex/b64 password | not logged | 0 | PARTIAL | same |
| S4 | **Session 15 Tier C**: b1+b2 with 24 tokens, sizes 1-7 | 1,072,308 | 0 retained | **VALID** | `session15_recovery.py` |
| S5 | `probe_b1.py`: shabefour..., enter, phase-1 hash/password, z-decodes, SalPhaseIon variants, pairwise first-hint x last-command; EBK SHA-256/MD5/SHA1 + PBKDF2 | not persisted | none recorded | PARTIAL (printable gate; only ~170 lines inspected) | `verify-work\probe_b1.py` |
| S6 | `test_b1.py`: "We wont." variants | 6 | 0 | tiny | `D:\5btc\test_b1.py` |
| S7 | `execute_triangular_and_b1.py`: 13-row triangular E1 matrix sums, ourfirsthint + yourlastcommand/enter (`\n`, `\r\n`, binary) bindings | not persisted | none recorded | zero_loss validator; only ~170 lines inspected | `verify-work\execute_triangular_and_b1.py` |
| S8 | `enter484` on S | 1 | pad-1, 79 B, last byte 01 | **WITHDRAWN as false positive**. The header of `D:\GSMG_SHORT_enter484_lab_log.txt` still says "SHORT opened". The later `D:\GSMG_SalPhaseIon_lab_log.txt` withdraws it (derived addresses empty). The origin of "484" is unexplained | `D:\GSMG_*_lab_log.txt` |
| S9 | MD5 79 B output (sha256 `1449a217...`, hex `9fa9db91...`) from password `matrixsumlistenterlastwordsbeforearchichoicethispasswordmatrixsumlist`, and WIF `5K2byJMs...` | 1 | pad-1 noise | **RETRACTED false positive** (entropy 6.13, IC 0.0023, zlib expands 79 to 90 B) | DOSSIER §10.5/10.6; GSMG-CLEAN 05 |
| S10 | Each 80 B ciphertext tried as a 64-hex key on C and the other container | small | pad>=2: 0 | closed | `D:\GSMG_SalPhaseIon_lab_log.txt` |
| S11 | SalPhaseIon pre-registration v1-v22 | 71,184 | 253 pad vs 279 expected | null | GSMG-CLEAN 04 §I |
| S12 | Row selector 34,272 SalPhaseIon trials (+270 downstream); wrapper literals: firsthint SHA x1-8 (8,004), G2 (15,060), wrapper (7,265) | as listed | null | GSMG-CLEAN 04 §F / 03 |
| S13 | `keyed_ck_rescore.py`: dbbi 64-token straddle keyed-checkerboard "L5" sweep, 9! orderings x 32 hex alphabets x {raw, sha256hex} x 3 containers | ~69.7M **computed from script, no saved output** | no hit recorded | PARTIAL (unverified completion) | `astra-puz\keyed_ck_rescore.py` |
| S14 | Not recorded in any script inspected: standalone b2 keyed with a salt from elsewhere (e.g. b1's salt). This is an inference, not a grep-proven gap | n/a | n/a | **untried** | Agent A |

Community note (unverified): a 2026 Telegram post (`2026.txt:40455`, ~2026-08-16) says the yin-yang program converged "but cannot produce the password BLOB1 accepts", which is consistent with b1 still being locked.

---------------------------------------------------------------------
## 5. Container C: Cosmic Duality (`2d3f6fe06dc950e6`)

| # | Attempt | Scale | Result | Status | Source |
|---|---|---|---|---|---|
| C1 | **Community "solve"**: password = XOR of raw SHA-256 of 5 distinct tokens (enter, lastwordsbeforearchichoice, thispassword, yourlastcommand, secondanswer; `matrixsumlist` listed twice so it cancels) = `a795de117e472590e572dc193130c763e3fb555ee5db9d34494e156152e50735`, EVP MD5, AES-256-CBC -> 1,327 B, pad 1, SHA-256 `4f7a1e4e...c081` | 1 | **Reproducible but statistically noise.** 20,000 random MD5 passwords gave 85 valid pads, all pad=1 (1 in 235); 200,000 XOR-of-labels gave 808 (1 in 247.5). Entropy 7.87, IC 0.0038, zlib expands 1327 to 1338 B, same as urandom | **do not treat as an opening** | DOSSIER §10.5/6.5; `D:\5btc\adversarial-review` |
| C2 | Follow-up on C1's 68-byte base-38 output: split as two 32-byte scalars + tail `fc0c1b02`; BIP32 CKDpriv with index `0xfc0c1b02` / `0x021b0cfc` (both byte orders, swapped halves); tail vs SHA-256-first4, double-SHA-first4, CRC-32, Adler-32 and parent fingerprints; D[:64] and D[:65] as raw / SEC1 points | defined layouts only | 0 matches against both hash160s | **closed for these layouts** | `adversarial-review\bounded_tests.py` |
| C3 | Half/Better Half follow-ups: residue rule-2 XOR at every offset, XOR triangle with 16-byte leaves, 1,296 raw-32 windows of the body, 23 prime-indexed AES blocks | as listed | 0 prize hash160 | closed | DOSSIER §6.5 (E2) |
| C4 | Null-control for C1's 103x103 matrix range test: 479/4096 random matrices pass. Candidate addresses were first funded 2026-02-05, **after** their public "zero transactions" report (2026-01-29) | n/a | later funding is not authentication | informational | `adversarial-review\review.md` |
| C5 | Cosmic judged on **content** (corrected recogniser) over 605,214 decrypts (33,623 candidates x 3 password profiles x 2 digests x 3 containers) | 605,214 | 0 | closed | DOSSIER §10.5 ("MD5 gap closed") |
| C6 | Book runs (1,889,907; two random pad-3); Looking Forward OCR 1,311,445; three-slot cross 82,710 | as listed | null | closed | DOSSIER §10.6 |
| C7 | Cosmic reader: 21 language strings x raw / sha256-hex / -md sha256 / -md md5 (soup tokens, 2023 concat, flower line, HASHTHETEXT, halfandbetterhalf, lastwordsbeforearchichoice, theproblemischoice, therearetwodoors) | 21 x 4 | pad>=8: 0; nested/gzip: 0; prize/peel window: 0 | closed | `D:\GSMG_SalPhaseIon_lab_log.txt` |
| C8 | `jackdevs66/GSMG5_CDuality` `validate_uniqueness.py`: 7x5x6 = 210 combinations, 1 pad hit; its SHA-256 is the claimant's **own output**, not an external commitment (claimant clarification, GitHub issue #72, 2026-02-01) | 210 | 1 pad hit expected about 36% of the time | not independent confirmation | `adversarial-review\review.md` |

Other Cosmic targeting is already counted in T1, T7, T9, T11, T12, T39, T41, T45-T47.

---------------------------------------------------------------------
## 6. Retracted or false-positive openings (do not rebuild on these)

- Cosmic 1,327 B MD5 decrypt (C1). GitHub #55, retracted in #104; Gemini Add.29/30. Telegram claims of a "1327-byte blob" (`2026.txt:23874`, #60201 thread, `2026.txt:57585`) are the same fluke.
- The 79 B MD5 SalPhaseIon output and its WIF (S9). The WIF also pad-1-opens T under raw-MD5 ("Chain 4"), an unauthenticated padding chain.
- `enter484` on S (S8).
- Other pad-1 flukes recorded: itsinfrontofyoureyes, wewill, andend, Apropos, screenplay, hillfexmgsgq->C, HEISENBERG->S, a->T, absvolt (#10597), faed relabel `heacgdibf` (pad-3 on T, 77 B, 0.44 printable).
- GitHub #108 (mutated-base64 "Salph small blob"), #18782 (troll), April 2026 inbound payments to `1Kv59xv...` / `1KY3yqm...` (solver activity from fluke-derived keys).
- Community Telegram claims, **all unverified, none with a reproducible key plus authenticated plaintext**: "gnosis" (~2026-02-17, #60067), WhoAmI and others (2023-2024), `2026.txt:56983` "you opened 2 of the 3 blobs?". Nobody has posted a SHA-256 of an S plaintext (the TekniskTrading suggestion, `2026.txt:57390`).

---------------------------------------------------------------------
## 7. Non-decryption dead ends

**Website and chain**
- Live verifier `POST gsmg.io/phase1verification` is stage-1 only. 10 submissions already made; do not submit more. (A single re-POST of the known password on 2026-09-07 returned 302 to the Merovingian route.)
- Poem hashes: 12 SHA-256 `gsmg.io/<hex>` routes (whole poem / minus "Hush hush." / minus "Go back..." x 4 normalisations), plus `theseedispla~ted` (raw `~` and `%7E`): all 404 "Hello :-)". First-hint token hashes as URLs also 404. Plated / plaoted / plate / plane / unlocking / yinyang as doors: 404. 481 door paths tested.
- Wayback: the SPA-era captures return 200 for unknown paths, so a Wayback 200 is not evidence. 831 CDX URLs: no hidden route. PNG LSB clean; alpha all 255; no tEXt or post-IEND data.
- On-chain: the 2026 OP_RETURN stream (blocks 938165, 944096) is inbound dust spam to `17ucy...`; the creator denied authoring on-chain messages (#12653). The 379-candidate screen was null. The "creator cluster" idea was refuted (common-input rule). Six prize ECDSA signatures have distinct `r` (no nonce reuse; 187 signatures audited elsewhere). 18 `1GSMG*` vanity P2PKH hash160s are not a key family. `Desktop\1gsmg` was an on-chain forensics effort: no Schnorr/ECDSA match for the 64 B WITNESS blobs against 947 pubkeys, ~240 derived keys with 0 hits, and the dust channel is undecodable.
- "Half" and "Better Half" are post-hoc labels (halving day, #3901/#3902). The prize is a single key (#4624).

**Image side (opening poster, bunny, rebus)**
- Spiral URL: 24 bytes / 192 bits, with no spare capacity. Yellow/blue cells are the low-bit markers at spiral indices 7,15,...,191. The centre 4 bits (`0000`/`0100`/`1111`, depending on the layer chosen) are not an authenticated payload. `#fefefe` at cell (7,4), spiral 163: bit-flip, n-delete, n->o, XOR, DEL (0x7F) readings all negative (2,511 + 204 + 136 tests).
- Footer QR decodes to the blockchain.com prize-address URL only. Poster QR is pristine v4-L. No QR finder pattern in 138 candidate bitmaps.
- Rebus: the red tile does **not** spell CRYPTOLOGIC (it reads `crypto/gic`). The earlier 13,264-passphrase run rested on that error. REEX retested the corrected joins: 2,286 candidates, 27,432 decrypts, 0. Eight tile dimensions, sRGB chunk pattern (`;`) and tile containers: nothing found.
- Bunny faces LEFT; earlier east-facing analysis was wrong. "Interesting" (#2905) and "yin-yang is the next phase" (#39237) are not proof the phase has been reached.
- 479 prime-sum pointer: chance-level after multiple-comparison null. Treat as an index, not a password.

**E1, E3, E2 and matrixsumlist**
- E1 (91 letters): `(E1 - VIC) mod 26` gives a crib-authenticated candidate, with `YOUWON` at positions 22-27. It has not opened any envelope. The 64 leftover letters, as two 32-letter halves H1/H2, were tried: reverse, atbash, interleave, XOR/sum/diff A=0 and A=1, prime-extract (2,658 trials, 0). The 15 prime-basic cells (2,3,5,7,11,13,19,29,31,59,61,67,71,73,79; PT letters `OZJDBGNCKJLRYEX`, A=0 sum 171, A=1 sum 186) were reinserted as 79-char passwords (576 trials, 0).
- E3 (570 letters, a-i): still undecoded. Tried and negative: 7-bit ASCII of 196 coarse cells; z-field decimal (237 B, 33-38% printable); multi-tap keypad (excluded); prime/composite zeroing (max 44.7% printable); rabbit sublayer as bits; Beaufort/Vigenere with `thematrixhasyou` (570 = 15 x 38); straddling board (482 letters, 30 undefined codes, not English). Width 14 does not divide 570, 661 (E1+E3) or 765 (E1+E2+E3), so the reshape is excluded. The 15-mask / 6x91+24 VIC tiling (1,440 trials) is null. The (E-VIC) crib does not carry over to E3.
- `matrixsumlist`: session 16 executed sol's pre-registered forms. Alternating-RLE bitmaps (40x71, 40x72, both polarities) are noise, with no QR. Row/column sums mod 256 and the literal sums E1 w13, E3 w10/w19 and E1+E3 w40 gave nothing. 215,408 source-sum constructions, 0 exact matches. The 7x13/13x7 boards were tried. On the poster grid, 1,224 screens: 0. Theorem: no stream can be a row+column sum list. 7,480 further screens on faed/dbbi/residue/Architect/VIC-91/149 digits/soup: 0.
- Other negatives: periodic table, 5x15 board, knight tour, single-substitution crib (session 4); 75-group sum partition (session 8); 3024-total linkage unproven; homophonic solver (800 restarts, 1.6M proposals: no promotion); chess/straddle digits {1,4} forced by exhaustion over C(10,2)=45.
- faed/dbbi/residue as key material: 362,880 relabelings (3 streams, 2,903,040 screens), substrings >=8 (1,556,802), base-9 keystreams (188,352), Vigenere/Beaufort (632,944), byte-level codecs (13,536), zero-reinsertion to k<=18 (18.8B nodes), running keys (1,132,326), periodic keys 2-100, columnar widths 2-120, 21,145 homophonic partitions. All null. dbbi residue is statistically uniform (chi2 12.3, p~0.14) and ~190 bits, so too short for a 256-bit key.
- Architect decode instructions executed: Beaufort with `thematrixhasyou` (1539 letters) and the checkerboard (91 letters). Empty slots 10 and 44-49 are derived holes. `J,Q,Z,X,W` is not part of the decode.
- "Source code pointer" lead: last 60 ordinary digits give two lists summing to 1008 and 868 (difference 140). Architect index 1008 starts `TORETURNTOTHESOURCECODES`, and 140 is the genesis-code length. This is a lead, not a recipe. Follow-on width/23-triplet/14-wide/prime-position runs gave only fragments of the genesis headline.

**Other puzzles found on disk, unrelated to the containers**
- `Desktop\500\puzzle-solver` and `500\.firecrawl`: the separate "Phy Challenge" (bitcointalk 5584952, secp256k1 emoji puzzle): 872,585 oracle checks, 0 passes. No AES containers.
- `Desktop\22\tools\hunt_log.md` (BIP39 weak-mnemonic hunt), `coinbit`, `btc-140`, `bunny`, `gpt-projects` registry, `D:\CHAIN_CHECK_PROMPT.md`, `D:\candidate_addresses.csv`, `D:\bitcoin-info\analysis\puzzle_owner_trace` (160-bit btc-puzzle creator trace): no GSMG container attempts.

---------------------------------------------------------------------
## 8. What has NOT been covered (genuine gaps, not ruled out)

1. **40-token odd-size XOR universe** (~38.6M two-KDF trials) was never re-run with the fixed validator. The same applies to b1-standalone tiers.
2. **Ciphers and KDFs.** Nearly everything used AES-256-CBC with EVP SHA-256 (and MD5 in later runs). PBKDF2 and SHA-1 ran on only ~40 candidates (`kdf_probe.py`) and 90 attempts (§10.8). Other ciphers ran only on the T41 vocabulary (7.16M). ECB and AES-128/192 are only lightly covered.
3. **Binary or non-text intermediate data.** REEX explicitly says transformations before the decimal stage and binary plaintext cannot be excluded.
4. **170,295-form trailing-space / no-padding / raw-key residue** for T and S (700,582 total proposal): never launched (DOSSIER §12).
5. **Untried or partial per dossier:** `infrared` inside longer passphrases; the RYB reading; the full-scale "-42 join" replacement; the `O`/zeroing operators on non-Architect objects; `newest-puzzle-9.15.26-creator-attachments/` and Wayback captures beyond the CDX index.
6. **Standalone b2 keyed with a borrowed salt** (S14).
7. **Items with no saved output**, so completion is unverified: `short_brute.py` (~13.6M candidates), `dict_*.py`, `salt_probe.py`, `concat_rescore*.py` (~2.7M), `keyed_ck_rescore.py` (~69.7M), `crack_v24_zero_loss.py`, `crack_seven_concatenations.py`, and the `probe_youwon_payload.py` / `probe_seven_trigrams.py` outputs.
8. **Unresolved referents named by the creator and by every source:** what `thispassword`, `yinyang`, `enter`, "reinserting the prime basics", "return to the source codes", and the "twenty-three ciphers / sixteen encryptions / seven intertwined passwords" refer to. Each source concludes the missing piece is a **justified operation on an existing object** (dbbi residue, the off-white cell, the 140-char code, the 479/1008 pointers), not another hash sweep over candidate strings.

---------------------------------------------------------------------
## 9. Source index (where to look for detail)

| Location | Contents |
|---|---|
| `D:\5btc\known-real\VERIFICATION.md`, `D:\5btc\adversarial-review\review.md` | Current verification register and adversarial audit (2026-09-08) |
| `D:\5btc\verify-work\` | Session 2-18 scripts, `session13-log.txt` (1 MB), `session15-output.txt`, `*_results.json`, `gpt_sol_*.md` AI consults (superseded claims) |
| `D:\5btc\independent-analyst-report-2026-09-08.md` | Independent report (flagged the salt transcription error) |
| `D:\5btc\telegram-export-9.8.26\txt\*.txt`, `known-real\creator-statements\` | Community claims (unverified); creator statements, including #8446 command order |
| `C:\Users\lucas\Desktop\astra-puz\DOSSIER.md` (180 KB), `REEXAMINATION_2026-09-21.md`, `qr_analysis\` | Largest attempt record; REEX 4.47M decrypts |
| `C:\Users\lucas\Desktop\GSMG-CLEAN-main.zip` | Docs `04_DEAD_ENDS_TESTED.md`, `05_CORRECTIONS_AND_PITFALLS.md`, `03_OPEN_LEADS.md`, `06_SESSION_LOG_REVIEW.md` |
| `D:\GSMG-PUZZLE-DOSSIER.md`, `D:\GSMG_SalPhaseIon_lab_log.txt`, `D:\GSMG_SHORT_enter484_lab_log.txt` | §10 large-scale runs; lab logs |
| `C:\Users\lucas\Desktop\8.7-fresh-start\` | Clean-room workspace; `pipeline_enum.py` |
| `C:\Users\lucas\Desktop\1gsmg\` | On-chain forensics (not an AES attack) |

**Not fully read when compiling this:** GSMG-CLEAN docs 02/07/08/09/12/14 and `runs\*\results.json`; `brief*.txt` and `gpt_sol_*` (grep only); `solve_*.py`, `plot_and_sweep.py`, `verify_cosmic_duality.py`; `D:\5btc\hint-photos\index.md`; Telegram 2021 and 2025 hits (2025 alone has 260 matching lines); `foreign-repos/`, `tmpblobs/`, Wayback HTML; the tails of four `verify-work` scripts (past line ~170-199). Treat the ledger as comprehensive for the major sources but not exhaustive.
