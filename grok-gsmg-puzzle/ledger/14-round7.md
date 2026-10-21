# 14 — Round 7: chained pipeline (all brainstorm + Reader inter-container)

**Spec:** `team/preregister_chained_pipeline.json`  
**Code:** `team/round7_chained_pipeline.py` → `artifacts/round7_chained_pipeline.json`  
**Control:** §4.1 `causality` **PASS**

## Families executed

| Family | What it tests |
|--------|----------------|
| **h1_8446** | Strategist H1: `tok23` + msl → Sal (§4.1 ± EVP-MD5) → `sha256hex(pt‖lw)` → Terminal → `+yinyang` → Cosmic |
| **m3_baselines** | Cryptanalyst M3 single-step `{msl}enter{lw}thispassword{msl}` on each container |
| **m3_orders** | M3-style 3-step chains with **11 derivations** from each PKCS-valid plaintext, **6 container permutations**, Sal MD5 + Cosmic `raw32` profile on last step |
| **reader_TSC** | Reader narrative **Terminal → Sal-short → Cosmic** (pad-gated chain + hash-chain on same order; **not** full derivation grid — see `15-team-audit.md`) |
| **yinyang_mid** | Sal decrypt → yin-yang / XOR **7 variants** → Cosmic (± raw32) |
| **checker_lw** | Brainstorm step 4: 149-digit `msl` + checker **HALF** lw, Sal→Cosmic→Term and Sal→Term→Cosmic |
| **xor_enter_chain** | Sal → XOR(`enter`) with tok23/lw/checker/ab → Terminal → XOR → Cosmic |
| **hash_chain_no_pt** | Password hash-chain **without** plaintext: `sha256hex(s0‖msl)` → `‖lw` → `‖yinyang` on all **6 orders** (+ cross-container stress) |
| **liberal_enter** | M3 order using **raw CBC blocks** (no PKCS requirement) for `enter` derivations |
| **cosmic_kdf_probe** | Strategist step 4 convention probe on Cosmic from chained `p2` (§4.1 raw32, EVP-MD5 variants) |

## Operand catalogs (frozen in JSON)

- **msl:** spiral list (dash/concat), spiral ab-hex, Sal ab 14-row-sums, poster row/col/diag, checker 149 sum/decode, `tok23+rows`, etc.
- **lw:** SELECT-context choice join, arch tail-40, checker half-45, #8446 head-8, flower hash, word-lastwords set
- **Derivations:** latin-1, sha256hex, prefix-64, body hex, pt‖lw, pt‖yinyang, XOR(checker/tok23/lw)

## Results

| metric | value |
|--------|------:|
| Total decrypt attempts | **34,434** |
| Budget cap | 120,000 |
| Structured plaintext | **0** |
| Prize hash160 | **0** |

## Falsification

| hypothesis | status |
|------------|--------|
| H1 ordered multi-container (Sal → Term → Cosmic) | **Tested null** |
| M3 `enter` as pipeline verb (pad-valid pt feeds next) | **Tested null** |
| 6 container order permutations | **Tested null** |
| Hash-chain passwords without plaintext | **Tested null** |
| Liberal raw-block `enter` chain | **Tested null** |
| Yinyang mid-chain after Sal | **Tested null** |
| Reader T→S→C narrative chain | **Tested null** |
| XOR `enter` multi-hop | **Tested null** |
| Cosmic KDF convention probe on chained `p2` | **Tested null** |

## Note

Most **pad-valid** intermediate plaintexts are rare (~chance); **hash_chain_no_pt** and **liberal_enter** explicitly cover paths that do not require a lucky Sal open. Still null.

## Open (non-pipeline)

Strategist **H2** (faed→Beaufort factory), **H3** (door-index deletion), Sal **full page** 1075-char key, Cosmic Duality **title**, #6913 **bit-width** windows — not in this battery.
