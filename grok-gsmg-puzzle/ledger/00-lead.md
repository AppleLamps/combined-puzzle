# Lead log

## Round 0 (17 Oct 2026)

- **Archivist:** `src/archivist_check2.py` → **106/106** PASS on second-build handoff. Merged to `main`.
- **Agents:** Composer **2.5** via Task tool (Reader, Cryptanalyst, Statistician, Tester, Skeptic).

## Round 1 report (Composer team)

### 1. Reproduced

| Source | Result |
|--------|--------|
| Archivist | 106/106 [V] checks, zero mismatches |
| `check_report3_2026-10-17.py` | 8/362 880 Bifid squares; mask6 84/230 interior; URL/host bit splice |
| Cryptanalyst | 18/18 self-checks; 108 decrypts; planted §4.1 control OK |
| Tester | 34 669 decrypts on 9 blobs; planted control OK; pads ≈ chance |

Hard limits: no live gsmg.io submission in repo scripts (Skeptic **PASS**).

### 2. Findings

**Why we are stuck:** The solved chain (phase 2→3.2) is **literal on procedure** but **interpretive on part strings** ([R]). Everything after phase 3.2 is **named operands without operations**: `matrixsumlist`, `lastwordsbeforearchichoice`, `yellowblueprimes` decode to labels or #8446 ordering, not to inputs that §4.1 passwords have consumed successfully.

**faed / Bifid:** Period-570 Bifid yields prefix `btcseedd` but **8/362 880** square orderings share it; tail is not ASCII under Beaufort(`btcseed`) or whole-block decimal. **mask6 zero** pins `yM`/`szqu` but interior printable rate matches chance; **mask6 deletion** is null (pins lost).

**Containers:** Under **§4.1 std-hex**, fixed operands (#8446 string, flower, tok23×matrix sums, mask6 hash, recipe concat) → **0** structured plaintext across terminal / SalPhaseIon-short / Cosmic (+ yin-yang XOR variants). Community SalPhaseIon recipe uses **EVP-MD5** and yields non-text — not reproduced as a win path.

**Epistemic (Skeptic):** Tail `szqu` and `btcseed` are **[V] search artifacts**, not checksums; README/handoff §9 still says “deletion not tried” while repo **has** run mask6 deletion → document drift.

### 3. Open (Round 2 priorities)

| P | Owner | Action |
|---|--------|--------|
| P0 | Tester | **2⁶ deletion masks** on faed → bytes → §4.1 — **done** (`ledger/07-deletion-sweep.md`, null); next: arbitrary-position deletion on fillers/dbbi |
| P0 | Reader + Cryptanalyst | Define **one** pre-registered recipe: what is summed in `matrixsumlist`, what text is `lastwords` (Architect windows vs film), then `enter` → which container |
| P1 | Cryptanalyst | **8 Bifid squares** full plaintexts × §4.1; Beaufort keys beyond `btcseed` |
| P1 | Reader | **New Year dots** 1..5 as encoding; **another door** {1,4,21} with #6913 A/R/B |
| P2 | Statistician | Re-run **dbbi 200k shuffle** null with frozen rule in repo script |
| P2 | Lead | Align handoff §9 with deletion experiment; tone down prefix-only `btcseed` in README |

**Top untested readings (Reader):** (1) letter deletion broadly, (2) dot-count channel separate from #53342 ASCII, (3) another-door coordinates.

## Round 2 (17 Oct 2026)

- **P1 batteries:** `team/round2_battery.py` — 960 decrypts, **null** (`ledger/08-round2.md`). Pre-registered recipe documented; `lw-arch-tail40` = `primebasicsafterwhichyouwillberequiredto` (already in prior fixed-string tests as `afterwhich…` variant).
- **Round 3:** `team/round3_battery.py` — EVP-MD5 **151** tries (community literal reproduces 79 B pad only); **1770** filler pair deletions × §4.1 **null** (`ledger/09-round3.md`).
- **Round 4:** `team/round4_battery.py` — **1.67M** §4.1 null (`ledger/10-round4.md`).
- **Round 5–8:** … + Reader gap G1–G7 pilot **1 995** decrypts, **null** (`ledger/16-round8.md`).
- **Open:** H2/H3 strategist batteries; Sal full-page key; Cosmic title; #6913 bit-width; quintuple filler deletion.

**Chained pipeline (R7):** H1, M3, 6 orders, hash-chain without plaintext, yinyang mid-chain, XOR enter hops, liberal raw-CBC enter — **34,434** tries, **0** structured (`ledger/14-round7.md`).

**Team audit (R15):** five Composer agents — coverage gaps, KDF/detector bugs, overstated falsifications (`ledger/15-team-audit.md`).

**Round 9:** Reader G8–G15 + unified classify + H1 Cosmic raw32 audit — **2 000** decrypts, **null** (`ledger/17-round9.md`).

**Round 10:** Audit cleanup (dbbi host, controls, §9) + **G12** phase-3 part falsification (`ledger/18-round10.md`).

**Round 11:** Sal **enter**-split layout check + Terminal-first chain + joint #8000 door/zero — **null** (`ledger/19-round11.md`).

**Round 12:** z-stage program + pre-decode b64 joins + liberal Terminal-first — **2 000** decrypts, **null** (`ledger/20-round12.md`).

**Round 13:** Byte XOR `enter`, poster MSL z-chain, full Sal stage-0 — **1 025** decrypts, **null** (`ledger/21-round13.md`).

**Round 14:** Missed-clue battery (hint pair, door/checker, bifid streams, spiral MSL, yinyang XOR) — **1 688** decrypts, **null** (`ledger/22-round14.md`).

**Detector audit (18 Oct):** the batteries' detector called phase 3.2 itself opaque. All 18 batteries re-run under the kit recogniser with planted controls: 1,763,105 locked decrypts, 6,886 valid pads against 6,914 expected, 0 flagged (`ledger/23-detector-audit.md`).

Index: `ledger/README.md`. Runners: `team/README.md`.
