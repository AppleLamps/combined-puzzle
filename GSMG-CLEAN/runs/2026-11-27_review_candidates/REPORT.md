# NULL: Bounded Cosmic Replay — Three Reviewer Families (`2026-11-27_review_candidates`)

**Verdict: NULL.** 20 candidates × 3 locked envelopes = **60 decrypts** under profile `gsmg` only (`lowercase sha256(answer)` hex passphrase, OpenSSL `EVP_BytesToKey` SHA-256 1 iteration, AES-256-CBC, strict PKCS#7). **1** pad-valid output (`salphaseion_short`, `cand_20` = `X2SH4Y0QB15`, pad = 1, 79 B, 41.8% printable ASCII, random bytes, 0 key hits); **0** pad ≥ 2, **0** pad ≥ 3, **0** outputs > 85% printable, **0** Half or Better Half key matches, **0** DBBI equality-pattern matches. Both controls passed.

---

## 1. Preregistration and Provenance

Because `tools/prereg.py seal` refuses any run directory containing files other than `PREREG.json`, preregistration was performed cleanly in two sealed steps **before any decryption ran**, without moving or hiding files:

1. **Step 1 (empty-dir seal):** Wrote `PREREG.json` declaring the exact 20 candidates across the three families, profile `gsmg`, controls, and `candidate_bound: 20`. Ran `python tools/prereg.py seal runs/2026-11-27_review_candidates` while the directory contained only `PREREG.json`.
   - Sealed UTC: `2026-11-27T19:51:33Z`
   - `PREREG.sealed` SHA-256: `d0e90059333c66804f9fa498e0f822b6125bd4a7c30dff78081be7f611e3f3e6`
2. **Step 2 (candidate build + coverage grep + second seal):** Built `candidates.txt` via `replay.py build`, importing `P1`, `P2`, `P3`, `P32`, `CAP`, and `SLUG` directly from `tools/verify_chain.py` (with `P2` and `P32` extracted from `verify_chain.py`'s AST so no phase answer was retyped) and asserting before use that:
   - `sha256(P1) == 5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75`
   - `P2` reopens the Phase 2 envelope to `phase2_plaintext.bin` (648 B)
   - `P3` reopens the Phase 3 envelope to `phase3_plaintext.bin` (4,090 B)
   - `P32` reopens the Phase 3.2 envelope to `phase3_2_plaintext.bin` (2,422 B)
   - `sha256(CAP) == SLUG` and `SLUG` is present in `originals/cdx_wayback_gsmg.json`

   Then ran `replay.py grep` and bound `candidates.txt` to `PREREG.sealed` via `python tools/prereg.py record runs/2026-11-27_review_candidates --outcome passed --evidence runs/2026-11-27_review_candidates/candidates.txt` (`SELFCHECK.json`, recorded `2026-11-27T19:52:53Z`, `candidates.txt` SHA-256 `ab5da4f35196aea6afd832f49b335605be4968606966403c761236cdecd0b077`).
3. **Step 3 (decrypt):** `replay.py run` re-verified `prereg.verify()` and `SELFCHECK.json` against `candidates.txt` before executing any control or envelope decryption.

### Exact Candidate List (20 strings, no other variants)

| # | Family | Label / String | Len | SHA-256 (prefix) |
|---:|---|---|---:|---|
| 1 | F1 cross-phase | `P1+P3+P32` | 342 | `f889c010da1915ea` |
| 2 | F1 cross-phase | `P1+P2+P3+P32` | 351 | `646a9dc593a8a32f` |
| 3 | F1 cross-phase | `P3+P32` | 289 | `f8328e45e85dd882` |
| 4 | F1 cross-phase | `P1+P2+P32` | 124 | `d9d1d6f6d2067c94` |
| 5 | F1 cross-phase | `P1+P3+P32+CAP` | 401 | `40e589f8fa731375` |
| 6 | F1 cross-phase | `P1+P3+P32+SLUG` | 406 | `bd11c7e7aed7fcc0` |
| 7 | F2 duality text | `theseedisplantedwhenoppositesattract` | 36 | `59f2aa931d8fd9dd` |
| 8 | F2 duality text | `whenoppositesattract` | 20 | `77d3199d06f49a87` |
| 9 | F2 duality text | `oppositesattract` | 16 | `8b7259160e2b0f4c` |
| 10 | F2 duality text | `The seed is planted when opposites attract` | 42 | `b9cbe557a97e9694` |
| 11 | F2 duality text | `theseedisplantedwhenoppositesattracttheflowerblossomsthroughwhatseemstobeaconcretesurface` | 89 | `ef37ded01cba30c9` |
| 12 | F2 duality text | `mysteriesoftheunknowncosmicduality` | 34 | `92205a7b2deaeaae` |
| 13 | F2 duality text | `Mysteries of the Unknown: Cosmic Duality` | 40 | `a67e3b286b129455` |
| 14 | F2 duality text | `0809465175` | 10 | `871f6094f8ba123f` |
| 15 | F2 duality text | `0809465167` | 10 | `61772033efa3e5e7` |
| 16 | F3 roadmap / Phase 2 | `yellowblueprimesmatrixsumlistlastwordsbeforearchichoice` | 55 | `7f81ffcc18c548fa` |
| 17 | F3 roadmap / Phase 2 | `choiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecialdessertiwroteitmyself` | 94 | `d5765dc8d929f448` |
| 18 | F3 roadmap / Phase 2 | `theseedisplantedchoiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecialdessertiwroteitmyself89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32` | 174 | `f21eb9623a8c4609` |
| 19 | F3 roadmap / Phase 2 | `# X 2 S H 4 Y 0 Q B 15 #` | 24 | `c010f535bd4a311f` |
| 20 | F3 roadmap / Phase 2 | `X2SH4Y0QB15` | 11 | `91f25f4a2459ef5b` |

---

## 2. Pre-Run Coverage Grep

Every valid Cosmic null candidate set in the repository was grepped (exact string, SHA-256 hex, and UTF-8 hex) before decrypting (`coverage_grep.json`, plus direct raw-text check on `zero_envelopes` arms A and C):

| Prior valid Cosmic null source | Path checked | Exact AES-tested hits | Notes |
|---|---|---:|---|
| `gapset_v2` | `GSMG-CLEAN/runs/2026-11-27_cosmic_null_validity/gapset_v2/gap_candidates.txt` (3,461) | **0** | None of the 20 present |
| `matrixsum_replay` forms | `GSMG-CLEAN/runs/2026-11-27_matrixsum_replay/forms.txt` (9,236) | **0** | None of the 20 present |
| `fefefe_replay` | `GSMG-CLEAN/runs/2026-11-27_fefefe_replay/candidates.txt` (106) | **0** | None of the 20 present |
| `zero_envelopes` | `GSMG-CLEAN/runs/2026-09-13_zero_envelopes/arm_{A,C}_candidates.json` (raw text) | **0** | 0 raw substring hits in both JSONs |
| `exp2_first_hint_last_command` | `GSMG-CLEAN/runs/2026-09-14_adversarial_reanalysis/exp2_first_hint_last_command/` | **0** | 0 hits in `results.jsonl.json` and `run_exp2.py` |
| `cosmic_six_hash` | `GSMG-CLEAN/runs/2026-11-27_cosmic_six_hash/{results.json,followup.txt}` | **0** | 0 exact or `inner_sha256` hits |
| `gsmg-haiku/review_leads` | `gsmg-haiku/review_leads/**` (127 files) | **0** (6 substring matches in non-AES / doc files) | See breakdown below |
| `seven_key_bifid` *(bonus)* | `GSMG-CLEAN/runs/2026-09-13_seven_key_bifid/candidates.json` (59,976) | **0** | None of the 20 present |
| `last_words_referents` *(bonus)* | `GSMG-CLEAN/runs/2026-09-13_last_words_referents/*` (15,676) | **0** | None of the 20 present |

**Breakdown of the 6 substring matches in `gsmg-haiku/review_leads/**` (none tested on Cosmic AES):**
- Candidate #16 (`yellowblueprimesmatrixsumlistlastwordsbeforearchichoice`) matched as a **substring** of the full `#8446` string (`...yinyang...`) in 4 documentation/input files (`CREATOR_CHAT_REVIEW_2026-10b.md`, `cryptanalysis_2026_10_15/inputs/hint8446-exact.txt`, `cryptanalysis_2026_10_15/README.md`) and in `ltc_scan2/ltc_scan2.py:39` (which tests `...yinyang` with `yinyang` appended as a BTC/LTC brainwallet address only, never AES).
- Candidate #17 (`choiceisanillusion...`) and Candidate #19 (`# X 2 S H 4 Y 0 Q B 15 #`) appeared only in prose inside `cryptanalysis_2026_10_15/inputs/public-walkthrough.md`.
- **0 of the 20 candidates** were previously tested against Cosmic Duality (or any locked envelope) under profile `gsmg`.

---

## 3. Controls

1. **`cc.selftest()`:** **PASSED** — reopened the real Phase 3.2 envelope (`pad = 10`, `2,422 B`), verified Half's `hash160` (`a9553269572a317e39f0f518cb87c1a0ee1dbae4`), EC `k=1`, WIF, raw32/hex64 detectors, and DBBI equality-pattern helper.
2. **Planted control envelope through identical code path (`decrypt_and_scan`):**
   - Synthetic `Salted__` blob (salt `0102030405060708`) encrypted under profile `gsmg` with answer `planted_control_review_candidates_2026_11_27`, encrypting a 168-byte plaintext containing `k=1` in three forms (`raw32`, `WIF`, `hex64`, expected PKCS#7 pad = `8`).
   - Run through `decrypt_and_scan()` alongside all 20 real candidates (21 decrypts total) with `k=1` temporarily added to `cc.TARGETS`:
     - Planted answer opened with **`pad = 8`**, byte-exact plaintext match (`controls/planted_control/cand_01.bin`).
     - `cc.find_keys()` fired on all three key formats: `['WIF', 'hex64', 'raw32']`.
     - Real candidates gave `0` pad hits on the planted envelope.
     - `cc.TARGETS` was restored and asserted to contain only Half (`1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`) and Better Half (`17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`).

---

## 4. Results

Profile: **`gsmg` only** (`sha256(answer).hexdigest()` ASCII passphrase → `EVP_BytesToKey(SHA-256, 1 iter)` → AES-256-CBC → strict PKCS#7).
Chance expectation per envelope for `N = 20`: `pad ≥ 1` = `20/256 = 0.0781`; `pad = 1` = `20 × 255/65536 = 0.0778`; `pad ≥ 2` = `0.000305`; `pad ≥ 3` ≈ `1.19 × 10⁻⁶`. Combined across 60 decrypts: `pad ≥ 1` expected = `0.2344` (`Poisson P(X ≥ 1) = 0.209`).

| Envelope | Salt | Decrypts | pad = 0 | pad = 1 | pad ≥ 2 | pad ≥ 3 | Expected pad ≥ 1 (1/256) | Key hits | >85% printable |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `terminal_phase3_2_end` | `b45a5e3d827593ca` | 20 | 20 | 0 | 0 | 0 | 0.078 | 0 | 0 |
| `salphaseion_short` | `3ab585348552415d` | 20 | 19 | 1 | 0 | 0 | 0.078 | 0 | 0 |
| `cosmic_duality` | `2d3f6fe06dc950e6` | 20 | 20 | 0 | 0 | 0 | 0.078 | 0 | 0 |
| **Total** | | **60** | **59** | **1** | **0** | **0** | **0.234** | **0** | **0** |

### Retained Pad-Valid Outputs (all checked with `cc.find_keys`)

| Envelope | Cand # | Candidate | Pad | Bytes | Printable fraction | SHA-256 | `.bin` file | `cc.find_keys` hits (Half / Better Half) |
|---|---:|---|---:|---:|---:|---|---|---|
| `salphaseion_short` | 20 | `X2SH4Y0QB15` | 1 | 79 | `0.417722` (41.8%) | `69d756b5ed0b611d...` | `outputs/salphaseion_short/cand_20.bin` | **0** |

- Outputs with printable fraction `> 0.85`: **none (0)** — no first-200-byte text block applies.
- DBBI equality-pattern matches: **0**.

---

## 5. Verdict and Files

**Verdict: `NULL`.** None of the 20 reviewer candidates opens `terminal_phase3_2_end`, `salphaseion_short`, or `cosmic_duality` under the pinned `gsmg` profile. The lone pad-1 output (`salphaseion_short`, `X2SH4Y0QB15`, 41.8% printable) is chance-rate random bytes (`Poisson P(X ≥ 1 | λ = 0.234) = 0.209`) with zero Half or Better Half key matches.

Files in `GSMG-CLEAN/runs/2026-11-27_review_candidates/`:
- `PREREG.json`, `PREREG.sealed`, `SELFCHECK.json`
- `replay.py` (`build`, `grep`, `run`)
- `candidates.txt`, `provenance.tsv`, `candidates_manifest.json`
- `coverage_grep.json`, `results.json`, `REPORT.md`
- `controls/planted_control/cand_01.bin`
- `outputs/salphaseion_short/cand_20.bin`
