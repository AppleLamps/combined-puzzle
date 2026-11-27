# 20 - Key construction, not another envelope password

**Status (2026-11-27): UNSOLVED.** No prize address matched. No envelope was opened.

Doc 19 closed the KDF question for the saved material: the two unopened envelopes stay shut because the passwords are wrong, not because the derivation is MD5 or PBKDF2. The Architect line says the seven-password selection yields the actual private key. This run skips the padding gate and tests that key directly.

## What was compared

Both prize addresses, both pubkey serializations, and the P2WPKH of the compressed key:

| Target | Address |
|---|---|
| Half | `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` |
| Better Half | `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` |
| Half hash160 as P2WPKH | `bc1q492ny62h9gchuw0s75vvhp7p5rhpmwhytj2ypp` |
| Better Half hash160 as P2WPKH | `bc1qf0zxs3rluxcy3tgrpghe5yj50r4tcnkkh2umwh` |

There is no separate published segwit prize address. The two bech32 strings are the witness-version-0 encodings of the two prize hash160s.

## The strings

The 84-cell census is unchanged: 23 prime tokens, 16 `b`, 7 `be`. The seven yellow groups are `g ggege b ffcdb eggec dci eea`.

No saved file held the SELECT combinations, so `tools/key_construction.py` rebuilt them from those seven groups only: concatenation, braid, zip and reversed-braid, every cyclic start, both directions (56 strings). The seven groups were tested on their own as well.

No saved file held the yin-yang operator outputs. The script applied identity, reverse, atbash, both half-interleaves and xor-mod-26 to the 3,240 saved last-words selections, in the written case and in lower and upper case (27,184 distinct strings). The 120 distinct saved colour-selector renderings were taken as written.

The 479/484 extractions are the 476 saved M4 candidates and the 315 saved pointer windows whose note names 479 or 484.

The Phase 3.2 answer was the control and was not counted in the table.

## Matrix

| Interpretation | Valid keys | Addresses derived | Prize matches |
|---|---:|---:|---:|
| WIF, whole string, valid checksum only | 0 | 0 | 0 |
| 64 hex characters as a raw scalar | 0 | 0 | 0 |
| SHA-256 of the UTF-8 string | 28,158 | 84,474 | 0 |
| BIP39 mnemonic, or passphrase over the empty mnemonic, `m/44'/0'/0'/0/0` | 28,158 | 84,474 | 0 |

None of the 28,158 strings was a valid mnemonic, a WIF, or 64 hex characters. Every SHA-256 digest and every empty-mnemonic BIP44 key was inside the curve order. Each of those keys was checked as compressed P2PKH, uncompressed P2PKH, and P2WPKH.

The Phase 3.2 answer's brainwallet is a real key. Compressed `1K23RS1y2fnuZRkhw5nUpFr5Jk5WN11Zeq`, uncompressed `1jT9hMhmg8oZdrzD788c4j2aXZYwFuTtw`, P2WPKH `bc1qckjt8q5gh27n26afcdcaukt4ul2fhglyy8vr3u`. It does not match either prize. Before the sweep, the script reproduced the BIP173 vector, the BIP39 abandon/TREZOR seed, BIP44 of `abandon … about` (`1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA`), and both WIF forms of key 1.

## What this closes

These materials are not the prize key under the four readings above. The envelope path was not used. Detail is in [runs/2026-11-27_key_construction/REPORT.md](runs/2026-11-27_key_construction/REPORT.md).
