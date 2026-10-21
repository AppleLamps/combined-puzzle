# 17 — Round 9: Reader gap G8–G15 + audit fixes

**Specs:** `team/preregister_reader_gap9.json`, `team/classify_unified.py`  
**Code:** `team/round9_reader_gap.py` → `artifacts/round9_reader_gap.json`  
**Budget:** 2 000 (filled)  
**Control:** §4.1 `causality` **PASS**

## Audit fixes (R15)

| Fix | Change |
|-----|--------|
| **Unified detector** | `team/classify_unified.py`; `cryptanalyst_tests.classify_plaintext` delegates to it |
| **H1 Cosmic raw32** | `G_audit`: H1-style `s2`/`s3` answers on **Cosmic** with `raw32-sha256` + std-hex (288 tries) |
| **Round 8 detector** | `round8_reader_gap.py` uses `classify_unified` |

## Gaps (Reader rows 8–15)

| Gap | Item | Tries | Result |
|-----|------|------:|--------|
| **G8** | dbbi continuation / alternate colour sequences past pos 97 | 18 | null |
| **G9** | Roses **five** weight tuples → 161 as `msl` + recipe | 40 | null |
| **G10** | Bifid periods **57,95,114,190,285,570** × canonical + **filler** square | 144 | null |
| **G11** | Parse chain: host bits / shabef / dbbi91 → Sal → Cosmic (+ raw32) | 33 | null |
| **G12** | Phase-3 seven-part [R] | — | **Deferred** (interpretive; needs disputed-part study, not bulk decrypt) |
| **G13** | Filler keep **prime indices only** | 4 | null |
| **G14** | New Year **dots** → spiral/sal index channel | 192 | null |
| **G15** | Off-white **F** in dbbi walk (F→Y, F→B, with F) | 18 | null |
| **G2r** | #6913 **21**-bit (+ cosmic **1812**) window replay to budget | 1 263 | null |
| **G_audit** | H1 Cosmic **raw32** repair | 288 | null |

## Result

**0** structured, **0** prize hash160.

## Note

`round2_battery.py` `dbbi_shuffle_sample` still uses a **non-[V]** 23-host string; see `ledger/15-team-audit.md` C2 — not fixed in this round (documentation-only follow-up).
