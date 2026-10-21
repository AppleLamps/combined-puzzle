# Combined GSMG.IO 5 BTC puzzle research

Each directory is a snapshot of one research repository, taken on 2026-10-21 from
its `claude/clever-feynman-rnoof7` branch head. The snapshot is the tracked
files only; each source repository keeps its own full history.

| Directory | Source repository | Commit | What it is |
| --- | --- | --- | --- |
| `puzle/` | AppleLamps/puzle | `bbcf6c0` | Forensic record: tested solver package, append-only attempt log |
| `GSMG-CLEAN/` | AppleLamps/GSMG-CLEAN | `795f85d` | Proven chain, open leads, dead ends, critical reviews |
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
