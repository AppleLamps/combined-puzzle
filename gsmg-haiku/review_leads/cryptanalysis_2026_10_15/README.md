# GSMG cryptanalysis — reproducible investigation, 15 October 2026 UTC

No remaining container was opened. No new complete instruction or prize private key was recovered. This packet records new computations, exact limitations, and a concrete correction to the current framing. It is not a claim that the puzzle, Hill ciphers, or seed derivation have been exhausted.

**The principal correction.** The alternating four-letter stream is a coordinate projection forced by the nine-letter input alphabet. Its existence is not separate evidence of an encrypted message. Likewise, the apparently attractive 512-bit object contains eight bits belonging to the interleaved `BTCSEED` header. Once the header is removed, its genuinely subsequent row payload is 504 bits. Both objects are reversible extractions; neither verified cryptographically.

## Evidence and provenance

The two live SalPhaseIon textareas match the retained originals exactly after the documented whitespace normalization. The 1,075-character first field also matches the independently retrieved public walkthrough. The poster was visually inspected and its actual pixel colors measured. Repository copies were checked against Git blob hashes, not accepted because a note called them correct. Known phase-3.2 AES decryption recovered the exact 2,422 bytes; its 1,539-letter Architect text was independently recovered and re-encoded through the EBCDIC/Beaufort stages.

`provenance.json` records source URLs, repository heads, limitations, and SHA-256 hashes. `inputs/` holds the exact retained evidence. The live page's current agreement does not authenticate every historical revision. Creator excerpts are from a repository-held Telegram export; they were not independently authenticated with Telegram. Research notes were used to locate sources and inspect prior coverage, not as premises for the new computations.

The source explicitly supplies encoded fields, three remaining OpenSSL-format containers, the poster, and instructions. Exact decoded fields include `matrixsumlist`, `lastwordsbeforearchichoice`, `thispassword`, and `enter`. Literal strings remain `shabefourfirsthintisyourlastcommand` and `shabefanstoo`; I have not silently expanded the latter into another phrase. `field_boundaries.json` partitions all 1,075 characters, including all three `z` separators and both separated base64 halves.

The Architect text is an unspaced letter stream, with editorial word boundaries excluded from the source record. Its sequence contains `SOURCECODES`, `REINSERTINGTHEPRIMEBASICS`, and `OVERTWENTYTHREECIPHERSSIXTEENENCRYPTIONSANDORSEVENINTERTWINEDPASSWORDS`. The later binary hint independently decodes, by reversing the entire bit string, to:

```
yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyangwewontgiveawaythepassworditsinfrontofyoureyesbutyourenotseeingitverylaststepisatruegiveawaypromised
```

The encoder reproduces that exact bit string. This order constrains possible readings, but does not specify separators, operands, a cipher receiver, or a password concatenation. “Zeroed out” comes from a separate reported creator message; zeroing bytes is not equivalent to deleting them or replacing their numerical contribution with zero. “Choice” could locate a passage, a branch, or a selection operation; no tested reading independently fixed that operand. “Source codes” does not itself identify Bitcoin source code, HTML, the prior decoded strings, or a cipher alphabet. Those remain competing references.

## What the bytes establish, and what the constructions add

| Relationship | Reproduced fact | Extra assumptions / limitations |
|---|---|---|
| DBBI prime grammar | The 91 characters have exactly two parses under prime positions taking `b` or `be`: 83 and 84 cells. | This grammar is a model; the bytes do not label their cell boundaries. |
| 23/16/7 | The 84-cell parse has 23 prime cells, with 16 `b` and seven `be`. | Counts support that parse conditionally. The 83-cell alternative has 15/8 and cannot be discarded merely because it lacks the desired counts. |
| Poster correspondence | All 24 blue/yellow cells mark the last bit of a URL byte. A separate off-white cell occurs inside byte 21. Enumerating all 300 choices of 23 out of 25 events reproduces three 83-cell and two 84-cell matches when off-white is treated as blue. | A unique 84-cell match requires both no duplicate byte and selecting bytes 1–23. That last rule is not an established instruction. |
| Prime sums | Numbering the 24 ordinary color events by successive primes gives blue 484, yellow 479. | The ordinary colors also encode URL parity. Color counts, order and sums are not independent witnesses once the URL and marking rule are fixed. The off-white event requires a separate treatment. |
| HILLFEXMGSGQ | In the 84-cell parse, replace prime `b` by minus its position, `be` by plus its position, and ordinary letters by 1–9. A row-major 7×12 arrangement has column sums `[-45,34,37,37,-73,30,49,38,32,44,-124,42]`. Modulo 26, A=0, these spell `HILLFEXMGSGQ`. | Sign rule, shape, orientation and modulus are introduced choices. Summation and reduction lose information: this operation is not a reversible decoder of all DBBI bytes. |
| Bifid prefix | Deduplicating DBBI followed by the natural alphabet without J yields `dbifhcegaklmnopqrstuvwxyz`. Full-period Bifid decoding of the 570-letter FAED field starts `btcseed`. Re-encoding recovers all 570 letters. | The square construction and Bifid model are hypotheses. Eight of the 9! tested first-nine-letter arrangements give that header; only period 570 does so with the selected square. These are bounded uniqueness statements. |
| Hill prefix | Treat FEXM→GSGQ as a column-vector Hill example over the natural 25-letter alphabet. Its encryption matrix is `(1,19;6,3)`, inverse `(2,4;21,9)`. Applying the inverse to `bif[7::2]` yields `ifindonvfrvodtfmdryqw…`. | Reading the two groups as an example, using modulus 25 after a modulus-26 construction, splitting at seven, and choosing this alphabet are assumptions. `IFINDO` is not a complete instruction. All continuation bytes are retained. |

The combination of reproducible prefixes warrants continued investigation. It is not a proof of authorial intent. Fixed-recipe shuffle probabilities are recorded in `structural_tests.json`, but cannot be used as global significance levels: the recipe was historically selected after searches. The 23/16/7 counts, HILL string and chosen branch also share construction assumptions.

## The exact forward encoding and its information accounting

Let `S = dbifhcegaklmnopqrstuvwxyz`. Pair original FAED letters at positions `i` and `i+285`, for `i=0..284`. If their square coordinates are `(r1,c1)` and `(r2,c2)`, the Bifid output pair is exactly:

```
S[5*r1+r2], S[5*c1+c2]
```

Every source letter is in the first two rows. Consequently the first output in each pair must be one of `d,b,c,e`, corresponding to row bits `00,01,10,11`. This explains the four-letter alphabet without invoking another cipher. The second output encodes the two column values. Keeping both outputs is lossless; deleting the row stream generally loses information.

The source letter pairs by column are `(d,c), (b,e), (i,g), (f,a)`, with singleton `h`. Whenever a column equals four, the source row must be zero: the other cell would be `k`, absent from FAED. There are exactly 58 `h` occurrences. Removing these 58 determined zeros from 570 row bits leaves 512 bits, and the column stream tells the decoder exactly where to restore them. A random planted 512-bit object was encoded with these columns and recovered exactly, preserving the column stream.

Crucially, the full Bifid output starts `btcseed`; the column stream alone starts `tsedom…`, not `btcseed`. The first four row symbols are `bced`, encoding `01101100` (hex `6c`). These eight free row bits belong to the seven-character interleaved header. Removing the header's row symbols leaves 281 symbols, 562 row bits, of which 58 are forced: **504 payload bits / 63 bytes**. The header has a row symbol paired with the first carrier letter, so treating its odd length as an ordinary byte boundary is an indexing error.

This distinguishes a reversible factorization from a demonstrated seed format. In particular, 512 bits, the four-letter alphabet, and the row-bit representation are related consequences of the same coordinates; they must not be counted as three independent clues.

## Hypotheses executed and decisive results

| Hypothesis and predicted result | Test and controls | Result and exact scope |
|---|---|---|
| A single ordinary 2×2 Hill stage should decode the entire carrier to instructions. | Exhaust all 300,000 invertible matrices mod 25 on the stated streams. Recover a full forward-generated 282-letter control. Compare against 12 digraph shuffles preserving the six-letter prefix and block counts. | No coherent complete decode in retained leaders; shuffled continuations can score above the real one. This is a language-ranking negative, not a theorem excluding every possible plaintext. |
| Mod-26 Hill may be singular, with the companion supplying the lost information. | Solve all four matrices taking FEXM→GSGQ, then test whether each carrier digraph lies in each matrix's image. | Exact contradiction for the unchanged carrier: respectively 65, 72, 100 and 63 of 141 digraphs have no preimage. Additional side information cannot recover a nonexistent preimage. Changing the carrier would be a different hypothesis. |
| A 3×3 Hill cipher extends IFINDO to IFINDOUBT. | Constraint enumeration, independently checked by a mod-5 invariant. | In natural25 A=0, carrier triples DOM and SHK obey `C3=4*C1 mod 5`. Any linear map preserves this. IFI requires the third plaintext triple to be `(2,0,2) mod 5`; UBT is `(4,1,3)`. Impossible under this model, including singular keys. |
| An affine offset or a different finite field repairs that failure. | Enumerate all invertible affine keys consistent with IFINDO (2×2) or IFINDOUBT (3×3) for three alphabets; two complete forward controls. Also test ten GF(25) quadratic representations with example-derived / crib-derived keys. | Some models can force the prefix, but no coherent continuation emerged. The supplied crib receives no language-score credit. Singular crib systems in the GF(25) test were reported as unresolved, not excluded. |
| The companion applies a symbol-dependent Caesar correction. | Require the existing IFINDO prefix to remain unchanged. Its first six companion symbols contain all four companion symbols. | Every symbol's shift is forced to zero. This rejects only that stationary per-symbol correction, not arbitrary feedback or permutations. |
| The raw nine-letter field is a Hill-transformed base-9 rendering of plaintext bytes. | Three explicit input digit maps; 2×2 and 3×3 unit-determinant keys over Z/9 and all three GF(9) polynomial representations. For 3×3, all `9^9` matrices per model are considered with a conservative prefix filter. Four independent 226-byte planted controls recover exactly. | No complete ASCII-text byte object under the specified maps/blocks/arithmetic. ASCII includes printable bytes and tab/LF/CR. Binary, EBCDIC, compression, other digit maps, transposition and other block sizes are not excluded. Python exact arithmetic independently reproduced every retained C++ output and checked filter bounds. |
| FAED digits are gaps through the Architect text. | The digit sum is exactly 3079 = 2×1539+1. Test cyclic cumulative indexing at every start, both directions and source variants; compare against 40 histogram-preserving shuffles. | No coherent reading, and 15 controls beat the best real score. The total-sum identity survives every shuffle; it does not validate the ordering or the gap interpretation. |
| The row stream is directly encoded binary text or key material. | All 24 two-bit assignments, both bit directions, every 7/8-bit alignment; 1,440 models with leftover bits retained. Exact planted bit/AES control. | No complete text; 8,640 bounded OpenSSL password trials produced padding-only outputs, all retained. 82,704 distinct direct scalar candidates did not match the prize. No padding event was accepted as a solve. |
| The new free-row object is a Bitcoin seed or private-key/chain-code pair. | Four header-producing squares with 512 bits, two natural orders, polarity/reversal/bit-order variants: 32 distinct 64-byte objects, 96 HD roots, 295 explicit paths each. Repeat as 32 header-stripped 63-byte seeds. Official BIP32 root/hardened/nonhardened test vectors pass. | 28,480 full-object and 9,472 header-stripped public-point checks: zero prize matches. Raw/hex/SHA256-hex and stated half-material OpenSSL variants over three containers: 960 + 576 trials, ten padding-only outputs, no coherent plaintext. Arbitrary HD paths, passphrases, or other derivations are not excluded. |

The seed checks compare the exact secp256k1 public point, whose hash independently matches `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`. They do not depend on address balances, padding, or an English-word detector. All key tests are local; nothing was broadcast.

The alternative hypotheses were selected to distinguish mechanisms, not to turn each suggestive phrase into another password. Later tests were driven by specific failures: a singular-image test follows failed invertibility; the mod-5 invariant follows the tempting IFINDOUBT extension; affine tests check the exact missing constant term; header-stripped seed tests correct the discovered boundary error.

## Strongest surviving explanation and the missing operation

The most useful surviving model is an intentionally staged coordinate construction: DBBI supplies a candidate square and Hill-related hint; the FAED field interleaves row and column information and exposes a header. That is an inference, not a recovered next instruction. The full ordinary Hill interpretation has not earned acceptance; the companion cannot simply be discarded or hailed as an independently meaningful ciphertext.

**The precise unsolved interface is the transformation of the 282-letter post-header column carrier together with the 281 remaining row symbols into a complete instruction or cryptographically verifiable object.** We do not know whether it requires a new key, a permutation, a feedback rule, a different representation, or rejecting part of the inferred route. No original instruction yet fixes that transformation and its operands. The ultimate remaining AES cipher/KDF/password assembly is also not established merely by `Salted__`.

A strong continuation must predict material beyond the already-known prefixes, account for the companion and the odd header boundary, supply a forward encoder that recovers the source, and then either produce a coherent whole instruction or pass an exact container/key check. An arbitrary rule can be fitted to these bytes; that is not evidence of the intended mechanism. The unresolved labels are constraints on such a rule, not verified passwords.

## Reproducing and inspecting this packet

Python dependencies used: pycryptodome, Pillow, numpy, coincurve; C++17 for the accelerated scans. `quadgrams.bin` is the bundled heuristic scoring table. Its rankings are fallible and are not used to establish the algebraic exclusions or exact key comparisons.

From the repository root, enter this research folder:

```
cd review_leads/cryptanalysis_2026_10_15
python reconstruct.py
python audit.py
python free_rows.py
python row_payload.py
python affine_hill.py
```

`audit.py` checks stored scan receipts with Python integer arithmetic; it does not repeat the expensive exhaustive scans. To repeat those, compile the included C++ files and use the prepared model files:

```
g++ -O3 -std=c++17 hill_scan.cpp -o /tmp/gsmg_hill
/tmp/gsmg_hill .

g++ -O3 -std=c++17 radix_scan.cpp -o /tmp/gsmg_radix
/tmp/gsmg_radix . ring
/tmp/gsmg_radix . 01
/tmp/gsmg_radix . 12
/tmp/gsmg_radix . 22
```

The corresponding Python scripts specify all tested maps, paths, indices and candidate membership. `row_payload.py` imports and reruns the full-object control/test script first. The JSON files preserve complete selected outputs, binary bytes, padding-only plaintexts, and leftovers; exhaustive-scan files retain leaders/qualifying outputs, with the full enumeration reproducible from code. Older superseded radix logs and compiled binaries are excluded from the deliverable. No claims of historical search exhaustion depend on missing prior search manifests.

Repository integration: original source-artifact copies in this folder are preserved byte for byte. `manifest.json` uses paths relative to this folder. `provenance.json` corrects the local checkout label `gsmg-haiku-review` to its actual source repository, `AppleLamps/gsmg-haiku`. The repository snapshot adds links and status updates; it does not replace earlier experiment histories.
