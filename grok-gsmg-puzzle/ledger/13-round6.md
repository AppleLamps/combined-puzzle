# 13 — Round 6: Reader top 5

**Code:** `team/round6_battery.py` → `artifacts/round6_battery.json`  
**Source:** [Reader untested readings](bc-5fd657d0-8b88-5cc6-a514-aa6139dc8e89) priorities 1–5  
**Control:** §4.1 `causality` **PASS**

## P1 — Phase 3.2 after `SELECT`

Architect suffix phrases (constraint list after `SELECT`), including `fromovertwentythreeciphers…`, `bruteforcingmightberequired`, plus `recipe` / `matrixsumlist…` wraps.

## P2 — Checkerboard 149 digits as `matrixsumlist`

| `msl` form | value |
|------------|--------|
| sum | **504** |
| literal | 149-digit string from `phase32.bin` |
| pairs | two-digit chunk sums |
| mod256 | 3-digit chunks mod 256 → bytes |
| decode | 91-char checkerboard plaintext |
| decode-half | first 45 chars |

Recipes with `lw=halfandbetterhalf`; §4.1 + EVP-MD5 on Sal-short/Cosmic for recipes.

## P3 — #6509 “unforeseen hint” → `matrixsumlist`

Three hint families as `matrixsumlist` operand inside label recipe:

1. **Spiral / URL** — `gsmg.io/theseedisplanted`, first 192 spiral bits, full 196 bits  
2. **#8446** — decoded 161-char string + sha256hex  
3. **#1710 Roses poem** — full quote + `yellowhasanumberandsodoesblue`

## P4 — Yinyang phase

Decrypt **7** `load_containers()` yin-yang / XOR variants with **7** prior-stage passwords (checkerboard text, digit sum, tok23, after-SELECT slice, `yinyang`, sha256hex(checker)) — plain + sha256hex EVP password forms.

## P5 — `enter` as XOR

`enter(A,B) = A ⊕ B` on: tok23⊕lw, spiral⊕ab-bits, checker⊕tok23, checker⊕ab, terminal_ct⊕sal_ct → hex / latin-1 / recipe.

## Results

| metric | value |
|--------|------:|
| §4.1 decrypts (approx) | **408** |
| EVP-MD5 decrypts | **52** |
| Structured hits | **0** |
| Prize hash160 | **0** |

## Falsification (Reader)

| priority | status |
|:--------:|--------|
| 1 after SELECT | **Tested null** (this battery + R5 overlap) |
| 2 checkerboard 149 | **Tested null** |
| 3 #6509 hint ops | **Tested null** (all three families) |
| 4 yinyang phase | **Tested null** |
| 5 enter XOR | **Tested null** |

## Open

Inter-container **chain** (plaintextₙ → passwordₙ₊₁), Cosmic Duality **title**, SalPhaseIon **full page** key, #6913 **bit-width** windows — still on Reader extended list, not Round 6 scope.
