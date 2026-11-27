# Fresh-eyes candidates · November 27, 2026

**Zero of 45 real decrypts passed strict PKCS#7.** There was no real plaintext to retain or inspect, and no Half or Better Half key hit. A second implementation using the Python cryptography library, an independent SHA-256 key derivation, and its PKCS#7 unpadder reproduced all 45 results.

The 15 supplied strings produced 30 forms when each was emitted verbatim and in lowercase. First-seen, byte-exact deduplication left 15 candidates. Both `privatekey` and `PRIVATEKEY` were tested. The preamble replay folder was absent from the checkout, so this arm has its own directory.

| Envelope | Decrypts | Pad 1 | Expected pad 1 | P(zero pad 1) | Pad ≥2 |
|---|---:|---:|---:|---:|---:|
| Phase 3.2 terminal | 15 | 0 | 0.058594 | 94.2982% | 0 |
| SalPhaseIon short | 15 | 0 | 0.058594 | 94.2982% | 0 |
| Cosmic Duality | 15 | 0 | 0.058594 | 94.2982% | 0 |
| **Total** | **45** | **0** | **0.175781** | **83.8513%** | **0** |

The exact binomial model assumes independent uniform wrong decrypts. A final byte of `01` always gives exactly one byte of valid padding. For N decrypts, the expected count is N/256 and the probability of zero is (255/256)^N. The one-sided excess probability P(X ≥ observed) is 1.000 for every row.

## Seal and controls

The preregistration fixed the candidates, the three ciphertext hashes, the `gsmg` profile, and the planted ciphertext before testing. Its canonical SHA-256 is `93af931f27f1273a98e05d80e721651ce0688780ddfd4c23ea84bec05e43e33c`.

The repository self-test reopened the known Phase 3.2 envelope at pad 10. The same loop used for real candidates recovered the planted 207-byte plaintext with `requiredto` at pad 1. Scanning the saved bytes with `cc.find_keys` detected the planted scalar in all four encodings (raw32, hex64, WIF, and Base64). A second candidate, `takethisprivatekeyyouveearnedit`, also produced pad 1 on the synthetic envelope. Its 207 bytes were retained and scanned, with no key match. Both control plaintext files are under `controls/planted/`. The real scan used only the two puzzle targets.

## Creator messages after #81838

**None.** The analyst export contains 1,886 later records, through #83873 on November 27. All 511 distinct message IDs authored by `user9815232` match the repository's September export plus its November supplement. The additional 18 account-attributed records were Telegram service events (15 member removals, two invitations, and one group join). The last creator message was #81838, sent November 13, 2026 at 3:13:40 p.m. EST in reply to #81836. Its full text was `42`. The analyst export was therefore left out of the repository.

[Sealed plan](PREREG.json) · [Candidate list](candidates.txt) · [Decrypt results](results.json) · [Export comparison](export_comparison.json)

To reproduce the decrypts in a separate directory, run `python replay.py <new-output-directory>` from this folder with PyCryptodome installed.
