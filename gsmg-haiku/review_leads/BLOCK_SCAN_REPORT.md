# Full-block OP_RETURN scan: blocks 630001 and 840725

Scan: every transaction in each block, every OP_RETURN output, from `scratchpad/block_scan.py` (mempool.space block API). Date: 2026-10-08.

| block | time (UTC) | txs scanned | OP_RETURN outputs | printable | non-UTF-8 | outputs linked to 1GSMG1JC9 / 3GSMG24 / 17ucy1K9 inputs |
|---:|---|---:|---:|---:|---:|---|
| 630001 | 2020-05-11 20:02:50 | 3295 | 33 | 18 | 15 | 1 (`Halving`, creator 3GSMG24…) |
| 840725 | 2024-04-24 21:47:27 | 2438 | 921 | 305 | 616 | 0 |

## Block 630001

- The creator's `Halving` OP_RETURN (txid `a798905f…`, vout 0) is in this block. It is the same block as the 2.5 BTC spend `2aa9a4a9…`, which consumes a 700-sat output of that transaction. This is the link already recorded in OP_RETURN_LOG.md.
- Other printable texts are unrelated third-party messages. Nine contain "halving", "Satoshi" or similar. These are not linked to the target.
- The 15 non-UTF-8 payloads are binary (e.g. `6f6d6e69…` = "omni" protocol markers) and are not linked to the puzzle addresses.

## Block 840725

- 921 OP_RETURN outputs, 305 printable. The keyword filter (GSMG, door, prize, halv, neo, matrix, satoshi, btc, key, secret, hint, 1357, answer, puzzle) found 0 matches.
- No output in the block has an input from 1GSMG1JC9, 3GSMG24 or 17ucy1K9. The 1.25 BTC spend `88cdb3cd…` therefore has no OP_RETURN partner in its block.

## Conclusion

Only the 630001 `Halving` message is linked to the puzzle addresses in these two blocks. The 2024 spend block contains no puzzle-linked message.

## Brainwallet extension (same session)

`review_leads/BRAINWALLET_CANDIDATES.md` (499 passphrases) was extended with 31 printable texts from these two blocks. Each passphrase was tested as SHA-256 and as double SHA-256, in compressed and uncompressed form (530 passphrases, 1060 keys). No match to hash160 `a9553269…dbae4`.
