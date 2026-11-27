# Combined GSMG.IO 5 BTC puzzle research

**Status: unsolved.** No locked envelope has been opened and no private key has been found.

## Canonical ledger

`GSMG-CLEAN/` is the single source of truth. Start at
[`GSMG-CLEAN/16_CANONICAL_LEDGER_AND_WORKING_RULES_2026-11-10.md`](GSMG-CLEAN/16_CANONICAL_LEDGER_AND_WORKING_RULES_2026-11-10.md).
The other nine directories are frozen snapshots; each has a `CANONICAL_NOTICE.md` listing the
statements in it that the ledger contradicts.

Last checked against the chain, the chat and the live site on 2026-11-10:
[`GSMG-CLEAN/17_STATE_REFRESH_2026-11-10.md`](GSMG-CLEAN/17_STATE_REFRESH_2026-11-10.md).

Connections and reasoning traps across docs 01 to 17 (2026-11-27):
[`GSMG-CLEAN/18_CONNECTIONS_AND_REASONING_2026-11-27.md`](GSMG-CLEAN/18_CONNECTIONS_AND_REASONING_2026-11-27.md).
A thinking pass, not a solve: no envelope opened, no key derived.

KDF check on the two unopened envelopes (2026-11-27):
[`GSMG-CLEAN/19_KDF_MODEL_CHECK_2026-11-27.md`](GSMG-CLEAN/19_KDF_MODEL_CHECK_2026-11-27.md).
EVP-MD5 and PBKDF2 do not open them, and a zero IV does not fail the padding gate.

Key construction against the two prize addresses (2026-11-27):
[`GSMG-CLEAN/20_KEY_CONSTRUCTION_2026-11-27.md`](GSMG-CLEAN/20_KEY_CONSTRUCTION_2026-11-27.md).
The saved step-2/3/4 strings, read as WIF, hex, brainwallet and BIP44 keys, match neither prize.

Prime-5 reinsertion into the pre-Beaufort source record (2026-11-27):
[`GSMG-CLEAN/21_PRIME5_REINSERTION_2026-11-27.md`](GSMG-CLEAN/21_PRIME5_REINSERTION_2026-11-27.md).
116 scalars, no prize match.

Cosmic Duality with the six SalPhaseIon answers hashed (2026-11-27):
[`GSMG-CLEAN/22_COSMIC_SIX_HASH_2026-11-27.md`](GSMG-CLEAN/22_COSMIC_SIX_HASH_2026-11-27.md).
32 decrypts, no padding hit, no legible plaintext.

How the creator thinks, from his own words and the public record (2026-11-27):
[`GSMG-CLEAN/22_CREATOR_THINKING_PROFILE_2026-11-27.md`](GSMG-CLEAN/22_CREATOR_THINKING_PROFILE_2026-11-27.md).
Analysis only, nothing run.

Runs without a numbered document yet (2026-11-27):

- [`GSMG-CLEAN/runs/2026-11-27_cosmic_null_validity/`](GSMG-CLEAN/runs/2026-11-27_cosmic_null_validity/REPORT.md):
  of 16 recorded families that claim a null on Cosmic Duality, 5 are valid, 1 is partial and 10
  are invalid under the pinned profile. Replaying 3,461 gap candidates opened nothing.
- [`GSMG-CLEAN/runs/2026-11-27_matrixsum_replay/`](GSMG-CLEAN/runs/2026-11-27_matrixsum_replay/REPORT.md):
  the 2026-09-13 matrix-sum pipeline rerun with every pad-valid plaintext kept. 9,236 forms against
  3 envelopes under the pinned profile gave 111 pad-1 outputs (chance rate), no pad 3 or higher,
  and no prize key.
- [`GSMG-CLEAN/runs/2026-11-27_typo_stream/`](GSMG-CLEAN/runs/2026-11-27_typo_stream/README.md):
  hypothesis only. The seven letters the Architect text inserts as typos, and a 1,532-letter
  text with them removed. The poster colour map does not confirm it.

The working rules set on 2026-11-10 (no envelope sweeps, preregistration before every experiment,
the derivation gate in `GSMG-CLEAN/tools/check_candidate.py`) were removed on 2026-11-27. New findings
still go in `GSMG-CLEAN/` as a numbered document plus a `runs/` directory.

## The directories

Each directory started as a snapshot of one research repository, taken on 2026-10-21 from
its `claude/clever-feynman-rnoof7` branch head. The snapshot is the tracked
files only; each source repository keeps its own full history. `GSMG-CLEAN/` has been
edited here since then. The other nine have only gained their `CANONICAL_NOTICE.md` and the
provenance fixes of 2026-11-10.

| Directory | Source repository | Commit | What it is |
| --- | --- | --- | --- |
| `puzle/` | AppleLamps/puzle | `bbcf6c0` | Forensic record: tested solver package, append-only attempt log |
| `GSMG-CLEAN/` | AppleLamps/GSMG-CLEAN | `795f85d` | **Canonical ledger.** Proven chain, open leads, dead ends, critical reviews |
| `gsmg-puzzle-kit/` | AppleLamps/gsmg-puzzle-kit | `db3b28d` | Working kit: dossier, harness, evidence ledger, doc 120 |
| `gsmg/` | AppleLamps/gsmg | `85a99d9` | Dossier fork (docs 115 to 122) |
| `gsmg-1.2/` | AppleLamps/gsmg-1.2 | `35ea6a4` | Dossier fork |
| `gsmg-1.2-2/` | AppleLamps/gsmg-1.2-2 | `c9d19a3` | Dossier fork with verification harness (records 127 to 141) |
| `gsmg-haiku/` | AppleLamps/gsmg-haiku | `eefccc4` | Coordinate and Hill cryptanalysis, October chat export |
| `grok-gsmg-puzzle/` | AppleLamps/grok-gsmg-puzzle | `289c3e6` | Battery audits and ledger |
| `5g-puzzle/` | AppleLamps/5g-puzzle | `df66e78` | Synthesis of the solver chat, yearly transcripts |
| `gsmgio-5btc-puzzle-sept/` | AppleLamps/gsmgio-5btc-puzzle-sept | `939a18a` | Community README fork, assets, ciphertexts |

`claude-gsmg` had no commits and is not included.

## Shared across all of them

`tools/prize_gate.py` (in `puzle/` it is `gsmgio-5btc-puzzle-master/solver/prize_gate.py`)
is the same checker everywhere. It gates a candidate against both prize addresses under
both public-key serializations and parses keys stored as raw bytes, hex, WIF, mini key,
base64 or decimal out of any plaintext:

```
python3 GSMG-CLEAN/tools/prize_gate.py selftest
python3 GSMG-CLEAN/tools/prize_gate.py scan <path>
```

Each directory has a rescan report of its own committed outputs through that checker.

## Large file

`GSMG-CLEAN/runs/2026-09-14_source_cipher_keys/keys.json` (110 MB) is stored with Git LFS,
as in its source repository. Run `git lfs pull` after cloning to fetch it.

Each directory's own `CLAUDE.md`, `README.md` and `.gitignore` still apply inside it.
