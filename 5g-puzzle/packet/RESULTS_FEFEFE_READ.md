# FEFEFE as a read instruction (2026-09-08)

Closed packet. 72 takes. No AES. Machine log: `packet/out/results_fefefe_read.json`.

Grey is at CCW spiral **164** = midpoint of 160 and 168 = byte group **21**, offset **4**. This packet treats that as a *how to read*, not as a password (already closed in `RESULTS_YBPOS.md`).

Source: majority-vote grid of `follow_the_white_rabbit.png` (census K86 W85 G1 B15 Y9). Self-check: cell 164 is `G`; unflipped main-door bits still decode `gsmg.io/theseedisplanted`.

## Frozen encodings

1. **Bit 164.** Insert 0, insert 1, flip, drop. Also XOR offset-4 of character 21 of the URL.
2. **Half-step spiral.** Classify the pixel at the midpoint of every consecutive pair of cell centres (195 samples). Read those; also interleave cell/midpoint (391).
3. **Stride 4.** Four phases of the 196-cell spiral; plus stride-4 forward and backward from 164.
4. **Read-heads** at 164 / 21 / 4 into the 765-letter stream, `faed` (570), `dbbi` (91): suffix, prefix, 24-letter window, stride-4. `dbbi` 7×13 / 13×7 row and column named by 4 and by 21 mod shape. `faed` 15×38 row/col of index 164 and of 4 / 21.
5. **25-event gather** of letters at the 9Y+15B+1G indices (positional, not a password retry).
6. Y/B/G cells from 164 onward.

Success: a `gsmg.io/` path other than the main door, an in-channel SHA-256, or a `1GSMG` window. No sliding windows. `{1,4,21}` unused as coordinates.

## Verdict

**No second door.** Zero prize-key hits. Zero in-channel SHA-256 hits.

| Encoding | Result |
|---|---|
| Flip bit 164 / XOR char-21 bit 4 | `gsmg.io/theseedispla~ted` — that is `n` (0x6E) flipped at MSB-first offset 4 to `~` (0x7E). Not in the Wayback CDX. Not a door. |
| Insert 0 / 1 at 164 | Garble after `pla`: `…plag:2\xb2` / `…plaw:2\xb2` |
| Drop bit 164 | `…pla\|\xe8\xca\xc8` |
| Half-step 195 | Census W85 K82 B17 Y10 G1 (edge bleed of Y/B). 24 bytes of noise, not ASCII. |
| Interleave 391 | 48 bytes of noise |
| Stride-4 phases | 49 bits each; one leftover decode `$+0`. Not a URL |
| Letter heads / dbbi / faed rows | a–i runs, not English, not a URL |
| 25-event gather | same a–i strings already hashed as passwords in the ybpos packet |
| YBG from 164 | `GYYBY` (grey plus the four remaining LSB colours) |

## What this closes

The extra door on piece 1, as a **grid encoding**, is closed. Grey is authored, it sits at a half-step, and every closed way of letting that half-step change the read — extra bit, flipped bit, dropped bit, half-cell sample, stride 4, stream head, matrix row/col — either reproduces the main door, produces the one-bit tilde of `planted`, or produces noise.

It is still a fact that cell (8,5) is FEFEFE. That fact does not open a path under the encodings above. Do not grow the list. Do not resume leftover-3.2 on these strings.
