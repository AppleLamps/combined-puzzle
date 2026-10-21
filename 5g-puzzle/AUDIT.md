# Audit of packets 1–4 (2026-09-08)

Re-derived every load-bearing claim instead of restating it. Three defects, one of which invalidates a conclusion I published.

## Defect 1 — a classifier that erased FEFEFE (confirmed by execution)

`packet/extra_door_pixels.py` at commit `bb29c5d`, function `hsv_bucket`:

```python
if mn > 220 and mx - mn < 25:
    return "white"
```

`(254,254,254)` → `mn=254 > 220`, `mx-mn=0 < 25` → `white`. `(255,255,255)` → `white`. Both shades collapse. Executed both, confirmed identical output.

Blast radius:

| Artifact | Affected? |
|---|---|
| Main-door URL decode | **No** — grey encodes a `0` bit either way, so the decode validates regardless. This is why the bug survived. |
| `blue = 96791` in packet 2's frozen list | **Yes** — see defect 2 |
| "the colours contain nothing beyond the URL" | **Yes** — see below |
| Current `palette_bucket` / `extra_door_find.classify` | **No** — both keep `G` distinct, count 5625 grey px, and log spiral 164 |

The bug is not present in the current code. But the conclusion I drew *this turn* — that the colour layer is URL-redundant — was reached over a 24-event set, and the 25th event is exactly the one this classifier had erased.

## Defect 2 — packet 2 tested the wrong blue

Packet 2 froze `blue = 96791`, an HSV miscount. The exact-palette blue is **83700**. The channel had it right: `2026.txt` **#56158** `yelllow 50400?` / **#56159** `blue 83700?`. I explicitly excluded 83700 as "a second colour heuristic, not frozen here" — I excluded the correct number and kept the wrong one.

12 of packet 2's 20 strings involved blue, so the "yellow/blue numbers as an AES password" hypothesis was **not** closed by that packet. Re-run with 83700: still no decrypt (below).

## Defect 3 — one KDF, never justified

Packets 1–4 used only `EVP_BytesToKey` with **MD5**. OpenSSL ≥ 1.1.0 changed `enc`'s default digest to SHA-256, and nobody has ever opened the leftover 3.2 blob, so its KDF was an assumption, not a fact.

## Corrective runs

`packet/run_kdf_audit.py` re-runs **all** previously frozen passwords (199 unique) plus corrected blue operands under four KDFs — `evp_md5`, `evp_sha1`, `evp_sha256`, `pbkdf2_sha256_10000` — against leftover 3.2, the Salphaseion small blob, and Cosmic Duality. **4776 attempts.**

It self-tests first: reproduces the published Cosmic Duality 7-XOR plaintext hash `4f7a1e4e…c081` under `evp_md5`. Without that, a negative result proves nothing about the puzzle and everything about the harness. It passes.

Result: **25 PKCS#7 successes, 0 readable, 0 prize hits.** Every one of the 25 has `pad = 0x01` (`pt_len` 79 or 1327 — the maximum for each blob), at a rate of 25/4776 ≈ 1/191 against the 1/256 expected by chance. All noise.

`packet/password_list_ybpos.json` then tests the 25-event reading (960 attempts, four KDFs): **3 successes, 0 readable, 0 prize hits** — again exactly chance.

## What the audit changes

**`f73d92` is a tautology.** It is the low bit of each character of `gsmg.io/theseedisplanted`:

```
g s m g . i o / t h e s e e d i s p l a n t e d
1 1 1 1 0 1 1 1 0 0 1 1 1 1 0 1 1 0 0 1 0 0 1 0  ->  f7 3d 92
```

Yellow = even ASCII (9 chars), blue = odd (15). The counts follow too: 9 × 5625 = 50625 vs 50400 measured (0.4% edge loss); 15 × 5625 = 84375 vs 83700 (0.8%). So `50400`, `83700`, `9`, `15`, and `f73d92` are all the same fact restated, and that fact is the URL. Packets 2 and 3 spent their budget on a channel with no capacity.

**The FEFEFE cell is the one thing that is not.** Grey sits at CCW spiral **164** = the exact midpoint of 160 and 168, the LSB cells of characters 20 and 21. Byte group **21**, offset **4**. Character 21 is `n` = `0x6E` = `01101110`, whose MSB-first bit 4 is `0` — which is why grey-as-zero decodes the URL correctly and why the marker is invisible to any check that validates on the URL alone.

Read as 25 events the deltas are `8×19, 4, 4, 8×4`: a step-8 arithmetic sequence with one extra point wedged at a half-step. Twenty-four redundant symbols and one free parameter. Its value is not a password — that is now tested across four KDFs and three blobs — so it is positional: it names group 21, offset 4, or index 164.

## Process errors worth naming

- I called packet 2 "closed" on an operand I had measured wrong, and defended the freeze as procedural discipline. Freezing a list is only a guard against motivated search; it is not a licence to keep a wrong input.
- I stated a negative result about MD5-derived AES without ever validating the KDF assumption.
- I wrote "hashed observation" over `f73d92` without checking whether the observation had any information in it. Hashing something does not make it a finding.
- Every packet's success criterion was "readable plaintext or a `1GSMG` hit." Neither fires on a *positional* result, so the one non-redundant thing in piece 1 could not have been detected by any packet I ran.

## Still open, unchanged by this audit

`140` is consumed as a length on the spiral. The extra door on piece 1 is closed as a grid encoding (`packet/RESULTS_FEFEFE_READ.md`). Leftover 3.2 is unopened under four KDFs and every frozen list. Yinyang is unreached.
