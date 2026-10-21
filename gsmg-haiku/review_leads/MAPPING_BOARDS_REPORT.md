# Different digit mappings and checkerboards

**No remaining container opened and no target private key matched.** Two bounded searches were completed. No solved-stage decryptions or free substitution solves were rerun.

## 1. Consistent alternative digit mapping

Hypothesis: preserve b=2, e=5, f=6, as suggested by `shabef`, but allow the six remaining letters a,c,d,g,h,i to map injectively to six of `0,1,3,4,7,8,9`. Applying these constraints to the unresolved runs is an assumption, not established by the decoded marker elsewhere.

Exactly 7P6 = 5,040 mappings were applied to both the 91- and 570-character runs, each forwards/backwards. For each mapped decimal string, generate:

- The digit string itself as ASCII.
- Its decimal integer serialized to minimal big-endian bytes, keeping one zero byte for zero.
- Two-decimal-digit bytes for the even-length 570-digit stream.
- Complete outputs from the established checkerboard, in uppercase and lowercase.

All candidates were hashed with SHA-256 into lowercase hexadecimal password bytes, then tried against all three containers with the supplied SHA-256 EVP derivation. **There was no printability filter before AES**, unlike the earlier prepared `digit_map()` test. Binary candidates were retained and tested.

Actual counts:

| Measurement | Count |
|---|---:|
| Mappings | 5,040 |
| Stream decodings | 20,160 |
| Complete fixed-board parses | 17,520 |
| Distinct candidate answers | 85,440 |
| AES trials | 256,320 |
| Scalar/public-point comparisons | 157,346 |
| Recognized payloads or target matches | 0 |

## 2. Ten-column boards with different prefix digits and alphabets

Specific difference from logged work: previous experiments included selected nine-column boards and a free substitution solve of the b/e parse. This test uses **ten columns and 28 cells**, explicitly enumerating numeric row-prefix and column-order changes rather than solving a free substitution.

The a–i → 1–9 digit mapping is retained in this family. Both runs and their reversals are tested. Enumerate:

- All 90 ordered pairs of distinct row-prefix digits from 0–9. Pair order sets the order of the two long rows.
- All ten cyclic rotations of `0123456789`, each forwards and backwards: 20 column orders.
- 22 full 28-symbol alphabets: the established fill `FUBCDORA.LETHINGKYMVPS/JQZXW`; plus first-occurrence deduplication of each seed below followed by `ABCDEFGHIJKLMNOPQRSTUVWXYZ./`; plus the reversal of every resulting alphabet.

```
<empty seed>
FUBCDORACLETHINGKYMVPS
MATRIXSUMLIST
THEMATRIXHASYOU
LASTWORDSBEFOREARCHICHOICE
OURFIRSTHINTISYOURLASTCOMMAND
YINYANG
THISPASSWORD
ESTONIAR
ATONESIR
```

The last two seeds are speculative frequent-letter arrangements, not claims about a cipher named in the puzzle. The top row uses the eight non-prefix columns in the current column order. The remaining twenty symbols fill the two prefixed rows in that same column order. An incomplete final prefix rejects the parse; no padding digits or null deletions are invented.

Test complete decoded outputs uppercase/lowercase. Where both runs parse under the same board and direction, also test their concatenation in both run orders, uppercase/lowercase. The shared-board requirement prevents arbitrary mixing of independently selected boards.

Actual counts:

| Measurement | Count |
|---|---:|
| Boards: 90 × 20 × 22 | 39,600 |
| Stream decodings | 158,400 |
| Complete parses | 129,360 |
| Generated answers, including joins and case | 466,400 |
| Distinct answers within this family | 461,978 |
| AES trials | 1,385,934 |
| Scalar/public-point comparisons | 883,037 |
| Recognized payloads or target matches | 0 |

## Acceptance and language inspection

Both families used the established AES password protocol. SHA256(answer) was also tested directly as a private scalar. Every padding-valid decrypted output was retained and checked for recognized binary structures and the existing scalar/share interpretations. Arbitrary raw candidate answers of at most 32 bytes were checked in both byte orders. Comparisons used the supplied target public point.

Across both families there were **1,642,254 AES trials** and **1,040,383 public-point comparisons**, summed across runs; the latter count is deduplicated within each family, not globally across prior work. Padding was valid 963 and 5,541 times respectively; it was not considered a solution. Short-container padding-valid lengths were exclusively 78 or 79 bytes, with no outputs of length 64–77.

A separate inspection ranked all 17,520 fixed-board mapping outputs and 129,360 alternative-board outputs using the existing local interpolated English character-four-gram model. It did not run another substitution solver or AES pass. The top candidates still have no sustained grammatical message. For example, one high-ranked short-board output begins:

```
NTTRTCIOOTESTRIATETERITESSESETETTSEIIETIICATFITEHO...
```

The fragment `TEST` is not evidence of success. Language scores only rank hypotheses; they do not identify a plaintext or establish a different natural language. Full top candidates and derivation labels are retained in `mapping_boards/language-ranking.json`.

## Scope and reproduction

These are two separate models: changed mapping with the established board, and changed board with the original mapping. They do not exhaust arbitrary mappings, arbitrary alphabets, all ten-column permutations, or combinations with transposition. In particular, neither family changes the mapping and board and transposition simultaneously. No inference that those broader constructions are impossible follows from these negatives.

Commands executed:

```powershell
python review_leads/mapping_boards.py digit-map
python review_leads/mapping_boards.py boards
python review_leads/rank_mapping_text.py
```

The scripts refuse to overwrite existing result JSON files. Per-family results and padding logs are in `review_leads/mapping_boards/digit-map/` and `review_leads/mapping_boards/boards/`. The candidate generators are deterministic and record precise source labels for every padding-valid candidate. A synthetic alternate-board encode/decode control passed before each search. All facts and counts here come from the supplied puzzle artifacts and completed local computations; no historical assertion is needed.
