# NULL: FEFEFE candidate replay -- 0 key hits, 0 pad >= 3 in 318 decrypts

**Result: NULL.** 106 candidates x 3 envelopes = 318 decrypts under the pinned gsmg profile.
3 outputs are pad-valid, all pad = 1 (expected 1.24). None reads as language, and `find_keys`
finds no Half or Better Half key in any of them. All three controls passed.

## Candidates

Read exactly from two files, nothing added:

| Arm | Source | Entries | Unique | New |
|---|---|---:|---:|---:|
| A | `5g-puzzle/packet/password_list_ybpos.json`, key `passwords` | 40 | 40 | 40 |
| B | `5g-puzzle/packet/out/results_fefefe_read.json`, `takes[].printable` | 72 | 69 | 66 |
| | **candidates.txt** | | | **106** |

- Arm A asserts 40 strings, 40 unique. Arm B asserts 72 takes.
- 3 of arm B's 72 printable values repeat inside arm B, for example `letters[:21]_1based` and
  `dbbi[:21]_1based` give the same string.
- 3 of arm B's 69 unique values are already in arm A: `caebhhbbefababaaaabbbbaab`,
  `ehfbgghifagagcadgheacggcc` and `hhbebdbfbfebaaabbaababbaa` (the three 25-event readings).
- `candidates.txt` keeps the first occurrence, arm A first in file order. `provenance.tsv` has all
  112 rows (string, arm, source name), duplicates included, so every dedupe can be traced.
- candidates.txt SHA256: `ccd637e883545ff7f18e78953539934d2649c6f1dbb610c8cb3c890aa4bd3d98`

## Pinned profile

**gsmg**: passphrase = lowercase hex of sha256(candidate) as 64 ASCII bytes; EVP_BytesToKey SHA-256,
1 iteration; AES-256-CBC; salt = envelope bytes 8..16; strict PKCS#7. No other profile was run.

## Preregistration

- `PREREG.json` holds the input file hashes, the candidates.txt hash, the counts, profile `gsmg`, the
  three `cc.ENVELOPES` names with their hashes, the three controls and the pass rules.
- Sealed 2026-11-27T19:30:41Z. `PREREG.sealed` = sha256 of the raw bytes of PREREG.json:
  `949c91a99d078a2aa88a1e989339e94f9ef531a8c7edb501022cf9b352f0f47c`
- Order: `replay.py build` wrote candidates.txt and provenance.tsv, `replay.py prereg` wrote and sealed
  PREREG.json, then `replay.py run` checked the seal and the candidates hash before the first decrypt.
- The seal was written by `replay.py`, not `tools/prereg.py seal`. That tool refuses a run directory
  that already holds the candidate file and requires `aes_use: "none"`, so it cannot seal an envelope
  replay whose statement includes the candidate hash.
- The hash is over LF line endings, as stored in git. A Windows checkout with `core.autocrlf=true`
  has CRLF copies whose hash differs; check against `git show HEAD:<path>`.

Pass rules (from PREREG.json): the run is valid only if all three controls pass. A **hit** is any
`find_keys` reading that derives Half or Better Half. Any real pad >= 3 is **notable** and inspected.
Otherwise the result is **null**.

## Controls

1. **Harness:** `cc.selftest()` passed. It reopens the Phase 3.2 envelope (pad 10, 2,422 B) and checks
   the Half hash160, EC k=1, WIF and the raw/hex detectors.
2. **Planted envelope, same loop:** an 80-byte `Salted__` envelope was built under the gsmg profile
   from passphrase `planted_control_fefefe_replay_2026_11_27` (fixed salt, 56-byte plaintext). The 106
   real candidates plus the planted string went through `decrypt_loop`, the same function as the real
   run. **Found: pad = 8, plaintext matches byte for byte.** One real candidate (`0x1ee7b32`) also gave
   pad 1 on the planted envelope by chance. Both are kept in `controls/planted_control/`.
3. **find_keys, k=1:** k=1 was added to `cc.TARGETS`, and a sample holding k=1 as raw32, hex64 and WIF
   went through `key_scan`, the same wrapper used on the retained outputs. All three readings hit.
   k=1 was then removed and `cc.TARGETS` was confirmed to be exactly:
   - Half `a9553269572a317e39f0f518cb87c1a0ee1dbae4` (1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe)
   - Better Half `4bc468447fe1b048ad030a2f9a125478eabc4ed6` (17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa)

## Pad histograms

Expected per envelope with N = 106: pad >= 1 = N/256 = 0.414; pad 1 = N x 255/65536 = 0.412;
pad 2 = 0.0016; pad >= 3 about 6 x 10^-6.

| envelope | decrypts | pad 0 | pad 1 | pad >= 2 | expected pad 1 |
|---|---:|---:|---:|---:|---:|
| terminal_phase3_2_end | 106 | 106 | 0 | 0 | 0.41 |
| salphaseion_short | 106 | 105 | 1 | 0 | 0.41 |
| cosmic_duality | 106 | 104 | 2 | 0 | 0.41 |
| **total** | **318** | **315** | **3** | **0** | **1.24** |

- No pad >= 3 on any envelope.
- All envelopes, Poisson lambda 1.242: P(X >= 3) = 0.130.
- Cosmic Duality alone, lambda 0.414: P(X >= 2) = 0.065. That is not small after looking at three
  envelopes, and the two outputs are random bytes (below).

## Retained plaintexts and key scan

Every pad-valid plaintext is kept whatever its pad. `find_keys` ran on each one against Half and
Better Half, compressed and uncompressed.

| file | candidate | source | pad | bytes | printable | raw32 windows | hex64 / WIF / base64 | key hits |
|---|---|---|---:|---:|---:|---:|---|---|
| `outputs/salphaseion_short/0.bin` | `faedggeedfcbdabhhggca` | B `faed[:21]_1based` | 1 | 79 | 43.0% | 48 | 0 / 0 / 0 | none |
| `outputs/cosmic_duality/0.bin` | `cicggifdcgaaggfbigaicfbh` | B `faed[164:188]_1based_24` | 1 | 1,327 | 36.6% | 1,296 | 0 / 0 / 0 | none |
| `outputs/cosmic_duality/1.bin` | `ihbegge` | B `dbbi_13x7_row4_1based` | 1 | 1,327 | 39.2% | 1,296 | 0 / 0 / 0 | none |

Printable = bytes in Python's `string.printable` minus `\x0b\x0c` (98 of 256 values, so random bytes
average 38.3%). All three sit at that level. None reads as language.

**find_keys hits: 0** on Half, **0** on Better Half, across 2,640 raw32 windows and 0 hex64, WIF or
base64 key-shaped strings.

## Files

| file | what |
|---|---|
| `replay.py` | `build`, `prereg`, `run` |
| `candidates.txt` | 106 unique candidates, one per line |
| `provenance.tsv` | 112 rows: string, arm, source name |
| `PREREG.json`, `PREREG.sealed` | statement and its seal |
| `results.json` | histograms, controls, every retained output with its key scan |
| `outputs/ENVELOPE/N.bin` | the 3 pad-valid plaintexts |
| `controls/planted_control/N.bin` | the planted plaintext and one chance pad-1 output |

Reproduce: `python replay.py run` on a fresh copy without `outputs/`, `controls/` and `results.json`.
After the run, one comment in `replay.py` was corrected (the planted plaintext is 56 B, pad 8, not
57 B, pad 7). No code changed; the planted length in PREREG.json was computed, not taken from the
comment.
