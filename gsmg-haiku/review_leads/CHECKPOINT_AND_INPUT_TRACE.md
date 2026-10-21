# Checkpoint preimages and input traces (open items from BLOCK_SCAN_REPORT)

Read-only checks against mempool.space. Date of check: 2026-10-08.

## 1. Phase 3.2 checkpoint: `1K23RS1y2fnuZRkhw5nUpFr5Jk5WN11Zeq`

- Preimage: `jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple` (from `mywork/do_it.py`, Phase 3.2 answer).
- SHA-256 hex: `250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c`.
- Compressed hash160 derived from that key matches the address. Same brainwallet construction as the 227-character checkpoint.
- Creator reply: tx `2f64b8758f97eb5b…`, block 622767, "GSMG.io: phase3.2 pass OK", 1000 sat.

## 2. Sender of the 227-character submission

- Checkpoint `1M5ypvDbp124ZtKPbg3GJg1JqNs1x7TPoN` has four transactions:
  - 2020-03-24, creator reply `62dbb701…` (block 622774), 990 sat to 1M5yp.
  - 2020-03-31, spend `56631ed0…` (block 623645), 760 sat to `16z9HAbw…`.
  - 2025-05 (block 897354), payment `30e4803d…` of 1000 sat from `bc1q0rwru9…` with 32919 sat change. No OP_RETURN.
  - 2025-05 (block 897355), spend `bd250ac4…`, 577 sat to a P2SH address.
- No transaction sends the answer or any OP_RETURN message to 1M5yp before the creator's reply.
- The creator address `3GSMG24…` has no non-self incoming transaction in blocks 622600–622800 with an OP_RETURN. The one non-self payment in the window, `1f8eb99e…` (block 622711), is a plain transfer of 15000 sat from `37mh7EYe…` to 3GSMG24 with change, no message.
- Conclusion: the 227-character submission is not on-chain in this data. It was most likely sent off-chain (e.g. a web form). The on-chain trail starts at the creator's reply.

## 3. Inputs of the 2024 spend (`88cdb3cd…`, block 840725)

The spend has three inputs, all from the target address:

| input | value (sat) | source |
|---|---:|---|
| `2aa9a4a9…:0` | 249815966 | the 2020 spend (block 630001) |
| `81d35929…:0` | 535500 | tx in block 809252, funded from `bc1qey9rjg…` (53428063 sat), change 52889203 sat to `bc1qfyaxmt…`, fee 3360 |
| `f28b0b68…:0` | 666 | tx in block 798906, funded from `1GmTEC3…` (121136 sat), with outputs 666 sat to target, 700 sat to sink `17ucy1K9…`, 12260 sat to `1PJtgVF…`, fee 107510 |

- The 700-sat output to the sink (`f28b0b68…:1`) is a link between the target's UTXO and the sink address. The sink is the 2.5 BTC spend's output address too (block 630001). Not yet interpreted.

## 4. Funding source of the 2019 deposit (`73e48ff5…`, block 571497)

- Seven inputs, all from `1EtbTvVB8QTGN4mduSdy7n4cZQm4iYTpQ1`, total 865,890,724 sat.
- Outputs: 500000000 sat (5 BTC) to the target, 365857304 sat change back to `1EtbTvVB…`, fee 33420.
- Totals reconcile: 865890724 − 500000000 − 365857304 = 33420.
- Not traced further: the history of `1EtbTvVB…` itself (not fetched).

## 5. Other input checked

- The 666-sat input of the 2020 spend (`a2d2481d…`, block 622713) comes from `1JEDYYneiRTgDVpyavXf2wedzwtN3v7QKS` (2013 sat in, 1026 sat change, 321 fee). The 666 sat is the same value as the target's 666-sat outputs, which is an amount repeated across the target's transactions.

## Still open

- The origin of `1EtbTvVB…` (who funded the 2019 deposit). Partly covered by [FUNDING_WALLET_TRACE.md](FUNDING_WALLET_TRACE.md) and [DEPOSIT_UTXO_TRACE.md](DEPOSIT_UTXO_TRACE.md); the origin of its self-change chains is still unresolved.
- The sink address `17ucy1K9…`'s other inputs and outputs, in relation to the 700-sat link above.
- The phrase or key behind the 227-character submission, if it was off-chain.
