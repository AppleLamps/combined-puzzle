# The on-chain checkpoint oracle

Rewritten 29 September 2026. The 19 September edition called the checkpoint set closed and said the trail stopped in April 2020. Doc 113 found that the oracle address signed transactions until 2021-07-18 and that every later message is inbound, and the checkpoints were paid on 2020-03-24. This edition carries those corrections. The transaction-by-transaction table is in `07-onchain-facts.md`, and the keys and addresses are in `04-key-material.md`.

A checkpoint check needs no website and cannot rot. It gives a signal on a single candidate value, where the live verifier needs a whole password to be right at once.

## The filter

Take `sha256(phrase)` as a private scalar and derive the compressed-key P2PKH address. A real checkpoint address carries an OP_RETURN that begins `GSMG.io:`, sent by the oracle address `3GSMG24TujqfMJG1kQoBX18DzJHQLeJYMK`.

Checking for on-chain activity alone gives false positives, because brainwallet sweeper bots touch any phrase anyone has used. The literal string `matrixsumlist` derives to `1BM4GJpBLs45Je589ZH426T2FUqBRyZPF3`: two transactions (1,200 sat received on 2026-01-18, swept an hour later) and no OP_RETURN. That is a bot. The OP_RETURN is the discriminator.

Controls, all run live on 29 September 2026:

| phrase | address | result |
|---|---|---|
| `causality` | `1Jqq37KkZEt4F3Dt6qXdtyiMEFBBdawbkJ` | `GSMG.io: Right, this is causality` (14 transactions) |
| `theflowerblossomsthroughwhatseemstobeaconcretesurface` | `1AD2wfwXukZ1kUAy848hTQQ72aSBZPB75r` | `GSMG.io: are you sure?` (12 transactions) |
| `matrixsumlist` | `1BM4GJpBLs45Je589ZH426T2FUqBRyZPF3` | none (sweeper bot) |
| two arbitrary strings (`notaphrase1`, `notaphrase2`) | `1LthYJkLak...`, `1KwEBQBK9t...` | none |

## The set

Six checkpoints exist. All were paid by the oracle address on 2020-03-24, in blocks 622762 to 622774, and every preimage is known:

| block | OP_RETURN | preimage |
|---:|---|---|
| 622762 | `do you beleive me you need it?` | the address string `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` itself |
| 622762 | `Right, this is causality` | `causality` |
| 622766 | `part of the cipher` | the 149-digit phase-3.2.2 checkerboard input |
| 622767 | `phase3.2 pass OK` | the 62-byte unspaced phase-3.2 answer |
| 622767 | `are you sure?` | the phase-1 answer |
| 622774 | `You are here because 227 chars were correct` | the 227-character phase-3 answer |

The addresses are in `04-key-material.md`. The set was enumerated from the complete history of the oracle address (30 transactions, 14 signed by its key), so paging cannot have missed a checkpoint. A message-text filter alone would have missed two signed payments: the 1,050 sat payment to `1NULY7Dhzu...` in block 624768 has no OP_RETURN (it is a tip address of a kangaroo tool), and the two `Good job, Neo!` messages do not start with `GSMG.io:`. The two `Good job, Neo!` addresses are poster checkpoints: their keys come from the poster URL, so they are not targets, and anyone can send from them.

After 2020-03-24 the oracle signed the `Good job, Neo!` payments (2020-04-03), the tip payment (2020-04-07), `Halving` (2020-05-11) and `GSMG.io neighbors, half and double` (2021-07-18). None of these is a phrase checkpoint. Everything later is inbound from other keys (`07-onchain-facts.md`), so it says nothing about the puzzle's answers.

**Consequence.** No unsolved checkpoint exists. The last phrase checkpoint is the 227-character answer, which is the phase 3 answer. The oracle confirms a value you already hold and cannot lead to one. A future candidate for `matrixsumlist` or `lastwordsbeforearchichoice` can still be checked against it at no cost, but it fires only if the oracle's operator happened to checkpoint that intermediate, and nothing was checkpointed after phase 3.2.

The oracle reads as an early solver's ledger. The creator replied "Correct" (#12653) to the statement that the blockchain messages are not his and not part of the puzzle, and doc 113 lists the evidence on each side.

**The other verifier.** `gsmg.io/phase1verification` is live and discriminating, but it validates only the phase-1 answer: `causality`, the 227-character answer and the 62-byte answer are all rejected (dossier section 1, doc 63). Together the two oracles confirm known values and lead to none. That is the complete verification surface of the puzzle.

## Reusable code

The code below is tested: the offline control `address_of('causality') == 1Jqq37KkZEt4F3Dt6qXdtyiMEFBBdawbkJ` passes, and the live controls above return the results in the table. It needs `coincurve` and network access to mempool.space. Rate-limit to about one request per second, which makes it practical for hundreds or a few thousand candidates. Screen candidates offline first. For a scalar that is not a phrase hash, use the win test in dossier section 1 instead.

```python
import hashlib, json, time, urllib.request
import coincurve

B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def b58check(payload):
    data = payload + hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    n = int.from_bytes(data, 'big')
    s = ''
    while n:
        n, r = divmod(n, 58)
        s = B58[r] + s
    return '1' * (len(data) - len(data.lstrip(b'\0'))) + s

def h160(b):
    return hashlib.new('ripemd160', hashlib.sha256(b).digest()).digest()

def address_of(phrase, compressed=True):
    """P2PKH address of the key sha256(phrase)."""
    priv = hashlib.sha256(phrase.encode()).digest()
    pub = coincurve.PrivateKey(priv).public_key.format(compressed)
    return b58check(b'\x00' + h160(pub))

def get(url):
    for _ in range(4):
        try:
            return json.load(urllib.request.urlopen(url, timeout=30))
        except Exception as e:
            err = e
            time.sleep(2)
    raise err

def gsmg_checkpoint(addr):
    """Return the GSMG.io: OP_RETURN text if this address carries one (a real
    checkpoint), else None. Pages through all confirmed transactions, because
    later dust pushes the 2020 message off the first page of 25."""
    last = None
    while True:
        url = 'https://mempool.space/api/address/%s/txs' % addr
        if last:
            url += '/chain/%s' % last
        page = get(url)
        for t in page:
            for o in t['vout']:
                if o.get('scriptpubkey_type') != 'op_return':
                    continue
                for p in o.get('scriptpubkey_asm', '').split():
                    if len(p) >= 8 and all(c in '0123456789abcdef' for c in p):
                        try:
                            s = bytes.fromhex(p).decode('utf-8')
                        except Exception:
                            continue
                        if s.startswith('GSMG.io:'):
                            return s
        if len(page) < 25:
            return None
        last = page[-1]['txid']
        time.sleep(1)

if __name__ == '__main__':
    assert address_of('causality') == '1Jqq37KkZEt4F3Dt6qXdtyiMEFBBdawbkJ'   # offline control
    for phrase in ['causality', 'theflowerblossomsthroughwhatseemstobeaconcretesurface',
                   'matrixsumlist', 'notaphrase1', 'notaphrase2']:
        a = address_of(phrase)
        print(phrase, a, gsmg_checkpoint(a))
        time.sleep(1)
```

The EC-neighbour hash160s (`P-G`, `P+G`, `P/2`, `2P`) are in `04-key-material.md` and in the win test. A derived scalar one step from the prize scalar would hit one of them and miss the prize.
