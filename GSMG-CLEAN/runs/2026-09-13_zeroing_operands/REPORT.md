# Investigating the operand of “zeroed out”

**Result:** no tested mask is authenticated. The tests separate operations that had previously been easy to conflate. No passwords were generated, no AES trials were run, and all intermediate bytes are retained.

## Bounded tests

- **96 field constructions:** DBBI and FAED single-symbol classes; raw prime positions; blue/yellow positions under the explicit first-24-primes/poster-colour pairing; and the prime, b-only and be-only cells of both complete logical DBBI parses. Each has numeric-zero, deletion and retention variants. Logical tokens additionally distinguish replacing a whole `be` cell by one `0` from replacing its two source digits by `00`. There are no shifted or repeated masks, arbitrary subsets, signs or moduli.
- **18 poster bit constructions:** each original pixel class and all coloured cells together, using zero, delete and retain. The source image's 196-cell spiral is re-extracted and checked against the saved bits. Leftover bits are preserved explicitly; they are not silently padded to create a text result.
- **Nine poster character constructions:** blue, yellow and off-white classes identify their containing decoded URL bytes; those bytes are replaced by NUL, replaced by ASCII `0`, or deleted. These are different operations from zeroing the selected bit.

These are hypotheses motivated by actual source features. The creator has not confirmed any of the chosen masks. Some overlap prior prime/matrix experiments, but this audit tests direct zeroing/decoding rather than repeating matrix sum or password sweeps.

## Findings

1. **No field reconstruction or complete instruction.** None of the 96 constructions reconstructs the other field or produces the checked complete Architect substring. No zeroing/deletion construction yields wholly printable ASCII through the demonstrated decimal-integer-to-bytes method or a complete printable-ASCII decimal segmentation. The ten format-positive constructions are all single-symbol *retention* controls: one `o` or repeated punctuation/letters. For example, retaining `f` creates repeated decimal 6 digits, which naturally parse as 66 -> B. These are deterministic encoding artifacts, not hidden instructions.

2. **Zeroing white, off-white or yellow bits is a no-op under the verified poster decoder.** Those classes already encode zero. Returning the known URL after this operation cannot validate the hint's intended operand.

3. **Zeroing blue bits remains printable for a structural reason.** All 24 coloured cells lie at the least-significant bit of successive URL bytes. Blue bits are 1, yellow bits are 0. Clearing blue or all coloured bits therefore produces the same string: `frlf.hn.thdrdddhrpl\`ntdd`. It clears character parity; it does not reveal a demonstrated second URL or instruction. Its printability is inherited from the original URL.

4. **The off-white discrepancy stays unresolved.** The off-white square is bit index 163, in URL byte 20 (`n`), while colour marker 21 is bit 167. Zeroing bit 163 changes nothing. Zeroing/deleting byte 20 affects the entire `n`; any readable surviving URL text is expected and cannot independently authenticate the deletion. No repair of the b/be correspondence was justified here.

## Interpretation

The simple claim “zero one letter class or the prime markers, then apply the nearby decimal/text encoding” has no successful realization in this finite family. The poster bit model has stronger negative evidence for white/yellow/off-white: zeroing them literally does nothing under the already verified convention.

This does not rule out zeroing after an additional cipher, using a different source-grounded representation, or using a zeroed matrix as a key rather than as direct text. The original hint says “along the way” and does not locate the step. We should therefore stop treating zeroing as necessarily the immediate missing operation between DBBI and FAED. That placement remains an assumption.

## Reproduce and inspect

Run `python tools/test_zeroing_operands.py` in GSMG-CLEAN. The script checks the original poster URL, exact spiral bytes, the off-white byte position and a synthetic deletion/decimal-ASCII control. `manifest.json` records scope and source hashes. `field_outputs.json`, `poster_outputs.json` and `poster_character_outputs.json` preserve every result; `summary.json` includes every format-positive field result. Unknown bytes are retained, not classified as irrelevant.
