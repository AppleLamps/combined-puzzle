# Active solve attempt

Goal: recover the GSMG.IO puzzle's private key and verify its public key against `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`.

**Status: unresolved. The goal remains active. No key or new stage has been verified.**

This directory contains new executable attacks and exact results, rather than another inventory of suggested clues. Original evidence was preserved.

## Completed work in this attempt

### DBBI–VIC tail: constrained hexadecimal recovery

The 64-letter tail was treated as a candidate encoded hexadecimal scalar. The explicit cipher model is `c_i = a*h_i + s*k_(i mod p) mod 26`, with `h_i` a hex nibble 0–15, an invertible multiplier `a`, and repeating shifts. This is a hypothesis; the length 64 does not establish it.

* For the native tail, every multiplier fails the hex-alphabet constraints at periods 1–16. Ordinary Vigenère/Beaufort multipliers fail through period 20.
* Rectangular row, column, snake and spiral read/fill transforms produced 220 distinct tails. At periods 1–12, only twelve finite models survived the alphabet constraints.
* Four models were enumerated directly: 155,520 constructions; none was the prize key. Additional source-key tests yielded two further valid scalars, also negative.
* An exact elliptic-curve meet-in-the-middle search then completed **all twelve** models, including the eight initially skipped large models. Together they represent 11,560,320 scalar constructions. Only 20,688 curve scalar multiplications were needed. No public-key match occurred. These counts include overlap between models.
* The 155,520 enumerated hex strings were also tested as passwords for all three locked envelopes. Forms: raw hex text, SHA256 hex of that text, and SHA256 hex of decoded key bytes; EVP-SHA256 and EVP-MD5, AES-256-CBC. **2,799,360 decryptions**, 10,945 padding-valid outputs, no readable/nested/valid compressed stage and no verified key. Every padding-valid plaintext is retained, including binary outputs.

All three already-opened puzzle envelopes were recovered to their exact known plaintext hashes before this last search. The curve meet-in-the-middle implementation passed point addition/subtraction checks against Node's secp256k1 implementation and recovered a synthetic known key.

Files: `structural-search.cjs`, `structural-results.json`, `tail-meet-in-middle.cjs`, `tail-mitm-results.json`, `tail-envelope-search.cjs`, `tail-envelope-results.json`, `tail-envelope-padding.jsonl`.

### Tail cipher keys selected from actual source text

Tested contiguous letters-only passages from 4,092 source documents containing 595,038 letters: original puzzle plaintexts, the local Looking Forward edition, and the creator's messages in both community exports. Tested native, reversed, and 8×8 row-snake tails; periods 1–64; all invertible affine multipliers and both source-key signs.

Only three passages satisfied all 64 hex constraints. All were the already-known VIC tail, at lengths 62, 63 and 64. The 64-letter case simply reverses `DBBI − VIC`, recovering DBBI digits; it is a positive control, not a new cipher key. None matched the prize public key. The accompanying JSON records the short envelope follow-through.

Files: `source-key-constraints.cjs`, `source-key-results.json`.

### FAED: exhaustive 3×3 Bifid followed by number-to-byte decoding

Tested every 3×3 square up to simultaneous row/column relabelling (60,480 representatives covering all 9! squares), every period 1–570, both input directions, and three numerical readings: base 9 with zero-based digits, bijective base 9, and one-based decimal.

**206,841,600 models.** Exact integer intervals reject impossible readable/header prefixes without requiring a nine-symbol intermediate to resemble English. All 94,161 prefix survivors are saved in full. None is completely printable; the best printable fraction is 0.539823. No retained compressed-header candidate successfully decompressed. This rejects the stated readable/recognized-header models; it does not reject arbitrary binary intermediates or other numeral/zeroing rules.

Controls: full Bifid round trips, numerical bounds, synthetic English → numeral → Bifid → exact original English, and 151 independent JavaScript reproductions of saved C++ results, all byte-exact.

Files: `bifid-numeric.cpp`, `bifid-numeric.exe`, `bifid-numeric-run.txt`, `bifid-numeric-results.jsonl`, `bifid-numeric-inspection.json`, `bifid-independent-check.json`.

### FAED: null symbol and octal packing

Removed each possible letter class in turn and tested all 8! remaining letter-to-octal-digit bijections, both input directions, offsets 0–7 and both per-byte bit orders. This includes the concrete hypothesis that the frequent `g` is a filler.

**11,612,160 models**, 2,368 retained prefix survivors, zero complete readable texts or successful decompressions.

Files: `null-octal.cjs`, `null-octal-results.json`, `null-octal-survivors.jsonl`.

### FAED and DBBI: direct Morse encodings

Independently checked the American Cryptogram Association's published Morbit example, then exhausted all 9! Morbit pair assignments and all 3^9 Pollux assignments in both directions, separately for FAED and DBBI.

FAED has no complete valid Morse parse under these direct models. DBBI has twelve grammar-valid Pollux outputs, all retained; none is a coherent instruction. Historical community messages had already proposed Morbit and claimed a negative brute-force result; this is an independent, controlled reproduction and extension to Pollux, not a claim that Morse is a newly discovered lead.

Reference: https://www.cryptogram.org/downloads/aca.info/ciphers/Morbit.pdf

Files: `morse-search.cjs`, `morse-results.json`.

### FAED: complete 2×2 affine matrix families

Tested all invertible 2×2 matrices and affine offsets modulo 9 and modulo 10, both input directions, adjacent/half pairing and interleaved/half output, followed by the stated numeral readings. All 3,888 invertible matrices mod 9 and all 2,880 mod 10 were covered.

**9,862,272 models**, 2,848 retained prefix survivors, no complete readable text or successful decompression. An affine encryption/decryption round trip passed.

Files: `affine-pairs.cjs`, `affine-pairs-results.json`, `affine-pairs-survivors.jsonl`.

### FAED: prime-marker transposition test

670 distinct full rectangular readings/fills were checked for a repeated symbol covering all prime positions, under both index conventions. No complete prime mask was found. The leading partial score is exploratory and does not establish a new pattern.

## Continuation: larger tail models and matrix-to-checkerboard bridges

The native tail's first feasible affine hex model occurs at period 17 with multipliers 5 and 21. Each permits **94,058,496,000** scalar constructions. Both were searched exactly against the prize public key using an incremental meet-in-the-middle method. Each search used 302,400 baby entries, 311,040 giant entries, 700,919 curve additions and 85 precomputed scalar multiplications. Neither matched. Curve arithmetic was checked against Node's secp256k1 implementation and the search recovered a synthetic known scalar. See `tail-period17.cjs` and `tail-period17-results.json`.

The complete 83/84-token parses were reconstructed from DBBI. Fifty distinct numeric keys were generated from the retained vectors, exact rectangular row/column sums and the first-occurrence key. Stable columnar and Myszkowski transposition, both directions, key reversal and input reversal produced **582 distinct complete FAED streams**. No source value was silently dropped. Exhaustive, prefix-pruned searches covered all **211,196,160 Morbit assignments** and **11,455,506 Pollux assignments** across these streams. None produced a complete valid Morse parse. Additional full-search controls recovered the exact synthetic plaintext in both families, beyond merely checking a published example. Files: `prepare-matrix-morse.cjs`, `matrix-morse-inputs.json`, `morbit-pruned.cpp`, `morse-matrix-pruned.cpp`, the corresponding run logs, and `morse-pruning-controls.json`.

The historical claim that Morbit was close came from solver discussion surrounding WhoAmI, not a verified creator endorsement. The inspected messages do not justify treating it as an authenticated hint.

The direct FAED stream was also parsed as a nine-column straddling checkerboard. Of the two-prefix cases, **58 complete parses** were attacked as unknown monoalphabetic substitutions. The `gi` prefix choice gives 436 symbols and IC ≈ 0.0743, but frequency similarity did not become a decode. Twenty simulated-annealing restarts per parse, 50,000 iterations per restart, produced no coherent full text. The 436-letter held-out control was recovered **exactly**. Its mean quadgram score was −4.01847; the best FAED result was −5.45227. Another 28 runs treated each single-symbol code in the `gi`/`eg` cases as a space; these also failed to produce coherent text. This is a heuristic search, not an exhaustive rejection of substitution. See `checkerboard-inputs.json`, `checkerboard-inspection.json`, `checkerboard-substitution.tsv` and `checkerboard-space-substitution.tsv`.

Finally, **21,820 complete one/two-prefix checkerboard parses of the 582 rearrangements** were compared against every eligible passage in 65 source documents (343,281 letters): the supplied Architect transcripts, original puzzle plaintexts, Looking Forward and long creator messages. The matching test permits any bijective substitution and requires the entire candidate's repetition pattern to agree. There were 79 short-pattern matches, but no complete puzzle match. The synthetic full-passage control was recovered. This is an exact negative for contiguous, letters-only source passages under the declared constructions; it does not exclude edited quotations, arbitrary selectors, digit-containing text or another layer. Files: `prepare-known-passages.cjs`, `known-passages.cpp`, `passage-inputs.json`, `passage-run.txt`, `passage-matches.tsv`.

The tail-envelope padding histogram contains only pad1/pad2 results. In particular, no candidate in that run produced 64-byte plaintext (pad16), whether textual hex or two raw 32-byte values.

## What remains unresolved

The DBBI prime-position construction still lacks a source-selected operation that produces the complete `matrixsumlist` operand or an unambiguous transformation of FAED. None of the above negatives excludes all further layers or establishes which branch must open first.

The original 83/84-token ambiguity, exact source order, full output of DBBI−VIC, and three actual locked envelopes remain the working constraints. Future work should build on these completed families instead of repeating the same plaintext/password guesses.

Possible next bounded attacks: source-derived matrix-sum keys followed by a distinct second decoding layer; direct use of the public key to solve larger additive scalar families; or an independently specified selector into the exact Architect text. These are pending hypotheses, not claimed solutions.
