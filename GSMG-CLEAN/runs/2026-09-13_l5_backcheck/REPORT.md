# L5 back-check: strings on disk → DBBI hash pattern — 2026-09-13

**Status: STOPPED at 4,443 of 4,444 jobs** (at the user's request, t ≈ 1,100 s). `results.json` was never written, because the script writes it only at the end. Everything below comes from `run_log.txt`, which logs every DBBI match line and a progress line every 200 jobs or whenever a job takes more than 30 s, plus a separate control re-check (`controls_recheck.txt`).

**Result so far: no real match.**
- 22 DBBI-pattern lines were logged. **All 22 are the identity view of the pattern string itself**, `01234556728966286abc61c88b48de3086dd501d5557d6bab5605233df7bbb96` (raw + upper), where our own notes, tools and chat logs quote it.
  - That string trivially has its own equality pattern. It is not a digest of anything.
- **0 matches came from hashing a string** under sha256, sha256d, sha256-of-hex or sha3-256, in any orientation.

## What the gate is

- **L5:** DBBI tokenised with `b`/`g` starting 2-letter tokens gives 64 tokens and 16 codes. The first-seen equality pattern is shown above. It is recomputed from `data/DBBI_91.txt` at start-up.
- **Match condition:** a digest matches only if its 64 hex characters have exactly that pattern.
- **Chance for a random 64-hex string:** 16!/16^64 = **2^-211.7**.
  - The manifest text says "2^-212.1", a rounding slip; the exact value is 2^-211.75.
  - The older docs say "≈ 2^-100", which is conservative.
- **Over this run:** ≈ 1.1 × 10^9 digest checks ≈ 2^30, so the chance of any false positive is ≈ 2^-182. A single non-trivial hit would have been proof.
- **Gate self-test (at prepare and run):** a synthetic DBBI-substituted digest matches, and the same digest with one nibble changed does not.

## What was covered (manifest `ebaf8580…adcf`, script sha256 `33d611f6a185…`)

**Sources** (read-only walk):

| Root | Unique files | MB |
|---|---|---|
| E:\rabbit-combined | 1,941 | 435.6 |
| D:\puzle | 740 | 1,538.0 |
| D:\astra | 354 | 57.4 |
| E:\testing-btc-p\fresh-start | 137 | 65.2 |
| Desktop\idk-btc | 1,152 | 319.2 |
| .claude\projects (7 puzzle project dirs, this session excluded) | 31 | 50.7 |
| .codex\sessions + archived (only files containing gsmg / salphaseion / dbbi / cosmic duality / theseedisplanted) | 74 | 1,255.4 |
| **Total** (7,139 listed, deduplicated by content hash) | **4,429** | **3,721.6** |

Plus 15 special jobs:
- **word n-grams 1–12 and sentences** of the 6 reference texts and the readable Architect plaintext
- **substrings of length 1–64** of the Architect letters, checkerboard, DBBI, FAED, DBBI−VIC, FAED-Bifid, Hill IFINDO and the 1,075-character SalPhaseIon stream

**Harvest per file** (deduplicated within a file):
- **JSON:** every string value, key and number, joined Telegram texts, and every line of multi-line strings
- **`.py`:** every literal
- **text files:** lines, table cells and quoted / backticked substrings
- **hex strings (16–8,192 characters):** also decoded to bytes. This is how the `password_hex` / `preimage_hex` fields of the 770 MB and 550 MB pre-registered candidate files were covered.

**Per string:**
- up to 11 forms: raw, strip, lower, upper, no-whitespace lower/upper, alnum lower, letters lower/upper, +LF, +CRLF
- 4 hash views, or identity if the form is itself 64 hex
- 3 orientations: hex, char-reversed, byte-reversed

**Counts at the last progress line** (4,443/4,444): 16,797,214 unique strings (summed per file) → **1,117,326,681 digest checks**.

## Controls

**Planted controls: 8 / 8 recovered.**
- Method: eight real strings from eight random files of different types. Each got a random form, view and orientation, and its digest pattern was added as an extra target.
- The in-memory control tallies were lost when the run stopped. The script (hash-verified against the manifest) was therefore re-run on the 8 control files alone, and every planted control was found at its planted file, digest-input bytes, view and orientation (`controls_recheck.txt`).
- Those files also give a DBBI prefilter pass rate of 4,666 vs 4,765.6 expected (0.979).
- Separately, 3,000,000 sequential sha256 digests gave 11,666 vs 11,718.75 expected (0.995).

## Where it left off (for a resume)

**Not covered: exactly one job**, the one still running when the run was stopped.
- The log does not name it, because jobs under 30 s are logged only every 200th completion.
- Every file larger than 20 MB appears in the log as finished, except three that may simply have finished in under 30 s:
  - `C:\Users\lucas\.codex\sessions\2026\08\22\rollout-2026-08-22T23-23-35-01a02ca5-….jsonl` (58 MB)
  - `E:\testing-btc-p\fresh-start\derived\rotating_grille_bridge.json` (37 MB)
  - `runs/2026-09-13_seven_key_bifid/candidates.json` (23 MB)
- The long-running job is most likely one of these three. A resume should add a per-job completion log and re-run just these three files; each takes minutes at most.

**Not written:** `results.json`, which would have held the per-root tallies, the harvest-mode counts, the files changed since prepare, and read errors. None of these are needed for the headline null.

## Scope of this null

It covers exactly the strings that the harvest rules extract from the files in `manifest.json`, under the forms, views and orientations above. It does **not** cover:
- **Generated candidates that were never saved.** Round-1 generators such as `matrix_quotes.py` / `sweep2.py` / `bigsweep.py` contribute only their literals, not the combinations they built at run time.
- **Other text extraction:** words inside long prose lines of Telegram messages (whole messages, lines and quoted pieces only), and n-grams outside the 7 reference texts.
- **Other hashes or preprocessing:** md5 / ripemd / keccak, salted or iterated hashes, other encodings (UTF-16, Latin-1), other case or spacing variants.
- **Other token maps:** mappings of DBBI other than the `bg` 64-token parse.
- **The one unfinished job** (above).

A null here is decisive **only for those strings**: none of them is the answer whose sha256 is DBBI under L5. It says nothing about whether L5 is real.

## Files

| File | Contents |
|---|---|
| `run_l5_backcheck.py` | `prepare` / `run` |
| `manifest.json` | pre-registration: roots, rules, all 4,429 files with sha256, 8 controls, gate self-test digest |
| `run_log.txt` | progress lines and all 22 identity-view match lines |
| `controls_recheck.txt` | re-check of the 8 planted controls after the stop |

## Verification

```
python run_l5_backcheck.py prepare   # 7,139 listed / 4,429 unique / 3,721.6 MB / 8 controls, 31.7 s
python run_l5_backcheck.py run       # stopped at 4,443/4,444 jobs, t ≈ 1,100 s; 22 DBBI lines, all identity of the pattern string
```
