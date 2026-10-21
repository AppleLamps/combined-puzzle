# FAED model constraints: derive the required key instead of guessing it

**Decision:** stop expanding short repeating numeric keys for the specific model “FAED is a decimal-encoded Architect quotation encrypted with Beaufort/Vigenère.” An exact necessary-condition test excludes every short key for the source passages and formatting cases below, not just the keys previously generated.

## Source scope

694 unique complete-word passages were collected from individual Architect utterances in the pinned movie transcript and the modified puzzle speech, using exact, lowercase and lowercase-alphanumeric forms, at 236 or 237 UTF-8 bytes. Navigation, Markdown headings and mixed-speaker windows are excluded. These lengths bracket the byte size of the direct 570-digit conversion; they are declared hypotheses, not a universal plaintext-length requirement after arbitrary encryption.

This improves the earlier broad quotation-window scan: that scan included some transcript-page navigation text. It produced no successful match, so no claimed solution is invalidated, but its “quotation” label was too broad.

## 1. Decimal lengths expose an extra formatting assumption

The passages naturally produce:

| Decimal digits | Unique passages |
|---|---:|
| 568 | 262 |
| 569 | 77 |
| 571 | 355 |
| 570 | 0 |

A positive 570-digit integer represented as 237 big-endian bytes has first byte at most **45**. Thus a 237-byte ASCII quotation beginning with an ordinary letter cannot have a natural 570-digit decimal encoding. This arithmetic fact does not exclude shorter byte strings whose decimal representation was padded before encryption, or different encodings.

The test explicitly allows two alternatives rather than silently rejecting them:

- Left-pad the 568/569-digit plaintext numbers to 570 digits.
- For 571-digit plaintext, restore a hypothesized omitted leading zero to FAED's ciphertext digits.

Neither formatting step is established by the puzzle. They are recorded alternatives, not corrections to source bytes.

## 2. Necessary key sequences exclude all short repeating keys in this model

For each full passage and compatible length case:

- Beaufort requires `K[i] = (C[i] + P[i]) mod 10`.
- Vigenère requires `K[i] = (C[i] - P[i]) mod 10`.

These directly determine the full required key stream. There is no guessed key. A prefix-function calculation finds its shortest repeating period, including periods that do not divide the message length exactly.

**1,388 required streams were checked. The shortest period is 567.** The longest derived key in the previous prime/sum pass was 103 entries. Therefore **no repeating key of length 103 or less**, whether previously generated or not, can map any of these specific passages to FAED under these arithmetic/formatting models. The result also excludes all periods below 567 within the same scope.

Controls include a non-dividing period and a planted full decimal-encoding/Beaufort example whose three-digit key is recovered exactly. Every reported shortest period is also checked by reconstructing the full required stream from its prefix.

## 3. Symbol counts constrain plain transposition/substitution too

All 694 natural decimal passage encodings contain all ten digit values, including at least 38 zeros. FAED uses nine symbol values and no zero symbol. A pure transposition, or transposition combined with a bijective digit-to-symbol substitution, cannot change ten distinct symbols into nine. This rejects those direct quotation models for the same passage set. It does not reject fractionation, non-bijective encodings, removed/implicit symbols, or a different plaintext source.

The missing zero is consequently not sufficient evidence to select a nine-symbol cipher alphabet, nor does adding the tenth symbol validate the decimal-quotation model. Both the representation and its use need evidence.

## What this changes

The earlier test's negative result could have meant that we merely chose the wrong sum keys. This test shows that, for the declared full passages, choosing another short numeric key cannot fix it. We should not spend more runs extending that key family.

The unresolved alternatives now differ in substance: FAED may use another numerical representation, a non-repeating operation, another plaintext entirely, or may itself be instruction/key material rather than an encoded quotation. DBBI may still control FAED, but the specific short-key/decimal-quotation construction has been constrained much more strongly.

No envelope was opened, no result was discarded as unimportant, and no password/AES search was performed.

## Reproduce

`python tools/audit_faed_constraints.py` writes `manifest.json`, `required_keystreams.json` (complete passages, provenance and required streams), and `summary.json`. Source files remain unchanged.
