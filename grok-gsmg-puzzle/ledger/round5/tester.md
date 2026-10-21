# 11 — Round 5 battery plan (Tester, design only)

**Status:** Pre-registered **offline** plan — **do not execute** full `C(60,5)` (~5.46M) or million-scale sweeps in this round.  
**Prior null:** Round 3 (`ledger/09-round3.md`) and Round 4 (`ledger/10-round4.md`) batteries completed **null**; controls valid.  
**Planned code:** `team/round5_battery.py` → `artifacts/round5_battery.json` (not run for this ledger entry).

## Pre-registered detector

Same as Rounds 3–4 and `ledger/05-tester.md`:

- **Function:** `classify()` from `src/step1_btcseed.py`
- **Structured iff:** `Salted__` / JSON / PEM magic, hex-key-shaped plaintext, or **high printable prose** (≥90% printable, ≥50% letters, length ≥16)
- **Explicitly not a hit:** valid PKCS#7 pad alone; phase-3.2-scale printable noise (~59% printable)

**Win side-channel (logged, not “structured”):** `crypto_known.is_win_uncompressed` on SHA-256(answer) and on 32-byte filler/peel digests where applicable.

## Planted controls per KDF (must pass before puzzle decrypts count)

| KDF / password form | Control action | Pass criterion |
|-------------------|----------------|----------------|
| **§4.1 sha256-hex** | `planted_control()` in `team/cryptanalyst_tests.py` | Phase-2 blob decrypts with answer `causality`; plaintext == `artifacts/phase2.txt` |
| **EVP-MD5 plain** | Decrypt `salphaseion_short.bin` with UTF-8 community recipe | Body length **79**, body SHA-256 `1449a2178eea7c0e3fabac8c1ad2afa294be4fc1800c594a025a056e88c626bf` (handoff §8.1) |
| **EVP-MD5 sha256hex-ascii** | In-run: encrypt 48 B plaintext `ROUND5_MD5_PLANTED_PLAINTEXT` to a temp `Salted__` blob with EVP-MD5 password bytes = **lowercase hex** of SHA-256(`round5-md5-planted-v1`); decrypt same | Round-trip plaintext match |
| **EVP-MD5 raw32** | Same with password bytes = **32-byte** SHA-256(`round5-md5-planted-v2`) | Round-trip plaintext match |

If any control fails, **abort** and do not record a null on puzzle material.

## Container scope

| Stream | Blobs | KDF |
|--------|-------|-----|
| **§4.1 std-hex** | `terminal`, `salphaseion_short`, `cosmic` (`cryptanalyst_tests.CONTAINERS`) | Password passed to EVP = **lowercase hex** of SHA-256(**answer string**); EVP SHA-256, 1 iter, AES-256-CBC |
| **EVP-MD5** | **Same three** (`terminal.bin`, `salphaseion_short.bin`, `cosmic.bin`) — extends R3–4 (Sal-short-only MD5) to **Cosmic + Terminal** | `evp_bytes_to_key` with **MD5**; password bytes per variant table below |

Yin-yang / XOR rearrangements from `load_containers()` are **out of scope** for Round 5 (keep decrypt budget bounded; unchanged from R3–4 three-container convention).

### EVP-MD5 password byte variants (per answer string `A`)

| variant | password bytes |
|---------|----------------|
| `plain` | UTF-8(`A`) |
| `sha256hex-ascii` | UTF-8 lowercase hex of SHA-256(`A`) |
| `sha256-raw32` | 32-byte SHA-256(`A`) digest |
| `md5hex-of-plain` | UTF-8 hex of MD5(`A`) |
| `sha256hex2-ascii` *(open item from R4)* | UTF-8 hex of SHA-256( UTF-8 hex of SHA-256(`A`) ) |

## Hypothesis table

| ID | Hypothesis | Candidate construction (exact) | §4.1 answers | EVP-MD5 targets | Expected if false |
|----|------------|--------------------------------|--------------|-----------------|-------------------|
| **H1** | Spiral **matrixsumlist** is a **list→concat recipe**, not a raw row-sum digit string | Along spiral walk: 14 groups × 14 cells → list `S = [s₁…s₁₄]`. **Ban** standalone password `''.join(str(x) for x in S)` (R4 null). **Allow** only template outputs: `enter`/`-`/`,`/bracket joins of `S` inside `matrixsumlist…enter…thispassword…`, `tok23` brackets, per-element `matrixsumlist{sᵢ}enter…`, `yellowblueprimes{join}enter{lw}yinyang`. `lw` = `word_lastwords_candidates()` (Architect before `SELECT`, film tokens, tails k∈{2,4,6,8,10,12,20,40}, `primebasicsafterwhich…`). | Each template string **plain + sha256hex** × 3 containers | Same **169** strings (incl. community) × 5 byte variants × **3** containers | 0 structured; MD5 community may still show 79 B pad on Sal-short only |
| **H2** | **Phase 3.2 Architect bytes after `SELECT`** are the password (or feed recipes), not char windows before `SELECT` | From `phase32_beaufort.txt`: `after = text[SELECT+6:]` (390 chars). Answers: full lower/upper, prefixes 16/32/64/128/256, **latin-1 bytes** of `after`, **hex** of those bytes, plus `matrixsumlist{frag}enterlastwords…` for `frag` ∈ {first 64, first 128, spiral `enter`-join}. **Not** in this batch: entire 1143-char prefix (`lw-arch-all` already null in R2). | plain + sha256hex × 3 | Included in H1 MD5 set | 0 structured |
| **H3** | **Quintuple** letter deletion on `yellowblue_fillers.txt` (60 letters) → integer bytes → §4.1 | Delete 5 distinct indices, map `a→1…z→26`, concat digits → `int` → minimal big-endian bytes → answer = **sha256hex** of bytes only (R4 quad convention). **Sample:** `4096` combinations via stride through lexicographic `C(60,5)` (seed index 0, step `⌊5461512/4096⌋`); **documented bound** for full sweep: **5,461,512** combos. | 4096 × 3 = **12,288** decrypts | — (§4.1 only) | 0 structured; pad count ≈ 48 (12,288/256) |
| **H4** | **Cosmic + Terminal** use the same Sal-short **EVP-MD5** community KDF as §8.1 | For all H1/H2 strings plus `matrixsumlistenterlastwordsbeforearchichoicethispasswordmatrixsumlist`, run MD5 variants on **terminal** and **cosmic** (not only Sal-short). | — | **169** × 5 × 3 = **2,535** decrypts | 0 structured prose on Terminal/Cosmic; Sal-short may retain 79 B community pad under `plain` only |

## Candidate counts (unique answer strings)

| family | unique strings | notes |
|--------|---------------:|-------|
| Spiral list→concat recipes (H1) | **158** | Raw `spiral-list-rowsums` digit string excluded |
| Phase32 after `SELECT` (H2) | **11** | Overlap 1 with H1 → **168** union for §4.1 |
| MD5 superset | **169** | Adds community recipe literal |
| Quintuple filler sample (H3) | **4096** | sha256hex answers only |
| Quintuple **full bound** (not run) | **5,461,512** | Documented ceiling |

## Decrypt estimate (executed plan = sample quint)

| batch | formula | decrypts |
|-------|---------|----------|
| §4.1 curated (H1+H2) | 168 × 2 forms × 3 containers | **1,008** |
| §4.1 quintuple sample (H3) | 4096 × 3 containers | **12,288** |
| EVP-MD5 (H4) | 169 × 5 variants × 3 containers | **2,535** |
| KDF planted checks | 4 controls (not puzzle containers) | **4** |
| **Total puzzle decrypts** | | **15,831** |

**Total including controls:** **15,835**.

### Alternate bound (full quintuple, not authorized this round)

| batch | decrypts |
|-------|----------|
| §4.1 full `C(60,5)` sha256hex only | 5,461,512 × 3 = **16,384,536** |
| + curated + MD5 as above | **16,388,079** puzzle decrypts |

## Implementation sketch (`team/round5_battery.py`)

1. Run four KDF planted controls (table above).  
2. Build `spiral_list_recipe_candidates()` — templates only, no raw row-sum string.  
3. Build `phase32_after_select_candidates()` — latin-1 / hex / truncated / recipe wraps.  
4. `try_password()` for §4.1 (plain + sha256hex) on three containers.  
5. `try_mdp5_containers(answer, label)` — five byte variants × `{terminal, salphaseion_short, cosmic}`.  
6. Quintuple: `itertools.combinations(range(60),5)` strided sample → `filler_bytes` → sha256hex → `try_password` only.  
7. Emit JSON: counts, control flags, `structured_hits`, pad histogram, `md5_community_by_container`.

## Result (pre-registered)

**Expected:** **Null** on puzzle material if R3–R4 conclusions hold; **controls must fire** (§4.1 causality, MD5 community 79 B on Sal-short, two in-run MD5 planted round-trips). Any structured hit on `terminal` or `cosmic` under EVP-MD5 would be **novel** relative to R3–R4.

## Relation to team rounds 3–4

| Round | Gap closed in R5 plan |
|-------|------------------------|
| R3 | MD5 was Sal-short only → **H4** adds Terminal + Cosmic |
| R4 | Spiral row-sum **as raw password** → **H1** forbids; recipes only |
| R4 | Quad filler exhausted at sha256hex → **H3** quintuple **sample** (+ documented full bound) |
| R2 | `lw-arch-all` before SELECT null → **H2** pivots to **after SELECT** bytes |
