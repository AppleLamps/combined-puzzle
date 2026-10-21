# Test of the 60-character remainder as matrixsumlist material

**Result: no complete sum-list relationship or instruction was recovered.** The 83-cell marker alignment remains exact, but these tests do not validate its 60 ordinary characters as the intended matrixsumlist input or output. All numerical outputs and decoded bytes are retained. No passwords were generated and no AES trials were run.

## Source and direct decoding

The script independently extracts the poster, builds the 25-marker schedule including off-white, and consumes all 91 DBBI source characters under that schedule. The resulting 83 logical cells contain 23 prime markers and this unchanged 60-character remainder:

```text
difhccgihaeeihggegebgehhehhfafdhffcdbfcccgfeggecdcifffgigeea
496833798155987757527588588616486634263337657753439666797551
```

The second line applies the page's demonstrated a=1 through i=9 mapping. Treating the full decimal string as one big-endian integer gives **25 bytes**:

```text
4f2672e27e0d78d5a3f30ee8f82e316eeff67ee50ef4257bef
```

The byte-to-decimal round trip is exact. Those bytes are neither ASCII nor valid UTF-8; their length is incompatible with complete UTF-16 or UTF-32. Both previously used EBCDIC interpretations contain control characters and do not recover an instruction. All successful strict decodings are in `summary.json`, and the original bytes are in `direct_integer.bin`.

The alternative reading as concatenated decimal printable-ASCII codes has **zero complete segmentations**, computed by dynamic programming without choosing character boundaries in advance. The neighboring labels' known whole-integer encodings and a planted ASCII-code sequence pass as controls.

The bytes have 22 distinct values, so the fact that 25 bytes form a 5x5 square does not make them a direct 25-symbol alphabet permutation. Arbitrary numerical matrix use remains a separate hypothesis and was tested below.

## Exact poster-to-remainder comparisons

This broadens the earlier 40 direct decimal comparisons rather than presenting them as new discoveries.

The original 14x14 geometry is retained. Twenty boards place either ordinal primes or ordinal marker numbers on the first 23 or all 25 selected cells, using unsigned values, either global sign assignment, or one colour only; unselected cells are zero. The established binary poster supplies one additional board.

For each board, the script takes rows, columns, both concatenation orders and their reversals. It compares complete decimal strings, minimum-width decimal fields, space/comma/semicolon/newline lists, compact JSON, and applicable 8-/16-bit signed/unsigned byte formats. Integer byte formats include both endiannesses where applicable. Complete representations are compared with the remainder's decimal string, literal letters and decoded integer bytes.

**2,098 serialization/model comparisons across 21 boards: zero exact matches.** Counts include equivalent representations and overlaps with earlier tests; they are not independent statistical trials. Every list and serialization is saved in `poster_boards.json` and `poster_serializations.json`.

A representation-independent length limit excludes one narrow version outright: the unpadded decimal concatenation of all binary row and column sums can contain at most **56 digits for a 14x14 board**, or **58 for a 14x15 board**. The remainder has 60. This bound does not apply to weighted matrices, extra totals, padding, separators, or further encodings.

## Treat the remainder itself as matrix data

All exact rectangular shapes of the 60 a=1..i=9 values were tested, with rows, columns, both concatenation orders and reversals. The digit total is 336; every row/column calculation preserves that total. Each complete list was read as decimal integer bytes, direct ASCII where possible, and A=0/A=1 letters modulo 26.

**96 complete sum-list readings:** no exact reconstruction of DBBI, FAED or the declared label/instruction targets. No complete instruction was recovered. Direct ASCII sums sometimes produce short fragments such as `SIX\`; the complete output and its remaining character are retained, not promoted to a solved word. None of the whole-integer byte readings is fully printable ASCII.

The 25 non-text bytes were also treated as numerical matrix data, rather than rejected solely for lacking readable text. All exact rectangles (1x25, 5x5, 25x1), unsigned/signed-byte values and the same reading orders produce **48 further complete sum-list readings**, with no exact target reconstruction or recovered instruction.

For the straightforward unsigned 5x5 case:

```text
Row sums:    583, 752, 589, 950, 657
Column sums: 230, 873, 858, 684, 886
Modulo 26, A=0: LYROH WPAIC
```

Complete digit and byte-matrix results are saved separately in `payload_sum_readings.json` and `decoded_byte_sum_readings.json`. Modulo-26 readings are explicit hypotheses, not newly established instructions.

## Meaning of the result

The tested straightforward sums and formatting choices do not supply the missing connection. The exact marker alignment does not automatically prove that deleting prime tokens leaves plaintext, a sum list, or the correct next key. Conversely, failure of these particular models does not disprove the 83-cell alignment or make its payload unimportant.

What remains unverified is the role of those 60 ordinary values and whether prime cells should be removed, restored, or combined with them. This pass provides no reason to start another password cross-product from the resulting fragments.

Reproduce with `python tools/test_payload60_matrixsum.py`. Known page-codec controls, exact input reconstruction, sum conservation, JSON and signed-integer round trips passed. The manifest records the scope and source hashes; original puzzle files were not modified.
