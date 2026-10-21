# New-lead review — 2026-10-08

No private key or remaining-container plaintext was recovered. The supplied solved stages and negative sweeps were treated as inputs, not rerun. The tests below either change the operation being tested or address a channel absent from that list.

At the initial review, the first three hypotheses were prepared but NOT RUN. Their helper functions passed synthetic round-trip checks. The remaining experiments were run; results and narrowly defined exclusions are below. The local experiments below make no network calls and no transactions. Later chain work is read-only: it queries public explorers and sends nothing. See [BSV_FUNDING_TRACE.md](BSV_FUNDING_TRACE.md) (historical BSV claims and recovered local script evidence; no fresh query during correction) and [LTC_SCAN_2026-10-08.md](LTC_SCAN_2026-10-08.md) (partial LTC/BTC brainwallet scan, 257 of 2,176 addresses, read-only mempool.space and litecoinspace.org queries, no match). **Follow-up:** the partitions hypothesis and broader hash-placement/selection tests have now been run; see [HASH_SCOPE_REPORT.md](HASH_SCOPE_REPORT.md). Transposition has also run with no confirmed result; see [TRANSPOSE_REPORT.md](TRANSPOSE_REPORT.md). The digit-map hypothesis has now run without the printable filter, alongside alternative ten-column boards; see [MAPPING_BOARDS_REPORT.md](MAPPING_BOARDS_REPORT.md). No confirmed result was recovered.

## Ranked next tests

> Corrected 2026-10-14: all three tests below have since run; they are kept as originally specified. Test 1 ran as specified: 414 AES trials after deduplication, no hit ([TRANSPOSE_REPORT.md](TRANSPOSE_REPORT.md)). Test 2 ran as the contiguous-partition family of [HASH_SCOPE_REPORT.md](HASH_SCOPE_REPORT.md): 756 trials, no hit. Test 3's printable-filtered variant never ran; it was superseded by the unfiltered digit-map run (256,320 trials) in [MAPPING_BOARDS_REPORT.md](MAPPING_BOARDS_REPORT.md), no hit.

### 1. Undo a digit transposition before checkerboard parsing

**Plausibility:** moderate relative to the other remaining leads; strongest text-specific next test. It does not require a historical fact.

**Hypothesis:** the unsuccessful substitution solve used the wrong stage order. A transposition of the digit stream changes where variable-length checkerboard symbols begin. Substitution-solving symbols parsed before that transposition cannot recover the intended text. This is a materially different experiment from transposing the already-decoded 91-letter ownership message or freely solving the original b/e parse.

**Exact inputs:** `S[:91]` and `S[195:765]`, where `S` is the whitespace-free first SalPhaseIon textarea. Each is tested forwards and backwards. Column keys, exactly lowercase:

```
matrixsumlist
thematrixhasyou
lastwordsbeforearchichoice
fubcdoraclethingkymvps
```

Sort column indices by `(key_character, original_index)`; this specifies repeated-letter handling. Try the columnar encryption and inverse permutations, with ragged columns and no invented padding. Only then map a..i to 1..9 and parse with the already-established decimal checkerboard:

```
0 F, 2 U, 3 B, 5 C, 6 D, 7 O, 8 R, 9 A
10..19: .LETHINGKY
40..49: MVPS/JQZXW
```

Also test the transformed digit string itself and its decimal-integer-to-big-endian-bytes conversion. For the even-length stream, include two-decimal-digit bytes. All are passed through the established SHA-256-hex password and SHA-256 EVP derivation, not a new KDF.

**Cost:** 32 transposition cases; at most 480 AES trials before deduplication.

**Confirmation:** sustained grammatical text with the fixed board is a lead; an intelligible decrypt is stronger; a resulting private scalar must reproduce the target hash160. A padding match alone is not confirmation.

```
python C:\gsmg-puzzle-clean\review_leads\next_tests.py transpose
```

### 2. Hash contiguous groups of the seven original answers before the final hash

**Plausibility:** moderate-low, but unusually cheap. The explicit seven-password language and the two `shabef` markers motivate testing hash placement, not more synonyms.

**Hypothesis:** some individual answers or groups were hashed before being intertwined. The old four-stage-answer XOR/sum/product experiments do not cover every contiguous partition of the seven parts within Phase 3.

**Exact input:** the seven accepted Phase 3 parts in `next_tests.py:parts`, preserving `Safenet`, `Luna`, `HSM`, the uppercase hex digits and lowercase `0x`, and all FEN spaces. These are the same seven parts documented in STEPS.md, not alternate historical answers.

There are six boundaries between seven parts. For each nonzero six-bit cut mask, concatenate within each group, SHA-256 each group, and concatenate the group digests. Test digests as raw bytes and lowercase hex. Also test interleaving the equal-length digests one byte/hex-character at a time. Finally SHA-256 that result into lowercase hex for EVP.

For example, the all-cuts candidate is:

```
C = hex(SHA256(part1)) || ... || hex(SHA256(part7))
password = hex(SHA256(C))
```

The no-cut mask is deliberately omitted because it just repeats a whole-answer double hash already covered.

**Cost:** 63 partitions × 2 digest representations × 2 joins × 3 containers = at most 756 AES trials.

**Confirmation:** a structured decrypt, followed by key/address validation where applicable. No inference from padding alone.

```
python C:\gsmg-puzzle-clean\review_leads\next_tests.py partitions
```

### 3. A different digit alphabet local to the two unresolved runs

**Plausibility:** low. It explicitly assumes the unresolved runs need not share the complete digit alphabet of the already-decoded z-delimited runs.

**Hypothesis:** `shabef` establishes b=2, e=5, f=6, but the remaining letters in the unresolved runs encode another injective digit assignment. This differs from selectively replacing occurrences of g/i/e with zero: it also permutes the other nonzero digits consistently.

**Exact transform:** hold b=2, e=5, f=6. Assign `a,c,d,g,h,i` injectively to six of `0,1,3,4,7,8,9`. For each mapping, interpret each run and its reverse as a decimal integer, then minimal big-endian bytes. Leading decimal zeros have ordinary integer semantics. No zeros are inserted or deleted.

**Cost:** 7P6 = 5,040 mappings × 4 streams = 20,160 complete decodings. Only wholly printable outputs are sent to AES, at most 60,480 AES trials. This model searches text, not arbitrary binary payloads.

**Confirmation:** a coherent full decoding under one fixed assignment, ideally fitting both runs; then a decrypt or target-address match. If no full printable strings exist, that excludes this specific local-alphabet model.

```
python C:\gsmg-puzzle-clean\review_leads\next_tests.py digit-map
```

## New experiments actually run

### 4. Known puzzle seeds plus a vanity-search scalar offset

**Plausibility:** low-moderate before testing. The visible `1GSMG` prefix motivates a vanity-generation mechanism, but there is no evidence that the creator initialized one with a known puzzle answer. That initialization is an assumption, not a fact about the creator.

**Exact hypothesis:** `d_target = ±seed + delta (mod n)`. The ten seeds were SHA-256 of the four accepted stage answers, the 149-digit checkerboard string, the uppercase ownership plaintext, the exact poster title/address preimage, and the target address; plus raw poster URL bytes as an integer and its complete bit reversal.

**Specific difference:** previous tests compared the seeds and algebraic combinations directly. This tests a scalar neighborhood around each seed, using the published target public point, not hashes of `answer || counter`.

For each seed/sign solve the bounded discrete log of `Q_target - (±seed - 2^31)G` in `[0,2^32)`, using baby-step/giant-step. This covers offsets `[-2^31, 2^31-1]`.

**Actual cost/result:** 1,376,276 point additions, 8.70 seconds, zero matches across 20 intervals. Synthetic positive controls covered both interval boundaries, negative offsets and the identity point. Results: `vanity-offset-32.json`.

The mathematical reason for covering more than ten million candidate scalar values is that this is a square-root algorithm: the actual computational work is under 1.4 million additions, not exhaustive testing of those values.

**Confirmation:** the recovered scalar's uncompressed public key hashes to exactly `a9553269572a317e39f0f518cb87c1a0ee1dbae4`; the script checks that.

```
python C:\gsmg-puzzle-clean\review_leads\vanity_offset.py --bits 32
```

An optional, **unrun** expansion is `--bits 36`: offsets `[-2^35,2^35-1]`, approximately 5.51 million point additions over the same 20 intervals. This is lower priority than the first three tests; the existing negative is not evidence that a larger interval is promising.

Background only: [vanitygen's own documentation](https://github.com/samr7/vanitygen) confirms exact-prefix generation is a real tool capability. It does not establish how this puzzle's key was generated.

### 5. Primes as matrix values, rather than selection masks

**Plausibility:** moderate before testing; tested variants now deprioritized.

**Exact transform:** assign values to the 14×14 poster in row, column, or the established spiral order, each forwards/backwards. At position i use (a) the ith prime, (b) i if prime and zero otherwise, or (c) the prime rank of i if prime and zero otherwise. Retain colours Y, B, Y∪B, K∪B, W∪Y∪F, the complement of Y∪B, or all cells. Sum rows and columns. Serialize row sums, column sums, both orders of their concatenation, interleaving, elementwise sum and elementwise difference; each forward/backward, with empty, comma or space separators.

**Specific difference:** prime values are summed. The logged prime-position/value masks and unweighted sum lists do not do this.

**Actual cost/result:** 4,308 unique candidate answers; 12,924 AES trials; no structured candidate. Also no exact match to either unresolved digit run, including reversed and zero-deleted serializations. Highest printable fraction among padding-valid decryptions was 0.532. Padding-valid binary outputs are retained for inspection, not called solutions.

### 6. Treat the short numeric run as a keystream seed

**Plausibility:** moderate-low before testing; the narrow variants run here are negative.

**Exact transform:** map a..i to 1..9. Use R1, reversed R1, the poster's binary row sums and column sums, or the decimal-digit expansions of those sum lists as key seeds. For each rotation of the seed, generate 570 key values either by repetition or by `K[t+L]=(K[t]+K[t+1]) mod m`, with m=9 or 10. Combine with R2 and reversed R2 as `(C-K) mod m`, `(K-C) mod m`, or `(C+K) mod m`. Test the resulting decimal digits, whole-number big-endian bytes and paired decimal bytes as answers.

**Specific difference:** this is an arithmetic relationship between the two runs, including non-carrying chain addition, not a mask or substitution solve of either run in isolation.

**Actual cost/result:** 17,352 unique answers; 52,056 AES trials; no structured candidate. Highest printable fraction among padding-valid decryptions was 0.570. This does not exclude a further transposition or other subsequent decoding layer.

Tests 5–6 and their exact labels/results are in:

```
python C:\gsmg-puzzle-clean\review_leads\run_new_leads.py
```

The script refuses to overwrite its existing `results.json`. Preserve/rename that output before rerunning. The existing JSONL files retain every padding-valid output, including binary ones. Such outputs were not subjected to exhaustive arbitrary binary-format interpretation.

### 7. QR redundancy as a second payload — closed for module-level alterations

**Hypothesis:** altered QR padding/error-correction bits could preserve the known decoded URL while encoding another message. This is a new residual-channel test, not another URL decode.

**Exact input:** sample the QR's 33×33 modules from the poster at `(x,y)=(1+7c+3,1290+7r+3)`. Generate the known URL as a version-4 QR for all eight masks, with and without UTF-8 ECI 26. The URL fits only error-correction level L at that version.

**Cost/result:** 16 fitting candidate matrices, 1,089 module comparisons each. Version 4, level L, mask 2, UTF-8 ECI 26 matches **all 1,089 modules**. Thus there is no residual module difference carrying altered padding/ECC data. This does not make a claim about sub-module pixel steganography or symbolic interpretations of standard QR metadata.

Code: `qr_residual.py`; result: `qr-results.json`. The normal ECI marker matters: without it, a standard QR differs and would misleadingly look anomalous. The implementation is [Nayuki's documented QR generator](https://www.nayuki.io/page/qr-code-generator-library), installed locally in `review_leads/vendor`.

## Text constraints that should steer further work

- **The two short containers admit plaintext lengths 64–79 bytes**, assuming the stated AES-CBC/PKCS#7 format: 80 ciphertext bytes minus padding of 1–16. A bare 64-character hex private key fits. A bare 32-byte scalar or 51/52-character WIF does not. Metadata or two 32-byte quantities are alternatives. This is a deduction from the supplied sizes, not a decrypt.
- **"Select from" is not "apply all."** The Architect's 23/16/7 wording does not require 23 serial ciphers. Seven normally padded nested OpenSSL `Salted__` envelopes would require at least 224 bytes even with empty innermost plaintext, so they cannot fit a 96-byte short container. Cosmic's length does not exclude nesting.
- **Consume `shabef` before reading the next word.** In `shabefourfirsthintisyourlastcommand`, consuming the full `sha256` marker leaves `ourfirsthintisyourlastcommand`. Reading "four first" reuses the f. The final `shabefanstoo` is compatible with another hash operation on an answer, but that interpretation remains a hypothesis. This motivates test 2's operation boundaries.
- **H's sign remains an explanatory loose end.** The Phase 2 text explicitly multiplies H by −1, while the accepted coordinate derivation in STEPS.md uses +42. The accepted Phase 3 answer is not being questioned or retried. A future coordinate-based extraction should state exactly how it handles this sign instead of silently dropping it.
- **The historical riddle has a stronger Overlord link than the notes record.** Roosevelt's signed message appointing Eisenhower to command Overlord is a [verified primary document](https://history.state.gov/historicaldocuments/frus1943CairoTehran/d503). Interpreting "floating zerg house" as the StarCraft Overlord is recalled game knowledge, not verified here. This improves one clue's explanation without replacing the already-solved 11110 answer; it does not establish all the other political allusions or their causal claims.
- **Do not elevate every misspelling into ciphertext.** The local `2021-03-01-spelling-hint.png` visibly has the attributed creator call "fourty" old spelling and "one of the many many typos." That is verified image content, not independent authentication of the screenshot. A typo channel would need a rule that predicts unused text, not corrections chosen until letters look meaningful.
- **The 1357 clue has a concrete historical alternative.** The local screenshot is filed as `2024-04-10.png`; the image itself has no visible full date. `840000−1357=838643`. A fresh mempool.space API lookup returned block 838643 at **2024-04-10 18:08:53 UTC**, hash `0000000000000000000131d0bc22c71142022320b04f6d5291dc19f620d16b11`. [Block record](https://mempool.space/block/0000000000000000000131d0bc22c71142022320b04f6d5291dc19f620d16b11). Bitcoin's 210,000-block subsidy interval is [documented](https://developer.bitcoin.org/reference/block_chain.html?highlight=bits). This makes a countdown to block 840000 a well-supported inference, not proof of the message date. Do not anchor 1357 to the 2026 chain tip without contrary evidence.

All creator screenshots here are local copies. Their visible text was inspected; their attribution and integrity were not independently authenticated. No private facts about the creator were inferred.
