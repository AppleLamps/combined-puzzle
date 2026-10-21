# On-chain facts

Historical tables in sections 1–4 are as of 29 September 2026, when their figures were pulled from mempool.space and checked against transaction data. Section 5 records a separate 6 October 2026 check. Machine-readable forms: `keys.json` (addresses and balances) and `message-sequence.json` (the May 2026 sequence).

**Authorship.** These are facts about data that exists on the Bitcoin blockchain. On 29 August 2023 the creator answered "Correct" (#12653) to a general statement that blockchain messages were not his and not part of the puzzle. That reply predates later 2025/2026 texts and is not a specific denial of them. The text exists and can be read. Its author is unproven, and a message sent from a key that anyone can compute proves nothing about the sender.

## 1. The oracle address `3GSMG24TujqfMJG1kQoBX18DzJHQLeJYMK`

Thirty transactions touch it. Fourteen spend an output of the address, so its key signed them. Sixteen are inbound: other keys paid it and attached messages. Balance 21,128 sat.

| block | date | txid | class | OP_RETURN | what it does |
|---:|---|---|---|---|---|
| 622711 | 2020-03-24 | `1f8eb99e2da7b573` | inbound | none | funding: 15,000 sat from `37mh7EYet...` |
| 622759 | 2020-03-24 | `8ee72f469561c85c` | signed | none | staging: splits the balance into five outputs to itself |
| 622762 | 2020-03-24 | `0ba2a2e2d5255bc9` | signed | none | staging: three outputs to itself |
| 622762 | 2020-03-24 | `117e2796e6c1ab36` | signed | `GSMG.io: Right, this is causality` | 1000 sat to `1Jqq37KkZE...` (`causality`) |
| 622762 | 2020-03-24 | `3891dd146dce36ed` | signed | `GSMG.io: do you beleive me you need it?` | 1000 sat to `1GyT5WrLYp...` (sha256 of the prize address string) |
| 622766 | 2020-03-24 | `496ab2c73a15ce53` | signed | `GSMG.io: part of the cipher` | 1000 sat to `18CchrjA3U...` (the 149 digits) |
| 622767 | 2020-03-24 | `2f64b8758f97eb5b` | signed | `GSMG.io: phase3.2 pass OK` | 1000 sat to `1K23RS1y2f...` (the 62-byte phase-3.2 answer) |
| 622767 | 2020-03-24 | `bd1b5d81b3eab6d8` | signed | `GSMG.io: are you sure?` | 1000 sat to `1AD2wfwXuk...` (the phase-1 answer) |
| 622774 | 2020-03-24 | `62dbb701ee67c3f4` | signed | `GSMG.io: You are here because 227 chars were correct` | 990 sat to `1M5ypvDbp1...` (the 227-character answer) |
| 622832 | 2020-03-24 | `547246e9fec52847` | signed | none | staging: six outputs to itself |
| 624209 | 2020-04-03 | `364de511fda4a139` | signed | `Good job, Neo!` | 1000 sat to `148XH2YBmL...` (poster URL as a key) |
| 624209 | 2020-04-03 | `722fbf3507b025e7` | signed | `Good job, Neo!` | 1000 sat to `13HGhjkmKU...` (poster URL bits reversed as a key) |
| 624768 | 2020-04-07 | `d6ff3da13c67f8e7` | signed | none | 1,050 sat to `1NULY7Dhzu...`, no OP_RETURN (kangaroo-tool tip address) |
| 630001 | 2020-05-11 | `a798905f53fdcadc` | signed | `Halving` | 700 sat to the prize address, same block as the 2.5 BTC halving transfer |
| 691562 | 2021-07-18 | `e5db0968fdaed768` | inbound | none | funding: 21,048 sat from `bc1q5rs27kn...` |
| 691563 | 2021-07-18 | `a82052a216cad8f5` | signed | `GSMG.io neighbors, half and double` | 5000 sat each to the addresses of P-G, P+G, P/2 and 2P |
| 876734 | 2024-12-28 | `097a0806a714b673` | inbound | none | dust, 2,870 sat from `bc1qz5jznn...` |
| 887683 | 2025-03-13 | `8d8497ece6ca166f` | inbound | `BULLSHIT` | 600 sat from `3JC6NJz2vX...` |
| 897169 | 2025-05-17 | `f77d6b4a3a05446b` | inbound | `From Neo` | 1000 sat, sent from `13HGhjkmKU...` (poster key) |
| 897360 | 2025-05-19 | `8aaa96d3a945cf74` | inbound | `Neo wallet bc1qyw9qv8qntl48rqdfa4g5szzrlaq4d4cn6zhrmg` | 666 sat, sent from `148XH2YBmL...` (poster key) |
| 901814 | 2025-06-18 | `557d13006666cd4e` | inbound | `Yes` | 600 sat, sent from `1AD2wfwXuk...` (checkpoint key) |
| 901814 | 2025-06-18 | `5b7a4390523ea4e2` | inbound | `Yes` | 600 sat, sent from `1GyT5WrLYp...` (checkpoint key) |
| 904113 | 2025-07-05 | `3ed3932f6629fd0a` | inbound | `Its in good hands with Gavin and everyon.` | 1000 sat from `1BaCkUvsep...` |
| 904971 | 2025-07-10 | `b9d1b0e9f5a6c9c6` | inbound | `Happy late mothers day!` | 546 sat from `1ECSdS4YGu...`; the transaction also pays 546 sat to the prize address |
| 911590 | 2025-08-25 | `a4d1f5fbe980a800` | inbound | `I thought choice was an illusion?` | 546 sat from `16RGFo6hDt...` |
| 944115 | 2026-04-08 | `38162e4fd40822d3` | inbound | none | dust, 2,600 sat from `1Kv59xvBVG...` |
| 944115 | 2026-04-08 | `6c543613d42b32b3` | inbound | none | dust, 2,600 sat from `1KY3yqm9CG...` |
| 946416 | 2026-04-24 | `7aed1985a0d5fe30` | inbound | none | dust, 2,500 sat, sent from `148XH2YBmL...` (poster key) |
| 946416 | 2026-04-24 | `e6b79a146e9e1707` | inbound | none | dust, 2,500 sat from `bc1qmegut04...` |
| 946416 | 2026-04-24 | `f675e8f87159e088` | inbound | none | dust, 2,500 sat, sent from `13HGhjkmKU...` (poster key) |

Reading the table:

- **The signed set runs from 2020-03-24 to 2021-07-18.** It holds six `GSMG.io:` checkpoints (blocks 622762 to 622774, all on 2020-03-24), two `Good job, Neo!` payments, one unlabelled payment, the `Halving` marker and the neighbours payment.
- **The staging transactions** (blocks 622759, 622762 and 622832) split the balance into outputs of about 1,200 sat that the checkpoint payments then spent.
- **Every checkpoint preimage is known** (`04-key-material.md`). The oracle confirms a value you already hold and cannot lead to one.
- **The `Good job, Neo!` addresses are poster checkpoints.** Their keys are computable from the poster URL (`04-key-material.md`), so the 2025 messages `From Neo` and `Neo wallet ...`, sent from those keys, are unauthenticated.
- **The 1,050 sat payment in block 624768** goes to the hard-coded tip address of alek76's GPU Pollard-kangaroo tool. That tool's first commit containing the tip line is dated 2020-04-05 00:41 UTC, about 51 hours before the payment (git history, doc 113; not re-checkable from this project).
- **The `Halving` message** was sent in block 630001, the block that carried the 2.5 BTC move to `17ucy...`.
- **"neighbors, half and double"** funded the four elliptic-curve neighbours of the prize public key (`04-key-material.md`).
- **Everything after block 691563 is inbound.** The two `Yes` messages were sent from the checkpoint keys of the phase-1 answer and of the prize address string, which anyone can compute. `BULLSHIT`, `Its in good hands with Gavin and everyon.`, `Happy late mothers day!` and `I thought choice was an illusion?` came from four other addresses (see the table).

## 2. Other messages sent from the public checkpoint keys

- Block 897195 (2025-05-18): `SalPhaseIon sumlist AES`, in a transaction signed by `13HGhjkmKU...` (1000 sat to `3HX5tttedD...`).
- Block 903635 (2025-07-02): an unrelated address (`16DUcZT3T6...`) paid 546 sat to eight addresses, seven of them checkpoint or poster addresses, with the message `Its in good hands with Gavin and everyone...`. The same block holds a transaction that spent the dust on six of those addresses (`13HGhj...`, `148XH2...`, `1AD2wf...`, `1GyT5W...`, `1K23RS...`, `18Cchr...`) to one destination, so whoever signed it holds those six keys, all of which anyone can compute.

## 3. `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` and the 2026 batches

`17ucy...` has never spent an output (45 transactions, all inbound), so it cannot be the sender of anything. Its two 2026 OP_RETURN batches (blocks 938165 and 944096) sit in transactions that pay it 546 sat of dust and were sent by two dust bots. The payloads, the bots' addresses and the tests run on them are in dossier section 1.

## 4. The May 2026 vanity-address sequence

The vanity address `1GSMG9VDLTU6jyuG7bkNMdmnHBLtbbM51M` (public key `04d3b822...`, independent of the prize key) was funded with 20,000 sat by `11111119536NnU2vPAvoQhvkheQ8ejYJ`, a dust recipient, and every message it inscribed pays 546 sat of dust to that address, except the WITNESS message, which pays its dust to the prize address. Each transaction spends the change of the one before it, so the spend chain fixes the order even though five of them share block 949574. Earlier versions of `message-sequence.json` listed `hereismysecret` before `yourlastcommand` and `GSMGBH` before `GSMGJH`; the order below is the chain order.

| order | block | time (UTC) | txid | content |
|---:|---:|---|---|---|
| 0 | 949573 | 2026-05-15 22:40:29 | `0b609ab380f1aba7` | funding, 20,000 sat from the dust-witness address, no OP_RETURN |
| 1 | 949574 | 2026-05-15 22:48:51 | `e430715b19eaf3aa` | `leavethematrix` |
| 2 | 949574 | 2026-05-15 22:48:51 | `5132c90023baa686` | `yourlastcommand` |
| 3 | 949574 | 2026-05-15 22:48:51 | `80a8dde46584c801` | `hereismysecret` |
| 4 | 949574 | 2026-05-15 22:48:51 | `cd415b951ea1bc3e` | `isolveditwithanabacus` |
| 5 | 949574 | 2026-05-15 22:48:51 | `6b4e2cb8f8d3099c` | `secondanswer` |
| 6 | 949653 | 2026-05-16 12:15:28 | `808f812f13a3137e` | `GSMGJH` binary payload, 64 bytes (after a 0x20 separator byte) |
| 7 | 949653 | 2026-05-16 12:15:28 | `22381b6013973fed` | `GSMGBH` binary payload, 65 bytes |
| 8 | 949664 | 2026-05-16 13:13:13 | `973646bb3204b9e6` | `GSMG WITNESS BLK 949653 TX 808f812f` |
| sweep | 961334 | 2026-08-06 20:34:00 | `112ceccab20bb32a` | sweep of the remaining balance, no OP_RETURN |

The two payloads are in `payload-gsmgjh.txt` and `payload-gsmgbh.txt`. What was established about them:

- **GSMGBH (65 bytes)** is consistent with a Bitcoin compact signature at about 6 bits of evidence: header `0x1f` (compressed key, recovery id 0), `r` and `s` below the curve order, `s` canonical-low. Random 65 bytes clear all three with probability about 1.6%.
- **GSMGJH (64 bytes)** is not classifiable. It is not a curve point as `x||y` (x lifts, the given y does not match). It is a canonical `(r, s)` pair, but random 64 bytes are canonical about half the time, so that carries no evidence. The "headerless signature" reading is withdrawn.
- **Recovery test (doc 59 section 6):** signature recovery over 41 messages, three hash conventions and four recovery ids against 12 known GSMG addresses, with a self-signed control that fired at recovery id 0: 2,160 recoveries, 0 matches. Reuse of the prize key's six known `r` values as nonces was tested and is null.
- **Provenance:** GSMGBH does not appear in the chat export. GSMGJH appears only in a solver's message (#71393, 2026-09-09). The vanity prefix does not authenticate the sequence. The word "abacus" in the fourth message is no evidence of a method.


## 5. The “it myself 140 investment” transaction (checked 6 October 2026)

[Transaction 2b6f8b68f6174e432a2cdd33ce1e46d365e4cef3a51272432baf35fed86bb449](https://mempool.space/tx/2b6f8b68f6174e432a2cdd33ce1e46d365e4cef3a51272432baf35fed86bb449),
block 898064, 23 May 2025, contains the literal OP_RETURN text
`it myself 140 investment`. Script:
`6a186974206d7973656c662031343020696e766573746d656e74`.
It pays 70,000 satoshis to the community donation address listed in the
[community repository](https://github.com/puzzlehunt/gsmgio-5btc-puzzle/blob/master/README.md).
The text exists; creator authorship or endorsement is not established. The 2023
denial above cannot specifically authenticate or refute this later transaction.
No 140-fold investment rule follows from it. See [doc 119 §6](claude/119-current-evidence-ledger.md#6-hundred-fourty-and-the-genesis-source).
