# Comparing label interpretations through intermediate results

No passwords generated and no AES trials performed. Run `python tools/compare_label_models.py` from GSMG-CLEAN to reproduce the JSON evidence. Original puzzle files remain unchanged.

## Criteria

The source order is `DBBI | matrixsumlist | FAED | lastwordsbeforearchichoice | ...`. Labels are decoded facts; their scope is an interpretation. Success here requires exact reconstruction of a complete field, an exact source-text encoding, or a complete structural parse. Readable fragments and failed envelope attempts are not substitutes.

| Interpretation | Reproducible test | Result and scope |
|---|---|---|
| Trailing labels: each field independently encodes the answer named after it | Apply the nearby labels' demonstrated decimal-integer-to-bytes codec, with reverse encoding as a control | DBBI becomes 38 bytes; FAED becomes 237 bytes. Neither is ASCII or valid UTF-8; cp037/cp273 produce control-filled text, not a readable instruction. The simple direct-text version fails; a further cipher is not excluded. |
| FAED is a directly encoded Architect quotation | Exact, lowercase and lowercase-alphanumeric contiguous windows from the pinned movie transcript and modified puzzle speech; compare complete encoded fields | 1,589 length-compatible comparisons across both fields, zero exact matches. This excludes the tested direct encodings, not another transcript or a transformed quotation. |
| The letters stand for concatenated decimal character codes rather than one large number | Complete dynamic-programming segmentation into printable ASCII codes 32–126 | Zero complete parses for either field. The printable-ASCII version fails without needing a quotation guess. |
| `matrixsumlist` is an operation connecting the fields | Every exact rectangular factor, both axes, and concatenated row/column lists in both orders | Across 304 checks, no output even has the target length. Neither direct FAED→DBBI sums nor the tested DBBI→FAED sums reconstruct the other field. |
| Labels name separate components with an additional unresolved operation | Reproduce complete DBBI prime grammar and require independent FAED evidence | DBBI still has the 84-cell 23/16/7 parse and the 83-cell alternative. No independently decoded FAED component has been obtained. This model remains open, not validated. |

## Matrix scope

Raw letters use a=1 through i=9. For DBBI's two complete prime parses, separate hypotheses use the token's decimal value (b=2, be=25), its prime position, zero, or removal. Every rectangle, including degenerate one-row/one-column cases, is tested without rearrangement. Output is the decimal concatenation of ordinary sums, using the page's digit letters. These replacements are explicit hypotheses, not creator-confirmed instructions. Signed values, modular sums, transpositions before arranging the grid, arbitrary digit partitions and hashes are outside this test.

The 304 checks broaden the earlier 32 direct-sum cases; they are not all historically new. `matrix_checks.json` retains each computed list. `quote_checks.json` retains all length-compatible quotation comparisons, including texts and source positions. `results.json` retains full decoded bytes, not only text scores.

## What survives

The exact positive intermediate remains DBBI's complete prime-position structure. Merely turning b/be into signed numbers and choosing a rectangle would add unsupported steps. The numerical 23/16/7 correspondence favors the 84-cell parse, but the alternate ending and the poster's colour mismatch remain unresolved.

The trailing-label interpretation has not been disproved: only its simplest direct-text realization has failed. Likewise ordinary matrix sums failing to map one field to the other does not disprove a matrix sum list derived from some third source, or a sum list serving as a cipher key.

The next justified problem is identifying that additional operation through an explicit source clue and testing whether it predicts FAED or a complete plaintext. Until such a relation exists, none of these label interpretations qualifies as a verified password recipe.
