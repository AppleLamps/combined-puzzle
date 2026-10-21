# Adversarial reanalysis of the GSMG research state — 2026-09-14

Directory: `E:\rabbit-combined\GSMG-CLEAN\runs\2026-09-14_adversarial_reanalysis\`
Nothing outside this directory was modified. Corrections to earlier documents are in `ERRATA.md` here.

Contents: §1 method · §2 evidence-status table · §3 ranked mistakes and missing interpretations · §4 dependency map ·
§5 three explanations (A–G) · §6 experiments, results, reproduction · §7 final answer.

---

## 1. What was done, and what was not

Read directly this session (not from inventories): `README.md`, `01`, `02`, `04`, `05`, `08`, `09`, `10`, `11`, `12`;
`data/*` (all files, byte-level for the plaintexts and envelopes); `originals/pages/phase2_choice.html`,
`puzzle_20201109.html`, `theseedisplanted.html`; `originals/poster/puzzle.png` (pixel-sampled); the Scott and kedri
Architect transcripts; `telegram/ChatExport_2026-09-13_result.json` for every message id cited below (verbatim);
`reference_texts/community_github_readme_snapshot.md` (first 60 lines only); the run directories named in the task;
`prior_research_ledgers/rabbit_r1/FINDINGS_round1.md` (firsthint sections); and the source of eight `tools/audit_*.py` scripts.
The outside workspaces `E:\rabbit-combined\`, `D:\downloads-8.8\puzle-main\`, `D:\puzle\`, `D:\astra\` were confirmed to exist
but were **not read** beyond that; nothing below relies on them.

Three bounded computations were run, each with a spec written before execution and every output retained:

| exp | question | verdict |
|---|---|---|
| 0 | Can the poster spiral, both DBBI parses, the marker-prefix matches, L1 (479/484) and L2 (`hillfexmgsgq`) be reproduced from `puzzle.png` + `DBBI_91.txt` without workspace code? | all reproduced |
| 1 | Re-run the six audit scripts' dead address oracle (keys-vs-values bug) over their 38,615 retained candidates with a correct hash160-set oracle and planted controls through the production loop | controls 42/42; 0 hits |
| 2 | "sha256: our first hint is your last command": bounded source-based candidate set × 3 representations × 2 KDF profiles × 3 envelopes, harness validated on Phases 2/3/3.2 first | harness valid; 900 decrypts; 1 chance-level pad; 0 key hits |

No broad cipher sweep was run.

---

## 2. Evidence-status table

Status meanings: **VERIFIED** = reproduced this session from primary material; **HYPOTHESIS** = consistent, not established;
**CONTRADICTED** = contrary evidence found; **NOT TESTED** = no valid test on record; **TEST INVALID** = a test was run but cannot have failed.

| # | claim | status | basis (this session) |
|---|---|---|---|
| 1 | Poster 14×14, spiral from top-left going down, counter-clockwise; black/blue = 1, white/yellow/off-white = 0 → `gsmg.io/theseedisplanted` | VERIFIED | exp0: unique spiral among 4 corners × 2 senses × 4 start directions × both orders × every colour subset. Tail bits after byte 24 are `0000` |
| 2 | Coloured cells along the spiral: `BBBBYBBBYYBBBBYBBYYB O YYBY` (15 blue, 9 yellow, 1 off-white rgb(254,254,254) at row 7 col 4, spiral index 163) | VERIFIED | exp0. `data/verify_log.txt:2` (blue=15, yellow=9 over the 24 regular cells) is correct |
| 3 | Phase 1 answer, #225 digest, Phase 2 `causality`, Phase 3 seven-part password, Phase 3.2 password and all three plaintexts (byte-exact) | VERIFIED | exp2 harness validation: three decrypts equal `data/phase*_plaintext.bin`; one-digit-changed negatives fail; MD5 profile does not open any of them |
| 4 | Envelope boundaries: Terminal = last two 64-char lines of Phase 3.2 plaintext (96 B, salt `b45a5e3d827593ca`); SalPhaseIon short = b64 `[895:959]`+`[999:1063]` (96 B, salt `3ab585348552415d`); Cosmic 1344 B, salt `2d3f6fe06dc950e6` | VERIFIED | decoded and hashed this session; hashes in `exp2_first_hint_last_command/run.log` |
| 5 | DBBI has exactly two prime-slot parses: 83 cells (15 b + 8 be, 60-char payload) and 84 cells (16 b + 7 be, 61-char payload = 60 + `e`) | VERIFIED | exp0 `parses()` enumerates all consistent parses: count = 2 |
| 6 | 83 tokens prefix-match the serial marker string (off-white read as blue) leaving `BY` unused; 84 tokens prefix-match the per-byte string leaving `Y` unused | VERIFIED | exp0. Both readings leave at least one poster marker unconsumed |
| 7 | L1: 24 regular markers vs primes 2..89 → yellow 479, blue 484 | VERIFIED (as arithmetic) / HYPOTHESIS (as meaning) | exp0. It uses only the poster; it is not tied to either DBBI endpoint |
| 8 | L2: 84-cell signed slot values, 7×12 column sums mod 26 → `hillfexmgsgq` | VERIFIED (as arithmetic) / HYPOTHESIS (as meaning) | exp0. Depends on the 84 parse and on the 7×12 shape, which is chosen, not derived |
| 9 | 84-cell b/be split (16/7) equals the Architect/film numbers 23/16/7; 83 gives 15/8 | VERIFIED (arithmetic, new) | exp0. See §3 item 2 and §5 E1 |
| 10 | Architect replacement table: 22 shared edit rows; the extra rows in→TO and then→THAN are kedri-transcript artefacts | VERIFIED | checked against both transcripts directly (kedri "quicker then the others"; Scott "quicker than"; kedri "inherent in the programming") |
| 11 | Six 2026-09-14 audit scripts' "0 marker/prize address hits" | TEST INVALID | membership tested against dictionary keys (addresses) — see `ERRATA.md` E1 with lines |
| 12 | The same null, over the same 38,615 candidates, with hashed derivations | VERIFIED null | exp1 (valid oracle, planted P1–P6 and N1–N3 recovered/rejected through the production loop, 476,912 unique scalars, 0 hits) |
| 13 | `audit_structural_key_formats.py` rescan "closes" the key-format question for those outputs | CONTRADICTED (as a closure) | it never hashes a candidate; exp1 supplies the missing derivations |
| 14 | Earlier firsthint sweeps (8,004 / 15,060 / 540) exclude "first hint = last command" | NOT TESTED (as recorded) → now VERIFIED null for the bounded family in exp2 | earlier runs used raw-only key oracles, printability gates and retained no outputs (round 1 lines 1594-1600; `04` §G) |
| 15 | Poster colour-bit semantics (blue replaces a 1, yellow replaces a 0, off-white is a 0) | VERIFIED (as pixel fact) / NOT TESTED (as an instruction) | no workspace model uses the *bit value* a marker sits on; both DBBI models use only its colour and order |
| 16 | "SELECT FROM OVER TWENTY-THREE CIPHERS SIXTEEN ENCRYPTIONS AND OR SEVEN INTERTWINED PASSWORDS" | VERIFIED text | `01:112`, `data/architect_plaintext_readable.txt`. Film: "select from the matrix 23 individuals, 16 female 7 male". The creator replaced "the matrix" with "OVER" and the nouns |
| 17 | The 479/484 "balance" is confirmed | HYPOTHESIS | it is one arithmetic on one marker string; nothing downstream consumes it |
| 18 | The HTML textarea spacing carries boundary information | CONTRADICTED | uniform single spacing (checked pre-compaction) |
| 19 | Telegram ids cited in `08`/`09`/forward reports (#225, #866/867, #879, #881, #1710, #3389/3390, #4096–4105, #5717, #5952–5977, #6250, #6491–6514, #6712, #7914, #8000, #8330, #8446, #8566–8569, #9605–9607, #11247–11249, #12653, #16624, #20222–20224, #24071, #33445, #66586–66588) | VERIFIED | quoted from the export; wording matches the citations |
| 20 | #8446 bit-reversed bytes decode to the reversed string "yellowblueprimes matrixsumlist lastwordsbeforearchichoice yinyang wewontgiveaway thepassword…" | VERIFIED | reproduced |

---

## 3. Ranked mistakes and missing interpretations

Ranked by how much they change what can be claimed. Paths are absolute.

1. **Dead address oracle in six audit scripts (TEST INVALID).**
   `E:\rabbit-combined\GSMG-CLEAN\tools\audit_m4_zeroing_oracles.py` lines 86-87 (dict `{address: hash160}`) and 252-256
   (`hh in TARGET_H160`); `audit_pointer_selectors.py` 157/218; `audit_board_shape_sums.py` 127/162; `audit_colour_selectors.py`
   164-167/200; `audit_keyed_faed.py` 139-142/175; `audit_tail_cipher.py` 160-163/194. Each self-test goes through a different
   path (`addresses(k)['compressed'] == MARKER_ADDRS[i]`), so the self-tests pass while the production loop can never hit.
   The reports built on them state "0 marker/prize hits" as a result. Fixed by exp1: the null is now real for those corpora.
   `tools/check_replacement_outputs.py` and `tools/audit_structural_key_formats.py` build the dictionary correctly.

2. **The 23/16/7 census was dismissed as "not a prediction".**
   `E:\rabbit-combined\GSMG-CLEAN\runs\2026-09-14_dbbi_forward_comparison\REPORT.md` line 152: "preferring 84 merely because
   23/16/7 appears elsewhere cannot supply that prediction." That is wrong in a narrow, checkable sense. The Architect line
   gives three integers. Under the prime-slot grammar the token count is 23 in *both* parses, so "23" cannot discriminate; but
   the b/be split is 16/7 for 84 and 15/8 for 83 (exp0). The final poster marker (B in the per-byte string, Y in the serial
   string) is exactly the endpoint-dependent information the report says a discriminator must predict, and the Architect
   numbers predict it as B (= b, 84). This is a one-bit prediction, so its evidential weight is small (about 1 bit, with the
   caveat that the 16/7 assignment "b = encryptions, be = passwords" is itself a choice). It is nevertheless the only place in
   the material where the endpoint is *predicted by an independent field* rather than fitted, and the report should say so.

3. **The marker semantics that the poster itself establishes are unused.**
   The poster's only proven function is the URL, and in it the colours have bit values: blue sits on 1-cells, yellow on
   0-cells, off-white on a 0-cell (exp0; `data/verify_log.txt:1`; community readme). Both DBBI models consume only the colour
   *sequence* and slot primes. No workspace model or run treats the marker as (bit value, position) or uses the 8-bit URL
   byte the marker modifies. This is a representation the source establishes and the research never tested (see §5 E3).
   `runs/2026-09-13_offwhite_alignment/` records the off-white cell's *position* but not its bit role.

4. **"OVER TWENTY-THREE" was not analysed as a count claim.**
   The creator replaced the film's "the matrix" with "OVER" (`01_PROVEN_CHAIN.md:112`). Both DBBI parses leave poster markers
   unused (`BY` or `Y`; exp0), i.e. the poster holds *more than* 23 markers (24 regular, 25 with off-white). "Over twenty-three"
   is consistent with the poster being the "select from" set and with the unused markers being intentional, not leftovers.
   No document records this reading; `runs/2026-09-14_dbbi_forward_comparison/REPORT.md` treats the unused markers only as a
   model-fit residue.

5. **Firsthint sweeps recorded as excluding a reading, without retained outputs.**
   `04_DEAD_ENDS_TESTED.md:52` ("firsthint SHA×1–8 | 8,004") and `:81` ("G2. First hint | 15,060"); round-1 ledger lines
   1594-1600 admit the printable-ASCII acceptance rule was wrong. Nothing on disk lets a reviewer re-inspect those decrypts.
   exp2 replaces the source-supported core of that family with a retained, validated run (§6).

6. **The structural-key rescan was described as covering the key-format question** (`runs/2026-09-14_structural_key_formats/REPORT.md`)
   although `tools/audit_structural_key_formats.py` derives scalars only from raw/hex/WIF/base64/decimal tokens and never from
   `sha256(candidate)`, the one derivation that produced every solved marker. exp1 covers it.

7. **Transcript-dependent edit rows.** Already correctly flagged in `runs/2026-09-14_aligned_replacement_v2/REPORT.md`; confirmed
   independently. Not a mistake, but any table that counts 24 rows (kedri) must be treated as containing two non-puzzle rows.

8. **Minor: my own pre-compaction tally "16 B + 8 Y + 1 O" was wrong;** the poster has 15 B + 9 Y + 1 O (exp0, and `verify_log.txt:2`).
   Recorded so it is not propagated.

Items the task said not to re-report as discoveries were checked and are not claimed: direct poster sums vs 60-char payload;
the 320-comparison FAED-margin test; 82 shared cells; DBBI−VIC tail; Bifid prefix; final `e` in the HILL construction; low IoC.

---

## 4. Dependency map

Legend: **V** verified link, **C** conjectured link, **×** no link established.

```
poster.png ──V── spiral bits ──V── gsmg.io/theseedisplanted ──V── Phase 1..3.2 chain ──V── Phase 3.2 plaintext
   │                                                                                        ├─V─ Architect block (1,539 letters) ──V── replacement table (22 rows)
   │                                                                                        ├─V─ 149-digit checkerboard ──V── Half/Better-Half message ("as wide as the first one seen")
   │                                                                                        └─V─ Terminal envelope (96 B)      ──×── password
   ├─V── 24 regular markers (15 B, 9 Y) + 1 off-white
   │        ├─V── L1 479/484 (arithmetic only)            ──×── any consumer
   │        ├─C── serial83 marker string ──C── DBBI 83 parse (unused BY)
   │        └─C── per-byte84 marker string ──C── DBBI 84 parse (unused Y) ──C── L2 hillfexmgsgq (7×12 chosen)
   │                                                        └─V── b/be split 16/7 = Architect "SIXTEEN … SEVEN" (83 gives 15/8)
SalPhaseIon page ──V── 1075-char stream
   ├─V── DBBI[0:91] ──V── exactly 2 prime-slot parses
   ├─V── "matrixsumlist"[91:195] (binary label)   ──C── names an operation on DBBI/FAED; object not identified
   ├─V── FAED[195:765] (570 digits)                 ──×── DBBI (every tested relation excluded by length or null)
   ├─V── "lastwordsbeforearchichoice" ──C── Architect scene ("Which door?" region) ──×── password
   ├─V── "thispassword" ──C── refers to the following material
   ├─V── "shabef ourfirsthintisyourlastcommand" ──C── sha256 of some "first hint" is the final step ──V(null)── exp2 bounded family
   ├─V── b64[895:959]+[999:1063] = locked_salphaseion_short.bin (96 B) ──×── password
   ├─V── "enter"[959:999] (binary label between the two b64 halves)
   └─V── "shabefanstoo" (sha256 answers too)
Cosmic Duality (1344 B) ──×── any of the above (no dependency established either way)
Architect film numbers 23/16/7 ──V── text edit "OVER … CIPHERS … ENCRYPTIONS AND OR … INTERTWINED PASSWORDS" ──C── DBBI token census
```

What is *not* established: any password dependency between the Terminal envelope and the SalPhaseIon short envelope; that
either short envelope precedes Cosmic; that FAED and DBBI are related by any tested operation; that "matrixsumlist" refers
to column sums of a DBBI matrix at all. Source containment (Terminal inside Phase 3.2; SalPhaseIon short inside the
SalPhaseIon page) is verified; discovery order is a community fact; password dependency is conjecture everywhere.

---

## 5. Three materially different explanations

### E1 — The Architect census fixes the DBBI endpoint at 84 cells

- **A. Source instruction.** Architect block (Phase 3.2 plaintext): "SELECT FROM OVER TWENTY-THREE CIPHERS SIXTEEN ENCRYPTIONS
  AND OR SEVEN INTERTWINED PASSWORDS" (`01_PROVEN_CHAIN.md:112`; the creator's edit of the film line).
- **B. Input object.** `data/DBBI_91.txt` under the prime-slot grammar (b or be in prime slots).
- **C. Representations.** Token census only: count of `b` tokens and `be` tokens per parse; no shape, no sums.
- **D. Operation.** Enumerate all consistent parses (exp0: two). Read `b` = "encryption", `be` = "intertwined password"
  (the two-letter token being the "intertwined" one).
- **E. Prediction.** Exactly one parse has 16 b and 7 be. exp0: the 84-cell parse. The 83 parse has 15/8.
- **F. Decisive test.** It has already run and could have failed (e.g. 14/9 for both). What remains falsifiable: the assignment
  direction. If a later construction needs `be` = 16 and `b` = 7, E1 is wrong. Also falsifiable through the poster: under 84 the
  per-byte string leaves one `Y` unused; "OVER twenty-three" then means 24 markers — consistent; under 83 the serial string
  leaves `BY` (25 markers incl. off-white) — also "over", so this does not separate them.
- **G. Not a duplicate.** The forward-comparison report considered 23/16/7 and rejected it as not predicting the endpoint;
  it did not compute the split. This is the computation.

Support gained by 84: about one bit, conditional on the b/be↔encryption/password reading. It does not open anything.

### E2 — "sha256: our first hint is your last command" names a concrete final action

- **A. Source instruction.** SalPhaseIon `[860:895]` `shabefourfirsthintisyourlastcommand` = sha256 + "our first hint is your
  last command" (letter-digits b=2, e=5, f=6 are the page's own convention; `08:18,29-30`). Creator reply to a hint request on
  this exact line: #20224 🤐 (a refusal, i.e. the line is meaningful and not to be explained).
- **B. Input object.** The candidates the material itself supports as "our first hint": #225 digest / Phase 1 answer;
  #867 "giveit = givetit" (first thing the creator called a hint); "Follow the white rabbit" (forward #11248; poster file name);
  the poster's own decode `gsmg.io/theseedisplanted`; the #1710 poem as a control; the SalPhaseIon literals themselves.
- **C. Representations.** raw passphrase; sha256hex; sha256hex twice. KDF SHA-256 (proven) and MD5 (declared second profile).
- **D. Operation.** OpenSSL Salted__ AES-256-CBC decrypt of each of the three envelopes; PKCS#7 check; key recogniser
  (sha256 / sha256d / raw 32-byte windows / hex64 / decimal / stripped-text sha256 → hash160 set of the five targets).
- **E. Prediction.** One envelope opens to language or a structured key.
- **F. Decisive test.** exp2 (§6). Result: 900 decrypts, one valid pad of length 1 (chance expectation 3.5), printable ratio
  0.36, no key. **The bounded family fails.** What is not excluded: a "first hint" outside this list, a different join
  (e.g. answer + `enter`), or a non-OpenSSL container.
- **G. Not a duplicate.** The earlier 8,004/15,060/540 sweeps had raw-only oracles, a wrong acceptance rule and no retained
  outputs; this run is validated end-to-end and every output is on disk for re-inspection.

### E3 — The poster markers carry (bit value, position), not just colour order

- **A. Source instruction.** The poster's only proven reading: black/blue = 1, white/yellow/off-white = 0 (`verify_log.txt:1`;
  community readme; exp0 unique spiral). #1710: "Yellow has a number and so does Blue." #8446 reversed text: "yellowblueprimes".
- **B. Input object.** The 25 coloured cells with, for each: spiral index (0-based), URL byte index and bit index within the
  byte, the bit value it carries (blue → 1, yellow/off-white → 0), and colour.
- **C. Representations.** Exp0 gives all of these; the untested ones are the bit values and the in-byte bit positions
  (0-based or 1-based, MSB- or LSB-first), and the off-white cell as a 0 that *looks* like a marker.
- **D. Operation (family, deliberately narrow).** Read the marker sequence as a 24- or 25-bit word (blue=1, yellow=0, off-white=0
  or excluded); read the in-byte bit positions as a digit sequence; compare each against DBBI's prime-slot tokens (b/be) and
  against the 84-vs-83 endpoint. The one relation that would matter: whether the DBBI `b`/`be` schedule equals the marker
  *bit values* rather than the marker colours — under blue=1/yellow=0 these are the same sequence, so E3's discriminating
  content is the off-white cell: as a 0-bit it reads as yellow-like (`be`), as a "blue-ish" mark it reads as `b`.
- **E. Prediction.** If the off-white cell is a 0-bit marker, the serial string becomes `…BBYYB Y YYBY` (off-white = Y): 23 tokens
  would then need to prefix-match `BBBBYBBBYYBBBBYBBYYBYYY`. exp0 shows neither parse has that token string (83 ends `BBYY`,
  84 ends `BYB`), so **read by its bit value the off-white cell is not a token under either parse**. It can be a token only if
  it is read as blue (`b`) despite sitting on a 0-bit, which is what the serial-83 string does. The per-byte (84) model instead
  folds it into its byte as a 0. So E3 collapses to: the bit-value reading and the serial-83 reading contradict each other;
  the bit-value reading and the per-byte-84 reading do not.
- **F. Decisive test.** Computed in exp0 (the parse enumeration is exhaustive). It could have failed: a parse ending `BYYY`
  would have made the off-white cell a live token.
- **G. Not a duplicate.** `2026-09-13_offwhite_alignment` located the cell; no run asked whether its *bit value* is consistent
  with it being a token.

E3 therefore gives the 84 side a second, weak, independent nudge (off-white is a 0-bit and no parse admits it as a token), but
it is not an instruction and it produces no new field.

---

## 6. Experiments: results and reproduction

All commands from `E:\rabbit-combined\GSMG-CLEAN\runs\2026-09-14_adversarial_reanalysis\`.

### exp0 — reproduction (`exp0_reproduction/`)

```bash
cd exp0_reproduction && python repro_dbbi_parse.py
```

Outputs `repro_dbbi_parse.json`. Key values: spiral TL/ccw/start-down/ones={K,B}; 25 coloured cells; parses = 2;
83 → 15 b / 8 be, payload `difhccgihaeeihggegebgehhehhfafdhffcdbfcccgfeggecdcifffgigeea`; 84 → 16 b / 7 be, payload + `e`;
L1 yellow 479 / blue 484 / total 963; L2 7×12 `hillfexmgsgq`.

### exp1 — valid address oracle over the retained candidate corpora (`exp1_address_oracle_rerun/`)

```bash
cd exp1_address_oracle_rerun && python rerun_address_oracle.py
```

Spec: `SPEC.md` (written first). Inputs and their SHA-256: `manifest.json`. Controls: `controls.json` — 42/42
(6 positives × 7 files recovered by line number; 3 negatives × 7 files rejected). Real corpora: 7 files, 38,615 rows,
476,912 unique scalars, **0 hits** (`results.json`, `hits.jsonl` empty), 147.6 s. First run voided (dedup suppressed two
planted controls) and retained as `run_v1_voided.log` / `controls_v1_voided.json`.

### exp2 — first-hint-as-last-command, validated harness (`exp2_first_hint_last_command/`)

```bash
cd exp2_first_hint_last_command && python run_exp2.py
```

Spec: `SPEC.md` (written first). Harness validation (in `run.log`): Phase 2 (672 B ct, salt `06286612d43ed7ed`), Phase 3
(4112 B, `9fbc451d13d071f4`), Phase 3.2 (2448 B, `eefc4c5befc1656a`) all decrypt byte-exact to `data/phase*_plaintext.bin`
under the SHA-256 profile; one-digit-changed passwords fail; the MD5 profile opens none. Recogniser positives (Phase 1 answer →
marker_phase1; embedded raw 32-byte key at offset 2) and negative pass.

| candidates | decrypts | pad-valid | expected by chance | key hits | seconds |
|---:|---:|---:|---:|---:|---:|
| 50 | 900 | 1 | 3.5 | 0 | 107 |

The single pad-valid output (idx 19: "Follow the white rabbit" raw passphrase, SHA-256 profile, SalPhaseIon short) has pad
length 1 and printable ratio 0.36; it is chance-level. All 900 raw outputs are in `outputs/` (named by index, family,
representation, KDF, envelope); per-row metadata in `results.jsonl.json`; `summary.json` carries input and code hashes.

Unfinished branches: none within the spec. Not attempted (outside spec): joins such as answer+`enter`, non-OpenSSL containers,
other KDF iteration counts.

---

## 7. Final answer

**What was missed.** Three things, none of which is a password:

- The Architect census 23/16/7 *does* predict the DBBI endpoint: only the 84-cell parse has 16 `b` and 7 `be`. The
  forward-comparison report rejected this without computing the split.
- The poster's own bit semantics were never applied to the markers. Doing so shows that the serial-83 string needs the
  off-white 0-bit cell to be read as blue, while the per-byte-84 string does not; the bit-value reading is consistent only with 84.
- "OVER twenty-three" fits a poster with 24/25 markers of which 23 are selected; the unused markers may be intentional.

**Conclusions to withdraw.** The "0 marker/prize hits" statements of the six audit scripts listed in §3.1 (test could not fail);
the claim that the structural-key rescan closed the key-format question; the "not a prediction" sentence at
`dbbi_forward_comparison/REPORT.md:152`; the standing of the old firsthint sweeps as exclusions. Details in `ERRATA.md`.
The 38,615-candidate null itself survives on a valid test (exp1).

**Does either endpoint gain independent support?** 84 gains two weak, independent nudges (the 16/7 split; the off-white cell's bit value
is consistent with the per-byte reading and not with the serial one). Neither is decisive, and both depend on a reading choice. 83 gains nothing new. The fork is not resolved.

**Did a complete new instruction, field, password or key emerge?** No. exp2's source-based "first hint" family fails under a
validated harness with full retention; exp1 confirms no retained candidate is a key.

**Single best next step.** Build the one construction that uses the 84 endpoint *and* consumes the poster's leftover `Y` and the
final `e` together, then test it against the Terminal and SalPhaseIon-short envelopes with the exp2 harness. Concretely: treat
the 23 selected markers plus the one unselected as "select from over twenty-three", derive the selection as a 23-of-24
mask, and use that mask (not the colour order) as the operation applied to FAED or to the Architect edit rows. That is the
smallest test that ties the three fields that currently have no verified link (poster leftovers, DBBI endpoint, FAED) into a
single falsifiable prediction.
