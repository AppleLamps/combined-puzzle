# What to do next (2026-09-08, post-audit)

The audit turned up a defect that turned out to be the smaller half of the problem. Chasing it produced a provenance finding that changes the footing of everything.

> ## Correction (2026-09-08, later)
>
> **`puzzle.png` is authentic and this document originally said otherwise.** The Wayback Machine serves `gsmg.io/puzzle` as sha256 `38125bbd…1830`, byte-for-byte identical to `artifacts/puzzle.png`, with the same Wayback digest `3L3FK2TTD6NM` across captures on 2020-11-12, 2023-01-08, 2026-01-04 and 2026-04-18. It is the original site asset, and the third-party repo mirrored it faithfully.
>
> So the red `(237,28,36)`, the `(245,245,245)` footer and the QR region at y=1297–1512 are **authentic puzzle content**, not writeup furniture as claimed below. The red is confirmed independently: it is the exact same red as the eight authored images on `gsmg.io/theseedisplanted`.
>
> `follow_the_white_rabbit.png` is a *separate, smaller* asset — 350×350, the 14×14 grid alone at 25 px per cell, with no footer and no red. Both files are genuine; they are not two versions of one thing. The FEFEFE cell appears in both (625 px in the 350, 5625 px in the 1048), so the 25-event conclusion holds and is now confirmed twice over on independent authored assets.
>
> Also withdrawn: `door.png` is not a payload. It and `static/images/door.png` are the site's app-shell HTML under brotli and gzip respectively, both decompressing to the same 36123 bytes. Wayback's `id_` returns the compressed response body, which is why it looked like high-entropy binary. `door.bin` has been deleted from the repo.
>
> What survives from the section below: the Cosmic Duality file really is a browser screenshot and must never be measured again, and asset provenance really is load-bearing. See `packet/RESULTS_140.md`.

## The finding that reorders the work

**We have never analysed an original puzzle asset.**

| What we analysed | What it actually is |
|---|---|
| `artifacts/puzzle.png` — 1048×1556, 453 colours | ~~third-party composite~~ — **wrong, see correction above: this is the authentic `gsmg.io/puzzle`** |
| `artifacts/SalPhaselonCosmicDuality.png` — 668×619, 593 colours | a **browser screenshot** — Chrome toolbar band `(241,243,244)` across the top rows |

The real asset is `gsmg.io/img/follow_the_white_rabbit.png`, recovered from the Wayback Machine. Three separate captures (2020-11-15, 2024-04-06, 2026-01-03) are **byte-identical**, sha256 `5e8d84b8…d204f`, 1958 bytes:

- **350×350**, cell size **25**, not 75
- **exactly 5 colours, zero antialiasing**
- black 54675 · white 52200 · blue 9375 · yellow 5625 · **FEFEFE 625**

Cell arithmetic closes perfectly: 9 yellow + 15 blue + 1 grey = 25 cells = 15625 px; the remaining 171 cells = 106875 px = black 54675 + white 52200 exactly. 196 cells, no slack.

Everything in the composite that is *not* in the original — red `(237,28,36)` 15705 px, the `(245,245,245)` 422912-px footer, the QR region at y=1297–1512 — is somebody's writeup furniture. The pixel counts we argued about (50400, 83700, and the 96791 miscount) were all measurements of a 3× upscale of someone else's reconstruction.

## The 25th event is authored, and confirmed on clean data

This settles it. In a 5-colour image with no antialiasing, FEFEFE occupies **625 px = exactly one 25×25 cell**. It cannot be a resampling artifact. Re-extracting the grid from the original:

- cell census `K 87 · W 84 · B 15 · Y 9 · G 1` = 196
- CCW spiral, K/B=1, Y/W/G=0 → `gsmg.io/theseedisplanted`
- all 24 Y/B cells on multiples of 8
- grey at spiral **164** → byte group **21**, offset **4**

So the colour layer is 24 URL-redundant symbols plus one deliberately placed marker, and the marker is design intent. It is not a password — closed across four KDFs and three blobs — so it is positional.

## Priorities

**1. Rebase on originals, then re-derive.** Piece 1 is done (`artifacts/original/follow_the_white_rabbit.png`). The Cosmic Duality / SalPhaseIon page assets still need recovering; the screenshot must not be measured again. Retire the composite from any measurement role and keep it only as a provenance exhibit. Note the 2019 fact from `EXTERNAL_THREADS.md` — Telegram got a JPEG, the website served a PNG, and the PNG was the one intended for "hidden things" — which makes asset provenance load-bearing rather than pedantic.

**2. Fix the success criterion.** Every packet so far scored "readable plaintext or a `1GSMG` match." Neither fires on a positional or structural result, so the one non-redundant thing in piece 1 was undetectable by construction. A packet needs to score base58/WIF shape, BIP39 hits, `gsmg.io/<path>` strings, and matches against in-channel SHA-256s.

**3. ~~Find the consumer for "group 21, offset 4."~~ Done — closed as a grid encoding.** Half-step midpoints, bit insert/flip/drop at 164, stride-4, letter-stream heads at 164/21/4, dbbi/faed row/col. 72 takes, no second `gsmg.io` path, no prize hit. Flip-164 is `gsmg.io/theseedispla~ted` (bit identity of `n`→`~`), not in the archive. The extra door on piece 1, as a grid encoding, is closed. `packet/RESULTS_FEFEFE_READ.md`.

**4. Identify `gsmg.io/door.png`.** Archived 2025-05-05, 10035 bytes, saved as `artifacts/original/door.bin`. It is **not** a PNG: magic `1b1a8dcc484dea01`, all 256 byte values present, no `Salted__` header. High-entropy payload under a `.png` name on the puzzle's own domain, and nothing in our notes mentions it.

**5. Harvest the full archive inventory.** The CDX query hit its 500-row limit (`artifacts/original/wayback_cdx_gsmg_500.json`); page through the rest. Already visible and unexamined: `img/blue_ca.png`, `img/blue_dig_i.png`, `img/blue_lock_lo.png`, `img/black_banking - war.png`. Also diff captures of the same URL across timestamps — the rabbit is stable across three, but other assets may not be, and a changed asset is a dated authorial edit.

**6. 140 is a property of the grid, consumed as a length on the spiral.** Majority 86/86/15/9 and `1²+…+7² = 140` next to `14² = 196`. The exact cut is `gsmg.io` = 7 chars = 56 cells, 196−56 = 140, and those 140 main-door bits decode to `/theseedisplanted` plus four zero bits (`WWWW`). First-140 is `gsmg.io/theseedis` plus the first nibble of `p`. So 140-as-length is the main door with the hostname stripped, not a second door. VIC / faed / CD-plaintext 140-windows produced nothing. AES closed earlier (528 attempts). `packet/RESULTS_140.md`, `packet/RESULTS_140_LENGTH.md`.

**7. Read the eight `theseedisplanted` images.** Recovered to `artifacts/original/theseedisplanted/`. `gsmg.io/theseedisplanted` as archived 2020-11-12 is a bare page whose entire body is eight `<img>` tags: one black, three blue, four red, each about 80×70. The filenames read as a rebus — `lock_lo` plus `crypto_gic` gives `lo` + `gic`, and `dig_i` plus `t` starts `digit…`. They use exactly the `puzzle.png` blue and red. Nothing in our packets or the forum dumps mentions them. (They are the already-solved Phase-1 Logic *The Warning* rebus → password `theflowerblossomsthroughwhatseemstobeaconcretesurface`.)

**8. ~~Stage-3 `# X 2 S H 4 Y 0 Q B 15 #` as leftover-3.2 SHA-256.~~ Done — consumed architecture, not an unused key.** Phase 2 plaintext, already spent as the Safenet Luna HSM hint that opened `phase3.txt`. B=25 and H=42 drop the puzzle's own `²` / `×-1`. 29 strings including `32,42,82,25`, reversal, published −42/−16, and the Rotterdam DMS: 696 attempts, 0 readable. `packet/RESULTS_STAGE3.md`.

**9. ~~Architect substitution delta as leftover-3.2 passwords.~~ Done — instructions, not a password.** The Beaufort 3.2.1 speech is Reloaded's Architect almost verbatim; the replacements are the message. 42 strings × raw + sha256hex × 4 KDFs × 3 blobs = 1008 attempts, harness self-test pass, 7 PKCS#7 `pad=0x01` collisions, 0 readable, 0 prize. Do not brute despite the inserted sentence. Do not resume 7-interleave. `packet/RESULTS_ARCHITECT_DELTA.md`.

## What does not need more work

Leftover 3.2 is closed against every frozen list under four KDFs, including the Architect substitution phrases. The 7-intertwined-passwords reading is closed. `{1,4,21}` is falsified. The yellow/blue *counts* are closed. 140-as-password and 140-as-length are closed. The piece-1 extra door, as a grid encoding, is closed. Stage-3 numbers are consumed HSM architecture. The Architect delta is instructions, not an AES password. Do not resume the 7-interleave. Do not grow leftover-3.2 lists from already-closed operands. Do not brute leftover 3.2.
