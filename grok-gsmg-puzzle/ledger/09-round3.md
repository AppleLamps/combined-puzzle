# 09 — Round 3: EVP-MD5, word lastwords, spiral MSL, filler pairs

**Code:** `team/round3_battery.py` → `artifacts/round3_battery.json`  
**§4.1 control:** phase-2 `causality` **OK**

## 1. SalPhaseIon-short EVP-MD5 (community KDF)

| check | result |
|-------|--------|
| Planted `matrixsumlistenterlastwordsbeforearchichoicethispasswordmatrixsumlist` | **79 B**, 30 printable, sha256 `1449a217…` — matches handoff §8.1 [V] |
| Recipe variants (151 passwords) | **0** structured prose / magic |

**Operand substitutions tested:** each spiral/diag/row/col sum as `matrixsumlist` value; templates `{msl}enter{lw}thispassword{msl}`; label-wrapped `matrixsumlist{val}enter…`; `tok23`, #8446.

## 2. Word-bounded lastwords (before `SELECT`)

| candidate | string |
|-----------|--------|
| `lw-word-to` | `to` |
| `lw-word-requiredto` | `requiredto` |
| `lw-word-required` | `required` |
| … | suffixes `berequiredto`, `willberequiredto`, `primebasics`, full `afterwhichyouwillberequiredto` |
| `lw-film-to` / `lw-film-required` | script tokens |

Used alone and inside MD5 recipe templates above.

## 3. Spiral / diagonal `matrixsumlist` inputs

| key | value |
|-----|------:|
| `spiral-bits` | **101** (196 spiral cells) |
| `spiral-kb` | **101** |
| `spiral-by-weight` | **33** (23-cell B/Y spiral segment) |
| `diag-main` / `diag-anti` | **7** / **8** |
| `sum-rows` / `sum-cols` | **101** / **101** |
| `ab-sum-bits` | 56 (SalPhaseIon ab span) |

(See JSON for exact integers.)

## 4. Filler pair deletion

- **1,770** two-position deletions on 60 filler letters.
- Each → whole-block integer bytes → `{latin1, hex, sha256hex}` × **3** containers (§4.1 std-hex).
- **15,930** decrypts, **0** structured, **0** key hits.

## Result

**Null** on all new paths except the known **EVP-MD5 padding artifact** on the retracted community literal (not text).

**Open:** MD5 with **sha256(answer)** as password (some solvers double-hash); `matrixsumlist` as **operation** on spiral bit **string** not sum; triple deletion on fillers; word-split Architect via dictionary.
