# DBBI: a source-accounting error and two necessary corrections

**A real error was found in an earlier follow-up's derivation: the final `e` is not left over from the construction that produces `HILLFEXMGSGQ`.** It has already contributed to its final `Q`. This does not solve an envelope, but it invalidates the stated justification for appending that character to make `FEXMGSGQE` a nine-character Hill key.

## 1. The final e is already used

Under the existing 84-cell prime parse, signed-prime values and 7x12 column-sum model, every one of DBBI's 91 source characters is consumed exactly once. The final `e`, source `[90,91)`, is logical cell 84: row 7, column 12, value 5.

The seven values in column 12 are:

```text
7 + 7 + 5 + 6 + 6 + 6 + 5 = 42
42 mod 26 = 16 = Q    (A=0)
```

Consequently:

| Construction | Complete sum text | Leftover source e |
|---|---|---|
| All 84 logical cells | HILLFEXMGSGQ | None |
| Reserve the final e; sum the other 83 cells in the same columns | HILLFEXMGSGL | One |
| Use the alternative complete 83-cell parse, with final be as prime cell 83 | HILLFEXMGSQL | None |

`../read/SOLVE/hill_faed_exact.cjs` says the sum list “leaves a final e=5” and constructs `FEXMGSGQE`. That premise is false. `hill_bifid_count_matrix.cjs` similarly describes a “retained final e=5” in constructing `[23,16,7,5]`. The value exists, but it is reused, not left unconsumed. Their file hashes and relevant opening comments are retained in `summary.json`.

Reusing source material is not inherently forbidden in a puzzle. The correction is narrower: reuse requires a separate rationale; it cannot be justified by claiming a leftover. Nor do the old negative results become positive evidence for their underlying derivation.

### Test the corrected hypothesis

If the final e is deliberately reserved from the sum list, the corresponding nine-character key is **`FEXMGSGL` + `E` = `FEXMGSGLE`**, not `FEXMGSGQE`.

`test_hill_reserved_e.py` tests this correction using rendered A=0/A=1 key values and the corresponding raw sums. It covers invertible 3x3 Hill matrices modulo 9 and 10, transpose, encryption/decryption, a=0/a=1 input values, and adjacent/three-rail grouping of all 570 FAED symbols. Singular matrices are recorded, not silently treated as reversible ciphers.

There are **32 complete reversible models and 96 whole-integer byte readings**, including decimal and base-9 alternatives. No output is complete printable ASCII or strict UTF-8; the highest ASCII fraction is 0.4473. All bytes are preserved. Planted full-message recovery and every applicable round trip passed. No complete instruction or authenticated result was recovered. Reserving the cell remains an additional hypothesis; correcting its bookkeeping does not establish the operation.

## 2. BTCSEED does not require choosing a 13-character key prefix

The standard first-occurrence deduplication of the **entire DBBI** field, completed with the same no-J alphabet, gives:

```text
dbifhcegaklmnopqrstuvwxyz
```

This is exactly the square obtained from DBBI's first 13 characters. The first a occurs at source offset 16; a is also the first unused letter supplied by the alphabet completion. Thus both procedures give the same entire square, and their full 570-character Bifid outputs are identical.

The prefix remains `btcseeddeoemckeadhbschdkbdcsdkdvbxcpcoch...`. This corrects any inference that selecting a 13-character key prefix was necessary to obtain BTCSEED. It does not establish Bifid as the intended cipher, a seven-character header, or the remainder as decoded prose.

The audit also tests the complete-field Bifid/Hill compositions in both orders under the twelve alphabet/base/example-direction conventions from the earlier carrier audit. **20 complete 570-character outputs** round-trip exactly. Four more compositions are undefined because a natural-26 Hill result contains J, which is absent from the specified Bifid square; those complete intermediates are retained. J is not silently deleted or merged. No complete output matches a contiguous normalized Architect passage, and no complete instruction was recovered. Synthetic complete-message controls passed where the composition is defined.

## 3. The poster discrepancy directly affects the word HILL

In the signed model, substituting the poster's yellow at marker 21 for DBBI's blue changes prime 73 from -73 to +73. Only the first column changes:

```text
-45 + 146 = 101
101 mod 26 = 23 = X
```

The result becomes **XILLFEXMGSGQ**. Therefore “correcting” DBBI to the poster would erase the opening cipher name under this model. It is not a harmless normalization. Preserve both sources and this exact dependency.

There are only 23 primes at or below 84; the 24th prime is 89. Comparing this finite 84-cell object to the first 23 poster colours naturally leaves the 24th colour outside its range. That non-use alone does not require an extra deletion operation or falsify the prefix comparison. The mismatch at marker 21 remains a separate substantive issue.

## Limits and consequence

The signed-prime convention, 7x12 shape, modulo 26 and interpretation of FEXM/GSGQ as a Hill example remain hypotheses. These checks establish exact consequences of those hypotheses, not the creator's intended construction.

The corrected research position is to retain the complete DBBI-keyed Bifid lead, remove the false leftover-e justification, and keep the poster disagreement explicit. There is still no verified operation that explains the complete FAED field or opens a locked envelope. The tail-frequency lead supplies no reason to bypass these source-accounting constraints.

Reproduce:

```text
python tools/audit_dbbi_accounting.py
python tools/test_hill_reserved_e.py
```

`ownership.json` maps every source character to its logical cell and sum. Full compositions, alphabet-incompatible intermediates, corrected-key outputs, manifests and controls are saved alongside this report. No password candidates or AES trials were generated.
