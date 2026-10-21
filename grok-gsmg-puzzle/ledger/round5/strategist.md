# 11 — Strategist: post–Round 4 synthesis

**Win:** uncompressed pubkey hash160 `a9553269572a317e39f0f518cb87c1a0ee1dbae4`.  
**Evidence base:** `00-lead.md` … `10-round4.md`, `06-skeptic.md`, handoff §8–9.  
**Hard limits:** offline; no gsmg.io submit; no creator contact.

---

## 1. What null results RULE OUT (high confidence)

Interpretation: “rules out” = **this construction class does not yield structured plaintext or the prize key under the tested KDF**, with planted §4.1 controls firing. Does **not** prove the puzzle has no solution.

| Ruled out | Basis |
|-----------|--------|
| **Literal SalPhaseIon label concat as §4.1 password** (`matrixsumlist`, `enter`, `lastwords…`, `thispassword`, full #8446 string, retracted 81-char recipe) | Tester 34k + cryptanalyst 108 + round2 recipe batch → 0 structured; retracted recipe is **EVP-MD5 Sal-short padding only** (§8.1), not prose. |
| **EVP-MD5 Sal-short with substituted “operands”** (spiral/diag/row/col sums, word-bounded lastwords, sha256-derived EVP password bytes, 3,300+ tries) | Round3–4: only **plain** community literal reproduces 79 B pad; no other template structured. |
| **sha256(answer) as EVP password bytes** (raw32 / hex-as-bytes / md5hex-of-plain) rescuing spiral **bitstring** ops or filler deletion | Round4: 3,300 MD5 + 1.67M §4.1 decrypts → 0. |
| **Filler letter deletion → whole-block decimal → §4.1** at tested depths | Pair: 15,930 null (R3); triple+quad: **1,668,423** §4.1 null (R4). |
| **MASK6 faed deletion** (any subset of `{1,3,551,557,561,563}`) as container password material | `07-deletion-sweep.md`: 576 decrypts, pins lost, 0 structured. |
| **mask6 zeroing as semantic payload** | Interior printable **84/230** ≈ chance (`04-statistician`, `06-skeptic`); pins are **tail-only search artifacts**, not checksums (§8.1). |
| **Bifid plaintext / Beaufort(`btcseed`) / 8 square variants as direct §4.1 answers** | Round2: 720 decrypts null; prefix `btcseed` **not forced** (8/362,880). |
| **Fixed operands without recipe** (#8446 alone, tok23, row/col sums, `lw-arch-tail40`, mask6 latin1/hex/sha256hex, yin-yang XOR blob rearrangements at step3 scale) | Cryptanalyst + Tester + R2 → 0 structured. |
| **Candidate answer string → sha256 → secp256k1 private key** (incl. sha256hex forms) for tested batteries | 0 uncomp hash160 across ledgers. |
| **Stream peel on faed** as a single coherent byte rule | `06-skeptic`: stream vs whole-integer disagree; no completion. |
| **“Padding = progress” on Sal-short MD5** | §8.1 + R3: ~1/256 chance; retracted by solvers; 30/79 printable. |

**Not ruled out by these nulls (explicit):** wrong cipher/KDF on locked blobs (§4.1 unproven for them); **correct** MSL/LW *operations* not yet instantiated; deletion with **structure** (prime-gap, door indices, per-letter rules) vs brute `C(60,k)`; depth ≥5 filler deletion; MD5 on **Terminal/Cosmic**; intermediate binary → key **without** passing through answer-string sha256hex; multi-container **order** where step *n* plaintext feeds step *n+1* password.

---

## 2. What remains PLAUSIBLE (given solved chain 2 → 3.2)

The solved path is **procedure-literal, operand-interpretive** (`02-reader`): concat + sha256hex + AES works for phases 2–3.2 once answer strings are known. Locked stage likely continues **password = f(derived material)**, not brute English.

| Plausible lane | Why still live |
|----------------|----------------|
| **#8446 as ordered program**, not a password | Tokens are [V] decoded; **verbs** (`matrixsumlist`, `lastwords…`) lack on-page operands (§9). Creator #6509 “unforeseen hint” + #39237 **yinyang = next phase** imply staged ops, not one string. |
| **Poster `matrixsumlist`** | §8 [T] exhausted many sum encodings at billion scale, but **SalPhaseIon ab span [91,195)** names the op; “unforeseen” may be **off-white / spiral splice / 14×14 list** not yet tied to one pre-declared encoding. |
| **`lastwordsbeforearchichoice`** | Beaufort Architect block is [V]; char-tail `primebasicsafterwhich…` tested; **per-choice word extraction** (film vs speech, multiple “choice” anchors) not exhaustively pre-registered. |
| **`sha256` hint lines** (`shabef…`) | Phase-1 flower hash [V #225]; “last command” / `theseedisplanted` family tested as **passwords** [§8 T] but not as **hashes of derived binaries** from faed/dbbi. |
| **dbbi + faed as coupled channel** | Walk + URL splice [V]; fillers + Bifid square **reading-dependent** but mechanically reproducible; tail constraints on decimal model [V] — may be **intermediate**, not final key. |
| **Three `Salted__` containers + yinyang** | Sizes (64–79 B terminal/sal-short) fit **key fragment / next password**; XOR/yin-yang layouts partially tried, not as **recipe output → next container input**. |
| **Same §4.1 family** | Headers match solved phases; simplest default until a **single** locked blob falsifies it. |
| **`another door` + primes + zeroing** (#8000) | Round2 coordinate/password batch null; door may be **index rule** into spiral/SalPhaseIon/faed, not literal `{1,4,21}` strings. |
| **New Year dots** | #53342 ASCII [V]; dot-count channel 1..5 **not** in repo batteries as operand. |

---

## 3. Top 3 coordinated hypotheses (pre-registerable)

Each states **inputs, transform, output role, container, detector** before running. No parameter fit from tail pins or padding hits.

### H1 — `#8446 pipeline` (ordered multi-container)

| Field | Pre-registration |
|-------|------------------|
| **Inputs** | `tok23` = 23-cell B/Y spiral segment [V]; `msl` = **one** of: (a) 14 spiral row-sum list joined by `-`, (b) 196-bit spiral as `a/b` bytes hex, (c) Sal [91,195) **as list of 14 row sums of ab-bits** (not scalar sum 56). |
| **lastwords** | For each occurrence of token `CHOICE` in Beaufort Architect plaintext, take **last dictionary word** on the same line; join with `-` (order: speech order). |
| **Chain** | `step0 = tok23`; `step1 = sha256hex(step0 ‖ msl)` → decrypt **SalPhaseIon-short**; if pad-valid, `step2 = sha256hex(plaintext ‖ lw)` → **Terminal**; `step3 = sha256hex(step2 ‖ literal yinyang)` → **Cosmic**. |
| **KDF** | §4.1 sha256hex primary; **Sal-short only** also EVP-MD5 on `step1` string (max 2 KDFs). |
| **Fail** | No step produces structured plaintext; padding rate ≈ chance per step. |

### H2 — `faed → Beaufort → bytes` (Bifid channel as password factory)

| Field | Pre-registration |
|-------|------------------|
| **Square** | Fixed: first-appearance order of **distinct letters in dbbi filler string** (26 letters), not post-hoc `dbifhcega…` from walk hosts. |
| **Bifid** | Period 570 on `faed` ciphertext block [V layout]. |
| **Key** | Beaufort key = `sha256hex(phase1_flower)` **or** literal `btcseed` (2 keys only). |
| **Output** | (i) full Beaufort output as UTF-8 answer; (ii) bytes after `btcseed` prefix; (iii) whole-block decimal of Beaufort output mod 2²⁵⁶ as **raw EVP password** (not sha256hex) — **3 forms × 3 containers**. |
| **Fail** | 0 structured; 0 uncomp hash160 on (i–iii). |

### H3 — `another door` structured deletion on fillers

| Field | Pre-registration |
|-------|------------------|
| **Indices** | From #6884/{#6913}: delete filler letters at positions **{1, 4, 21}** in the 60-char filler string **and** at prime indices **{2,3,5,7,11,13,17,19,23}** in the same string (union, max 12 deletions). |
| **Sibling** | Same index sets applied to **faed** letters at those 1-based positions (if length permits). |
| **Encode** | Surviving string → dbbi re-walk **or** faed whole-block int → **32-byte big-endian tail** → test as (a) §4.1 password `sha256hex(hex(tail))`, (b) direct scalar key. |
| **Containers** | Cosmic + Terminal only (door hint post–SalPhaseIon). |
| **Fail** | 0 structured; 0 key hit; do **not** expand index set without new creator-facing [V] token. |

---

## 4. Five-step research plan (ordered) + stop criteria

| Step | Action | Stop criterion |
|------|--------|----------------|
| **1** | Write `team/preregister_h1_h2_h3.json` (frozen strings, no runtime search knobs). Commit before decrypt script. | — |
| **2** | Implement `team/strategist_battery.py`: run **only** H1–H3 constructions; log pads vs chance; uncomp hash160; `classify()` structured detector. | **STOP branch** if any structured hit or key hit → ledger + minimal repro script. |
| **3** | If H1 null: run H1 **container-order permutation** (3! orders, same ops) — max 6× step-2 decrypts. | Stop if null; do not add new `msl` encodings. |
| **4** | If H2–H3 null: **convention probe** on **Cosmic only** — handoff §8 list: EVP-MD5, double-sha256 hex, raw 32-byte digest as password (≤12 candidates derived from H2 outputs). | Stop if null; if Cosmic opens with non–§4.1, re-run H1 on that KDF only. |
| **5** | If all null: publish **negative result** — locked stage is not reachable by {H1,H2,H3} × {§4.1, Sal-short MD5, cosmic convention probe}; next work needs **new [V] token** (creator message or on-page label), not wider `C(60,k)` deletion. | Stop autonomous expansion; no billion-scale sweeps without new pre-registration. |

**Global stop:** Prize hash160 hit **or** documented falsification of §4.1 on one locked container with structured plaintext **or** completion of steps 1–5 with all stop criteria met.

---

## Executive summary (3 lines)

1. **~1.67M+ new §4.1 decrypts and 3.3k EVP-MD5 tries are null:** literal recipe strings, spiral-bit MSL ops, sha256-as-EVP-password, filler deletion (≤4), MASK6 deletion, and Bifid/Beaufort-as-password do **not** open containers or yield uncomp `a9553269…dbae4`.
2. **Still plausible:** #8446-ordered **operations** (MSL + lastwords + yinyang) feeding **chained** container opens; coupled dbbi/faed/Bifid **byte factories**; structured “another door” indices — not label concatenation or tail-pin narratives.
3. **Next:** pre-register H1 (8446 pipeline), H2 (faed→Beaufort→bytes), H3 (door-index deletion); five-step battery with hard stop on success, KDF falsification on Cosmic, or refusal to expand without new [V] material.
