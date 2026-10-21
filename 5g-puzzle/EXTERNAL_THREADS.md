# External threads (pulled 2026-09-08)

Three files uploaded to `main` (`23b31c9`). Checked against the closed packets. None of them open leftover 3.2 or `1GSMG`.

| File | What it is |
|------|------------|
| `reddit2.txt` | Reddit JSON: [r/bitcoinpuzzles/bf7siz](https://www.reddit.com/r/bitcoinpuzzles/comments/bf7siz/gsmgio_5_btc_puzzle_challenge/) — **2019-04-20**, OP `fecell`, 69 comments |
| `reddit1.txt` | Reddit JSON: [r/bitcoinpuzzles/dfwcqk](https://www.reddit.com/r/bitcoinpuzzles/comments/dfwcqk/gsmgio_5_btc_puzzle/) — **2019-10-10**, OP `Sandalphon69`, 128 comments |
| `bitcointalk-5151725-page-000.md` | Bitcointalk scrape of [topic 5151725](https://bitcointalk.org/index.php?topic=5151725.0), **page 1 only**, 11 posts, 2019-06-07 → 2026-01-01 |

## What is actually new (contemporaneous 2019)

**JPG vs PNG.** Same-week comments (2019-04-22): the image went into Telegram as **JPEG**, the website copy is **PNG**. OP update **2019-06-05**: picture “changed to PNG for better hidden things quality.” That is the one historically useful fact. The extra-door packet already used the PNG (the intended carrier). Raster LSB of that PNG is solid-color noise; `N82BIV` is **not** in the file bytes.

**fecell, 2019-10-16:** “about 6 month ago was solved all except last AES with PK” and ~200 days to the first halving. Matches the Telegram stall: leftover AES treated as the finish by late 2019, **before** Jrk’s 2020 extra-door comments. Not a new method.

Phase-2/3 walkthroughs on Reddit (hidden POST form, Logic lyrics, `causality`, chess / Luna HSM / genesis hex) are the published path already in the puzzlehunt README.

## What looks important and is not

**`Comprehensive-Bag493` (2025):** “hidden key in the QR finder corners,” dots-and-dashes 14×14 overlay, “PNG update messed up the image,” plus a tip address `12fdR7eLWYCLd767wXMkLQnS3eVdm9Zi22`. Same person (or same pitch) as the Bitcointalk miller420 quote: found a key, will share for 0.25 BTC. **No in-thread SHA-256 of a find.** Footer QR whites on our PNG are anti-aliased logo colors, not a second matrix. This is the failure mode already logged in `GROUP_COMMS_ANALYSIS.md` (DM / “I found it”).

**`Capable_Leather_9237` (2025-03-29):** LSB payload `BMP / EXE / GZIP / Clue(N82BIV)`. Not in `puzzle.png`. SHA-256(`N82BIV`) is not the prize pubkey. `N82BIV` / `n82biv` do not decrypt leftover 3.2.

**Bitcointalk `RaghavS19` (2025-09-11):** restates the published VIC sentence; posts a Beaufort hex blob and AES key `31f6b59a…173c12` + IV. That 32-byte key is **not** the `1GSMG` private key. It does not decrypt leftover 3.2 (OpenSSL password or raw key+IV).

**Bitcointalk `Furtumatic` (2025-09-19):** pastes the Architect Beaufort plaintext and VIC line, concludes “no solution / psychological trap.” That is a misread of 3.2.1/3.2.2 as the finish. Jrk 2026 `#63957`: puzzle still valid.

**Bitcointalk `pbies` (2026-01-01):** leftover blob is “solved, just put nonce/tag in an AES decrypter.” The blob is OpenSSL `Salted__` AES-256-CBC. Packet 1–2–4 already exhausted the closed passwords we had.

Late Reddit “Puzzle solved” posts (2025-12-17) only quote the same two published sentences.

## Closed checks run from these files

| Candidate | Prize pubkey | Leftover 3.2 |
|-----------|--------------|--------------|
| Posted key `31f6b59a…173c12` | no | no |
| Posted IV as password | — | no |
| `N82BIV` / `n82biv` / sha256(`N82BIV`) | no | no |

No Jrk extra-door / yinyang / passport statements here that are missing from the Telegram export. No new `gsmg.io` path.

## Board impact

Do not grow AES or FAED from these threads. The only durable addendum is **2019 PNG-for-hidden-things + Telegram-JPEG**, which does not change the extra-door verdict: the published PNG’s finite encodings are closed; a hashed door was not opened.
