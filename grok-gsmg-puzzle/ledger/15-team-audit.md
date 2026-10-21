# 15 — Team audit: missed items & mistakes (Composer agents)

**Date:** 17 Oct 2026  
**Agents:** Skeptic · Archivist · Reader · Cryptanalyst · Tester  
**Scope:** `/workspace` offline GSMG repo; no new large decrypt sweeps in this round.

---

## Executive summary

The **byte-level [V] chain** (`archivist_check2.py` 106/106) and **artifact decrypt counts** (rounds 2–7 reconcile to JSON) are trustworthy. What failed is **coverage claims**, **null-methodology**, and **a few implementation bugs** that make some “falsified” labels too strong.

**Do now (process):** treat Reader extended rows and H2/H3 as **open** until run; qualify R7 `reader_TSC` / pad-gated chains; fix KDF probes; unify detectors.

**Do not claim:** handoff **200k dbbi shuffle** reproduced (repo uses simplified 10k host-string null); **full quintuple** filler deletion run; **Cosmic raw32** on H1 paths tested.

---

## CRITICAL

| # | Issue | Action |
|---|--------|--------|
| C1 | **`double-hex` cosmic probe** in `round7_chained_pipeline.py` duplicates `std-hex` — probe never ran | Fix or remove; re-label `ledger/14-round7.md` cosmic KDF row |
| C2 | **`dbbi_shuffle_null_10k`** uses wrong 23-host string (`…BBYY` vs handoff `…BFYY`) — not handoff [T] shuffle | Retract as reproduction; rename in `ledger/08-round2.md` or reimplement |
| C3 | **Hard limits** | **PASS** — no live submit / HTTP puzzle calls in `team/` or `src/` |

---

## HIGH — science & coverage

| # | Issue | Notes |
|---|--------|--------|
| H1 | **STOP list (R5):** quintuple filler sample + **M4** Bifid tail → §4.1 after brainstorm STOP | Document exception or accept violation |
| H2 | **H1 / Reader T→S→C / m3 baselines** use **std-hex on Cosmic**; M1 prereg assigns **raw32** on Cosmic — “falsified” is **KDF-conditional** | Re-run H1 with Cosmic `raw32` or downgrade claims |
| H3 | **`reader_TSC` = 4 decrypts** — chain never left Terminal step 0 | Not a counter bug; **overstated falsification** in `14-round7.md` |
| H4 | **Reader table still open:** Cosmic title, Sal full 1075, #6913 bit-width, shabefour/our, Bifid periods ≠570, dbbi past 97, roses tuples, **H2/H3** strategist | See `ledger/round5/reader.md` + Reader agent TOP 15 |
| H5 | **Batteries trust `artifacts/*.bin`** — most §4–§6 structural [V] rows never re-decrypted in `team/` | Archivist OK; **tester scope ≠ reproduction scope** |
| H6 | **`MASK6` includes pins {1,3}→`yM`** — not handoff §6.3 [V] (only 557→`yI u`, quad→`szqu`) | Label [R] in ledgers when citing mask6 zero |

---

## HIGH — implementation (Cryptanalyst)

| # | Issue | File |
|---|--------|------|
| I1 | M3 generic chain **middle step `plain-md5`** not in M3 spec | `round7_chained_pipeline.py` |
| I2 | **`list_row_sums_sep`** in prereg JSON but missing from `msl_catalog()` | `round7_chained_pipeline.py` |
| I3 | **`round5_preregistered` M1–M5** budgets in ledger (240–480) vs actual **48–112** | `ledger/round5/cryptanalyst.md` vs code |
| I4 | **M3 step gating** — step 3 runs when step 1 ≠ `no-pad` without step 2 pad | `round5_preregistered.py` |
| I5 | **Two detectors:** `classify_plaintext` (SHA/R7) vs `step1_btcseed.classify` (MD5 rounds) — hex/JSON PEM may be **missed** on SHA path | Unify or document |

---

## MEDIUM

- **Handoff §9** “deletion not tried” stale in `uploads/`; repo truth in `ledger/experiments.md`.
- **README** still points “latest” at round6; round7 exists.
- **EVP-MD5** not fully fair across 3 containers per `ledger/round5/skeptic.md` fairness note.
- **Win test:** batteries mostly `is_win_uncompressed(sha256(answer))`, not **plaintext 32-byte key** / WIF in decrypt body (`pubkey_hash160s` in `step1` unused in chains).
- **Round 5** `enter.join(row_sums)` recipe shape likely unintentional (`round5_battery.py`).
- **Planted control** only inside M1 in `round5_preregistered.py`.

---

## LOW

- Dead `n += 0` in `run_h1_fixed_chain`.
- Tester driver script not in repo (artifact + ledger only).
- Naming `mdp5_*` typos.

---

## Reconciled decrypt totals (~1.79M)

| Source | Decrypts |
|--------|----------|
| Tester 9-blob | 34,669 |
| R2–R4 | 1,686,764 |
| R3 MD5+filler | 16,081 |
| R5 pilot + prereg | 16,033 |
| R6 | 460 |
| R7 | 34,434 |
| Cryptanalyst + deletion + step3 | ~10k+ |

Ledgers match JSON for spot-checked rounds.

---

## Recommended next work (priority)

1. ~~Reader gap rows 1–7~~ — **done** (`ledger/16-round8.md`).
2. ~~Reader G8–15 + classify + H1 Cosmic raw32~~ — **done** (`ledger/17-round9.md`).
3. ~~**Methodology:** dbbi host, `planted_control` on preregister + deletion sweep~~ — **done** (`ledger/18-round10.md`).
4. ~~**§9 / experiments alignment**~~ — **done** (handoff footnote + `experiments.md`).

---

## Agent IDs (traceability)

- Skeptic: `bc-730a8169-27ec-5c77-8d6a-0cc9009b72d7`
- Archivist: `bc-068067a8-a2ca-53d7-ac4a-a160967a54fb`
- Reader: `bc-9067207d-8198-52a4-ac8d-07376ba240f0`
- Cryptanalyst: `bc-06220393-e191-57b1-8230-031493994a72`
- Tester: `bc-5084724f-d1c6-520e-ba1f-29cf9b31cad2`
