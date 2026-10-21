# Failed-attempts log: index and crosswalk

**Current crosswalk corrections, 6 October 2026.** Read [doc 119](119-current-evidence-ledger.md)
for interpretation and [doc 118](118-correctness-audit-remediation.md) for detector
limits. Historical controls and zero flags are bounded evidence. Filler purpose,
global L84 exclusion, mandatory envelope order, and a binding of 140 to the
Architect instruction are not established. All original raw run logs are retained.

`claude/FAILED-ATTEMPTS-LOG.md` is a "do not repeat" register for the three locked containers, compiled on 3 October 2026 from the owner's local drives (Desktop, D:, E:). Its original body is retained beneath a dated supersession note. This file says what it adds to the repo, which of its rows the repo already carries, and where the two disagree.

Read the log alongside the dossier, not instead of it. The log's own caveats hold: every row is "ruled out for that candidate set, KDF, password form and validator only", and its counts overlap between sources and must not be summed.

**Source naming.** When the log cites "DOSSIER" it means `D:\GSMG-PUZZLE-DOSSIER.md` or `astra-puz\DOSSIER.md` on the owner's drive, not `claude/GSMG-PUZZLE-DOSSIER.md`. Section numbers mostly line up with the repo dossier (10.1, 10.5, 10.6, 10.7), but not always: the log's "§10.8 (record 122)" PBKDF2 row has no counterpart in the repo's section 10.8. The `D:\5btc`, `astra-puz`, `GSMG-CLEAN` and `8.7-fresh-start` sources are not in the repo.

## 1. Checked against the repo

- **Salts and sizes match.** Decoding `terminal.b64`, `salphaseion-short.b64` and `cosmic-duality.b64` gives salts `b45a5e3d827593ca`, `3ab585348552415d`, `2d3f6fe06dc950e6` and files of 96, 96 and 1,344 bytes, as in log section 1 and dossier 6.5. The phase-3 salt in `phase3.b64` is `9fbc451d13d071f4`, confirming the log's correction of the `35f64511d3d11f4c` mis-transcription.
- **Plaintext sizes match.** Phase-2 plaintext 648 bytes (dossier 3.2, 13) and the phase-3.2 plaintext ending at byte 2,422 (doc 67 errata, doc 59) agree with the log's CRLF-preserving sizes.
- **Cosmic Duality is locked in both.** The log lists it as locked and calls the community 1,327-byte MD5 output (its C1) noise; dossier 10.5 records the same pad-1 false positive. Only the `D:\5btc` register, which the log quotes, still calls it an "opened, unconfirmed candidate".

## 2. Rows the repo already carries

These are recorded in `claude/GSMG-PUZZLE-DOSSIER.md` section 10 (or doc 115) with the same counts. The log adds only its source paths.

| log row | repo location |
|---|---|
| T39 (551,714,300 chain-order combinations) | dossier 10.1 |
| T40 (2^30 corpus subsets) | dossier 10.1 |
| T41 (7,163,600 decrypts, eight ciphers) | dossier 10.1 |
| T42 partly: 475,808 generator, 1,808,960 last-words frames, 2.7M + 5.5M four-slot, 215,550 raw-key | dossier 10.1 |
| T43 (8,812 creator strings) | dossier 10.5 |
| T44 partly: Neo 307, episode 1,586, OP_RETURN 379, film lines 6,720, Infrared | dossier 10.5, 10.1 |
| T46 (all seven runs, 154,784 to ~28M) | dossier 10.7 |
| C1 (community Cosmic "solve"), C5 (605,214 content-judged) | dossier 10.5 |
| C6 (book 1,889,907; Looking Forward 1,311,445; three-slot 82,710) | dossier 10.6 |
| Section 7: verifier (10 submissions), poster has no spare capacity, `#FEFEFE` tests, 479 pointer, rebus 13,264, OP_RETURN spam | dossier 1, 4.6, 10.4, 10.5, 12 |
| Section 7: `matrixsumlist` theorem, 1,224 grid screens, 7,480 stream screens | dossier 10.5 |
| Section 7: faed/dbbi/residue as key material (362,880 relabelings, 1,556,802 substrings, 188,352, 632,944, 13,536, 18.8B nodes, 1,132,326, periods, widths, 21,145 partitions) | dossier 10.2, 10.3 |
| Section 7: Architect decode (Beaufort `thematrixhasyou`, checkerboard 91 letters) | dossier 3.4a, 3.4b |

## 3. Rows that are new to the repo

Nothing below appears in the dossier, doc 115 or doc 67.

- **Section 2, validator defects.** The table of defects that void or weaken older negatives (session 12 ASCII gate, session 13 unpad-before-check bug, 13b odd sizes only, MD5-default harnesses, truncated Terminal loader, the b1 half-blob `z` bug, Base58Check bug before 2026-09-12, CRLF-stripped cached plaintexts). New and worth reading before trusting any pre-September negative.
- **T1 to T26**, the `D:\5btc\verify-work` sessions 2 to 18, including the only fixed-validator XOR-subset runs (session 15 Tiers A, B, C: 1,072,308 + 7,570,104 + 1,072,308) and the bounded b2-as-key/IV layouts (T26).
- **T27 to T38**, the GSMG-CLEAN and clean-room runs: `pipeline_enum` (44,979 paths), `zero_envelopes`, `seven_key_bifid` (1,079,568), `l5_backcheck` (1,117,326,681 digest checks), the 2026-09-14 Moves 0 to 6, the M4 zeroing at 479, Hill recovery tests, classical attacks on dbbi/faed, brute masks, Round 1.
- **T42 remainder**: the SafeNet/Luna count of 550,660 and the 236-token creator vocabulary (732,336).
- **T44 remainder**: prime masks over known answers (220) and `infrared` as 384 strings.
- **T45, REEX 2026-09-21**: 141,846 bases, five password forms, 4,467,816 decrypts.
- **T47** PBKDF2 at 10,000 and 600,000 iterations (90 attempts) and **T48** salts as passwords.
- **S2 to S14** for SalPhaseIon short, including the b1-standalone tiers, the withdrawn `enter484` opening (S8), the retracted 79-byte MD5 output and its WIF (S9), the pre-registration v1 to v22 (71,184), and the untried borrowed-salt b2 reading (S14).
- **C2, C3, C4, C7, C8** for Cosmic Duality (follow-ups on the C1 output, Half/Better Half tests, the matrix range null, the 21-string reader, the `jackdevs66` uniqueness script).
- **Section 6**, the register of retracted and pad-1 openings, with GitHub issue and Telegram references.
- **Section 7 remainder**: the on-chain signature audit (six prize signatures, distinct `r`), the 18 `1GSMG*` vanity hash160s, the `Desktop\1gsmg` forensics, the E1/E3 tests (H1/H2 halves, 15 prime-basic reinsertion, E3 negatives), the "source code pointer" lead (1008 and 868, `TORETURNTOTHESOURCECODES`), and the unrelated puzzles found on disk.
- **Section 8 gaps 1, 4, 6, 7**: the 40-token odd-size universe never re-run with a fixed validator (~38.6M), the 170,295-form trailing-space residue never launched, the borrowed-salt b2, and the scripts with no saved output.

## 4. Where the log and the repo disagree

| topic | log | repo | note |
|---|---|---|---|
| SalPhaseIon short | two halves, b1 (48 B with header) and b2 (48 B, no header), with the 40-bit `enter` field between; b1 alone is a third target with 16 to 31 B plaintext | one 96-B container, the two halves joined (dossier 6.5) | b1-standalone exists only in the log. The joined form is the same bytes. |
| E1 minus VIC, `YOUWON` | "crib-authenticated candidate" | the pivot "cannot coexist with the prime grammar"; creator answered "Pfff. Coincidence." (#70307); `YOUWON` at 21 is p = 0.088 (dossier 8.1, 10.5; doc 67 errata for 81a) | The repo's reading is the later one. Treat the log's word "authenticated" as stale. |
| 481 door paths | tested, all 404 | **void, not null**: the original site returned 200 for every path and today's site is a 2026 rebuild (dossier 10.5) | The log's own section 7 says a Wayback 200 is not evidence, which supports the repo's caution. |
| dbbi residue | "statistically uniform (chi2 12.3, p~0.14), ~190 bits" | faed is non-uniform (chi2 43.7) and the residue fits faed's biased distribution (G = 10.40, p = 0.26); historically interpreted as filler (doc 67 errata for 81b) | Distribution compatibility does not prove no payload or a shared generator; doc 119 supersedes that conclusion. |
| Non-AES-256 coverage | T41 is the "only non-AES-256 coverage"; PBKDF2 on ~40 + 90 candidates | doc 29 also swept 4,153 candidates over EVP and PBKDF2, CBC and ECB, five password forms, both 80-byte containers (dossier 10.1, pad-8 row) | Log gap 2 is narrower than it says. |
| Community Cosmic null | 20,000 random MD5 passwords gave 85 pads; 200,000 XOR-of-labels gave 808 | "808 of 200,000 random passwords" (dossier 10.5) | The repo merges the two controls into one sentence. Same rate (about 1 in 250). |
| Session 15 total | 9,714,720 by output file; README says 9.88M | not in repo | Internal to the log. |
| Centre 4 cells | "not an authenticated payload" | listed as unconsumed surplus (dossier 12) | Compatible: unconsumed, and nothing authenticates a reading. |

## 5. Gap lists side by side

The log's section 8 and doc 115 section 6 list different gaps, and neither covers the other. Doc 115 section 6 is about the doc 115 runs (double-hash forms not run in `h3`, the four large crosses in one order and hex form, the unscripted pools). The log's section 8 is about the older off-repo runs (the 40-token odd-size universe, KDF and cipher breadth, binary intermediates, the 170,295-form residue, borrowed-salt b2, unsaved outputs, unresolved referents). The doc 115 list was closed on 3 October 2026 by doc 116 (null); the log's section 8 list still stands.

## 6. Nulls added on 3 and 4 October 2026 (repo runs, not in the log)

Every row below ran with its planted controls firing in the same run, valid pads at expectation and 0 flags beyond the controls. Testers: `rt` = `claude/riddle-method/rt.py` (6 containers, 4 forms, EVP SHA-256 and MD5, win test); `ms` = `claude/microstep/ms.py` (newline forms); `ct` = `claude/independent-model/ct.py` (14 ciphers x 5 KDFs incl. PBKDF2-SHA256 10,000). Detail in `claude/117-riddle-rounds-and-the-pair-ledger.md`.

| id | what | size | testers | controls | result |
|---|---|---:|---|---|---|
| doc 116 | doc 115 gaps: second order, raw and double-hash forms, five scripted pools, crossed win test | 26.8B decrypts; 195.7M scalars | `h3`, `wintest.py` | four planted `h3` controls; `controls ok` in both win-test orders | null; 1,940 flags, all noise |
| R1-R10 | 23/16/7, door line, `theproblemis`, `wewont`, #225, Smith, `neo`, sha256-each joins | 78 cands, 3,744 decrypts | rt | key 1; phase 2, 3, 3.2 open | null |
| R11-R14 | `yourlife`, `trace`, `infrared`, `theone`/`anomaly` x film last words | 125 / 6,000 | rt | same | null |
| R15-R21 | all earlier answers under 13 more ciphers and PBKDF2; #867 first hint; `giveit` in front; `101`; 3.2 blank choice; self-reference | 528 / 443,520 | ct | 11 planted containers (7 openssl CLI) | null |
| R22-R27 | per-lock split (Terminal left door, short right door, Cosmic the pair) | 25 / 22,200 | rt, ct | both sets | null |
| R28-R30 | `\n`, `\r\n`, ` \r\n` forms of every answer; answers as written; `causality` last | 599 / 106,428 | ms, rt, ct | three planted openssl newline containers, plus the above | null |
| R31 | canonical last-words line, transcript wording, x every ledger M x 9 assemblies | 428 / 426,288 | rt, ms, ct | all three | null |
| R32 | shell history `!!`, `!1` | 6 / 288 | rt | rt set | null |
| R33 | poster remainder: `0000`, `zero`, B+Y = `3` | 198 / 175,824 | rt, ct | both | null |
| R34-R35 | Satoshi's genesis comment block, then the rest of the v0.3.10 construction | 50 / 42,624 | rt, ct | both, plus an openssl container keyed from the candidate file | null |
| structural | solved-gate keys/IVs as scalars, raw-ASCII atoms, every 32-byte and 64-hex window, grid and digit integers | 11,397 tests | `rabbit-holes/structural.py` | poster URL reproduces the `148XH2YBmL` checkpoint | null |
| leak | historical fake-ciphertext and length tests | n/a | `rabbit-holes/leak.py` | short/Terminal random-control lengths mismatched; provenance uncertain | does not establish AES; doc 118 corrects source, no artifact rerun |
| photo | PNG chunks, alpha, hidden marks, logo LSB, QR codewords and RS parity, glyph determinism | n/a | `photo-analysis/photo_checks.py` | a planted panel pixel is found; a planted LSB payload shows; one flipped QR module fails RS parity | no additional payload found in the inspected channels |
| pair (a) | poster row/col sums in six list forms x film last words | 456 / 454,176 | rt, ms, ct | all three | null |

Historical unrun spaces, not queued and not null: pair block (b) (riddle M x 175 `lw_core` windows, about 3,500) and the approved 23/16/7 ordered selection over 23 atoms (about 1.31 billion; stopped twice by an automated safety check).

Reading rule from doc 117 section 11: a joint-password null kills the **pair** tested. The rows above do not strike any single reading of one label off for all partners.
