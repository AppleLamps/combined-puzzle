# 25-event packet results (2026-09-08)

Closed list SHA-256 recorded in `packet/out/results_ybpos.json`
(`packet/password_list_ybpos.json`, 40 unique strings × raw + sha256hex × 4 KDFs × 3 blobs = **960** attempts)

Tests what packet 3 recorded but never tested: the FEFEFE cell as a 25th event.

## Why this packet exists

Packet 3 read the colour layer as 24 events (9 yellow + 15 blue) and I concluded the colours carry nothing beyond the URL. The first half is right and stronger than I realised — `f73d92` *is* the URL's ASCII low bits, and the pixel counts are just 9 and 15 cells. The second half was too strong, because the 25th marked cell is not URL-derivable and an earlier classifier (`hsv_bucket`, commit `bb29c5d`) had erased it by bucketing `(254,254,254)` and `(255,255,255)` both as white. Details in `AUDIT.md`.

## The marker

| Property | Value |
|---|---|
| CCW spiral index (1-based) | **164** |
| Cell (1-indexed) | (8, 5) |
| Byte group | **21** |
| Offset in group | **4** |
| Geometry | exact midpoint of 160 and 168 |
| Character 21 | `n` = `0x6E` = `01101110` |
| Bit it carries | `0` (MSB-first offset 4) |

Grey encoding `0` is why the URL decode validates with or without the distinction — the bug was invisible to the only check packet 3 applied.

25-event deltas: `8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8`. Step-8 with one half-step insertion.

## Verdict

**The marker is not an AES password.** 3 PKCS#7 successes in 960 attempts (chance ≈ 3.75), zero readable, zero `1GSMG` hits.

| Hypothesis | Result |
|---|---|
| `164`, `21`, `4`, `21,4`, `160168`, cell `8,5` as password | **Closed — no decrypt** |
| 25-bit stream with grey=0 and grey=1 (`0x1ee7b22` / `0x1ee7b32`, byte-aligned both ways) | **Closed — no decrypt** |
| Yellow/blue as *positions*: sums 143 / 157, spiral sums 1144 / 1256, concatenations | **Closed — no decrypt** |
| Salphaseion letters read at the 25 event indices (4 variants) | **Closed — no decrypt** |
| All of the above under `evp_sha1`, `evp_sha256`, `pbkdf2_sha256_10000` as well as `evp_md5` | **Closed — no decrypt** |

Harness self-tested against the published Cosmic Duality 7-XOR decrypt before each run.

## What this leaves

The marker survives as a **positional** datum, and no packet I have run could detect a positional result — every success criterion was "readable plaintext or a prize-key match." Group 21 / offset 4 / index 164 needs a consumer, not a cipher.

Incidental confirmation that the letter extraction is sound: Salphaseion letters `[91:195]` are an a/b-only run, and read as `a=0 b=1` they are `6d617472697873756d6c697374` = **`matrixsumlist`** in ASCII. The `dbbi` block proper is the first 91 letters, 91 = 7 × 13, with `matrixsumlist` being 13 bytes.

Machine log: `packet/out/results_ybpos.json`.
