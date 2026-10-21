# 10 — Round 4: MD5+sha256 EVP, spiral bitstring MSL, triple/quad filler deletion

**Code:** `team/round4_battery.py` → `artifacts/round4_battery.json`  
**§4.1 control:** phase-2 `causality` **OK**

## 1. EVP-MD5 with sha256-derived password bytes

For each candidate string, SalPhaseIon-short decrypt attempted with EVP password bytes:

| variant | password bytes |
|---------|----------------|
| `plain` | UTF-8 answer |
| `sha256hex-ascii` | 64-char lowercase hex of SHA-256(answer) |
| `sha256-raw32` | 32-byte SHA-256(answer) digest |
| `md5hex-of-plain` | MD5(answer) as hex ASCII |

Applied to spiral MSL operands, recipe templates, and community-string substitutions.

**3,300** MD5 decrypts → **0** structured (community literal still **79 B** pad with **plain** only).

## 2. matrixsumlist on spiral **bitstring** (not sum)

| operation | description |
|-----------|-------------|
| `spiral-ab-bytes-hex` / `latin1` | 196 spiral bits → a/b → 8-bit bytes |
| `spiral-bits-literal` / `rev` | 196-bit string and reverse |
| `spiral-url192` | URL bits without tail 0000 |
| `spiral-list-rowsums` | 14×14 spiral walk grouped in 14s; **concatenate row sums** |
| `spiral-list-rowsums-sep` | same with `-` separators |
| `spiral-int` / `int-rev` | binary integer decimal |
| `+tok23` | prepend/append tok23 to each |

Each operand × MD5 variants × recipe chains; each also × §4.1 (`plain` + `sha256hex`).

## 3. Filler deletion

| depth | combinations | §4.1 decrypts | structured |
|-------|-------------:|--------------:|------------|
| **3** letters removed | 34,220 | 205,320 (latin1 + sha256hex × 3 containers) | 0 |
| **4** letters removed | 487,635 | 1,462,905 (sha256hex only × 3 containers) | 0 |

**Total §4.1:** 1,668,423 decrypts. **MD5:** 3,300. **0** prize keys, **0** structured plaintext.

## Result

**Null.** sha256-as-EVP-password does not turn spiral string ops or filler triple/quad deletions into container opens or keys.

**Open:** quintuple+ deletion; spiral MSL as **list of sums** fed to custom concat (not string password); MD5 double-sha256 hex; Terminal/Cosmic with same MD5 variants.
