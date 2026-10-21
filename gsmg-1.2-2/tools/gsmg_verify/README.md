# GSMG puzzle verification harness

Independent scripts that rebuild the dossier's primary data from this
repository's actual source files — the poster PNG's pixels, the archived
HTML pages, the Telegram export — and cross-check every pinned hash, salt,
length and decoded string in `GSMG-PUZZLE-DOSSIER.md` against that
independently-derived data. Nothing here retypes a dossier data block by
hand; `lib.block_joined(idx)` pulls fenced code blocks straight out of the
dossier's markdown by index (see `lib.fenced_blocks()`).

See `../../SESSION-LOG-131.md` for the write-up of what these confirmed.

## Requirements

```
pip install pycryptodome coincurve pillow ebcdic base58
```

## Running

Run in this order (each later script reads intermediate files the earlier
ones write to `out/`):

```
mkdir -p out
python3 verify_chain.py                    # phase 1 -> 2 -> 3 -> 3.2 decrypt chain
python3 verify_architect_checkerboard.py   # Architect (cp273 + reciprocal Beaufort) + straddling checkerboard
python3 verify_containers_textarea.py      # the 3 locked containers + textarea segmentation
python3 verify_poster.py                   # poster spiral, derived from pixels
python3 verify_colorlayer_dbbi.py          # colour-layer LSB claim + both DBBI walk models
python3 verify_wintest_segments.py         # win-test target self-consistency + rule1/rule2 decodes
python3 verify_key_relations.py             # P-G, P/2, 2P, P+G -> unattributed addresses
python3 verify_onchain_relations.py         # offline accounting/cross-reference checks
python3 verify_onchain_relations.py --live  # optional: independent explorer verification
```

Each script prints one `PASS`/`FAIL` line per check and a `SUMMARY` line.
The original six scripts were last reported with zero failures. The two new
scripts passed in this change; the original image-based suite was not rerun
in the partial local checkout.

The key relation verifier needs only Python's standard library and recomputes
the four uncompressed P2PKH addresses from the exposed prize public point.
The on-chain verifier's offline mode checks a pinned manifest against five
saved Esplora transaction JSON snapshots for accounting, scripts, and linkage;
the saved snapshots alone do **not** establish transaction authenticity.
`--live` reads each
listed transaction from the Blockstream Esplora API and checks the values,
outpoints, embedded public key, OP_RETURN, vanity-address inputs, and the two
2020 block positions. It requires network access and fails if it cannot fetch.
The manifest and transaction snapshots are in `../../source/onchain/`.
The funding vanity address has not been authenticated as creator-controlled.

`tg.py` is a small helper for looking up Telegram export messages by id
(`python3 tg.py 8446 1710 ...`), used to spot-check dossier citations against
`../../gsmg-group-telegram-by-year/*.json`.

`lib.py` holds the shared primitives: dossier block extraction, the
EVP_BytesToKey/AES-256-CBC decrypt matching the proven convention (section 2
of the dossier), and the HASH160/win-test check against the prize address,
its compressed twin, and the halving sentinel.
