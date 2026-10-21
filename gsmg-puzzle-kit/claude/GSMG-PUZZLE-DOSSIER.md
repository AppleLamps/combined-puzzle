# GSMG.IO 5 BTC PUZZLE: COMPLETE DOSSIER

**Current interpretation: 6 October 2026.** Read [doc 119](119-current-evidence-ledger.md)
and [doc 118](118-correctness-audit-remediation.md) before using this dossier's
historical verdicts. Primary data and old run reports are preserved. “Closed”,
“consumed”, “unique” and “null” in older tables are scoped to their stated models
and tests; they are not proofs of intended purpose or exhaustive exclusion.
The current unknowns include operands, operation, selection, receiver, assembly,
serialization and lock order. No new unlock or active search is reported.

Self-contained for the analysis. This file holds the primary data of the puzzle, the
verified derivations, the creator's statements with the messages they answer, every dead
end with its evidence, and the exact test that confirms a win. Four things live in other
Project files and are listed in section 0: the creator's 492 messages, the poster image,
the solved stage ciphertexts and the scripts in `tools/` that rebuild the search pools.

Updated 5 October 2026: docs 116 (coverage gaps, 3 October) and 117 (riddle rounds R1 to
R35, per-container verdicts and the pair ledger, 3 and 4 October) are folded into sections
10.10, 12, 14 and 15. The rest of this edition is current as of 29 September 2026.

The 29 September revision folds in docs 111 to 114 (25 September),
doc 115 (the 29 September queue) and the corrections from a full audit of the project. The 23 September addendum, 33
superseded log docs and five superseded reference docs (01, 02, 03, 05, 06) were
retired after their content had been folded in here, and a duplicate data file was
removed (the README lists what remains; doc 67 indexes the analysis log, with errata).
Section 15 lists every change. Every data block in this file was carried over unchanged from the 25 September
edition, which generated each one from the ciphertexts, the poster and the Telegram
export by script. They were reported re-verified for the 29 September edition (section 13). The 6 October documentation reconciliation did not rerun those programs or decryptions.

---

## 0. HOW TO USE THIS DOCUMENT

Read section 1 for the goal and the win test. Section 3.A is the song that the
puzzle is built on. Sections 2 to 7 are the primary material. Section 8 is what the
creator said, paired with what he was answering. Section 9 is the current model of
how the puzzle is built. Section 10 is everything that has been tried and failed,
which is the most valuable part, because the failure modes are expensive to
rediscover. Section 11 is methodology learned the hard way. Section 12 is where it
stands and what remains. Doc 67 indexes the surviving analysis log.

**Files outside this document.** The dossier reproduces every quotation and data block it
relies on. These files hold the rest, all in the same Project:

| file | holds | needed for |
|---|---|---|
| `jrk_messages.txt` | the creator's 492 messages plus 18 admin actions, with reply headers | searching for a hint that section 8 does not quote |
| `puzzle.png`, `matrix.json` | the poster, and its 14x14 grid as colour letters and bits | new readings of the poster (section 4 has the spiral bits and counts) |
| `phase2.b64`, `phase3.b64`, `phase3.2.b64` | the three solved stage ciphertexts | rebuilding the plaintexts; the answers are in section 3 |
| `theseedisplanted.html`, `phase2_choice.html`, `salphaseion_phase3.html` | the captured pages | checking a page detail |
| `tools/` (start at `tools/README-tools.md`) | the harness, the win test, the pool builders, the fit tests and the dossier verifiers | re-running anything in section 10 without rebuilding it from prose |
| `04-key-material.md`, `07-onchain-facts.md`, `claude/21` | full address and transaction tables | on-chain questions beyond section 1 |
| `claude/NN-*.md` | the detail behind each result in section 10; `claude/67` indexes them | the exact lists behind a count |

Five warnings before you start.

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

**The historical working approach screened three locked containers** (section 6.5). Their authenticity is supported, but mandatory use, order and the source of the eventual key remain unproved. No search is currently running.

A second address is carried in the test as a sentinel:

    17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa
      HASH160 4bc468447fe1b048ad030a2f9a125478eabc4ed6

**`17ucy...` is not a puzzle output.** It is the destination of the two halvings,
and the chronology is on chain:

    2019-04-13  block 571,497   prize address funded with 5 BTC
    2019-04-20                  Telegram group opens; first code already cracked
    2020-05-11  block 630,001   2.5 BTC to 17ucy..., nLockTime 629,998 (the halving)
    2024-04-24  block 840,725   1.25 BTC to 17ucy..., nLockTime 840,003 (the halving)

Both moves carry an nLockTime set to the halving block (block 630,000 was mined on
2020-05-11 and block 840,000 on 2024-04-20), so they were pre-signed and timed
deliberately; the second one confirmed four days after the halving. `17ucy...` was first funded on 2020-05-11, while the phase-3.2
envelope containing the "half and better half" message was in chat roughly 30 hours
before block 630,000. The message predates the address; the label was applied to the
address afterwards. Balances on 2026-09-29 were 1.25636967 BTC at the prize address
(the 1.25 BTC principal plus dust it keeps receiving) and 3.75055856 BTC at `17ucy...`. That address has **never been spent**, so its public
key is not exposed. Keep it in the test as a free safety net. Do not treat it as a
goal: the Architect text says `TAKETHEPRIVATEKEY`, singular, and the creator answered
"a private key", singular, when asked directly (#4624).

A third address, `1cc6xayvqpeetixmuXDRsGug7GKyoRdxP` (HASH160
`06bbdc66fda09110435c79a86656a604c2d5c69b`), is the prize key's compressed twin and
is empty. The win test checks both point forms, so it is covered by the same scalar.

### The exact win test

```python
import hashlib, coincurve
def h160(b): return hashlib.new('ripemd160', hashlib.sha256(b).digest()).hexdigest()
TARGETS = {'a9553269572a317e39f0f518cb87c1a0ee1dbae4',   # the puzzle target
           '4bc468447fe1b048ad030a2f9a125478eabc4ed6'}   # sentinel, non-puzzle origin
NEIGHBOURS = {'a4ae210a25bb8e2c359a134fafc2e30c6709dbc0',   # P-G
              'f8fca692ffc90cba0c330dc56e02fa8da8d2d6e6',   # P+G
              '3de34fca1bd6b7607243b0316a8102b7598cc9dc',   # P/2
              'c889dfbf698413209b6131895250b869f68560e0'}   # 2P
def win(X, targets=TARGETS):
    priv = hashlib.sha256(X.encode() if isinstance(X,str) else X).digest()
    pk = coincurve.PrivateKey(priv).public_key
    return any(h160(pk.format(c)) in targets for c in (True, False))
```

Validate it before trusting it: private key = 1 must give
`751e76e8199196d454941c45d1b3a323f1433bd6`. `win(X, NEIGHBOURS)` is a near-miss
detector: the 2021 "neighbors, half and double" transaction funded the addresses of
P-G, P+G, P/2 and 2P, so a scalar one step from the prize scalar would hit one of
them rather than the prize (doc 113).

The standard harness since 23 September also runs a double-hash path
(`sha256(sha256(x))` and `sha256` of the hex digest), for the win test and as
container passwords, with its own planted control.

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

Each bot's block-938165 run also carries the string
`bc1qks8zrshwmu3m8vgqdzwl2u8jjfgnvgjlezwqcd`, a bech32 address with 15 transactions of
its own; nothing in this project ties it to the puzzle.

**The varying output amounts are change.** Each transaction spends the previous
change, pays 546 sat of dust to the vault, attaches the message, and returns the
remainder to itself; the step is dust + fee (546 + 450 = 996 at block 938165,
546 + 550 = 1096 at block 944096), measured exactly. The 2175 "pair offset" is the
difference between two bots' balances. There is no second channel.

**The senders are dust bots.** Inputs come from `145ZQ9siLrsXBKf465wjdyQYAP5dRwhRhQ`
and `1JG648yaB7Wp2dpUfcZoRSD4q35oq47vCu` (lifetime inflow 0.01786 and 0.01762 BTC; both
now empty). `matrixsumlistenterlastwordsbeforearchichoicethispassword` is a re-cut of
the published #8446 tokens, so the stream is derivative. The creator publicly denied
authoring on-chain OP_RETURN messages (#12653).

**Tested and null.** 379 candidates: every token alone, both batch orders forward and
reversed, all 2- and 3-term permutations within each batch, cross-batch pairs, and
each token crossed with 996, 1096, 2175 and the endpoint amounts.

**The "creator cluster" built from these sprays does not hold.** Shared control is
established by common input ownership, not by a shared payer. The 2025-09-09 spray at
block 913830 has 1 input and 9 outputs: one outsider paid eight P2PKH addresses (the
prize address, `17ucy...` and six others) and took change to a bech32 address. Dusting is the standard way to manufacture a false cluster. What survives
is narrow: `1EtbTvVB8...` funded the prize address on 2019-04-13 and also paid
`1GSMG1CLx...` (2018) and `1BEN1x8p...` (2020). The prize address has only ever signed
its two self-transfers.

**The `11111119536NnU2vPAvoQhvkheQ8ejYJ` "witness pair" is a dust recipient.** Valid
base58check, hash160 with 48 leading zero bits (about 2^48 work, an affordable
collectible). It is spendable and spent (46 of 47 outputs). It funded the vanity
address `1GSMG9VDL...` (20,000 sat, block 949573), and every message that address
inscribed pays 546 sat of dust back to it, the same dust-bot shape as above. In spend
order: `leavethematrix`, `yourlastcommand`, `hereismysecret`, `isolveditwithanabacus`,
`secondanswer`, the blob `GSMGJH` (64 bytes), the blob `GSMGBH` (65 bytes) and the
WITNESS message (`GSMG WITNESS BLK 949653 TX 808f812f`, which pays its dust to the prize
address). Each transaction spends the previous one's change, so the spend chain fixes the
order although five of them share block 949574 (`message-sequence.json`; earlier
editions of that file listed a different order). The blobs are unauthenticated; nonce
reuse against the prize's six known `r` values was tested and is null.

**Prefix sharing is forced.** Keeping only the top 3 bytes `a95532` and randomising
the rest, 1227 of 2000 hash160s still render as `1GSMG...`. Landing `1GSMG` takes
about 58^4 = 1.13e7 vanity attempts. Prefix sharing establishes taste, not control.

### The on-chain oracle is closed (docs 21, 113)

Six checkpoint addresses exist on chain and every preimage is known. They are outputs
of one funding address, `3GSMG24TujqfMJG1kQoBX18DzJHQLeJYMK`. Doc 113 classified all
30 of its transactions by whether an input spends from 3GSMG24 (signed by its key) or
not (inbound). The 14 signed transactions run from 2020-03-24 to 2021-07-18:

    2020-03-24  blocks 622762 to 622774   six GSMG.io: checkpoints, 1000 sats each (990 for the last)
    2020-04-03  block 624209              two "Good job, Neo!" payments
    2020-04-07  block 624768              1,050 sats to 1NULY7Dhzu..., no OP_RETURN
    2020-05-11  block 630001              "Halving", 700 sats to the prize address
    2021-07-18  block 691563              "GSMG.io neighbors, half and double"

- **The two "Good job, Neo!" addresses are poster checkpoints.** `148XH2YBmL...` is
  `gsmg.io/theseedisplanted` as a 32-byte big-endian private key (compressed);
  `13HGhjkmKU...` is its 192 bits reversed. Anyone holding the poster can compute
  both keys, so messages sent from them (`From Neo`, `Neo wallet ...`) carry no
  authentication.
- **`1NULY7Dhzu...` is a tip address.** It is hard-coded in alek76's GPU
  Pollard-kangaroo tool (built on VanitySearch 1.15; first commit containing the tip
  line 2020-04-05 00:41 UTC). The oracle paid it about 51 hours later, so the operator
  of 3GSMG24 followed a new ECDLP tool within two days of release. That fits an
  experienced solver better than the creator, and falls short of proof.
- **"neighbors, half and double"** paid 5000 sats each to the addresses of P-G, P+G,
  P/2 and 2P, where P is the prize public key: `1G1kRAFR68y6CUq1SAJMzHmjd6sEEgtVUT`,
  `1PhXF3xVQ8Sg9FomBcmRwRbvvGfm3Y2os1`, `16eEXbSuKN8tvcos1iKjdju6dAaWWRBMEs` and
  `1KHMK2C8uBptRz67FbrXy43yHzhZG16Hbm`, in that order. All four are addresses of the
  uncompressed public keys, regenerated from P by script on 29 September. None has ever
  spent (doc 04). They are near-miss targets in the harness (above).
- **Every later message is inbound.** `BULLSHIT`, `From Neo`, `Neo wallet ...`, `Yes`
  (twice, signed with the public checkpoint keys), `Its in good hands with Gavin...`,
  `Happy late mothers day!`, `I thought choice was an illusion?` and later dust were
  signed by other keys. The oracle's own voice ends at block 691563.
  One more message from the poster key `13HGhjkm...`, `SalPhaseIon sumlist AES`
  (block 897195, 2025-05-18), does not touch the oracle address. It is as
  unauthenticated as the rest.
- **Authorship.** For the creator: the oracle held every answer through phase 3.2 on
  the day solvers first discussed the 3.2 plaintext (#2918, 2020-03-24), wrote in his
  voice, and marked the halving in the block that carried it. Against: #12653
  ("Correct"), no common-input link to the prize wallet, a custodial hot wallet as
  funding source, poster checkpoints that any phase-0 solver could compute, and the
  kangaroo tip. On balance it reads as a strong early solver's ledger. Treat block
  691563 as a solver's gesture unless new evidence ties 3GSMG24 to the creator.

The oracle confirms a value you already hold. It cannot lead to one.

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
application shell, with no door (doc 106; #32699, #32701). The original site answered
200 to every path, so 404 never discriminated on it (doc 68).

---

## 2. THE ENCRYPTION CONVENTION

Proven on three separate envelopes.

| item | value |
|---|---|
| container | OpenSSL `Salted__` + 8-byte salt + ciphertext, base64 |
| password | `sha256(answer)` written as **64 lowercase hex ASCII characters** |
| KDF | legacy `EVP_BytesToKey`, **md = SHA-256**, 1 iteration |
| cipher | AES-256-CBC, PKCS#7 padding |

Equivalent command:

    echo <b64> | openssl enc -d -aes-256-cbc -a -md sha256 -pass pass:<sha256hex>

`-md sha256` belongs on both encrypt and decrypt: the `Salted__` header stores only
the salt, and OpenSSL otherwise uses its compiled default digest (doc 70 §8). MD5 and
SHA-1 both fail the padding check on phase 2, so the SHA-256 KDF is the author's
parameter, demonstrated.

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
chance (sections 10.3 to 10.8 record four pad-3 events and one pad-4 event, all
random). Pad 1 and pad 2 are legal for the 80-byte containers and must be
preserved independently of ranking; heuristics alone cannot exclude binary plaintexts.
The revised testers retain up to 1,000 full records and report overflow explicitly;
no new puzzle searches or encrypted runtime checks were performed for this correction.

### The recogniser (doc 110)

Until 24 September the content check at pad 1 and 2 accepted printable prose, hex
keys, `gsmg.io/` + hex, WIF, BIP38, raw 32-byte windows and BIP39. It did not
recognise EBCDIC, UTF-16, compressed or container formats. The historical recogniser below was used in earlier tooling; the current `rt.py`,
`ct.py`, `ms.py` and `h3.c` have different rankings and do not implement all these
detectors or lock chaining. Revised tooling preserves valid pads independently of
ranking. Historical detector list:

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
another lock. Historical doc 110 tooling tried valid-padding outputs as passwords for the other
two locks (raw, hex, sha256 hex of each, both EVP digests), and the second-step output
goes through the recogniser. Control: a 79-byte random plaintext whose hex keys a
second envelope holding UTF-16 text. Found.

**What no recogniser can see.** A plaintext that is itself headerless ciphertext or
uniformly random bytes, at pad 1 or 2, cannot be told from a wrong password by its
content. Only a downstream step can test it. An encrypted 32-byte key in the usual
framings (IV + 48 bytes, or a nested `Salted__` with 48 bytes) is 64 bytes, which gives
pad 16 in an 80-byte container, and every harness flags that.

---

## 3. THE VERIFIED CHAIN

Four gates opened. Every value below is reproducible from the data in this file. The
phase-2/3 page is byte-identical to a 12 Nov 2020 archive capture (doc 69 §2).

### 3.A The backbone: Logic, "The Warning" (restored)

The puzzle follows the song "The Warning" by Logic (doc 22). It was dropped from this
file after doc 22 and restored on 23 September (docs 98 to 100). The full 13-line text
was supplied by the user and is kept out of the project; lines are described here, not
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

**The established solution uses this ten-slot template.** The unsigned coordinate is independently corroborated; the explicit minus sign and its intended treatment remain unresolved.

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

**The dropped `H` sign remains unresolved.** The retained plaintext explicitly
contains `* -1`; agreeing historical transcriptions corroborate that sign, but
this review did not freshly decrypt the stage. The accepted location reading
uses +42. The `B=25` step likewise uses the `i5` wordplay rather than ordinary
algebra on `5i` (which would yield -16 after squaring `4i`). Neither geographic
agreement nor historical negative tests repairs those semantic choices.

**Independent location corroboration (5 October 2026).** The unsigned point
falls inside the current official BAG footprint linked to Seattleweg 5,
3195 ND Rotterdam-Pernis, about 21 m from its address point. The historical
SafeNet address is documented by an official 2015 office-page capture, a 2019
NATO notice and a Companies House record. See [doc 119 §5](119-current-evidence-ledger.md#5-the-safenet-coordinate)
for exact sources and limits. This is stronger than the former regional/A15
association, but current geometry does not prove the footprint or a particular
entrance during the puzzle's original period. It does not settle the sign or
make the coordinate an unused downstream operand. The ambiguous multi-part
reply #8569 does not resolve that issue.

**The inline numerals are assembly indices into the seven-part phase-3 answer:**

| index | clue | where the clue lives | part |
|---|---|---|---|
| 1 | "1... are you looking for the private keymaker?"; the door's own answer, reused | page prose | `causality` |
| **2** | "the ironic **2name** of the keymakers" (a safe net, nearly unprotected in plain sight) | phase-2 plaintext | `Safenet` |
| **3** | "Crypto finally to the latin **3Moon**?" | phase-2 plaintext | `Luna` |
| **4** | "Tell me, **4How so mate**?", read aloud | phase-2 plaintext | `HSM` |
| 5 | "The **5binary** code is a part of the piece of this puzzle", via Executive Order 11110 | page prose | `11110` |
| 6 | "Its' raw data after 4 on row 1616" | page prose | genesis headline as reversed hex |
| 7 | "And now a buddhist is forced to move. What will be the next situation?" | page prose | the FEN after Rg6-c6 |

Only five parts carry a numeral (part 1's marker is "1... are you looking for the
private keymaker?" in the page prose); parts 6 and 7 carry none. The count is stated
another way: the page prints `--> parts 1..7 --> sha-256 -> dgst is the password to
enter Phase 3` (doc 69 §4).

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

Part 6 is the 69-byte Bitcoin genesis headline in reversed-byte hexadecimal:
`0x` plus 138 uppercase hex digits is exactly 140 characters. This is a
comment/printer representation, not an executable integer, a wallet address or
a hidden CBigNum operation. Bitcoin v0.3.10 matches row 1616, but the earlier
SourceForge-r133 walkthrough prevents treating it as a uniquely established
creator-selected release. A 140-character part does not establish a binding to
the later Architect “HUNDRED FOURTY” or “code you carry” sentence. #5960 addresses
the typo; it endorses neither 104 nor a new numerical rule. See [doc 119 §6](119-current-evidence-ledger.md#6-hundred-fourty-and-the-genesis-source).

Part 7 is the exact accepted puzzle FEN string after the Rg6-c6 move. Preserve
its case, spaces and counters rather than silently regenerate it. The retained
halfmove counter after a quiet rook move raises a move-history issue, not
malformed FEN grammar. The historical chess argument in doc 42 does not by
itself uniquely fix every textual counter.

The page also wraps two words in underscores, `_green_` and `_back_` ("Years later
the idea of this _green_ came _back_."), exactly twice on the page, both in the
paragraph that encodes part 6 (doc 69 §5). The `greenback` family was swept (226
candidates, 54,240 decrypts, planted control fired): null (doc 70 §1). It stays
unconsumed as a marker.

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
             = jacquefresco + giveitjustonesecond + heisenbergsuncertaintyprinciple
    password 250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c  (verified)
    plaintext 2,422 bytes, pad 10
    sha256   b82afeb86f9e50848220f9b64b744b821400308aea273a1c949b9d2d0e408a34  (verified)

The join is bare concatenation. The three answers separated by single spaces make a
64-byte string with sha256 `69706591bab926deb56b46707a2aa6e8a9ea8ab7219ea581f483b030c0a90fb6`,
which opens nothing.

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

The intro of the phase-3.2 plaintext names the cipher in the clear: "a beautiful
strategic position" is Beaufort, and "One for one, four for one" is 1141, the EBCDIC code page
(CP1141 is CP273 plus the euro sign, and no euro occurs in this data), as well as the
checkerboard's escape digits 1 and 4.

Take plaintext bytes [447:1986), decode as latin-1, **encode** to **cp273**, read the
resulting bytes as lowercase letters (a = 0), then **reciprocal Beaufort** decrypt,
`P = K - C mod 26`, with key `THEMATRIXHASYOU`. Result, 1,539 letters, canonical as
unbroken lowercase (uppercase here for legibility). Of the EBCDIC code pages tried, only cp273 turns all
1,539 bytes into lowercase letters; cp1140, cp500 and cp037 give 1,451 letters and
cp1026 gives 1,368. Generated from the plaintext and re-derived by script on 29
September:

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

It is a rewritten Matrix Reloaded Architect speech. Doc 45 reported an alignment
with 22 edits and 46% creator-authored wording; those counts depend on the chosen
transcript. Later comparison confirms inherited wording such as `sedulously` and
does not make `inherent to` a unique source fingerprint. Film audio was not checked;
punctuation and word breaks are editorial. Representative differences follow:

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

**Read as a manual (doc 96).** "Return to the source codes ... reinserting the prime
basics, after which you will be required to select from over twenty three ciphers
sixteen encryptions and/or seven intertwined passwords" can be read as a procedure,
but its receiver and selection are unknown. Prime reinsertion may already be DBBI;
the numbers lack a category-bound corpus. Doc 97's named index sets into nine texts
were historically tested, without exhausting alternate event selections or rules.

### 3.4b The straddling checkerboard

The 149 digits, generated from the plaintext:

```
15165943121972409169171213758951813141543131412428154191312181219433121171617137
149110916631213131281491109166131412199114371612126021664313711154112
```

Working key `FUBCDORA.LETHINGKYMVPS/JQZXW`, digits 1 and 4 blank in the top row
(the straddles). The riddle supplies "fubcd-king & oracle-queen, thingky mvps";
`ORA.LE` is a solver-constructed alphabet representation, not literal creator
punctuation or an independently authenticated dot clue.
Over all 45 choices of blank pair, exactly one reproduces the plaintext, and it is
{1,4}. The 149 digits parse as 33 single-digit tokens and 58 two-digit tokens, 91 letters
in all, and the 91 letters re-encode to the same 149 digits. The sentence immediately before the ciphertext is `One for one, four for
one.`, read as naming the two straddle digits (INFERRED). `ORACLE` appears as
`ORA.LE` in the solver-constructed alphabet: the repeated `C` is replaced by a
placeholder. That working representation is not creator punctuation and does not
establish a general dot convention. Result, 91 letters, verified:

```
INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE
```

The board's `.` cell (row 1, column 0) and `/` cell (row 4, column 4) are never used,
so the cipher emits no word breaks. The spaced reading ("In case you manage to crack
this...") is a human word-split.

**Read that message as ownership logistics.** "Half" and "Better Half" are people:
the creator and his partner (he calls his wife "the better half", #39241, #60324).
It sits immediately before the Terminal envelope and reads as a warning attached to
that object (section 6.5). The Architect text and the creator's "a private key"
(#4624) both speak of one key.

---

## 4. THE FIRST IMAGE, COMPLETE

### 4.1 Layout

14x14 grid of 75-pixel cells at the top of the image, then a red divider `#ED1C24`
from y = 1047, the title, a QR code and the prize address. The image is 1048 pixels
wide, so the last column is clipped to 73 pixels, and the divider starts 3 rows inside
the last row of cells. The grid region contains **exactly five colours and zero
anti-aliasing**:

    #000000  86 cells      #FFFFFF  85 cells      #3F48CC  15 cells
    #FFF200   9 cells      #FEFEFE   1 cell

These colours are the Windows Paint default palette. Measured on the image on 29
September, every cell is one flat colour except the seven rabbit cells (section 4.4),
a one-pixel white column at the right image edge and the three divider rows in the
bottom row of cells; there is no sub-cell steganography. The poster has **101** set
cells (black 86 + blue 15), a prime.

### 4.2 The colour layer

Exactly 15 blue and 9 yellow. Their spiral positions are all `= 7 (mod 8)`, the LSB
of each of the 24 characters, blue = 1 and yellow = 0. The colour layer repeats
information the black and white cells already carry. Sequence in spiral order:

    B B B B Y B B B Y Y B B B B Y B B Y Y B Y Y B Y

The 9 yellow and 15 blue match the 9 primes and 15 non-primes up to 24 in count only.
The yellow cells sit at character positions 5, 9, 10, 15, 18, 19, 21, 22 and 24
(1-based), and the primes up to 24 are 2, 3, 5, 7, 11, 13, 17, 19 and 23.

### 4.3 The anomaly cell: the painted rose

One cell is `#FEFEFE` at grid row 7, column 4 (0-based): row-major 1-based 103,
spiral 0-based 163 (bit 3 of character 20, the `n` of "planted"). It is a light cell
with **6 of its 8 neighbours dark**. A solver marked the same cell in 2020 (#2899) and
the creator replied "Interesting" (#2905). It is the splice at position 21 of the
25-symbol program that parses dbbi (section 6.3), where it must act as blue although
it carries bit 0.

**Fixed-prefix result.** With the first 23 events assigned in order to the first
23 prime positions, the off-white cell must act as blue for the recorded DBBI
fit. The song/painted-rose reading is an interpretation. The following comparison
does not cover alternate event selections or globally exclude L84:

| treatment of `#FEFEFE` | consumed | hosts | all hosts start `b` | exact fit |
|---|---:|---:|---|---|
| forced to blue (consume 1) | 91/91 | 23 | yes | **yes** |
| forced to yellow (consume 2) | 92/91 | 23 | no | no |
| left in between (dropped) | 91/91 | 23 | no | no |

Read through *Alice* Ch. VIII (section 7.2), it is the white rose painted by the
gardeners. Uniqueness here is restricted to the tested fixed-prefix grammar; the later audit
retains alternate selections. It does not prove that every possible painting or
selection rule has been excluded.
The creator's farewell page prints it as 0, its message bit, and gives it no special
status (doc 108); the forced-blue reading is neither supported nor refuted by that.

**Which cell (doc 105, correcting "1 in 12").** **14** spiral positions (152 to 158,
160 to 166) give the walk the same program. Of those, only 163 is prime counted from
zero on the spiral and prime counted from one in reading order, which is "First or
zero" (#4105), posted right after the creator re-pointed to the Roses poem. Two other
pairings (spiral 1-based with row-major 1-based; spiral 1-based with row-major
0-based) each select a single different cell. The pairing was chosen after seeing the
answer. Fair price about 1 in 5. It supports the cell's identity and does not prove
the rule.

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
the first two nest counts; an observation, null as passwords (doc 103). The rabbit
faces left with its eye at cell (7,7); its gaze along row 7 reaches the off-white cell
(7,4), the only anomaly on its line of sight, which a solver noted in March 2020 (doc
43).

### 4.5 Other poster facts

The QR code encodes the blockchain.com URL for the prize address; pristine, no hidden
data. `sha256("GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe")` =
`89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32` is the side-page
URL, reached via `HASHTHETEXT` from the Decentraland (-41, -17) audio side quest (the
word comes from the audio's spectrogram after inverting one stereo channel and mixing
to mono; carried from the earlier logs, not re-derived). This is the "second door" of
2020 (doc 39). `follow_the_white_rabbit.png` is an uncropped copy: 350x350, 14 cells of
exactly 25 pixels, no divider. Sampled at one pixel in three, the poster's grid has zero
differences from it over 121,801 compared pixels. Its colour counts are black 54,675
(86 cells of 625 pixels plus 925 ink pixels, the 37 rabbit ink blocks of 25), white
52,200 (85 cells minus those 925), blue 9,375, yellow 5,625 and `#FEFEFE` 625.

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
`<!-- Nice to see you around! Good luck little bunny hunter ;) -->`, which is a
rebuild addition and absent from the archives (doc 55).

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
| `dbbi` | [0,91) | 91 | `a..i` | fixed-prefix prime-host/color fit; remaining role unproved, see 6.3 |
| a/b run | [91,195) | 104 | `a`/`b` | `matrixsumlist` VERIFIED |
| `faed` | [195,765) | 570 | `a..i` | characterized stream; filler model unproved, see 6.4 |
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
   literals read "sha256, our first hint is your last command" and "sha256 the
   answer too" under one reading. The literal is `anstoo`; `enter` coincides
   with the 64-character `openssl enc -a` wrap, but its full role is unsettled.

"Our first hint" is identified from primary data: the creator's first hint is #225,
the bare phase-1 hash, followed by #226 "just try hit your options against that
hash", described by him in #257 as "A hash which we provided". The first hint was a
sha256, and the last command is one too. **This supports a method reading, but does not uniquely settle the two SHA
operations, `enter`, or the receiver of `anstoo`.** Asked for help with it in 2024, he replied 🤐 (#20224).

```python
def rule2(block):
    d=''.join('0' if c=='o' else str(ord(c)-96) for c in block)
    n=int(d); h=hex(n)[2:]
    if len(h)%2: h='0'+h
    return bytes.fromhex(h)
# control: rule2(soup[766:829]) == b'lastwordsbeforearchichoice'
```

### 6.3 dbbi: verified fixed-prefix fit, unresolved purpose

```
dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe
```

**The parse.** Splice the off-white `#FEFEFE` cell into the poster's colour sequence
at its spiral position, which lands it 21st, giving a 25-symbol program:

    BBBBYBBBYYBBBBYBBYYBFYYBY          F = FEFEFE, at position 21

Walk logical positions from 1. At a non-prime position, consume one character of
dbbi as filler. At a prime position, take the next program symbol and consume 1
character if blue (F counts as blue), 2 if yellow; that chunk is a "host". 23 primes
are <= 83; 8 of the symbols are yellow. 83 + 8 = **91, the stream consumed exactly**
(re-verified by script for this edition).

    hosts 23, consumed 91/91, last logical position 83
    hosts starting with 'b'      23/23
    yellow hosts exactly 'be'     8/8

Controls: F as blue parses; F as yellow overruns (92); F dropped does not parse
under strict acceptance. Nulls: 200,000 frequency-preserving shuffles of dbbi, zero
at 23/23; 200,000 random programs of the same composition, zero valid parses.
Exhaustion over all C(23,8) = 490,314 assignments leaves exactly one,
`BBBBYBBBYYBBBBYBBYYBBYY` (the spliced program's first 23 with F as blue), under an
acceptance rule written after seeing the winner; the shuffle null stands on its own.

The parse was first posted by the solver Ugur Keser (#72215, 2026-09-18), who read
dbbi as a checksum confirming the poster's colours and left the puzzle. That reading
has a verified mathematical part: the host characters restate the color program
under the stated correspondence. Calling the remainder filler is an interpretation
(below), not proof that no other payload exists.

This is what `yellowblueprimes` names. The creator's own confirmation: asked about
primes while a solver discussed `#FEFEFE`, "You are at the prime part already???"
(#5966, section 8.1).

**L=83 is selected by the fixed first-23-event model, not globally.** An older
program-free grammar gave one L84 construction; the later independently reported
selection audit retains three L83 branches and two L84 branches. One-per-byte
does not uniquely select a branch, and an extra prefix criterion is unsupported.
Only the final raw character 91 (`e`) changes endpoint role between the L83/L84
residue views; their 22 internal gaps contain the same 59 letters. The L84
residue appends `e` to the L83 residue below. No audited branch has a fully
supported continuation. Counting event 24 blue again after an L84 branch has
already consumed it is an accounting error. Exact branch scope and receipt
limits are in [doc 119 §2](119-current-evidence-ledger.md#2-dbbi-the-poster-and-faed).
The 23/16/7 count match does not identify a source-mandated selection operation.

**What the parse leaves.** The program has 25 symbols and the walk consumes 23; the
two left over are `B` and `Y` (unexplained). The 31 host characters (23 `b`, 8 `e`)
re-encode the colour program. The 60-character residue:

```
difhccgihaeeihggegebgehhehhfafdhffcdbfcccgfeggecdcifffgigeea
```

**The residue is statistically compatible with a filler model (doc 101).** A shared generator and absence of another payload are not established.

| symbol | a | b | c | d | e | f | g | h | i |
|---|---|---|---|---|---|---|---|---|---|
| residue (60) | 3 | 2 | 8 | 4 | 10 | 10 | 10 | 8 | 5 |
| faed (570) | 54 | 49 | 52 | 49 | 69 | 57 | 107 | 58 | 75 |

G-test against faed's distribution G = 10.40, p = 0.26 (20,000 simulations); against
uniform G = 13.59, p = 0.11; log-likelihood ratio +1.59 for faed's generator (about 5
to 1). The `g` share is 0.167 against faed's 0.188 and uniform's 0.111, so the residue
carries faed's signature excess of `g`. `b` is under-drawn (2 of 60, about 5
expected), which fits a generator that kept `b` out of the filler so as not to confuse
the `b`-marked hosts.

**Verified under the fixed correspondence:** DBBI contains `b`/`be` hosts at prime
positions matching the color program. The checksum-only/shared-filler-generator
interpretation is plausible but not proven, and does not exclude another role.

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

The final 32 characters contain no `e` and no `g`: the longest pair-free suffix in
faed, P = 0.0201 after paying for the choice among the 36 symbol pairs. (The
change-point G-test at cut 538 has P = 0.0040, and BIC does not support a split;
doc 86.) Carry faed as one object.

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

**dbbi with `b` as the zero (2^25) is closed** (doc 115): all 33,554,432 subsets, in
numeric and string forms, forward and reversed, 4.03 billion decrypt tests, 0 hits.

**Open by size alone:** faed with arbitrary `g` choices (2^107, not enumerable).

**Current conclusion:** the recorded statistics are compatible with a biased
filler generator; purpose, shared generator and absence of other payload remain
unproved. Negative tests in section 10 are restricted to their actual coverage
and detector. The last 60 characters contain six `g`s; do not confuse that with
the verified 32-character `e`/`g`-free suffix. Asked in September
2026 whether dbbi and faed were meant to be decoded or used only as ingredients, the
creator replied 🤐 (#70325).

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

**Conditional plaintext bounds.** Under CBC/ECB with 16-byte PKCS#7 padding,
80 bytes imply 64–79 plaintext bytes and 1,328 imply 1,312–1,327. Bare WIF/BIP38
length exclusions apply only under that hypothesis; `Salted__` and length do
not identify the locked cipher or rule out stream modes. Cosmic Duality's
content is unknown; its size does not prove “message, not key.”

The two 80-byte containers are two objects (separate headers and salts, no shared
block, no salt XOR structure). The salts are `openssl`'s random values: the three
containers that are already open (phase 2, phase 3, phase 3.2) carry salts that mean
nothing, and the shut ones look the same. The byte-level XOR and interleave of the two ciphertexts, their salts and
first blocks, and each container keyed by another's text or bytes, are null (docs 103,
107).

**Order and use remain unknown.** #39237 calls yinyang the next phase in reply
to an AES-decode question. It does not name Cosmic Duality's plaintext, prove
that short opens first, or establish mandatory use of all three containers.
Their different provenance strengths are summarized in [doc 119 §3](119-current-evidence-ledger.md#3-envelopes-route-and-the-two-sha-readings).

**The Terminal has no riddle beside it (doc 96).** Every other locked object has its
instructions adjacent. The object immediately before it is the checkerboard message
("in case you manage to crack this, the private keys belong to half and better
half..."), which reads as a warning attached to the Terminal. That adjacency is
in-artifact evidence: the Terminal is the last object in the phase-3.2 plaintext. Asked
"is the PK in the last cipher of 3.2?", the creator answered "There must at least be
something hidden in there" (#2918). Doc 59 §2b hedges that quote: the question relays
a third-hand claim, the Terminal blob was first pasted in chat at #3806 (2020-05-09),
and twenty minutes before #2918 he declined to localise the key as "too much of a hint"
(#2910). Those details motivated two historical hypotheses: instructions on the SalPhaseIon
page, or an association with “raising the stakes.” They are not an exhaustive
either/or or a verified mapping of instructions to this envelope.

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

    yellowblueprimes             SOLVED: the dbbi parse, section 6.3
    matrixsumlist                a label also inside the textarea; a prime operation
                                 (section 8.1); operand outside the page (section 9)
    lastwordsbeforearchichoice   a label also inside the textarea
    yinyang                      NEVER IDENTIFIED; the operation reading is closed
                                 (section 9)

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
there" (#4102), and again on 2025-12-31 (#53342, section 7.3). It is the most
authoritative hint in the corpus (doc 103). "First or zero" (#4105) answers a question
about which piece is "the first puzzle piece" (rabbit poster = piece zero, rebus =
piece one); it is not a general indexing convention (doc 39), though it fits the cell
test in section 4.3.

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

On 2025-12-31 the creator posted five messages of 1, 2, 3, 4 and 5 dots (22:15 to 22:19
local time, one minute apart; the four-dot message is #53339), then a binary message
at 22:20 that decodes (from the export) to:

    Happy new year! Make the best of everything. Oh, and here's a "tiny hint" <3.

**The quotation marks cite #881 (docs 111, 112).** In the creator's own words "tiny
hint" occurs twice: #881 (2019, "we'll release a tiny hint at the start of 2020, that
will be the final hint") and this message. #881's tiny hint is the Roses poem (section
7.2), so #53342 is a third re-pointing to it after #4096 and #4102. The `<3` fits the
Queen of Hearts, whose croquet ground is Chapter VIII. This strengthens the *Alice*
reading and the {2, 5, 7} prime set. It yields no value.

**The dots.** Some solved text supports one-dot-per-letter readings. The following
examples have different provenance and do not establish a universal convention:

| location | dots | elided | status |
|---|---:|---|---|
| phase-3 riddle 1, "the ...... is ours" | 6 | CHOICE (*The Choice Is Ours*) | verified by the chain |
| phase-3.2 intro, "... am I here?" | 3 | WHY (Neo's line to the Architect) | exact film line |
| checkerboard working key `ORA.LE` | 1 | C | solver-constructed duplicate-letter placeholder; not a creator punctuation clue |
| #8311, reply to the Cosmic Duality cover | 4 | nothing | ordinary ellipsis (doc 112) |
| #53335 to #53341 | 1 to 5 | unknown | open; locator null |

In chat the convention has no support. He writes four dots as a plain ellipsis in
#990 (`Well.... yes`), #8311 and #66568 (`On that thing... is the actual answer....`).
No run of five consecutive words of lengths 1, 2, 3, 4, 5 (or 5 to 1) exists in any of
the 492 creator messages (shuffled word order gives a mean of 0.43 such runs) or in any
chain text, and 3,000 four-letter words, each also crossed with `yinyang`, `cosmicduality`,
`thatisveryspecific` and `choice`, are null (section 10.8). Playing-card pips, Ace to Five, the natural *Alice* reading of five
counted dots, were run in doc 115 with the gardeners as cards (13,319 strings, alone and
crossed with the last-words pool, 112 million decrypts): null.

### 7.4 The Cosmic Duality cover, #8310, verified

The export's file for #8310 (`image_2022-12-11_07-09-14.png`, barrystyle,
2022-12-10) is the cover of Time-Life *Mysteries of the Unknown: Cosmic Duality*: a
starry yin-yang whose two seed dots are a white light (upper half) and a yellow light
(lower half). barrystyle found it by searching the page heading ("honestly, i just
searched for cosmic duality: mysteries of the unknown", #26257), so it reflects no
hidden insight. The creator's reactions are to the book itself: ".... That is very
specific" (#8311, four dots as an ordinary ellipsis) and "If the puzzle is solved
you'll see how scary specific that is" (#8315). The book's page-9 caption reads: each
half of the yin-yang "holds the seed of its opposite: the dark yin contains a tiny
speck of yang, and the paler yang embodies an embryonic germ of yin". The seed, the
planting and the opposites all sit in the song line that built the URL (section 3.A).
Every contiguous passage of the book is screened and null; the seed-of-the-opposite
operation is screened and null (section 10.6).

---

## 8. THE HINT CATALOGUE

Every id was checked verbatim against the Telegram export. Attributed to Jrk Bgrt /
SoWut. The creator-only extract is `jrk_messages.txt` in this project: 492 messages
with the header of each reply (the parent's author and first words; a reply to a
message missing from the export reads "not in export"). All 492 were re-read against
their parents on 23 September (doc 103); section 8.6 lists what that changed.

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
On balance it answers gnomad. The idea behind the book, a resource-based economy
(#26875, "I simply liked Jacque's ideas a lot"), lines up with the Architect's added
"please just help us build it" and the checkerboard message's "they also need funds to
live" (doc 111).

**The Hope line answers a question about the door.**

```
3389 Tracer   The door that leads to the source?
3390 Jrk      Humph. Hope, it is the quintessential human delusion, simultaneously
              the source of your greatest strength, and your greatest weakness.
3391 Jrk      (not a hint btw, just fooling around)
```

The Architect's last speech before Neo's choice of door, which is what
`lastwordsbeforearchichoice` names. Screened and null (section 10.6).

**Other endorsements with their parents.**

| creator | parent | note |
|---|---|---|
| #2905 "Interesting" | #2899 spiral grid with the `#FEFEFE` cell marked | then #2918 "There must at least be something hidden in there" (answering whether the PK is in the last cipher of 3.2; caveat in section 6.5) |
| #3902 "Well spotted" | #3901 "the half of prize went to better half" | the halving |
| #4096 "This one" | #1710 the Roses poem | then #4102 "answer is there" |
| #4696 "Correct" | #4695 "Is it the next stage of the second route?" | 2020 second door |
| #7418 "Good point" | #7416 "go to the first puzzle piece (image) and hash all the text you see" | HASHTHETEXT |
| #8311 ".... That is very specific" | #8310 the Cosmic Duality cover | section 7.4 |
| #8483 "👆" | #8448 the reversed #8446 decode | confirms the decode |
| #12653 "Correct" | #12580 "the blockchain messages are not his and are not part of the puzzle" | 29 August 2023 generic denial; not a specific reply to later 2025/2026 texts |
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
| #66587, #66588 | 2026-07-12 | "salphaseion is 100% solveable?" then "Yes" (adjacent messages; #66588 carries no reply link) |
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
| #5960 | typo response to a solver proposing 104; establishes neither 104 nor an operational meaning of 140 |
| #7529 | the 1 Apr 2021 `{1},{4},{21}` post was an April Fools joke |
| #9607 | "is there another URL to find?" -> "No need. You have all the info." |
| #12653 | generic blockchain-message denial dated 29 August 2023; later messages require their own authentication |
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
| #2918 | "There must at least be something hidden in there" | answers "is the PK in the last cipher of 3.2?"; that is the Terminal (caveat in section 6.5) |
| #3404 | "And Oen" | unexplained. One and Neo are both anagrams |
| #3923 | "The price is in half, but what does it mean" | halving/ownership wording; a key-split operation is not established |
| #9595 | "my friends and family can get to all my data if they'd work together" | no established instruction to combine key shares or contact anyone |
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

## 9. CURRENT MODEL AND OPEN OBLIGATIONS

The decoded labels and embedded artifacts are facts. Their intended operations,
operands, assembly, selection and receiver remain unknown. No derivation yet
fixes a route through the three locked envelopes. [Doc 119](119-current-evidence-ledger.md)
is the current discovery ledger and supplies the detailed corrections.

| block | length | established versus inferred |
|---|---:|---|
| dbbi | 91 | fixed-prefix poster-color prime-host fit; checksum-only purpose unproved |
| a/b run | 104 | decodes to `matrixsumlist` |
| faed | 570 | measured biased stream; filler is a model |
| segment 1 | 63 | decodes to `lastwordsbeforearchichoice` |
| segment 2 | 29 | decodes to `thispassword`; assembly and lock mapping unknown |
| literals | 35 + 12 | `shabef` supports SHA-256; the two operations/receivers remain open |
| a/b run | 40 | decodes to `enter`; matches a wrap boundary, full role unproved |
| base64 halves | 128 | joined short envelope; use and cipher not independently solved |

`yellowblueprimes` has a strong fixed-correspondence mathematical realization.
The prime hints do not prove that a distinct “reinsertion” operation remains.
`matrixsumlist` and `lastwordsbeforearchichoice` are unsolved labels; their
operands are not proven to lie outside the page. `yinyang` is an unresolved
operation/destination; no named envelope is uniquely established as its receiver.

The known stage grammar and song/film correspondences are useful analogies,
not a theorem of unique answers or universal formatting. Phase 3 combines
different source classes and retains mixed case and FEN spaces. The 23/16/7
numbers lack a category-bound corpus. “Half and better half” describes ownership
and funding, without an authenticated split/secret-sharing instruction.

---

## 10. WHAT HAS BEEN TRIED AND FAILED

Historical reported experiments, ordered by how expensive they would be to rediscover. A null applies only to its full tested tuple. “Closed” below means the recorded family, not all possible mechanisms; doc 118 supplies detector and membership caveats. Some of
the per-run logs behind these tables were retired in the 29 September cleanup (section
15 lists them); the tables here are their record, and doc 67 indexes the logs that
remain.

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

### 10.2 FAED: historical tested families

The numerical rows below preserve reported results. Older statistical “all”
exclusions were too broad: non-uniformity does not exclude every modern cipher
or payload representation, and the dependence/randomness statistics do not
prove all substitutions impossible or establish filler purpose. Each method is
limited to its explicit representation, source and detector; see docs 118/119.

| family | scale | result |
|---|---|---|
| modern cipher | historical broad claim | non-uniformity is an observation, not universal cipher exclusion |
| positional encoding of a payload | historical broad claim | depends on the modeled payload distribution; not an exclusion of all encodings |
| zero-reinsertion | exhaustive to k<=18, 18.8 billion nodes | 0 survivors |
| zero-substitution (a symbol stands for both its digit and 0), as text | exhaustive, all nine symbols, six objects, both directions | 0 solutions (doc 90) |
| zero-substitution as a binary payload against the locks | ~16.8M decryptions, then the recogniser with chaining | 0 (docs 109, 110) |
| running key, aperiodic, 19 keystreams, every offset to 1400 | 1,132,326 | nothing beats the ciphertext (doc 87) |
| short periodic key, periods 2..100 | 99 | P = 0.71 |
| straddling checkerboard / VIC, all 45 escape sets | 45 | P = 0.9225 |
| the phase-3.2 checkerboard reused on residue, dbbi, faed, every zero choice | 3 objects x 18 | below each block's own shuffle null (doc 101) |
| columnar transposition, widths 2 to 120 | 119 | P = 0.83 / 0.91 |
| homophonic substitution, all 21,145 set partitions | 21,145 | P = 0.2233 / 0.4300 |
| binary partitions under rule 1 | 2,976 | 0 hits |
| substitution of text | historical broad claim | measured dependence does not exclude every substitution model |
| hand-typed filler | historical broad claim | reported randomness tests do not prove provenance or purpose |
| all 362,880 symbol relabelings | 2,903,040 | 0 |
| every substring of length >= 8 of the five letter objects | 1,556,802 | 0 |
| faed as a matrix: row and column sums at every width dividing 570, as ASCII | 28 lists | noise (doc 96) |

### 10.3 The passphrase-screen sweep

Every candidate below went through the exact win test and all containers, with
controls validated first.

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
| 481 hand-visited door paths on the live site | **void, not null**: the original site returned 200 for every path, and the live site is a 2026 rebuild (doc 68) |
| the "Infrared" hint (#6250), three readings | negative; the hint itself is unexplained |
| `matrixsumlist` as key-operation-payload | null, and one theorem: row sums and column sums of any matrix total the same, so a list of row sums followed by column sums must split into two halves of equal sum; with a = 1 ... i = 9 the residue totals 336, dbbi 422 and faed 3,079, and none has a contiguous equal-sum split (faed's odd total forbids it), so no stream in the textarea is itself a row+column sum list. Sum lists as running keys over faed, 3,024 configurations: 19 of 20 shuffles match or beat the real best. Sum lists computed from the streams: beaten 30 of 30 by shuffles for each stream. The residue as a zero-reinsertion map: beaten 40 of 40 |
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
| `F` as consume-0 in the walk | the only strict parse remains F as consume-1 at L=83 |
| the riddle-block vocabulary, alone and spliced into every join | ~590,000, 0 |
| derived-key constructions (XOR, HMAC, PBKDF2 of corpus pairs) under both password profiles | ~38,000, 0 |
| the dbbi residue as a number | 0 |
| prime-position zeroing of published text | null everywhere |
| the 479 prime-sum pointer: 42 traversals x 3 `#FEFEFE` treatments, 263 numbers | 3,196 screens, 0; consistent with chance (section 12) |
| creator-authored single tokens and short messages | 8,812 strings, 0 |
| Neo's passport (11 Sep 2001) | 307, 0; conversational, not a hint |
| `{eps3.4_...}` clause and the episode's strings | 1,586, 0 |
| `_green_` and `_back_` (the emphasis markers on the phase-2 page) joined as `greenback` and swept | 54,240 decrypts, 0 (docs 69, 70) |
| the 2026 OP_RETURN stream | 379, 0 |

### 10.6 Session of 22 September 2026 (docs 90 to 95)

Docs 92 to 94 were retired in the 29 September cleanup; their results are in this
table. Harness for every row: win test on both point forms (key 1 validated), all
three containers, both password profiles (sha256 hex and raw), both EVP digests
(SHA-256 and MD5), padding then content. Controls: `causality` opens phase 2; a
planted 79-byte pad-1 plaintext is caught. Liveness measured on every run (for
example 1,092 valid pads against 1,050 expected over 268,728 decrypts).

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
| three-slot cross: 10 `yellowblueprimes` outputs x 58 `matrixsumlist` outputs x 25 last-words candidates, every order, with and without `thispassword` (the 58 include the 479/484 and 563/497 prime sums) | 82,710 | 0 |
| `phase3.1_old.aes` | 1 | a re-encryption of the known plaintext |
| prime-walk detector on faed (program-free, 1, 2 or 3 characters at primes, all nine host letters, start 1 to 1,100). Control: dbbi parses completely at position 1 | 19,800 walks | no complete parse; best run 6 hosts, the median of 30 shuffles |
| poster sum lists as keys over the residue and dbbi: 54 lists (rows, columns, both diagonals, 2x2 blocks, per-character popcounts along the spiral, spiral rings, prime rows and columns, ones counted up to each prime, sums between consecutive primes in spiral and row-major order, prime-weighted colour sums), values or digits, cumulative or not, both directions, every offset, add / subtract / reverse-subtract mod 10, then rule 2. Planted control recovered at 1.00 | 45,888 | best lowercase 0.44 (residue), 0.34 (dbbi); null ceilings 0.44 and 0.37 |
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

### 10.8 Session of 25 September 2026 (docs 111 to 114)

Harness (doc 111): win test on both point forms plus the four EC-neighbour targets (key
1 validated), all three containers, four password forms (sha256 hex, raw, sha256d hex,
sha256 of the hex), both EVP digests, the structure-agnostic recogniser and lock
chaining. Controls before every run: `causality` opens phase 2, key 1 gives
`751e76e8...`, a planted 79-byte cp273 pad-1 envelope is caught. Doc 114 used the fixed
convention of section 2 (sha256 hex, SHA-256 EVP), flagged pad >= 2, ran the
recogniser on every valid pad, and planted a joint plaintext as its control.

| what | scale | result |
|---|---:|---|
| `matrixsumlist` on the poster with the gardeners' {2, 5, 7}: 1,558 lists (13 cell encodings including the resistor colour code, Paint palette position, dbbi consume counts and the painted cell as white, red or blue; row, column, block, chunk, diagonal, residue-class, cumulative and prime-index forms), each tested three ways for exact fit against shuffled posters | 1,558 lists | longest digit run inside a textarea block: 8 real, median 8 shuffled (range 7 to 10); list total equal to one of 40 published numbers: 72 lists real, mean 79 shuffled; dbbi-style prime walk that consumes a block exactly with one host letter: 0 real, 0 in 96 of 100 shuffled. No fit beats chance (doc 111) |
| the same lists as passwords: four joins, reversed, a1z26, ASCII where valid, with each label front and back | 104,885 candidates, 2,517,240 decrypts | 0 flags; 9,837 valid pads against 9,872 expected |
| last words at the position each list total names: Architect text, phase-2 plaintext, checkerboard message, phase-3.2 intro; at T, T+1, T-1; last 3 to 30 letters and last 1 to 5 words; the Architect ones also prefixed by their own list | 318,448 candidates, 7,642,752 decrypts | 0 flags; one chain flag, noise (below) |
| halves: the first and second half of every chain answer, label and key phrase, swapped, reversed, interleaved (doc 111); every ordered pair of the 23 chain atoms, the two container base64 halves as one key, the "half / better half" phrases (doc 114) | 292 + 1,757 | 0 |
| dots: the 3,000 most frequent four-letter English words in three casings, each also with `yinyang`, `cosmicduality`, `thatisveryspecific` and `choice` front and back; the word-length locator over chain texts (doc 111) and all creator messages (doc 112) | 3,000 words, crossed | 0 flags; no length-1..5 run anywhere |
| *Looking Forward* as a Fresco idea: 70 concepts (resource-based economy, The Venus Project, sociocyberneering, cybernation, the circular city and others) in six casings with every label front and back and all ordered pairs; "help us build it"; "funds to live"; the #8446 binary read forward | about 9,800 | 0 |
| the literal #8446 joint password: 2,500 poster sum-list strings x 1,620 last-words strings (the last 3 to 27 letters before the Architect's choice points, and those located by every sum-list total), with and without `thispassword` | 8,100,000 joint passwords, 24,300,000 decrypts | 0 flags (doc 114) |
| the 23/16/7 selection: round-robin and plain interleave of every ordered 2- and 3-atom selection over the 23 atoms; the first 7, 16 and 23 atoms concatenated, interleaved and reversed | 22,221 | 0 flags (doc 114) |
| every string generated in docs 111 to 113 against the EC-neighbour addresses | 1.56 million | 0 hits (doc 113) |

Doc 111 totals: 466,441 candidates, 11,194,584 decrypts, 43,710 valid pads against
43,900 expected, 467,040 chain decrypts.

**The one chain flag is noise (doc 111).** Candidate `646457108795886mmingofthispuzzleyouare`
gave a pad-1 output on SalPhaseIon short (MD5 EVP, hex form). That 79-byte output's
hex, used as the Cosmic Duality password (SHA-256 EVP), gave **pad 4**, 1,324 bytes.
Content: printable 0.35 (random 0.37), 255 distinct bytes (expected 254.6), no bit
bias, no header, no nested salt. Pad >= 4 has a chance of about 2^-32 per decrypt; over
11.66 million decrypts about 0.0027 events are expected, so this is a 1-in-370
coincidence, and the key is the hex of a random pad-1 output from a meaningless
candidate. Recorded so it is not rediscovered as a lead.

**What the session adds.** The poster under the gardeners' primes yields no list that
fits any textarea block or published number better than a shuffled poster. The words
"last words before" have been read at the position each list total names, in four
chain texts (the Architect text, the phase-2 plaintext, the checkerboard message and
the phase-3.2 intro). The recorded halves, selected list strings and literal-text crosses gave no
validated result under their tested configurations. They do not establish that
all arrangements of known objects fail or that the operands must lie elsewhere.

### 10.9 Session of 29 September 2026

Harness: win test on both point forms plus the four EC-neighbour targets (key 1
validated), all three containers, sha256 hex and raw sha256 as passwords, both EVP
digests, pad then content. Controls fired first: key 1 gives `751e76e8...` and
`causality` opens phase 2.

| what | scale | result |
|---|---:|---|
| **The `yellowblueprimes` output as the `matrixsumlist` operand.** The 25-symbol spliced colour program laid out as a 5x5 grid (5 is a gardener, and the two leftover symbols `B`, `Y` sit in it), five encodings (blue 1 / yellow 0 with `F` as 1 or 0, the reverse, and the consume counts 1 and 2), row, column, diagonal, reversed and joined sum lists, as digit strings, comma, space, dash, letters and a..i forms | 327 candidates, 3,924 decrypts | fit: longest run of a list (as a..i letters) inside the textarea is 5 for the real program against a median of 5 for 300 shuffles of the same composition (max 10); 0 flags; 11 valid pads against about 15 expected |

The pipeline reading (each label acts on the previous stage's output, so the solved
`yellowblueprimes` result feeds `matrixsumlist`) names an operand with a definite form.
That form gives no fit and no password.

**The queue of doc 115.** Same harness and controls; every pad >= 3 flag re-decrypted and
content-checked (426 flags, 0 hits); the 85 pad-1 distinct-byte flags on Cosmic Duality
are the expected Poisson tail (about 71 predicted).

| what | scale | result |
|---|---:|---|
| **dbbi with `b` as the merged zero:** all 2^25 subsets of its 25 `b`, numeric (integer bytes, hex text) and string (digit string, letter string with `o`) forms, forward and reversed | 4.03 billion decrypt tests | valid pads 9,478,364 vs 9,474,192 expected (numeric), 6,316,109 vs 6,316,128 (string); 0 recogniser hits |
| **letter and mod-10 forms of the poster sum lists** (1,547 lists in 17 encodings; L1, L0, M10, forward and reversed) crossed with the last-words pools (`lw_core` 175, `lw_loc` 6,613, `lw_words` 6,341), with and without `thispassword`; plus the earlier digit, comma, space, ASCII, hex and total forms | 1.24 billion decrypt tests | 0 hits; pad statistics at expectation |
| **operand families with a fit test:** page-object sum lists read as English; sum lists as indices into six chain texts; digit-form lists against faed, dbbi and the residue; 73 constant and sequence corpora against the same | 10,094 letter strings; 25,660 selections; 23,417 digit strings; 473,421 digits | all at their shuffle nulls (longest word 7 vs 6 to 7; 914 selections with a 6-letter word vs 870 to 875; longest match 9 vs 11 shuffled; no constant match past the seed of 8) |
| **operand families, decrypts only:** remainder forms (mod 2 to 13), RGB and pixel values, the adjacent-operand reading, walk numbers (400, 474, 874; 317, 557), every textarea substring, card pips and gardeners, page-object lists | about 2.0 billion decrypt tests | 0 hits |
| **win test on the crossed pools:** 71,022 sum-list strings x `lw_core`, with and without `thispassword`, single hash; base pools of about 497,000 strings, single and double hash | 24.9 million strings; 497,000 strings | 0 hits |

Totals of doc 115: 22 runs, 7.29 billion decrypt tests, 28,576,797 valid pads against
28,574,986 expected. No derivation names the operand with a fit above its shuffle null.

**What the pools held.** So that the same cells are not run again. The scripts are in
`tools/` (`tools/README-tools.md` has the table of which pool each script rebuilds).

The 17 poster encodings (each maps a cell to a number; `cell` letters K black, W white,
B blue, Y yellow, F the painted cell): `bit_F0`, `bit_F1` (the cell's bit, F as 0 or 1);
`res_Fwhite`, `res_Fred`, `res_Fblue` (resistor code K 0, Y 4, B 6, W 9, F as 9, 2 or 6);
`consume` (K 0, W 0, B 1, Y 2, F 1); `idx_kbyw` (K 1, B 2, Y 3, W 4, F 4); `idx_wkyb`
(W 1, K 2, Y 3, B 4, F 1); `pal1`, `pal0` (Paint palette index from 1 or 0: K 1/0, W
11/10, B 9/8, Y 6/5, F 11/10); `w1_F0`, `w1_F1` (1 for white, F as 0 or 1); `painted`,
`colour_only`, `blue_only`, `yellow_only`, `dark` (1 for F; for B or Y; for B; for Y; for K
or B). Each encoding gave 91 sum lists: rows, columns, both reversed, rows plus columns
in both orders, prime-indexed rows and columns from 1 and from 0, gardener subsets of
{2, 5, 7} by index and by multiple, diagonals and anti-diagonals, the two main
diagonals, 2x2 and 7x7 blocks, and for the flat and the spiral order the chunks and windows
of 2, 5 and 7, the mod-2/5/7 classes, cumulative sums at the gardeners and at primes,
values at primes, the total, and the 3x3 gardener sub-matrix. Forms of each list: digits
joined, comma-joined, space-joined, a1z26 mod 26 (0 as `z`), a0 mod 26, each value mod 10,
ASCII characters (values 32 to 126), two hex digits per value (values below 256), and the
list total; forward and reversed, at most 400 characters. After removing duplicates:
10,677 strings.

The last-words pools, cut from the 1,539-letter Architect text: `lw_core` is `A[o-k:o]` for k
= 3 to 27 and o = 341, 371, 472, 479, 1238, 1483, 1539 (175 strings); `lw_loc` is the same
windows for o equal to each distinct poster sum-list total (6,613 further strings);
`lw_words` is the last 1 to 20 words at every word boundary of the 334-word split,
joined without spaces (6,341 strings). The joint password is the sum-list string followed
by the last-words string, with and without `thispassword` after the pair.

Other pools: the textarea substrings (lengths 4 to 120, forward and reversed, letter form
and, where all letters are a..i or o, digit form, plus the hex, binary, decimal-ASCII and
a1z26 forms of the six label words: 404,796 strings); the poster as RGB and pixel values
(14,936 strings); page-object sum lists under six value maps (24,454 strings); remainders
mod 2 to 13 of the poster lists (19,913 strings); the adjacent-operand pool (`dbbi` sum
lists with `faed` slices, and head and tail windows of `faed` and the residue in letter
and digit form); walk numbers (400, 474, 874, 420, 494, 317, 557 in several writings and
Architect windows anchored at them); playing-card strings (Ace to Five and the
gardeners, digit or word ranks, suits, `of`, five separators; 13,319 strings). The
remainder pool is rebuilt only in part (74%) and the adjacent, walk and card pools have no
script; their definitions above are what the record holds.

### 10.10 Sessions of 3 and 4 October 2026 (docs 116 and 117)

**Doc 116, the doc 115 coverage gaps.** Second password order, raw and double-hash forms
on the four large crosses, scripted re-derivations of the five unscripted pools
(`tools/mkmissing.py`), and the win test on the crossed pools in both orders and under
double hash: 26.8 billion decrypt tests and 195.7 million private scalars, valid pads at
expectation, 1,940 flags all content-checked as noise. Null with live controls. Run logs
in `claude/doc116-runs/`. No further coverage sweeps are planned.

**Change of method (`claude/critical-review-2026-10-03.md`).** Every opened password was a
riddle answered from outside knowledge and concatenated; decoded data only ever gave
messages or checks. New work must pass a retrodiction gate (does the method reopen
phase 2, 3 and 3.2 from what a solver could see, judged on the plaintext hash, not a
valid pad) and is tested as one reading, one candidate, a few at a time.

**Riddle ledger R1 to R35 (doc 117, `claude/riddle-method/README.md`).** Film readings of
both labels (23/16/7, the door line, `theproblemis`, `wewont`, `neo`, `yourlife`, `trace`,
`101`, the 3.2 blank choice), first-hint readings (#225, #867), a per-lock split (left door
Terminal, right door short, Cosmic the pair), line-ending forms, answers as written,
shell history, the poster program's remainder, and Satoshi's genesis comment block
(`main.cpp` v0.3.10, a corroborating row-1616 match in the checked tag survey, not a uniquely established creator source). About
2,500 candidate strings and 1.68 million decrypts under three testers (convention; newline
forms; 14 ciphers x 5 KDFs including PBKDF2-SHA256 10,000), valid pads at expectation,
0 flags, 0 win-test hits, controls fired in every run.

**Other results of the same days (doc 117).** Ciphertext lengths excluding headers are 80, 80 and 1,328 bytes, compatible with padded
16-byte block encryption. They do not establish AES or exclude stream modes. A 1/4,096
length-residue estimate requires independent uniform residues, not established here.
Historical leak controls used 64 random bytes for the 80-byte short/Terminal ciphertexts;
the log describes 80, so its calibration provenance is uncertain. Randomness cannot
identify AES. Under 16-byte PKCS#7 CBC/ECB, short/Terminal plaintexts are 64 to 79 bytes
and Cosmic is 1,312 to 1,327 bytes; contents and lock mapping remain hypotheses. A mandatory route, short-first order and Terminal-only rabbit-hole classification
were historical inferences, not established by those statements or blob provenance.
11,397 structural key checks (solved-gate keys and IVs, every 32-byte and 64-hex window,
grid and digit integers) are null. #6509's "unforeseen hint" is the prime slip #5966,
consistent with the DBBI interpretation, without proving its role fully spent. The
1008/868 pointer lacks reproducible selection provenance. The reported poster
checks found no additional channel in the inspected forms (QR clean at codeword level). The approved 23/16/7 bounded enumeration
(`claude/selection/`, about 1.31 billion candidates) was stopped twice by an automated
safety check and **never ran**: that space is untested, not null.

**The pair ledger (`claude/common-flaw/README.md`).** `matrixsumlist` and
`lastwordsbeforearchichoice` may feed one password; the clue says `thispassword`, not
a definite assembly or lock mapping. Under the joint hypothesis a null applies only to
the pair and complete configuration tested. The
record struck readings off per label anyway, and each camp paired only within itself
(docs 114 and 115: poster lists x Architect-text windows; R1 to R35: riddle M x film L).
Block (a), poster row and column sums in six list forms x film last words, 456 candidates,
454,176 historical decrypts with controls and no heuristic flags. The generator omitted
144 L+M+thispassword assemblies, and unranked padding-1/2 binary outputs were suppressed.
The corrected 600-string set has not been searched. Block (b), riddle M x the 175 `lw_core` windows
(about 3,500 candidates), is untested.

### 10.11 Session of 21 October 2026 (doc 120)

**Terminal and SalPhaseIon-short under a full-padding gate.** Both hold 80 bytes of
ciphertext, so a 64-character hex key would show pad 16 (pad 15 with a newline), which
chance gives at about 2^-120. A preregistered list of 753 strings generated from puzzle
text (the four literals in every order, the textarea's `sha…` strings and first hint,
phase-2 X2SH leftovers including H = -42, phase-3.2 text outside the Architect block,
literal pairs in `doc120-runs/pair_ledger.tsv`) under 17 password/KDF forms: 25,602
attempts, 97 valid pads against 100.4 expected, all pad 1, 0 recogniser hits, 0 prize
hits. Phases 2, 3 and 3.2 retrodicted through the same code; three planted envelopes
fired. Much of the list overlaps doc 117; the new parts are the gate and full retention.

**One shared prize gate.** `tools/prize_gate.py` (also in the sibling repositories)
gates Half and Better Half under both serializations and parses raw, hex, WIF, mini,
base64, decimal and sha256(text) keys out of plaintexts. Rescan of this kit and the
rebuilt phase plaintexts: 94,046 scalars, 0 hits.

---

## 11. METHODOLOGY, LEARNED EXPENSIVELY

1. **A null is only as good as its control.** State the control and confirm it fired.
2. **A null must sample the class of outcome, not the specific one.** Worked example:
   `keYmgma` -> "key eyes" was published at 1 in 200,000 with the first word held
   fixed; the honest price is about 1 in 481 conditional, and real faed yields fewer
   readable variants than its own shuffles.
3. **A null is only as strong as the target it ran against.**
4. **Screen cheap, confirm expensive.** Price every chain event before believing it: a
   pad-4 event over 11.7 million decrypts is a 1-in-370 coincidence (section 10.8).
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
17. **Check a data file against the artifact it was derived from.** `matrix.json`
    carried one wrong cell (row 7, column 6, the rabbit's ink) for twelve days; the
    image measured directly gave the right grid. A second copy of a value confirms
    nothing.

### Corrections of record

- `/phase1verification` was declared dead on a uniform 413; the 413 was CSRF.
- The EBCDIC codec is **cp273** with **reciprocal** Beaufort, and the cp273 bytes are
  lowercase letters.
- The checkerboard digit string is **149** digits.
- The four leftover spiral bits are **`0000`**.
- `#FEFEFE` is forced blue under the fixed first-23-event DBBI correspondence; alternate selections are not globally excluded.
- faed's "drift" is 32 of 570 characters, and the permutation P for its tail is 0.0201;
  0.0040 is the change-point test's figure (doc 86).
- A correction can be a regression: the 83-cell parse was "reopened" by a comparison
  that left the off-white cell out (doc 71 §1).
- This file regressed twice against doc 71 (the tag alphabet, "on the highway"). Fixed
  on 22 September.
- **Container order:** older short-first/Cosmic-message claims overread #39237. Section 6.5 now leaves the receiver and order open.
- **"First or zero"** is not a general indexing convention (doc 39).
- **The song was dropped** from this file after doc 22. Restored as section 3.A.
- **The painted-cell count is 14**, not 12 (doc 105).
- **The dbbi residue filler claim** (doc 101) was too strong; compatibility with FAED
  statistics does not establish purpose or absence of another payload.
- **The first farewell-page run used `--quiet`**, which hides pad 1 and 2. Redone with
  the recogniser (doc 108). Doc 118 later identified additional pad-1/2 retention
  limits; old zero flags are not an exhaustive binary-plaintext exclusion.
- **The oracle did not go silent in April 2020.** Its signed messages run to
  2021-07-18. The later ones are inbound from other keys (doc 113).
- **The two "Good job, Neo!" addresses are poster checkpoints** (docs 07 and 21 called
  them a solver's wallet; doc 113).
- **`1NULY7Dhzu...` is a tip address** (doc 113); an earlier reading took it for a
  vanity message.
- **The four-dot reply #8311 is an ordinary ellipsis** (doc 112); earlier editions took
  it for an elided word.
- **The 481 door paths are void, not null.** The original site answered 200 to every
  path (doc 68).
- **#2918 as proof that the Terminal holds the key** is hedged: the question relays a
  third-hand claim, and the Terminal blob first appears in chat at #3806 (section 6.5).
- **`matrix.json` centre cell (7, 6)** was black; the image says white. Fixed on 29
  September.

---

## 12. WHERE IT STANDS

Four gates opened. Three containers shut. Both oracles closed. Over 30 million
candidates were screened through 22 September; the 23 and 24 September sessions added
about 1.5 million more and about 28 million further decryptions under the
structure-agnostic recogniser with lock chaining; the 25 September sessions added
466,441 candidates (11.2 million decrypts) and 8.1 million joint passwords (24.3
million decrypts), plus 23,978 halves and selection candidates (doc 114); the 29
September queue (doc 115) added 7.29 billion decrypt tests; doc 116 (3 October) added
26.8 billion more and 195.7 million win-test scalars; the riddle rounds of 3 and 4
October (doc 117) added about 2,500 hand-justified candidates and 1.68 million decrypts
under 14 ciphers and 5 KDFs. All null with live controls.

**Current state (6 October).** The established stage solutions and exact artifact
identities stand. DBBI has a verified fixed-prefix fit; alternative selections,
FAED purpose, SHA/`enter` interpretation, operation, operands, receiver, selection
and lock order remain open. The unsigned SafeNet coordinate is independently
corroborated at a historical address/current building; its sign is unresolved.
Genesis part 6 has exactly 140 characters, but “hundred fourty” is not bound to
that length or to “code you carry.” See [doc 119](119-current-evidence-ledger.md).

**21 October (doc 120).** Terminal and SalPhaseIon-short were run under a full-padding
gate on 753 preregistered puzzle-text strings (25,602 attempts): null with live controls.
All stored outputs in this kit were regated through the shared `tools/prize_gate.py`
(both targets, both serializations): 0 hits.

No new unlock or private key is known and no search is running. Historical
negative counts do not establish proximity or exhaustive coverage. Under a
joint-password model, the complete tested tuple is what failed, not an isolated
label or all possible partners. No named envelope has a proven first priority.

### The five leads of the 25 September edition, worked (docs 111 to 114)

1. **`matrixsumlist` as a prime operation on the poster with {2, 5, 7}.** 1,558 lists,
   three exact-fit tests against shuffled posters, 104,885 password candidates. Null.
2. **"Last words before archi choice" by structure**, located by the sum lists. 318,448
   candidates. Null.
3. **The halves.** 292 + 1,757 candidates. Null.
4. **The dots.** Locator over every creator message and chain text: nothing. Fills:
   null. #8311's four dots are an ordinary ellipsis, and #53342's "tiny hint" cites
   #881.
5. ***Looking Forward* as a pointer to a Fresco idea.** About 9,800 candidates. Null.

Also worked: the literal #8446 joint password (8.1 million, null) and the 23/16/7
selection space (22,221, null) (doc 114); the EC neighbours as win targets (1.56
million strings, null) (doc 113).

### What remains

**The missing rule.** A new lead needs an independently supported operation and
its operands, receiver, selection and serialization, followed by a justified
downstream validation. Exact fits require their correspondence assumptions;
post-hoc uniqueness criteria and readable fragments are not sufficient.

**Provenance.** Exact Terminal and short-envelope bytes have historical
corroboration; Cosmic Duality's historical presence has screenshot support of
different strength. Current copies and shared ancestry must not be counted as
independent proof. See doc 119 §3. Authenticity alone does not fix the route.

**Untested extensions, all low prior:**

- faed with arbitrary `g` choices, 2^107, not enumerable (section 6.4)

Closed on 29 September (doc 115): dbbi with `b` as the merged zero, the letter and
mod-10 forms of the sum-list pool crossed with the last-words pools, and playing-card
pips for the New Year dots. The doc 115 coverage gaps (the double-hash
forms in the container harness, the second password order and raw form on the four
large crosses, the unscripted pools, the win test on the crossed pools in the second
order and under double hash) were closed on 3 October (doc 116): 26.8 billion decrypt
tests and 195.7 million private scalars, null with live controls.

**Historical unrun spaces, recorded 5 October (not queued):** block (b) of the pair ledger (riddle M answers x
`lw_core` windows, about 3,500 candidates, held back by the no-sweep rule), and the
approved 23/16/7 ordered selection over the 23 chain atoms (about 1.31 billion, never run;
doc 117 section 8). Neither is an active task or a source-established 23/16/7 construction.

**The Terminal's instruction mapping remains unknown.** The SalPhaseIon page and
“raising the stakes” were two proposed associations (section 6.5), not an
exhaustive choice or proof that no adjacent wording can instruct its use.

### Spent leads, kept so they are not re-proposed

- **The 479 prime-sum pointer.** Blue primes 484, yellow 479, and `Architect[479:]`
  starts `PRIVATEKEY`. With `#FEFEFE` counted as the 25th coloured cell the sums are 563
  blue and 497 yellow (doc 93, retired; both crossed in the 82,710-candidate cell of
  section 10.6). Only the canonical spiral produces 479, but over the 263 numbers the
  traversal family generates the expected loaded-phrase hits are 1.88 against 1
  observed. Honest range 1 in 13 to 1 in 388, no downstream result.
- **The personal census.** Closed.
- **Neo's passport.** Conversational, and null.
- **The yinyang operation.** Closed.
- **The song as text.** Closed (section 3.A).
- **The a..i block experiments.** Recorded negatives remain bounded; purpose is not fully accounted for (section 9).
- **The rabbit's nest pixels.** The drawing, no data.
- **The relaunched site.** No new operand.
- **The halves at string and password level, the dots, *Looking Forward* as a Fresco
  idea, the 23/16/7 selection.** Null (section 10.8).
- **Riddle ledger R1 to R35, block (a) of the pair ledger, the genesis code, the 1008
  pointer, the poster photo, the structural key checks.** Null (section 10.10, doc 117).
  Read with the pair caveat above: a reading of one label is spent only against the
  partners it met.

### The surplus, current

Unconsumed by any verified derivation: the four centre cells (measured `0000`, rabbit
ink only); the two program symbols left over by the L=83 parse (`B`, `Y`); the trailing
`O` of `CIAOBELLAO`; the doubled `SELF`; the New Year dots (#53335 to #53341; locator
null, card pips null); "And Oen" (#3404); "as wide as the first one seen" (read as
the chessboard and as the reused checkerboard, both null, not consumed); and the two
operations named `matrixsumlist` and `lastwordsbeforearchichoice`.

**Historical “consumed” list, corrected 6 October:** song/`war` and Roses-poem
interpretations remain documented. Forced blue is conditional on the fixed-prefix
model; L83/L84 selection, residue purpose and the dropped `H` sign are not settled.
The painted-cell identity argument was post hoc (about 1 in 5). **Reclassified since the 25 September edition:** the four-dot reply
(#8311) is an ordinary ellipsis and left the surplus list.

### Before any future execution

Establish a source-supported rule and its scope, and read docs 118/119. A historical
command or unrun gap is not an instruction to resume a search. The current update
is documentation-only and no search is running.

---

## 13. COMPLETENESS NOTE

Verbatim and reconstructible in this file: the 1,075-character textarea; dbbi (91),
faed (570), the residue (60); the 1,539-letter Architect text; the 149 digits and
the 91-letter checkerboard plaintext; the 648-byte phase-2 plaintext; the phase-3
riddle head, the phase-3.2 intro and the checkerboard riddle; the poster's 196-bit
spiral string; the 25-symbol spliced program; all three locked containers; every
answer and password hex in the chain; the #8446 and #53342 decodes.

**Generation and verification.** The data blocks were first produced by script from the
phase-2 ciphertext, the phase-3.2 plaintext, the textarea, the three container files,
the poster image and the Telegram export. For the 29 September edition they were
re-checked by script from the primary data, and a block that failed would have been
caught:

- The phase-3 and phase-3.2 plaintexts were re-derived from the phase-3 ciphertext
  (sha256 `9163a38d...`) using the seven-part answer in section 3.3: 4,090 bytes,
  `c4ad9455...`, then 2,422 bytes, `b82afeb8...`, with both passwords reproduced.
- The phase-2 plaintext block is 648 bytes with six CRLF and hashes to `e2f9dd65...`.
- The phase-3 riddle head, the phase-3.2 intro, the checkerboard riddle, the 149 digits
  and the Terminal base64 equal the corresponding bytes of those plaintexts; 1,426 of
  2,422 bytes are strictly printable (58.9%).
- The Architect decode (cp273, lowercase letters, reciprocal Beaufort, key
  `THEMATRIXHASYOU`) reproduces the 1,539-letter block, `PRIVATEKEY` at 479 and 1238.
  The 149 digits decode to the 91 letters, and exactly one of the 45 blank pairs does.
- The textarea is 1,075 characters. Every segment decodes as stated; SalPhaseIon short
  equals the two base64 halves joined; the dbbi, faed and residue blocks match; the L=83
  parse consumes 91 at position 83 with 23 hosts, 8 of them `be`, and reproduces the
  60-character residue; the symbol counts match the tables; the dbbi/faed
  homogeneity G-test (36.44) and faed's non-uniformity (chi2 43.7) recompute.
- All three containers match their sha256, size and salt.
- The poster: the image hashes to `38125bbd...`. Cell colours measured directly from
  the pixels give 86/85/15/9/1; the spiral equals the 196-bit block with tail `0000`;
  the colour sequence, the `= 7 (mod 8)` positions, `#FEFEFE` at spiral 163 with six
  dark neighbours, the 25-symbol program, the 37 rabbit ink blocks by spiral position,
  and the 14 equivalent painted-cell positions (only 163 is prime by both counts of
  section 4.3) all recompute.
- Every full address passes base58check; the prize public key lies on the curve and
  hashes to `a9553269...` (uncompressed) and `06bbdc66...` (compressed); key 1 gives
  `751e76e8...`; the win test's control fires; the four neighbour hash160s regenerate
  the four truncated addresses in section 1.
- The creator's quotations, ids and dates in sections 3 to 8 were compared with
  `jrk_messages.txt`, and the #8446 and #53342 binary messages, copied from it, decode
  by script to the strings in section 7 (161 bytes for #8446). Parent messages by
  other users are known only from the excerpts in that file's reply headers.
- The addresses in section 1 regenerate by script: each checkpoint address from its
  preimage, the two Neo addresses from the poster URL (32-byte big-endian key, and its
  192 bits reversed), and the four neighbour addresses from the prize public key.

- The on-chain figures were re-pulled from mempool.space on 29 September: balances and
  transaction counts of the prize address, `17ucy...`, the compressed twin, the four
  neighbours, the six checkpoint addresses, the two Neo addresses and `1NULY...`; all 30
  transactions of `3GSMG24...` (14 signed and 16 inbound, with the blocks, dates and
  OP_RETURN texts of section 1); all 45 transactions of `17ucy...` (no spends, the two
  batches, 546 sat of dust, fees 450 and 550); and the block, date and nLockTime of the
  two halving transfers.

Not re-checkable in this session: the git history of the kangaroo tool repositories and
the custodial-wallet and common-input statements of section 1 (doc 113), and the
statistics in section 10, which are carried from their documents. Concatenate the lines of any fenced data block with no separators to
reconstruct the original string (except the phase-2 and prose blocks, whose line
breaks are real).

The song's text is deliberately absent (section 3.A).

Not here, and not needed: the solved phase-2 and phase-3 envelope ciphertexts (the
plaintexts are given), the non-printable middle of the phase-3.2 plaintext (its
meaningful parts are given decoded), and image files (fully described numerically).

### Three states, kept distinct

- **DECODED**: the object has been read.
- **CONSUMED**: its role in the construction is accounted for.
- **MINED**: every value it yields has been put through the win test and the
  containers.

A decode is not a mining run, and an assertion that sounds like a test result is the
single most expensive failure mode in this project's record.

---

## 14. SESSION DOCUMENTS 94 TO 119

Doc 67 indexes every surviving doc from 09 to 115 with errata for their stale
sentences, and maps each retired doc to the section that now carries it.

| doc | subject | outcome |
|---|---|---|
| 94 | dossier rebuild; `matrixsumlist` and last words worked | null; retired, folded into 10.6 |
| 95 | four fresh derivations | null |
| 96 | review; sha-before-combine, newline, XOR families | null |
| 97 | L=84 "select from"; side-page hash as first hint | null |
| 98 | riddle readings; the song thread recovered | song restored |
| 99 | the song's full text | null as text |
| 100 | song phase three | `war` tile and `#FEFEFE` consumed; L=83 |
| 101 | the dbbi residue | historical filler/shared-generator interpretation; weakened by doc 119 |
| 102 | chessboard and phase-2 template as the matrix | null; `H` sign read |
| 103 | all 492 creator messages re-read | #881, #2918, halves |
| 104 | the Roses poem | *Alice* Ch. VIII, primes {2, 5, 7} |
| 105 | the painted cell; the nest | 14 cells, 1 in 5; nest is the drawing |
| 106 | another door; archive pulls | null; app shell |
| 107 | whole stages, scalar, container XOR | null |
| 108 | the August 2026 farewell page | nothing new |
| 109 | merged-zero payloads against the locks | null |
| 110 | structure-agnostic recogniser, lock chaining | null |
| 111 | the five leads: exact-fit tests, located last words, halves, dots, Fresco | null; one pad-4 event, noise |
| 112 | the dot hints against the export | #8311 an ellipsis; "tiny hint" cites #881 |
| 113 | the 3GSMG24 oracle re-audited; 1NULY; EC neighbours | signed set; tip address; 1.56M null |
| 114 | joint #8446 password, halves, 23/16/7 selection | null; the operand is the wall |
| 115 | 29 September queue: dbbi `b` as zero, letter and mod-10 crosses, operand fit tests | null; 7.29 billion decrypts, no fit above a shuffle null |
| 116 | the doc 115 coverage gaps: second order, raw and double-hash forms, scripted pools, crossed win test | null; 26.8 billion decrypts, 195.7 million scalars |
| 117 | riddle ledger R1 to R35, independent model, constraints, rabbit holes, genesis code, photo, the pair ledger | reported nulls; 1.68 million decrypts; tuple-scoped, with doc 118 detector limits |
| 118 | correctness audit and source remediation | non-encrypted checks; encrypted/C verification limits; no corrected search rerun |
| 119 | current evidence and discovery ledger | 6 October source/interpretation reconciliation; no new unlock or search |

---

## 15. REVISION HISTORY

**6 October 2026 reconciliation.** Added doc 119; updated current interpretations
of DBBI/L84, FAED, envelope provenance/order/cipher, SHA/assembly, SafeNet, genesis
140 and selection counts. Qualified historical detector/coverage claims. Preserved
primary streams, code, candidate files and raw run logs; no encrypted tests rerun.

### 29 September edition and 5 October update

**5 October 2026 update.** Docs 116 and 117 folded into the header, sections 10.10, 12
(totals, settled facts, the pair caveat, untested pairs and spaces, spent leads) and 14.
The work behind doc 117 is under `claude/` in one folder per workstream (listed in doc
117, section 12), and `claude/status.md` is the one-page status. Nothing else in this
edition changed.

This edition replaces the 25 September dossier. The 25 September edition had already
replaced the 22 September dossier and the 23 September addendum (docs 94 to 110 were
folded in then).

- **Docs 111 to 114 folded in:** sections 1, 7.2, 7.3, 8.1, 9, 10.8, 11, 12 and 14.
- **Doc 115 folded in (29 September, after the cleanup):** sections 6.4 (dbbi `b` as zero
  closed), 7.3 (card pips run), 10.9 (queue results), 12 (what remains) and 14.
- **Header, section 0 and section 10.9 (29 September, after doc 115):** the header and section 0 now list the files the dossier depends on (the creator's messages, the poster, the stage ciphertexts, `tools/`); section 10.9 defines the poster encodings and search pools that doc 115 named. The scripts were added to the Project under `tools/` and tested from a clean folder built from the Project's own files.
- **Section 0:** points to doc 67 as the index of the analysis log.
- **Section 1:** the win test carries the four EC-neighbour hash160s as near-miss
  targets; the oracle subsection is rewritten from docs 21 and 113 (signed set,
  checkpoints, the tip address, authorship) with the four neighbour addresses in full,
  regenerated from the prize public key; the original site's catch-all 200 (doc 68).
- **Section 2:** `-md sha256` is required on both encrypt and decrypt; MD5 and SHA-1
  fail phase 2; the pad-3 and pad-4 event count.
- **Sections 3.2, 8, 13:** #8569 is one three-line message ("Correct." / "No." /
  "Can't say anything about this."), so both quotes in the log docs are real and only
  their pairing with questions is open; `jrk_messages.txt` is named as the creator
  message source; the verification list gains the quotation, decode and address checks.
- **Section 3:** the chain of custody (doc 69), the #8569 quote note, the
  numeral-indices fact (five parts carry numerals; the page prints parts 1..7), the
  `greenback` null, the chess-move uniqueness (doc 42), the Beaufort hint, and the
  cp273 lowercase wording.
- **Sections 4.1, 4.4, 5:** the grid measured from the image; the rabbit-gaze note;
  the bunny comment is a rebuild addition.
- **Sections 6.3 to 6.5:** the Ugur Keser attribution; the tail P corrected to 0.0201;
  the BIP39 result and the padding note; the #2918 hedge.
- **Sections 8.4, 10 (intro), 10.2, 10.5, 10.6:** #66588 has no reply link; 19
  keystreams; the door paths are void; the matrixsumlist theorem and its supporting
  nulls; the composition of the 54 poster lists; the 10.6 heading now lists docs 90 to
  95 and says which are retired.
- **Section 13:** every data block re-verified from primary data (listed there).
- **On-chain re-check (29 September, mempool.space):** the prize balance is 1.25636967
  BTC (the 21 September figure was 1.25635374; the address keeps receiving dust); the
  second halving transfer confirmed on 2024-04-24 at block 840,725 (the chronology said
  2024-04-20, the date of block 840,003 that its nLockTime names); the 2025-09-09 spray
  had 9 outputs, not 10; the bots' inflow is 0.01786 and 0.01762 BTC; the bech32 string
  in block 938165 is noted; the May 2026 vanity-address messages are listed in spend
  order (`message-sequence.json` had them in another order and is regenerated). Every
  other on-chain figure listed in section 13 matched, including the 14 signed
  transactions of `3GSMG24...`. The re-check also found the `SalPhaseIon sumlist AES`
  message (section 1), sent from a key anyone can compute; doc 07 lists it with the
  other traffic on the public keys.
- **Added after the cleanup, same day:** section 10.9 (the colour program as a 5x5
  matrix, null, and the queue that followed) and the closed provenance item in section 12
  (later SalPhaseIon captures match ours).
- **Small facts folded in from the retired reference docs:** the spaced-join hash of
  the phase-3.2 answer, the cp273-only result, the checkerboard token counts and unused
  cells, the prime-position note on the colour layer, the rabbit image's size, hash
  relation and colour counts, and the salt argument (sections 3.4, 3.4a, 3.4b, 4.2,
  4.5, 6.5). Doc 05's decoded-artifact and hint tables and docs 01, 02, 03 and 06 were
  already in sections 3 to 9.
- **Retired (39 files and one duplicate):** the 23 September addendum, 33 numbered log
  docs (10, 11, 19, 20, 27, 28, 31, 32, 34, 36, 37, 44, 46, 47, 49, 51, 52, 54, 56, 57,
  61, 62, 74, 79, 80, 83, 84, 85, 88, 89, 92, 93 and 94) and the five reference docs
  01-overview, 02-verified-chain, 03-unsolved-material, 05-hints and 06-first-image.
  `cosmic-duality.txt` held the same base64 container as `cosmic-duality.b64`
  (which adds only a trailing newline).
  Their results are in sections 3 to 11. The README lists the files that remain, and doc
  67 lists the errata for stale sentences in the kept logs.

### Correctness audit, 5 October 2026 (doc 118)

Historical logs remain unchanged. Heuristic flags are rankings, not cryptographic
validity or complete exclusion. Revised testers preserve every padding-valid output
in bounded records, reporting overflow as incomplete review. The hardcoded
`gen_riddle.py` verifies known-answer regressions, not independent generation.
Reconstructed pool counts do not prove inclusion of vanished original artifacts.
Every result must record source, extraction, assembly, serialization, cipher/KDF,
detector and downstream validation; negative results apply only to that tuple.
