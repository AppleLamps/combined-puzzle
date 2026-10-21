# GSMG.IO 5 BTC PUZZLE: COMPLETE DOSSIER

Primary data, sourced derivations, creator statements with their contexts, and
documented negative families are collected here. Facts, interpretations and
incomplete execution records are distinguished; only the prize key confirms a win.

Current as of 26 September 2026, incorporating records through 130 and the saved-format review.
**Unsolved: all three authenticated containers remain locked; no prize key recovered.**
Latest completed follow-up: the six-row selector test.
The list [41,56,48,40,48,47] yielded no coherent instruction or exact gate hit
under eight fixed direct word-index readings of the pre-door Architect speech.
Six distinct selections and 24 forms are retained; no AES or address derivations.
These readings are completed exclusions, not an untested next move.
Latest supplied clue: the reported number pairs.
The existing 84-cell replacement model gives used yellow/blue prime sums 317/557;
native poster pixel (317,557) is #FEFEFE. Its prime-zeroed a=0..i=8 values in a
6×14 matrix give alternating row totals 137/143. These are exact witnesses for
the user's screenshot, not an opened door or unique proof of the second operation.
This revision corrects earlier interpretation and coverage claims in place, incorporates
attempts 111–122 and 128–130, reviews 123–126, and the saved-format/exclusion review.
It preserves primary data. Section 14 indexes the records; section 16 explains
integration 127 and section 17 the latest review. Section 15 is historical.

The source material and summaries are self-contained here. Exact candidate membership,
settings and retained outputs for each attempt are summarised here rather than
reproduced in full. Some original historical matrices remain missing, so this is not a complete per-attempt
execution inventory. The user's standing requirement is **do not repeat already tried
work**. A missing record is not proof that a combination is new.

---

## 0. HOW TO USE THIS DOCUMENT

Read section 1 for the goal and the win test. Section 3.A is the song that the
puzzle is built on. Sections 2 to 7 are the primary material. Section 8 is what the
creator said, paired with what he was answering. Section 9 is the current model of
how the puzzle is built. Section 10 is everything that has been tried and failed,
which is the most valuable part, because the failure modes are expensive to
rediscover. Section 11 is methodology learned the hard way. Section 12 is where it
stands and what to do next.

Six warnings before you start.

**A null is only as good as its control.** State what the control was and confirm
it fired. This project once published a dead-route verdict whose own positive
control had failed.

**A null must sample the class of outcome, not the specific one.** If your test
statistic names the answer you found, it measures nothing. This project published a
1-in-200,000 result that was really 1-in-500 because the null held the first word
fixed. That retraction is section 11.

**The exact win test is free and silent.** It never tells you that you are close.
Do not read a long run of negatives as evidence of proximity or distance.

**Read every creator line with the message it answers.** Several hints in earlier
editions were catalogued without their parent message and were misread as a result
(section 8.1). The Telegram export carries reply links; use them.

**Do not assume the locked plaintext is text.** The creator already hid an EBCDIC
block inside phase 3.2, which is only 59% printable. A recogniser that accepts only
printable output at pad 1 or 2 is blind to the most likely non-text plaintexts
(section 2, doc 110).

**Do not repeat completed work.** Compare exact password bytes, full settings and
target digest with recorded identities before execution. Reuse saved plaintexts
when changing a recognizer. Uncertain historical overlap must remain explicit.

---

## 1. THE GOAL AND THE WIN TEST

Find the private key controlling:

    1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
      HASH160       a9553269572a317e39f0f518cb87c1a0ee1dbae4
      uncompressed  04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a46
                    49c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559
      compressed    03f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464

**This is the only puzzle target.** The address has spent twice, so its public key
is exposed, and recovering the private key behind that exposed public key is what
the puzzle is for.

**The working objective is opening the three locked containers** (section 6.5).
Their plaintext may contain a key or a further instruction. Each actual test must
record its selected target, profile and validator; a structural check is not an
unlock attempt.

On-chain balances and spend counts below are historical observations carried from
the earlier dossier. They were not refreshed during this documentation update.

A second address is carried in the test as a sentinel:

    17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa
      HASH160 4bc468447fe1b048ad030a2f9a125478eabc4ed6

**`17ucy...` is not an established puzzle output.** It is the destination of the two halvings,
and the chronology is on chain:

    2019-04-13  block 571,497   prize address funded with 5 BTC
    2019-04-20                  Telegram group opens; first code already cracked
    2020-05-11  block 630,001   2.5 BTC to 17ucy..., nLockTime 629,998
    2024-04-24  block 840,725   1.25 BTC moved,      nLockTime 840,003

The locktimes are close to, but not equal to, halving heights 630,000 and
840,000. They constrain finality; they do not prove when either transaction
was signed. The repeated halving pattern suggests deliberate timing, not a
private-key range. `17ucy...` was first funded on 2020-05-11, while the phase-3.2
envelope containing the "half and better half" message was in chat roughly 30 hours
before block 630,000. The message predates the address; the label was applied to the
address afterwards. Balances on 2026-09-21 were 1.25635374 BTC at the prize address
and 3.75055856 BTC at `17ucy...`. That address has **never been spent**, so its public
key is not exposed. Keep it in the test as a free safety net. Do not treat it as a
goal: the Architect text says `TAKETHEPRIVATEKEY`, singular, and the creator answered
"a private key", singular, when asked directly (#4624).

Transaction `a82052a216cad8f57dee2a039c3b5cef9b5fcb2bc1c3bffa94d713cee0b30e2b`,
funded by the unattributed address `3GSMG24TujqfMJG1kQoBX18DzJHQLeJYMK`,
is in block 691,563 and carries `GSMG.io neighbors, half and double` in OP_RETURN
and sends 5,000 sats each to four uncompressed P2PKH addresses. Let `P=kG`
be the exposed prize public point. Direct secp256k1 point arithmetic gives:

| Relation | Address | Candidate scalar if `k` is prize scalar |
| --- | --- | --- |
| `P-G` | `1G1kRAFR68y6CUq1SAJMzHmjd6sEEgtVUT` | `k-1 mod n` |
| `P/2` | `16eEXbSuKN8tvcos1iKjdju6dAaWWRBMEs` | `k*2^-1 mod n` |
| `2P` | `1KHMK2C8uBptRz67FbrXy43yHzhZG16Hbm` | `2k mod n` |
| `P+G` | `1PhXF3xVQ8Sg9FomBcmRwRbvvGfm3Y2os1` | `k+1 mod n` |

`source/onchain/` preserves the pinned facts and five explorer JSON snapshots.
`tools/gsmg_verify/verify_key_relations.py` recomputes each address without
private-key knowledge, while `verify_onchain_relations.py --live` compares
the transaction fields to an explorer. A found scalar for one of these
related addresses could be normalized and checked against the prize. The
public relation itself neither reveals a scalar nor shrinks its search space.
The funding address's control is not authenticated as the puzzle creator's.
In the Telegram export, #12580 says blockchain messages are not the
creator's or part of the puzzle; the creator replies "Correct" in #12653.
These relations are reproducible on-chain observations, not endorsed
instructions. Do not promote them above the established locked containers.

A third address, `1cc6xayvqpeetixmuXDRsGug7GKyoRdxP` (HASH160
`06bbdc66fda09110435c79a86656a604c2d5c69b`), is the prize key's compressed twin and
is empty. The win test checks both point forms, so it is covered by the same scalar.

### The exact win test

Keep raw-key validation separate from answer-to-key derivation. A directly serialized
32-byte private key must be used as that scalar; hashing it first tests a different
key. SHA256(answer) is a separate candidate interpretation, supported at earlier
solved boundaries but not a universal rule for every unsolved output.

```python
import hashlib, coincurve

PRIZE_H160 = 'a9553269572a317e39f0f518cb87c1a0ee1dbae4'
SENTINEL_H160 = '4bc468447fe1b048ad030a2f9a125478eabc4ed6'

def h160(b):
    return hashlib.new('ripemd160', hashlib.sha256(b).digest()).hexdigest()

def match_raw_private_key(priv):
    if not isinstance(priv, bytes) or len(priv) != 32:
        raise ValueError('Expected an already serialized 32-byte private key')
    pk = coincurve.PrivateKey(priv).public_key  # rejects out-of-range scalars
    hashes = {h160(pk.format(c)) for c in (True, False)}
    return {'prize': PRIZE_H160 in hashes,
            'secondary_sentinel': SENTINEL_H160 in hashes}

def win(X):
    raw = X.encode('utf-8') if isinstance(X, str) else X
    priv = hashlib.sha256(raw).digest()  # explicit answer -> key hypothesis
    return match_raw_private_key(priv)['prize']
```

Only `prize=True` is the exact puzzle win. A sentinel match is a separate finding,
not a prize-key success. Both public-key serializations are checked, so the prize
point's compressed twin is covered through its uncompressed prize-address form.

Public scalar-1 controls must reproduce compressed HASH160
`751e76e8199196d454941c45d1b3a323f1433bd6` and the known uncompressed address
`1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm`. Audit 126 additionally verified that the
published prize public key reproduces the actual poster address and that the
production match expression accepts positive public controls and rejects negatives.

Historical harnesses also tested double-hash variants. Preserve those distinct
identities; neither SHA256 of binary digest nor SHA256 of hex ASCII is the same
as passing an existing raw scalar directly. No variant is automatically selected
by the word SHA256 alone.

### The 2026 OP_RETURN stream is inbound spam, not a creator channel

Verified against mempool.space on 2026-09-21. `17ucy...` has spent_txo_count = 0
across 45 transactions. It has never spent an output, so it cannot be the sender of
anything. Every OP_RETURN attributed to it sits in a transaction that **pays it 546
sat of dust** and carries the message alongside. Sending dust to someone else's
address costs cents and anyone can do it, so these messages carry no authentication.

Two batches exist and their payloads are real (hex decoded and checked):

    block 938165   hereismysecret, fourfirsthintisyourlastcommand,
                   matrixsumlistenterlastwordsbeforearchichoicethispassword,
                   yourlastcommandsecondanswer, secondanswer, yourlastcommand
    block 944096   secondanswer, isolveditwithanabacus, hereismysecret,
                   yourlastcommand, leavethematrix

**The varying output amounts are change.** Each transaction spends the previous
change, pays 546 sat of dust to the vault, attaches the message, and returns the
remainder to itself; the step is dust + fee (546 + 450 = 996 at block 938165,
546 + 550 = 1096 at block 944096), measured exactly. The 2175 "pair offset" is the
difference between two bots' balances. There is no second channel.

**The senders are dust bots.** Inputs come from `145ZQ9siLrsXBKf465wjdyQYAP5dRwhRhQ`
and `1JG648yaB7Wp2dpUfcZoRSD4q35oq47vCu` (lifetime throughput about 0.0176 BTC; both
now empty). `matrixsumlistenterlastwordsbeforearchichoicethispassword` is a re-cut of
the published #8446 tokens, so the stream is derivative. The creator publicly denied
authoring on-chain OP_RETURN messages (#12653).

**Tested and null.** 379 candidates: every token alone, both batch orders forward and
reversed, all 2- and 3-term permutations within each batch, cross-batch pairs, and
each token crossed with 996, 1096, 2175 and the endpoint amounts.

**The "creator cluster" built from these sprays does not hold.** Shared control is
established by common input ownership, not by a shared payer. The 2025-09-09 spray at
block 913830 has 1 input and 10 outputs: one outsider paid ten publicly known GSMG
addresses. Dusting is the standard way to manufacture a false cluster. What survives
is narrow: `1EtbTvVB8...` funded the prize address on 2019-04-13 and also paid
`1GSMG1CLx...` (2018) and `1BEN1x8p...` (2020). The prize address has only ever signed
its two self-transfers.

**The `11111119536NnU2vPAvoQhvkheQ8ejYJ` "witness pair" is a dust recipient.** Valid
base58check, hash160 with 48 leading zero bits (about 2^48 work, an affordable
collectible). It is spendable and spent (46 of 47 outputs). The WITNESS transaction
is the same dust-bot shape as above, emitted by vanity address `1GSMG9VDL...`. The
64-byte blobs are unauthenticated; nonce reuse against the prize's six known `r`
values was tested and is null.

**Prefix sharing is forced.** Keeping only the top 3 bytes `a95532` and randomising
the rest, 1227 of 2000 hash160s still render as `1GSMG...`. Landing `1GSMG` takes
about 58^4 = 1.13e7 vanity attempts. Prefix sharing establishes taste, not control.

### The on-chain oracle is closed

Six checkpoint addresses exist on chain, every preimage is known, and the message
stream ends April 2020.

### The live verifier is a stage-1 gate only

`POST https://gsmg.io/phase1verification` validates the phase-1 answer and rejects
everything else, including `causality`. It requires the CSRF token from the page's
`<meta name="csrf-token">` tag; a bare POST returns 413. Ten submissions
characterised it completely. Do not submit more.

### The August 2026 relaunch adds nothing (doc 108)

gsmg.io was restored in three steps (Last-Modified, UTC): `/theseedisplanted` and
`/puzzle` on 2026-08-15, `robots.txt` on 2026-08-16, and a farewell page at `/` on
2026-08-17. Audited through a browser on 2026-09-24:

- `/register`, `/help-center` and unknown paths return 404 with a 9-byte body
  `Hello :-)`. The legacy trading-bot text is hidden template residue.
- `robots.txt` is an ASCII rabbit and teacup, a figlet "Follow the white rabbit!",
  then `Disallow: /`.
- The Matrix-rain glyph pool is a fixed string, 56 alternating bits plus
  `GSMG.IO5BTCPUZZLECHALLENGE`, sampled at random. No message.
- A hidden terminal ("Trace program: running", "SYSTEM FAILURE") prints a 14x14 bit
  grid identical to the poster cell for cell (196/196, black and blue = 1, white and
  yellow = 0). It prints the `#FEFEFE` cell as 0, its message bit.
- No HTML comments on the root.

267 variants of every farewell line and 14 forms of the terminal grid were run
against the containers under three KDFs: 12,645 decrypts, 54 valid pads (about 49
expected), 0 readable. Older gsmg.io material still counts as creator material only
when it matches a pre-2022 archive capture or a hash in this document (#66584: the
original URL "and thus the original puzzle" is gone). The archived `/Puzzle`
(2020-11-09) and `/phase1verification` (2023-09-08) captures are the GSMG web
application shell, with no door (doc 106; #32699, #32701).

---

## 2. THE ENCRYPTION CONVENTION

Proven on three earlier solved envelopes. This is the best-evidenced default;
it does not prove the settings of any unopened container. `Salted__` identifies
the envelope family, not the cipher, KDF, iteration count or plaintext type.

| item | value |
|---|---|
| container | OpenSSL `Salted__` + 8-byte salt + ciphertext, base64 |
| password | `sha256(answer)` written as **64 lowercase hex ASCII characters** |
| KDF | legacy `EVP_BytesToKey`, **md = SHA-256**, 1 iteration |
| cipher | AES-256-CBC, PKCS#7 padding |

Equivalent command:

    echo <b64> | openssl enc -d -aes-256-cbc -a -md sha256 -pass pass:<sha256hex>

```python
import hashlib
from Crypto.Cipher import AES
def evp(pw, salt):
    d=b''; prev=b''
    while len(d)<48:
        prev=hashlib.sha256(prev+pw+salt).digest(); d+=prev
    return d[:32], d[32:48]
def decrypt(raw, answer):
    pw=hashlib.sha256(answer.encode()).hexdigest().encode()
    k,iv=evp(pw, raw[8:16])
    pt=AES.new(k,AES.MODE_CBC,iv).decrypt(raw[16:])
    p=pt[-1]
    return pt[:-p] if 1<=p<=16 and pt[-p:]==bytes([p])*p else None
```

A random wrong key passes a PKCS#7 check about 1 time in 255, almost always with
pad = 1. **A pad-1 success is not evidence.** pad >= 3 is about 1 in 16.7 million
per decrypt, so at tens of millions of decrypts a few pad-3 events are expected by
chance (sections 10.6 and 10.7 record three). Pad 1 and pad 2 are legal for the
80-byte containers and must be content-checked, not discarded.

### The recogniser (doc 110)

Until 24 September the content check at pad 1 and 2 accepted printable prose, hex
keys, `gsmg.io/` + hex, WIF, BIP38, raw 32-byte windows and BIP39. It did not
recognise EBCDIC, UTF-16, compressed or container formats. Doc 110 reports applying the structure-agnostic
recogniser to its registered valid-padding outputs:

- bit-position bias: any of the 8 bit positions with |z| >= 6 (catches ASCII, EBCDIC,
  digits, hex, base64, UTF-16)
- distinct-byte deficit: z <= -6 against random bytes of the same length
- magic headers (`Salted__`, gzip, zip, bzip2, 7z, png, pdf, xz, zstd) and a nested
  `Salted__` anywhere
- EBCDIC decode (cp273, cp037, cp500, cp1140, cp875, cp1026), alnum + space >= 0.95
- UTF-16 zero-byte alternation >= 0.6
- printable >= 0.80, and pad >= 3
- every 32-byte window as a private key against both targets, both point forms

Calibrated on 100,000 random strings of 64 to 79 bytes and 2,000 of 1,320 bytes: the
bias and distinct tests fired 0 times; the EBCDIC threshold was raised from 0.80 to
0.95 after it fired about 1 in 5,000. Controls for ASCII, EBCDIC cp273, UTF-16, gzip,
hex key, digit string and base64 all fire.

**Lock chaining.** A lock's plaintext may be binary and serve as the password of
another lock. Every valid-padding output is also tried as the password for the other
two locks (raw, hex, sha256 hex of each, both EVP digests), and the second-step output
goes through the recogniser. Control: a 79-byte random plaintext whose hex keys a
second envelope holding UTF-16 text. Found.

**What no recogniser can see.** A plaintext that is itself headerless ciphertext or
uniformly random bytes, at pad 1 or 2, cannot be told from a wrong password by its
content. Only a downstream step can test it. An encrypted 32-byte key in the usual
framings (IV + 48 bytes, or a nested `Salted__` with 48 bytes) is 64 bytes, which gives
pad 16 in an 80-byte container, and a recognizer explicitly including this framing can flag it.
A later recognizer improvement does not establish that every earlier run used it.

---

## 3. THE VERIFIED CHAIN

Four gates opened. Every value below is reproducible from the data in this file.

### 3.A The backbone: Logic, "The Warning" (restored)

The puzzle follows the song "The Warning" by Logic (doc 22). It was dropped from this
file after doc 22 and restored on 23 September (docs 98 to 100). The full 13-line text
was supplied by the user and is kept out of this document; lines are described here, not
quoted.

| song line | content (described) | used by the chain |
|---|---|---|
| 1 | title | the rebus answer WARNING |
| 2 | phase one header | |
| 3 | phase one opening line | first half: the poster URL `theseedisplanted`; second half (opposites attracting) unused |
| 4 | a four-word question | the rebus tiles CAN YOU DIG IT |
| 5 | phase one closing line | unused |
| 6 | phase two header | |
| 7 | phase two opening line | up to the comma: the phase-1 password; the list after it unused |
| 8 | phase two middle line | unused |
| 9 | a red or black rose, with nothing in between allowed | the design rule for the `war` tile and the off-white cell (below) |
| 10 | phase three header, "The Judgement" | unused |
| 11 | the judgement question | unused |
| 12 | the red-or-black choice | unused |
| 13 | closing line | unused |

The pattern holds for both used pieces: the opening of a phase, cut at its first
natural break. Phase three is the only phase whose opening the chain has never used.
The puzzle's own naming mirrors the song's numbered phases (Sal-PHASE-Ion).

**What the song explains.**

- **The black `war` tile** (section 5). WARNING is the only rebus word built from a
  black half and a red half. The song's two roses are red and black. Consumed.
- **The `#FEFEFE` cell** (section 4.3). The song rules out anything between red and
  black. The poster has exactly one in-between colour. Forced to one side, only blue
  parses dbbi. Consumed.
- **The Cosmic Duality cover** (section 7.4). The unused second half of line 3
  describes opposites attracting, which is a plain description of a yin-yang, and the
  book caption says each half holds the seed of its opposite. That is a better account
  of the creator's "scary specific" (#8315) than any earlier reading.

**Spent as text.** Every contiguous word span of the song (1 to 40 words) in five
forms, every line and clause, raw and double-hashed, and crossed front and back with
the labels and chain answers: null (doc 99, about 79,000 candidates). The rose answers
and opposites-attract forms: null (doc 98). If the song drives the endgame, it does so
as structure (which phase maps to which gate, what the red/black choice selects), not
as a string.

### 3.0 The poster to the URL

File `puzzle.png`, sha256
`38125bbdf1ea58b9b30b075bc6bf71e4089d04bba37098317e47097e2f2a1830`, 29,931 bytes,
1048x1556. Byte-identical to the Wayback capture of 12 Nov 2020.

A 14x14 grid of 75-pixel cells. Read as an inward counter-clockwise spiral from
the top-left, going down first. Black and blue = 1; white, yellow and one
off-white cell = 0. First 192 bits, 8 per character:

    gsmg.io/theseedisplanted

Full spiral bit string (196 cells; the last four are the surplus centre, measured
`0000`):

```
0110011101110011011011010110011100101110011010010110111100101111
0111010001101000011001010111001101100101011001010110010001101001
0111001101110000011011000110000101101110011101000110010101100100
0000
```

### 3.1 Phase 1, the rebus page

Page `gsmg.io/theseedisplanted`. Answer:

    theflowerblossomsthroughwhatseemstobeaconcretesurface
    sha256 5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75

The creator posted that hash himself (#225/#226, 22 Apr 2019: "just try hit your
options against that hash"). The phrase is the song's phase-two opening up to its
comma (section 3.A). Accepting it redirects to
`/choiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecialdessertiwroteitmyself`.

### 3.2 Phase 2

Textarea 1 of the choice page. Salt `06286612d43ed7ed`, 656 bytes ciphertext.

    answer   causality
    password eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf
    plaintext 648 bytes, six CRLF line breaks
    sha256   e2f9dd65604a3231f8b3301724e8d713a88fffc4b6c7c4aeeb20f58a582b593a

Full plaintext, generated from the decryption. The block below has exactly the
plaintext's six line breaks and no hard-wrapping; **replace each LF with CRLF** and
it hashes to `e2f9dd65...` exactly.

```
The ironic 2name of the keymakers trying to protect the current digital powers which are still in severe danger due to the keymaker's way of security by hiding, nearly unprotected, in plain sight. {eps3.4_[in one of the valleys of Phillip]runtime-error.r00., where daughters hit magic keypads} When this fails.. Crypto finally to the latin 3Moon? Tell me, 4How so mate?
# X 2 S H 4 Y 0 Q B 15 #
Q -> extend the name of a hackers' swordless fish, the I and W are below.
B -> ((BV80605001911AP)- (sqrt(-1)))^2
H -> (Answer to only this puzzle but nothing else) * -1
S -> cha' + (vagh * jav)
Ok kid, on the highway, let put it in the worst gear.
```

**This block is closed. It is a ten-slot template, and every slot resolves.**

| slot | clue | resolution | value |
|---|---|---|---:|
| `Q` | a hacker's swordless fish is Darlene's fish **Qwerty** (Mr Robot); "extend the name" is the keyboard row; **I and W sit below the digits 8 and 2** | 8, 2 | 82 |
| `B` | `BV80605001911AP` is the Intel SKU for the Core **i5**-750; `sqrt(-1)` is **i**; so (i5 - i) squared | 5^2 | 25 |
| `H` | the answer to life, the universe and everything, negated because this is "only this puzzle but nothing else" | 42 x -1 | 42, **sign dropped** |
| `S` | Klingon: `cha'` = 2, `vagh` = 5, `jav` = 6, so 2 + (5 x 6) | 32 | 32 |

"Put it in the worst gear" is reverse, applied twice: reverse the sequence, then
reverse the digits of each number.

```
printed        X    2    S    H    4    Y    0    Q    B    15
reverse seq    15   B    Q    0    Y    4    H    S    2    X
substitute     15   25   82   0    Y    4    42   32   2    X
reverse digits 51   52   28   0    Y    4    24   23   2    X
coord          51 deg 52' 28.0" N   4 deg 24' 23.2" E
```

The two letters with no definition, X and Y, land on the two hemisphere positions.

**The dropped `H` sign** has a reading and no value (doc 102). The Architect text opens
by calling the solver's life "the sum of a remainder of an unbalanced equation
inherent to the programming of this puzzle"; the one equation the puzzle leaves
unbalanced is this template, whose `H` clue is `x -1` while the coordinate uses +42.
The template sums with the sign kept, dropped and reversed are null (160 candidates).
The creator's "the theory of everything is also still a valid path" (#8354) and a bare
"42" (#8385) point at this slot.

**"On the highway" is consumed** (doc 71 §3). The coordinate is SafeNet's Rotterdam
site: business registers list **SafeNet Technologies B.V., Seattleweg 5, 3195 ND
Pernis Rotterdam** (Distripark Eemhaven), beside the **A15 motorway**. The district and
the motorway fit; exact geocoding of the street number was not obtained. On 2019-06-27
the creator posted a seedling emoji (#1210) and then a motorway emoji (#1211). Asked in
2023 whether the header is useless for reaching phase 3, he answered "Can't say
anything about this" (#8569). Carry the coordinate as **resolved as a value, possibly
unspent as an ingredient**.

**The inline numerals are assembly indices into the seven-part phase-3 answer:**

| index | clue | where the clue lives | part |
|---|---|---|---|
| 1 | the door's own answer, reused | the door | `causality` |
| **2** | "the ironic **2name** of the keymakers" (a safe net, nearly unprotected in plain sight) | phase-2 plaintext | `Safenet` |
| **3** | "Crypto finally to the latin **3Moon**?" | phase-2 plaintext | `Luna` |
| **4** | "Tell me, **4How so mate**?", read aloud | phase-2 plaintext | `HSM` |
| 5 | "The **5binary** code is a part of the piece of this puzzle", via Executive Order 11110 | page prose | `11110` |
| 6 | "Its' raw data after 4 on row 1616" | page prose | genesis headline as reversed hex |
| 7 | "And now a buddhist is forced to move. What will be the next situation?" | page prose | the FEN after Rg6-c6 |

The convention continues: phase 3's plaintext says "The thinker's **1name**" and
numbers its third riddle "**3.**".

**The `{eps3.4_...}` brace clause.** `{eps3.4_[in one of the valleys of Phillip]runtime-error.r00., where daughters hit magic keypads}`.
Delete the bracketed insert and the remainder is `eps3.4_runtime-error.r00`, the
title of *Mr. Robot* season 3 episode 5. Phillip Price; Angela (his daughter) at the
HSM. Thales and ESET writeups confirm the scene and its strings (`z1on0101`,
`022350`, key `B-TUDGTDL-0112180501042508051805`, whose A1Z26 tail reads
`ALREADYHERE`). A fourth pointer at the SafeNet/HSM theme; no new operand. 1,586
candidates from it screened, null. The creator later said "rewatch episode 3.5 with
the better half" (#60324), the same episode. `frank.bowman`, `hidd3nlynx` and
`room 23-148` are uncorroborated.

### 3.3 Phase 3, the seven-part password

Textarea 2 of the same page. Salt `9fbc451d13d071f4`, 4,096 bytes ciphertext.
The answer is the plain concatenation of seven parts:

1. `causality`
2. `Safenet`
3. `Luna`
4. `HSM`
5. `11110`
6. `0x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854`
7. `B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1`

Part 6 is the Bitcoin genesis message byte-reversed as in Satoshi's main.cpp line
1616 (verified: it reverses to "The Times 03/Jan/2009 Chancellor on brink of second
bailout for banks"). `0x` plus 138 hex characters is exactly 140 characters, which
matches the Architect text's "HUNDRED FOURTY". The creator dismissed the **spelling**
of "fourty" as a typo (#5960); the number is real. Part 7 is the position **after**
White's move; the page shows `.../6R1/... w - - 0 1`.

    password  1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5  (verified)
    plaintext 4,090 bytes
    sha256    c4ad94559a44a927c1032cc0e024515f9510a0806a2d14458dbf4a360af9865f

Its first 726 bytes are riddles, then the base64 phase-3.2 envelope. The riddle head:

```
What if the merovingian is wrong. What instead of causality something else could
be ours? Therefor, if so, the ...... is ours. The thinker's 1name behind all of
that would grant you access to the next step (of humanity). Definitely look into
his works might you have time. /(aa,connected enf)

I just passed a cheshire cat and I'm getting fed up with this puzzle.. It's taking
forever. But, How long is forever? I don't know, but just add giveit in front of
the answer and you can fall in the keyhole. /(aa,connected enf)

3.The fundamental limit to the precision with which certain pairs of physical
properties are know. /(aa,connected enf)

Phase 3.2 is ciphered with aes-256-cbc base64 and a sha256 pw, yet again.
```

**The six `/(...)` tags are format specifications. Closed** (doc 71 §2).

| # | location | exact text | adjacent part | fit |
|---|---|---|---|---|
| 1 | page HTML, before the 672-byte container | `/(aaa, connected enf)` | `causality` | lowercase, no spaces |
| 2 | page HTML, after the genesis paragraph | `/(aBa, connected enf)` | `0x736B6E61...` | mixed case, no spaces |
| 3 | page HTML, after the buddhist question | `/(aBa, connected not enf)` | the FEN | mixed case, **the only part that keeps its spaces** |
| 4-6 | phase-3 plaintext, after each riddle | `/(aa,connected enf)` | the three 3.2 answers | lowercase, no spaces |

`aa`/`aaa` = all lowercase, `aBa` = mixed case, `connected` = no spaces, `enf` =
enforced. Six for six, and the single negation lands on the single part with spaces.
The SalPhaseIon textarea carries **no tag**, so case and spacing stay free parameters
for its password.

### 3.4 Phase 3.2

Envelope embedded in the phase-3 plaintext. Salt `eefc4c5befc1656a`, 2,432 bytes.

    answer   jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple
             (spelled giveit, not givetit)
    password 250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c  (verified)
    plaintext 2,422 bytes, pad 10
    sha256   b82afeb86f9e50848220f9b64b744b821400308aea273a1c949b9d2d0e408a34  (verified)

"The ...... is ours" is Jacque Fresco's documentary *The Choice Is Ours*: six dots
for the six letters of CHOICE (see the dot convention, section 7.3). "How long is
forever?" is the Cheshire Cat ("sometimes, just one second"). The third is a
definition.

Measured: **1,426 of 2,422 bytes are strictly printable, 58.9%**. Any sweep that
filters for printable plaintext would have discarded this correct result.

| bytes | content |
|---|---|
| 0 to 446 | ASCII intro |
| 447 to 1985 | EBCDIC letters, the Architect text |
| 1986 to 1989 | `0d 0a 0d 0a`, blank line |
| 1990 to 2138 | 149 digits, the straddling checkerboard |
| 2139 to 2142 | `0d 0a 0d 0a`, blank line |
| 2143 to 2291 | the checkerboard key riddle |
| 2292 to end | the locked Terminal envelope |

The intro, generated from the plaintext:

```
I've been waiting for you. You have many questions, and although the process has altered your consciousness, you remain irrevocably human. Ergo, some of my answers you will understand, and some of them you will not. Concordantly, while your first question may be the most pertinent, you may or may not realize it is also irrelevant.

... am I here? Wake up, you... I've designed you a beautiful strategic position. One for one, four for one.
```

The checkerboard riddle:

```
Raising the stakes without extra chances of winning. A fubcd-king & oracle-queen, thingky mvps, on a sad board but as wide as the first one seen.
```

**`phase3.1_old.aes` is closed** (#67567, #71100). A 2,448-byte envelope with salt
`e2991cdcd2c957f9` opens under the pre-fix spelling
`jacquefrescogivetitjustonesecondheisenbergsuncertaintyprinciple`; its plaintext is
byte-identical to the current one (`b82afeb8...`). A re-encryption of the same text.

### 3.4a The Architect text

Take plaintext bytes [447:1986), decode as latin-1, **encode** to **cp273**, read the
resulting bytes as letters, then **reciprocal Beaufort** decrypt, `P = K - C mod 26`,
with key `THEMATRIXHASYOU`. Result, 1,539 letters, canonical as unbroken lowercase
(uppercase here for legibility). Generated and verified from the plaintext:

```
YOURLIFEISTHESUMOFAREMAINDEROFANUNBALANCEDEQUATIONINHERENTTOTHEPROGRAMMINGOFTHIS
PUZZLEYOUARETHEEVENTUALITYOFANANOMALYWHICHDESPITEMYSINCERESTEFFORTSIHAVEBEENUNAB
LETOELIMINATEFROMWHATISOTHERWISEAHARMONYOFMATHEMATICALPRECISIONWHILEITREMAINSABU
RDENTOSEDULOUSLYAVOIDITITISNOTUNEXPECTEDANDTHUSNOTBEYONDAMEASUREOFCONTROLWHICHHA
SLEDYOUINEXORABLYHEREYOUYOUHAVENTANSWEREDMYQUESTIONMEQUITERIGHTINTERESTINGTHATWA
SQUICKERTHANTHEOTHERSPLEASEIFYOUFINDAWAYTOCOMPLETETHELASTPARTOFTHEPUZZLETAKETHEP
RIVATEKEYYOUVEEARNEDITBUTPLEASETAKETHISTOHEARTTHATWHATAWISEMANABOVEHINTEDATISWOR
THHUNDREDFOURTYOFTHEINVESTMENTTHATSWHATUSGUYSATGSMGARETRYINGTOACCOMPLISHINTHEEND
PLEASEJUSTHELPUSBUILDITINSTEADOFJUSTWAISTINGYOURLIFETIMEBYHUNTINGFORWORTHLESSPRI
CESANDTHROPHIESLIKETHISIMSORRYTOTELLYOUTHATYOUVECOMETHISFARBUTYOULLNEVERFINISHTH
ELASTTASKIEXPECTYOUTOSAYBULLSHITWELLDENIALISTHEMOSTPREDICTABLEOFALLHUMANRESPONSE
SBUTRESTASSUREDTHISWILLNOTBETHELASTTIMEIHAVEDESTROYEDARESTLESSSOULANDIHAVEBECOME
EXCEEDINGLYEFFICIENTATITTHEFUNCTIONOFTHEYOUISNOWTORETURNTOTHESOURCECODESALLOWING
ATEMPORARYDISSEMINATIONOFTHECODEYOUHOPEFULLYCARRYREINSERTINGTHEPRIMEBASICSAFTERW
HICHYOUWILLBEREQUIREDTOSELECTFROMOVERTWENTYTHREECIPHERSSIXTEENENCRYPTIONSANDORSE
VENINTERTWINEDPASSWORDSTOFINDTHEACTUALPRIVATEKEYNOTETHATALSOBRUTEFORCINGMIGHTBER
EQUIREDFAILURETOCOMPLYWITHTHISPROCESSWILLRESULTINACATACLYSMICSYSTEMCRASHKILLINGY
OURWILLPOWERWHICHCOUPLEDWITHTHEEXTERMINATIONOFYOURWILLTOLIVEANDWILLULTIMATELYRES
ULTINTHEEXTINCTIONOFTHEENTIRENESSOFYOURSELFSELFGOODLUCKNEVERTHELESSIREALLYHOPEYO
URETHEONECIAOBELLAO
```

Letters-only index 479 (0-based) starts `PRIVATEKEYYOUVEEARNEDITBUTPLEASE`.
`PRIVATEKEY` occurs at 479 and 1238. **Always use the letters-only form.**

It is a rewritten Matrix Reloaded Architect speech, aligned word-for-word against
the film in doc 45 (22 edits, 46% creator-authored). Changes from the film:

- "the One" becomes THE YOU; "the source" becomes THE SOURCE CODES; "the prime
  program" becomes THE PRIME **BASICS**.
- "select from the matrix 23 individuals, 16 female 7 male" becomes SELECT FROM
  **OVER** TWENTY THREE **CIPHERS** SIXTEEN **ENCRYPTIONS AND/OR** SEVEN
  **INTERTWINED PASSWORDS**. The numbers are the film's own.
- Added: HOPEFULLY, ACTUAL PRIVATE KEY, BRUTE FORCING MIGHT BE REQUIRED, WISE MAN
  ABOVE ... HUNDRED FOURTY, the whole GSMG paragraph, CIAO BELLA.
- Speaker labels `YOU` (offset 341) and `ME` (offset 371) mark the dialogue turns.
- Offset 1483 is a doubled word, `YOURSELF` `SELF`, and the text ends `CIAOBELLAO`.
  The trailing `O` is authored (the final ciphertext byte decrypts to `O` under key
  letter `X`).
- **The film's door scene is deleted entirely.** The film says "choice" five times;
  this text contains no `CHOICE`. The one place CHOICE appears in the whole chain is
  the six-dot elision in the phase-3 riddle (section 3.4).

**Possible manual reading (doc 96).** "Return to the source codes ... reinserting the prime
basics, after which you will be required to select from over twenty three ciphers
sixteen encryptions and/or seven intertwined passwords" describes the SalPhaseIon page
step by step if the dbbi walk is the prime basics. Every index set the walk yields was
used to select from nine texts and is null (doc 97; section 10.7).

### 3.4b The straddling checkerboard

The 149 digits, generated from the plaintext:

```
15165943121972409169171213758951813141543131412428154191312181219433121171617137
149110916631213131281491109166131412199114371612126021664313711154112
```

Key `FUBCDORA.LETHINGKYMVPS/JQZXW`, digits 1 and 4 blank in the top row (the
straddles). The riddle spells the key: "fubcd-king & oracle-queen, thingky mvps".
Over all 45 choices of blank pair, exactly one reproduces the plaintext, and it is
{1,4}. The sentence immediately before the ciphertext is `One for one, four for
one.`, read as naming the two straddle digits (INFERRED). `ORACLE` appears as
`ORA.LE`: the repeated `C` is replaced in place by a placeholder, which is also an
instance of the dot convention (section 7.3). Result, 91 letters, verified:

```
INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE
```

**Read that message as ownership logistics.** "Half" and "Better Half" are people:
the creator and his partner (he calls his wife "the better half", #39241, #60324).
It is not an announcement that the puzzle yields two keys. It sits immediately before
the Terminal envelope and reads as a warning attached to that object (section 6.5).

---

## 4. THE FIRST IMAGE, COMPLETE

### 4.1 Layout

14x14 grid of 75-pixel cells in the top 1050 pixels, then a red divider `#ED1C24`,
the title, a QR code and the prize address. The grid region contains **exactly five
colours and zero anti-aliasing**:

    #000000  86 cells      #FFFFFF  85 cells      #3F48CC  15 cells
    #FFF200   9 cells      #FEFEFE   1 cell

These colours are the Windows Paint default palette. All 69 non-uniform 15-pixel
blocks lie in the bottom row that carries the red divider; there is no sub-cell
steganography. The poster has **101** set cells (black 86 + blue 15), a prime.

### 4.2 The colour layer

Exactly 15 blue and 9 yellow. Their spiral positions are all `= 7 (mod 8)`, the LSB
of each of the 24 characters, blue = 1 and yellow = 0. The colour layer repeats
information the black and white cells already carry. Sequence in spiral order:

    B B B B Y B B B Y Y B B B B Y B B Y Y B Y Y B Y

### 4.3 The anomaly cell: two parser interpretations

One cell is `#FEFEFE` at grid row 7, column 4 (0-based): row-major 1-based 103,
spiral 0-based 163, inside the 21st ASCII byte (`n` in "planted"). It is a light
cell with **6 of its 8 neighbours dark**. A solver marked it in 2020 (#2899);
the creator replied "Interesting" (#2905). Its URL bit is zero.

The earlier dossier treated its role as settled after testing insertion. That
comparison did not exclude replacing its byte's existing marker instead.

| Local parser treatment | Logical length | Consumed | Blue/yellow prime hosts | Unused markers |
|---|---:|---:|---|---|
| Insert a new blue marker at position 21 | 83 | 91/91 | 15 / 8 | B, Y |
| Replace byte 21's yellow marker with blue | 84 | 91/91 | 16 / 7 | Y |

Both are exact fits under their declared models. The replacement is the only
successful strict parse among the 24 single-marker flips, and the off-white cell
independently identifies byte 21. The 23/16/7 census agrees with the Architect/film
numbers; it does not select a downstream operation or password. Attempt 118
inadvertently repeated this already recorded `perbyte84` model from September 14.
Its novelty claim is retracted; the current dossier's insertion-only closure is
also retracted. Older L=84 selection/password negatives remain exclusions.

Reading the cell as the white rose painted in *Alice* Ch. VIII is a thematic
interpretation. It does not prove an insertion, global repainting, or a complete
endgame recipe. If retaining the separate `574061` macro branch (section 9), any
parser edit must remain local: global replacement produces composite `574053`
and changes the fixed digit sums from `[23,16,7]` to `[24,16,8]` (review 124).

**Which cell (doc 105, correcting "1 in 12").** **14** spiral positions (152 to 158,
160 to 166) give the insertion walk the same program. Of those, only 163 is prime
counted from zero on the spiral and prime counted from one in reading order.
That pairing was chosen after seeing the answer; two other indexing pairings
select different single cells. Its reported weight is about 1 in 5, not proof
of the indexing rule. "First or zero" (#4105) is not a universal index convention.

### 4.4 The rabbit and its nest

A white-rabbit line drawing covers exactly 7 cells with **37 black 15-pixel
pixels**. Per-cell ink, spiral order: 172:4, 184:2, 187:9, 192:4, 193:6, 194:3,
195:9. Spiral 192 to 195 are the four surplus centre cells, the 2x2 centre (rows 6-7,
cols 6-7), all white, all carrying rabbit ink. This is "the rabbits nest" of the Roses
poem (#2899/#2905).

**The nest pixels are the drawing (doc 105).** Read as a 10x10 nest, as 3x4 and 2x4
rabbit boxes, in row, column, boustrophedon and the poster's own spiral order, normal
and inverted, both directions, 8 bit offsets, as ASCII and as passwords and keys: best
0.64 printable, noise, no hits. The ink draws ears, head outline and eye. In the
resistor colour code the poem's "Yellow has a number and so does Blue" are 4 and 6,
the first two nest counts; an observation, null as passwords (doc 103).

### 4.5 Other poster facts

The QR code encodes the blockchain.com URL for the prize address; pristine, no hidden
data. `sha256("GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe")` =
`89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32` is the side-page
URL, reached via `HASHTHETEXT` from the Decentraland (-41, -17) audio side quest. This
is the "second door" of 2020 (doc 39). `follow_the_white_rabbit.png` is an uncropped
copy with zero differences.

### 4.6 The poster has no spare capacity

    196 cells
    192   the bits of "gsmg.io/theseedisplanted"        determined
      4   the centre 2x2, measured 0000                 MEASURED, NOT DERIVED
     24   which cells are coloured: exactly = 7 mod 8   forced
     24   blue vs yellow: blue = 1, yellow = 0          forced by the bit

With the three global conventions fixed (spiral walk, colour residue class,
polarity), every cell value is a function of the URL. The only per-cell free choices
are which cell is off-white (section 4.3) and the rabbit drawing (section 4.4).

---

## 5. THE REBUS PAGE, COMPLETE

`/theseedisplanted` is eight bare `<img>` tags with no CSS and no text, followed by a
`display:none` POST form to `/phase1verification`. With no CSS the images lay out in
DOM order, which is alphabetical by filename; the colour prefixes force the grouping.

| tile | size | padL | padR | text |
|---|---|---:|---:|---|
| black_banking - war | 78x70 | 0 | 8 | bank icon, `war` |
| blue_ca | 78x70 | 0 | 8 | `CA` |
| blue_dig_i | 77x70 | 0 | 7 | `dig i` / `+` |
| blue_lock_lo | 82x70 | 0 | 16 | closed padlock, `lo` |
| red_crypto_gic | 79x70 | 12 | 0 | `crypto` / `gic` |
| red_n_you | 80x70 | 13 | 0 | `n you` |
| red_open_lock_n_ing | 82x70 | 16 | 0 | open padlock, `n ing` |
| red_t | 79x70 | 12 | 0 | `t` / `-` |

**Black and blue pad on the right; red pads on the left; without exception.** Blue
or black is the left half of a word, red the right half: CAN YOU, DIG IT, LOGIC,
WARNING. The colour layer is a typesetting instruction with essentially zero
capacity. The page spells the song's title (WARNING), its artist (LOGIC) and its
phase-one question (CAN YOU DIG IT).

**The black `war` tile is consumed** (doc 100). WARNING is the only word built from a
black and a red half; the song's two roses are red and black.

**The judgement on the page.** The song and artist account for every letter except
`crypto` (red tile) and the bank icon (the only black tile). The open padlock is red
and the closed one blue. The page carries crypto (red, unlocked) against banking
(black), which matches part 6 of the phase-3 answer, the bailout-for-banks headline.
The crypto-versus-banking vocabulary is null as passwords (doc 100).

Unresolved: the only geometrically forced pair is closed padlock + open padlock
(66/66, 16+16), while semantics pairs `lo` with `gic`. Blue `#3F48CC` and red
`#ED1C24` are exactly the poster's colours. No second channel (no text chunks,
nothing after IEND; the `sRGB` chunk pattern `00111011` correlates with nothing). The
live page carries a later comment:
`<!-- Nice to see you around! Good luck little bunny hunter ;) -->`.

---

## 6. THE SALPHASEION TEXTAREA

The first `<textarea>` on the side page, whitespace removed, 1,075 characters
(generated; concatenate the lines with no separators). The whitespace in the archived
HTML is 1,074 separators, all 0x20, with no non-ASCII: no channel (doc 109).

```
dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbf
fgigbeeeabeabbabbababbaaaababbbabaaabbbaabaabbabaababbbbaaaabbbaabbabbbabababbab
bababbabbaaabbabaababbbaabbabbbabaafaedggeedfcbdabhhggcadcfeddgfdgbgigaaedggiafa
ecghggcdaihehahbahigceifgbfgefgaifabifagaegeacgbbeagfggeeggafbacgfcdbeiffaafcida
hgdeefghhcggaegdebhhegeghcegadfbdiagefcicggifdcgaaggfbigaicfbhecaecbceiaicebgbgi
ecdeggfgegaedggfiiciiififhggcgfgdcdggefcbeeigefibgibggghhfbcgifdehedfdagicdbhicg
aiedaehahghhcihdghfhbiicecbiichihiiigiddgehhdfdchcbafgfbhaheagegecafehgcfggggcag
fhhghbaihidiehhfdeggdgcihggggghadahigigbgecgedfcdggaccdehiicigfbffhggaeidbbeibbe
iifdgfdhieeeieeecifdgdahdiggfhegfiaffiggbcbcehceabfbedbiibfbfdedeehgigfaaiggagbe
iichiedifbehgbccahhbiibibbibdcbahaidhfahiihiczagdafaoaheiecggchgicbbhcgbehcfcoab
icfdhhcdbbcagbdaiobbgbeadeddezcfobfdhgdobdgooiigdocdaoofidhzshabefourfirsthintis
yourlastcommandU2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9za
bbaabababbabbbaabbbabaaabbaabababbbaabaQvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejU
qTvdWOX6nQjSpepXwGuN/jJshabefanstoo
```

### 6.1 Segmentation

| block | offset | length | alphabet | decodes to |
|---|---|---:|---|---|
| `dbbi` | [0,91) | 91 | `a..i` | exact prime-host relationships; residue role unresolved, see 6.3 |
| a/b run | [91,195) | 104 | `a`/`b` | `matrixsumlist` VERIFIED |
| `faed` | [195,765) | 570 | `a..i` | unresolved role; filler is a hypothesis, see 6.4 |
| `z` | [765,766) | 1 | separator | |
| segment 1 | [766,829) | 63 | `a..i`/`o` | `lastwordsbeforearchichoice` VERIFIED |
| `z` | [829,830) | 1 | separator | |
| segment 2 | [830,859) | 29 | `a..i`/`o` | `thispassword` VERIFIED |
| `z` | [859,860) | 1 | separator | |
| literal | [860,895) | 35 | text | `shabefourfirsthintisyourlastcommand` |
| base64 half 1 | [895,959) | 64 | base64 | |
| a/b run | [959,999) | 40 | `a`/`b` | `enter` VERIFIED |
| base64 half 2 | [999,1063) | 64 | base64 | |
| literal | [1063,1075) | 12 | text | `shabefanstoo` |

The segmentation traces to a solver's post (#7360); the creator never endorsed it.
The dbbi/faed boundary at 91 is confirmed independently (G-test of homogeneity
G = 36.44, df 8, p ~ 1.5e-5; no faed 91-window reaches dbbi's chi2 in 480).

### 6.2 The verified decode rules

1. **a/b runs**: `a` to 0, `b` to 1, 8-bit binary, ASCII.
2. **`a..i`/`o` blocks**: `a..i` to 1..9 and `o` to 0, read the digit string as a
   single **decimal integer**, convert to base 16, read as ASCII.
3. **`shabef`**: via a1z26, `sha` + `b`(2) + `ef`(5,6) gives `sha256`. The two
   literals read "sha256, our first hint is your last command" and "sha256 the answer
   too". `enter` is the line break: `openssl enc -a` wraps base64 at 64 characters.

"Our first hint" is identified from primary data: the creator's first hint is #225,
the bare phase-1 hash, followed by #226 "just try hit your options against that
hash", described by him in #257 as "A hash which we provided". The first hint was a
sha256, and the last command is one too. **Evidence for a method reading; it does not uniquely fix the operand.
The later creator-attributed reply #11248 identifies "Follow the white rabbit"
as a first-hint referent, and direct support messages independently establish
his use of that instruction. Preserve these as alternatives; neither selects
exact password bytes or the scope of the two SHA instructions.** Asked for help with it in 2024, he replied 🤐 (#20224).

```python
def rule2(block):
    d=''.join('0' if c=='o' else str(ord(c)-96) for c in block)
    n=int(d); h=hex(n)[2:]
    if len(h)%2: h='0'+h
    return bytes.fromhex(h)
# control: rule2(soup[766:829]) == b'lastwordsbeforearchichoice'
```

### 6.3 dbbi: exact structure, unresolved consumer

```
dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe
```

Walk logical positions from 1. Ordinary positions consume one character; prime
positions consume `b` for blue or `be` for yellow. The outer letter/digit mapping
also explains the host values: B=2 -> `b`, Y=25 -> `be` (record 112). Ordinary
characters are the residue; calling them filler is an additional interpretation.

**Insertion model, L=83.** Splice the off-white cell as a new blue marker at
position 21 of the original sequence:

    BBBBYBBBYYBBBBYBBYYBFYYBY       F = FEFEFE, treated as blue

Its first 23 symbols yield 15 `b` and 8 `be` hosts and consume all 91 characters
through logical position 83. It leaves B/Y unused. The reported insertion controls
reject F as yellow and dropping F under that model. Its reported shuffle tests
and C(23,8)=490,314 assignment enumeration support the exact structural relation;
the exhaustion acceptance rule was written after seeing the winner.

**Replacement model, L=84.** Preserve 24 markers and replace the final-bit yellow
marker in byte 21, rather than inserting an additional marker:

    original:    BBBBYBBBYYBBBBYBBYYBYYBY
    replacement: BBBBYBBBYYBBBBYBBYYBBYBY

Its first 23 symbols yield 16 `b` and 7 `be` hosts and consume all 91 characters
through logical position 84. It leaves one Y unused. Its 61-character residue is
the following 60-character insertion residue plus one trailing `e`:

```
difhccgihaeeihggegebgehhehhfafdhffcdbfcccgfeggecdcifffgigeea
```

The earlier statement **"L=83, settled" is withdrawn**. Both source-grounded
interpretations were already in the September 14 records. Attempt 118's claim
to have newly discovered replacement is also withdrawn (review 124). The shared
prefix is 82 logical cells; the final `be` changes from a yellow host to a blue
`b` host plus ordinary `e`. No old L=84 candidate/selector test becomes new.

**Residue statistics, preserved with their limits (doc 101).**

| symbol | a | b | c | d | e | f | g | h | i |
|---|---|---|---|---|---|---|---|---|---|
| insertion residue (60) | 3 | 2 | 8 | 4 | 10 | 10 | 10 | 8 | 5 |
| faed (570) | 54 | 49 | 52 | 49 | 69 | 57 | 107 | 58 | 75 |

The reported G-tests give p=0.26 against faed's distribution and p=0.11 against
uniform, with log-likelihood ratio +1.59 favoring the former model. This is
consistent with biased filler, but does not identify the generator, prove that
the residue is meaningless, or exclude an operand role. The exact parse verifies
a poster/prime relationship; its intended consumption remains unresolved.

### 6.4 faed, characterised

```
faedggeedfcbdabhhggcadcfeddgfdgbgigaaedggiafaecghggcdaihehahbahigceifgbfgefgaifa
bifagaegeacgbbeagfggeeggafbacgfcdbeiffaafcidahgdeefghhcggaegdebhhegeghcegadfbdia
gefcicggifdcgaaggfbigaicfbhecaecbceiaicebgbgiecdeggfgegaedggfiiciiififhggcgfgdcd
ggefcbeeigefibgibggghhfbcgifdehedfdagicdbhicgaiedaehahghhcihdghfhbiicecbiichihii
igiddgehhdfdchcbafgfbhaheagegecafehgcfggggcagfhhghbaihidiehhfdeggdgcihggggghadah
igigbgecgedfcdggaccdehiicigfbffhggaeidbbeibbeiifdgfdhieeeieeecifdgdahdiggfhegfia
ffiggbcbcehceabfbedbiibfbfdedeehgigfaaiggagbeiichiedifbehgbccahhbiibibbibdcbahai
dhfahiihic
```

Symbol counts: `a`54 `b`49 `c`52 `d`49 `e`69 `f`57 `g`107 `h`58 `i`75.

    memoryless             digram chi2 vs independence: P = 0.18
    aperiodic              no period 2..100: P = 0.71
    homogeneous            P = 0.45 at 19 blocks, once the last 32 chars are removed
    non-uniform            chi2 43.7 on df 8 (full 570), p = 6.4e-7;
                           chi2 52.8 (head 538), p = 1.2e-8
    entropy                3.120 of a maximum 3.170 bits per symbol

The final 32 characters contain no `e` and no `g` (permutation P = 0.0040); BIC does
not support a split. Carry faed as one object.

**The `g` count and the merged-zero model.** `g` = 107 is almost exactly double the
~57 mean of the other symbols. faed fits well as uniform decimal digits in which `g`
carries both 7 and 0 (chi2 11.5 on 8 df, p = 0.175, doc 16). Two versions are closed:

- **As printable text** (doc 90): an exhaustive search over which occurrences of each
  symbol are really `o`, with pruning on bytes already fixed, recovers both control
  segments with their zeros hidden and finds **zero solutions** for dbbi, the residue,
  faed, faed[0:538], faed's tail and dbbi+faed, forward and reversed.
- **As a binary payload against the locks** (doc 109): every letter as the hidden zero
  over every subset of its occurrences for the residue (3,644 choices), the faed tail,
  and dbbi's `e` (2^18); 144 structured zeroings of five objects (primes, prime
  ordinals, parity, complements); outputs as integer bytes and hex, forward and
  reversed, as raw passwords and sha256 hex under both digests. About 16.8 million
  decryptions, then re-run under the structure-agnostic recogniser with lock chaining
  (doc 110). Null.

**Open by size alone:** faed with arbitrary `g` choices (2^107, not enumerable) and
dbbi with `b` as the zero (2^25, enumerable, low prior because `b` marks the hosts).

**Conclusion: faed's role is unresolved.** Biased filler is a plausible model;
nonuniformity, failure to detect dependence and failed decoders do not prove it.
Nor does nonuniform displayed text exclude modern ciphertext followed by a biased
encoding. Asked whether dbbi/faed were decoded or used as ingredients, the creator
replied 🤐 (#70325), which selects neither role.

Record 111 completed 810 constrained EBCDIC/mixed/UTF-16 merged-zero searches with
zero candidates; records 114–117 add bounded split, cumulative-sum, prime-subsequence
and keyed-zero exclusions (section 10.8). Their exact models are closed, not every
possible FAED consumer. Decoder searches and pair statistics already exist for
GI and HE; the pair itself remains unselected. Do not repeat them for a new score.

### 6.5 The three locked containers

All three begin `Salted__`. **No password is known for any of them.**

| container | ciphertext | salt | sha256 |
|---|---:|---|---|
| Terminal / P3.2 | 80 B | `b45a5e3d827593ca` | `291dfd6f3e759ec2e272b35a00c24907da70c3e7a9291b4c13605c7b0b4f3de9` |
| SalPhaseIon short | 80 B | `3ab585348552415d` | `9e2831e1b34b5f34796df47ccaf6530d48d371c61a6bff84d60db1064fa7a258` |
| Cosmic Duality | 1328 B | `2d3f6fe06dc950e6` | `b18950551a4dd0cb8a9378f0906ba18c03a15f0ee83eb98c6bc90165c5f79805` |

All three generated from verified files. Terminal (the end of the phase-3.2
plaintext):

```
U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46zgKlIi8aaqY5gpJPP
EzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4
```

SalPhaseIon short (the two base64 halves of the textarea, joined):

```
U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9zQvX0t8v3jPB4okps
pxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ
```

Cosmic Duality (the second textarea on the side page):

```
U2FsdGVkX18tP2/gbclQ5tNZuD4shoV3axuUd8J8aycGCAMoYfhZK0JecHTDpTFedGJh4SJIP66qRtXv
o7PTpvsIjwO8prLiC/sNHthxiGMuqIrKoO224rOisFJZgARic7PaJPne4nab8XCFuV3NbfxGX2BUjNke
f5hg7nsoadZx08dNyU2b6eiciWiUvu7DSATSFO7IFBiAMz7dDqIETKuGlTAP4EmMQUZrQNtfbJsURATW
6V5VSbtZB5RFk0O+IymhstzrQHsU0Bugjv2nndmOEhCxGi/lqK2rLNdOOLutYGnA6RDDbFJUattggELh
2SZx+SBpCdbSGjxOap27l9FOyl02r0HU6UxFdcsbfZ1utTqVEyNs91emQxtpgt+6BPZisil74Jv4Emrp
RDC3ufnkmWwR8NfqVPIKhUiGDu5QflYjczT6DrA9vLQZu3kok+/ZurtRYnqqsj49UhwEF9GfUfl7uQYm
0UunatW43C3Z1tyFRGAzAHQUFS6jRCd+vZGyoTlOsThjXDDCSAwoX2M+yM+oaEQoVvDwVkIqRhfDNuBm
Efi+HpXuJLPBS1PbUjrgoG/Uv7o8IeyST4HBv8+5KLx7IKQS8f1kPZ2YUME+8XJx0caFYs+JS2Jdm0oj
Jm3JJEcYXdKEzOQvRzi4k+6dNlJ05TRZNTJvn0fPG5cM80aQb/ckUHsLsw9a4WzhHsrzBQRTIhog9sTm
+k+LkXzIJiFfSzRgf250pbviFGoQaIFl1CTQPT2w29DLP9006bSiliywwnxXOor03Hn+7MJL27YxeaGQ
n0sFGgP5X0X4jm3vEBkWvtF4PZl0bXWZLvVL/zTn87+2Zi/u7LA6y6b2yt7YVMkpheeOL0japXaiAf3b
SPeUPGz/eu8ZX/NnO3259hG1XwoEVcGdDBV0Nh0A4/phPCR0x5BG04U0OeWAT/5Udc/gGM0TT2FrEzs/
AJKtmsnj31OSsqWb9wD+CoduYY2JrkzJYihE3ZcgcvqqffZXqxQkaI/83ro6JZ4Pubml0PUnAnkdmnBC
pbClbZMzmo3ELZ0EQwsvkJFDMQmiRhda4nBooUW7zXOIb7WxbE9THrt3cdZP5uAgVfgguUNE4fZMN8AT
EDhdSsLklJe2GvihKuZVA6uuSkWAsK6uMGo76xpPwYs3eUdLjtANS83a6/F/fhkX1GXs7zbQjh+Inzk8
jhEdEogl9jPs/oDjKjbkUpFlsCWwAZGoeKlmX7c4OGuD5c+FEH+2nYHvYl8y1E/K5SDt9Uocio8XuxbD
ZOzhw7LMSGkD1MZxpDzsCZY1emkSNd88NFj+9U8VssIDDVMYwKMsHKfjc0x5OlzQ1f6ST0xCkwydDHHG
RKKxFC4y6H6fV9sgf9OPK/65z94Rx72+mfvTyizShjxYSRplsH9otU4parl8roD0KsVTfXZoYrYXzK6c
XBn1BO/OEqWlu++Dd9MiGaUGKd22fXERqNWoRAKlNn2b6EehD2D8WaAoliPURjkB0Lb/FpP9unI93Twg
6NxBXAj734nctukRb3kE08RydJV70eJsvEftF5hbED4HacGx9pzisaSz6t9AKiuSoF6uoCtlTIYatyfZ
kQA4wg50hAJqTynOQ09ArRHEchtB/7uvWZSBGJ7+zlzRGKx99P3oDZD+Y5D8bmUs3PV6FnAp+IRSlnsQ
6hChkwBoQUcngcfGSkBRvmGjsGercCetRRwBOfh9fbX2ruw4mzRYrGnz9eBtepkJXDRjD6yvhNfQMCSk
m6l9zMWxKvFbv5g2ae2SLrEt/x3MP2/G
```

**Plaintext length bounds, conditional on AES-CBC/PKCS7.** 80 ciphertext bytes
permit 64–79 plaintext bytes; 1,328 permit 1,312–1,327. A bare 64-hex key, a
64-byte binary pair and some URLs fit the short bounds. Bare WIF/BIP38 strings
do not fit alone under this framing. Length does not identify plaintext type:
Cosmic may contain text, structured binary data, keys, or an inner envelope.
Other cipher/framing hypotheses have different bounds.

The two 80-byte containers are two objects (separate headers and salts, no shared
block, no salt XOR structure). The salts are almost certainly `openssl`'s random
values. The byte-level XOR and interleave of the two ciphertexts, their salts and
first blocks, and each container keyed by another's text or bytes, are null (docs 103,
107).

**Stage order is not uniquely selected.** The threaded creator reply #39237
calls yinyang "the next phase" in response to a question about finding it after
an AES decode. This supports an ordering relation, not an identification of
yinyang with Cosmic's plaintext or SalPhaseIon as the next gate. Keep all three
authenticated targets distinct and record the target of each actual attempt.
No new test is warranted solely by rearranging an assumed stage order.

**The Terminal has no riddle beside it (doc 96).** Every other locked object has its
instructions adjacent. The object immediately before it is the checkerboard message
("in case you manage to crack this, the private keys belong to half and better
half..."), which reads as a warning attached to the Terminal. Asked "is the PK in the
last cipher of 3.2?", the creator answered "There must at least be something hidden in
there" (#2918); the last cipher of 3.2 is the Terminal. Either its instructions are the
SalPhaseIon page (the Architect's "return to the source codes") or it is the object
the stakes are raised on ("raising the stakes without extra chances of winning").

---

## 7. THE CREATOR'S DECODED ARTIFACTS

### 7.1 Message #8446, 23 Feb 2023

161 bytes written as 8-bit binary numbers. Reversing the whole bit stream reads as
ASCII (generated from the export):

```
yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyangwewontgiveawaythep
assworditsinfrontofyoureyesbutyourenotseeingitverylaststepisatruegiveawaypromise
d
```

    yellowblueprimes             exact poster/dbbi relationships; intended consumer open
    matrixsumlist                decoded label; operand and operation unselected
    lastwordsbeforearchichoice   decoded label; referent/operation/consumer unselected
    yinyang                      downstream state/operation not identified

Then: "we wont give away the password its in front of your eyes but youre not seeing
it very last step is a true giveaway promised". The creator later answered "Bingo" to
a reading of this line as Jacque Fresco's book *Looking Forward* (section 8.1).

### 7.2 The Roses poem, message #1710, 14 Jan 2020: the planned final hint

```
Roses are White but often Red.
Yellow has a number and so does Blue.
Go back to the first puzzle piece without further ado.

It might have shown you only one door, beware that the rabbits nest may contain a
whole lot more.

Hush hush.
```

**It was planned at design time.** At the start of 2020 the creator announced that a
tiny hint "will be the final hint", and that the key can be retrieved without it
(#881). He re-pointed to the poem on 2020-05-20 (#4096 "This one") and said "answer is
there" (#4102). It is the most authoritative hint in the corpus (doc 103). "First or
zero" (#4105) answers a question about which piece is "the first puzzle piece" (rabbit
poster = piece zero, rebus = piece one); it is not a general indexing convention
(doc 39), though it fits the cell test in section 4.3.

**It is *Alice in Wonderland*, Chapter VIII, "The Queen's Croquet-Ground" (doc 104).**

| poem | *Alice* |
|---|---|
| "Roses are White but often Red." | Ch. VIII opens with three gardeners painting a white rose-tree red, because a white tree was planted by mistake where the Queen wanted red |
| "Yellow has a number and so does Blue." | the gardeners are numbered playing cards: **Two, Five and Seven**, all prime |
| "Go back to the first puzzle piece" / "the rabbits nest" | the White Rabbit on the poster; the rabbit hole |
| "It might have shown you only one door" | Ch. I: a hall of locked doors, and a tiny golden key that fits one small door |
| "Hush hush." | Ch. VIII: the White Rabbit's own words, "Hush! Hush!" |

The puzzle already quotes *Alice* in the phase-3 riddle (the Cheshire cat, falling in
the keyhole). Read through Ch. VIII, the planned final hint names the prime set
**{2, 5, 7}**, without 3; compare #5963 ("just say which primes 2,3,5,7 we need use")
and the creator's "You are at the prime part already???" (#5966). The gardeners' task,
painting white to red to hide a mistake, is an operation on a white cell, which lines
up with #8000's characters "zeroed out" and with the painted `#FEFEFE` cell (section
4.3).

With the nest pixels empty (section 4.4), "the rabbits nest may contain a whole lot
more" points at doors: the rabbit hole leads to a hall of many locked doors. That
matches "there is another door" (#7914, #8000) and describes the site's door
structure rather than pixels. #9607 ("is there another URL to find?" -> "No need. You
have all the info.") says any such door must be derivable from what solvers hold.
Zeroed poster text as a second HASHTHETEXT door is null (doc 106).

### 7.3 The New Year "tiny hint" and the dot convention (#53335 to #53342)

On 2025-12-31 the creator posted five messages of 1, 2, 3, 4 and 5 dots, then a
binary message that decodes (from the export) to:

    Happy new year! Make the best of everything. Oh, and here's a "tiny hint" <3.

The quotation marks around "tiny hint" point back at the dots. Across the chain the
creator elides words as **one dot per letter**:

| location | dots | elided | status |
|---|---:|---|---|
| phase-3 riddle 1, "the ...... is ours" | 6 | CHOICE (*The Choice Is Ours*) | verified by the chain |
| phase-3.2 intro, "... am I here?" | 3 | WHY (Neo's line to the Architect) | exact film line |
| checkerboard key `ORA.LE` | 1 | C | verified, forced |
| #8311, reply to the Cosmic Duality cover | 4 | unknown | open |
| #53335 to #53341 | 1 to 5 | unknown | open |

The obvious fills are screened and null (section 10.6).

### 7.4 The Cosmic Duality cover, #8310, verified

The export's file for #8310 (`image_2022-12-11_07-09-14.png`, barrystyle,
2022-12-10) is the cover of Time-Life *Mysteries of the Unknown: Cosmic Duality*: a
starry yin-yang whose two seed dots are a white light (upper half) and a yellow light
(lower half). barrystyle found it by searching the page heading ("honestly, i just
searched for cosmic duality: mysteries of the unknown", #26257), so it reflects no
hidden insight. The creator's reactions are to the book itself: ".... That is very
specific" (#8311) and "If the puzzle is solved you'll see how scary specific that is"
(#8315). The book's page-9 caption reads: each half of the yin-yang "holds the seed of
its opposite: the dark yin contains a tiny speck of yang, and the paler yang embodies
an embryonic germ of yin". The seed, the planting and the opposites all sit in the
song line that built the URL (section 3.A). Every contiguous passage of the book is
screened and null; the seed-of-the-opposite operation is screened and null (section
10.6).

---

## 8. THE HINT CATALOGUE

Every id was checked verbatim against the Telegram export. Attributed to Jrk Bgrt /
SoWut. All 492 creator messages were re-read against their parents on 23 September
(doc 103); section 8.6 lists what that changed.

### 8.1 Endorsements, with the message each one answers

Built by pairing every creator endorsement (Bingo, Correct, Good point, Well spotted,
Interesting, specific, 👆, ✅, 🤐, "might have been a hint") with its parent: the reply
link where one exists, otherwise the nearest preceding non-creator message.

**`matrixsumlist` is a prime operation.**

```
5952 Janusz   ...hundred FOUR = 104 is the fefefe square fefefe is 101 010
5958 Janusz   AND OR logic gates
5960 Jrk      Ancient spelling. One of the many many typos.   (reply to 5952)
5963 Janusz   just say which primes 2,3,5,7 we need use
5966 Jrk      You are at the prime part already???
5969 Jrk      Oh wait, shouldn't have said that. That might have been a hint.
6508 anon     So don't you think it's time for a hint on matrixsumlist?
6509 Jrk      I gave an unforseen hint already            (reply to 6508, 14 Mar 2021)
```

#5966/#5969 (1 Mar 2021) is the only self-described accidental hint before #6509.

**"Bingo" to *Looking Forward*.**

```
60298 Jrk     Jacque was quite an inspiring lad I'd say.
60304 DG      Wasn't "it's in front of your eyes but you're not seing it" a
              recomendation to read "Looking forward" btw.? Was it a plan?  (reply to 60298)
60308 X       ...you need to hint us about the direction.
60309 Jrk     Looks at gnomad.                                              (reply to 60308)
60310 gnomad  Looks at DG's comment "its in front of your eyes but you're not seeing it"
60311 other   [unrelated quip]
60312 Jrk     Bingo
```

*Looking Forward* (Keyes and Fresco, 1969). **Attribution caveat:** an unrelated
message sits between 60310 and 60312, and its author took the Bingo as his (#60317).
On balance it answers gnomad.

**The Hope line answers a question about the door.**

```
3389 Tracer   The door that leads to the source?
3390 Jrk      Humph. Hope, it is the quintessential human delusion, simultaneously
              the source of your greatest strength, and your greatest weakness.
3391 Jrk      (not a hint btw, just fooling around)
```

This exchange was screened as literal text (section 10.6). The saved screenplay
and transcription place Neo's physical movement toward the door after "stop it",
before the Hope speech (record 112). Hope precedes the door's opening, not that
movement. "Choice" could instead mean the spoken word or another boundary;
none of these referents is selected just by the label.

**Other endorsements with their parents.**

| creator | parent | note |
|---|---|---|
| #2905 "Interesting" | #2899 spiral grid with the `#FEFEFE` cell marked | then #2918 "There must at least be something hidden in there" (answering whether the PK is in the last cipher of 3.2) |
| #3902 "Well spotted" | #3901 "the half of prize went to better half" | the halving |
| #4096 "This one" | #1710 the Roses poem | then #4102 "answer is there" |
| #4696 "Correct" | #4695 "Is it the next stage of the second route?" | 2020 second door |
| #7418 "Good point" | #7416 "go to the first puzzle piece (image) and hash all the text you see" | HASHTHETEXT |
| #8311 ".... That is very specific" | #8310 the Cosmic Duality cover | section 7.4 |
| #8483 "👆" | #8448 the reversed #8446 decode | confirms the decode |
| #12653 "Correct" | #12580 "the blockchain messages are not his and are not part of the puzzle" | |
| #20224 🤐 | #20222 a request for help with "our first hint is your last command" | |
| #66600 "Some already found it. And understood not to risk it" | #66599 objection to #66593 | "it" is the larger prize |
| #70307 "Pfff. Coincidence." | the DBBI-minus-checkerboard "YOUWON" pivot | section 10.5 |
| #70325 🤐 | #70324 "were dbbi and faed meant to be decoded, or only an ingredient?" | no direction |

**Reviewed and dismissed.** #60313's "ying yang… salvation" from prime indexes is, by
its author's own account (#60347), anagrams crafted by hand from extracted letters.

### 8.2 On primes and zeroing

| id | date | text |
|---|---|---|
| #8000 | 2021-12-26 | "The previous 'there is another door hint' is still a thing. ... prime numbers ... definitely an aspect which is required to proceed. Furthermore, along the way, some characters need to be 'zeroed out'.." |
| #5966 | 2021-03-01 | "You are at the prime part already???" (section 8.1) |
| #8328 / #8330 | 2023-01 | "@barrystyle, provided a very specific hint already." / "At least prime number is very important to get any further." |
| #32613 | 2024-11-29 | "I think I'll be going for ASCII 127 myself." Answering "What character do I have to imagine myself as?"; DEL is the last command in ASCII and 127 is prime |
| #66931 | 2026-07-16 | "You have to be in your prime for that." |

The planned final hint's prime set is {2, 5, 7} (section 7.2).

### 8.3 On the endgame and its order

| id | date | text |
|---|---|---|
| #9599 | 2023-08-06 | "Probably the last hint: Once you hit a 'ying yang', you'll be able to solve it the same day." |
| #39224 | 2025-04-28 | "Did anyone found yingyang? I don't think so... when yingyang is reached, 2 hours max." |
| **#39233 -> #39237** | 2025-04-28 | "is yinyang found after decoding an AES ciphertext?" -> **"It's the next phase, but I await the day someone finally gets there."** Threaded reply; the best-sourced ordering statement |
| #60314 | 2026-03-03 | "If any of you reaches the next phase, the price is taken in no-time." |
| #7832 / #7834 | 2021-08-11 | the solver finds an *encrypted* private key and "will find a way to 'decrypt' it". "Encrypted private key" is BIP38's own term; the scare quotes around decrypt fit a non-AES final step |
| #4624 | 2020-08-09 | "private key or seed phrase or phrase for brain wallet?" -> **"a private key"** |
| #20223 | 2024-01-26 | "Regular Bitcoin Private key" |
| #24627 | 2024-04-19 | "There are few prizes to win... A private key, some 'obscure' intel, or... the most obvious reason to make sure you hold on to Bitcoin" |
| #32579 | 2024-11-29 | "If you guys got 1 microstep further, the puzzle will likely be solved the same day." |

### 8.4 The 2026 statements

| id | date | text |
|---|---|---|
| #66568 | 2026-07-12 | "I have a hidden laptop which I haven't touched in years. On that thing... is the actual answer...." |
| #66571 | 2026-07-12 | "Some of you, can find me. Quite a few in this chat, already met me." |
| #66573 + **#66574** | 2026-07-12 | "My close friends have the best chance of solving it (a few tried). But they don't have the skills some of you do." **"NOTE: that is a hint."** |
| #66592 / #66593 | 2026-07-12 | "I held quite a secret in my head..." / "The '5' btc was never the actual prize. That was only a tiny fraction." |
| #66587 -> #66588 | 2026-07-12 | "salphaseion is 100% solveable?" -> "Yes" |
| #66589 / #66590 | 2026-07-12 | "...it's all still solvable with a few stable qubits." / "But... Bip360 anyone." |
| #66898 | 2026-07-16 | "Had my eyes closed, but still saw double." (standalone; beside #8446's "in front of your eyes") |
| #66903 | 2026-07-16 | "Well, it's hidden in a room with a hidden door." |
| #66938 | 2026-07-16 | "in a matrix cypher kinda way" (Cypher, the character; or a matrix cipher, i.e. Hill) |
| #66961 | 2026-07-16 | "Give yourself yourself and yourself will be given yourself." (standalone; tested as each container keyed by itself, null) |
| #66962 | 2026-07-16 | "Latetly, I'm working with many NOTES." (reply to someone awaiting a "NOTE: that is a hint" moment) |
| #70336 | 2026-09-01 | Asked how long the puzzle took and whether he worked alone: "Couple hours, and no." |

Read together, the 2026 cluster describes a physical machine in a physical place and a
prize larger than the 5 BTC. That reading is in tension with "You have all the info"
(#9607) and "is internet still required? Nope" (#16624). **It is also where the
cryptanalysis stops.** Acting on it would mean locating a private individual. That is
outside this project; the standing rule against contacting the creator applies.

### 8.5 The documented mistake, and statements that rule things out

| id | effect |
|---|---|
| #866 / #867 / #3384 | the phase-3 mistake, fixed by `giveit = givetit`; "The biggest blunder so far in the mainline of the puzzle" |
| #1806 | "Typos: ... No clues to be found in those typos." |
| #5960 | "hundred fourty" is "Ancient spelling. One of the many many typos." (the spelling, not the number) |
| #7529 | the 1 Apr 2021 `{1},{4},{21}` post was an April Fools joke |
| #9607 | "is there another URL to find?" -> "No need. You have all the info." |
| #12653 | on-chain OP_RETURN messages are not part of the puzzle |
| #16624 | "is internet still required to solve it?" -> "Nope." |
| #32699 / #32701 | the `/Puzzle` app page "doesn't affect the puzzle"; "we had a few FE guys working on it" |
| #60326 | the binary contact info on jrk.agency has nothing to do with the puzzle |
| #66584 | the original URL "and thus the original puzzle" is gone |
| #898 / #60289 | "No hints after stage 2"; "No hints, only free will". Both said, both since broken |

### 8.6 Re-read of all 492 creator messages, 23 September (doc 103)

| id | text (short) | reading |
|---|---|---|
| #881 | a tiny hint at the start of 2020 "will be the final hint"; the key can be retrieved without it | the Roses poem was planned as the final hint (section 7.2) |
| #1647 to #1703 | cake photo, "No, it's a dessert", "not trolling with scripted cake this time" | the Merovingian's programmed dessert, the tail of the phase-2 URL. He builds hints from that scene |
| #2918 | "There must at least be something hidden in there" | answers "is the PK in the last cipher of 3.2?"; that is the Terminal |
| #3404 | "And Oen" | unexplained. One and Neo are both anagrams |
| #3923 | "The price is in half, but what does it mean" | with the checkerboard message and #9595, a split |
| #9595 | "my friends and family can get to all my data if they'd work together" | two or more holders combining |
| #7832 / #7834 | the encrypted private key is stored online | section 8.3 |
| #8354 / #8385 | "the theory of everything is also still a valid path"; a bare "42" | the phase-2 template's `H` slot |
| #17891 | "Have you tried the purple pill already?" + "Candy flipping" | purple = red + blue; combining two |
| #23159 | "I prefer superpositions" (to "are you a one or a zero?") | the in-between state; the off-white cell |
| #60324 | "rewatch episode 3.5 with the better half" | the `eps3.4_runtime-error.r00` episode again |
| #66938 | "in a matrix cypher kinda way" | Cypher, or a Hill cipher |
| #66961 | "Give yourself yourself..." | a container opened by itself (null) |

Every reading above was screened alone, with the labels, and in pairs: 7,368
candidates plus 30,000 double-hash screens, null.

---

## 9. THE CURRENT MODEL OF HOW THE PUZZLE IS BUILT

The verified labels and exact structural relationships do not yet define a
complete password derivation. Adjacent-block and external-operand readings remain
alternatives. No source proves that all a..i material is filler or that the
operands must lie outside the SalPhaseIon page.

| Object | Established | Still missing |
|---|---|---|
| Poster/dbbi | two exact local prime-host models, L=83 and L=84 | intended model, residue role, consumer |
| FAED | authenticated 570 symbols and recorded distribution | operand role, decoder/operation, pair selector |
| matrixsumlist | exact decoded label | dimensions/source, value mapping, sums and serialization |
| lastwordsbeforearchichoice | exact decoded label | referent, word boundary, operation and output role |
| thispassword | exact decoded label | what expression it refers to and which lock consumes it |
| SHA instructions | SHA256 reading and prior hash-method precedent | preimage boundaries, representation and application count |
| enter/base64 pieces | reconstructed authenticated short envelope | password and plaintext role |
| yinyang | exact macro token; creator-supported downstream phase wording | operator, artifact or consumer identity |

### Recovered six-digit-prime macro hypothesis (review 124)

This branch pre-exists the current session and is not a new solve:

    Original 24 markers, Y=1 / B=0
        000010001100001001101101 = 574061, prime
    Six decimal digits as a 2x3 matrix
        [5 7 4]
        [0 6 1]
    Total, first-row sum, second-row sum
        [23,16,7]
    One-based words at the frozen pre-"choice" Architect speech
        BOTH / ULTIMATELY / THE
    Word beginnings / endings
        BUT / HYE

The saved film and screenplay extractions agree on the selected words; `BUT`
is the first Architect word after the selected spoken `choice` boundary. This
is a useful boundary match. It does not independently select every upstream
choice: polarity, 2x3 layout, sum order, scope and word-edge extraction remain
part of the hypothesis. Its next consumer is unresolved. Older mirror/BYE
continuations and direct passwords were already investigated; do not repeat them.

**Do not combine models by globally repainting the source.** Under the fixed
macro interpretation, global byte-21 replacement gives `574053=3x191351` and
`[24,16,8]`; global insertion gives `1148109=3x382703`, seven digits. Both lose
the recorded prime consumer. Retaining this macro branch therefore requires
the off-white adjustment to remain local to dbbi parsing. That constraint
selects neither parse and proves neither branch is intended.

The song and *Alice* connections remain coherent thematic readings. Translating
them into a particular matrix, zeroing mask or password still needs an operator
and operand. The explicit creator zeroing instruction does not name its
characters or representation. The September 13 source/context review already
examined that gap without finding a complete recipe.

The checkerboard's "half and better half" can describe people/ownership. It does
not uniquely require two 32-byte halves, two containers, combination arithmetic,
or recovery of the halving recipient's key. Terminal's adjacency and #2918 make
it relevant, but neither its output type nor the other containers' order is fixed.

The earlier successful stages support the answer -> lowercase SHA256 hex ->
EVP-SHA256 -> AES-256-CBC convention. Use that as evidence about the method,
not as a substitute for deriving the exact answer or proving the unopened profile.

---

## 10. WHAT HAS BEEN TRIED AND FAILED

Historical reports below preserve the stated scopes and counts; not every
original manifest or script is available. Rows are exclusions of their specified
constructions, not proofs that an entire source or cipher class is exhausted.
Do not add overlapping counts as unique attempts. Sections 10.8 and 12 contain
the current state; audits 120–121 distinguish execution evidence from missing records.

### 10.1 The corpus against the containers

| what | scale | result |
|---|---:|---|
| every combination of the 29 decrypted objects against Cosmic Duality: every chain-order subset and every ordering up to five atoms | 551,714,300 | 123 block-1 survivors against 117 predicted by noise, **0 confirmations** |
| all 2^30 corpus subsets against all three containers, with the dbbi residue and the header coordinate added as atoms, both solved containers firing as in-space controls | 2^30 | null |
| the solved vocabulary and every single-character corruption of the four multi-part answers, under eight ciphers and two KDFs | 7,163,600 decrypts | 1 hit, noise on full-length confirmation |
| SafeNet/Luna vocabulary | 12,395 candidates | null |
| the creator's world as a 384-string generator | 475,808 decrypts | null |
| frames for "last words" / "our first hint" | 1,808,960 decrypts | null |
| the film's pre-door lines as "last words" | 6,720 decrypts | null |
| four-slot concatenation plans | 2.7M + 5.5M phrases | 0 hits |
| acceptance test for raw binary keys | 215,550 configs | 0 hits |
| pad-8 recogniser, KDF/cipher matrix, CBC and ECB | 4,153 x 5 x 3 | 0 hits |

### 10.2 faed: documented model exclusions

| family | scale | result |
|---|---|---|
| uniform displayed-symbol model | distribution test | nonuniformity established; modern encryption followed by biased encoding is not excluded |
| tested positional/random-text model | reported distribution comparison | rejects the assumed encoding model, not every encoded payload |
| zero-reinsertion | exhaustive to k<=18, 18.8 billion nodes | 0 survivors |
| zero-substitution (a symbol stands for both its digit and 0), as text | exhaustive, all nine symbols, six objects, both directions | 0 solutions (doc 90) |
| zero-substitution as a binary payload against the locks | ~16.8M decryptions, then the recogniser with chaining | 0 (docs 109, 110) |
| running key, aperiodic, 17 key sources, every offset to 1400 | 1,132,326 | nothing beats the ciphertext |
| short periodic key, periods 2..100 | 99 | P = 0.71 |
| straddling checkerboard / VIC, all 45 escape sets | 45 | P = 0.9225 |
| the phase-3.2 checkerboard reused on residue, dbbi, faed, every zero choice | 3 objects x 18 | below each block's own shuffle null (doc 101) |
| columnar transposition, widths 2 to 120 | 119 | P = 0.83 / 0.91 |
| homophonic substitution, all 21,145 set partitions | 21,145 | P = 0.2233 / 0.4300 |
| binary partitions under rule 1 | 2,976 | 0 hits |
| simple text-substitution hypothesis | reported dependence test | no detected memory; not a universal substitution exclusion |
| hand-typed filler hypothesis | reported randomness battery | disfavors the modeled human process; generator identity not proven |
| all 362,880 symbol relabelings | 2,903,040 | 0 |
| every substring of length >= 8 of the five letter objects | 1,556,802 | 0 |
| faed as a matrix: row and column sums at every width dividing 570, as ASCII | 28 lists | noise (doc 96) |

### 10.3 The passphrase-screen sweep

The historical summary reports the candidates below screened against keys and
containers with controls. Exact historical membership/settings are incompletely
recovered; this row count is not a globally deduplicated execution ledger.

| family | candidates |
|---|---:|
| base-9 keystreams | 188,352 |
| mod-26 Vigenere and Beaufort, faed as key | 632,944 |
| byte-level faed codecs against the plaintexts | 13,536 |
| all relabelings of faed, dbbi and the residue | 2,903,040 |
| every unique string in the research archive, also as its own sha256 | 1,933,638 |
| every substring of length >= 8 of the five letter objects | 1,556,802 |
| **total** | **7,228,312** |

Result: 0 key hits. One pad-3 on Terminal (faed relabeled `heacgdibf`), noise.

### 10.4 The poster and the rebus

| what | result |
|---|---|
| poster program applied to faed, all L | chance |
| the method generalised to 18 chain strings | control fires on dbbi (0.913); nothing else above null |
| black/white cells as a consume-1/consume-2 program | base rate |
| faed prime-position composition | p = 0.77 |
| nine symmetry tests including the 180-degree anti-symmetry of a yin-yang | chance |
| the rabbit as a bitmap and as per-cell ink counts | nothing |
| the rabbit's nest at sub-pixel level, every reading order (doc 105) | best 0.64 printable, 0 hits |
| `#FEFEFE` as a bit-level prime pointer | 748 transforms, null |
| the gardeners {2, 5, 7} on the 196 spiral bits: select, paint, zero, every subset (doc 104) | 126 transforms, noise |
| 13,264 rebus-derived passphrases | 0 |
| poster stego, grid crop, all 8 rebus tiles | none |

### 10.5 Other closed lines

| what | result |
|---|---|
| the live verifier, 10 submissions | phase-1 only; do not submit more |
| 481 hand-visited door paths on the live site | null |
| the "Infrared" hint (#6250), three readings | negative; the hint itself is unexplained |
| `matrixsumlist` as key-operation-payload; theorem: no stream is a row+column sum list | null |
| the community "solved Cosmic Duality" claim, and the MD5 EVP re-derivation | **pad = 1 false positives**; 808 of 200,000 random passwords produce the same kind of 1,327-byte noise; 605,214 MD5/SHA-256 content-judged decrypts, 0 |
| the DBBI-minus-checkerboard "YOUWON" pivot | cannot coexist with the prime grammar (#70307 "Pfff. Coincidence.") |
| the archived pages' HTML, every string | 1,670, 0 |
| the corrected recogniser (pad 1 and 2 content-checked) over 807,585 archive strings | 0 |
| relabelings of residue, dbbi, faed tail, faed, faed head under the corrected recogniser | 1,814,400, 0 |
| the tag alphabet under two codecs and Morse | null; superseded by the format-spec reading (section 3.3) |
| "on the highway" as 33 glosses | 264, 0; consumed as the A15 (section 3.2) |
| "our first hint" candidates | 237, 0 |
| `matrixsumlist` executed on the grid: row and column sums in 14 variants x 12 encodings | 1,224, 0 |
| the literal last words before the Architect ciphertext | 120, 0 |
| the rabbit ink as a program | chance |
| the L=84 residue against the poster | 0 |
| `matrixsumlist` computed of the streams at every factorisation | 7,480, 0 |
| poster rows and columns as 14-bit numbers | ~200, 0 |
| yin-yang-shaped operations on the binary objects (complements, half-combinations) | 304, 0 |
| `F` as consume-0 in the insertion walk | negative under that model; L=84 byte-marker replacement is a separate exact fit |
| the riddle-block vocabulary, alone and spliced into every join | ~590,000, 0 |
| derived-key constructions (XOR, HMAC, PBKDF2 of corpus pairs) under both password profiles | ~38,000, 0 |
| the dbbi residue as a number | 0 |
| prime-position zeroing of published text | null everywhere |
| the 479 prime-sum pointer: 42 traversals x 3 `#FEFEFE` treatments, 263 numbers | 3,196 screens, 0; consistent with chance (section 12) |
| creator-authored single tokens and short messages | 8,812 strings, 0 |
| Neo's passport (11 Sep 2001) | 307, 0; conversational, not a hint |
| `{eps3.4_...}` clause and the episode's strings | 1,586, 0 |
| the 2026 OP_RETURN stream | 379, 0 |

### 10.6 Session of 22 September 2026 (docs 90 to 94)

Harness for every row: win test on both point forms (key 1 validated), all three
containers, both password profiles (sha256 hex and raw), both EVP digests (SHA-256
and MD5), padding then content. Controls: `causality` opens phase 2; a planted 79-byte
pad-1 plaintext is caught. Liveness measured on every run (for example 1,092 valid
pads against 1,050 expected over 268,728 decrypts).

| what | scale | result |
|---|---:|---|
| zero-substitution under rule 2 (section 6.4) | exhaustive | 0 solutions |
| dot-convention fills and crosses (section 7.3) | ~1,100 | 0 |
| Paint palette hex values, 1 to 3 permutations | ~700 | 0 |
| camelCase (`aBa`) and separator forms of the labels, 2- to 4-label permutations | ~1,300 | 0 |
| every 2- to 6-word compound inside every creator message, no stop-list | 19,321 | 0 |
| *Cosmic Duality* (Time-Life), every 1- to 12-word run from two OCR versions, plus ISBNs and titles | 1,889,907 | 0 key hits; two pad-3 events, both random bytes, ~1.4 expected |
| seed-of-the-opposite on the poster (4 neighbourhood rules, split by type, designed cells) and on every textarea block: flips, extracts, zeroing, absorbing, positions into six texts | 945 + hex | 0 |
| the yellow-39 / `#FEFEFE`-163 "two seeds" pair (priced about 1 in 70, criterion post hoc) | 55 | 0 |
| *Looking Forward* title, authors and label crosses | 944 | 0 |
| *Looking Forward*, every 1- to 12-word run from three Internet Archive OCR scans | 1,311,445 | 0 |
| the Hope line in the creator's and the film's wording, with the following exchange, crossed with every label | included above | 0 |
| three-slot cross: 10 `yellowblueprimes` outputs x 58 `matrixsumlist` outputs x 25 last-words candidates, every order, with and without `thispassword` | 82,710 | 0 |
| `phase3.1_old.aes` | 1 | a re-encryption of the known plaintext |
| prime-walk detector on faed (program-free, 1, 2 or 3 characters at primes, all nine host letters, start 1 to 1,100). Control: dbbi parses completely at position 1 | 19,800 walks | no complete parse; best run 6 hosts, the median of 30 shuffles |
| poster sum lists as keys over the residue and dbbi: 54 lists, values or digits, both directions, every offset, add / subtract / reverse-subtract mod 10, then rule 2. Planted control recovered at 1.00 | 45,888 | best lowercase 0.44 (residue), 0.34 (dbbi); null ceilings 0.44 and 0.37 |
| last words before a point of choice, by position (film door speech, Hope exchange, the Merovingian up to "Choice is an illusion", the six-dot CHOICE slot, the choice page, the puzzle Architect up to "SELECT", the phase-3.2 intro), last 1 to 30 words, four forms, crossed with labels | 3,331 | 0 |
| the four #8446 labels in order and permutations, the #8446 tail sentence (doc 95) | 84 | 0 |
| the residue as direct key material, base-9 and decimal integers (doc 95) | small | 0 |
| "matrix sum" on the Architect text: running letter sums, letters at prime running sums, prime-index letters (doc 95) | small | 0 |
| `matrixsumlist` as a selector into the Architect, faed, dbbi, residue and checkerboard message (doc 95) | 180 selections | noise |
| `sha256(ybp output + msl output + last-words output)` in #8446 order (doc 95) | 5,376 | 0 |

### 10.7 Sessions of 23 and 24 September 2026 (docs 96 to 110)

Harness as in 10.6, plus the double-hash path with its own planted control, rebuilt
from scratch in a fresh workspace (about 4,000 candidates per second). Controls fired
before every run.

| what | scale | result |
|---|---:|---|
| sha-before-combine (`shabefanstoo` as "sha256 the answers too"): hash each component, join the digests, hash again; newline joins as `enter`; XOR of two components' digests | 154,784 | 0 (doc 96) |
| 4-part orderings of 15 core components under those joins | 131,040 | 0 (doc 96) |
| filler sums between prime hosts under L=84 | 12 screens | 0 (doc 96) |
| L=83 and L=84 host index sets (yellow and blue primes and offsets) selecting from nine texts | all sets, 0- and 1-based | no readable selection (doc 97) |
| the side-page hash (sha256 of the poster text) as "our first hint", nine forms, crossed with labels | 595 | 0 (doc 97) |
| riddle readings of every #8446 label (colour mixing, Latin, Lo Shu, Python `sum(matrix, [])`, film trivia, Archimedes, read-aloud puns) crossed A x B x C x D in #8446 order | 726,067 | 0 (doc 98) |
| double hash over pool items, pairs and the label cross | 54,742 | 0 (doc 98) |
| first and last words of every sentence, acrostics, over all chain prose and the Roses poem | 348 | 0 (doc 98) |
| digitwise sum of dbbi and faed (and residue, poster bits) mod 10, then rule 2 | 7,422 configs | inside the noise ceiling (doc 98) |
| the song: opposites-attract forms, rose answers, crossed with labels and the phase-2 lyric | 95,466 + 60,000 double-hash | 0 (doc 98) |
| the song, every span of 1 to 40 words, five forms, every line and clause; double-hashed; crossed with labels; line pairs | ~79,000 | 0 (doc 99) |
| the Architect text, 3 to 200 characters before each of its two choice points, crossed with every answer to the choice and the labels | 163,904 | 0 (doc 100) |
| crypto-versus-banking vocabulary from the rebus, alone, paired, crossed | 53,370 | 0 (doc 100) |
| filler letters before and after each prime stop of the walk ("last words before a choice"), group lengths, host string | small | noise; group lengths forced by prime gaps (doc 101) |
| chessboard piece-value sum lists: three positions, two value sets, four sign rules, rank, file and prime-square lists | 216 lists, 4,620 candidates | 0 (doc 102) |
| phase-2 template sums with `H` as -42, 42, 24, -24 | 160 | 0 (doc 102) |
| self-reference: each container's base64, bytes, salt, their hashes, each keyed by the others | ~120 | 0 (doc 103) |
| purple pill, Oen/One/Neo, GSMG expansion, ink counts, resistor colours, passport dates, 42, episode 3.5, Cypher/Hill, ASCII 127, halves | 7,368 + 30,000 double-hash | 0 (doc 103) |
| *Alice* Ch. VIII vocabulary alone, with labels, in pairs | 3,562 + 20,000 double-hash | 0 (doc 104) |
| zeroed poster text as a second HASHTHETEXT door: prime, composite and gardener positions, five replacements, O/0 and I/1 swaps | 857 variants, 3,428 screens | 0 (doc 106) |
| whole decrypted stages as one string (phase-2 plaintext, Architect, checkerboard message, digits, both multi-part answers, pairs) | 12 objects | 0 (doc 107) |
| `matrixsumlist` as a raw 256-bit scalar from the poster's row, column and diagonal sums | 70 | 0 (doc 107) |
| `yinyang` as XOR or interleave of the two 80-byte ciphertexts, salts and first blocks | 32 | 0 (doc 107) |
| the August 2026 farewell page and its terminal grid, three KDFs | 12,645 decrypts | 54 valid pads, 0 readable (doc 108) |
| merged-zero digit payloads as binary against the locks (runs A to C, section 6.4) | ~16.8M decrypts | one pad-3 on Cosmic Duality, random (doc 109) |
| structure-agnostic recogniser with lock chaining over every string harvested from earlier runs (240,681 candidates) and every doc 108/109 output | ~28M decrypts, ~3M chain decrypts | 1 flag (the doc 109 pad-3), random; about 1.3 expected (doc 110) |

---

### 10.8 Records 111–130 and saved-format review: completed work and limits

These records extend the historical tables above. Exact existing exclusions must
not be rerun. Per-attempt manifests and ledgers are not reproduced; the rows below are
the record. Structural checks are not password attempts.

| Record | Scope and result | Limit / disposition |
|---|---|---|
| 111 | 810 EBCDIC, inverse/mixed-cp273 and UTF-16 constrained merged-zero profiles; all complete, zero candidates | fixed byte domains and one ambiguous-zero symbol; not arbitrary binary payloads |
| 112 | B=2/Y=25 interpretation; weighted poster matrices joined with bounded scene endings; 646 distinct answers, 2,584 password strings, 15,504 primary decryptions + 912 conditional chain decryptions; 57+6 padding survivors retained, no recognized result | literal, SHA256-hex and two double-hash representations; EVP-SHA256/MD5, AES-256-CBC, three targets; matrix/boundary choices remain hypotheses |
| 113 | scene word-sum serialization against complete FAED, 300 configurations, zero complete matches | five scopes, stated sum maps/zeros/directions; no partial-match passwords |
| 114 | FAED head479/tail91 as merged-zero text, 576 profiles, no candidates | exploratory split significance does not prove payload boundaries |
| 115 | cumulative 2D summed-area tables, 3,744 configurations / 2,304 serializations, no complete DBBI/FAED fit | fixed sources/transforms; no password sweep |
| 116 | prime-selected FAED/complements, 32,768 binary-partition profiles, no stated exact message/text/Base58Check result | fixed subsequences, partitions, directions and bit offsets |
| 117 | 11,816 matrix-derived numeric keys with merged g/zero, 141,400 domain checks, all complete, no hits | fixed keys and two strict text domains; not all keyed binary models |
| 118 | byte-21 replacement reproduces known L=84 | inadvertent repeat of September 14 perbyte84; novelty claim withdrawn; insertion-only closure also withdrawn |
| 119 | user's Chrome Trust export shares Salted__ framing and 80-byte ciphertext size; public synthetic comparisons show multiple KDFs can produce that size | format observation, not evidence of puzzle origin/settings; no wallet decryption; wallet bytes omitted |
| 120 | recovered EVP/PBKDF2/cipher/no-padding coverage; 63,000 E and 2,796 C ledger records verified | E corpus is retracted Chain4-derived material, not main clue coverage; partial inventory only |
| 121 | recovered Astra manifests/results totaling 4,468,632 reported EVP operations; Rabbit completed 325,440-operation sweep; focused 2,640-cell grid | Rabbit B1 is truncated SalPhaseIon, not Terminal; missing matrices prevent global novelty certification |
| 122 | 30 PBKDF2-SHA256/10,000 + 60 /600,000 attempts, all complete, zero valid padding | exact listed candidates and profiles excluded; every raw output retained; do not repeat these 90 identities |
| 123 | critique of documented families; no decryptions | withdraws filler/endpoint/container-order certainty; numbers do not substitute for password derivation |
| 124 | recovered prior 574061 -> sums -> BUT/HYE model; local/global edit consistency check | no old solver rerun; consumer unresolved; replacement's prior provenance established |
| 125 | whitespace scope difference: 170,295 provisional forms; retained short outputs: 240 raw windows -> 480 addresses, zero matches | no new decryptions; residual not globally certified untried; raw-key format/offsets are assumptions |
| 126 | verified actual target, address encoding, production membership expression and ledger identities with public controls | prize is goal; halving recipient secondary sentinel; no puzzle candidate derivation repeated |
| 127 | dossier integration | editorial changes only; primary data preserved |
| 128 | 104 matrixsumlist bits mask FAED primes; zero/delete/keep, rule 2, four password forms, EVP-SHA256/MD5, three targets; 48 configs / 1,152 reported decryptions, one pad-1, no readable result | "digits" password forms actually use letter strings; decoded prefixes only, no cipher plaintext retained; 192 configuration identities reconstructed for exclusion |
| 129 | carried-code subsequences versus shuffles and decimal-header checks: null; screen-line cipher keys unrun | alphabet argument does not rule out English; unselected interpretation remains unrun |
| 130 | wrap-width and HTML review: null; checkerboard IC not significant against matched shuffles; prior Hill coverage recovered | separate record read here, not rerun; planned variable-host FAED walk not executed here |
| Saved-format review | 90 retained outputs: no encoded keys/structures; 120 fixed public-point layouts: none valid; exact whitespace exclusions extended, count still 170,295 | zero new decryptions; raw-window checks not repeated; missing history still prevents global novelty certification |

### Exact attempt-122 exclusion

Both profiles are AES-256-CBC / PBKDF2-HMAC-SHA256, using the stored eight-byte
salt to derive 48 bytes: 32-byte key followed by 16-byte IV, with PKCS7 padding.
Each candidate uses literal UTF-8 and lowercase ASCII SHA256 hex on all three
authenticated targets.

The 10,000-iteration batch used these five answers:

    stopit
    sheisgoingtodieandthereisnothingyoucandotostopit
    sheisgoingtodieandthereisnothingthatyoucandotostopit
    therearetwodoors
    theproblemis

The 600,000-iteration batch used those five and:

    theflowerblossomsthroughwhatseemstobeaconcretesurface
    followthewhiterabbit
    gsmgio5btcpuzzlechallenge
    yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyang
    incaseyoumanagetocrackthistheprivatekeysbelongtohalfandbetterhalfandtheyalsoneedfundstolive

All 90 failed padding. Public known-answer, synthetic-length and invalid-padding
controls passed; two PBKDF2 APIs may share OpenSSL and are not independent
backend implementations. There are zero incomplete attempts. An existing start
record reserves its identity to prevent replay. Historical overlap with missing
manifests was explicitly unresolved when the user authorized this bounded batch.

The final attempt-122 ledger SHA256 is
`40d6efb0f38b73e5fa102754b0b9f4a28cc1487dde8fc9a6839ae287eea44381`.
The attempt-122 coverage matrix supersedes the
121 grid: **676 covered, 337 possible prior executions, 1,627 record gaps**.
The grid is 22 candidates x 5 forms x 8 profiles x 3 targets. It is a focused
audit, not the password universe; zero gaps are certified globally untried.

### Recovered settings coverage and source limitations

PBKDF2 is not generally untried. Records cover 10,000 iterations on curated and
broad short-target scopes, and Rabbit's completed literal-password sweep uses
SHA1/SHA256 at 1,000/10,000/100,000 plus four EVP digests and three AES sizes.
Only its authentic SalPhaseIon/Cosmic objects count toward those targets.
Alternate ciphers, ECB/stream modes, Key Wrap and no-padding already have
bounded completed runs. Eleven additional PBKDF2 counts in audit 120 apply to
a narrow retracted Chain4-derived corpus, not the main clue answers.

The eight cipher names in the older 7,163,600-operation summary were recovered:
AES-256, ARIA-256, Camellia-256, SM4, SEED, 3DES, Blowfish and CAST5. Its two
KDF identities/full settings and exact candidate manifest remain missing, as do
original 108–110 matrices. Source alone is not execution evidence. One older
Astra KDF probe has an unreachable EVP branch and suppresses KDF exceptions;
its hit count cannot certify intended coverage.

Trust's export documentation was reported in observation 119 to specify
AES-256-CBC/PBKDF2-SHA256/600,000. This historical observation led to the bounded
122 comparison; it does not establish the puzzle's much older authoring profile.
No wallet ciphertext, salt, password or private material is included here.

---

## 11. METHODOLOGY, LEARNED EXPENSIVELY

1. **A null is only as good as its control.** State the control and confirm it fired.
2. **A null must sample the class of outcome, not the specific one.** Worked example:
   `keYmgma` -> "key eyes" was published at 1 in 200,000 with the first word held
   fixed; the honest price is about 1 in 481 conditional, and real faed yields fewer
   readable variants than its own shuffles.
3. **A null is only as strong as the target it ran against.**
4. **Screen cheap, confirm expensive.**
5. **Recognisers must be block-size-aware.** Fix windows in bytes.
6. **The cipher is a parameter.**
7. **Do not filter for printable plaintext.** Phase 3.2 is 59% printable.
8. **Structure screens beat format screens.**
9. **Forced results are not evidence.** Check what the construction guarantees.
10. **Nothing on the live site is creator material** until matched to a pre-2022
    capture or a hash here.
11. **Do not contact the creator.**
12. **Read hints with their parents.** The endorsement audit (section 8.1) changed
    three readings in one pass.
13. **Generate data blocks, never retype them.** A retyped block is where silent
    corruption enters. If a block must pass through a hand, re-verify it by script.
14. **A new word source is not a lead.** Whole-book and whole-corpus sweeps have come
    back null again and again. What is missing is a derivation that names a candidate.
15. **Re-read the clues before running candidates.** The song that produced two of the
    four opened gates was missing from this file for about 75 documents; every session
    in between worked without it. Its return consumed two surplus items in one pass.
16. **Recognisers must not assume text.** Test the recogniser on EBCDIC, UTF-16,
    compressed data and binary before trusting a pad-1 or pad-2 null (doc 110). A
    `--quiet` flag that hides pad 1 and 2 silently turns a sweep into a pad-3 sweep
    (doc 108).
17. **A missing execution record is not novelty.** Pin exact password bytes,
    target digest and complete settings; preserve started/completed identities.
18. **Controls validate the implementation, not the interpretation.** A correct
    P2PKH matcher does not establish that a stage emits raw private keys.
19. **Reuse retained outputs.** A new detector is not a reason to repeat the
    same KDF/decryption. Keep the actual prize goal separate from sentinels.

### Corrections of record

- `/phase1verification` was declared dead on a uniform 413; the 413 was CSRF.
- The EBCDIC codec is **cp273** with **reciprocal** Beaufort.
- The checkerboard digit string is **149** digits.
- The four leftover spiral bits are **`0000`**.
- `#FEFEFE` supports two local parser models: blue insertion (L=83) and byte-marker replacement (L=84).
- faed's "drift" is 32 of 570 characters.
- An earlier comparison omitted the off-white cell (doc 71 §1). That mistake
  does not exclude the separate source-grounded replacement model.
- This file regressed twice against doc 71 (the tag alphabet, "on the highway"). Fixed
  on 22 September.
- **Stage-order certainty withdrawn:** #39237 supports a downstream phase, but
  does not uniquely identify Cosmic plaintext or SalPhaseIon as the next gate.
- **"First or zero"** is not a general indexing convention (doc 39).
- **The song was dropped** from this file after doc 22. Restored as section 3.A.
- **The painted-cell count is 14**, not 12 (doc 105).
- **Filler certainty withdrawn:** residue/FAED distributions are compatible with
  biased filler, but do not prove a generator or exclude an operand role.
- **The first farewell-page run used `--quiet`**, which hides pad 1 and 2. Redone with
  the recogniser (doc 108). The main sweeps already content-checked pad 1 and 2, so
  their results stand.

---

## 12. WHERE IT STANDS

**Unsolved. All three authenticated containers remain locked; no prize key found.**
Earlier large search totals overlap and their original manifests are partly
missing. They are not a globally deduplicated count or evidence of proximity.
Attempt 122 records 90 exact rows, all failed padding. Attempt 128 reports another
1,152 operations and no readable result, but did not retain decrypted bytes.

Verified: source envelope identities; the earlier solved encryption convention;
decoded labels; original poster colors/URL; two exact local DBBI parses; and the
recent target/matcher controls. Unresolved: intended DBBI endpoint/consumer,
FAED role, matrix operation, word boundary/consumer, SHA preimage scope,
thispassword referent, yinyang identity and the unopened profiles/stage order.
The song, filler, halves and macro interpretations must retain their evidence levels.

### Next work and its priority

**Recent evidence, with first proposed consumer now tested:** the user's screenshot reports
`Yellowblueprimes:317/557` and `Another door:137/143`. A comparison with the saved
replacement model matches both pairs: used yellow/blue host sums, then alternating
row sums of prime-zeroed a=0..i=8 values on a 6×14 layout. The first pair also locates
the actual #FEFEFE pixel on the native poster. This supports replacement over
insertion for the reported first pair. Other factorizations can reproduce the
second pair; exact operation/consumer remains unproved. Existing L=84 tests remain
excluded. Weigh this evidence before
proposing another matrix/password run. No parser search or decryption was repeated.

The direct six-row word-selector follow-up is now complete: full pre-door
Architect speech and final turn, start/end, base 0/1. Its eight specifications
give six distinct source selections and 24 word/initial/final forms. No coherent
instruction or exact known-literal/digest/edit-block/DBBI-pattern hit emerged.
The exact list was absent from 1,573 saved list records and the forms from
463,168 candidate records in R2A/R2B/R3A; this is scoped coverage, not global
novelty certification. No AES or address derivations. Do not repeat these direct
readings. Further work on this fit needs independent
support for the operation/consumer rather than additional ad hoc index variants.

**Highest potential clue leverage:** an independent selector for the Architect
edge/mirror relationship or another complete operand -> operation -> consumer
transition. The `574061 -> [23,16,7] -> BUT/HYE` hypothesis has a recorded boundary
match; its consumer is not identified. Existing unchanged-input mirror/grammar/
pair audits are already extensive. A new clue, authenticated variant or forced
consumer takes priority; none was recovered in reviews 124–126 or the saved-format review.

**Provisional computational residual, held:** a difference-only Tier-1 trailing-space
no-padding/raw-key check for Terminal and SalPhaseIon. The creator's recommended
historical hash tool preserved spaces, a modest implementation rationale, not
proof of an accidental trailing space or raw-key plaintext. The smaller curated
whitespace corpus is already negative (upstream Phase 163).

| Password set | Count |
|---|---:|
| Entire expanded Tier-1 proposal | 700,582 |
| Existing Tier-1 base forms | 525,436 |
| Additional trailing-space forms | 175,146 |
| Added forms already in completed smaller whitespace checkpoint | 4,851 |
| Provisional difference | **170,295** |

A whole-corpus rerun would repeat at least 530,287 forms. The provisional difference
is **not globally certified untried**. The saved-format review compared its exact
identities with audit 120, all 12 completed Astra manifests/results, attempt 122
and recovered attempt-128 identities; no additional overlaps, count unchanged.
The hash-only proposal and fingerprints were frozen in the
saved-format review. Missing original matrices and
unrecovered P378/P379 values still block certification. Reuse retained outputs
when changing a detector. No difference-only unlock run launched. This remains
low-expected-value coverage completion without a newly selected clue.

### Retained-byte check: precise result and limits

Record 125 inspected the 60 saved short-target outputs from 122, at offsets
0/16/32/48, as direct big-endian 32-byte scalars. **240 raw-key windows -> 480
compressed/uncompressed P2PKH addresses -> zero prize/sentinel matches.** Audit
126 verified the target on the original poster, reconstructed it from the
published prize public key, exercised the production match expression with
public positives/negatives, and checked output/container identities. No puzzle
candidate derivation or decryption was repeated for audit 126.

This is a narrow negative. Almost every random 32-byte window is a valid scalar,
so scalar validity gives essentially no plaintext evidence. Raw-key/no-padding
format and four offsets are unproved assumptions. The check does not exclude
passwords, seeds, instructions, encoded keys, further encrypted stages, other
offsets/byte orders or Cosmic contents. The halving recipient is a secondary
sentinel, not an established second puzzle goal. Do not repeat this raw-window check.

The saved-format review added typed checks on all 90 retained attempt-122 outputs:
hex64 tokens, canonical padded base64-32 tokens, checksum-valid WIF, complete DER
secp256k1 keys, complete printable UTF-8/JSON, specified start signatures and
literal goal/sentinel addresses. Zero candidates or structural hits. The 60
short outputs also received 120 fixed 0/32 XY/YX public-point layout checks;
zero valid points. Zero new scalar derivations/address comparisons; none of
record 125's raw windows repeated. Public controls passed. No new decryptions.
Other encodings, seed paths, combined halves and arbitrary raw offsets remain
outside these precise scopes. Invalid padding still fails the PKCS7 model.

### Stale recommendations and completed exclusions

- Cosmic Duality pages 57–58 were recovered/reviewed in upstream Phase 259; no
  matrix instruction found. The old missing-page recommendation is stale.
- GI chain addition completed in upstream Phase 123: 5,761,385 candidate pairs,
  zero hits. No-padding Tier 2 completed in upstream Phase 144.
- Architect mirror transfer to solved boundaries was already audited in upstream
  Phase 456; Phase 470 identifies another unchanged-input replay as duplicate work.
- GI/HE rescoring and thispassword grammar tests do not supply independent selectors
  merely through another score. Those recorded models and audits remain exclusions.
- Off-white replacement is prior perbyte84 work. Neither it nor the reopened
  interpretation licenses repeating L=84 selectors or passwords.
- All precise 111–117 families and all 90 attempt-122 identities remain excluded.
- Prior poster/gardener, song/book text, farewell-page and literal-label families
  are bounded negatives. Their results do not prove all conceivable operations closed.

### Unconsumed or underdetermined material

The four center cells/tail `0000`; unused B/Y or Y under the two DBBI models;
residue and FAED roles; trailing O of CIAOBELLAO; doubled SELF; four-dot reply;
"And Oen"; "as wide as the first one seen"; zeroing operand/representation;
matrixsumlist, lastwordsbeforearchichoice, thispassword and yinyang consumers.
The painted-rose/song readings account for thematic correspondences, not every
mechanical role of the off-white cell or every unused item.

Before a test, freeze source bytes, exact operand/normalization, operation,
settings, target and validator. Then check prior identities. A recognized result
needs independent confirmation; padding or attractive partial text is insufficient.

---

## 13. COMPLETENESS NOTE

Verbatim and reconstructible in this file: the 1,075-character textarea; dbbi (91),
faed (570), the residue (60); the 1,539-letter Architect text; the 149 digits and
the 91-letter checkerboard plaintext; the 648-byte phase-2 plaintext; the phase-3
riddle head, the phase-3.2 intro and the checkerboard riddle; the poster's 196-bit
spiral string; the 25-symbol spliced program; all three locked containers; every
answer and password hex in the chain; the #8446 and #53342 decodes.

**Historical generation and verification (25 September edition).** The data blocks were produced by script from the
phase-2 ciphertext, the phase-3.2 plaintext, the textarea, the three container files,
the poster image and the Telegram export. For that earlier edition they were re-checked by
script against the decrypted phase-2 and phase-3.2 plaintexts and the poster: the
phase-2 plaintext is 648 bytes with six CRLF and hashes to `e2f9dd65...`; the phase-3.2
plaintext hashes to `b82afeb8...`; the intro, the checkerboard riddle and the 149
digits match the plaintext bytes; the Architect decode equals the 1,539-letter text;
the 149 digits decode to the 91 letters under the stated key; the Terminal base64
inside the plaintext equals the Terminal block; the textarea is 1,075 characters and
both segments decode; the L=83 parse consumes 91 at position 83 with 23 hosts, 8 of
them `be`, and reproduces the residue; the residue and faed counts match the tables;
all three containers match their sha256; SalPhaseIon short equals the two textarea
halves joined; the poster spiral reads the URL with tail `0000`, the cell colour counts
are 86/85/15/9/1 and the colour sequence matches section 4.2. The #8446 and #53342
decodes are carried unchanged from the 22 September edition, where they were generated
from the Telegram export (not reproduced here). Concatenate the lines
of any fenced data block with no separators to reconstruct the original string (except
the phase-2 and prose blocks, whose line breaks are real).

For the 26 September editorial update, the unlabelled primary-data code blocks
were compared with the prior edition and preserved exactly. The three
base64 envelopes still decode to their pinned hashes/lengths. No earlier solver,
prime walk, password sweep or decryption was repeated to update this file.
The replacement parse and recovered macro model are carried from their existing
reports.

The song's text is deliberately absent (section 3.A).

Not here, and not needed: the solved phase-2 and phase-3 envelope ciphertexts (the
plaintexts are given), the non-printable middle of the phase-3.2 plaintext (its
meaningful parts are given decoded), and image files (fully described numerically).

### Three states, kept distinct

- **DECODED**: the object has been read.
- **CONSUMED**: its role in the construction is accounted for.
- **TESTED WITHIN SCOPE**: the explicitly frozen candidate bytes/operations
  were evaluated under recorded profiles/targets. This does not mean every
  possible value from the source has been tried.

A decode is not a mining run, and an assertion that sounds like a test result is the
single most expensive failure mode in this project's record.

---

## 14. SESSION DOCUMENTS SINCE THE LAST EDITION

| doc | subject | outcome |
|---|---|---|
| 94 | dossier rebuild; `matrixsumlist` and last words worked | null |
| 95 | four fresh derivations | null |
| 96 | review; sha-before-combine, newline, XOR families | null |
| 97 | L=84 "select from"; side-page hash as first hint | null |
| 98 | riddle readings; the song thread recovered | song restored |
| 99 | the song's full text | null as text |
| 100 | song phase three | historical interpretation; L=83 closure superseded |
| 101 | the dbbi residue | distribution fit; filler/generator certainty withdrawn |
| 102 | chessboard and phase-2 template as the matrix | null; `H` sign read |
| 103 | all 492 creator messages re-read | #881, #2918, halves |
| 104 | the Roses poem | *Alice* Ch. VIII, primes {2, 5, 7} |
| 105 | the painted cell; the nest | 14 cells, 1 in 5; nest is the drawing |
| 106 | another door; archive pulls | null; app shell |
| 107 | whole stages, scalar, container XOR | null |
| 108 | the August 2026 farewell page | nothing new |
| 109 | merged-zero payloads against the locks | null |
| 110 | structure-agnostic recogniser, lock chaining | reported null; original matrix missing |
| 111 | constrained non-ASCII merged-zero searches | 810 profiles, zero candidates |
| 112–113 | weighted poster / boundary correction / full FAED word sums | bounded negatives; outputs retained |
| 114–118 | split, integral sums, prime bits, keyed zeros, replacement | negatives; 118 novelty retracted |
| 119 | user test-wallet export framing | envelope ambiguity, no wallet decryption |
| 120 | encryption/settings execution audit | partial recovery, no new attempts |
| 121 | exact coverage recovery | 2,640-cell focused matrix; missing history remains |
| 122 | PBKDF2 10,000 / 600,000 unlock tests | 90 complete, zero valid padding; do not repeat |
| 123 | remaining-blob critique | overconfident closures withdrawn |
| 124 | prior macro model and local/global scope | BUT/HYE consumer open; perbyte84 provenance restored |
| 125 | next direction and saved-byte screen | 170,295 provisional forms; 480 addresses, zero matches |
| 126 | target/matcher scope audit | correct goal/conversion; raw-key role unproved |
| 127 | dossier integration through 126 | documentation only; primary data preserved |
| 128 | matrixsumlist mask on FAED primes | 48 configs / 1,152 reported decryptions, no readable result; cipher bytes missing |
| 129 | subsequences and screen-line review | null recorded checks; alphabet impossibility claim corrected by later review |
| 130 | layout, statistics and coverage review | null layout; IC explained by letter counts; prior Hill coverage |
| Saved-format review | saved formats, exclusions and record corrections | no format hits; 170,295 remains provisional; zero new decryptions |

---

## 15. HISTORICAL REVISION NOTE, 25 SEPTEMBER 2026

**Superseded interpretation claims:** this note records what that edition changed.
Its L=83/filler/operand/halves certainty is corrected in the current sections
and section 16 below; do not treat these historical bullets as current conclusions.

That edition replaced both the 22 September dossier and the 23 September addendum.

- **Section 0:** fifth warning, on non-text plaintexts.
- **Section 1:** the August 2026 relaunch audited (doc 108); archive pulls closed
  (doc 106); double-hash path added to the harness.
- **Section 2:** the structure-agnostic recogniser and lock chaining (doc 110).
- **Section 3.A (new):** the song restored as the backbone (docs 22, 98 to 100).
- **Section 3.2:** the dropped `H` sign read as the unbalanced equation (doc 102).
- **Section 3.4a:** the Architect text read as the SalPhaseIon manual (docs 96, 97).
- **Sections 4.3 and 4.4:** the off-white cell consumed as forced blue and the painted
  rose; 14 candidate cells, not 12; the nest pixels are the drawing (docs 100, 105).
- **Section 5:** the `war` tile consumed; the crypto-versus-banking judgement.
- **Sections 6.3 and 6.4:** L=83 settled; the residue is filler; the merged-zero model
  closed as a binary payload, with the two size-bound cases (docs 100, 101, 109).
- **Section 6.5:** the Terminal's missing riddle and #2918; container combinations
  null (docs 96, 103, 107).
- **Section 7.2:** the Roses poem as the planned final hint and as *Alice* Ch. VIII
  (docs 103, 104).
- **Section 8.6 (new):** the re-read of all 492 creator messages.
- **Section 9:** the a..i content accounted for; operands outside the page; the song as
  structure; the halves.
- **Section 10.7 (new):** every screen of 23 and 24 September with its scale.
- **Sections 11 and 12:** two new methodology rules; corrections of record; leads
  re-ranked; surplus updated.
- **Section 14 (new):** index of session documents 94 to 110.

The earlier revision history (the `# X 2 S H 4 Y 0 Q B 15 #` closure, the L=84
exhaustion, the tag inventory, the 479 lead run to completion, the nine families
suggested in review, and the 22 September repairs against doc 71) is preserved in
docs 71 to 93.


## 16. REVISION NOTE, 26 SEPTEMBER 2026: RECORD 127

This edit integrates the surviving records through 126 without new puzzle
attempts. It preserves primary data.

- Goal validation now distinguishes a raw private scalar from an answer hashed
  into a candidate key, and separates prize success from the halving sentinel.
- Sections 4.3/6.3 retain both exact DBBI models; L=83 certainty and 118 novelty
  are withdrawn. Section 9 restores the prior 574061/BUT-HYE branch and the
  conditional requirement that parser edits stay local.
- Filler/generator, external-operand, Cosmic-content, half-layout and next-gate
  assertions are downgraded to hypotheses. The Hope/physical-choice boundary is
  corrected without generating another password.
- Section 10.8 records 111–126, the exact 90 attempt-122 exclusions, recovered
  settings coverage and missing historical matrices. The focused coverage count
  is 676 covered / 337 possible / 1,627 gaps, with no globally certified new cell.
- Section 12 replaces stale next-step guidance and records the provisional
  whitespace difference and precise raw-window result. Source/consumer evidence
  takes priority over a low-value coverage expansion.
- Original ciphertexts, decoded source blocks and historical negative scopes
  remain available. Historical totals are not added as unique search coverage.

The puzzle remains unsolved; no private material from the user's wallet is added.


## 17. REVISION NOTE, 26 SEPTEMBER 2026: SAVED-FORMAT REVIEW

Integrates 128–130 and the separate saved-format/exclusion review. The review's
scripts shared the number 130 with the separate attempt 130; these are distinct
activities and were not substituted for one another.

Attempt 128 saved 16 complete small rule-2 outputs and 32 prefixes, not all full
outputs; none of its decrypted bytes were saved. Its four password forms are
recovered as 192 configuration identities for exclusions only. "Digits" labels
actually use a–i/o letter strings. Do not repeat its cipher operations.

Attempt 129's ten-letter-per-column argument cannot structurally exclude English;
screen-line Vigenere/Beaufort remains unrun and unselected. This correction did
not trigger another sweep. Attempt 130 was read, not rerun. The precise saved-format
negatives and extended whitespace exclusions are in sections 10.8 and 12.

No new decryptions or password tests. Primary blocks and container identities
preserved.
