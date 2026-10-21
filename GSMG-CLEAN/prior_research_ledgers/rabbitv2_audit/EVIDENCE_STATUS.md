# Primary-evidence recovery status (Sep 2026)

Wayback, Arctic Shift, and the Telegram export were reachable this pass.
Inventory: `analysis/out/binaries_status.txt`. Chain / mempool fetches still
out of scope here.

## 1. `gsmg.io/puzzle` bytes — PNG recovered, pre-PNG 2019 not in CDX

Status: **PNG in repo, all copies byte-identical.**
`sha256 38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830`
29931 B, 1048×1556 RGBA. Same digest as Wayback 2020-11-12
`3L3FK2TTD6NM25PIFB4TOXFYZUPLZ4MW`. CDX has **zero** `gsmg.io/puzzle` rows
before that date. 2020-11-09 `/Puzzle` (capital P) is the GSMG Vue SPA, not
the image.

Reddit `bf7siz` (Arctic Shift): created 2019-04-20, edited 2019-06-05 with
`09jszg03cf231.png` 1048×1556. Edit note: picture changed to PNG for hidden-
things quality; original link `https://gsmg.io/puzzle`. Pre-June-5 bytes
(whatever format they were) are not in Wayback and not in this repo.

Canonical local file: `posters/reddit_2019-04-20_09jszg03cf231.png`
(also `posters/wayback_20201112_gsmg_puzzle.png`). Stego-negative still
applies to *this* PNG only. Do not treat a missing 2019 JPEG as a second
poster until one is found.

## 2. Barrystyle Cosmic Duality image — recovered

Status: **IN REPO.** Telegram `#8310` 2022-12-10 `from: barrystyle`,
`files/image_2022-12-11_07-09-14.png`, copied to
`posters/barrystyle_2022-12-11_cosmic_duality.png`.
`sha256 3a9b0a6ecacef83e1ef9f688303105570b3dcae95fd82be75f1fcbd2f5fddd04`
146396 B, 377×499 RGBA.

Surface: Time-Life *Mysteries of the Unknown* book cover titled Cosmic
Duality — galactic yin-yang, white/blue nucleus on top, yellow nucleus
below. Matches Jrk `#8311`/`#8315` “very specific / scary specific”.
LSB R/G/B/RGB and PNG text chunks (`open_named_envelope.py`): no hidden
string. Cover title is not used as a Cosmic password here; Cosmic is the
upstream document (gate D), opened by a twin, not by the JPEG/PNG filename.

## 3. Gate status — do not cite as closed

- `zeroed.py`: INCOMPLETE, ~300,160/~659,640 (45%), process died, no summary.
  Re-run to completion under `yinyang_gate.fullcheck`.
- `regate.py` 1,228,240 decrypts (Add.19): OLD gate — raw 32B windows only,
  blind to hex/WIF/base64 text keys (Add.21). Re-run under `fullcheck`.
  The 25 pad-1 decrypts from `firsthintisyourlastcommand` are included in the
  re-run set: pad-1 is uninformative, not disqualifying.
- Cosmic claim (`cosmic_plaintext.bin` sha256 `4f7a1e4e...`, 1,327B, entropy
  7.87): UNRESOLVED. Add.3 called noise (weak reasoning), Add.29 called door
  (broken control, withdrawn Add.30). Under current gate: pad-1 + high entropy
  + KDF round-trip = NOT arrival. Needs gate A-E (pad16 / text-key / on-chain /
  intel-doc / pre-20260701 CDX). XOR-7-sha256/MD5-KDF shape is now swept as one
  password family in `second_door.py`/`yinyang_carry.py` — declare arrival E/D
  before claiming.

## 4. Yinyang arrival test (binding)

See `analysis/yinyang_gate.py` ARRIVAL_TEST A-E. No sweep claims hit/null
without declaring target. Pad-1 rows are not printed as shortlist
(`second_door`/`yinyang_carry` already suppress them; `keep_decrypt.inspect`
flags only).

## 5. Where we stand (9 Sep 2026)

Prize still on Half `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` and Better Half
`17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`. Three envelopes still **locked**. **Computational focus is the main-line
terminal envelope only** (`b45a5e3d827593ca`). Do not spend decrypts on
SalPhaseIon or Cosmic until this blob opens.

| envelope | salt | raw | what would count as open |
|---|---|---:|---|
| **Phase 3.2 nested (main line)** | `b45a5e3d827593ca` | 96 | Gate A (pad-16 → 64 B) or C on *that* plaintext |
| SalPhaseIon AES (side door) | `3ab585348552415d` | 96 | held — not attacked |
| Cosmic Duality | `2d3f6fe06dc950e6` | 1344 | held — Gate D after a twin |

**Do not treat already-solved text as prize keys.** Gate C is an acceptance
test on a decrypt. Sliding Architect / outer 3.2 / VIC / first-hint SHA-256s
as secp scalars (`next_object.py`) skipped the lock. 0 hits; that pass is
closed as the wrong object, not as a null on the blobs.

**Named twin opening, 0 arrival** (`open_named_envelope.py`,
`out/named_envelope.txt`). Used **whitespace-strip compact (1544)**, which
keeps punctuation. Letters-only compact is **1539** (one apostrophe at
ws-index 352 is why 1544 puts `PRIVATEKEY` at 480). That 0-arrival is about
the 1544 landings. Do not re-run 1544 landings.

- 1544: `EPRIVATEKEYYOUVEEARNEDITBUTPLEAS` / `PRIVATEKEYYOUVEEARNEDITBUTPLEASE`
- 1539: `PRIVATEKEYYOUVEEARNEDITBUTPLEASE` at 479 — now tested against **term
  only** (`term_mainline.py`), including 34 word-windows from that landing.
  Null-for-Gate-A.

**Carried orphans + 479/163 as index, null-for-Gate-A** (`term_carry.py`,
`out/term_carry.txt`). X2SH with X,Y unfilled (`H=-42`, `B=-16`); nest
cell-bits `0100`; 32-byte slices at 479 and 163 in Architect / Beaufort CT
/ p32; yinyang concat of the 479-windows; genesis ASCII and 138-hex.
72 trials. Digits 9/15/479/163 not used as passwords.

**Nest-module door 1, null-for-Gate-A — lead retired** (`nest_module_door1.py`,
`out/nest_module_door1.txt`). Door 1's decoder over the nest at 15px (CCW/CW
× invert × start 0/1, remainder dropped) does not open a twin. Nest 10×10
is 22 K / 78 W. All seven mixed cells are majority-white at module scale;
`(7,6)` is K=6 W=19 (19 is white). Spill cells packed as white=0; the
drawing does not flip door 1. The nest carries **no payload under door 1's
alphabet**. Do not re-run. Next envelope is still the nested twin.

**SalPhaseIon unread stream:** `dbbi` (91) and `faed` (570) — 661 symbols,
no `o`. Length-reconciled in the 1,075-char page stream; **not decoded**.
Do not cite “no surplus” as a decode.

**SalPhaseIon door hash, null-for-Gate-A** (`salph_doorhash.py`,
`out/salph_doorhash.txt`). `89727c59…` is the page URL, not the AES
password (nor sha256 of that hash, nor the caption||address preimage).
22 trials.

**Phrase 7 vs Cosmic, Salph half-split — both null**
(`phrase7_and_halves.py`). Phrase 7 EVP SHA-256: 3 trials, not Gate D.
Enter 2+3 named pairs: 44 trials, 0 pad-16.

**Prime-delete/DEL on Phase 2 and 3.2 text, null-for-Gate-A**
(`del_primes_pt.py`). 66 trials on the terminal envelope. Leftovers are
gappy source English, not a new answer.

**dbbi/faed keyed classical suite, null** (`dbbi_classical.py`). 412
mod-9 / Bifid-3×3 / codec decodes keyed by solved answers. 0 English.
Still unread.

**2019 original puzzle image:** still missing. Wayback CDX has no
`gsmg.io/puzzle` image before 2020-11-12. Arctic Shift `bf7siz` only
has the post-edit PNG `09jszg03cf231`.

**24-marker selector vs 161 + 16-block concat, null**
(`marker24_phrases.py`, `out/marker24_phrases.txt`). Colour-split prime
and spiral-mod-161 selections (15+9), repeating mask, deque zipper, and
the 5+5+6 AES concat (Cosmic head and tail, three salts). 1,575 EVP
SHA-256 trials. 0 pad-16, 0 Gate D. Digits 9/15/479 not used.

**Values that are not OpenSSL passwords** (`unique_use.py`,
`extra_door_right_object.py`, `yinyang_carry_values.py`, `next_object.py`):

- Blue = 15 three ways: poster count, seed-tile red=1 byte, X2SH literal `15`.
- Yellow = 9 is an **index**, not an X2SH fill. Filling Y=9 breaks the
  mixed two-row 80 vs 81 (`|H|=42`, `B=-16` → 90 vs 80). QWERTY: Y over 6.
  X stays a hole. Do not invent it.
- 479=479 is the yellowblueprimes pair (zero the blue imbalance 5).
  Compact rule: letters-only 1539 (puzzle convention) vs whitespace-strip
  1544 (Add.32 landings). 479 is prime.
- Unused Warning verses are the *mechanic*, not GET paths. 8-bit packing
  them round-trips the verse (tautology).
- 9th yellow spiral idx 191 `(5,6)` and 15th blue idx 183 `(8,5)` already
  encode `theseedisplanted` (`d` LSB / `e` LSB). Not a second URL.
- `#fefefe` at `(7,4)` is spiral **163** 0-based (prime). Door-1 start-0.
  Not 162.

**`#fefefe` as operator, null-for-A-and-E** (`fefefe_operator.py`,
`out/fefefe_operator.txt`). 147 mutations (DEL/NUL insert-replace, `0xFE`
mask, LSB flip, wrap 19/20/21, 1539 landing included). Twin protocol:
orig||mut, split KDF, Salph `enter` 2+3. Named pairs half/betterhalf,
first/zero, 254/127 — not 9/15/479. 3,688 trials, 0 pad-16. First-pass
CDX `e24bd2c0…` was identity `maskFE` on the first-hint string (SPA
shell 12276). Gate E now rejects ~12,2xx as well as 700–2100.

**`matrixsumlist` as coordinates, null-for-clean-words**
(`matrix_coords.py`, `out/matrix_coords.txt`). QWERTY / VIC / Polybius,
0- vs 1-based. No sentence. X2SH still carried data.

Do not hash 9 / 15 / 479 / leftover lyrics into OpenSSL. Do not GET
`gsmg.io/<unused verse>`. Extra door is local (creator: solve no longer
needs the internet). Extra door in the poster is **still unfound**.

Logs: `out/extra_door_right_object.txt`, `out/yinyang_carry_values.txt`,
`out/unique_use.txt`, `out/next_object.txt`, `out/named_envelope.txt`,
`out/nest_module_door1.txt`, `out/fefefe_operator.txt`,
`out/matrix_coords.txt`, `out/term_mainline.txt`, `out/term_carry.txt`, `out/salph_doorhash.txt`, `out/phrase7_and_halves.txt`,
`out/del_primes_pt.txt`, `out/dbbi_classical.txt`, `out/marker24_phrases.txt`, `out/binaries_status.txt`.
