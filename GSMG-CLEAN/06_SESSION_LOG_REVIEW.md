# 06 — Session-log and workspace review (2026-09-13)

This file records what came out of reviewing the AI session logs in `C:\Users\lucas\.codex` (including the archived rollouts in `D:\C-drive-relief\2026-08-22\CodexSessionsArchive`), `C:\Users\lucas\.claude` and `C:\Users\lucas\.cursor`, and the workspaces those logs pointed to. Most of those workspaces were outside `E:\rabbit-combined`, so the first clean-up never saw them.

**Method**
- 17 reviewer passes read the logs against 01–05.
- Every high-impact item was then re-checked locally. No decrypt searches, password sweeps or network calls were run; the only decrypts were single reproductions of values quoted in the logs.
- Corrections that change what 01–05 say have been **applied to those files**. This file keeps the evidence and everything that is new.

**Labels**
- **[checked]** — re-run or re-read locally during this review (command or file noted).
- **[log]** — tool output is shown in a session log, or the number is in a report file on disk; not re-run.
- **[claimed]** — asserted in a log or doc with no shown output.

---

## 1. Most important items (read these first)

| # | Item | Label | Effect |
|---|---|---|---|
| 1 | **Four "planted" prize-address senders/recipients are identified** (table in §2). The dossier listed them as unknown. `1NULY7…` is a kangaroo-tool tip address, not a door. | [checked] | Searches aimed at `1NULY7` are moot. The marker addresses give a way to confirm answers without decrypting. |
| 2 | **#66903 "hidden in a room with a hidden door" is about the laptop**, not a puzzle door. It replies to #66901 ("spent the whole night looking for your laptop 😂"). | [checked] export | Removed as door evidence (02 §4, 03 §7). |
| 3 | **Most late "edited" timestamps on creator messages are reaction bumps.** Of 122 creator messages edited >30 days after posting, **84** have an edit time within 2 s of a reaction time. The other 38 mostly have no reaction data in the export, so they are unexplained, not proven content edits. | [checked] (`verify_w.py` in this review) | 02's "hints were edited years later" caveat was much too strong; rewritten. |
| 4 | **The FAED row-selector strings and the Architect L1/L2 selectors *were* AES-tested.** Row selector: 34,272 SalPhaseIon trials, 135 pad-1, 1 downstream Terminal pad-valid, no key. L1/L2 on P1-EOF matrix sums: 606 trials, 0 pad. | [checked] report exists (`rabbitv3\rabbit\analysis\out\faed_row_selector_aes_2026_09_10\REPORT.md`) / [log] | 03 §4, §15 and 04 §F said "not tested"; fixed. |
| 5 | **`E:\testing-btc-p\fresh-start` Terminal nulls are void.** Its loader keeps only the first base64 line of the Terminal envelope (48 B instead of 96 B): `tools\evidence_first_solver.py:280-282`; `derived\openssl_cipher_family_audit.json` records `"phase32_80": {"bytes": 48 … "decryptions": 139288}`. | [checked] | 139,288 Terminal decrypts (1,514 passwords × 46 configs) test nothing. |
| 6 | **`Desktop\idk-btc` Better Half target is wrong** (`004bc468…4ed6`, 42 hex, leading `00`) in `verify-work\session15_recovery.py:23` and `adversarial-review\bounded_tests.py:12`. Those scripts could only ever match the Half address. | [checked] | Their nulls are **Half-only**, not full nulls. |
| 7 | **`session15_recovery.py:126` records only `if events:`**, so pad-valid 65–79 B outputs without a detected key were never kept. | [checked] line / [log] impact | The 9.88M "null" does not cover the Terminal envelope's plausible plaintext range. |
| 8 | **01 §5a "added words" list was wrong.** UNBALANCED EQUATION is in the film; PRIME BASICS only replaces "program"; 23 / 16 / 7 is film wording in context. | [checked] against `reference_texts/matrix_reloaded_architect_scene_transcript.txt` | 01 §5a corrected. |
| 9 | **The community "chain 1 → chain 2" link.** The 79 B MD5 fluke from SalPhaseIon short (`9fa9db91…`) gives WIF `5K2byJMssxFKuTgnk9YQjpBz5FhkwwF2LaZoAyTus8HjGEpz8AT`, and that WIF (raw, MD5 EVP) also pad-1-opens the Terminal envelope (79 B, `b06fa6f2…`). | [checked] (`check_candidate.py --profile raw-md5`) | Conditional chance is about k/256 for k key encodings tried. Across the hundreds of stage-1 pad-1 hits the community produced, a two-link chain is expected. Chain 4's XOR mask `e5364a3b4a0a367e ⊕ b657264f2f6e6921 = "Salted__"` is forced, so it is fitted. Still **not** evidence (05 §1). |
| 10 | **April 2026 inbound payments from `1Kv59xv…` / `1KY3yqm…`** come from keys in `D:\astra\gsmg-io-5btc-puzzle\oracle\chain_keys.json` (`cosmic_h_key1/2`), derived from the retracted fluke chain. | [checked] (earlier in this review) | They show no one opened an envelope; they are solver activity. |

## 2. Marker addresses: answers confirmable without decrypting

Private key → compressed P2PKH. Re-derived with `tools/check_candidate.py` EC helpers during this review. All are **[checked]**.

| Address (dossier) | Note in tx | Private key |
|---|---|---|
| `18CchrjA3Uzfrzy4DFqao9ric6YfK4hjdc` | "part of the cipher" | sha256 of the 149-digit checkerboard string (01 §5b) |
| `1AD2wfwXukZ1kUAy848hTQQ72aSBZPB75r` | "are you sure?" (later sent 600 sat "Yes") | sha256 of the Phase 1 answer `theflowerblossomsthroughwhatseemstobeaconcretesurface` (= `5ac40783…`) |
| `13HGhjkmKUkP8sk9k63BLmhkxRjy7uK4Rp` | "Good job, Neo!" (later "From Neo") | the 192-bit integer of `gsmg.io/theseedisplanted` **with bit order reversed**, used directly (no hash). Non-reversed gives `148XH2Y…`. |
| `1GyT5W…` | "do you beleive me you need it?" | sha256 of `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` |
| `1NULY7DhzuNvSDtPkFzNo6oRTZQWBqXNE9` | 1,050 sat, never spent | **Not a puzzle key.** #47068 quotes a "Pollard-kangaroo PrivKey Recovery Tool … Tips: 1NULY7…" banner; #56452 (2026-01-11) calls it the donation address of `github.com/keyjoke/vs-kangaroo-hybrid` (not fetched). #5241, often cited, was posted by Saber, not the creator. [checked] sender of #5241 |

Who sent these (creator or solvers) is not established. The pattern ("sha256 of a solved answer → address, with a note") is a cheap check: any new candidate answer can be hashed and its address looked up on-chain.

## 3. New leads (unproven; ranked by how specific they are)

1. **ZERO on the DBBI prime grid.** [log] (`D:\astra\gsmg-io-5btc-puzzle\tools\solve_zero_checkerboard.py`, `audit_prime_grid_zero.py`)
   - Use the 83-token b/be-at-prime parse. Place the 24 prime-coordinate cells in a 4×6 layout coloured by the poster stream (off-white = blue).
   - Row totals are 30, 29, 16, 29. Yellow − Blue per row is −26, −21, −8, 15; taken mod 26 in A1 (0 = Z) that reads Z E R O. The total is 104.
   - Controls: 150 of 1,307,504 colour placements give ZERO. An upstream-preserving null gives 12 of 319,770 (0.00375%) with total 104 plus ZERO.
   - It fits #8000 "zeroed out". No envelope test that uses the ZERO instruction was found.
   - Construction detail (astra `analysis/prime-grid-zero-review.md`): DBBI as 7×13, one-based prime rows 2,3,5,7 × prime columns 2,3,5,7,11,13 = 24 cells, coloured by the 24 regular poster markers in order. The 24 selected values total **104**, which is also the length of the adjacent `matrixsumlist` binary field [log].
   - Prior consumers [checked 2026-09-13]: fresh-start `tools/prime_matrix_cross_stage.py` tried 5,076 materials (literal / sha256-hex / sha256-raw; MD5 and SHA-256 EVP) **on the SalPhaseIon envelope only** (`stream_80`), never on Terminal or Cosmic. Its 45 saved pad hits are all 79 B (chance) and contain no Half / Better Half key (re-scanned with `check_candidate.find_keys`). astra's 24 zero-mask checkerboard decodes (`solve_zero_checkerboard.py`, 192 zeroed inputs) were decode-only: nothing was hashed or AES-tested.
   - **Envelope test done 2026-09-13 → clean null** (`runs/2026-09-13_zero_envelopes/REPORT.md`): 8,163 ZERO-family texts (poster schedule + 149 other ZERO schedules as controls), the 5,076 fresh-start materials and 944 astra zero-mask strings on all three envelopes (sha256-hex / raw / sha256-raw × EVP SHA-256 / MD5): 194,382 decrypts, pad rates at chance, 0 pad ≥ 3, 0 keys. Open only: ZERO applied as an instruction to other material, combined answers, other KDFs.
   - Caveat: there is a conflict between the 83- and 84-token parses (03 §4).
2. **Seven-key Bifid on FAED** (keys = successive 13-letter DBBI rows). [log]
   - Outputs start BTCSEED…, BARSK…, EOHW…, CANQ…, FEEF…, IKDG…, GTHW…, giving three BIP39 prefixes BAR / CAN / FEE.
   - Shuffle control: 2 of 2,000 (0.1%). A community member (#45661) found it and called it "probably a coincidence".
   - Prior envelope test [checked]: astra `check_source_bound_passwords.py` tried the 8 complete final successive outputs (listed/reverse × raw/400-474-zeroed × upper/lower) with sha256-hex + EVP SHA-256/MD5 on all 3 envelopes: 0 pad-valid.
   - **Envelope test done 2026-09-13 → clean null** (`runs/2026-09-13_seven_key_bifid/REPORT.md`): every round output (successive and independent), prefixes, BAR/CAN/FEE word forms, and the seven keys as passwords, for the real DBBI and 200 of astra's shuffle controls (histogram reproduced exactly), sha256-hex / raw / sha256-raw × EVP SHA-256 / MD5 × 3 envelopes: 1,079,568 decrypts, real 28 pad-valid of 6,408 (25 expected), 0 pad ≥ 3, 0 keys. Open only: other periods / key selections, BIP39 wallet derivation, use as an instruction.
3. **"Follow the white rabbit" as the "actual first hint".** [checked] On 2023-08-22 Jerry re-posted an old exchange: #11247 (his question "what was the actual first hint", forwarded), #11248 (forwarded from Jrk Bgrt: "Follow the white rabbit"), then #11249 "That was years ago". #8972 (2023-08-04) is Jerry's photo of it [log for the photo content].
   - A candidate for "first hint is your last command"; the poster file is `follow_the_white_rabbit.png`.
   - A 540-trial literal test exists (`read_solve_review/HINT-SYNTHESIS.md:117`). Hash/zeroing variants have not been tried.
4. **{1,4,21} on the 25-cell special stream selects the FE cell.** [checked]
   - Spiral order of all non-black/white cells: `BBBBYBBBYYBBBBYBBYYBFYYBY` (FE at spiral 163 falls between markers at 159 and 167).
   - One-based positions 1, 4, 21 give B, B, **F**. This depends on the convention (one-based, FE included); #6884 may be an April Fools joke.
5. **Sums of prime ordinals give −41, −17.** [checked]
   - Blue has 15 cells: primes ≤ 15 sum to **41**. Yellow has 9 cells: primes ≤ 9 sum to **17**. That matches parcel (−41, −17) (#1837).
   - It depends only on the counts 15 and 9, not on positions. That makes it weaker than 03 L1.
6. **All markers and the FE cell lie on the lattice (col − row) mod 4 = 1.** [checked]
   - 15 B, 9 Y and the F cell; spiral index ≡ 7 (mod 8) for markers.
   - The lattice has 49 cells: W 18, B 15, Y 9, K 6, F 1.
   - This is structural (colour sits on bit 7 of each byte), so it constrains how "grille" readings can be built; any disjointness is forced.
7. **Fresco quote = 140 characters and 23 words.** [checked] "The future is fluid. … The future is ours to direct." Without punctuation it has 140 characters including spaces, 23 words and 118 letters.
   - A second candidate for "WISE MAN ABOVE … HUNDRED FOURTY" / "TWENTY-THREE", next to the genesis `0x`+138 reading (01 §4).
   - Tested so far only through the passport mask (9,450 gates).
8. **Neo passport XOR poster low bits.** [checked] 11092001 = `0xA94021`; `0xF73D92 ⊕ 0xA94021 = 0x5E7DB3` (23 significant bits, 16 ones, 7 zeros = 23/16/7).
   - Apophenia-grade (about 1% per encoding tried). Follow-ups (9,450; 306,144 scalars) were null.
9. **Marker 21 is the only mismatch** between the DBBI 84-token parse's 16 `b` / 7 `be` prime markers and the poster stream (first 23: parse `…BBYB` vs poster `…BYYB`). [log]
   - The "flip marker 21 → DEL" variant was later retired by its author as an unsourced assumption.
10. **Creator #6509** (2021-03-14): "I gave an unforseen hint already 🤷‍♂", replying to "time for a hint on matrixsumlist?" [checked]. So a matrixsumlist hint already exists somewhere.
11. **Creator #66588 "Yes"** (2026-07-12 21:01) comes 3 minutes after #66587 "salphaseion is 100% solveable?". There is no reply link. [checked]
12. **F-A-E Sonata** (fresh-start): S570 = "fae" + 9 × 63. A pre-registered German note mapping is **untested**. [claimed] Links to #66962 NOTES.
13. **NotebookLM proposal:** DBBI 15/30 column sums as Vigenère/Beaufort mod-9 keys over FAED, plus an Architect passage. Never tested. [claimed]
14. **Poster palette values as bytes** (`3F48CC`, `FFF200`, `FEFEFE`). Also: the blue-channel low bit and red-channel bit 5 planes are unexplored. [claimed]
15. **Rebus tile glyphs** have explicit `+` (blue `dig_i`) and `−` (red `t`) and open/closed padlocks. They could be a sign convention for signed parses. Never used. [claimed]
16. **Unrun scripts** in `D:\astra\gsmg-io-5btc-puzzle\tools\`: `solve_first_hint_recipes.py`, `solve_enter_numeric.py`, `solve_hill_bytes.py`, `solve_signed_sum_transfer.py`, `resolve_reference_targets.py`. [claimed]

## 4. New or re-scoped dead ends (not previously in 04)

A null covers only its exact scope. "gate-only" means candidates never reached AES.

| Test | Scope / result | Label | Caveat |
|---|---|---|---|
| FAED row selector → SalPhaseIon → downstream | 34,272 + 270; 135 pad-1; 1 Terminal pad-valid; no key | [checked] report | — |
| Architect L1/L2 P2-AST selectors on matrix sums | 606 trials × 6 envelopes, 0 pad | [log] | only this use of L1/L2 |
| Gate audit re-run without top-5 cutoff | 23,222 texts, 282 pad-valid, none coherent / no key. The old gate rejected all three real plaintexts. The "412 rejected DBBI outputs" null was never logged (unsupported). | [log] (`rabbitv3\rabbit\GATE_CONVENTION_AUDIT_2026-09-11.md`) | — |
| Finite cross-product | 48 answers × 6 envelopes = 288 + 288 random controls, 0 pad | [log] | — |
| LOCKED_ENVELOPES sweep (rabbitv3) | 31,104 AES, no open | [log] | the rabbitv3 key checker missed WIF and base64 keys before its fix |
| SalPhaseIon pre-registration v1–v22 (`D:\puzle\…\SALPHASEION_PREREGISTRATION.md`) | 71,184 decrypts, 253 pad (279 expected), 0 accepted; v23–v36 ~200k more | [log] | v23/v35 checkers passed themselves |
| v49 "salvation" audit | 386,794 passwords / 3,094,352 attempts / 12,132 pad / 0 legible | [log] | **omitted sha256hex, the proven convention** — not a valid null for the default profile |
| Nest module door-1 (module resolution, own decoder) | 246 trials / 123 passwords, twins, EVP-SHA256, null | [log] (`D:\rabbitv2\rabbit\analysis\out\nest_module_door1.txt`) | — |
| pipeline_enum (8.7-fresh-start) | 17,905 unique passwords on Terminal, 62 pad vs 70.2 expected, 0 structural | [log] | — |
| clean-btc "session 5" on Terminal | 215,408 sum constructions + 42 routes + homophonic (73/99 controls outscored) + ~290k sha windows | [log] | 64 B / >90% printable gate (too narrow) |
| Cosmic XOR subsets | 131,064 decrypts on Terminal / SalPhaseIon, null | [log] | odd cardinalities only; order-blind; the duplicated matrixsumlist cancels |
| XOR-3/4/7 subsets, Chain 4 certificates, MITM (VERIFICATION_REPORT) | 13,684,660 gates; 9.48e12 logical MITM evaluations | [log] | built on the fitted Chain 4 |
| fresh-start C(7,3) / nested AES / seven-token Cosmic sets | 5,600; 21,280; 26,880 (111 pad); 11,466 (51 pad) + 10,296 | [log] | Chain-4-based |
| fresh-start ordered prime-zero pipeline | 1,024 sum lists, 19,128 AES, 0 | [log] | English / nested gates |
| fresh-start evidence-first / 14×14 bridge | 12,288 sum lists + 48 reinsertions; 608 sum lists | [log] | **gate-only** |
| Passport/Fresco seven-word gates; KTGFAIR Playfair | 9,450; 306,144 scalars | [log] | — |
| Nonce audit, Cosmic-derived cluster + prize | 187 signatures, all r distinct; 133/181 match RFC6979; 17,952 relation equations, 0 | [log] | — |
| hexgate | 29,045,480 decryptions, 0 | [log] | weak gate |
| Cursor v2–v6 | 242,166 | [log] | weak gate; v1 used MD5 (invalid) |
| tried_log_v2 / v3 (`Desktop\5g\analysis`) | 73,314 + 13,512 decrypts, 0 | [claimed] (files exist) | — |
| Terminal/SalPhaseIon DBBI/FAED 3×3 digit etc. (various astra) | column-sum word lookup, T13/T23 signed sums, Hill81 bytes, ENTER CR/LF (same 96 B envelope), BIP39 checksums (fail; a 21-word phrase cannot fit 80 B) | [log] | — |
| idk-btc CP-SAT / operand trials / KMODEST | 80 models; 161,802 operand trials; ~106k AES; 2,432 | [log] | **Half-only** (item 6 in §1) |
| Issue #106 (~2.5B tests) | used MD5 EVP | [claimed] | void for the default profile |
| `oracle.py` 349M / 437M runs (D:\puzle) | wrong target | [log] | void |
| Solver OP_RETURN burst (blocks 938164/938165) | 41 messages → 2,112 decrypts | [log] | — |
| Book anchors / base-9 permutations | 3,888 AES; 362,880 | [log] | — |
| "1357 blocks to go" B1357/S1357 automaton | built on #24071 | [log] | #24071 is a halving countdown (§5) |
| 1NULY7 candidate searches (~25.5M) | — | [log] | moot (§2) |
| floflo777/open-crypto-puzzles ledger | 49,808 word windows; 34,000 ASCII windows; 1,358,577 small-blob candidates with corrected oracle, 0 | [log] (the local clone is gone) | user claims ~335M total |

## 5. Creator messages to add or re-read (checked in `telegram/ChatExport_2026-09-13_result.json`)

Export times are about 4 h behind UTC (checked on #4624, #6497, #24071 against the UTC sourcebook / halving arithmetic).

| id | export date | text | note |
|---|---|---|---|
| #74 | 2019-04-20 | "Ok.. somebody has cracked the first code." | timeline |
| #325 | 2019-04-23 (ed. 2025-04-30) | "Ewout managed to crack the april 1st puzzle. He was the first to solve it." | the April puzzle is a side puzzle (ends in a Rickroll) |
| #881 | 2019-05-18 (ed. 2026-01-03) | "In case the private key hasn't been found in 2019 we'll release a tiny hint at the start of 2020, that will be the final hint. Can the private key be retrieved …" | the Jan-2020 hint = #1710 (see #4096) |
| #1448 | 2019-09-04 | "Still no hints ;-)" | — |
| #3384 | 2020-04-08 (never edited) | "Quite some typos have been changed already. The biggest blunder so far in the mainline of the puzzle was givetit instead of giveit 😩🔨" | typos *were* changed on the site |
| #3903 | 2020-05-11 | "Happy halving!" | context for #24071 |
| #4094 / #4096 | 2020-05-20 | "It is" (re #4076 "The January hint is missing on github") / "This one 👆." replying to **#1710** | confirms #1710 is the January 2020 hint |
| #4102 | 2020-05-20 | "answer is there" | precedes #4105 "First or zero" |
| #4624 | 2020-08-09 | "a private key" (re #4623 "private key or seed phrase or brain wallet?") | earliest format answer |
| #4688 | 2020-08-12 | "Indeed remarkable with the hints stating the path pretty obvious..." | — |
| #5960 | 2021-03-01 | "Ancient spelling 😅. One of the many many typos." | re "hundred four(ty)" |
| #6497 | 2021-03-14 (ed. 2025-06-26) | "…When people progress in salphation it might be cracked pretty soon. Breaking salphation, should be giving the feeling of the phase's name. Won't be easy … probably before next halving." | acceptance criterion for SalPhaseIon plaintext ("salvation") |
| #6509 | 2021-03-14 | "I gave an unforseen hint already 🤷‍♂" | re matrixsumlist hint (§3 item 10) |
| #6712 | 2021-03-22 (ed. 2026-05-06) | "Nr 5 in salph" | — |
| #8516 | 2023-05-02 | "Still remarkable that scene. Especially the expiration date of his passport 😁." | — |
| #9627 / #9629 | 2023-08-06 | "Something was solved rather... remarkable." / "Partly." | a partial solve exists privately |
| #11248 | 2023-08-22 | forward of Jrk Bgrt: "Follow the white rabbit" | the "actual first hint" (§3 item 3) |
| #24071 | 2024-04-10 14:21 (ed. 14:43) | "1357 blocks to go" | ≈ 9.4 days before the 2024-04-20 halving (block 840,000). A halving countdown, not an operand. Halving timestamp is from general knowledge, not re-fetched. |
| #66568 / #66588 | 2026-07-12 | laptop "On that thing... is the actual answer" / "Yes" | #66588 follows "salphaseion is 100% solveable?" |
| #66589 | 2026-07-12 (ed. 07-13) | "And IIFF I'm somehow still wrong, which I'm most likely not as I've verified many times back then after some sad rushed mistakes, it's all still solvable with a few stable qubits." (full text) | 02 quoted only the tail |
| #66590 | 2026-07-12 | "But... Bip360 anyone. Thoughts?" | BIP360 thread #66542–#66595 |
| #66903 | 2026-07-16 | "Well, it's hidden in a room with a hidden door." | **re #66901, the laptop** |
| #70325 | 2026-09-01 | "🤐" | — |

**Not the creator** (often mis-cited): #5241 (Saber, 1NULY7), #6891 "{30},{2},{77}" (x7x7x7x6), #39233 (silver_anth, the yinyang question; edited 2025-08-26), #60352 (Denis Golovkin), #67175 and the maze photo (solver 0×FL0K1), #18782 IV/salt JSON (troll, #18776/#18783), #65924 KEYEYES (community), #42477 "ArchiChoice awaits you" (community, unverified), #28307/#28308 Slack YouTube link (user).

**Forward duplicates** (do not count twice) [log]: #40135, #42852, #49927, #52493 = #39237; #37590, #38879, #57099 = #9599; #43778, #49796, #51279 = #39224; #61402 = #60314. #8446 forwards #15851/#28808/#34003 decode identically, so its 2023-12-02 edit did not change content.

## 6. Pitfalls and bugs found in other workspaces (added to 05)

- Truncated Terminal loader in fresh-start (§1 item 5). fresh-start also silently "corrected" WAISTING → WASTING and THROPHIES → TROPHIES in its Architect quote, and its selector script read a CDX cache from another checkout. [log]
- `session15_recovery.py` records only key events; the Better Half target is 42 hex in idk-btc (§1 items 6–7). [checked]
- Session-13 validator `Desktop\idk-btc\verify-work\session13_b1_architect.py:61` returns `(None, None)` for pad-valid non-printable output with pad > 2, affecting 781,312 trials. [log]
- `D:\astra\gsmg-io-5btc-puzzle\tools\oracle.py:116` picks `hashlib.md5` unless `digest == "sha256"`. [checked line; which setting the runs used is from the log]
- `D:\puzle` findings.md §10 S91 uses 419; the correct total is 422. [log]
- "pad10" filter bug; `refine_hot_case.py:199` swapped its input. [log]
- Community scripts: `aesdecodemultiprocessing v5.py` bails on first-block ASCII; `libaes.py` uses `except: pass`, requires 100% printable, and treats sha256-of-hex as raw. [log]
- `D:\5btc\known-real\verified\aes-envelope-recipe-and-decryptions.txt:27` has a wrong salt `35f64511d3d11f4c`. [log]
- AppleLamps/clean-btc brief lists the VIC checkerboard as "eliminated". That is wrong (01 §5b decodes it). [log]
- `GSMG-CLEAN\prior_research_ledgers\rabbit_r1\FINDINGS_round1.md:497` has the VIC key with a dot instead of `/`. The disputed cell is never used, so both decode the same digits. [log]
- astra: "neighbour addresses prove key possession" (P±G, 2P, P/2 are worthless); "3GSMG24 creator-signed" (unsupported); `PROGRESS.md` is GPT output (#70983). [log]
- Idk-btc notes contain made-up hint transcriptions ("7 by 13", R=133, "sixth password inherited", "seventh-password book"). Fabricated hint-image quotes elsewhere: "wrong direction", "cosmic language", "people, not passwords", "half is not the whole", "rotate the problem", Decentraland lines, "Sixteen years". [log]
- Session 063e04da invented a "floflo777" repo; the real `floflo777/open-crypto-puzzles` is separate. Treat AI-written repo names as unverified. [log]
- "Vanity address cannot come from a seed" (`D:\puzle\docs\TELEGRAM_2026_REVIEW.md:133`, `ATTEMPT_LOG.md:129`) is a false closure; see the dossier (VanitySearch `-s` is possible). [log]
- Architect offsets differ between tools: continuous 0-based gives REINSERTINGTHEPRIMEBASICS at 1089–1114 and SELECT at 1143, with CHOICE absent. An older Cursor run gave PRIMEBASICS@1103. State the compaction. [log]
- Phase 3.2 "printable" share: 59.8% (01) vs 29.11% (a strict count in one Codex run). The definition differs; neither value is a gate. [log]
- Filename conventions in group exports: `p3.b64` = Phase 2.1, `p32b` = Terminal. [log]
- Additional pad-1 flukes seen in logs: `itsinfrontofyoureyes`, `wewill`, `andend`, `Apropos`, `screenplay`, `hillfexmgsgq`→Cosmic, `HEISENBERG`→SalPhaseIon, ArchOptic absvolt, `a`→Terminal. The Cosmic base-38 Half/Better-Half pipeline splits 28 of 243 pad-1 decrypts (11.5%) into two "valid keys", so such splits are expected. [log]
- Shuffle-control rate for DBBI 64/16 tokenisation: 03 §2 says ~0.3% (304/100,000, one control). Another run reported 209/20,000 (~1%) with a different control. Quote the control you use. [log]
- Any FAED reorder read as one 570-digit number always gives 237 B; "key-size matches" from digit counts are arithmetic (77 digits → 32 B, 153 → 64 B). [log]
- "277" in the Reddit thread is a typo corrected to 227 on 2019-12-19. [log]
- Poster centre cells: only 1 of 4 has a black centre pixel; majority reading 0000 (the "0100" reading is an artefact). White strip is 171×2 px. [log]

## 7. Where the source material is (not copied here)

These are outside `E:\rabbit-combined` and were never in the earlier distillation. Several contain retracted claims; read them with 05 in hand.

| Location | What |
|---|---|
| `D:\astra\gsmg-io-5btc-puzzle\` (`tools\` 57 scripts, `oracle\chain_keys.json`, `analysis\`) and `D:\astra\gsmgio-5btc-puzzle-2\hints\` (34 hint images) | ZERO / seven-key Bifid / April binary chain / DEL scripts; fluke-derived keys (mark FLUKE-DERIVED); `The DEL Binding.pdf`, `GSMG Marker Stream Audit.pdf`; `ChatExport_2026-09-04\photos\photo_282@04-08-2023_17-52-15.jpg` (#8972) |
| `D:\puzle\` and `D:\downloads-8.8\puzle-main\` | `docs\ATTEMPT_LOG.md`, `REFOCUS_2026_08_06`, `SOLVED_STAGE_REAUDIT`, `TELEGRAM_2026_REVIEW`, `HALF_AND_BETTER_HALF`, `gsmgio-5btc-puzzle-master\SALPHASEION_PREREGISTRATION.md`, `VERIFICATION_REPORT.md`, `RESEARCH_LEDGER.md`, `ARCHITECT_479_CONTINUATION.md`, door-probe classification. `D:\downloads-8.8\puzle-main\SOLUTION.md` (50.6 KB) was **not read** — see 14 §M9: it and the neighbouring `gsmgio-5btc-puzzle-master\` (≈100 preregistered `solver\*` scripts including the `yinyang_*` series, `youwon_index21_audit.py`, `WITTEVEEN_IDENTITY_AUDIT.md`) still exist and carry material this folder lacks, e.g. the "479 balance" zeroing reading (14 §M4). They also carry retracted chains presented as verified, so read them with 05 in hand. |
| `E:\testing-btc-p\fresh-start\` | `EVIDENCE_FIRST_REPORT.md`, `AUTHENTICATED_STAGES`, `derived\canonical_chain.json` (status `REPRODUCIBLE_UNAUTHENTICATED_PADDING_CHAIN`), `derived\chain4.bin`, experiment reports. **Terminal loader bug** (§1). |
| `C:\Users\lucas\Desktop\idk-btc\` | `adversarial-review\`, `verify-work\`, `known-real\VERIFICATION.md`, `telegram-export-9.8.26\txt\`. **Wrong Better Half target** (§1). |
| `C:\Users\lucas\Desktop\8.7-fresh-start\` | clean-room digests, `artifacts\pipeline_enum_hits.json` |
| `C:\Users\lucas\Desktop\5g\` | `analysis\tried_log_v2.txt`, `tried_log_v3.txt`; Reddit captures `reddit1.txt`, `reddit2.txt` (source for the hint-edit diff, 03 §13) |
| `C:\Users\lucas\Desktop\read\` | `PUZZLE-REVIEW\` newer reports, `dbbi_state.txt` (newer than the copy in rabbit-combined) |
| `C:\Users\lucas\Desktop\gsmo-links\deep-research-2026-09-12\` | 855-file deep research bundle (`REPORT.md`); Decentraland L−R detail PNG |
| `C:\Users\lucas\Desktop\test\audit` | audit workspace (hint-audit, exact_binary_recipe, film/architect-diff, adversarial review) |
| `D:\rabbitv2\rabbit\` | `mod.npy` (13×14 int array, origin unknown), `analysis\out\nest_module_door1.txt` |
| `D:\5btc\` | `independent-analyst-report-2026-09-08.md`, `hint-photos\` (108 files); one wrong salt (§6) |
| `E:\rabbit-combined\rabbitv3\rabbit\analysis\out\` | row selector, gate audit, `bit167_constraints_2026_09_11`, `finite_crossproduct_2026_09_11`, `specified_constructions_2026_09_11\decisions.json`, `rabbit_tabs_2026_09_10`, `rebus_visual_audit_2026_09_10`, live CDX status csv; `rabbitv3\.firecrawl\live-root.html` |
| `D:\C-drive-relief\2026-08-22\CodexSessionsArchive\` | archived Codex rollouts (Aug 2026) |
| GitHub (not fetched) | private `AppleLamps/rabbitv2` (full chat text, 61,418 msgs), `AppleLamps/clean-btc`, `jackdevs66/GSMG5_CDuality` (210-combination Cosmic claim; one pad hit has ~36% chance), `keyjoke/vs-kangaroo-hybrid`, puzzlehunt issues #69–#110, Naddiseo, HosterjackAGV, bitcointalk 5151725 / 5532424 |

Lost: `E:\rabbitv3\rabbit\LOCKED_ENVELOPES_REPORT_2026-09-10.md`, `PUZZLE_REASSESSMENT_…`, `UNLOCK_CHAIN_REPORT_…`, `PASCAL_LINK_REVIEW_…` (removed as superseded in a Codex session; numbers survive only in the log). `telegram\files\key.py` (#65925 attachment) is not in the relocated puzle copy.

## 8. Site state additions

- Live root page (captured 2026-09-12 by a Codex session, `rabbitv3\.firecrawl\live-root.html`): "2017 — 2026 / The lights are off. / Nine years of chaos ended. One mystery remains. / Follow the white rabbit →" linking to `/puzzle`. [log]
- `robots.txt`: ASCII art plus `Disallow: /`. 403 CDX URLs live-checked: 19 return 200, 384 return 404. [log]
- 2026-08-04: some non-puzzle paths served a parking template (body 1029 + 3 × len(path) B). A Wayback 2026-07-08 capture of a `4f7a1e…` path shows a domain-for-sale page (DNS 103.224.212.141). Both are consistent with "unknown path ≠ door". [log]
- The user probes gsmg.io live; do not brute-force the site.

## 9. User intent recorded in the logs

- Wants gates that recognise **intermediate instructions**, not only prize keys ("maybe it shouldn't be checked against the prize key", 2026-08-07). This matches 05 §2.
- Asked for one fully specified chain executed with no heuristic gates and all rejections logged. A Codex session concluded that no single fully specified chain exists in the record (2026-09-11).
