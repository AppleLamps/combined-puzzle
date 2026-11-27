# NULL: Six-Slot Resolved Replay (Part 1) & Haiku `hash_scope` Replay (Part 2)

**Result: NULL.** Ran **141,666** total AES-256-CBC decrypts across all 3 envelopes in `cc.ENVELOPES` (**26,198** Part 1 candidates = **78,594** decrypts; **21,024** Part 2 passphrases = **63,072** decrypts). Retained all **608** pad-valid plaintexts as `.bin` files and ran both `find_keys` and the `cosmic_binary_scan` `scan.py` checks on every single one. **Key hits: 0. Binary-scan flags: 0. Printable > 0.8: 0. Pad >= 2: 2.** All controls passed.

## Preregistration & Controls

- **PREREG seal (`PREREG.sealed`):** `e892f4bd26f38c53959d9a6b2dbd3fec76ae97351ca6b25ad25cbc61aaf454eb` (sealed before any decryption).
- **Part 1 candidate list (`part1_candidates.txt`):** `3b6984960c472fb3bb1f327f6db5dde4225f0b808a43071d0b8f8a45d9edf9d9` (26,198 unique strings).
- **Part 2 passphrase list (`part2_passphrases.tsv`):** `651c029ffcf7fbd747124dd65cc80f24d46c70e5f2f43a29f8d122378aaa5f3e` (21,024 unique passphrases).
- **Harness & parity controls:** `cc.selftest()` PASSED (Phase 3.2 opens at pad=10, 2,422 B; Half hash160, EC `k=1`, WIF, raw/hex detectors); `cosmic_binary_scan/scan.py:selftest()` PASSED (22 positive vectors, 0 flags on 1,327 B negative control); `coincurve` parity verified against pure-Python `cc.scalar_hits` on 20 scalars; fast last-block CBC decrypt verified identical to `cc.try_envelope`.
- **Part 1 planted control (`controls/part1/planted_part1/`):** PASSED — recovered exact plaintext (`pad=9`, `231 B`, sha256 `f7b9f3932af054d6...`), `find_keys` fired on all 4 formats (`WIF, base64, hex64, raw32`), and `scan.py` flagged `magic_pdf, printable_gt_0_8, repeated_16b_block`.
- **Part 2 planted controls (`controls/part2/`):** PASSED on both arms — `outer-sha256-raw` (`pad=14`, `210 B`, `find_keys`: `WIF, base64, hex64, raw32`, `scan.py`: `magic_png, printable_gt_0_8, repeated_16b_block`) and `outer-sha256-hex` (`pad=13`, `211 B`, `find_keys`: `WIF, base64, hex64, raw32`, `scan.py`: `magic_pdf, printable_gt_0_8, repeated_16b_block`).
- **Targets verified after controls:** `a9553269572a317e39f0f518cb87c1a0ee1dbae4` (Half `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`) and `4bc468447fe1b048ad030a2f9a125478eabc4ed6` (Better Half `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`).

## Part 1 — Resolved Values in the Frozen Six-Slot String

- Frozen six-slot order (`SALPHASEION_PREREGISTRATION.md` lines 16–21): `matrixsumlist | lastwordsbeforearchichoice | thispassword | shabefourfirsthintisyourlastcommand | enter | shabefanstoo`. Separators: `""` and `"z"`. Slots 3–6 literal; no `yinyang` anywhere.
- Sets: `|A_core| = 68` (58 `salphaseion_roles` + 10 explicit `563/497` forms), `|A_pipeline| = 9,236` (`#8446` forms), `|B| = 55` (22 `salphaseion_roles` + 33 from the 8-base `PRE`/`DIG`/`RID` joins via `forms()`).
- Construction: (a) `A_core × B` × 2 seps + (b) `(A_core ∪ A_pipeline) × literal_B` × 2 seps + (c) `literal_A × B` × 2 seps → **26,198** unique candidates → **78,594** decrypts under pinned `gsmg` profile.

| Envelope | Decrypts | Pad-1 | Expected (N/256) | Poisson P(X >= pad-1) | Pad >= 2 | Retained `.bin` |
|---|---:|---:|---:|---:|---:|---:|
| `terminal_phase3_2_end` | 26,198 | 111 | 102.34 | 0.2081 | 1 | 112 |
| `salphaseion_short` | 26,198 | 119 | 102.34 | 0.0577 | 0 | 119 |
| `cosmic_duality` | 26,198 | 98 | 102.34 | 0.6791 | 0 | 98 |
| **Pooled** | **78,594** | **328** | **307.01** | **0.1217** | **1** | **329** |

- **Any `pad >= 2`:** 1
- **Any `printable > 0.8`:** 0
- **Any binary-scan flag (Cosmic Duality / SalPhaseIon short):** 0 (all 3 envelopes: 0)
- **Any `find_keys` hit:** 0

### Notable / Flagged / `pad >= 2` Records

| Envelope | File | Candidate / Label | Pad | Size | First 16B hex | H (bits/B) | Printable | Binary flags | `find_keys` |
|---|---|---|---:|---:|---|---:|---:|---|---|
| `terminal_phase3_2_end` | `outputs/part1/terminal_phase3_2_end/0047.bin` | `IEQHARNOUVIEANzlastwordsbeforearchichoicezthispasswordzshabefourfirst...` | 2 | 78 | `46b95d72b1fb6452f3731615db0547cd` | 6.0962 | 0.410 | none | none |

## Part 2 — `gsmg-haiku` `hash_scope` 876-Partition Replay

- Regenerated from `gsmg-haiku/review_leads/hash_scope.py:group_hashes()` (876 set partitions into ≥ 2 groups × 2 orders × 2 inner forms `hex`/`raw` × 2 joins `concat`/`interleave` = 7,008 unique bodies × 3 outer arms: `as-password` 7,008, `outer-sha256-hex` [pinned `gsmg`] 7,008, `outer-sha256-raw` 7,008).
- Count confirmation vs `HASH_SCOPE_REPORT.md`: **21,024** generated; skipping the **252** contiguous `outer-sha256-hex` passphrases from `next_tests.py:partitions()` reproduces **20,772** unique passphrases × 3 = **62,316** AES trials (exact match to `HASH_SCOPE_REPORT.md` line 10). This replay runs all **21,024** passphrases (**63,072** decrypts) with full retention, `find_keys`, and `scan.py`.

| Envelope | Decrypts | Pad-1 | Expected (N/256) | Poisson P(X >= pad-1) | Pad >= 2 | Retained `.bin` |
|---|---:|---:|---:|---:|---:|---:|
| `terminal_phase3_2_end` | 21,024 | 83 | 82.12 | 0.4762 | 1 | 84 |
| `salphaseion_short` | 21,024 | 102 | 82.12 | 0.0188 | 0 | 102 |
| `cosmic_duality` | 21,024 | 93 | 82.12 | 0.1271 | 0 | 93 |
| **Pooled** | **63,072** | **278** | **246.38** | **0.0254** | **1** | **279** |

- **Any `pad >= 2`:** 1
- **Any `printable > 0.8`:** 0
- **Any binary-scan flag (Cosmic Duality / SalPhaseIon short):** 0 (all 3 envelopes: 0)
- **Any `find_keys` hit:** 0

### Notable / Flagged / `pad >= 2` Records

| Envelope | File | Candidate / Label | Pad | Size | First 16B hex | H (bits/B) | Printable | Binary flags | `find_keys` |
|---|---|---|---:|---:|---|---:|---:|---|---|
| `terminal_phase3_2_end` | `outputs/part2/terminal_phase3_2_end/0050.bin` | `groups=[[0, 2, 3], [1], [4, 6], [5]]/reverse=False/hex/concat/as-pass...` | 2 | 78 | `385134297a4d8e2875bf3f6f1ea36a0c` | 6.0290 | 0.359 | none | none |

## Files

| File / Directory | Description |
|---|---|
| `replay.py` | Preregistration builder, planted-control harness, dual replay, and report generator |
| `PREREG.json`, `PREREG.sealed` | Pre-decrypt sealed specification and SHA-256 seal |
| `part1_candidates.txt` | All Part 1 candidate strings (verbatim, LF) |
| `part2_passphrases.tsv` | All Part 2 passphrases (`label\tpw_hex`, LF) |
| `controls/part1/`, `controls/part2/` | Retained planted control decrypts |
| `outputs/part1/`, `outputs/part2/` | Every retained pad-valid plaintext (`.bin`) across all 3 envelopes |
| `results.json` | Full machine-readable histograms, controls, and per-retained-file scan metadata |
| `REPORT.md` | This report |
