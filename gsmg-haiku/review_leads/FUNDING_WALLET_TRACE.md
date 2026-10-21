# Funding wallet 1EtbTvVB8QTGN4mduSdy7n4cZQm4iYTpQ1: partial history review

Source of the 5 BTC deposit `73e48ff5…` (block 571497, 2019-04-13) to `1GSMG1JC9…`. Read-only mempool.space queries, 2026-10-08.

## Scope

- The earlier review reports `chain_stats.tx_count = 50`. That total does not establish that the first `/api/address/<addr>/txs` page contains all transactions. No saved pagination cursor chain, deduplicated txid inventory, or terminal empty page is supplied here; completeness remains unverified. To claim it, retain every page, follow the confirmed-history last-txid cursor, deduplicate txids, and reconcile the count to the same snapshot.
- Reported observed span: block 334050 to block 933376; these are not established lifetime endpoints.
- Historical reported totals (rounded): funded 64.80 BTC, spent 64.80 BTC, balance 13,916 sat at the review snapshot. These are not fresh balance checks.

## What the history shows

- The address is a long-running, multi-purpose wallet. It receives change from many of its own spends and sends to many unrelated addresses.
- The earliest funding reported in this review is 1,000,000 sat from `16GRt5Wd…` in block 334050 (`a080236f…`).
- The 2019 deposit (`73e48ff5…`) consumed seven of its UTXOs, totaling 865,890,724 sat. The later parent review classifies four as self-change and three as external payments (see DEPOSIT_UTXO_TRACE.md); all are outputs of earlier transactions (e.g. blocks 542811, 544491, 558428, 501248). Two parents are large multi-input batches; the others have one or two inputs, as itemized in that review.
- Two additional observed transactions involve puzzle-related addresses:
  - block 503675 (`f931426c…`): 1,337,000 sat to `1GSMG1CLxGXuFtnKbwh1QWfp4xA6reAet3`. The earlier check reports three transactions (funded 1,347,934 sat), no spends and no OP_RETURN in its observed records; no further lead was established.
  - block 913830 (`3775e974…`): a dust transaction from `bc1qcsa5…` that includes 1,070 sat to the target. It is not from `1EtbTvVB`.

## Not done

- The subsequent bounded parent/grandparent review is in DEPOSIT_UTXO_TRACE.md. Ultimate origins remain unresolved.
- No OP_RETURN outputs were reported in the inspected subset; this cannot be extended to the full history without pagination evidence.

## Conclusion

The inspected subset is consistent with a general-purpose wallet. It does not establish the absence of OP_RETURN or puzzle messages throughout its history. Its observed puzzle-related transactions include the 2019 deposit (5 BTC to the target) and an earlier transfer to `1GSMG1CLx…` (block 503675). The dust transaction to the target (block 913830; the prior 2023 date was unsupported) is not from this wallet. The 5 BTC came from seven UTXOs of this wallet, four classified as self-change and three as external payments in the subsequent parent review. The origin of those earlier spends has not been traced.
