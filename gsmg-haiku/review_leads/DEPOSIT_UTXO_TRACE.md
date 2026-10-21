# Origin of the seven UTXOs behind the 2019 deposit

Deposit `73e48ff571a7e9a4387574a50cf2fcb7b21b6ea5702c777a035664df57cbce02` (block 571497, 2019-04-13): 5 BTC (500,000,000 sat) to `1GSMG1JC9…`, change 365,857,304 sat to `1EtbTvVB…`, fee 33,420 sat. All seven inputs are outputs of `1EtbTvVB…`.

Read-only checks against mempool.space, 2026-10-08.

## Parents (one level)

| # | parent txid (prefix) | block | date | consumed output | value (sat) | how the parent was funded |
|---|---|---|---|---|---:|---|
| 1 | `19e339ba0dbd` | 501248 | 2017-12-27 | vout 3 | 100,000,000 | batch: 201 inputs, 196 distinct senders; 115 outputs; fee 43,134,667 |
| 2 | `30a8a6303e92` | 558428 | 2019-01-14 | vout 3 | 150,000,000 | single input from `164ssHfE…` (200,000,000 sat); 5 outputs |
| 3 | `74c2ef9062ee` | 501247 | 2017-12-27 | vout 36 | 102,700,000 | batch: 201 inputs, 194 distinct senders; 120 outputs; fee 43,316,774 |
| 4 | `8a5d0979964b` | 542811 | 2018-09-24 | vout 1 | 299,798,400 | single input from `1EtbTvVB…` (399,866,200 sat); self-change |
| 5 | `9f024fcf80aa` | 458241 | 2017-03-21 | vout 1 | 1,258,124 | two inputs, both from `1EtbTvVB…`; self-change |
| 6 | `e7a17d65cc9d` | 544491 | 2018-10-05 | vout 1 | 185,716,800 | single input from `1EtbTvVB…` (353,763,933 sat); self-change |
| 7 | `f931426c3041` | 503675 | 2018-01-11 | vout 1 | 26,417,400 | single input from `1EtbTvVB…` (27,839,892 sat); also sent 1,337,000 sat to `1GSMG1CLx…` (the bounded observation in FUNDING_WALLET_TRACE) |

Check: 100,000,000 + 150,000,000 + 102,700,000 + 299,798,400 + 1,258,124 + 185,716,800 + 26,417,400 = 865,890,724 sat, equal to the seven inputs.

## Grandparents (second level, where the parent has few inputs)

- Parent 2 (`30a8…`) takes its 1.5 BTC (150,000,000 sat) output from a 2-BTC input of `164ssHfE…` (`039253f4…:0`). The other four outputs of that transaction pay `3QwRYRLR…`, `13heJh6n…`, `3MmvyKmg…`, `1N52wHoV…`.
- Parents 4, 5, 6, 7 are spends of earlier `1EtbTvVB…` outputs (grandparent txids `d78db95d…:1`, `866820ae…:1`, `4b6fec2b…:1`, `61df28cb…:178`, `e8e14d9f…:0`). Their own origins were not traced further.
- Parents 1 and 3 are batch transactions (201 inputs each). Their inputs were not traced: tracing 201 inputs per batch is out of scope here.

## Classification of the 8.65890724 BTC input total

By immediate source at the level traced; these percentages partition the inputs, not the 5 BTC target output. Fungible inputs cannot be uniquely assigned between target, change, and fee:

| origin | sat | share |
|---|---:|---:|
| external payments (`30a8…`, `19e3…`, `74c2…`) | 352,700,000 | 40.7% |
| `1EtbTvVB…` self-change chain (`8a5d…`, `9f02…`, `e7a1…`, `f931…`) | 513,190,724 | 59.3% |

The self-change chains are not resolved. Their ultimate sources are older `1EtbTvVB…` outputs, with a 1,000,000 sat funding reported in the inspected subset (FUNDING_WALLET_TRACE) from `16GRt5Wd…` in block 334050. Pagination is unverified, so that observation establishes neither the first lifetime funding nor the ultimate source of these self-change chains.

## Observations (no interpretation)

- The two batch transactions have unusually large fees (about 0.43 BTC each) for their size. This is noted as an observation only; the batches are not identified by this check.
- No OP_RETURN or puzzle message was reported in the transactions inspected here. This is bounded to that subset; FUNDING_WALLET_TRACE does not establish complete history.
- The block-503675 transaction (`f931426c…`) is also the source of the `1GSMG1CLx…` payment, for which no further lead was established in the inspected subset (see FUNDING_WALLET_TRACE).

## Not done

- Batch transactions `19e339ba…` and `74c2ef90…`: inputs not traced.
- Self-change chains: beyond the parent level, not traced.
- The `164ssHfE…` 2-BTC input (`039253f4…`) and its history: not traced.
