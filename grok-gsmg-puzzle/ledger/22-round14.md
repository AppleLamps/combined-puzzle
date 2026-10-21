# 22 — Round 14: missed connections & clue battery

**Spec:** `team/preregister_round14_clues.json`  
**Code:** `team/round14_clues.py` → `artifacts/round14_clues.json`  
**Budget:** 2 000 (used **1 688**)  
**Control:** §4.1 `causality` **PASS**

## Clue tracks (from structural review)

| Gap | Connection tested | Result |
|-----|-------------------|--------|
| **G1** | Split-header XOR (`xor_from_offset_16`, ct-tail, interleave bytes) + hint anchors | null |
| **G2** | **First hint / last command** pairs (#225 hash + `theseedisplanted`, flower + `yourlastcommand`, sha256our/anstoo) | null |
| **G3** | **Another door** `{1,4,21}` on digits149, checker decode, architect 1539, host bits; architect **23/16/7/140/161** in recipes | null |
| **G4** | Bifid **even/odd** streams, post-`btcseed`, faed last-32; even **b,c,d,e** nibble pack | null |
| **G5** | Beaufort key `THEMATRIXHASYOU`, `btcseed*`, phase 3.2 password; architect/beaufort **sha256hex** | null |
| **G6** | **Inline** Sal b64 spans (= sal short) decrypted with page / pre-ct / post-ct / shabef sha | null |
| **G7** | Round-4 **spiral MSL ops** in `matrixsumlist…enter…` recipes | null |
| **G8** | **Yinyang** XOR blobs keyed by checker / digits149 / #8446 | null |

## Confirmed [V]

Inline ciphertext in the 1075 stream (spans around `enter`) is **byte-identical** to `salphaseion_short.bin` (96 B).

## Result

**0** structured, **0** prize hash160. Clue-aligned readings above are **tested null** under the preregistered forms only; a null on one password form does not exclude the reading. Detector caveat and re-run: `ledger/23-detector-audit.md`.

## Still outside this battery

- Non–§4.1 ciphers on locked blobs  
- `#76033–#76034` retracted MD5 plaintext structure  
- Pixel / rebus / audio **HASHTHETEXT** side quest literals beyond flower hash  
- Full **200k** dbbi shuffle reproduction  
