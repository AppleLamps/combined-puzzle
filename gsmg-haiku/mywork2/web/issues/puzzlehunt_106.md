# puzzlehunt#106 [Research] Decoded author hint (2023), color-frame proof, oracle KDF correction, fake-solution debunking, and full KDF/mode sweep closure (eliooooooot 2026-08-22, open)

# GSMG.io research report: decoded author hint, color-frame proof, oracle KDF correction, fake-solution debunking, and exhaustive sweep results

Two-session independent investigation (~2.5B verified tests). Full ledger + reproducible scripts preserved; happy to share any artifact.

---

## Part A — [Correction] `open-crypto-puzzles` oracle.py uses EVP-MD5; its sweeps were void

`floflo777/open-crypto-puzzles` ships `tools/oracle.py` as a "certified" checker for the small final blob (salt `3ab585348552415d`). Its `evp_bytes_to_key()` uses **MD5** — but every *solved* blob in this chain decrypts only under EVP-**SHA256** (`openssl enc` post-1.1.0 default). Verified against phase2/phase3/phase3.2 with known passwords (MD5 fails all three; SHA256 succeeds all three). Every password sweep through that oracle (tested.md row 8: 116,043 candidates) was structurally void.

**Refinement:** the Cosmic Duality blob is the exception — it demonstrably decrypts under EVP-MD5 with a raw-digest password. The author mixed openssl versions across stages; test under BOTH KDFs.

## Part B — [New data] The author's hidden 2023 message decodes to plain English

His 2023-02-23 Telegram binary block is ASCII transmitted **bit-reversed** (every byte ends in `0b110`). Reversing bit-order per byte:

> "yellow blue primes matrixsumlist lastwordsbeforearchichoice yinyang
> we wont give away the password its in front of your eyes but youre not seeing it
> very last step is a true giveaway promised"

This is the author naming the final-password ingredients.

### Color-frame proof in puzzle.png (reproducible)
- Extract all 196 squares' colors. Bits (K,B=1 / W,Y=0), read on the **down-first counterclockwise spiral**, decode **24/24** to `gsmg.io/theseedisplanted`.
- All 24 blue/yellow squares sit at EXACTLY spiral positions {8,16,...,192} = the last-bit cell of each of the first 24 bytes. Blue marks bit=1, Yellow bit=0 at every byte boundary: an author-designed frame proving the reading convention.
- Counts: Black=86, White=86 (perfect balance), Blue=15, Yellow=9.
- True sum lists: rows `610876654997879`, cols `8108108736759668`.

### Author-confirmed red herrings (dated Telegram screenshots)
- **2021-02-12:** "#...# wasn't used." → the Phase-2 table (# X 2 S H 4 Y 0 Q B 15 #) is NOT part of the solution.
- **2021-02-12:** "2nd way wasnt founded (shared)." → an alternative path exists, unfound.
- **2023-08-06:** "Once you hit a 'ying yang', you'll be able to solve it the same day."
- **2023-01-09:** "At least prime number is very important to get any further."
- **2021-12-25:** primes definitely required; "some characters need to be 'zeroed out'"; "another door" still a thing.
- **2020-05-11:** after opening the "2nd door"... "The price is in half."

### Debunking the 2026 wave of fake solutions
The Half/Better-Half private-key claims rest on ONE AES decryption whose only evidence is valid PKCS7 padding (measured chance rate over 49,664 trials: **1/236**); token list items #5–#7 were admitted overfits ("constrained search + validation"). Issue #104's retraction is correct. Nobody holds any prize key; the dust/spend activity on 1JG648ya…/145ZQ9si… is just solvers sweeping publicly-derived addresses from that same unproven chain.

## Part C — [Sweep] Every openssl dimension is now exhausted
{EVP-MD5, EVP-SHA1, EVP-SHA256, PBKDF2-SHA256(10k)} × {raw-digest, hexdigest-string, direct-string} × modes {CBC, CFB128, OFB, CTR} × **all four open blobs** (small `3ab58534…`, dualite `2d3f6fe0…`, p32_trailing `b45a5e3d…`, urlblob `74c974e3…`) × ~56k principled candidates (hint assemblies, token orders, VIC/monologue renderings, hash chains, matrix-sum lists, selection masks): **zero genuine hits**. Padding events occur at exactly chance rate; stream-mode outputs checked by readability.

## What would actually move this forward
1. The **decoding method** of the two undecoded digit streams on the final page ("dbbi"/91 digits, "faed"/570 digits over {a..i}; canonical values via the Bifid square rows: D=0,B=1,I=2,F=3,H=4,C=5,E=6,G=7,A=8,K=9). Their mechanism is the last unexplained step — likely what "matrixsumlist" instructs.
2. Any primary material: pre-2023 Telegram archive, live Decentraland parcel state, or original contents of /followthewhiterabbit, /TheArchitectChoice, /hopeisthequintessentialhumandelusion… (never archived).
3. Author confirmation whether the small blob belongs to the intended path at all (his "2nd way" comment).

*Artifacts available on request: 21-section findings ledger, grid_color_analysis.py, gate.c/sweep2.c checkers, extracted streams, full hint-image corpus.*



---
## Naddiseo 2026-08-22
see #105 

---
## karim123e 2026-09-20
Hi eliooooooot,

I've spent 2 years 9 months on this puzzle. I've solved phases 0-3.2, SalPhaseIon tokens, and Cosmic Duality (SHA-256 matches).

I'm stuck on the FAED stream (570 chars).

I've tried:
- a1z26→hex, Bifid, matrixsumlist (10 sizes), yinyang (101)
- 14x14 grid mask, grid route, keyword transposition (30+ keys)
- Rail fence, Scytale, Playfair, Affine, Vigenère, Columnar
- XOR with JFK, THEMATRIXHASYOU, VIC, Master Key

Frequency analysis shows perfect English distribution (e:18.8%, t:12.8%, a:12.6%) but no readable text emerges.

The README says "the rest doesn't decode the same way." Naddiseo says "no one knows."

My question: Is FAED solvable? Or is it a red herring?

One hint would give closure after almost 3 years.

---
## Naddiseo 2026-09-23
> My question: Is FAED solvable? Or is it a red herring?
> 
> One hint would give closure after almost 3 years.

Puzzle creator says it's solvable. There have been no further hints. It's also been 5 years since this part of the puzzle has been discovered.
