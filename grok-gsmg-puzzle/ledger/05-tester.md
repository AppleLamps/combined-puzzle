# Tester ledger — §4.1 convention battery (17 Oct 2026)

| Field | Value |
|-------|-------|
| **hypothesis** | The three locked containers (plus yin-yang / XOR rearrangements from `load_containers()`) open under handoff **§4.1** (password = lowercase hex SHA-256 of answer string; EVP_BytesToKey SHA-256, 1 iter; AES-256-CBC) when the answer is drawn from: Logic-line candidate `afterwhichyouwillberequiredto`, phase-1 flower (+ hashes), decoded **#8446** recipe text, §8.1 `matrixsumlist…` recipe, tok23×matrix row/col×last-words combinatorics (step3-style), or mask6 integer bytes (latin-1 / hex / sha256hex). |
| **code** | One offline run: `crypto_known.encrypt_salted` / `decrypt_salted` (§4.1); `step1_btcseed.load_containers`, `classify`; `step3_mask.FLOWER`, `tok23()`, `matrix_strings()` for the combinatorial battery. Report: `artifacts/tester_battery_report.json`. |
| **convention** | §4.1 std hex only (not EVP-MD5, double-hash, or raw-digest variants in this run). |
| **containers tried** | 9 blobs with `Salted__` header: `terminal`, `salphaseion_short`, `cosmic`, `sal_yinyang_blocks`, `sal_yinyang_ct_bytes`, `xor_ct_salt_terminal`, `xor_ct_salt_salphaseion`, `term_sal_block_ab`, `term_sal_block_ba`. (`sal_yinyang_b64_chars` not present in `load_containers()`.) |
| **candidates** | **3852** unique answer strings (includes plain / sha256hex / sha256hex2 forms of tok23×{row,col,255,161}×{flower, sha256(flower), sha256²(flower), thispassword}×separators × tails, plus fixed strings below). |
| **decrypts** | **34669** (= 3852×9 + 1 planted-control decrypt). |
| **valid pads vs expected** | **123** valid PKCS#7 pads vs **~135.4** expected at chance (1/256); **122** are 1-byte pads, **1** longer pad; **122** pad-only near-misses (no structured detector). |
| **planted control** | **Fired.** Answer `tester-planted-control-v1`; ciphertext encrypted in-run with §4.1; round-trip plaintext `PLANTED_CONTROL_PLAINTEXT_FOR_TESTER_BATTERY_RUN` (48 B). |
| **detector** | `classify()` from `step1_btcseed`: structured iff `Salted__` / JSON / PEM magic, hex-key shape, or **high printable prose** (≥90% printable, ≥50% letters, len≥16) — **not** printable-ASCII alone. |
| **structured hits (puzzle containers)** | **0** |
| **structured hits (control only)** | 1 — planted blob only (`structured:prose 1.00`). |
| **win test** | SHA-256 digest of each candidate string (and of each candidate’s sha256hex form) tested as secp256k1 private key; **compressed and uncompressed** hash160 vs prize `a9553269…dbae4`: **0** matches. |
| **result** | **Null** on puzzle material with **control valid** — padding rate consistent with chance; no prose/Salted__ plaintext on real containers. |

## Fixed candidate strings (representative)

| label | answer (preview) |
|-------|------------------|
| `afterwhich_literal` | `afterwhichyouwillberequiredto` |
| `phase1_flower` | `theflowerblossomsthroughwhatseemstobeaconcretesurface` |
| `phase1_sha256hex_flower` | `5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75` |
| `msg8446_full` | `yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyangwewontgiveawaythepassworditsinfrontofyoureyesbutyourenotseeingitverylaststepisatruegiveawaypromised` (161 chars) |
| `recipe_81_sec81` | `matrixsumlistenterlastwordsbeforearchichoicethispasswordmatrixsumlist` |
| `mask6_sha256hex` | `a6bd84cee5d27234602aec8bcaf4c9c204144afc89797586cd8e2d2b1aae3242` |
| tok23 | `2222252222525222225222525222525` |
| msl row / col | `610876654997879` / `8108108736759668` |

## Notes

- §8.1 documents the solver recipe string with **EVP-MD5** on SalPhaseIon-short (1-byte pad, non-text). This battery used **§4.1 SHA-256** only; that recipe produced **no** valid pad here (expected divergence).
- Combinatorial tok23×matrix×last-words grid matches the prior `#8446` + poster-totals scale (~9k decrypts on three containers only); this run adds yin-yang/XOR variants and mask6/masked-faed passwords for **~3.5×** more decrypts.
