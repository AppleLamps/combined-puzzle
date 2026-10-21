# 08 — Round 2 batteries (P1)

**Code:** `team/round2_battery.py` → `artifacts/round2_battery.json`  
**Convention:** §4.1 std-hex, containers `terminal` / `salphaseion_short` / `cosmic`  
**Control:** phase-2 `causality` decrypt **OK**

## Pre-registered recipe (matrixsumlist / lastwords)

| Step | Operand | Construction |
|------|---------|--------------|
| yellowblueprimes | `tok23` | 23 consumed spiral colours → `2222252222525222225222525222525` |
| matrixsumlist | `msl-sum-bits` | sum of 104 ab bits in SalPhaseIon [91,195) → **56** |
| matrixsumlist alt | `msl-ab-int`, `msl-row`, `msl-col`, row+col | poster / ab integer readings |
| lastwordsbeforearchichoice | `lw-arch-tail40` | 40 chars before `SELECT` in phase 3.2 Beaufort speech → `primebasicsafterwhichyouwillberequiredto` |
| lastwords alt | `lw-arch-all` | full prefix before SELECT (1143 chars) |
| chain | `recipe-8446-order` | `tok23` + sum(bits) + lw-tail40 + `yinyang` |

Each operand also tested with `:sha256hex` suffix form.

## Batteries run

| batch | candidates (×2 sha256hex) | decrypts | structured | keys |
|-------|---------------------------|----------|------------|------|
| 8 Bifid squares × {full, tail, after-d} | 48 | 288 | 0 | 0 |
| Beaufort on canonical bifid × 12 keys × {full, even, odd} | 72 | 432 | 0 | 0 |
| Recipe operands | 28 | 168 | 0 | 0 |
| Another door {1,4,21} + ARB + 1812/21 | 20 | 120 | 0 | 0 |
| Dots (#53335–42) + 8446 head | 14 | 84 | 0 | 0 |
| Filler single-letter deletion (60) | 60 | 120 | 0 | 0 |

**Total:** 960 decrypts, **0** structured, **0** uncomp hash160.

## Null sample

`dbbi_shuffle_null_10k`: simplified null — 10k random 23-char B/Y strings vs canonical **`BBBBYBBBYYBBBBYBBYYBFYY`** (not handoff 200k letter shuffle; see `ledger/experiments.md`).

## Result

**Null** on all P1 batches. Next: EVP-MD5 on recipe strings for SalPhaseIon-short only; Architect **word**-bounded lastwords (not char tail); diagonal/spiral matrix sums; 2-letter deletion on fillers.
