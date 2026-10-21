# 140 (2026-09-08, revised)

The Architect Beaufort of phase 3.2.1 says a wise man above hinted at something **worth hundred forty of the investment**. That is a named 140, and it had never been in any password list. Two calculated 140s then showed up. They are not the same fact, and they are not equally good.

## The screenshot 140 is dead, for a better reason than “it’s a rendering”

`SalPhaselonCosmicDuality.png` is a screenshot of `gsmg.io/89727c598b9c…` — the Salphaseion letter grid over the Cosmic Duality blob. The 11 R↔B mirror-pair colours are **ClearType fringes of black glyphs**, not a palette:

| Colour | Count | Adjacent black | Side |
|---|---|---|---|
| `(0,0,135)` (blue-ish) | 1196 | 610 left, **0 right** | sits on the **right** of a black stem |
| `(135,0,0)` (red-ish) | 1056 | **0 left**, 444 right | sits on the **left** of a black stem |

That is exactly LCD subpixel antialiasing: left of a stem goes red, right of a stem goes blue, and the two are R↔B mirrors *by construction*. They occupy 281 and 221 different rows from y=60 to y=607 — throughout the letter box, not a barcode. Snap the screenshot to its discrete 7-level palette and the 140 **moves**: the dark pair becomes a 145-diff, and a pale pair `(255,255,231)` / `(231,255,255)` becomes 140. A number that jumps pair under the most natural cleanup is not authored.

So the Cosmic Duality file coinciding with 140 was the kind of coincidence it looked like. Discarded, with a stronger autopsy.

## The grid 140 is real, and I had the census wrong

Center-pixel classification of `follow_the_white_rabbit.png` (and of `puzzle.png`) gave K87 W84. **Majority vote** — the right call on the 7 rabbit cells, which are impure white — gives:

| | K | W | G | B | Y |
|---|---|---|---|---|---|
| majority | **86** | **85** | **1** | **15** | **9** |
| grey counted as white (it already encodes 0 in the URL) | **86** | **86** | — | 15 | 9 |

86+86+15+9 = 196 = 14². The group had this exact census in January 2026 (`2026.txt` #54988) and wrote `86+15b+9y = 140` with `y=1, b=3`:

```
86×1  (black)
+ 15×3 (blue)
+  9×1 (yellow)
= 140
```

White contributes 0. That weighting is black=1, yellow=1, blue=3 — i.e. the 2-bit value with the main-door bit as 1 and an extra +2 on blue. Whether that weighting is *the* intended one is not proven. The arithmetic identity is.

Independently, the 14×14 grid has a number-theoretic 140 sitting next to its 196:

```
4 × (1+3+5+7+9+11+13)  = 196  = 14²
1²+2²+3²+4²+5²+6²+7²   = 140
```

That pair was also in the channel (`2026.txt` #57369). It needs no colour weights.

## 140 is not an AES password

Never tried, now tried. `packet/password_list_140.json`, 22 strings × raw + sha256hex × 4 KDFs × 3 blobs = **528** attempts, harness self-tested against the published Cosmic Duality decrypt.

**2 PKCS#7 successes, both `pad=0x01` / 79 bytes, chance ≈ 2.1. Zero readable. Zero `1GSMG` hits.**

| Tried | Result |
|---|---|
| `140`, `14` (“cut some zeroes”), `86`, `8686`, `86,86` | Closed — no decrypt |
| `1+4+9+16+25+36+49` and the concat `14916253649` | Closed — no decrypt |
| `hundred forty of the investment` and the full Architect capitals | Closed — no decrypt |
| `unbalancedequation` / `thesumofaremainderofanunbalancedequation` | Closed — no decrypt |

Machine log: `packet/out/results_140.json`.

## What that actually means

The Architect named 140. The grid *is* 140, two different ways, on clean authored assets. 140 is not a key for leftover 3.2, the Salphaseion fragment, or Cosmic Duality. So it is the same kind of thing the FEFEFE cell is: a **positional / structural** datum the Architect told us to expect, which no packet’s “readable plaintext or prize-key match” criterion can detect.

A natural next consumer is a length or a skip: take 140 of something (letters, bits, cells after a cut), or treat 140 as the “investment” count in whatever process the yin-yang still names. What is *not* next is another AES list built from the screenshot pair, and not another leftover-3.2 password.
