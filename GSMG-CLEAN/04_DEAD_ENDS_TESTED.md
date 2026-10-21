# 04 — Dead ends already tested (with scope)

**What a "null" means here.** A null is a null only for the **exact candidates, conventions and success gate** that were used. The counts come from the round ledgers in `prior_research_ledgers/` and were not re-run during this clean-up.

**Weaker nulls.** Treat these as weaker than later results (details in 05):
- Nulls from before round gemini Add.21, and round-1 runs with raw-only oracles, used narrower checks.
- Runs that used the "exactly 64 B / pad 16", printable, English, hex64 or top-5 gates may have discarded real plaintexts.
- Literal-key comparisons made before 2026-09-12 were invalid because of the Base58Check bug.

Legend: *trials* = candidate × envelope decrypt attempts unless stated otherwise.

## A. Classical attacks on DBBI / FAED / the DBBI−VIC tail (`read_solve_review/STATUS.md`)

| Test | Scope | Result |
|---|---|---|
| Tail affine meet-in-the-middle | 11,560,320 scalars; period 17 at 94,058,496,000 each | null |
| Hex strings from tail/DBBI models → envelopes | 155,520 strings → 2,799,360 decrypts; 10,945 pad-valid | none readable, no key |
| Source documents as keys | 4,092 docs | null |
| FAED 3×3 Bifid, numeric | 206,841,600 | null |
| Null-octal readings | 11,612,160 | null |
| Morbit / Pollux | 211,196,160 / 11,455,506 | null |
| Affine 2×2 | 9,862,272 | null |
| Checkerboard with simulated annealing | heuristic, not exhaustive | null |
| Known-passage parses | 21,820 | null |
| Prime transposition | 670 | null |
| source_chain (lead 1) | 540 | null |
| Hill continuation (lead 4) | 12 conventions + 9 AES trials | null (`HILL-CONTINUATION`) |
| KEY-REVIEW literal key hunt | 31,957 keys | 0 |

## B. DBBI state work (grade C ledger)

- Literal-key hunt, re-run after the Base58 fix: 0.
- AES ladders over ~500k forms: 0.
- Matrix-sum constructions: ~160k.
- 14 maze traversals: null.

## C. Brute masks and sweeps

- 7,983,360 digit substitutions.
- Baseline masks: 1.64B / 9.87B / 470M.
- My2cents small-blob sweeps: 72.8M, 145.3M, 47.4M.

## D. Rounds v2 and gemini (`rabbitv2_audit`, `rabbit_gemini_audit`)

| Test | Scope |
|---|---|
| sweep | 787,788 |
| X2SH-VIC / X/Y passphrase | 475,212 / 22,810,176 |
| raise / carry / structural | 86,868 / 115,956 / 1,181,682 (pad ≥ 3: 0) |
| raw-key | 516, then 20,379 |
| final_block / lastwords / pipeline / twins | 46,956 / 5,800 / 8,952 / 47,752 |
| firsthint SHA×1–8 | 8,004 |
| fefefe | 6,138 |
| Poster readings | 5,120 |
| regate | 1,228,240 (**old gate**; see 03 lead 14) |
| genesis / whitepaper | 41,400 / 43,758 |
| zeroed | completed in Add.36 (1,195 readings) |
| Add.36 terminal campaign | null |
| Live-site path batteries | all 404 (unknown path) |
| Add.47 | ~17k + 19,104 paste_eval |
| Add.48 | ~1,061 key derivations + 4,200 decrypts |
| Add.42 / Add.43 nest-as-index | 624 / 1,404 |
| second_door (after 163 fix) | 684 |
| yinyang_carry | 11,496 + 15,120 |
| solve_32_stage | 1,296 |
| board_80_81 | 492 |
| term_mainline / term_carry | 168 / 72 |
| twin protocol | 3,688 |
| marker24 | 1,575 |

## E. Round v4 workstreams A–K (`rabbitv4_leads/RESULTS.md`)

| Workstream | Scope |
|---|---|
| A. *Looking Forward* text | 289,764 + 4,058,691 |
| B. Norton / X/Y | 265,512 + 60,356 |
| C. Colours | 173,700 |
| D. Numbers 661 / 121 / 103 | 8,736 |
| E. Executive Order | 200,364 + 821,784 |
| F. Neo's passport | 1,861,464 + 33,048 + 18,480 |
| G2. First hint | 15,060 |
| G3. Other door | 8,064 |
| H. Decimal encoding | exhaustive |
| I. Prime / zero | 39,840 |
| J. Poster re-decode | 8,904 |
| K. Poster method | 267,648 |
| lead_test_0912 | 235,620 |
| jerry11 | 22,176 |

## F. puz-op and v3 (`puz_op`, `rabbitv3_reviews`)

**puz-op**
- dbbi_faed_transform: 58,292 trials, 221 pad-1 (chance level), no key.
- wrapper: 7,265.
- prime/colour: 2,934.
- Pascal: 2,106.
- FAED 19×81: 29,184 + 1,488.
- bridge: 432.
- row selector: 34,272 SalPhaseIon trials with the selector strings **AES-tested** (rabbitv3 report, 135 pad-1, 270 downstream, 1 Terminal pad-valid, no key). The old "not AES-tested" note was wrong.

**v3**
- passport: 124,860.
- signed operands: 42,560.
- full61: 27,512.
- classical: 32,114 transforms + 168 AES.
- gate differential: 69,666 calls, 379,817 scalars.
- 2,436 bitstreams door search.
- gate audit (2026-09-11): the old screen rejected all three real plaintexts; re-run without the top-5 cutoff gave 23,222 texts, 282 pad-valid, none coherent. The "412 rejected DBBI outputs" null was never logged, so it is **unsupported**.
- L1/L2 P2-AST selectors on matrix sums: 606 trials, 0 pad.
- finite cross-product: 288 + 288 random controls, 0 pad.
- LOCKED_ENVELOPES sweep: 31,104 (before the key-checker WIF/base64 fix).

## I. Found in session logs and outside workspaces (2026-09-13)

Full table with labels and caveats: **06 §4**. The ones that change how older nulls should be read:
- **Void or partial:** fresh-start Terminal leg (48-B truncation, 139,288); idk-btc session15 / bounded tests (Half-only target; pad-valid outputs without key events dropped); v49 salvation audit (no sha256hex); Issue #106 (MD5); `oracle.py` 349M / 437M runs (wrong target); Cursor v1 (MD5); idk-btc CP-SAT / 161,802 operand trials / KMODEST 2,432 (Half-only).
- **Gate-only** (never reached AES): fresh-start evidence-first 12,288 sum lists; 14×14 bridge 608.
- **Chain-4-based** (built on a fitted mask): VERIFICATION_REPORT certificates and MITM; fresh-start C(7,3) / nested AES / seven-token sets.
- **Moot:** searches aimed at `1NULY7…` (a tool tip address); B1357/S1357 automaton (#24071 is a halving countdown).
- **Clean nulls of note:** nest module door-1 (246); pipeline_enum (17,905); SalPhaseIon pre-registration v1–v22 (71,184; 253 pad vs 279 expected); Cosmic XOR subsets (131,064; odd sizes, order-blind); hexgate (29,045,480; weak gate); nonce audit (187 signatures).

## J. Runs made in this folder

| Run | Scope | Result |
|---|---|---|
| `runs/2026-09-13_zero_envelopes` (pre-registered, controls passed) | ZERO prime-grid family 8,163 texts incl. 149 ZERO-schedule controls; fresh-start prime_matrix 5,076; astra zero-mask 944; × 3 envelopes × 6 (or 2) derivations = 194,382 AES-CBC. Plus fresh-start cipher family 1,514 × 46 configs × 2 EVP digests on the **full** Terminal = 139,288. | null: pad rates at chance, 0 pad ≥ 3, 0 coherent, 0 keys. Restores the voided fresh-start Terminal null (06 §1 item 5). |
| `runs/2026-09-13_seven_key_bifid` (pre-registered, astra 2,000-shuffle histogram reproduced exactly) | Seven-key Bifid: rounds 1–7 successive and independent, listed/reverse order, raw and 400/474-zeroed FAED, full / prefix 3–12 / after-BTCSEED forms, BAR/CAN/FEE word combinations, the seven keys as passwords (joined, intertwined, sha256 concat/intertwine/XOR); upper and lower case; real DBBI + 200 shuffle controls = 59,976 texts × 3 envelopes × 6 derivations = 1,079,568 AES-CBC. | null: real 28 pad-valid / 6,408 (25 expected), controls 4,214 / 1,072,944 (4,207 expected), 0 pad ≥ 3, 0 text-like, 0 keys. Reproduces astra's 0-pad result on the 8 final outputs. |
| `runs/2026-09-13_l5_backcheck` (pre-registered, 8/8 planted controls recovered; **stopped at 4,443/4,444 jobs**) | L5 DBBI hash-pattern gate (chance 2^-211.7 per digest) over every string harvested from 4,429 unique files (3.7 GB: rabbit-combined, puzle incl. v38/v39 candidate files, astra, fresh-start, idk-btc, puzzle-related Claude/Codex logs) plus reference-text n-grams and letter-stream substrings; 11 forms × sha256 / sha256d / sha256-of-hex / sha3-256 / identity × 3 orientations = 1,117,326,681 digest checks on 16.8 M strings. | null: 0 hashed-string matches. The 22 logged lines are all the pattern string itself quoted in notes/logs (identity view). One unfinished job, and generated-but-unsaved candidates, are not covered (REPORT scope). |
| `runs/2026-09-13_last_words_referents` (pre-registered, controls passed) | Structural referents for `lastwordsbeforearchichoice` (09 §2: P1 Scott Manning l.105 before _Neo walks to the door on his left_, both transcript wordings; P2 before "the problem is choice"; P3 before Neo's "Choice."; P4 puzzle text before SELECT; P5 whole puzzle text; after-choice control) as every suffix / sentence / clause, plus 144 L1/L2 prime sum-list strings; 15,676 unique strings × L5 gate (4 views × 3 orientations = 188,112) × 3 envelopes × 4 profiles (188,112). | null: 0 L5 matches; 0 pad ≥ 3, 0 keys; pad=1 750 vs 731.9 expected. Scope: literal answers only, not use as key/selector. |
| `runs/2026-09-13_matrixsum_pipeline` (pre-registered v1 + v2, controls passed) | #8446 pipeline: poster/DBBI/FAED/L2 matrices with yellow/blue × prime selections (69) → row/column sums fwd/rev/nonzero/cumsum (552 lists) → 12 decodes (a1z26, mod26 ×2, ascii, parity→ASCII, digits→bytes, index into Architect letters ×2, transcript letters ×2, puzzle/transcript words); 400 shuffled-input controls, planted controls; all 4,677 outputs × 8 forms → L5 gate (110,832) and 3 envelopes × 4 profiles (110,832). | null: 10 letter families at control level (planted 47–56 beat all controls); 2 word-index families have NO power (planted 7 vs control max 21), so they are uninformative; 0 L5, 0 pad ≥ 3, 0 keys. Not covered: diagonals, rings, blocks, modular sums, lists as cipher keys. |

## G. Round 1 logs (`rabbit_r1/FINDINGS_round1.md`)

**Runs**
- allwin: 11,817,000.
- arch / arch2 / arch3 / arch4: 664,020 / 3,159,432 / 22,171,500 / 11,964,024.
- kdfsweep: 325,440 (includes PBKDF2 variants).
- bigsweep: 20,284.
- msl: 137,952.
- h140: 5,242,860.
- seven: 1,088,640.
- lastw: 78,984.
- newblob: 56,784.
- runall: 170,352.
- src1616: 31,248.
- yb: 192,192.

**Caveats**
- The B1 half-blob bug affects B1-only sweeps.
- fastoracle checked only the Half address.
- The oracles were raw-only.

## H. Web, image and chain checks

- **Web census:** 831 CDX URLs, 843 candidates (`evidence/web_archive/`). No hidden route; the SPA router has only `/puzzle`.
- **Images:** the PNG structure and LSB are clean. The poster QR is pristine.
- **Chain:** no ECDSA nonce reuse (6 distinct r values). The OP_RETURNs are third-party (#12653 "Correct").
- **DBBI vs VIC:** DBBI is **not** a simple substitution of the VIC plaintext.
- **13×7 transposition of DBBI:** z = +0.68 (no signal).
