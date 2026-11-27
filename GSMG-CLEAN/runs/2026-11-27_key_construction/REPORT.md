# Key construction against the two prize addresses — 2026-11-27

No envelope was opened. The chat sweep was not run. The 84-cell parse still has 23 prime tokens, 16 `b` and 7 `be`.

## What was tested

Each string was turned into a private key in four ways. A scalar of 0 or at or above the secp256k1 order was rejected. Every accepted scalar produced a compressed P2PKH address, an uncompressed P2PKH address, and the P2WPKH address of the compressed key.

1. The whole string as a WIF. Compressed and uncompressed mainnet WIFs are both accepted. Only a valid Base58Check checksum proceeds.
2. The whole string as 64 hex characters, read as a raw 32-byte scalar.
3. SHA-256 of the UTF-8 string, as the brainwallet scalar.
4. BIP39. A valid mnemonic is derived with an empty passphrase. Every string is also the passphrase over the empty mnemonic. The key is `m/44'/0'/0'/0/0`.

The two prize addresses are `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` and `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`. Their hash160s were compared as well. No native-segwit prize address is on record, so the P2WPKH of each key was compared with the bech32 form of each prize hash160: `bc1q492ny62h9gchuw0s75vvhp7p5rhpmwhytj2ypp` and `bc1qf0zxs3rluxcy3tgrpghe5yj50r4tcnkkh2umwh`.

## Where the strings came from

The seven yellow groups of the standing 84-cell parse are `g`, `ggege`, `b`, `ffcdb`, `eggec`, `dci`, `eea`. No earlier file held the braid, zip, reversed-braid and concatenation variants, so those 56 strings were rebuilt from these seven groups: every cyclic start, both directions. The seven groups themselves were gated separately.

The yin-yang operator dump was not on disk either. The six operators (identity, reverse, atbash, both half-interleaves, xor of the halves as a letter) were applied to the 3,240 saved last-words selections in `runs/2026-11-10_step2_sumlist_lastwords_v3/outputs.jsonl`, in the original case and in lower and upper case. The 142 saved colour-selector renderings were included as they stand; 120 of them are distinct.

The 479/484 extractions are the 476 saved M4 candidates and the 315 saved pointer windows whose note names 479 or 484.

## Matrix

Unique strings, then valid keys and derived addresses. Addresses are three per valid key. Matches are prize hits.

| Family | Strings | WIF keys / addr | Hex64 keys / addr | SHA-256 keys / addr | BIP39 keys / addr | Matches |
|---|---:|---:|---:|---:|---:|---:|
| Step-2 SELECT combinations | 56 | 0 / 0 | 0 / 0 | 56 / 168 | 56 / 168 | 0 |
| Step-2 seven groups | 7 | 0 / 0 | 0 / 0 | 7 / 21 | 7 / 21 | 0 |
| Step-3 colour renderings | 120 | 0 / 0 | 0 / 0 | 120 / 360 | 120 / 360 | 0 |
| Step-3 yin-yang operators | 27,184 | 0 / 0 | 0 / 0 | 27,184 / 81,552 | 27,184 / 81,552 | 0 |
| Step-4 M4 extractions | 476 | 0 / 0 | 0 / 0 | 476 / 1,428 | 476 / 1,428 | 0 |
| Step-4 479/484 windows | 315 | 0 / 0 | 0 / 0 | 315 / 945 | 315 / 945 | 0 |
| **All** | **28,158** | **0 / 0** | **0 / 0** | **28,158 / 84,474** | **28,158 / 84,474** | **0** |

No string was a valid BIP39 mnemonic, so every BIP39 key is the empty-mnemonic passphrase. No string was a checksum-valid WIF or 64 hex characters.

## Control

`jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple` is the Phase 3.2 answer. Its SHA-256 is inside the curve order and derives

- compressed P2PKH `1K23RS1y2fnuZRkhw5nUpFr5Jk5WN11Zeq`
- uncompressed P2PKH `1jT9hMhmg8oZdrzD788c4j2aXZYwFuTtw`
- P2WPKH `bc1qckjt8q5gh27n26afcdcaukt4ul2fhglyy8vr3u`

None of those is a prize address. The same string is not a WIF and not 64 hex characters. As an empty-mnemonic passphrase it also misses both prizes.

The path was checked before the sweep: the BIP173 bech32 vector, the BIP39 abandon seed with passphrase `TREZOR`, BIP44 `m/44'/0'/0'/0/0` of `abandon … about` with an empty passphrase (`1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA`), key 1 (`1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH`), and both WIF forms of key 1.

## Result

Zero prize matches. These strings are not the Half or Better Half private key under WIF, raw hex, brainwallet SHA-256, or BIP44 `m/44'/0'/0'/0/0` from a mnemonic or from the empty mnemonic.
