# BSV history of 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe: funding trace (2026-10-08)

Historical read-only checks reported on 2026-10-08 against WhatsOnChain.
Correction on 2026-10-09 used existing local records only: no new chain fetch,
transaction, signing operation, or Telegram-embedded link access occurred.

## Evidence recovered and verification limits

Six decoded public transaction JSON records were recovered from the original
session scratchpad and copied byte-for-byte to `evidence/bsv_*.json`.
[evidence/bsv_manifest.json](evidence/bsv_manifest.json) records source filenames,
full txids, and SHA-256 hashes. Tests parse their saved OP_RETURN script hex and
compare the relevant prevout/change scripts. All preserved Memo scripts are checked end-to-end: Send money has exactly the two-byte tag, 20-byte recipient hash, and message (at most 194 bytes); Like/tip has exactly the two-byte tag and 32-byte transaction reference. The tests check every push length and consume the complete script, including OP_FALSE OP_RETURN and PUSHDATA1 for the blob. These are checks of a saved explorer
response, not independent full serialized-transaction, signature, token-state, or
chain-inclusion validation. Balances and history totals below remain historical
reports; the six address transactions are not a pagination proof.

Verified integer conversions: `9325.to_bytes(2, 'little') = 6d24` and
`1133.to_bytes(2, 'little') = 6d04`. The [Memo protocol](https://memo.sv/protocol)
defines these as **Send money** and **Like / tip memo**. The recovered scripts
contain those exact pushed bytes, so these are not unidentified mystery markers.
`5262419.to_bytes(3, 'little')` gives ASCII **SLP**, and
`1145980243.to_bytes(4, 'little')` gives **SEND**. The saved token script pushes
`534c5000` (`SLP` followed by NUL) and `53454e44` (`SEND`); the ASM decimal omits
the leading numerical zero represented by that terminal NUL byte.

## Public checkpoint attribution

The full address is `1GyT5WrLYpwFkuiVoPDJZa1Q6jtjbjuBff`. It is derivable from
SHA256 of the public target-address string, interpreted as a scalar, using the
compressed public-key P2PKH form. The existing BTC record
`mywork2/web/gsmg_txs.json` index 25, txid
`3891dd146dce36ed7f97e5476aa3cd427ebc9a8535ce6353b72309b28e686ced`, records a
1,000 sat payment to it with `GSMG.io: do you beleive me you need it?`.

A truncated `1GyT5...` label alone did not establish equality. Recovered local
records now show `7ea6eb76...` spending `b7611598...:2`, whose saved P2PKH output
is this exact checkpoint; `7ea6eb76...:2` returns change to the same script.
This verifies equality within those saved records, while independent on-chain
validation remains unperformed. A publicly derivable checkpoint cannot prove
exclusive creator control or authenticate the sender as the creator.


Address history (6 txs): heights 896117, 896121, 898879 (x3), 968354. Confirmed balance 100,001,215 sat. Address is the puzzle hash160 `a9553269…`, scriptPubKey `76a914a9…88ac`.

## Correction

The previous table said `7ea6eb76…` pays "1 sat" to `1GSMG…`. It pays **100,000,000 sat (1 BSV)**. The earlier print rounded the value. Fee is 300 sat (input 100,026,145, outputs 100,025,845).

## Reported block 968354 (blocktime 2026-09-25 19:35 UTC; corrected 2026-10-14 from 2026-09-24)

Read backward from the puzzle address:

| Tx | Inputs | Outputs | OP_RETURN |
|---|---|---|---|
| `7ea6eb76…` | `b7611598…:2` (100,026,145) | 100,000,000 to `1GSMG…`; 25,845 change to `1GyT5…` | `9325` + target hash160 + "100,000,000 satoshis (100,000,000 BSV)" |
| `b7611598…` | `4da81727…:2` | 666 sat to `1DLt5…`; 100,026,145 to `1GyT5…` | `9325` + `1DLt5` hash160 + "THEMATRIXHASYOU" |
| `4da81727…` | `44d8935d…:2` | 1,000,000 sat to `1FR2JT9…`; 100,027,088 to `1GyT5…` | `9325` + `9e1cd479…` + "recharge" |
| `44d8935d…` | `6279e05b…:2` | 50,000 to `1NkfYu…`; 101,027,358 to `1GyT5…` | `1133` + `0004938e…` |
| `6279e05b…` | `f26508a7…:0` | 25,000 to `1DLt5…`; 101,077,631 to `1GyT5…` | `1133` + `108a9813…` |
| `f26508a7…` | `e7992114…:0` | 101,102,904 to `1GyT5…`; 25,030,371 to `132SjH…` | none |

Only `7ea6…` pays the puzzle address a large amount (1 BSV). The other large outputs in this block go to `1GyT5…` and `132SjH…`.

Observations:
- The saved subset shows `1GyT5…` used as a relay/change address. It is the public checkpoint described above; this is a behavioral observation, not owner identification.
- The saved `7ea6…` input references the checkpoint output in `b761…`; this establishes the recorded source output, not the identity of the person making the payment.
- `9325` tags appear in `7ea6…`, `b7611598…`, `4da81727…`, and in the May 2025 transactions below. `1133` appears in `44d8…` and `6279…`.
- The same block has `1DLt5…` receiving small outputs from several txs.

## May 2025 chain (heights 896117–898879)

| Tx | Height | Inputs | Outputs | OP_RETURN |
|---|---|---|---|---|
| `816fccdb…` | 896117 | `9d56a8be…:1`, `9d56a8be…:3` | 546 to `1JHYLp…`; 546 and 12,517 to `1DLt5…` | `5262419`, `1`, `1145980243`, `9d56a8be…` (decodes to ASCII "SLP" and "SEND") |
| `0af0d4c6…` | 896117 | `816fccdb…:2`, `816fccdb…:3` | 546 to `14xtCa…`; 546 and 11,489 to `1DLt5…` | same "SLP SEND" tag structure |
| `1f542bbe…` | 896117 | `0af0d4c6…:2`, `0af0d4c6…:3` | 546 to `1GSMG…`; 546 and 10,461 to `1DLt5…` | "SLP SEND" structure again (from the earlier decode) |
| `fb1cfdd0…` | 896119 | `1f542bbe…:3` | 546 to `1JHYLp…`; 9,605 to `1DLt5…` | `9325` + `bd9af4de…` + "My yo" |
| `bc7d915b…` | 896121 | `fb1cfdd0…:2` | 666 sat to `1GSMG…`; 8,484 to `1DLt5…` | `9325` + target hash160 + 192-byte blob (not decoded) |
| `451c20ce…`, `caf09a70…`, `7b1c1915…` | 898879 | chain of 1-sat outputs | 1 sat to `1GSMG…`; 0.33 BSV to `14mzuL…` | "Push-The-Button.app \| Lambda" |

Note: the May 2025 outputs to `1GSMG…` are dust (546 to 666 sat). The only large amount sent to `1GSMG…` is the 1 BSV in `7ea6…` (September 2026). The `9325` + target hash160 tags are on `bc7d915b…` (blob) and `7ea6…` (text).

## Follow-up traces

**`9d56a8be…` (reported height 896117): saved token-genesis record.** Its OP_RETURN has `SLP\0` / `GENESIS` fields: action "GENESIS", name "Bitcoin SV", symbol "VSB", 8 decimals, supply 2,100,000,000,000,000 base units (21,000,000 tokens), and a text link to memo.sv (not opened). Its outputs go to `1DLt5…`, and the later `SLP SEND` transactions (`1f542bbe…` and others) move dust-sized token outputs to `1GSMG…` and other addresses. These fields support a token-protocol interpretation. Token validity and any puzzle meaning have not been established; a protocol label alone does not rule out an accompanying message.

**`e7992114…` (height 968328) and the input chain:**
- `d367e46d…` (height 967897, 2026-09-21) is a coinbase transaction (block reward). Output 1 (175,942,077 sat) goes to `1k4tYE…`.
- `e7992114…` spends `d367e46d…:1`. It sends 126,133,500 sat to `132SjH…` and 49,808,434 sat to `1k4tYE…`.
- `f26508a7…` (block 968354) spends `e7992114…:0`. It sends 101,102,904 sat to `1GyT5…` and 25,030,371 sat back to `132SjH…` (its balance now).
- This branch goes back to a block reward. The 1 BSV that reached the puzzle address passed through `132SjH…` and `1GyT5…`, but `1GyT5…` also has other inputs (`44d8935d…`, `6279e05b…`, `4da81727…`), so the full origin of that 1 BSV is not established.

**`132SjH…`:** earlier check reports two observed transactions and balance 25,030,371 sat. Complete history is not established here.

**`1k4tYE…`:** balance 2,476,735,839 sat (24.77 BSV). Its history shows activity in blocks 969306–970159, after the trace. Not traced further; its full history was not counted.

**`1NkfYu…`:** balance 94,197 sat, 66 transactions. It received 50,000 sat from `44d8935d…`. Its older history (from block 898963) was not traced.

## Blob record and bounded claims

The recovered `bc7d915bfb67e10c13b8530959727938f07bcb6db1be0a115e6fff430b4887e3`
record's output 0 is `OP_FALSE OP_RETURN`, followed by pushes for `6d24`, the
20-byte target hash160, and a `PUSHDATA1 c0` payload. Parsing that saved script
confirms **192 payload bytes, 83 UTF-8 characters, and 24 distinct symbols**,
with no whitespace. Payload SHA-256:
`0fc9fef5cb79891c52feae29c2b13b1f010070c18bad696e84cb3146fea0ed0d`.
The text includes box-drawing, punctuation, degree signs, and Cyrillic characters;
UTF-8 decoding succeeds but does not by itself recover intelligible plaintext.

The previous narrative claimed zlib/gzip/base64, single-byte XOR/add/subtract,
code-point shifts, legacy code pages and reversal tests had produced no readable
result. No corresponding scripts, parameters, scores, or output logs were found
in the recovered scratchpad. Those experiment claims remain **unverified and
unreproduced**. No such search was rerun. Neither the narrative nor the dimensions
establish exhaustive exclusion, a particular cipher, or that the text cannot be
solved. The raw payload is now preserved so a separately authorized bounded
experiment could be reproduced later.

The protocol markers and public checkpoint link are identified. The authorship,
meaning of the blob, token validity, and ultimate funding provenance remain open.
