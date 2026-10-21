# GSMG.io 5 BTC puzzle: project index

Current interpretation: 6 October 2026. Artifact and balance snapshots retain their stated dates.

Start with [the current evidence ledger](claude/119-current-evidence-ledger.md) and [status](claude/status.md). They supersede stronger interpretations in older dated logs; no new unlock or search is reported.

**The dossier, `claude/GSMG-PUZZLE-DOSSIER.md`, holds the detailed artifact record:** the goal and exact win test, derivations with their assumptions, creator statements with reply context, and historical experiments. Read its older negative results with the limits in docs 118 and 119. The other files in this project are data, three short reference sheets and an analysis log.

`claude/67-document-index.md` lists every surviving log doc with its status and the errata for stale sentences inside them, and maps each retired doc to the dossier section that now carries its content.

## State in brief

- **Target.** `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` held 1.25636967 BTC on 2026-09-29. It has spent twice, so its public key is exposed. `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` (3.75055856 BTC, never spent) is the destination of the two halvings and serves as a sentinel in the win test. It is not a puzzle output.
- **Chain.** Four gates are open (phase 1, phase 2, phase 3, phase 3.2). Three containers are shut: Terminal, SalPhaseIon short and Cosmic Duality.
- **The SalPhaseIon textarea.** The labels decode. DBBI matches the poster-color prime walk under the fixed first-23-event model. L84 alternatives remain; FAED/residue filler is a model, not proof of no payload.
- **Oracles.** The six recorded `GSMG.io:` checkpoints have known preimages; the phase-1 verifier is not a remaining-stage oracle.
- **Unresolved.** The operations, operands, assembly, selection, receiver, and lock order remain unknown. Joint concatenation is one model. A null applies to its complete tested hypothesis tuple, not an isolated reading or every possible continuation.
- **Envelopes.** Terminal, SalPhaseIon short and Cosmic Duality remain locked. Their provenance is established to different strengths; their mandatory use, order, cipher and contents are not established.
- **Latest corrections.** The unsigned coordinate independently matches the historical SafeNet address and current building. Genesis part 6 is exactly 140 characters, but its link to the Architect's “hundred fourty” or “code you carry” is unproved. Category counts do not establish a 23/16/7 selection.
- **Historical work.** Docs 115–117 report large negative runs. Doc 118 identifies detector and membership limits, including an omitted 144-form assembly set, and distinguishes source-only checks from encrypted execution. No corrected search or new unlock is claimed here.
- **Current activity.** No search is running. Old blocked selections and Atlas work are historical records, not a queue to resume.

## Standing rules

1. Do not submit anything more to `gsmg.io/phase1verification`. Ten submissions characterised it completely.
2. Do not contact, locate or profile the creator (dossier section 11). Do not propose anything that needs another person.
3. On-chain OP_RETURN text is unauthenticated. The generic denial (#12653, 29 August 2023) predates later 2025/2026 messages and is not a specific denial of them. Later oracle traffic is inbound from other keys, several publicly computable (`07-onchain-facts.md`).
4. The win test in dossier section 1 is free and silent. A long run of negatives says nothing about proximity.
5. A null counts only when its control fired. Confirm the control before publishing the null.
6. Nothing observed on `gsmg.io` today is creator material until it matches a pre-2022 archive capture or a hash this project already holds.
7. No new method gets CPU unless it retrodicts the phase 2, 3 and 3.2 answers. One reading, one candidate. No more coverage sweeps (set 3 October 2026).

## Files

All files sit at the top level of the project, apart from the analysis log under `claude/` and the scripts under `tools/`. There are no `source/`, `ciphertexts/` or `data/` folders; the dossier's section 13 lists the checks that were run against the primary data, and `tools/verify.py` and `tools/poster.py` re-run them.

### Reference sheets

| file | contents |
|---|---|
| `04-key-material.md` | prize and twin addresses, the four elliptic-curve neighbours, the six checkpoints, the two poster checkpoints, the tip address, balances |
| `07-onchain-facts.md` | the 30 transactions of the oracle address (signed and inbound), the later traffic, the May 2026 vanity-address sequence |
| `ARTIFACTS.md` | sizes, salts and sha256 of every container, plaintext and image; which file holds which object |

### Machine-readable data

| file | contents |
|---|---|
| `keys.json` | every address, hash160 and public key in `04-key-material.md`, with balances and transaction counts pulled from mempool.space on 2026-09-29 |
| `message-sequence.json` | the May 2026 vanity-address messages in spend-chain order, with txids, blocks and payload hex |
| `matrix.json` | the poster's 14x14 grid as colour letters and bits, the spiral parameters, the blue and yellow spiral indices, the anomaly cell |
| `jrk_messages.txt` | the creator's 492 messages plus 18 admin actions from the Telegram export, with reply headers naming the parent message. It is the source for every creator quotation in the dossier |

### The puzzle's own artifacts

| file | contents |
|---|---|
| `puzzle.png` | the poster (1048 x 1556, sha256 in `ARTIFACTS.md`) |
| `follow_the_white_rabbit.png` | the rabbit image (350 x 350) |
| `red_t.png`, `red_n_you.png`, `red_crypto_gic.png`, `red_open_lock_n_ing.png`, `blue_ca.png`, `blue_dig_i.png`, `blue_lock_lo.png`, `black_banking - war.png` | the eight rebus tiles of phase 1 |
| `theseedisplanted.html` | the phase-1 page as captured by the Wayback Machine on 2020-11-12 (eight tile images and the hidden form that posts to `/phase1verification`) |
| `phase2_choice.html` | the phase 2 and phase 3 page: riddle text, the chess FEN, and the phase 2 and phase 3 base64 containers |
| `salphaseion_phase3.html` | the SalPhaseIon side page: the 1,075-character textarea and the Cosmic Duality textarea (wrapped at 64 characters) |
| `phase2.b64`, `phase3.b64`, `phase3.2.b64` | the three solved containers as base64 |
| `terminal.b64`, `salphaseion-short.b64`, `cosmic-duality.b64` | the three locked containers as base64 |

### Extracted and derived streams

| file | contents |
|---|---|
| `salphaseion-textarea.txt` | the 1,075-character SalPhaseIon textarea, verbatim |
| `dbbi.txt`, `faed.txt` | the two soup segments (91 and 570 symbols) |
| `architect_letters_1539.txt` | the phase 3.2.1 output, 1,539 letters. Stored in uppercase. The decode itself emits lowercase, and case is presentation |
| `checkerboard_vic_91.txt` | the 91-letter straddling-checkerboard plaintext (no word breaks) and the 149 digits that encode it |
| `payload-gsmgjh.txt`, `payload-gsmgbh.txt` | the two binary OP_RETURN payloads (64 and 65 bytes) of the May 2026 vanity address, as hex. Unauthenticated |

### Scripts (`tools/`)

`tools/README-tools.md` is the entry point. The folder holds the container-testing harness (`h3.c`), the win test (`wintest.py`), the flag checker (`chk_flags.py`), the pool builders (`pools.py`, `mkpools.py`, `mkmore.py`, `mk_rgb.py`, `n2.py`, `mkrem_approx.py`), the planted-control builders (`mk.py`, `mkctl.py`), the exact-fit tests (`n1.py`, `n2.py`, `fit.py`, `constfit.py`), the dossier verifiers (`verify.py`, `poster.py`) and `setup.py`, which rebuilds the working files from the Project's own files and checks each against the hashes in the dossier. Put the Project files and `tools/` in one folder and run `python3 setup.py`. Five of the pools in doc 115 have no script or only an approximate one; the table in `tools/README-tools.md` says which.

## Analysis log (`claude/`)

- `119-current-evidence-ledger.md` is the current interpretation and discovery ledger; `GSMG-PUZZLE-DOSSIER.md` carries the detailed evidence.
- `118-correctness-audit-remediation.md` records corrected source behavior, historical detector limits, and verification that was not run.
- The historical catalog spans docs 09–117; this checkout retains docs 21, 67 and 114–118 alongside the dossier and workstream records. Other catalogued docs may be absent. Doc 67 maps their content and old errata; doc 119 supersedes overbroad interpretations.
- `claude/21-checkpoint-oracle.md` holds the on-chain checkpoint enumeration and the reusable checker; `claude/113` holds the re-audit of the oracle's signed set.
- Docs that were folded into the dossier and retired are listed in `claude/67` with the sections that now carry them.
- `claude/FAILED-ATTEMPTS-LOG.md` is the off-repo do-not-repeat register for the three locked containers (3 Oct 2026); `claude/FAILED-ATTEMPTS-INDEX.md` maps it against the dossier and, in its section 6, lists every null of 3 to 4 October with its controls.
- `claude/116-coverage-gaps-closed.md` reports runs addressing named doc 115 gaps (logs in `claude/doc116-runs/`); its title does not establish exhaustive coverage or repair missing original membership evidence.
- `claude/117-riddle-rounds-and-the-pair-ledger.md` covers the work of 3 and 4 October: `claude/critical-review-2026-10-03.md` and one folder per workstream (`riddle-method/`, `independent-model/`, `microstep/`, `constraints/`, `rabbit-holes/`, `selection/`, `source-pointer/`, `genesis-main-cpp/`, `photo-analysis/`, `common-flaw/`), each with its write-up, scripts, candidate lists and run logs.
- `claude/status.md` is the one-page status.

## Corrections of record

The current correction hierarchy is docs 118 and 119, then the updated active summaries and dossier. Dossier section 11 and doc 67 section 5 preserve earlier errata; those earlier errata can themselves be superseded. Original candidate files, primary artifacts and run logs are unchanged.
