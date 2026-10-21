# Stage-3 string as leftover-3.2 key (2026-09-08)

Closed list: `packet/password_list_stage3.json` (29 strings × raw + sha256hex × 4 KDFs × 3 blobs = **696** attempts). Harness self-tested against the published Cosmic Duality 7-XOR decrypt. No `dbbi`, no `faed`.

Machine log: `packet/out/results_stage3.json`.

## What the request got right

The leftover blob it named (`U2FsdGVkX1+0Wl49gnWTyiimluu7V3…`) **is** `artifacts/phase32_leftover.b64` — the last unpublished AES in the README, after Beaufort 3.2.1 and VIC 3.2.2. It has never opened.

S = 32 (Klingon `cha' + vagh×jav`) is the one mapping the puzzle text actually computes. Q = 82 (digits above I and W on QWERTY) is a fair reading of “the I and W are below.”

## What it got wrong

**This is Phase 2 plaintext, not Phase 3.** It sits in the `causality` decrypt, and the published writeup already spent it: Mr Robot / Thales → **Safenet Luna HSM**, which is parts 2–4 of the 7-part concat whose SHA-256 (`1a57c572…`) opened `phase3.txt`. The coordinates `51°52'28.0"N 4°24'23.2"E` are Seattleweg 5, Rotterdam — an old Thales/Safenet office — and were identified in-channel in 2025 as solved for years (`2025.txt` #42611). Decentraland parcels from the same pairs were mapped again on 2026-09-07 (`2026.txt` #71176). Treating them as an unused parameter matrix ignores that they already bought the HSM name that opened Phase 3.

**B → 25 and H → 42 drop operators the puzzle wrote.**  
H is `(Answer to only this puzzle but nothing else) * -1` → **−42**, not 42.  
B is `((BV80605001911AP)-(sqrt(-1)))^2` → `(5i − i)² = (4i)² = `**−16**, not 25. 25 is “treat i5 as the integer 5, then square,” which deletes the imaginary unit the formula puts in.

**“your sum is” is not in the blobs.** The Architect line is `YOUR LIFE IS THE SUM OF A REMAINDER OF AN UNBALANCED EQUATION`. `in case you` is the already-decoded VIC sentence.

**Worst-gear reversal as unused geography.** Reverse gear is a fair reading of the highway line. The reversed tuple is not a new door: it is how the community already got Rotterdam / DCL parcels, which fed the HSM password.

## AES result

**The numbers do not decrypt leftover 3.2.** 7 PKCS#7 successes in 696 attempts, all `pad=0x01` at blob-max length (79 or 1327), chance-rate, zero readable, zero `1GSMG` hits.

Tried, all closed: `32,42,82,25` and reverse `25,82,42,32`; published signed `32,-42,82,-16`; concatenations and sum 181; DMS and decimal forms of 51°52'28.0"N 4°24'23.2"E; the pair encodings `(32,82)`, `(-42,-16)`, `(4,15)`, `(2,0)`; the raw Stage-3 string; `matrixsumlist32,42,82,25`. Each as OpenSSL password and as SHA-256 hex, under `evp_md5` / `evp_sha1` / `evp_sha256` / `pbkdf2_sha256_10000`.

## After this packet

Do not resume `dbbi`/`faed` frequency work on the back of this. Do not grow another Stage-3 AES list. The Stage-3 string is consumed architecture (HSM name → Phase 3), not an unused key for leftover 3.2. Leftover 3.2 remains unopened with no remaining closed operand from this string.
