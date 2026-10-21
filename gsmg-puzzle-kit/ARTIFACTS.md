# Artifact integrity

Interpretation updated 6 October 2026: see [doc 119](claude/119-current-evidence-ledger.md). The tables preserve the original artifact identities; provenance strength, mandatory use and lock order are separate questions.

Current as of 29 September 2026. Every hash, size and salt below was recomputed on that date from the project's own files: the container hashes from the base64 decoded bytes of the `.b64` files, and the plaintext hashes by decrypting the containers with the passwords derived in the dossier (sections 3.2 to 3.4). To repeat the check, base64-decode a `.b64` file and run `sha256sum` on the result.

## Containers

Each is an OpenSSL `Salted__` container: 8 magic bytes, an 8-byte salt, then ciphertext. AES-256-CBC is established for the three opened stages; it is a hypothesis for the three locked blobs. The header and block-compatible sizes do not identify their cipher. Sizes here are the decoded file size, so the ciphertext alone is 16 bytes shorter (the two short containers hold 80 bytes of ciphertext, Cosmic Duality 1,328). Some log docs use the ciphertext-only figures.

| container | file | decoded bytes | salt | sha256 |
|---|---|---:|---|---|
| Phase 2 (solved) | `phase2.b64` | 672 | `06286612d43ed7ed` | `a089144531c666e59770c799427c05d1ea4ae074857b97d61b8d3924ff14c7e7` |
| Phase 3 (solved) | `phase3.b64` | 4112 | `9fbc451d13d071f4` | `9163a38d8c49038d01005bc468d9c677183b49b14d7a88fdf3bade75d1443f30` |
| Phase 3.2 (solved) | `phase3.2.b64` | 2448 | `eefc4c5befc1656a` | `9d172dc017034564b40eb381fa61e31421f509a08430864c77ccf86cfc8fe784` |
| Terminal (locked) | `terminal.b64` | 96 | `b45a5e3d827593ca` | `291dfd6f3e759ec2e272b35a00c24907da70c3e7a9291b4c13605c7b0b4f3de9` |
| SalPhaseIon short (locked) | `salphaseion-short.b64` | 96 | `3ab585348552415d` | `9e2831e1b34b5f34796df47ccaf6530d48d371c61a6bff84d60db1064fa7a258` |
| Cosmic Duality (locked) | `cosmic-duality.b64` | 1344 | `2d3f6fe06dc950e6` | `b18950551a4dd0cb8a9378f0906ba18c03a15f0ee83eb98c6bc90165c5f79805` |

The phase 3.2 container is the tail of the phase 3 plaintext. The Terminal container is the tail of the phase 3.2 plaintext. The two short containers are two independent encryptions, not one stream cut in half.

## Plaintexts of the solved containers

| plaintext | bytes | sha256 |
|---|---:|---|
| Phase 2 | 648 | `e2f9dd65604a3231f8b3301724e8d713a88fffc4b6c7c4aeeb20f58a582b593a` |
| Phase 3 | 4090 | `c4ad94559a44a927c1032cc0e024515f9510a0806a2d14458dbf4a360af9865f` |
| Phase 3.2 | 2422 | `b82afeb86f9e50848220f9b64b744b821400308aea273a1c949b9d2d0e408a34` |

## Images

| file | size | sha256 |
|---|---|---|
| `puzzle.png` (the poster) | 1048 x 1556 px, 29,931 bytes | `38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830` |
| `follow_the_white_rabbit.png` | 350 x 350 px, 1,958 bytes | `5e8d84b88f8f829428df5d2a8bf36c7268346f169b799ac7570b6223990d204f` |

The rabbit image is a 3x reduction of the poster's 14x14 grid (dossier section 4.5). The eight rebus tiles are described in dossier section 5.

## Stream files

| file | object | length |
|---|---|---|
| `salphaseion-textarea.txt` | the SalPhaseIon textarea, verbatim | 1,075 characters |
| `dbbi.txt` | the dbbi segment | 91 symbols |
| `faed.txt` | the faed segment | 570 symbols |
| `architect_letters_1539.txt` | the phase 3.2.1 output | 1,539 letters |
| `checkerboard_vic_91.txt` | the checkerboard plaintext, then the 149 digits that encode it | 91 letters, 149 digits |
| `payload-gsmgjh.txt` | GSMGJH payload (hex) | 64 bytes |
| `payload-gsmgbh.txt` | GSMGBH payload (hex) | 65 bytes |

Two notes on these files. First, `architect_letters_1539.txt` is stored in uppercase, while the decode (cp273, then reciprocal Beaufort with key `THEMATRIXHASYOU`) emits lowercase. Case is presentation and the letters are the same. Second, the checkerboard result has no word breaks, because the board's `/` separator cell is never used; any spaces shown elsewhere are reading aids.

The three page files (`theseedisplanted.html`, `phase2_choice.html`, `salphaseion_phase3.html`) carry the artifacts above in their original markup, and `README.md` lists what each one is.
