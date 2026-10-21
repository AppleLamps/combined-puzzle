# Base58 string in the 2025-12-30 message

String: `1Pi36y7LJugXwFNDVjR1p8p5JoB7eN5zSZ`

Decoded (Base58Check):
- version byte: `00` (P2PKH mainnet address)
- hash160: `f91593bb5957f50a8e34a3d336b06630201fdc5a`
- checksum: `c6af1c5e` (double SHA-256 of the payload, first 4 bytes; valid)

Result: a valid P2PKH address, not a private key or WIF. It is the change address of the fan-out transaction that carried the 2025-12-30 message, per the earlier on-chain check. It is not a puzzle address and is not linked to 1GSMG1JC9… by any key.

Decoding was done locally in Python (no network). The checksum matches, so the string is well formed.
