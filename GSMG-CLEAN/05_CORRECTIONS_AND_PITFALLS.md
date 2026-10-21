# 05 — Corrections, retracted claims and pitfalls

Earlier rounds contain claims that were later shown wrong. The raw ledgers in `prior_research_ledgers/` still contain them. Check this list before trusting anything from those ledgers.

## 1. False "decrypts" (chance padding)

**Background**
- A wrong key gives valid PKCS#7 padding about 1 time in 256 (pad byte 01).
- A plaintext that only has valid padding is **not** a result.

**Retracted results**
- **Cosmic Duality "decrypt."**
  - Key: `a795de11…` XOR prekey, raw MD5 EVP → 1,327 B (sha256 `4f7a1e…`), entropy 7.87 bits/byte. It is a pad-1 fluke.
  - The "route" it suggested leads to a parking page.
  - It was claimed in GitHub issue #55 and retracted in #104.
  - The addresses derived from it, `1JG648…` and `145ZQ9…`, are not the prize.
  - Gemini Add.29 "4f7a1e door" was the same thing, retracted in Add.30.
- **`818af53d…` prekey.** It opens nothing. It also appears unused in r1 bigsweep.
- **79 B MD5 SalPhaseIon output** (sha256 `1449a217…`, hex `9fa9db91…`): a fluke.
  - Its first 32 bytes as an uncompressed WIF (`5K2byJMssxFKuTgnk9YQjpBz5FhkwwF2LaZoAyTus8HjGEpz8AT`), used raw with MD5 EVP, also pad-1-open the **Terminal** envelope (79 B, `b06fa6f2…`). Re-checked 2026-09-13.
  - This second link is not searched, so its chance is about k/256 (k = key encodings tried), not 1/256 per blind guess. But the community produced hundreds of stage-1 pad-1 hits, so some two-link chain is expected. The later Cosmic → Chain 4 step needs an XOR mask that is forced to make `Salted__` (`e5364a3b4a0a367e ⊕ b657264f2f6e6921`). fresh-start's own `canonical_chain.json` says `REPRODUCIBLE_UNAUTHENTICATED_PADDING_CHAIN`. Still not evidence.
  - Keys derived from this chain (astra `oracle\chain_keys.json` `cosmic_h_key1/2`) sent the April 2026 inbounds from `1Kv59xv…` / `1KY3yqm…`.
- More pad-1 flukes seen in session logs: `itsinfrontofyoureyes`, `wewill`, `andend`, `Apropos`, `screenplay`, `hillfexmgsgq`→Cosmic, `HEISENBERG`→SalPhaseIon, `a`→Terminal. A Cosmic "split into Half and Better Half keys" happens for 28 of 243 pad-1 decrypts (11.5%) under the base-38 pipeline, so a split is not evidence.
- GitHub issue #108 "Salph small blob decrypts" only after mutating two base64 letters, with MD5 EVP [claimed]. `jackdevs66/GSMG5_CDuality` (210 combinations, one pad hit ≈ 36% chance).
- #18782 IV/salt JSON is a troll post (#18776/#18783), not creator material.
- `salphaseion_plain_79.bin` (sha `9c14868c`) has unknown provenance. Ignore it.
- **ArchOptic #10597 "absvolt":** pad-1.

## 2. Broken success gates

**Unjustified**
- "Plaintext must be exactly 64 B / pad 16." A 64–79 B plaintext is possible on an 80-byte envelope.

**Too narrow** (can discard real hits)
- printable-only
- English score
- hex64-only
- top-5 ranking

**Use instead**
- Padding validity plus key detection on every pad-valid output: raw 32-byte windows, hex64, WIF, base64, each compared with both hash160s. This is what `tools/check_candidate.py` does.

## 3. Script bugs found in earlier rounds (their nulls are weaker)

- Base58Check bug in `hunt_literal_key`: all literal-key comparisons before 2026-09-12 were invalid (re-run after the fix: 0).
- Harness defaulted to MD5 EVP and applied a printable filter.
- `second_door.py` used index 162 instead of 163.
- Gemini Add.28 used the wrong genesis address (`12PNCr…`; the real one is `1A1zP1…`).
- Old `bifid9` applied the forward transform instead of decoding (412 transforms, 0 AES).
- r1: the B1 half-blob bug; fastoracle checked only Half.
- Centre-pixel colour sampling miscounted (102 → 101, 62 → 37).
- This clean-up: `check_candidate` IV slice fixed (d[32:48]); the Bifid port was fixed and verified in `reproduce_leads.py`.

**Outside `E:\rabbit-combined` (found via session logs, 2026-09-13; evidence in 06 §1, §6)**
- `E:\testing-btc-p\fresh-start\tools\evidence_first_solver.py:280-282` loads only the first base64 line of the Terminal envelope (48 B). Its Terminal nulls are void. [checked]
- `Desktop\idk-btc\verify-work\session15_recovery.py:23` and `adversarial-review\bounded_tests.py:12` use a 42-hex Better Half hash160 (`004bc468…`), so only Half could match. `session15_recovery.py:126` saves results only `if events:`. [checked]
- `Desktop\idk-btc\verify-work\session13_b1_architect.py:61` never key-checks pad > 2 non-printable output (781,312 trials). [log]
- v49 "salvation" audit omitted sha256hex. `D:\astra\…\tools\oracle.py` has an MD5 branch; the 349M / 437M runs used a wrong target. Cursor v1 used MD5; v2–v6 used a weak gate. [log]
- rabbitv3 key checker missed both WIF forms and base64 keys before its fix (affects the 31,104 LOCKED_ENVELOPES sweep). [log]
- Cosmic XOR-subset searches used odd cardinalities only and cancel the duplicated matrixsumlist. [log]
- "pad10" filter bug; `refine_hot_case.py:199` swapped its input; `D:\puzle` findings.md §10 S91 uses 419 (correct 422). [log]
- fresh-start silently altered WAISTING/THROPHIES in its Architect quote, and a selector script read a CDX cache from another checkout. [log]
- Community `libaes.py` (`except: pass`, 100% printable, treats sha256-of-hex as raw) and `aesdecodemultiprocessing v5.py` (bails on first-block ASCII). [log]

## 4. Retired claims

**Leads and payloads**
- The "341" lead.
- "The nest is the door-1 payload."
- "X2SH is officially dead." Unsourced; #8569 says "Can't say".
- "14 blobs." Textarea 2 is one Cosmic blob.
- `#fffeff`. The value is `#fefefe`.
- The "invisible rabbit". Old images ENDGAME_EMBLEM and RABBIT_AND_GATE still show it; they were excluded.

**btcseed and the Phase 3 slug**
- btcseed "creator-confirmed", and the odds "1 in 8,031,810,176". The creator never wrote "btcseed" (see 03 lead 4 for real odds).
- "Phase-3 page slug = sha256(password)."

**Coincidences read as clues**
- passport ↔ EO 13224.
- "13224" found in FAED[10::11]: chance.
- "KEYNOTE": a segmentation artifact. The arithmetic 91 − 23 = 68 goes with it.
- "604 / 1812 bits."
- B91 mod-13 (retracted).
- Colour / `b` overlap: p = 0.87, not significant.

**Stale framing**
- "Five-year blind spot."
- "~1.25 BTC unmoved." Balances are in 01 §9.
- Gemini Add.30 "site dead", overturned by Add.40 (the site is live; 01 §10).
- "urlblob is in no archived URL." False: it is in CDX at 2026-01-05, and it is solver-made.

**Errors in "Last solved and unsolved parts.txt"**
- "ourlasthint" (the real text is "firsthintisyourlastcommand").
- Wrong placement of `shabefanstoo` (01 §6 has the right placement).

**Rejected by solvers**
- `flag{8KJ}`.
- "part2 = evilcorp". The part is Safenet.
- The April puzzle ends in a Rickroll.

**Typos**
- Typos are not clues (#1806, #5960), except giveit/givetit (#867).

**Found in session logs and outside workspaces (2026-09-13; 06 §5–§6)**
- #66903 "hidden in a room with a hidden door" is about the laptop, not a puzzle door. [checked]
- Late `edited` timestamps are mostly reaction bumps (84 of 122), not proof of rewritten hints. [checked]
- `1NULY7…` is not a planted door: #5241 is Saber's post; #47068 / #56452 identify a kangaroo-tool tip address. 18Cchrj, 1AD2wf, 13HGhjk and 1GyT5W are solved (01 §9). [checked]
- #24071 "1357 blocks to go" is a halving countdown, not a cellular-automaton rule.
- 01 §5a previously listed UNBALANCED EQUATION as an added word; it is in the film. [checked]
- Not creator messages: #6891 {30},{2},{77}; #39233; #60352; #65924 KEYEYES; #42477; #28307/#28308; the maze photo (0×FL0K1).
- Fabricated hint transcriptions exist in AI-written notes ("7 by 13", R=133, "sixth password inherited", "seventh-password book", "wrong direction", "cosmic language", "people, not passwords", "half is not the whole", "rotate the problem", "Sixteen years"). Quote only from the export or the image itself.
- AI-invented artefacts: a "floflo777" repo in session 063e04da; astra `PROGRESS.md` is GPT output (#70983); astra's "neighbour addresses prove key possession" and "3GSMG24 creator-signed" are unsupported.
- AppleLamps/clean-btc lists the VIC checkerboard as "eliminated". Wrong (01 §5b).
- `D:\5btc\known-real\verified\aes-envelope-recipe-and-decryptions.txt:27` has a wrong salt (`35f64511d3d11f4c`).
- "Vanity address cannot come from a seed" (`D:\puzle\docs\TELEGRAM_2026_REVIEW.md:133`) is a false closure.
- Grille/lattice "disjointness" of markers is forced by the (col − row) mod 4 structure; not evidence.
- Base64 `z` at position 64 of half 1 is ciphertext; hashing a copy without it gives the bad value `422a96e4…`.
- Group-export filenames: `p3.b64` = Phase 2.1, `p32b` = Terminal.
- Any FAED reorder read as one 570-digit number gives 237 B; "key size" matches from digit counts are arithmetic.

## 5. Index conventions (state which one you use)

| Item | Conventions |
|---|---|
| Architect text | 1,539 letters only (PRIVATEKEY at 479) vs 1,544 with extra characters (480) |
| `#fefefe` | index 163 (0-based) vs 164 (1-based) |
| Phase 3.2 byte offsets | vary by ±4 depending on EBCDIC decoding (443 vs 447) |
| YOUWON | 21–26 (0-based) vs 22–27 (1-based) |
| Architect offsets | letters-only 1,539 vs continuous 0-based with spaces (REINSERTINGTHEPRIMEBASICS 1089–1114, SELECT 1143) vs older Cursor (PRIMEBASICS@1103) |
| Coloured cell "at a prime position" | none under 1-based raster; 11 under physical-spiral indexing |
| DBBI parse | 84 tokens (L2) vs 83 tokens (FE as marker) |
| Printable share of Phase 3.2 | ~60% vs 29.11% (definition) |
| Telegram times | export ≈ UTC−4; sourcebooks are UTC |
| Yellow / blue numbers | door numbers vs spiral order |

- The preamble line "One for one, four for one" is omitted from SOLVED_PLAINTEXTS in some older copies.

## 6. giveit vs givetit

- The creator's #867 says `giveit = givetit`.
- The **current** Phase 3.2 blob opens with the password containing **giveit**: `jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple` (self-test in `check_candidate.py`).

## 7. Misnamed or wrong files in the old folders (not copied)

- `rabbit-gemini\corpus\terminal_envelope.*` is actually the **SalPhaseIon** envelope.
- The Terminal and SalPhaseIon envelopes are two different blobs with salts `b45a…` and `3ab5…`.
- `read\phase3_plaintext.txt` (4,095 B) is wrong. The correct file is `data/phase3_plaintext.bin` (4,090 B).
- The `sol_consult_pending` token list is wrong.

## 8. Junk that was deliberately excluded

- `rabbit-gemini\THE_PUZZLE`: a derivative puzzle, not GSMG.
- `.mimosa` folders.
- `found.txt`: 30 MB of vanity keys.
- The sQRt CTF writeup; "dbbdi and fead solve.txt" (a joke).
- Generated audio, plots, turtle images, and `VIEW_*.png` renders.
- Duplicate PDFs and exiftool fragments.
- `rabbitv4\other` conversion tooling.
- The redundant 9.9.26 export copy, `read\result.json`, and `read\photos`.

## 9. Website pitfalls

- `Hello :-)` with a 404 only means an unknown path.
- Uppercase `/Puzzle` is the SPA shell. URLs found by directory hunting are SPA fallbacks.
- `/phase1verification` POST returns 404 for a wrong answer and 302 for the right one.
- Wayback captures of made-up paths after July 2026 are placeholders.

## 10. Stale paths in old ledgers

- `E:/rabbitv3`, `E:\rabbitv4`, and `C:\Users\lucas\Desktop\…` refer to earlier locations. The material now lives under `E:\rabbit-combined\` and, for what was kept, in this folder.

## 11. Line map for `reference_texts/GSMG_COMPLETE_PUZZLE_REFERENCE_2026-09-10.txt`

Open it with `newline=''`; the line numbers assume the file's own line endings.

| Line | Section |
|---|---|
| 54 | walkthrough |
| 2586 | Phase 2 ciphertext |
| 2600 | Phase 3 ciphertext |
| 2650 | Phase 3.2 ciphertext |
| 2838 | Architect letters |
| 2931 | SalPhaseIon compact |
| 3104 | FAED |
| 3148–3175 | Cosmic |
| 3189 | Bifid |
| 3208 | forwarded hex |
| 3222 | April puzzle |
| 3251 | CREATOR_MESSAGES |
| 7884 | forwarded posts |
| 12393 | forwarded-only texts |
| 12739 | media review |
| 13052 | New Year sequence |
| 13105 | creator raw json |
| 187117+ | captured HTML |
| 187614 | harness audit |

## 12. DBBI's final e is consumed, not left over

The historical `../read/SOLVE/hill_faed_exact.cjs` derives `FEXMGSGQE` by claiming the HILL sum construction leaves e=5. It does not: all 91 source characters form 84 logical cells, and that e is the last value in the column whose total 42 produces Q. Reserving e instead changes the sum text to HILLFEXMGSGL. Reuse may be hypothesized, but cannot be described as a leftover. See `runs/2026-09-13_dbbi_accounting/REPORT.md` for the ownership trace and corrected-key test. The same audit shows that the whole DBBI produces the same Bifid square as its first 13 characters; an arbitrary prefix cutoff is unnecessary.
