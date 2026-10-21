# puzzlehunt#84 My journey through the GSMG 5 BTC puzzle – and why I believe it's unsolvable (a11yot 2026-03-02, open)

I've spent a considerable amount of time on this puzzle and wanted to share my findings, both to help others and to document the dead end I (and apparently others) have reached.

The Path So Far
I followed the well-known steps:

Decoded the 14×14 image spiral → gsmg.io/theseedisplanted

Uncovered the hidden form and password → causality

Decrypted Phase 2 and Phase 3 AES blobs using the provided passwords and the seven tokens (matrixsumlist, enter, lastwordsbeforearchichoice, thispassword, yourlastcommand, secondanswer, etc.)

Obtained the raw output from the Phase 3.2 blob (2432 bytes), then applied the final XOR mask and AES decryption as described in PR #68, yielding a 1168-byte file I called chain4.bin.

The Final Data: chain4.bin
chain4.bin (SHA256: a80a399af1221bd62538594141bee1064e1b071b547d60729f13c0224041a0f7) consists of:

A 48-byte header

Followed by 35 blocks of 32 bytes each

I extracted the 35 blocks and the header's first 32 bytes. The target public key x-coordinate (from the address 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe) is:
f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464

What I Tried
I systematically tested many ways to derive a private key from the 35 blocks and header:

XOR pyramid on the full list and on various splits (halves, prime-indexed blocks, etc.)

SHA256 of all those XOR results

XOR of all blocks and its SHA256

XOR with header as a mask (both per-block and cumulative)

Each individual block and its SHA256

XOR combinations of up to 5 blocks (brute-force) and their SHA256

XOR triangles with different row sizes (including the 1,2,3,4,5,6,7,7 arrangement and the half-splits with 1,2,3,4,5,2 and 1,2,3,4,5,3 as suggested by another AI)

None of these produced a value that matched the target public key.

The Turning Point
While searching for clues, I came across this Bitcointalk thread:
https://bitcointalk.org/index.php?topic=5151725.0

In it, multiple users report reaching the exact same point. One user (citb0in) posted the decrypted messages that I also encountered:

"YOUR LIFE IS THE SUM OF A REMAINDER OF AN UNBALANCED EQUATION ..."
followed by:
"IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF AND THEY ALSO NEED FUNDS TO LIVE."

Another user explicitly states:

"So the puzzle is a psychological trap, not a cryptographic challenge. The creator never intended a real solution. The BTC was never meant to be won."

Conclusion
After countless hours of work and testing every reasonable transformation I could think of, I've come to agree with that assessment. The puzzle appears designed to lead solvers through layers of cryptography only to end in a meta-message that questions the pursuit itself. The 5 BTC was likely never claimable; the real "prize" is the lesson.

I'm posting this to save others from the same fruitless effort and to document that the puzzle, as far as I and others can tell, has no solution. If anyone has a different experience or has found a way forward, I'd be glad to hear it, but for now, I'm moving on.

Thanks to everyone in the community who shared hints and code – it was a fascinating journey even if it didn't end with a reward.


---
## Naddiseo 2026-03-03
PR #68 is a rabbit hole of bad assumptions and faulty logic. That is, it's just spam, I wouldn't base any analysis on it, particularly how they "decrypt" the aes blob. 

---
## andersonbig 2026-04-26
> I've spent a considerable amount of time on this puzzle and wanted to share my findings, both to help others and to document the dead end I (and apparently others) have reached.
> 
> The Path So Far I followed the well-known steps:
> 
> Decoded the 14×14 image spiral → gsmg.io/theseedisplanted
> 
> Uncovered the hidden form and password → causality
> 
> Decrypted Phase 2 and Phase 3 AES blobs using the provided passwords and the seven tokens (matrixsumlist, enter, lastwordsbeforearchichoice, thispassword, yourlastcommand, secondanswer, etc.)
> 
> Obtained the raw output from the Phase 3.2 blob (2432 bytes), then applied the final XOR mask and AES decryption as described in PR [#68](https://github.com/puzzlehunt/gsmgio-5btc-puzzle/pull/68), yielding a 1168-byte file I called chain4.bin.
> 
> The Final Data: chain4.bin chain4.bin (SHA256: a80a399af1221bd62538594141bee1064e1b071b547d60729f13c0224041a0f7) consists of:
> 
> A 48-byte header
> 
> Followed by 35 blocks of 32 bytes each
> 
> I extracted the 35 blocks and the header's first 32 bytes. The target public key x-coordinate (from the address 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe) is: f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464
> 
> What I Tried I systematically tested many ways to derive a private key from the 35 blocks and header:
> 
> XOR pyramid on the full list and on various splits (halves, prime-indexed blocks, etc.)
> 
> SHA256 of all those XOR results
> 
> XOR of all blocks and its SHA256
> 
> XOR with header as a mask (both per-block and cumulative)
> 
> Each individual block and its SHA256
> 
> XOR combinations of up to 5 blocks (brute-force) and their SHA256
> 
> XOR triangles with different row sizes (including the 1,2,3,4,5,6,7,7 arrangement and the half-splits with 1,2,3,4,5,2 and 1,2,3,4,5,3 as suggested by another AI)
> 
> None of these produced a value that matched the target public key.
> 
> The Turning Point While searching for clues, I came across this Bitcointalk thread: https://bitcointalk.org/index.php?topic=5151725.0
> 
> In it, multiple users report reaching the exact same point. One user (citb0in) posted the decrypted messages that I also encountered:
> 
> "YOUR LIFE IS THE SUM OF A REMAINDER OF AN UNBALANCED EQUATION ..." followed by: "IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF AND THEY ALSO NEED FUNDS TO LIVE."
> 
> Another user explicitly states:
> 
> "So the puzzle is a psychological trap, not a cryptographic challenge. The creator never intended a real solution. The BTC was never meant to be won."
> 
> Conclusion After countless hours of work and testing every reasonable transformation I could think of, I've come to agree with that assessment. The puzzle appears designed to lead solvers through layers of cryptography only to end in a meta-message that questions the pursuit itself. The 5 BTC was likely never claimable; the real "prize" is the lesson.
> 
> I'm posting this to save others from the same fruitless effort and to document that the puzzle, as far as I and others can tell, has no solution. If anyone has a different experience or has found a way forward, I'd be glad to hear it, but for now, I'm moving on.
> 
> Thanks to everyone in the community who shared hints and code – it was a fascinating journey even if it didn't end with a reward.

@a11yot — your gap analysis in #84 documents chain4.bin as 1168 bytes 
(SHA a80a399af1221bd6...) with structure "48-byte header + 35 blocks of 
32 bytes each". My local reproduction of the same pipeline (PR #68 c2) 
yields:
- pre-AES (post-XOR-mask) = 1168B SHA f0bd54d102d8d930... (≠ yours)
- post-AES post-PKCS7-strip = 1151B SHA e4269ed5fbb202a8... (canonical)

Tested 12 reconciliation hypotheses (Salted__ prefix include/exclude, 
PKCS7 strip variants, header offset 31B vs 48B layout) — 0 matched 
a80a399a.

Could you specify exactly:
1. Is your 1168B chain4.bin pre-AES or post-AES?
2. Does it include the OpenSSL "Salted__" + 8B salt prefix?
3. PKCS7 padding stripped or kept?
4. Any byte transformation between PR #68 c2's output and yours?

This would let other solvers reconcile the divergence without re-running 
the full pipeline.
