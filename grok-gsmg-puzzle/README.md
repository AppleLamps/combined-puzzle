# GSMG.io 5 BTC puzzle — offline cryptanalysis

Independent reconstruction of the solved phases, then a data-level reading of the SalPhaseIon `faed` block. Nothing in this repo contacts `gsmg.io` or any other endpoint. A candidate is accepted only when its public key hashes to the prize address.

Prize address `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`, hash160 `a9553269572a317e39f0f518cb87c1a0ee1dbae4`.

## Layout

| Path | Contents |
|------|----------|
| `uploads/GSMG-handoff.md` | Canonical second-build handoff (single source) |
| `data/puzzle.png` | Poster image (provenance in `ledger/README.md`) |
| `src/` | Trust chain (`step0`–`step3`), archivist checks, crypto helpers |
| `artifacts/` | Plaintexts, containers, battery JSON — see `artifacts/README.md` |
| `team/` | Preregistered decrypt batteries — see `team/README.md` |
| `puzzle-order.md` | Step-by-step path through the puzzle |
| `ledger/` | Agent notes and round reports (`00-lead.md` … `22-round14.md`, plus `round5/`) |

## Run

```bash
pip install -r requirements.txt
python3 src/step0_trust.py    # known-answer tests, solved phases, Bifid
python3 src/step1_btcseed.py  # tail-as-seed, containers, yin-yang rearrangements
```

`src/step0_trust.py` exits non-zero unless every check passes, including the FIPS-197 / SP 800-38A AES vectors, the private-key-1 hash160 control, and decryption of phases 2, 3 and 3.2. Intermediates land in `artifacts/` with sha256 sidecars.

## Result

The full-period Bifid of the 570-letter `faed` block on the square `dbifhcegaklmnopqrstuvwxyz` is in `artifacts/faed_bifid.txt`. It begins `btcseedd` on that square; **8 of 362,880** nine-letter square orderings share the `btcseed` prefix (handoff §6.3 / §8.1 — not a unique checksum). The tail is not hex, not a WIF, and not a BIP39 mnemonic. SHA-256 of the plaintext, of the tail, and of the odd-position stream, plus BIP39 derivations of those digests, do not produce the prize key. The same strings do not open the Terminal, SalPhaseIon-short, or Cosmic Duality containers, nor the yin-yang rearrangements of those containers, under the solved OpenSSL convention or the raw-digest and double-hash variants.

The yellow/blue prime walk over the `dbbi` block does parse: at 1-indexed position 83 the 91 letters are exhausted, and every prime chunk is `b` (blue or off-white) or `be` (yellow). The 60 filler letters are in `artifacts/yellowblue_fillers.txt`. Read with the page's own decimal decoder they are 25 opaque bytes; as base-9 they are 24 bytes whose BIP39 mnemonic does not derive the prize key.

No container was opened. No private key matched the address.

`python3 src/step2_peel.py` runs the whole-integer base-256 peel and the cp273 symbol table. The streaming peel in that file is not the page's rule; `lastwordsbeforearchichoice` and `thispassword` come from the integer reading only.

`python3 src/step3_mask.py` zeros faed digits at 1-based positions `{1, 3, 551, 557, 561, 563}` and reads the integer as 236 bytes. The ends are `yM` and `szqu`; the interior is not ASCII. It also runs the last-words × yellow-blue × matrix-sum password battery.

`python3 team/deletion_sweep_faed.py` tries **all 64 subsets** of those six positions with **letter deletion** (not zeroing) → integer bytes → §4.1 passwords (`ledger/07-deletion-sweep.md`).

Team ledgers: `ledger/00-lead.md` through `ledger/22-round14.md`. Batteries: `team/round11_pipeline.py` … `round14_clues.py` (structural / clue pipelines), `team/round8_reader_gap.py` … `round10_phase3_g12.py`. Unified detector: `team/classify_unified.py`.

`python3 team/audit_rerun.py team/round4_battery.py …` re-runs any battery with every AES decrypt checked by a recogniser that flags the phase 3.2 plaintext; all 18 batteries come back with valid pads at chance and nothing flagged (`ledger/23-detector-audit.md`). `python3 src/checkerboard_pairs.py` checks the 149-digit blank pair.

`python3 src/check_report3_2026-10-17.py artifacts` re-runs the 17 October check script against `faed.txt`, `dbbi.txt`, `matrix.json`, and the Architect letters.
