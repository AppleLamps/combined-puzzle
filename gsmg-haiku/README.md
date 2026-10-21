# GSMG.io 5 BTC puzzle

Unmarked values in this folder were recomputed from the files in `files/` on 2026-10-06.
Values marked **[kit]** are copied from the source kit's records and were not recomputed here.

## Target

Find the private key of this address.

| item | value |
|---|---|
| address | `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` |
| address form | P2PKH of the uncompressed public key |
| hash160 | `a9553269572a317e39f0f518cb87c1a0ee1dbae4` |
| public key, uncompressed | `04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a4649c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559` |
| public key, compressed | `03f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464` |

## On-chain history of the target [kit]

| date | block | event |
|---|---:|---|
| 2019-04-13 | 571,497 | address funded with 5 BTC |
| 2020-05-11 | 630,001 | 2.5 BTC sent to `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` |
| 2024-04-24 | 840,725 | 1.25 BTC sent to `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` |
| 2026-09-29 | | balance 1.25636967 BTC (mempool.space) |

## Status

| stage | state |
|---|---|
| Poster | decoded |
| Phase 1 | answered |
| Phase 2 | decrypted |
| Phase 3 | decrypted |
| Phase 3.2 | decrypted |
| Terminal container | not decrypted |
| SalPhaseIon short container | not decrypted |
| Cosmic Duality container | not decrypted |

Where things stand overall, with what has been tried and what is open: [STATUS.md](STATUS.md).
The steps are in `STEPS.md`. The review corrections and offline validation are in [REVIEW_CORRECTIONS.md](review_leads/REVIEW_CORRECTIONS.md).

## Latest cryptanalysis: 2026-10-15 UTC

[Reproducible investigation and complete results](review_leads/cryptanalysis_2026_10_15/README.md). No new complete instruction, container unlock, or matching prize key was recovered.

The new analysis reconstructs the DBBI/HILL/Bifid route, retains both 83/84-cell parses, and explains both alternating streams as coordinate projections. The reversible 512-bit row extraction includes eight `BTCSEED` header bits; the subsequent payload is 504 bits (63 bytes). Specific Hill interpretations fail exact algebraic tests. The documented 64-byte and 63-byte seed/key derivations produced 37,952 public-point comparisons without a prize match. These are bounded results, not a claim that arbitrary derivations are exhausted.

The folder includes source snapshots and hashes, forward encoders, planted controls, exact outputs, retained padding-only plaintexts, the scoring table, and executable audit scripts. See the report for every assumption and exclusion.

## Encryption used by the decrypted stages

| item | value |
|---|---|
| container | base64 of `Salted__` + 8-byte salt + ciphertext |
| password | `sha256(answer)` as 64 lowercase hex characters |
| key derivation | OpenSSL `EVP_BytesToKey`, SHA-256, 1 iteration |
| cipher | AES-256-CBC, PKCS#7 padding |

```
openssl enc -d -aes-256-cbc -a -A -md sha256 -pass pass:<sha256 hex of answer> -in <file>.b64
```

## Containers

Sizes and hashes are of the base64-decoded bytes. All six begin with `Salted__`.

| container | file | bytes | salt | sha256 |
|---|---|---:|---|---|
| Phase 2 | `files/phase2.b64` | 672 | `06286612d43ed7ed` | `a089144531c666e59770c799427c05d1ea4ae074857b97d61b8d3924ff14c7e7` |
| Phase 3 | `files/phase3.b64` | 4112 | `9fbc451d13d071f4` | `9163a38d8c49038d01005bc468d9c677183b49b14d7a88fdf3bade75d1443f30` |
| Phase 3.2 | `files/phase3.2.b64` | 2448 | `eefc4c5befc1656a` | `9d172dc017034564b40eb381fa61e31421f509a08430864c77ccf86cfc8fe784` |
| Terminal | `files/terminal.b64` | 96 | `b45a5e3d827593ca` | `291dfd6f3e759ec2e272b35a00c24907da70c3e7a9291b4c13605c7b0b4f3de9` |
| SalPhaseIon short | `files/salphaseion-short.b64` | 96 | `3ab585348552415d` | `9e2831e1b34b5f34796df47ccaf6530d48d371c61a6bff84d60db1064fa7a258` |
| Cosmic Duality | `files/cosmic-duality.b64` | 1344 | `2d3f6fe06dc950e6` | `b18950551a4dd0cb8a9378f0906ba18c03a15f0ee83eb98c6bc90165c5f79805` |

## `files/` — original artifacts

| file | bytes | contents | sha256 |
|---|---:|---|---|
| `puzzle.png` | 29,931 | the poster, 1048 x 1556 | `38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830` |
| `follow_the_white_rabbit.png` | 1,958 | 350 x 350 image of the poster grid | `5e8d84b88f8f829428df5d2a8bf36c7268346f169b799ac7570b6223990d204f` |
| `theseedisplanted.html` | 14,886 | Phase 1 page, Wayback Machine capture of 2020-11-12 | `5b0c9e5785d88ddd17564ddf707f770588696dcf59efe565b272ea5f17c0ef84` |
| `black_banking - war.png` | 996 | Phase 1 tile | `907b489f6e77a828595805d7e370535a0aa85697ca951e0e09553e6c9a3410d2` |
| `blue_ca.png` | 627 | Phase 1 tile | `e59d42e85997d395d41eaad6fb64f343eadb752918bf33098093e96a8a9dd8be` |
| `blue_dig_i.png` | 1,030 | Phase 1 tile | `a6889a2e090d32920e47124f0187d2e61979409f9bb32a09bf0c990db56d05f9` |
| `blue_lock_lo.png` | 783 | Phase 1 tile | `60b01e5bc4181ed4236df736f7f7841aa98dde1aac108d65a385f5dc7a97cc6b` |
| `red_crypto_gic.png` | 1,642 | Phase 1 tile | `8aad87b987ee7d8ee8c7884ba47abc022cb31753fd1a16a7e59101e50dd4a6f6` |
| `red_n_you.png` | 863 | Phase 1 tile | `89a81a1b30cc399ca77dde6ffa2b01d0807e8db9b22636d157ca9f54eaf86aeb` |
| `red_open_lock_n_ing.png` | 963 | Phase 1 tile | `ea1cd545040c051a62e7695eb2dd2ad983be26849b54cd686feea12b11f3d203` |
| `red_t.png` | 506 | Phase 1 tile | `86fb2eff01d3b4f25e7bd9c64c736ce0ffd0e129b8c77fab81aac5d02fd04d35` |
| `phase2_choice.html` | 9,232 | Phase 2 / Phase 3 page | `32a531bf8b03b5d1d7699f765ab62698b61f11fd51d2d9a6f3a59dd09549844f` |
| `phase2.b64` | 898 | Phase 2 container, first textarea of that page | `411370fb9d173d1ff61eb54408782d289ab560b657a52435ee050e2842ca44df` |
| `phase3.b64` | 5,486 | Phase 3 container, second textarea of that page | `5a247f62dc0dc896d88ab2032e3adf625a4c15e1e8fda9322b4770370aac4895` |
| `phase3.2.b64` | 3,266 | Phase 3.2 container, embedded in the Phase 3 plaintext | `b296e6b450f51faa0687f468799c24f3a6e328b1ddd77bd1b631f4ee699d4300` |
| `terminal.b64` | 130 | Terminal container, embedded in the Phase 3.2 plaintext | `b2e31ce37db55bf6929d954df3676caf29c334cb9db181a6bf9adf8efbf383f1` |
| `salphaseion_phase3.html` | 4,556 | SalPhaseIon page | `18a8369df1364911d5e94fcac341ef85480ff194f4500f509fbed34f19e6308b` |
| `salphaseion-textarea.txt` | 1,075 | first textarea of that page, whitespace removed | `26e37652067c549c0eee624356be9ffd40a243901197335a41f91fb6c78e6156` |
| `salphaseion-short.b64` | 130 | the two base64 runs of that textarea, joined | `b62bb7d4c3bb27f604b67235e0a90becb98828a0d4571ad292408e27417f6779` |
| `cosmic-duality.b64` | 1,794 | second textarea of that page, whitespace removed | `9bfda585804fcf7f5183086813ca82095a829f3bc0b1922f47f0545d3414b4a4` |

## `derived/` — outputs of the steps

The three phase plaintext files are intentionally stored with LF line endings;
`.gitattributes` makes that representation consistent across checkouts. Their
sizes and hashes below describe those committed bytes. The original decrypted
CRLF representations have the following sizes and SHA-256 hashes:

| plaintext | original CRLF bytes | original CRLF SHA-256 |
|---|---:|---|
| Phase 2 | 648 | `e2f9dd65604a3231f8b3301724e8d713a88fffc4b6c7c4aeeb20f58a582b593a` |
| Phase 3 | 4,090 | `c4ad94559a44a927c1032cc0e024515f9510a0806a2d14458dbf4a360af9865f` |
| Phase 3.2 | 2,422 | `b82afeb86f9e50848220f9b64b744b821400308aea273a1c949b9d2d0e408a34` |

For these three known artifacts only, replacing LF with CRLF reproduces the
original hashes. Byte offsets in STEPS and in the descriptions below refer to
that original CRLF representation, with zero-based inclusive ranges. Do not apply
those offsets directly to the LF files or normalize encrypted/binary artifacts
in general. `mywork/candidate_pool.py` selects prose using validated section
boundaries and accepts either representation. Canonical encrypted artifacts in
`files/` have not been modified.


| file | bytes | contents | sha256 |
|---|---:|---|---|
| `phase2-plaintext.txt` | 642 | Phase 2 plaintext | `d7f90fc1c36826d62c7fae5825f245edf1e3609a6f16b5b233f51659859eebd5` |
| `phase3-plaintext.txt` | 4,032 | Phase 3 plaintext | `38360080f8fb7613466a616b5be7765e2ff19e75e6bdcfe8485500cabb424258` |
| `phase3.2-plaintext.bin` | 2,411 | Phase 3.2 plaintext | `b04876a956baac1a08d09ed17b5cf4c4337da21fe2d7f6fd55d0ae945e877da1` |
| `architect-text.txt` | 1,540 | 1,539 letters decoded from Phase 3.2 bytes 447–1985, plus newline | `1750bfac6e69270516593b40f28c004e4334622c5b8bd2ab9239fb3d8d18942b` |
| `checkerboard-digits.txt` | 150 | 149 digits from Phase 3.2 bytes 1990–2138, plus newline | `3725ee365db3caad044df38922f0d7f0cfb427680f1f9f9a086abf72758f6eab` |
| `checkerboard-plaintext.txt` | 92 | 91 letters decoded from those digits, plus newline | `0f8fd053a2c767c1cfc3332ab5443b5e176199d38311a0885caefa761678b2d1` |

## Repository layout

| path | contents |
|---|---|
| `files/`, `derived/` | original artifacts and step outputs, described above |
| `STATUS.md` | current state: open containers, hints, bounded negatives, open leads, known doc errors |
| `STEPS.md` | how each solved stage was opened |
| `matrix-reloaded.txt` | The Matrix Reloaded Architect scene transcript, read by many scripts |
| `scratchpad_grid.txt` | the 14x14 poster grid as W/K/B/Y/F letters, identical to the grid in `STEPS.md` (two cells corrected 2026-10-14). Not read by any script |
| `work/` | first round: decoding the SalPhaseIon textarea and trying passwords on the three unopened containers. Shared helpers: `openssl_decrypt.py`, `btc_check.py` |
| `mywork/` | second round: transcript, checkerboard and matrix-sum candidates, and the 40k-candidate pool search. Helpers: `lib.py`, `candidate_pool.py`. Notes: `LOG.md`, `report.md` |
| `mywork2/` | third round: zero insertion/replacement decoders and substitution solving. `*.out` files are saved script output. `web/` holds collected creator hints, GitHub issues and community notes |
| `review_leads/` | audited reviews. Start with `REVIEW.md` and `REVIEW_CORRECTIONS.md`. Scripts sit beside their reports. Results are in folders named after the script or in `*results.json` / `*padding.jsonl` files. `evidence/` holds saved chain data |
| `review_leads/cryptanalysis_2026_10_15/` | independently reproduced coordinate/Hill analysis, 512/504-bit extraction, bounded cryptographic checks, source evidence and audit scripts |
| `tests/` | regression tests for `review_leads/` and the `mywork/` candidate pool |
| `ChatExport_2026-10-08/` | Telegram chat export |
| `CLEANUP_PLAN.md` | record of the redundant-script review and the scripts it removed |

## Running scripts and tests

```
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

- Run scripts from the repository root, for example `python mywork2/zero_mixed.py`. Scripts in `mywork2/` and some in `mywork/` open `matrix-reloaded.txt` and `mywork/...` relative to the current directory.
- 30 scripts in `mywork/` and 6 in `work/` use absolute paths under `C:\gsmg-puzzle-clean` and only run from a checkout at that location.
- `work/systematic_explore.py` imports a function that `work/openssl_decrypt.py` does not define, and `work/decode_large_ai_runs.py` reads two input files that do not exist. See "Observations" in `CLEANUP_PLAN.md`.

