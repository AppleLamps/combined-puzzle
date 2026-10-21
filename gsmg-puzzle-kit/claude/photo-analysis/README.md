# The poster photo: is anything in it being missed? (4 Oct 2026)

**6 October 2026 interpretation notice.** This is a dated research record.
Its candidate counts and original logs are preserved, not freshly rerun.
Read [doc 118](../118-correctness-audit-remediation.md) for detector/coverage
limits and [doc 119](../119-current-evidence-ledger.md) for current findings.
A null applies only to its complete tested tuple.

Negative results are limited to the inspected files and channels. The later 384-candidate overlay review found no exact/probable match, not universal image-source absence.

**Reported result:** no additional payload was found in the inspected channels of `puzzle.png`. This is not a proof against every possible image encoding. Every pixel is accounted for by the solved grid, the rabbit drawing, the off-white cell, a plain font render, the logo and a standards-clean QR code. Every check below had a planted control that fired.

## Image used
`puzzle.png` from the repo: sha256 `38125bbd...2a1830`, 29,931 bytes, 1048x1556 RGBA. That is the hash the dossier (section 3.0) records as byte-identical to the Wayback capture of 12 Nov 2020, so this is the original, not a 2026 rebuild copy. No fresh web fetch was needed.

## Already covered before today (not repeated)
Dossier 4.1 to 4.6, 5, 10.4 and docs 15, 53, 55, 58, 105: the grid's five-colour palette and zero anti-aliasing, the spiral bits, the colour layer, the #FEFEFE cell, the rabbit and nest pixels in every reading order, the "Infrared" readings, file-level stego on the poster and all eight rebus tiles, the follow_the_white_rabbit.png comparison, the QR's decoded URL, and the title text via HASHTHETEXT.

## New checks today (`photo_checks.py`, output in `run.log`)

| # | check | result | planted control |
|---|---|---|---|
| 1 | PNG chunks, bytes after IEND, alpha | IHDR, sRGB, gAMA, pHYs, IDAT, IEND only; 0 trailing bytes; alpha is 255 everywhere (no data in transparent pixels) | n/a (structural) |
| 2 | hidden marks below the divider: every pixel that is not the flat #F5F5F5 panel, grouped | 38 components, all inside the logo, title, QR or address boxes; nothing outside | one #F4F4F4 pixel planted in the panel is found as a new component |
| 3 | grid palette | 5 colours, as recorded | n/a |
| 4 | logo LSB plane | horizontal stripes (a vertical gradient), 2,436 LSB transitions | a random LSB payload in one channel gives 11,601 |
| 5 | QR at codeword level (new; earlier work only decoded the URL) | version 4-L, mask 2, 0 impure pixels; ECI 26 (UTF-8), byte mode, 73 bytes = the blockchain.com address URL, terminator 0000, standard pad `EC 11 EC`, remainder bits 0, Reed-Solomon parity matches the data exactly. No extra bytes, no deliberate module errors hidden under the error correction | one flipped data module makes the RS parity fail |
| 6 | font render | the three title G's are pixel-identical; the two C's differ only by a neighbour's anti-alias pixel. A straight ClearType render, no glyph edits | n/a |

## Construction traces (explained, not data)
- The QR finder rings carry 345 pixels of #FAFAFA in a period-7 pattern, identical in all three finders: a scaling artifact of the generator (module = 7 px).
- White rows at y 1062 to 1064 and 1553 to 1555, and a 2-row white strip at x 877 to 1047, y 1065 to 1066: edges of pasted layers in a Paint-style composition (gAMA 45455 and pHYs 96 dpi are Windows defaults).
- The QR has no left quiet zone (starts at x = 1): cropped when pasted.

## What this means
The photo has no spare channel left. Its payload was the URL, the colour program (dbbi) and the off-white cell, all consumed. The operands of `matrixsumlist` and `lastwordsbeforearchichoice` are not in this image.
