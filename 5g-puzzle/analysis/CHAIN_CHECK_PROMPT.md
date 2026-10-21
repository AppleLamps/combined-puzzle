# Prompt: on-chain checks for the GSMG.IO 5 BTC puzzle

Paste everything below the line into an AI that has working internet / blockchain
API access. Return its full raw output.

---

You have internet access. I need you to pull Bitcoin chain data and analyse it.
Work from primary API responses only. **Do not summarise data away — I need the raw
values.** If an API fails, say so and try the next one; never fill a gap from memory
or from what a block explorer's web page says in prose.

## Background

These two addresses hold/held the prize of the GSMG.IO 5 BTC puzzle, published
January 2019 and still unsolved. The puzzle's own decrypted text says *"the private
keyS belong to half and better half"* — two keys, two holders.

| role | address | hash160 | status |
| --- | --- | --- | --- |
| **Half** | `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` | `a9553269572a317e39f0f518cb87c1a0ee1dbae4` | has **spent**, so its public key is exposed on chain |
| **Better Half** | `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` | `4bc468447fe1b048ad030a2f9a125478eabc4ed6` | has **never spent** |

Half's uncompressed public key, recovered from its spends:

```
04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464
9c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559
```

(That is one value, line-wrapped. Verify it: `hash160(pubkey)` must equal Half's
hash160 above. If it does not, stop and tell me — my source is wrong.)

`1GSMG1` is a **vanity prefix**, so Half's key was found by grinding, not derived
from a passphrase.

Why I am asking: the puzzle's first artefact is a poster whose QR code resolves to
`https://www.blockchain.com/btc/address/1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`.
The creator's most-repeated unsolved hint (2020-01-14) reads *"It might have shown
you only one door, beware that the rabbits nest may contain a whole lot more."*
Everything else in the poster is exhausted — the grid encodes exactly one URL, and
the QR is a clean version-4-L symbol with all Reed–Solomon syndromes zero. So the
open question is whether *the address's transaction history* is the next surface.

## Data to fetch

Use whichever of these work; try more than one and say which you used:

```
https://mempool.space/api/address/<ADDR>
https://mempool.space/api/address/<ADDR>/txs            # paginate with /chain/<last_txid>
https://blockstream.info/api/address/<ADDR>/txs
https://blockchain.info/rawaddr/<ADDR>?limit=100
https://api.blockchair.com/bitcoin/dashboards/address/<ADDR>?limit=100
https://mempool.space/api/tx/<TXID>/hex                 # raw tx hex, needed for check 4
https://blockstream.info/api/tx/<TXID>/hex
```

Do this for **both** addresses.

## Check 1 — vanity or message-bearing output addresses

For every transaction that spends *from* either address, list **every output
address** with its value in satoshis and the block time.

Flag any output address whose leading characters after the `1` look deliberate
rather than random — English words, names, `GSMG`, `SALPHASEION`, `YINYANG`,
`MATRIX`, `NEO`, `RABBIT`, `SEED`, `DOOR`, `PRIME`, `KEY`, and so on. Dust-value
outputs (546–1000 sats) to many distinct addresses is the classic pattern for
pushing a message onto the chain: if you see that, transcribe the addresses **in
transaction output order** and then in block order, and show the concatenated
leading characters.

## Check 2 — OP_RETURN

For every transaction touching either address, report any output with
`scriptpubkey_type == "op_return"`. Give the full hex of the script and its ASCII
and UTF-8 decodings.

## Check 3 — Better Half's funding

Report the transaction(s) that funded `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` in full:
inputs, all outputs, values, block height, block time, and the funding address.
Note anything unusual about the output structure — an odd count, equal-value
outputs, non-standard scripts, or a value that reads as a number rather than a
round amount.

## Check 4 — ECDSA nonce reuse across Half's spends

This is the one check that could recover a key outright. Old wallets sometimes
reused the signature nonce `k`, which leaks the private key. It is a soundness
check on whether the prize is even still safe — I expect it to come back clean,
because a reused nonce on a 2019 address would have been drained by bots years ago.
Report the null clearly if that is what you find.

Method:

1. Fetch the **raw hex** of every transaction that spends from Half.
2. For each input, parse the `scriptSig`: it is `<DER signature + sighash byte>
   <pubkey>`. Extract `r` and `s` from the DER structure.
3. Report every `(txid, input index, r, s, sighash type)` as hex.
4. **Group by `r`.** If any two signatures made by the same public key share an
   `r`, the nonce was reused and the key is recoverable:

   ```
   k = (z1 - z2) * inverse(s1 - s2)  mod n
   d = (s1 * k - z1) * inverse(r)    mod n
   n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
   ```

   where `z` is the sighash of each input as an integer (compute it properly:
   BIP143 does not apply, these are legacy P2PKH inputs, so `z` is the
   double-SHA256 of the serialised transaction with that input's scriptSig replaced
   by the previous output's scriptPubKey and all other scriptSigs emptied, plus the
   4-byte sighash type appended).
   Try both `(s1 - s2)` and `(s1 + s2)` for the sign ambiguity.
5. If you recover a candidate `d`, verify it before reporting: derive the public
   key and check `hash160` equals Half's hash160 above. **Do not report an
   unverified candidate.**

## Also report

- Current balance and total received/sent for both addresses, in satoshis.
- The full transaction list for both, oldest first: txid, block height, block time
  (UTC), total in, total out, fee.
- Whether either address has any transaction after 2019 that is *not* simply the
  original funding.

## Discipline — this matters

This puzzle has burned seven years of solvers on coincidences, and I have already
had to throw out several apparent findings in this investigation for exactly this
reason. So:

- **Separate what the API returned from what you infer.** Quote the raw values.
- Do not call something a message because it contains a readable substring. Base58
  addresses are 34 characters over a 58-symbol alphabet; short English fragments
  appear in random addresses constantly. If you flag a vanity address, say how many
  leading characters are non-random and give the rough odds.
- If a check comes back empty, **say it came back empty.** A clean null is a useful
  result here and I would rather have it than a stretched positive.
- Do not guess at data you could not fetch. Name the endpoint that failed.
