# Next best move

Not a private key. One work packet, in order, using only what survived the critical review in `WHAT_THE_GROUP_MISSED.md`.

## Do this next (one packet)

**Treat yinyang as the next unused phase, and Cosmic Duality as the leading candidate for it.**

Why this, not another FAED/96-state consumer:

- Jrk, 2025-04-28 `#39224` (near-unedited): yinyang **has not been reached**; once it is, **hours**, not years.
- The 2023 roadmap string (decoded same week as `#8446`): `yellowblueprimes → matrixsumlist → lastwordsbeforearchichoice → yinyang → …giveaway`. The chat already used earlier tokens as **stage passwords** (`matrixsumlist` for phase 3; `lastwordsbeforearchichoice` reported as an AES-256 password in 2026). **Yinyang is the next named token that Jrk says they have not hit.**
- Cosmic Duality has been mapped to yinyang in-channel since 2023. That mapping is a hypothesis, not proven — but it is a **published blob**, unlike XOR-triangle / 4×21 heatmaps.
- `#69940` already reports hundreds of millions of 96-state / yinyang-bitmask keys checked against `1GSMG`. Repeating that family is negative EV.
- Extra door on piece 1 is still **unhashed** (`#4590`, `#7914`) but **cannot be the whole remaining puzzle**: people were in Salph by March 2021.

## How to run the packet (falsifiable)

1. **Freeze the password list before touching the blob.** Only:
   - SHA-256 of already-solved stage outputs (the same class Jrk used in 2019 `#225`–`#257`).
   - Raw and hashed `yinyang` / `yingyang` / `ying yang` / `YinYang`.
   - Hashes of Cosmic Duality–adjacent published strings already in writeups (no new “operands” from LLMs).
2. **Success:** OpenSSL-style decrypt of the Cosmic Duality AES yields readable text **or** a 32-byte candidate that matches the known `1GSMG` public key.
3. **Fail / close:** that list is exhausted. Write the SHA-256 of the list itself into the board. Do **not** grow the list with FAED slices, `0x7B9ECC`, URL LSBs, or `{1,4,21}`.
4. **Time box:** if it does not behave like Jrk’s “same day / two hours” after a *successful* decrypt, it was not yinyang. Park it.

## 20% side packet (do not let it eat the main one)

**Piece 1 extra door, using only contemporaneous text:** `#1710` as quoted in 2020 `#3388` (yellow/blue numbers, rabbit nest, more than one door, hush/hash). Unedited `#4590` / `#7914` say a door was unfound / still named. Require an in-channel SHA-256 of any claimed find. **Do not use `{1},{4},{21}`** (April Fools + `#7529` + 2025 edit).

## First hour (required, not optional)

Write a one-page **unedited-hint sheet**: message id, date, `(edited …)` or not, and only lines that have a same-day quote. Anything edited in 2025–2026 (`#8000` primes/zeroing, `#6884`, `#8330`) is marked `unsafe canon`. Without this, the next month repeats 2024–26 hint drift.

## Explicitly not the next move

- Another FAED / 96-state “consumer” or frequency dashboard.
- Treating leftover 3.2 AES vs Salph vs Cosmic Duality as one blob.
- Waiting for Jrk, or treating 2026 wording of old posts as 2020 law.
- DMs / “I found it but won’t share.”

## If the Cosmic Duality list fails

Then the remaining high-EV fork is: **leftover 3.2 AES with `reinserting prime basics` as an operation on already-known primes (yellow/blue from piece 1), not a new cipher family.** Still one closed list, still an oracle (readable decrypt or `1GSMG` match). Do not run both forks as an open-ended chat.

Board rule from `GROUP_COMMS_ANALYSIS.md`: KPI is hypotheses **closed**, not messages sent.

---

## Outcome of packet 1 (2026-09-08)

Ran as `packet/`. **Yinyang-as-password did not decrypt Cosmic Duality or leftover 3.2.** The published 7-XOR decrypt of Cosmic Duality was reproduced (`4f7a1e4e…`) and is **not** the `1GSMG` key. Full log: `packet/RESULTS.md`.

## Packet 2 (do this next)

**Leftover phase-3.2 AES** (`artifacts/phase32_leftover.b64`) with a **new** closed list: mechanical encodings of yellow **50400** and blue **96791** from `packet/out/extra_door_pixels.json`.

Those numbers were never in packet 1. The leftover blob already failed the 55 yinyang/roadmap passwords. Do not retry that list. Do not grow this list with a second color heuristic (in-channel `blue 83700` is a different bucket, not frozen here), red counts, FAED slices, or `{1,4,21}`.

Caveat: **neither 50400 nor 96791 is prime.** This packet tests “yellow/blue numbers as OpenSSL password,” not a proof that they are “prime basics.”

```bash
python3 packet/run_packet.py \
  --spec password_list_leftover32.json \
  --results-name results_leftover32.json
```

Success: readable leftover-3.2 plaintext **or** a 32-byte candidate matching the `1GSMG` pubkey.  
Fail / close: write the list hash on the board; do not add strings.

If packet 2 is also negative, stop inventing AES passwords. The remaining unhashed object is the extra door (`#4590`, `#7914`) as a **find with an in-channel SHA-256**, not another ciphertext consumer.

---

## Outcome of packet 2 (2026-09-08)

Ran leftover 3.2 against the frozen 50400/96791 encodings (**40** OpenSSL attempts, list SHA-256 `c558330f…5e71`). **No decrypt. No prize-pubkey hit.** Full log: `packet/RESULTS_LEFTOVER32.md`.

That closes both AES forks named in this note. Do not add a third password list.

## Packet 3 (extra door as a hashed find)

Not AES. Piece 1 only. Contemporaneous text: `#1710` / `#3388`, `#4590`, `#7914`. **No `{1,4,21}`.**

```bash
python3 packet/extra_door_pixels.py
python3 packet/extra_door_find.py
```

Success: a second `gsmg.io/…` path, or a candidate whose SHA-256 is claimed as the find.  
Fail / close: the frozen encodings of the 14×14 grid are exhausted; write the hashes on the board; do not grow the encoding list.

---

## Outcome of packet 3 (2026-09-08)

Main door reproduced (`gsmg.io/theseedisplanted`). **No second URL.** Yellow/blue occupy exactly the 24 byte-LSB spiral slots; extra channel `f73d92` / `08c26d` is hashed and **not** claimed as a door opening. Exact palette blue is **83700** (HSV 96791 was a miscount). Full log: `packet/RESULTS_EXTRA_DOOR.md`.

**Superseded in part by `AUDIT.md`.** `f73d92` turned out to be the URL's own ASCII low bits — zero new information — and so are the pixel counts (9 and 15 cells). The one non-redundant datum in piece 1 is the FEFEFE cell at spiral **164** = byte group **21**, offset **4**, which an earlier HSV classifier had erased. Tested as a password across 4 KDFs and 3 blobs: no decrypt (`packet/RESULTS_YBPOS.md`). It survives as a positional result, which no packet's success criterion could ever have detected.

## Audit of packets 1–4

`AUDIT.md`. Three defects: a classifier that collapsed `(254,254,254)` into white, packet 2 freezing the wrong blue (96791 instead of the in-channel 83700), and four packets assuming OpenSSL's MD5 KDF without validating it. Corrective sweep `packet/run_kdf_audit.py` re-ran all 199 frozen passwords under `evp_md5` / `evp_sha1` / `evp_sha256` / `pbkdf2_sha256_10000` against all three blobs — 4776 attempts, harness self-tested against the published Cosmic Duality decrypt, **0 readable plaintexts, 0 prize hits**.

The extra door remains unopened. Leftover 3.2 remains encrypted. Yinyang remains unreached.

## Packet 4 (matrixsumlist → enter)

Treat `matrixsumlist` as **sum the a–i matrix, list the remainders, enter that list**. Leftover 3.2 only. Tiny add-on: Jrk-named Neo passport date forms and the two Architect door sentences with punctuation. **Do not retry 7-interleave.**

```bash
python3 packet/matrixsumlist.py
python3 packet/run_packet.py \
  --spec password_list_synthesis.json \
  --results-name results_synthesis.json
```

Reading: `SYNTHESIS.md`.

---

## Outcome of packet 4 (2026-09-08)

20 sum records, 94 unique enter-passwords, **188** leftover-3.2 attempts, list SHA-256 `60f29326…2baf`. **No decrypt. No URL. Sum letters are not English.** Passport dates and punctuated two-door lines included. Full log: `packet/RESULTS_SYNTHESIS.md`.

140 is consumed as a length on the spiral (drop `gsmg.io` → `/theseedisplanted` + 4 zero bits) and closed as an AES password. Extra door on piece 1 is closed as a grid encoding (`packet/RESULTS_FEFEFE_READ.md`). Yinyang still unreached. Do not resume 7-interleave.

## External threads (reddit + bitcointalk)

Pulled from `main`: `reddit1.txt`, `reddit2.txt`, `bitcointalk-5151725-page-000.md`. Review: `EXTERNAL_THREADS.md`. No new leftover-3.2 decrypt, no prize-pubkey hit. The only 2019 fact worth keeping is Telegram-JPEG vs website-PNG (PNG intended for “hidden things”). 2025 “hidden QR key” / `N82BIV` claims are unhashed and failed the closed checks.

