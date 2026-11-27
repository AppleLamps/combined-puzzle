# Cosmic Duality null validity audit — 2026-11-27

**Lead.** Of the 16 recorded families that claim a null against Cosmic Duality, **5 are VALID, 1 is
PARTIAL and 10 are INVALID** under the pinned key-derivation profile. **3,461 gap candidates** from 5
source-grounded families were carried into a preregistered replay; 6 more recorded families are listed
with the reason they were not carried. Result of the replay: **null** — 3,461 candidates × 3 envelopes,
0 notable, no pad ≥ 3, no key, no unity-of-opposites text.

Nothing was opened. No new password family was created. Every candidate string came out of a file
already in the repository.

## 0. The profile, and what counts as a test of Cosmic

Pinned profile (authenticated on Phases 2, 3 and 3.2 by `tools/verify_chain.py`):

- passphrase = lowercase hex of `sha256(answer)`, as 64 ASCII bytes
- OpenSSL `EVP_BytesToKey` with **SHA-256**, 1 iteration, key and IV from the same stream
- AES-256-CBC, salt = bytes 8:16 of the `Salted__` blob
- strict PKCS#7 on the full plaintext

The MD5 profile opens none of the three proven envelopes
(`runs/2026-09-14_adversarial_reanalysis/REPORT.md` row 3; re-derived in
`runs/2026-11-27_kdf_model_widen/REPORT.md` §2). **An MD5-only result is therefore not a test of Cosmic
Duality**, and neither is a raw-32-byte passphrase, a printable-ASCII gate, or a run whose plaintexts
were thrown away.

The envelope audited: `data/locked_cosmic_duality.bin`, 1,344 B, salt `2d3f6fe06dc950e6`, ciphertext
1,328 B, SHA-256 `b18950551a4dd0cb8a9378f0906ba18c03a15f0ee83eb98c6bc90165c5f79805`.

**Verdict rule used below**, fixed before the table was filled:

| verdict | requires |
|---|---|
| **VALID** | SHA-256 digest *and* the hex convention both present, strict PKCS#7 acceptance, every pad-valid output retained and re-inspectable, a control that fired through the same loop, harness validated on the authenticated chain (Phase 3.2 at minimum) |
| **PARTIAL** | SHA-256 + hex present, but one leg missing (no through-loop control, or no chain validation) |
| **INVALID** | any of: MD5-only for the Cosmic cells, raw-only passphrase, printable-gated acceptance, plaintexts not retained, or a documented bug (`ERRATA.md` E1–E4, the B1 half-blob bug) |

Two consequences of the rule are deliberate. Padding is not evidence: a wrong key passes PKCS#7 about
1/256 of the time (05 §1, 14 §M6), so a family is only VALID if its pad-valid outputs can still be
read. And a family is only VALID for Cosmic if the *Cosmic* cells ran under SHA-256 with the hex
passphrase — an MD5 cell that produced a "decrypt" is a bug, not a test.

## 1. Inventory

One row per family. "Claimed scope on Cosmic" is what the record says, not what it proves.

| # | family | recorded in | claimed scope on Cosmic | verdict |
|---|---|---|---|---|
| 1 | ZERO prime-schedule family (arms A–C: 8,163 + 5,076 + 944 texts) | `runs/2026-09-13_zero_envelopes` | 194,382 AES-CBC; 762 pad-1 + 3 pad-2; 0 pad ≥ 3; 0 keys | VALID |
| 2 | Seven-key Bifid BAR/CAN/FEE (59,976 texts) | `runs/2026-09-13_seven_key_bifid` | 1,079,568 AES-CBC; real DBBI 28 pad-valid of 6,408 vs 25.1 expected; 0 pad ≥ 3; 0 keys | VALID |
| 3 | Last-words referents (15,676 strings) | `runs/2026-09-13_last_words_referents` + `runs/2026-09-13_recheck_755` | 188,112 trials; 750 pad-1 / 5 pad-2 vs 734.8 / 2.87 expected; 0 keys | VALID |
| 4 | #8446 matrix-sum pipeline (4,677 outputs, 9,236 text forms) | `runs/2026-09-13_matrixsum_pipeline` | 110,832 trials; pad histogram {0: 110,394, 1: 437, 2: 1}; 0 keys | INVALID |
| 5 | "our first hint is your last command" (50 source strings) | `runs/2026-09-14_adversarial_reanalysis/exp2_first_hint_last_command` | 900 decrypts; 1 chance pad-1; 0 keys | VALID |
| 6 | Six SalPhaseIon answers hashed (32 cells) | `runs/2026-11-27_cosmic_six_hash` | 32 decrypts; 0 valid PKCS#7; printable 0.345–0.397 | VALID |
| 7 | Saved step-2/3/4 strings × 3 KDFs (19,106 strings) | `runs/2026-11-27_kdf_model_widen` | 57,318 tests per KDF/IV cell; pad ≥ 1 at chance; 0 pad ≥ 3; 0 structured | INVALID |
| 8 | 5g-puzzle packets 1–4 (55 frozen strings) | `5g-puzzle/packet/RESULTS*.md`, `AUDIT.md` | "no decrypt" for yinyang / Cosmic Duality names; 3 PKCS#7 successes on the 79-byte Salph fragment | INVALID |
| 9 | 5g-puzzle audit packet (199 frozen strings, 4 KDFs) | `5g-puzzle/packet/run_kdf_audit.py` | 4,776 attempts; 25 PKCS#7 successes, all pad 1; 0 readable, 0 prize | INVALID |
| 10 | SalPhaseIon pre-registration v1–v22 (11,864 passwords, 3,735 preimages) | `puzle/gsmgio-5btc-puzzle-master/SALPHASEION_PREREGISTRATION.md` | 71,184 decrypts; 253 strict-padding hits vs 279 expected; 80 on Cosmic, all pad 1; 0 accepted | INVALID |
| 11 | Seven intertwined passwords, raw-phrase reading (v49) | `puzle/docs/ATTEMPT_LOG.md` §14e | 386,794 passwords, 3,094,352 attempts; 12,132 padding hits (0.392%); 0 legible | INVALID |
| 12 | sha256-format passwords + braid/zip intertwines (v50-A, v50-B) | `puzle/docs/ATTEMPT_LOG.md` §14e; `intertwined_password_coherence_audit.json` | A: 840 attempts, 5 pad; B: 4,800 attempts, 23 pad; 0 legible | INVALID |
| 13 | "Unity of opposites" phrase family (10 strings) | `puzle/docs/ATTEMPT_LOG.md` §19; `unity_of_opposites_audit.json` | 240 AES trials; **0 strict-padding hits**; 0 legible | PARTIAL |
| 14 | S570 seven-9×9 fold and its Architect selector use | `puzle/docs/ATTEMPT_LOG.md` §20, §21 | 2,928 + 4,608 AES trials; 18 + 15 padding hits at chance; 0 legible | INVALID |
| 15 | 23/16/7 endgame and cipher catalogue (v56, v57) | `puzle/docs/ATTEMPT_LOG.md` §23, §25 | 13,248 + 528 AES trials; 43 + 2 padding hits at chance; 0 legible | INVALID |
| 16 | Cosmic checkpoint master key (5-token XOR) | `gsmg-haiku/review_leads/CHECKPOINT_4F7A_VS_A5502.md` | MD5/raw reproduces `4f7a1e4e…`; "EVP-SHA256 and the hex-string form give no valid padding" | INVALID |

Not Cosmic claims, and outside this audit (address/digest oracles, or no envelope byte was read):
`runs/2026-09-14_m4_zeroing_oracles`, `2026-09-14_pointer_selectors`, `2026-09-14_board_shape_sums`,
`2026-09-14_colour_selectors`, `2026-09-14_keyed_faed`, `2026-09-14_tail_cipher`,
`2026-09-14_structural_key_formats`, both `prize_gate_rescan` runs, `2026-11-27_key_construction`,
`2026-11-27_prime5_reinsertion`, the 2026-11-10 step-2 runs, and the `gsmg-haiku/review_leads` AES
families (those target the two 96-byte envelopes).

## 2. Validity, read from the code and the artifacts (not from summary lines)

| # | KDF digest(s) actually used | passphrase form | acceptance check | outputs retained | control fired through the same loop | harness validated on 2 / 3 / 3.2 | verdict |
|---|---|---|---|---|---|---|---|
| 1 | SHA-256 **and** MD5 | sha256-hex, raw text, raw digest | strict PKCS#7 on the full block; notable = pad ≥ 3 or key; no printable gate | yes — `results.json` keeps `plaintext_hex` for all 1,027 pad hits | yes — Phase 3.2 opens (pad 10, 2,422 B); planted k=1 found as raw32 and WIF; arm-B loader control reproduced fresh-start's 45 hits | 3.2 | VALID |
| 2 | SHA-256 **and** MD5 | sha256-hex, raw text, raw digest | strict PKCS#7; the text gate is applied afterwards, never as the trigger | yes — every pad-valid hit with a plaintext preview in `results.json` | yes — 200 shuffled DBBIs; Phase 3.2 opens; planted k=1 | 3.2 | VALID |
| 3 | SHA-256 **and** MD5 (4 profiles: `gsmg`, `raw`, `gsmg-md5`, `raw-md5`) | sha256-hex and raw | strict PKCS#7 | **yes, after remediation** — the original run kept counts only (flagged in `2026-09-13_assumption_audit` §1); `recheck_755` rebuilt all 755 pad-valid plaintexts with an independent AES implementation and kept every byte | yes — `check_candidate.selftest()`; 100 random-length control batches; planted k=1 | 3.2 | VALID |
| 4 | SHA-256 **and** MD5 (same 4 profiles) | sha256-hex and raw | strict PKCS#7 | **no** — only the pad histogram and the top-12 outputs per family; the 438 pad-valid plaintexts and their provenance were never written | yes — selftest, 400 shuffled pipelines, planted decodes | 3.2 | INVALID |
| 5 | SHA-256 **and** MD5 | raw, sha256-hex, sha256-hex twice | strict PKCS#7 + address oracle + legibility; every decrypt written first | yes — all 900 raw decrypts in `outputs/` | yes — three authenticated decrypts plus one-digit-changed negatives; MD5 opens none | 2, 3, 3.2 | VALID |
| 6 | MD5 **and** SHA-256 | hex-lower (primary), raw digest, hex-upper, double-sha256 hex | strict PKCS#7; the sentence flag is a note, not the gate | yes — first 200 bytes of all 32 decrypts in `REPORT.md` and `results.json`, printable ratio over all 1,328 bytes | yes — `verify_phase32()` requires pad 10 / 2,422 B under hex+EVP-SHA256 **and** requires MD5 to fail | 3.2 | VALID |
| 7 | MD5, SHA-256, PBKDF2-SHA256×10,000 (two IV modes) | literal, sha256-hex, raw digest | strict PKCS#7 + structured gate (quadgram ≥ −4.6, or ≥ 90% printable ≥ 20 B) | **no** — `results.json` holds counts and the control matrix only | yes — an 18-cell Phase 3.2 matrix in which only hex+EVP-SHA256 opens | 3.2 | INVALID |
| 8 | **MD5 only** (packets 1–4 predate the KDF audit) | raw UTF-8 + sha256-hex | strict PKCS#7, then Half's **uncompressed pubkey only**, over 4 windows | **no** — `packet/out/*.bin` is not committed | the self-test is the retracted MD5 pad-1 Cosmic output `4f7a1e4e…` | none | INVALID |
| 9 | MD5, SHA-1, SHA-256, PBKDF2 | literal + sha256-hex (199 strings) | strict PKCS#7 + shared prize gate (both targets) | **no** — 25 successes kept as `pt_sha256` only; the 120-character preview is emitted only if the whole plaintext is printable (none was) | the self-test is again the retracted MD5 pad-1 `4f7a1e4e…`; no Phase 2/3/3.2 validation | none | INVALID |
| 10 | MD5 **and** SHA-256 | raw + sha256-lowerhex (+ raw digest from v3) | strict PKCS#7 **plus** a frozen readable-text/format validator; "padding alone is never success" | **no** — by design: "padding hits are recorded by hash and metrics only"; no plaintext anywhere | the three blobs are all targets; nothing authenticated is decrypted as a control | none | INVALID |
| 11 | MD5 **and** SHA-256 | **raw only** (v49 never applied the hex format) | printable ≥ 0.85 and entropy ≤ 5.9, or a ≥ 6-letter English run — a legibility gate, no strict-pad reporting | **no** — counts in `salvation_coherence_audit.json` | Phase 3.2 legible-control passes | 3.2 | INVALID |
| 12 | MD5 **and** SHA-256 | sha256-hex, double-hex, raw digest, raw braid/zip | legibility (v49 gate) or a prize-gated 32-byte window | **no** — `intertwined_password_coherence_audit.json` records 5 and 23 padding hits and two empty lists; family B's committed artifact covers 400 passwords / 4,800 attempts while `ATTEMPT_LOG` §14e claims 102,991 materials / 1,235,892 attempts, and no artifact holds that run | none recorded | none | INVALID |
| 13 | MD5 **and** SHA-256 | raw, sha256-lowerhex, raw digest | legibility (`_legible` / `_legible_bytes`) | nothing to retain — **0 strict-padding hits in 240 trials** | none recorded (the module is its own seal) | none | PARTIAL |
| 14 | MD5 **and** SHA-256 | raw, sha256-hex, raw digest | legibility | **no** — counts only (18 and 15 padding hits) | planted scalar control accepted, prize gate rejects | none for the AES legs | INVALID |
| 15 | MD5 **and** SHA-256 | literal, normalised, sha256-hex, raw-32 | legibility | **no** — counts only (43 and 2 padding hits) | Phase 3.2 positive control opens; planted scalar accepted | 3.2 | INVALID |
| 16 | MD5 (reproduction), then **SHA-256 asserted** | raw 32 bytes, then "hex-string form" | strict PKCS#7 | **no** — the scripts are "in the session scratchpad (outside the project)" | the control is the MD5 pad-1 reproduction itself | none | INVALID |



What the table changes, family by family:

- **3 (last-words)** is VALID only because of the remediation. `2026-09-13_assumption_audit` §1 found
  that `check_candidate` treats a plaintext as notable only at pad ≥ 3 or a key hit, so the original run
  kept nothing for pad-1/2 outputs. `2026-09-13_recheck_755` rebuilt all 755 padding-valid outputs from
  the same candidates with `cryptography` instead of PyCryptodome, matched every saved byte and retained
  the full plaintext of each. That family now has the retention the others lack.
- **4, 7, 10, 12, 14, 15** are INVALID on one ground: the plaintexts are gone. Each reports a padding
  count and an empty list of legible hits, but no pad-valid plaintext survives, so a correct 1,328-byte
  text with pad 1 would have been discarded and nobody could tell. Family 10 did this deliberately
  ("padding hits are recorded by hash and metrics only") — defensible as a rule, and still unauditable.
- **8, 9, 16** fail on the KDF or the control. Packets 1–4 are MD5-only, so their "no decrypt" says
  nothing about Cosmic under the pinned profile. The audit packet does run SHA-256 with the hex form, and
  its self-test is the retracted MD5 pad-1 output `4f7a1e4e…` — a control that validates the wrong
  profile. The checkpoint note asserts the SHA-256 and hex-string cells but its scripts live outside the
  repository, so nothing can be re-run or re-read.
- **11** is INVALID twice over: raw-only passphrase, and no retention.
- **13** is PARTIAL rather than INVALID: 10 strings × 3 forms × 2 KDFs × 4 envelopes = 240 trials with
  **zero** strict-padding hits, so there is nothing unretained. What is missing is a control and any
  validation of the decryptor on an authenticated envelope.
- **1, 2, 5, 6** are the four-square nulls: SHA-256 with the hex convention, strict PKCS#7, every
  pad-valid output on disk, and a control that fired through the same code. Families 1, 2 and 6 validate
  on Phase 3.2 only; exp2 (5) validates on Phases 2, 3 and 3.2 with one-digit-changed negatives.

## 3. Gaps

Two classes. **3a** is carried into the replay of §4: the family is source-grounded (creator message or
page offset), its only Cosmic test is PARTIAL/INVALID, and its exact strings can be read out of a
committed file. **3b** is recorded but not carried, with the reason.

### 3a. Carried gap families — 3,461 unique strings

**G1. "Unity of opposites" phrase family (10 strings) — PARTIAL.**
Provenance: the Time-Life *Cosmic Duality* contents-page essay title, plus creator messages #8311
".... That is very specific", #8315 "If the puzzle is solved you'll see how scary specific that is",
#8328 "@barrystyle, provided a very specific hint already" (all replies to the 2022-12-10 photo of the
book cover, #8310), and the point-up endorsement #60285 "Instead we should be turning inward to find the
solution." Strings, exactly as sealed in `unity_of_opposites_audit.json → phrases_sealed`:

`theunityofopposites` · `TheUnityOfOpposites` · `unityofopposites` · `UnityOfOpposites` ·
`unity of opposites` · `the unity of opposites` · `turninginward` · `turninward` ·
`turninginwardtofindthesolution` · `TURNINGINWARD`

**G2. 5g-puzzle frozen packet list (199 strings) — INVALID.** Provenance: the closed list frozen on
2026-09-08 (`packet/password_list*.json`), assembled from the creator's own words and the roadmap —
`yinyang` / `yingyang` (creator #39224 "yinyang not reached, then hours"), the Cosmic Duality names, the
seven pipeline phrases and the SalPhaseIon tokens (#8446; page offsets 91:195, 766:829, 830:859, 959:999,
1063:1075), `HASHTHETEXT`, `THEMATRIXHASYOU`, the two poster pixel counts 50400 / 83700 (#56158,
#56159), the phase-1 answer and its digest (#225), and the two 64-character base64 fields spelled out.
All 199 are reproduced verbatim in `APPENDIX_GAP_STRINGS.md` §2 and are the first 199 rows of
`gapset_v2/gap_candidates.txt`. The distinctive members:

`yinyang` · `yingyang` · `ying yang` · `YinYang` · `YingYang` · `yin yang` · `Yin Yang` · `YINGYANG` ·
`YINYANG` · `cosmic duality` · `Cosmic Duality` · `cosmicduality` · `CosmicDuality` · `COSMICDUALITY` ·
`yellowblueprimes` · `matrixsumlist` · `enter` · `lastwordsbeforearchichoice` · `thispassword` ·
`yourlastcommand` · `secondanswer` · `shabefanstoo` · `HASHTHETEXT` · `SalPhaseIon` · `salphation` ·
`giveit` · `givetit` · `theflowerblossomsthroughwhatseemstobeaconcretesurface` · `THEMATRIXHASYOU` ·
`IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF AND THEY ALSO NEED
FUNDS TO LIVE` · `Are you really looking for just the btc...?` · `Actually, the hardest part is done.` ·
`reinserting the prime basics` · `50400` · `83700` · `5040096791` · `9679150400`

**G3. v50-A "named creator texts" (35 strings → 140 passwords) — INVALID.** Provenance: `_creator_texts()`
in `solver/intertwined_password_coherence_audit.py` — the seven phrases of the 2023-02-23 image (#8446),
the seven SalPhaseIon tokens, the Architect text at 0:479 and 479:end, S91 and S570, the two numeric
label fields, the phase-3.2 answer, the phase-1 answer, `HASHTHETEXT`, and the phrases concatenated 1–4
and 1–7. The seven that anchor the family, in the creator's order (#8446):

`yellowblueprimes` · `matrixsumlist` · `lastwordsbeforearchichoice` · `yinyang` ·
`wewontgiveawaythepassword` · `itsinfrontofyoureyesbutyourenotseeingit` ·
`verylaststepisatruegiveawaypromised`

All 35 are listed verbatim with their internal names in `APPENDIX_GAP_STRINGS.md` §3 (group
`v50 _creator_texts`), e.g. `heisenberg_preimage` =
`jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple`, `tokens_all7` =
`matrixsumlistenterlastwordsbeforearchichoicethispasswordmatrixsumlistyourlastcommandsecondanswer`.

**G4. Cosmic checkpoint master key (1 string) — INVALID.**
Provenance: XOR of `sha256` over five page literals — `enter` (offset 959:999),
`lastwordsbeforearchichoice` (766:829), `thispassword` (830:859), `yourlastcommand` and `secondanswer`
(the two 64-character base64 fields at 895:959 and 999:1063). Exactly one of 32,767 non-empty subsets of
a hand-chosen 15-token pool gives it:

`a795de117e472590e572dc193130c763e3fb555ee5db9d34494e156152e50735`


**G5. SalPhaseIon pre-registration v1–v22, text preimages (3,263 strings) — INVALID.**
Provenance: the candidate manifests themselves, each row carrying its own `provenance` string. The
classes are the ones `SALPHASEION_PREREGISTRATION.md` froze: contiguous runs of the six decoded fields in
page order and with one space between fields; every suffix, sentence and clause of the seven words before
"choice" in the Matrix Reloaded line prompted by `lastwordsbeforearchichoice`; the literal row, column,
row-then-column, column-then-row and total sum lists of S91 at 7×13 and 13×7 and of S570 at 19×30 and
30×19, under both page mappings (a=1..i=9, a=0..i=8) in four serialisations; and the `HASHTHETEXT`
access loop. 3,735 distinct preimages exist; 389 are raw bytes a Python `str` cannot carry and 83 hold a
Unicode line-boundary character, leaving 3,263. The full string-to-provenance map is
`gapset_v2/gap_provenance.tsv`; the appendix shows the first 40 rows and the provenance-class counts.
Examples:

`105 90 125 113 100 81 96 103 103 104 92 102 120 93 84 113 104 101 115 103 101 112 91 80 112 119 114 108 98 97`
— `matrix-sum-list/S570/one-based/19x30/columns/decimal-space-separated`

`105,90,125,113,100,81,96,103,103,104,92,102,120,93,84,113,104,101,115,103,101,112,91,80,112,119,114,108,98,97`
— the same list, comma-separated

`can do to stop it` — `lastwords/…` suffix of the transcript line, and the one that produced a (chance)
pad-1 Cosmic hit in the run below.

### 3b. Recorded PARTIAL/INVALID families not carried, and why

| family | candidates | why not carried |
|---|---|---|
| 4 — #8446 matrix-sum pipeline | 4,677 outputs / 9,236 text forms | no committed candidate file: the strings exist only by re-running `run_pipeline.py` over the poster, DBBI and FAED. Rebuilding 9,236 derived strings is a sweep of a generated enumeration, which the brief forbids; status stays INVALID and is flagged here |
| 7 — saved step-2/3/4 strings | 19,106 | same: selected at run time from saved JSON, no candidate list on disk |
| 11 — v49 raw phrases | 386,794 passwords | no committed list, and raw-only, so a hex replay would be a new form rather than a replay |
| 12 — v50-B braids/zip | 102,991 recorded / 400 committed | no artifact for the recorded scope; replaying 102,991 braids is a sweep |
| 14, 15 — S570 fold, 23/16/7 endgame, cipher catalogue | derived | generated enumerations with no committed candidate list |
| 10 — 389 byte-only and 83 line-boundary preimages | 472 | not expressible as a `check_candidate` answer line; counted here rather than silently dropped |


## 4. The gap run

Step 3 is non-empty, so the gap set was preregistered, controlled and run once.

**Preregistration.** `gapset_v2/PREREG.json`, sealed before any candidate file existed —
`prereg_sha256 35a9c359c89b484f4eceea805c8fddef23932c7c3fe31065357db4bcee0b6cac` — fixing the five
sources, the single profile, the acceptance rule, the two controls and `candidate_bound: 3461`.

**Predicted second artifact** (fixed before the run): if one of these strings is the Cosmic password,
the 1,328-byte plaintext reads as language whose subject is unity of opposites, or its bytes carry a key
that derives `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`. Operationally that is pad ≥ 3 on the 1,328-byte
ciphertext (chance 1/16.8M) or a Half/Better-Half hash160 hit; pad 1–2 at the chance rate is the null.

**Self-check without AES** (`gapset_v2/gap_manifest.json`, recorded with
`prereg.py record --outcome passed`): 3,508 manifest rows → 3,461 unique strings, 47 duplicates; the
candidate file has exactly 3,461 `str.splitlines()` tokens, equal to the declared bound; four sentinel
strings present, one planted absent string not present; every source file's SHA-256 written into the
manifest, and the twenty-two SalPhaseIon manifests still hash to the seals printed in
`SALPHASEION_PREREGISTRATION.md` (v1 `80dcc210…`, v9 `e58643f4…`, v22 `c243f6b0…`).

**Controls.**

- *Tool self-test:* `python tools/check_candidate.py --selftest` → `SELFTEST PASSED (envelope open,
  hash160 of Half pubkey, EC k=1, WIF, raw/hex detectors, pattern helper)`. The envelope leg is the real
  Phase 3.2 envelope, pad 10, 2,422 bytes.
- *Planted control through the same loop:* a byte-identical copy of `tools/check_candidate.py`
  (sha256 `d164ba16d2632d87ee89dcf44451cc0d262441ce5a9f0c821044273713d66f1a`) run against a sandbox in
  which `data/locked_terminal_phase3_2_end.bin` is replaced by a 96-byte synthetic `Salted__` blob whose
  passphrase is sha256("planted control opens here") as lowercase hex. It printed
  `[STRONG pad] terminal_phase3_2_end pad=16 len=64` and `1 candidates x 3 envelopes, profile=gsmg:
  1 notable`. Canonical data was not touched. `make_planted_control.py`, `planted_control.log`,
  `planted_control.json`.

**Void first attempt.** The first sealed statement at this level (seal `f22e5207…`) declared 3,544
candidates and wrote 3,544 lines, but `check_candidate` reads with `str.splitlines()`, which also breaks
on `\v \f \x1c \x1d \x1e \x85 \u2028 \u2029`. 83 strings hold one of those characters, so the tool tried
3,720 tokens instead of 3,544. That run is kept and **not counted**: `VOID.md`, `gap_run.log`. Its numbers
were 0 notable, 0 pad ≥ 3, 0 keys, 47 pad-1 hits (cosmic 16 / terminal 14 / salphaseion 17).

**The run** (one invocation; `gapset_v2/gap_run.log`, 19 KB; `gap_run.err` empty):

```
python tools/check_candidate.py \
  --file runs/2026-11-27_cosmic_null_validity/gapset_v2/gap_candidates.txt \
  --derivation runs/2026-11-27_cosmic_null_validity/gapset_v2 --profile gsmg
...
3461 candidates x 3 envelopes, profile=gsmg: 0 notable
```

| measure | value |
|---|---|
| candidates × envelopes | 3,461 × 3 = **10,383 decrypts**, pinned profile only |
| candidates the tool actually tried | 3,461 (equals the declared bound) |
| notable outputs | **0** |
| pad ≥ 3 | **0** (expected 0.0006) |
| Half / Better-Half hits | **0** |
| DBBI equality-pattern matches | **0** |
| pad = 1 | 45 total: **cosmic 16, terminal 12, salphaseion 17**, against 13.52 expected each (40.6 total) |
| cosmic pad-1 tail probability | Poisson P(X ≥ 16 │ λ = 13.52) = **0.284** |
| every cosmic pad-valid plaintext | 1,327 bytes, pad 1, first 80 bytes binary in all 16 cases — no ASCII run |
| longest / shortest candidate | 1,539 / 1 characters |

The 16 chance-level Cosmic hits came from strings such as `17a17`, `deidhifbfcdii`, `bahdcce`,
`can do to stop it`, `9 8 1 7 6 7 1 4 4 5 2 5 7`, and the Architect `[:479]` slice beginning
`yourlifeisthesumofaremainderofanunbalancedequation…`. Every one decrypts to noise, so padding is the only
thing they share, which is exactly what 1/256 looks like. No preview is language; none reads as unity of
opposites.

**Verdict on the gap set: null, and now retained.** The five carried families have a pinned-profile
Cosmic test whose every pad-valid output is in `gapset_v2/gap_run.log` — the tool's 80-byte preview, its
pad length and its answer, which is the same retention standard applied to families 1 and 2 above (not
`recheck_755`'s full 1,327 bytes). Under the §2 rule their status moves to VALID for the 3,461 strings
carried; the 472 preimages that cannot be written as an answer line (389 byte-only, 83 line-boundary)
stay unaudited and are named in §3b.


## 5. What this audit changes

1. **The Cosmic null is not as weak as the record suggested, but it was overstated in eleven places.**
   Five families (1, 2, 3, 5, 6) were already valid: SHA-256, hex passphrase, strict PKCS#7, outputs on
   disk, controls that fired. Eleven were not — 10 INVALID and 1 PARTIAL — and in every INVALID case the
   failure has the same shape: the plaintexts are gone (4, 7, 10, 12, 14, 15), the KDF or the passphrase
   form is wrong (8, 16), or the control validates the wrong profile (9).
2. **Five source-grounded families with no inspectable Cosmic test now have one** — 3,461 strings,
   replayed once under the pinned profile with the tool's full output retained.
3. **Two record defects are now on paper.** `ATTEMPT_LOG` §14e's family-B numbers (102,991 materials /
   1,235,892 attempts) have no artifact; the committed JSON says 400 / 4,800. And
   `SALPHASEION_PREREGISTRATION.md`'s 253 padding hits are recorded "by hash and metrics only", so the
   family that produced them can never be re-read — a policy, but one that makes 71,184 decrypts
   unauditable.
4. **Nothing about the puzzle moved.** No readable unity-of-opposites text, no Half address, no key, no
   pad ≥ 3. The families still open are named in §3b, each with the reason it was not carried.

What this does **not** establish: that any family is wrong. A null here means "these exact strings, this
profile, retained and re-read" — nothing about strings outside the five manifests, other KDFs, other
containers, or the unfetched remainder of the SalPhaseIon manifests (the 472 preimages of §3b).

## 6. Reproduce

```
python runs/2026-11-27_cosmic_null_validity/gapset_v2/build_gap_set.py
python tools/prereg.py verify runs/2026-11-27_cosmic_null_validity/gapset_v2
python tools/check_candidate.py --selftest
python runs/2026-11-27_cosmic_null_validity/make_planted_control.py
python tools/check_candidate.py --file runs/2026-11-27_cosmic_null_validity/gapset_v2/gap_candidates.txt --derivation runs/2026-11-27_cosmic_null_validity/gapset_v2 --profile gsmg
python runs/2026-11-27_cosmic_null_validity/make_appendix.py
```

The gap run takes about seven minutes on this machine: `find_keys` runs pure-Python elliptic-curve maths
over every 32-byte window of each pad-valid 1,327-byte plaintext, and there are 16 of those, about 15 s
each. An early attempt was voided because Python's `str.splitlines()` broke 83 candidates into fragments;
see `VOID.md`.

## 7. Files

| file | contents |
|---|---|
| `REPORT.md` | this report |
| `PREREG.json`, `PREREG.sealed`, `SELFCHECK.json` | the void first statement (3,544) and its recorded self-check |
| `VOID.md`, `gap_run.log` | why that attempt was void and what it produced (not counted) |
| `build_gap_set.py`, `gap_candidates.txt`, `gap_provenance.tsv`, `gap_manifest.json` | the void extractor and its artifacts |
| `gapset_v2/PREREG.json`, `PREREG.sealed`, `SELFCHECK.json` | the sealed gap set (3,461), sealed before any candidate file existed |
| `gapset_v2/build_gap_set.py`, `gap_candidates.txt`, `gap_provenance.tsv`, `gap_manifest.json` | extraction, bound check, source hashes, controls |
| `gapset_v2/gap_run.log`, `gap_run.err` | the single pinned-profile run; every pad-valid output with its first 80 bytes |
| `make_planted_control.py`, `planted_control.log`, `planted_control.json` | the through-loop control (pad 16 on a synthetic envelope) |
| `make_appendix.py`, `APPENDIX_GAP_STRINGS.md` | all 3,461 exact strings with their provenance, rendered from the artifacts |

Hashes: `gapset_v2/gap_candidates.txt`
`5b744206bcfbfe446f885574be00cb19dd0df3670e2adf1ab6a3cf1416ca42d2`;
`gapset_v2/gap_provenance.tsv`
`99fee3a86b2a1e2733154d63a6d08f51404a70caeb10e84e21baa186eaf7244f`;
`APPENDIX_GAP_STRINGS.md`
`30b90041213aa80b6fe48d6505d0e872d5ab6a063f354aca0375c24a49dd6ad5`.

