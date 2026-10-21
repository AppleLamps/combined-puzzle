# Off-white cell: an exact alternative to repairing marker 21

**A consistent serial-marker rule matches all 23 prime markers in the complete 83-cell DBBI parse.** Count the off-white cell as an additional marker in the established spiral, with the same token value as a blue marker. No poster pixel or DBBI character is changed. This selects the final `be` as one prime token, rather than splitting it into prime `b` and ordinary `e`.

This is a reproducible relationship, not a decrypted instruction or proof of the author's intent. A competing per-byte rule also fits the 84-cell parse. The distinction is now explicit and testable.

## 1. Pixel evidence

The original PNG was inspected visually and sampled afresh. Each of the 196 grid cells was classified by its most frequent RGB value. Every selected marker agrees with an independent center-pixel sample. The established spiral still decodes the full URL `gsmg.io/theseedisplanted`, followed by four zero bits.

The census is 86 black, 85 pure white, 15 blue, nine yellow, and **one off-white** cell. That off-white cell occupies the complete box `[300,525,375,600)`: all **5,625 pixels** equal `(254,254,254)`, or `FEFEFE`. It is not an antialiased edge, a center-pixel sampling accident, or part of the rabbit outline.

| Feature | Zero-based row/column | Spiral bit index | Ordinal among all 25 non-black/non-white cells |
|---|---|---:|---:|
| Off-white | 7, 4 | 163 | 21 |
| Disputed yellow cell | 9, 6 | 167 | 22 |
| Remaining blue | 8, 5 | 183 | 24 |
| Remaining yellow | 5, 6 | 191 | 25 |

The first two features belong to the same 21st URL byte, but they are different cells. Treating each marked **cell** as an item does not require changing either bit in that byte.

## 2. One rule for the full marker stream

Use the established top-left, down-first inward spiral. Keep cells whose modal RGB is neither pure black nor pure white. Encode yellow as `be`, and the other marked cells as `b`.

An equivalent numerical classification on these selected cells is: **blue-channel value zero -> be; positive blue-channel value -> b**. Yellow has blue channel 0, blue has 204, and off-white has 254. This makes the classification uniform across all 25 selected cells; it does not independently prove that this channel rule was intended.

The full stream, retaining F as the off-white identity, is:

```text
BBBBYBBBYYBBBBYBBYYBFYYBY
```

With F assigned token b, the comparison is:

```text
Poster first 23: BBBBYBBBYYBBBBYBBYYBBYY
DBBI 83 cells:  BBBBYBBBYYBBBBYBBYYBBYY
                        23 / 23 agree
```

The script does not choose 83 as a desired length and then trim the input. A deterministic parser takes the poster schedule as its input. At every prime-numbered logical cell it consumes the specified `b` or `be`; at every other cell it consumes one source character. It reaches the end of all **91 original DBBI characters at logical cell 83**. The final source `[89,91)` is `be`, the marker at prime 83.

The resulting bookkeeping is:

- 23 prime cells: 15 `b` and eight `be`.
- 60 ordinary cells, all retained.
- 91 source characters consumed exactly once, with nothing appended or deleted.
- The complete source is reproduced exactly from the marker schedule and retained ordinary characters.

That round trip retains the ordinary characters from DBBI; it does **not** derive those 60 characters from the poster. Their meaning remains unknown. They are saved in `payload_60.txt`:

```text
difhccgihaeeihggegebgehhehhfafdhffcdbfcccgfeggecdcifffgigeea
```

## 3. Compare the alternatives fairly

| Whole-poster rule | 83-cell marker agreement | 84-cell marker agreement |
|---|---:|---:|
| Ignore off-white; use blue/yellow cells | 21/23 | 22/23 |
| Include off-white as an additional b marker | **23/23** | 22/23 |
| Include off-white as an additional be marker | 22/23 | 21/23 |
| Keep one marker per byte; XOR its bit with a flag for an off-white cell in that byte | 22/23 | **23/23** |

The serial rule changes indexing after the off-white cell. The per-byte rule changes the marker value within the same byte. Both account for the observed discrepancy under different grouping assumptions, so a matching colour stream alone cannot establish which is correct.

The serial rule no longer requires choosing the 84-cell endpoint to obtain the old 23/16/7 counts or HILL sum. Those counts appear in the original film dialogue as well as the puzzle rewrite; they do not by themselves override the exact alternative correspondence. Conversely, the new 83-cell fit does not prove that HILL is accidental.

The F -> b choice was investigated after observing the mismatch; no discovery p-value is claimed. As a check on uniqueness, the script tests insertion of B or Y at every gap in the regular 24-marker sequence. Two adjacent positions can give the same 83-cell fit because a neighboring marker is already B. The actual pixel location is known independently, but the marker text alone cannot distinguish those two positions.

## 4. The two remaining poster markers are retained

The full poster schedule has 25 items. The 83-cell DBBI field uses only the first 23, because its last logical prime is 83. The remaining items are B and Y at spiral indices 183 and 191. Their next ordinal primes would be 89 and 97 if the schedule continued.

There is no evidence here that those two cells should be deleted. A direct continuation into the following encoded `matrixsumlist` label matches the marker at prime 89, then fails at prime 97: source offset 104 contains `aa`, whereas the schedule requires `be`. Therefore that label cannot simply be absorbed as more of this prime-marked stream. The full failed continuation is retained in `continuation_check.json`.

## 5. Test a direct next relation without passwords

The 60 remaining digit-letters were compared against an explicit source-shaped `matrixsumlist` model: place the ordinal primes on the marked poster cells, zero the unmarked cells, and read complete row/column sums from the original 14x14 geometry. Separate cases use the first 23 or all 25 markers; unsigned values, either global sign assignment, or one colour only; rows, columns, or their two concatenation orders.

**40 complete sum-list comparisons produced no exact match to the complete 60-digit payload.** This excludes that direct decimal concatenation model only. It does not exclude other representations, matrix operations or use as a key. Every computed list is retained in `poster_sum_bridge.json`; no password candidates or AES trials were generated.

## Consequence

The unresolved question is no longer simply “which bit must be flipped?” A complete alternative explains the discrepancy by **including a source cell previously omitted from the marker sequence**, and resolves the DBBI endpoint differently. Keep both the serial 83-cell and per-byte 84-cell models until an independent downstream reconstruction distinguishes them. Do not silently pad 83 cells into a 7x12 matrix or call its final e a leftover.

Reproduce with `python tools/test_offwhite_marker_alignment.py`. `grid.json`, `marked_cells.json`, `guided_parses.json`, `summary.json`, the payload, the continuation and every tested sum list preserve the evidence. Original poster and ciphertext data remain unchanged.
