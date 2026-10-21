# On-chain activity: 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe

- Source: mempool.space public API, read 12 Sep 2026.
- Chain tip at the time of reading: block 966742.
- The address has 126 transactions. The computed balance matches the explorer's totals.

## Key events

| Date (UTC) | Block | Tx | What happened |
|---|---|---|---|
| **2019-04-13 16:32:40** | 571497 | `73e48ff571a7e9a4387574a50cf2fcb7b21b6ea5702c777a035664df57cbce02` | **First use: 5.00000000 BTC funded.** 7 inputs from `1EtbTvVB8QTGN4mduSdy7n4cZQm4iYTpQ1` (compressed keys). Change 3.65857304 went back to that address. This was 6 days before the poster was posted in the community chat (#28507, 2019-04-19). |
| 2020-03-24 | 622713 | `a2d2481d57e976db` | Dust, 666 sat (third party) |
| **2020-05-11 20:02:50** | 630001 | `2aa9a4a90be819d5122d70c993280785a0508f163521e7b38cebb4db0b071b13` | **First halving withdrawal.** 2.50000000 BTC to `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`. Mined in the block right after halving block 630000, as announced (#28876). |
| **2024-04-24 21:47:27** | 840725 | `88cdb3cdca12b471551b1b26188508a14ca5fd8a415223ffb7c190381c9b9df3` | **Second halving withdrawal.** 1.25000000 BTC to the same `17ucy1…`. Locktime 840003, so it was built just after halving block 840000. |
| 2023-07 → 2026-08-29 | – | 118 txs | Dust and small deposits only (546–70,000 sat), including a spam burst on 2026-02-24. No further spends. |

- **Current balance:** 1.25635374 BTC in 120 unspent outputs.
- **Creator control:** both withdrawals were signed with the prize key, so the creator still held it in 2024.

## What the spends reveal about the key

- Every input signed by the prize address carries a **65-byte (uncompressed) public key**. That confirms the address is uncompressed.
- If the key is written as WIF, it starts with `5`. It could also be raw 64-hex.
- The original vanitygen and oclvanitygen tools make uncompressed addresses by default; VanitySearch makes compressed ones by default. This supports vanitygen as the tool, but it is an inference.
- The funding wallet `1EtbTv…` uses compressed keys. So it is separate wallet software, and the prize key was generated on its own.

## Linked addresses

- **`1EtbTvVB8QTGN4mduSdy7n4cZQm4iYTpQ1`** (funder)
  - Active from 2014-12-12 to 2026-01-22; 50 txs; 64.8 BTC received in total; now nearly empty.
  - On **2018-01-11** it also funded the cookie-jar vanity address `1GSMG1CLxGXuFtnKbwh1QWfp4xA6reAet3` (0.01337 BTC, tx `f931426c30411640`).
  - That transaction's change output (0.264174 BTC) is one of the inputs to the 2019 prize funding.
  - **The same creator wallet paid both 1GSMG1 vanity addresses.** The cookie-jar address was in use 15 months before the puzzle.
- **`17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`** (halving destination)
  - Holds 3.75055856 BTC, never spent.
  - Its only inputs are the two withdrawals plus dust.
- **`1GSMG1CLxGXuFtnKbwh1QWfp4xA6reAet3`**
  - 3 txs, 0.01347934 BTC, never spent, so its key type is unknown.
