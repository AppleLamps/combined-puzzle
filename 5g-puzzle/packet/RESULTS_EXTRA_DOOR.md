# Extra-door packet results (2026-09-08)

Not AES. Piece 1 only. `{1,4,21}` not used.

`puzzle.png` SHA-256: `38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830`  
Machine log: `packet/out/extra_door_find.json`

## Verdict

**No second door opened.** The published main door reproduces. Frozen alternate encodings of the same 14×14 grid do not yield another `gsmg.io/…` path. No find is claimed.

What *is* hashed, and is not a door opening:

| Object | Value | SHA-256 |
|--------|--------|---------|
| Main door (reproduced) | `gsmg.io/theseedisplanted` | `3a3f0e24…b2e9` |
| Footer HASHTHETEXT (known Salph entry, **not** extra door) | title+address | `89727c59…6a32` |
| Extra channel B=1 Y=0 | 3 bytes `f73d92` | `2bd15e7d…5913` |
| Extra channel Y=1 B=0 | 3 bytes `08c26d` | `36402a06…887b` |
| Spiral color string | 196-char Y/B/K/W/G | `a8bc867b…f1ab` |

HASHTHETEXT is the known hash of the piece-1 title+prize address that opens Salphaseion. Unedited `#7914` still named another door **after** Salph was a reached stage, so that hash is not the extra door.

## What the image actually is

Exact palette (HSV blue **96791 was wrong**; leftover-3.2 list that used it stays frozen):

- Yellow `(255,242,0)`: **50400** pixels, **9** cells
- Blue `(63,72,204)`: **83700** pixels, **15** cells
- Grey `(254,254,254)`: **5625** pixels = one full cell at **(8,5)** 1-indexed (CCW spiral index **164**)
- No PNG text/stego chunks. Raster LSB prefix is solid-color noise.

CCW spiral, black/blue = 1, yellow/white/grey = 0 → `gsmg.io/theseedisplanted` (**main door**, the one Jrk said the nest had already shown).

## Extra channel (hashed observation)

All 9 yellow + 15 blue cells sit on 1-based CCW spiral indices that are **multiples of 8** — the LSB of each of the 24 bytes of the main-door ASCII.

Those 24 bits, B=1 Y=0, are `f73d92`. Invert: `08c26d`.

> **Correction (audit, 2026-09-08).** This section originally called `f73d92` "the yellow/blue distinction the 1-bit main door throws away." That is wrong. `f73d92` is **exactly** the low bit of each character of `gsmg.io/theseedisplanted`, so it is fully determined by the URL and carries **zero** additional information. Yellow marks the 9 characters with even ASCII, blue the 15 with odd. The pixel counts are redundant for the same reason: 50400 and 83700 are 9 and 15 cells of 5625 px, less edge antialiasing.
>
> **The FEFEFE cell is the exception and this packet under-tested it.** Grey at spiral 164 is not on a byte LSB, and that line was treated as a dismissal. It is not. 164 is the exact midpoint of 160 and 168 — the LSB cells of characters 20 and 21 — i.e. byte group **21**, offset **4**. That position is *not* derivable from the URL. Read with grey as a distinct state, the colour layer is **25 events**, not 24: twenty-four URL-redundant ones plus one free marker. See `RESULTS_YBPOS.md`.

The rabbit is black/white pixels on white cells around rows 7–9, cols 7–10 (1-indexed). It is not a second color layer.

## Frozen encodings that did not open a door

13 alternates (invert, yellow-only, blue-only, 2-bit maps, skip-KW, grey=1). Zero extra `gsmg.io` paths. Do not grow this list.

## After this packet

The extra door is still **unopened**. This packet closed the finite 14×14 encodings of the published PNG. Next work is not another AES list and not `{1,4,21}`. Leftover 3.2 remains an encrypted blob; yinyang remains unreached (Jrk 2025). The extra-channel bytes are on the board if a later *closed* operation needs an operand — they are not used here as a password.
