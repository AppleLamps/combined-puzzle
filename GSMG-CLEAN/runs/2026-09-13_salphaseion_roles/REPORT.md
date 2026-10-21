# SalPhaseIon field-role test

No authenticated envelope result. All 518 padding-valid outputs remain unresolved and retained.

## Exact reconstruction before password guessing

Tested whether DBBI is the directly serialized row/column sums of FAED, or vice versa, with a..i = 1..9, all nontrivial rectangular factor shapes, row-major layout, ordinary sums, decimal concatenation and the page's digit-letter substitution. All 32 cases fail exact reconstruction. In fact, none has the target field's length.

This closes only this simple direct-serialization model. Delimiters, signed/prime-transformed inputs, other encodings and other operators are not covered.

## Composite-password model

Earlier solved stages concatenate independently derived answers before SHA-256. The local source order places matrixsumlist material before lastwordsbeforearchichoice. Tested the corresponding **hypothesis**, not an established recipe:

`A + B`, `sha256hex(A) + B`, `A + sha256hex(B)`, or `sha256hex(A) + sha256hex(B)`.

A is one of 58 explicit representations: DBBI/FAED literal or decimal, colour-prime totals/lists, poster row/column sums, DBBI 7x13 sums, FAED 19x30/30x19 sums, and the existing L2 7x12 sums. Lists use joined, comma, space, or page-digit serialization where applicable. The matrix shapes and extra component hashing are hypotheses; they are not claimed to follow uniquely from the clues.

B is one of eight pinned Architect/choice endings in exact, lowercase, or connected lowercase-alphanumeric form (24 named variants). Only source-order A then B is used; joining is empty or one space. Literal A/B controls are included. Complete provenance is retained after deduplication.

The candidate file and manifest were saved before testing. There are 10,288 unique candidate strings. Only 37 overlap the earlier 15,676-string last-words candidate file; this does not establish novelty against every historical run.

## Results

- 123,456 trials: 10,288 candidates x 3 complete envelopes x 4 named profiles.
- Primary proven `gsmg` profile: 30,864 trials, 120 pad-1 outputs.
- Secondary `raw`: 130 pad-1; `gsmg-md5`: 143; `raw-md5`: 125.
- All 518 retained results have padding 1.
- No L5 pattern matches and no final-target key matches.
- Three whole-message format flags: all invalid zlib-header interpretations, not validated streams.
- Independently re-decrypted all 518 with the second AES implementation and matched the saved bytes.
- Additional embedded-fragment/compression inspection is in `fragment_reviews.jsonl` and `followup_summary.json`. No complete embedded compressed stream was found.

Files: `candidates.jsonl`, `manifest.json`, `structural_results.json`, `all_padding_valid.jsonl`, `inspections.jsonl`, `results.json`, and the follow-up files. `tools/test_salphaseion_roles.py` is the experiment script; it requires a new run directory to rerun unchanged. Known-envelope/key self-tests passed before trials, and matrix/poster/quoted-source assertions passed during construction.

No inference that every result is noise follows from padding or the format checks. What failed to emerge is independent support for these specific literal composite constructions. Further expansion of the same cross-product is not presently justified.

## Where the evidence points next

A subsequent structural review verified the previously unreproduced remove-g prime-prefix claim and resolved the existing 83/84-cell DBBI parse ambiguity. See `../2026-09-13_dbbi_prime_prefix/REPORT.md`. That full-input structure is a better basis for the next derivation than adding more literal composite variants here.
