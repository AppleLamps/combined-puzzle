# DBBI prime-derived control material applied to complete FAED

**Result:** 243 distinct numeric key lists produced 477 distinct full FAED transformations. None reconstructed a checked target or produced complete readable text under the declared numeric-byte decoding. No passwords or AES trials were generated. All unknown outputs remain retained.

## A necessary correction to the previous scope

The preceding raw-sum/Beaufort pass used a nine-symbol alphabet because FAED contains only a–i. That is one hypothesis, not a demonstrated alphabet size. Adjacent fields explicitly use **a–i plus o**, representing decimal digits 1–9 and 0. Restricting a transformed result to digits 1–9 prevents it from expressing any literal decimal byte-encoding that contains a zero.

The known label `thispassword` is decimal `36026487402470099740341006948`. Its zeros are indispensable in that encoding. A planted encode/Beaufort/decode control verifies that the ten-digit model preserves them. The old nine-symbol run was not a test of this ten-digit construction; neither model is proved by the alphabet inventory alone.

## Full models, with provenance

Inputs include raw DBBI and both complete 83/84-cell prime parses. For each parse, separate models:

- Restore prime position numbers, keeping non-prime digits.
- Zero prime cells, keeping non-prime digits.
- Retain the non-prime payload (60 or 61 values).
- Restore only blue/b prime positions, zeroing the other prime cells.
- Restore only yellow/be prime positions, zeroing the other prime cells.

Each input is arranged at every exact rectangular factor, including one-row/one-column controls. Row and column sums supply keys, represented either as numeric entries or as concatenated decimal digits. Those representations are different and are tracked separately. No negative-prime convention, shifted mask, reversed stream or arbitrary subset is introduced.

Each key operates on the **entire 570-character FAED field** by repeating-key Beaufort: plaintext residue = key minus ciphertext modulo the declared alphabet size. Modulo 10 is the page-digit hypothesis; modulo 9 with a=1 is the previous-model comparison. The resulting full decimal string becomes one big-endian integer byte sequence, as in the nearby known label encoding. Leading-zero counts are preserved because integer conversion itself discards them.

These are source-motivated experiments: matrixsumlist names sums, prime reinsertion is hinted, and Beaufort appears in an earlier stage. However, the puzzle has not specified that the sums are repeating Beaufort keys or that this is FAED's final decoding layer. These remain explicit assumptions.

## Results and verification

| Check | Result |
|---|---:|
| Distinct numeric key lists | 243 |
| Distinct full outputs, modulo 10 | 238 |
| Distinct full outputs, modulo 9 | 239 |
| Exact full Beaufort inverse checks | All passed |
| Exact matches against saved DBBI, FAED or Architect-letter target bytes | 0 |
| Entire byte output printable ASCII | 0 |
| Broad whole-text review flags across UTF-8, UTF-16/32 both byte orders, cp037/cp273 | 0 |
| Known decimal-zero positive control | Passed |

The broad review flag requires at least 95% non-control characters across a successfully decoded **whole** text. It is only a review aid, not an authentication test. Absence of a flag does not prove that bytes cannot be an encrypted, compressed or other nontext intermediate. No prefix or isolated word was used to qualify a result.

## What this establishes

The simple prime-derived sum-key/Beaufort/numeric-byte construction has yielded no complete text or exact target. This is a narrower conclusion than “DBBI cannot control FAED.” A different operator, different key construction, or an additional layer remains possible.

It also establishes a concrete limitation in the earlier search scope: ciphertext symbol count is not enough to choose the full cipher alphabet. Further work must preserve that distinction rather than declaring every model tested under modulo 9.

## Reproduce

Run `python tools/test_prime_control_faed.py` from GSMG-CLEAN. `manifest.json` records the model and input hashes. `outputs.json` contains every 570-character transformed stream, full numeric string, bytes, and all key derivations that converge on it. `format_reviews.json` is empty for this run; `summary.json` records the controls and counts. No source data was changed.
