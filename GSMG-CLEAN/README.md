# GSMG.IO 5 BTC puzzle — clean working set

**Status (2026-09-13): UNSOLVED.**
- No locked envelope has been opened and no private key has been found.
- The prize address `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` still holds funds (01 §9).

This folder was distilled from every research round in `E:\rabbit-combined`: rabbit (r1), rabbitv2, rabbit-gemini, rabbitv3, rabbitv4, rabbitv5, read, puz-op, nice, gsmo-links, newest-puzzle-9.9.26 and New folder. It keeps only four things:
- material that is **proven and reproducible**
- **original source files**
- the **open leads**, clearly marked unproven
- records of what was **already tested** or **retracted**, so work is not repeated

## Read in this order

**83/84-cell forward comparison:** `E:\rabbit-combined\GSMG-CLEAN\runs\2026-09-14_dbbi_forward_comparison\REPORT.md` records both lossless poster-guided parses. They share 82 logical cells, and payload84 is exactly payload83 plus `e`. The explicit model FAED margins -> ordinary payload -> prime insertion produced 320 comparisons but no 60/61-character payload or complete DBBI reconstruction. Frozen-marker continuation into the label or FAED fails for both models. Five controls and an independent arithmetic verifier pass. **Neither endpoint is selected or eliminated.** This does not repeat the older direct-poster-sum nulls as a new discovery, and does not exhaust the other roles of DBBI.

**Aligned replacement table and matrix tests:** The completed, lossless table is at `E:\rabbit-combined\GSMG-CLEAN\runs\2026-09-14_aligned_replacement_v2\REPLACEMENT_TABLE.md`, with all eight alternatives in `replacement_table.csv` and `tables.json`. Read the accompanying `REPORT.md` for scope. Both transcripts share 22 puzzle-edit intervals; the apparent 24-row table depends on two extra transcript differences (`in/TO`, `then/THAN`). No intended matrix is established. 264 explicit matrix candidates and the eligible 24-edit-row interpretation produced 1,944 sum lists and 28,170 retained text/binary outputs. Independent accounting/serialization checks pass; 425,198 unique scalars yielded no prize match, and no DBBI hash-pattern match was found. This supersedes earlier claims that the edit map is the correct operand or that a matrix must be 14 wide. Those remain hypotheses, not findings.

**Recursive structural key-format audit (2026-09-14):** [runs/2026-09-14_structural_key_formats/REPORT.md](runs/2026-09-14_structural_key_formats/REPORT.md). The envelope inspectors already covered raw32/hex64/WIF/base64 keys recursively, but several new pre-AES structural runs had only checked hashes or whole-output scalars. All 38,615 retained structural outputs were therefore regenerated and scanned recursively: 20,436 byte nodes, 518,386 BE/LE sliding raw32 checks, 198 explicit 32+32 Half/Better-Half checks, 35 base64-to-32 values, one hex64 and 42 WIF-shaped tokens. Seven planted format/target controls passed. **0 valid WIFs and 0 target-key matches among 463,290 unique valid scalars.** A WIF made from either raw half is fully covered; concatenating textual WIF fragments across unrelated alternative records is not justified without a source-specified order.

**Closed-system correction (2026-09-14):** [15_CLOSED_SYSTEM_RESET_2026-09-14.md](15_CLOSED_SYSTEM_RESET_2026-09-14.md). Creator #9607 directly ruled out another URL / required brute force (“No need. You have all the info”), and #16624 said internet was not required. The previous conclusion that new information must come from outside the puzzle is retracted. `tools/audit_architect_differential.py` shows prior “source reinsertion” work did not model the actual source-to-rewrite differential. `tools/audit_matrixsum_lastwords.py` tests the literal command grammar omitted by the old pipeline (sum-list word indices → selected words’ last letters): 34,860 outputs vs 557,760 controls, 0 above control, 0 DBBI-pattern hits. Conclusion: the internal matrix sum list or its source matrix is still being constructed incorrectly; the puzzle input is not missing.

**Move 5, the 64-letter tail as its own cipher object, executed 2026-09-14** ([runs/2026-09-14_tail_cipher/REPORT.md](runs/2026-09-14_tail_cipher/REPORT.md), `python tools\audit_tail_cipher.py`, no envelope bytes read): the `DBBI − VIC` tail profiled (IoC **0.0397** — flat, not English's 0.065), attacked as monoalphabetic substitution with a 60×400 hill-climber (score 8 vs control max 7: control level; best "decrypt" is letter soup, 0 oracle hits) and through **178 layered forms** (Vigenère/Beaufort with the balanced numbers and Architect/transcript windows at 0/479/484, rails 2–16, columnar permutations at every exact divisor — max score 2 vs control max 2, **0 exact-oracle hits**; planted round-trip passed). Closed: the tail as an English-shaped cipher object. Left open (non-English by design, needing their own oracle): substitution+transposition composition, the tail read as numbers/bytes, the tail as a *key*.

**Move 6, the sibling corpus, executed 2026-09-14** (same report, §2): `D:\downloads-8.8\puzle-main\` SOLUTION.md / STATE_OF_PLAY.md and the `gsmgio-5btc-puzzle-master\` inventory read and reconciled against 01–14. Everything evidenced outside is represented here or refuted by 04/05/06; the `yinyang_*`/`youwon_*` series rest on the retracted Chain-4/fluke primitives (05-void). One entry stays open, framed as the outside file frames it: the **F-A-E sonata mapping is a pre-registered untested hypothesis owned nowhere**. Nothing was copied in from the outside workspaces.

**Move 4, DBBI material as keys over FAED, executed 2026-09-14** ([runs/2026-09-14_keyed_faed/REPORT.md](runs/2026-09-14_keyed_faed/REPORT.md), `python tools\audit_keyed_faed.py`, no envelope bytes read): the one sourced reading never run as a bounded family — 31 key families (6×14/7×12 sum lists, the six balanced numbers, all primes and colour splits, the 84 cell values, the poster sums) × Vigenère both ways and Beaufort × 9-letter/+codec and 26-letter alphabets. **93 decodes vs 240 controls: 0 above control** (max real 4, control max 8), **0 exact-oracle hits**. Closed: the prime structure as *key material*; open: the 64-letter tail as its own object, non-additive constructions, and the sibling-corpus reconciliation.

**Move 3, colours as selectors, executed 2026-09-14** ([runs/2026-09-14_colour_selectors/REPORT.md](runs/2026-09-14_colour_selectors/REPORT.md), `python tools\audit_colour_selectors.py`, no envelope bytes read): the 16 blue / 7 yellow markers used only to *select* DBBI's 61 ordinary cells — nearest-marker sides, colour-bounded segment sums (the most literal `matrixsumlist` reading), masked 6×14/7×12 lattices, colour-containing rows, and FAED at the blue/yellow/ordinary slots. **142 outputs vs 15,600 shuffle controls: 0 above control** (max real 2, control max 3) and **0 exact-oracle hits**. Planted control sits at control level here, so only a strong outcome could have been accepted — none appeared. Closed: the sourced prime+colour+sum family; open: the balanced numbers as cipher *keys* over FAED, the 64-letter tail as its own object, and the sibling-corpus reconciliation.

**Move 2, the 14-wide board, executed 2026-09-14** ([runs/2026-09-14_board_shape_sums/REPORT.md](runs/2026-09-14_board_shape_sums/REPORT.md), `python tools\audit_board_shape_sums.py`, no envelope bytes read): 744 outputs (84/83-cell parses × five value models — signed, unsigned, colour, and the M4 prime-5-zeroed variants — × 6×14/14×6/7×12/12×7 × five decode families) judged against **25,015** shuffle-control readings and the exact oracles. 0 outputs above control (max real 2, control max 4), 0 DBBI-pattern or address hits. The known `HILLFEXMGSGQ` reproduces as a sanity check and is the *only* strong word any model produces — which, by the folder's own standard (09 §5), is a weakness of the 7×12 model, not evidence for it. Closed: row/column-sum value lattices; open: colours as selectors (not weights), DBBI material as a cipher key, the 64-letter `DBBI − VIC` tail.

**Move 1, the balanced pointer as an operand, executed 2026-09-14** ([runs/2026-09-14_pointer_selectors/REPORT.md](runs/2026-09-14_pointer_selectors/REPORT.md), `python tools\audit_pointer_selectors.py`, no envelope bytes read): selectors 5/479/484/963 and six derivatives on FAED, DBBI, the 149 checkerboard digits, the SalPhaseIon stream and the Architect text. Exhaustive window decode through the page's own codec: **0 readable messages** (the only printable windows are chance runs, plus the two known labels). Prime/zeroing selectors decode to nothing readable. 2,119 selector-window candidates × 6,738 scalar forms → **0 exact-oracle hits**. Closed: the 03 §1 "next idea" of indexing the unread fields under the page codec with the balanced pointer.

**M4 zeroing construction closed against the exact oracles (2026-09-14):** [runs/2026-09-14_m4_zeroing_oracles/REPORT.md](runs/2026-09-14_m4_zeroing_oracles/REPORT.md) (`python tools\audit_m4_zeroing_oracles.py`, no envelope bytes read). Split result: the colour-prime balance is **unique** — of 48 prime assignments only the authenticated one is zeroable, and its balanced 479 is the only index in 48 × 3 conventions that selects `PRIVATEKEY` — but all **476** literal outputs of the construction are null against every exact oracle (three chain digests, part-replacement against `250f3772…`/`1a57c572…`, four marker addresses plus both prize addresses, DBBI token pattern), with the oracle machinery passing all seven controls first. So the construction is a pointer to Architect offset 479, not a payload.

**Critical review (read this before trusting any lead's strength):** [14_CRITICAL_REVIEW_2026-09-14.md](14_CRITICAL_REVIEW_2026-09-14.md) separates what is arithmetic from what is evidence. It shows that "23 prime cells" is `π(84) = 23` and therefore not independent confirmation (the real signal is the parse's 0/20,000 control); that the DBBI matrix shape used by the `HILLFEXMGSGQ` lead (7×12) contradicts the puzzle's own sentence "as wide as the first one seen" (14 → 6×14), where no word appears; that the 479 index survives only under two unstated conventions; that the `YOUWON` 64-letter tail is not a hex digest (24 distinct letters); and that a 50 KB `SOLUTION.md` plus a ~100-script solver repo and a whole `yinyang_*` audit series were listed as "not read" (06 §7) and never reconciled. Reproduce with `python tools\audit_critical_review.py`.

**2026-09-14 recovery tests:** [13_FAED_RECOVERY_TESTS_2026-09-14.md](13_FAED_RECOVERY_TESTS_2026-09-14.md) tests selective decimal zero/nine restoration after all affine 2×2 mod-9 Hill maps, arbitrary Hill keys against complete numerical source passages, Architect text as classical cipher keys, prime digits serialized before matrix formation, and full checkerboard matches preserving spaces/punctuation. End-to-end planted recovery passed; no complete FAED plaintext or new locked-stage decryption was recovered. The solve remains unfinished and all unresolved data remains retained. The goal runner reported a usage limit at the final checkpoint.

**Current direction audit:** [12_WHOLE_PUZZLE_DIRECTION_AUDIT.md](12_WHOLE_PUZZLE_DIRECTION_AUDIT.md) maps the entire available route, reproduces the solved connections and distinguishes incomplete clue interpretations from complete operations. It adds the source-supported straddle explanation for “Raising the stakes…” and corrects the claim that X/Y necessarily remain unused. Earlier “where to push” recommendations below are historical hypotheses, not required gates or a proven envelope order.

**Latest intermediate-only tests:** `runs/2026-09-13_label_models/REPORT.md`, `runs/2026-09-13_operation_instructions/REPORT.md` and `runs/2026-09-13_zeroing_operands/REPORT.md`. No authenticated field reconstruction, zeroing operand or locked-envelope solution was found. All generated intermediate bytes remain available.

**Complete SalPhaseIon framing:** `runs/2026-09-13_salphaseion_construction/REPORT.md` accounts for all 1075 characters with an exact source round trip, constrains binary/separator/envelope boundaries, tests shared prime-grammar continuation and a full sum-key/Beaufort/numeric model. The 661 characters in DBBI and FAED remain cryptographically unexplained.

**Latest model constraint:** `runs/2026-09-13_faed_constraints/REPORT.md` derives necessary decimal Beaufort/Vigenère keys for 694 full Architect passages, including explicit length-padding alternatives. All 1388 required streams have minimum period at least 567, excluding every short repeating key in that declared quotation model. This is not a rejection of all possible DBBI-to-FAED operations.

**FAED representation review:** `runs/2026-09-13_faed_structure/REPORT.md` retains a weak frequency change in the last 47 characters, finds no short-period signal in the declared controlled tests, and checks complete variable-length token streams against source passages. No full match; 25-symbol coverage is common to all 29 complete prefix-pair parses, not special evidence for b/g.

**FAED tail follow-up:** `runs/2026-09-13_faed_tail/REPORT.md` traces the full field to an April 2021 solver post and the saved June 2023 archive. The larger split control gives p=.0222; the boundary remains unconfirmed. Exact symbol counts exclude a shared DBBI/tail hex bijection and a standalone SHA-256 hex suffix under the b/g model. A damaged 462-character community copy was identified; the clean 570-character input is unaffected. No missing instruction or envelope solution was recovered.

**DBBI accounting correction:** `runs/2026-09-13_dbbi_accounting/REPORT.md` identifies a false leftover-e premise in earlier Hill-key scripts: the e already contributes to HILLFEXMGSGQ. It tests the corrected reserved-e key without success, verifies that the whole DBBI reproduces the BTCSEED Bifid square without a 13-character cutoff, and traces the poster mismatch specifically to H versus X in HILL. Twenty complete Hill/Bifid compositions and all corrected-key byte outputs are retained; no locked envelope opened.

**Off-white marker alignment:** `runs/2026-09-13_offwhite_alignment/REPORT.md` finds a complete 23/23 correspondence when the off-white cell is included as an additional b marker in spiral order. This deterministically selects the 83-cell DBBI parse, consumes final be intact and retains 60 ordinary characters. A competing per-byte XOR rule selects 84 cells, so intent is not yet settled. Two remaining poster markers are preserved; a direct continuation into matrixsumlist fails, and 40 direct poster-sum/payload comparisons are negative.

**60-character remainder tested:** `runs/2026-09-14_payload60_matrixsum/REPORT.md` expands the exact poster comparison to 2,098 serialization/model checks, tests 96 sum-list readings of the 60 digits and 48 of their 25 decoded bytes, and checks complete numerical text decodings. No exact sum-list relationship or instruction was recovered. The 83-cell alignment remains a structural lead; the role of its ordinary values is still unverified. All bytes and matrices are retained.

**Latest context review:** `10_ENVELOPE_CONTEXT_AND_SOLVING_STRATEGY.md` verifies the three solved decryptions and locked-blob extraction, distinguishes source branches from unproven solve order, corrects short-envelope format assumptions, and specifies how to derive and validate new candidates. The 755 recovered outputs remain unresolved and retained (`runs/2026-09-13_recheck_755/REPORT.md`).

**Latest experiments:** `runs/2026-09-13_salphaseion_roles/REPORT.md` tests direct field reconstruction and 10,288 source-derived composite candidates; no authenticated result, all 518 pad-valid outputs retained. `runs/2026-09-13_dbbi_prime_prefix/REPORT.md` verifies the old remove-g claim and reconciles the complete 83/84-cell prime grammar. The 84-cell reading gives 23 prime cells split 16 b / 7 be; its numeric meaning and next operation remain open.

| File | What it is |
|---|---|
| `01_PROVEN_CHAIN.md` | Every solved step, with the exact method and hashes. Everything here is re-checked by `tools/verify_chain.py`. |
| `02_CREATOR_HINTS.md` | Creator (Jrk Bgrt) quotes with message ids, dates and edit dates, grouped by topic. Includes caveats and contradictions. |
| `03_OPEN_LEADS.md` | 19 ranked, **unproven** leads: what is exact, what is inference, what has been tested. |
| `04_DEAD_ENDS_TESTED.md` | What earlier rounds tested, with trial counts and each null's scope. |
| `05_CORRECTIONS_AND_PITFALLS.md` | Retracted "decrypts", broken gates, script bugs, index conventions, excluded junk, reference-file line map. |
| `06_SESSION_LOG_REVIEW.md` | Review of the Codex / Claude / Cursor session logs and the workspaces they used outside `E:\rabbit-combined` (D:\astra, D:\puzle, E:\testing-btc-p, Desktop\idk-btc, …): solved marker addresses, new leads, voided nulls, new creator ids, where that material lives. Items are labelled [checked] / [log] / [claimed]. |
| `07_DUTCH_LENS_REVIEW.md` | Reading of every creator message with his Dutch in mind. "price" = prize (#3923), "better half" = his partner (#60324), NOTES = a joke echo, translated Dutch forwards #65528–65535 (photo_2244 = a scam-DM joke), day-first passport dates already tested. No new key or instruction was found. |
| `08_SALPHASEION_RECIPE.md` | Historical stream-order recipe interpretation. The labels are decoded; their operational roles remain hypotheses. L5 is an optional digest-pattern check, not a mandatory gate. See 10–12 for qualifications. |
| `09_UNFORESEEN_HINT_AND_LAST_WORDS.md` | The matrixsumlist "unforseen hint" (#6509) is most likely #5966/#5969 "prime part" (plus #6514 "Hush hush" → #1710). "Last words before archi choice": pinned referents P1–P5; P1 is the Scott Manning transcript that the creator quotes in #3390, right before Neo walks to the door. All referents and the prime sum lists were checked against the L5 gate and the envelopes: null. |

## Tools (Python 3, `pip install pycryptodome pillow`)

Run from this folder. Results observed when this folder was built:

| Command | Does | Outcome |
|---|---|---|
| `python tools\verify_chain.py` | Rebuilds the solved chain from `originals/` and `data/`: poster spiral, Phase 2/3/3.2 decrypts, Architect and checkerboard decodes, SalPhaseIon labels, DBBI−VIC, envelope bytes. Writes `data/verify_log.txt`. | `ALL CHECKS PASSED` |
| `python tools\reproduce_leads.py` | Recomputes leads L1–L6: colour-primes 479/484 → PRIVATEKEY, prime matrix → HILLFEXMGSGQ, Bifid/Hill, DBBI−VIC, DBBI hex tokens, b positions. Writes `data/leads_reproduced.json`. It does not search. | `ALL LEAD CALCULATIONS REPRODUCED (meaning unproven)` |
| `python tools\check_candidate.py --selftest` | Tests the envelope code, hash160, EC maths, WIF and the detectors. | `SELFTEST PASSED (…)` |
| `python tools\check_candidate.py "answer" …` / `--file list.txt` / `--quiet` / `--profile raw\|gsmg-md5\|raw-md5` | Tries your candidate answers on all three locked envelopes. Pad-valid outputs are scanned for keys matching Half or Better Half. It also flags a `[DBBI-PATTERN MATCH]`. | Writes `CANDIDATE_HIT.bin` if pad ≥ 3 or a key matches. pad = 1 is chance (1/256). |

- The default profile is the proven convention: passphrase = sha256(answer) as lowercase hex, EVP_BytesToKey SHA-256 with 1 iteration, AES-256-CBC.
- The other profiles are explicit opt-ins.

## Layout

```
originals/            source files as published: poster PNGs, rebus pieces, captured puzzle pages
                      (incl. 2026 live captures), Wayback CDX, Cosmic Duality images
reference_texts/      full community reference (line map in 05 §11), Matrix Reloaded Architect
                      transcripts (kedri; Scott Manning = the wording the creator quotes, 09 §2),
                      Looking Forward (1969), EO 11110, community readme, prize-address dossier
data/                 decrypted plaintexts (Phase 2 / 3 / 3.2), DBBI_91, FAED_570, Architect letters,
                      checkerboard plaintext, DBBI−VIC, poster bits, SalPhaseIon stream, 3 locked
                      envelopes (.bin/.b64), seven-part answer, lead outputs, verify log
evidence/decentraland/  parcel -41,-17: puzzlepiece.mp3, L−R spectrogram (HASHTHETEXT),
                      frames 4/15/131, scene/entity json, source map
evidence/web_archive/ deep web research report, 19 live URLs, 843 URL candidates, CT hostnames, PNG analysis
telegram/             chat exports (JSON, text only) + sourcebooks of creator messages
tools/                verify_chain.py, reproduce_leads.py, check_candidate.py
runs/                 pre-registered test runs made from this folder (manifest, candidates, results, REPORT.md)
prior_research_ledgers/  raw round ledgers kept for detail. They CONTAIN RETRACTED CLAIMS; see their README and 05.
SHA256SUMS.txt        hashes of every file here
```

## Telegram

**Exports in this folder**

| File | Chat | Messages | Dates |
|---|---|---|---|
| `telegram/ChatExport_2026-09-13_result.json` | "GSMG Puzzle Solvers" | 61,798 | 2019-04-20 → 2026-09-13 |
| `telegram/CommunityGroup_2026-09-10_result.json` | "GSMG - Community & support group" | 52,913 | 2018-04-17 → 2026-09-10 |

- `telegram/messages_missing_from_2026-09-13_export.json` holds 12 messages that are in older exports but deleted from the newest one.

**Media was NOT copied** because of its size. It is still in:
- Puzzle Solvers media (~1.3 GB): `E:\rabbit-combined\newest-puzzle-9.9.26\` (files, photos, stickers, video_files, voice_messages). An identical-size copy is at `E:\rabbit-combined\rabbitv4\telegram-export-9.9.26\`.
- Community group media (~359 MB): `E:\rabbit-combined\New folder\` (files, photos, stickers, video_files).
- `telegram/sourcebooks/MEDIA_REVIEW.md` summarises the media that was reviewed.

## Integrity notes

- **Original folders were not modified.** Everything here is a copy.
- One exception: running `node .\PUZZLE-REVIEW\session-recovery-check.cjs` during the review regenerated `E:\rabbit-combined\read\PUZZLE-REVIEW\session-recovery-check.json`. Its output is deterministic.
- The only file deleted was a misnamed copy that I had made inside this folder myself (an unrelated OFAC notice XML).
- `prior_research_ledgers/` files are verbatim copies. Their paths (`E:\rabbitv4`, Desktop, …) are stale.
- 2026-09-13 session-log review: `reference_texts/prize_address_dossier.txt` was replaced by the newer rabbitv4 copy (it still lists four solved marker addresses as unknown; see 01 §9). 01–05 were corrected and 06 added. No source folders or outside workspaces were modified, and nothing from them was copied.
- 2026-09-14 critical review and closed-system reset: added `14_CRITICAL_REVIEW_2026-09-14.md`, `15_CLOSED_SYSTEM_RESET_2026-09-14.md`, the `tools/audit_*` scripts including `audit_architect_differential.py` and `audit_matrixsum_lastwords.py`, and their `runs/2026-09-14_*` evidence directories. Additive corrections were applied to `README.md`, `03_OPEN_LEADS.md` (§1, §3, §4), `06_SESSION_LOG_REVIEW.md` (§7), `12_WHOLE_PUZZLE_DIRECTION_AUDIT.md` (§5) and `14_CRITICAL_REVIEW_2026-09-14.md`. Those files no longer match their entries in the 2026-09-13 `SHA256SUMS.txt` snapshot. `originals/`, `data/` and the outside workspaces were not modified, and nothing was copied in from them.

## Where to push next (details in 03)

**Qualification:** this older list is preserved for provenance. Use 12's source/dependency audit to set current priorities. In particular, do not require L5, impose Terminal-first, or infer that a correct intermediate must open an envelope alone. For retaining and inspecting padding-valid outputs, use `tools/inspect_decrypts.py`; the legacy `check_candidate.py` notable-output behavior is not a complete plaintext acceptance rule.

1. **Colour-primes 479 → Architect PRIVATEKEY at 479.** It has zero free parameters; find the step that uses it.
2. **DBBI as a substituted SHA-256 digest.** Only the `bg` tokenisation gives 64/16. Every candidate run through `check_candidate.py` is checked for it automatically. On 2026-09-13 every string still on disk from earlier rounds and logs was back-checked: 0 matches (`runs/2026-09-13_l5_backcheck/`, stopped at 4,443/4,444 jobs). New answers must come from a new idea, not old lists. The pinned "last words before archi choice" referents and the L1/L2 prime sum lists were also checked as literal answers: null (09 §3).
   - Next idea: treat matrixsumlist and last-words as *operations*. A yellow/blue × prime selection on the DBBI matrix gives a sum list; decode or index it to *extract* the last words (09 §4). Its direct form, row/column sums (`runs/2026-09-13_matrixsum_pipeline/`), was tested on 2026-09-13 against shuffled-input controls: null (09 §5). Diagonal, ring, block and modular readings, and sum lists used as cipher keys, are still open.
3. **Primes and "zeroing"** applied to DBBI/FAED (#8000, #8330), then the SalPhaseIon `shabef…` literals as instructions for what to hash.
4. Treat the **Terminal** envelope (64–79 B plaintext) as the likely next door (#2918, #8569). Treat yin yang / Cosmic Duality as the last phase (#9599, #39237). Both are unproven. Several Terminal "nulls" from outside workspaces are void (06 §1).
5. From the session logs (06 §3): the ZERO construction on the DBBI prime grid and the seven-key Bifid have the best-controlled odds. ZERO's direct materials were envelope-tested on 2026-09-13 with a clean null (`runs/2026-09-13_zero_envelopes/`); only its use as an instruction on other material is still open. The seven-key Bifid (every round output, BAR/CAN/FEE word forms, the keys themselves, with 200 shuffle controls) was also envelope-tested on 2026-09-13 with a clean null (`runs/2026-09-13_seven_key_bifid/`). "Follow the white rabbit" is a creator-named first hint for `firsthintisyourlastcommand`.
6. Cheap answer check: hash a candidate answer and derive its compressed address. Three dust-marker addresses were made this way, and a fourth from the bit-reversed URL (01 §9, 06 §2).
