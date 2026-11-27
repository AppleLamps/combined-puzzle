# 22 - Six SalPhaseIon answers hashed into Cosmic Duality

**Status (2026-11-27): nothing opened.** 32 decrypts, no valid PKCS#7 padding, no legible plaintext. A follow-up checked the row labels and tried the Half public key. No padding hit, and no printable ratio above 0.42.

The family is the one the creator's group named: all of the SalPhaseIon answers, hashed, as the Cosmic Duality passphrase. The six answers, in page order, are `matrixsumlist`, `lastwordsbeforearchichoice`, `thispassword`, `shabefourfirsthintisyourlastcommand`, `enter`, `shabefanstoo`. They are joined with nothing or with `z`, and the string is hashed either alone or with `yinyang` appended. The primary passphrase is the lowercase hex of that SHA-256, which is the phase 3.2 convention. The same grid is also tried as the raw 32-byte digest. Both EVP_BytesToKey digests are MD5 and SHA-256, one iteration, AES-256-CBC, salt from the Cosmic `Salted__` blob.

Two backstops sit on the same separators and the same yin choice: the hex passphrase in uppercase, and SHA-256 of the first digest, again as lowercase hex.

Every raw decrypt is binary. Printable-ASCII ratios run from 0.3449 to 0.3968, around the 0.371 expected from random bytes. No cell is an English or Dutch sentence.

Rows 07, 15, 23 and 31 are SHA-256 of the first SHA-256, written as lowercase hex, then EVP-MD5. The `md=md5` label is the KDF digest. Those rows did not hash MD5 twice, so the MD5-then-SHA256 cells were not added. The Half uncompressed public key, as raw bytes and as lowercase hex, then went through the same four password forms and both KDF digests: 16 decrypts, none marked.

Detail, including the first 200 bytes of the original 32 decrypts: [runs/2026-11-27_cosmic_six_hash/REPORT.md](runs/2026-11-27_cosmic_six_hash/REPORT.md). Follow-up: [runs/2026-11-27_cosmic_six_hash/followup.txt](runs/2026-11-27_cosmic_six_hash/followup.txt).
