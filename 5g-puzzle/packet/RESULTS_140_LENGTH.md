# 140 as a length (2026-09-08)

Closed packet, no AES. 43 takes. Machine log: `packet/out/results_140_length.json`.

Rule: take exactly 140 of an authored stream — first, last, skip-140-then-140 — plus the one exact arithmetic cut on the spiral. Score URL / printable English / in-channel SHA-256 / `1GSMG` pubkey. Do not feed the takes back into leftover 3.2.

## The cut that actually equals 140

`gsmg.io` is **7 characters = 56 cells**. The spiral is 196. 196 − 56 = **140**. That is not a coincidence with `1²+…+7² = 140` sitting next to `14² = 196`: 7 is half of 14, and 7 characters is the hostname.

Majority-vote spiral, drop the first 56 cells, read the remaining 140 as the main-door bit (K/B = 1, Y/W/G = 0):

```
/theseedisplanted + 0000
```

The four trailing bits are the four cells after the 192-bit URL: **`WWWW`**. They carry zeros. The 140-cut is the main door with the hostname stripped, padded with four empty cells.

The other end of the same stick — first 140 bits of the full spiral:

```
gsmg.io/theseedis + 0111
```

`0111` is the first nibble of `p` (`01110000`). So first-140 vs last-140 is the URL split after `theseedis` / after `gsmg.io`. Both are the door we already have.

## Everything else

| Stream | n | 140-takes | Result |
|---|---|---|---|
| Spiral cells / main bits / 2-bit (the 86+15×3+9×1 weights) | 196 | drop-56, first, last | URL split as above. 2-bit is not ASCII. |
| Salphaseion letters | 765 | 5 non-overlapping windows + last | a–i runs, not English, no URL |
| `faed` | 570 | 4 windows + last | same |
| VIC digits | 149 | first 140 / last 140 | leftover 9 digits `711154112` / dropped 9 `151659431`. VIC already decodes at full 149; cutting it does not produce a key. Drop-zeros is 145, not 140 (only 4 zeros). |
| Cosmic Duality plaintext | 1327 bytes | first/last/skip 140 bytes, and 140-hex windows | binary, no prize-key window, no known SHA-256 |
| Architect clause that names 140 | 89 chars | the clause itself (shorter than 140) | already-published sentence |

Zero `gsmg.io/` paths that we did not already have. Zero `1GSMG` hits. Zero matches against the four in-channel SHA-256s.

## What this closes

140-as-length on the spiral **has** a consumer: it is the main-door URL with `gsmg.io` removed. That is why the Architect could name 140 without it being a password or a leftover-3.2 key. It is not a second door.

140-as-length on VIC, `faed`, the letter stream, and the Cosmic Duality plaintext does not produce a new artifact under this closed rule. Do not slide a 140-window across those streams one offset at a time — that is an unbounded search dressed as a length.

The FEFEFE cell at spiral 164 is still unconsumed: it sits *inside* the 140 (drop-56 index 164−56 = 108, still group 21 offset 4 of the original). The 140-cut does not isolate it.
