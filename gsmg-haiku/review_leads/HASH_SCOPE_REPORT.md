# Hash placement, plaintext lengths, and selected answers

Follow-up to the three user-selected constraints. **No private key, structured decrypt, or confirmed intermediate password was recovered.** This work tested new hash scopes and selection rules, not the old flat password dictionary or solved-stage decryptions.

## Results

| New family | AES trials | Result |
|---|---:|---|
| Contiguous partitions of the seven original Phase 3 parts | 756 | Negative |
| All set partitions, group order canonical/reversed, separate group hashes | 62,316 | Negative |
| All ordered subsets of two through seven parts, hash each part first | 492,840 | Negative |
| Hash selected operands, leaving other operands literal | 4,752 | Negative |
| Two-marker command scopes and ENTER at hash boundaries | 15,960 | Negative |
| XOR selected original-part digests | 1,440 | Negative |
| Decrypt, then use/hash the bytes to open another container | 14,322 | Negative |
| Complete hash-command output bytes used as password material | 115,344 | Negative |
| **Total** | **707,730** | **No structured candidate** |

The two larger passes additionally checked **450,344 scalar candidates**, deduplicated within each pass, against the supplied target public point. None matched. Checks included raw/hex password digests, hashes of decrypted bytes, every 32-byte window of short plaintexts in both byte orders, and arithmetic combinations of two raw scalar shares. They did not perform an arbitrary HD derivation-path search.

Across all passes, 2,810 decryptions happened to have valid padding. That is close to the approximately 2,775 expected from 707,730 unrelated guesses at probability 1/255. Padding alone was never treated as a solution. Every padding-valid output was saved, including binary outputs.

All padding-valid **short-container** plaintexts had length 78 or 79:

```
78 bytes:    8 outputs
79 bytes: 1913 outputs
64–77:      0 outputs
```

None contained a 64-character hexadecimal scalar or reached the 85% printable screening threshold. The 78-byte outputs also failed the standard serialized extended-private-key prefix/type screen. The exact candidate generators are in the scripts below; these negatives apply to those generated passwords, not to every possible answer to the puzzle.

## 1. What was tested around the two SHA markers

Consuming `shabef` leaves `ourfirsthintisyourlastcommand`. The trailing `shabefanstoo` remains semantically ambiguous. I tested both of the useful interpretations:

1. SHA-256 applies separately to operands before building an AES password.
2. The second SHA-256 applies after decrypting one container, to obtain another password or a private scalar.

For the seven-part tests, the exact inputs were the accepted parts returned by `next_tests.py:parts()`. Case, `0x`, uppercase hex and FEN spaces were preserved.

Let `H(x)` be SHA-256 represented either as 32 raw bytes or 64 lowercase hex characters. The set-partition pass enumerated all 876 partitions into two or more groups, concatenated the original parts within each group in their original order, hashed each group, and concatenated or interleaved those digests. Groups were ordered by their first original index and also tried in reverse order. The resulting byte string C was passed to EVP as C, lowercase-hex SHA256(C), or raw SHA256(C). This extends the initial 63 contiguous partitions; the already-run 252 passwords were skipped.

The selected-parts pass enumerated all ordered subsets of size 2..7. Every chosen part was hashed before concatenation/interleaving, avoiding a repeat of flat concatenations of the original answers. The selective-hashing pass instead held the order fixed and hashed a nonempty proper subset of operands. It covered both the seven Phase 3 parts and the three Phase 3.2 parts.

The command-scope pass used these four explicit meanings of the first hint F:

```
GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
gsmg.io/theseedisplanted
theflowerblossomsthroughwhatseemstobeaconcretesurface
matrixsumlist
```

Answer A ranged over the seven original parts, the complete Phase 3.2 answer, the ownership plaintext, `thispassword`, three documented last-word candidates, and the poster row/column sum lists with three serializations. This operand list is a hypothesis, not a claim that the unresolved digit runs have been decoded.

Exact tested scopes included:

```
H(F) || H(A + ENTER)
H(A + ENTER) || H(F)
H(F || H(A) + ENTER)
H(H(F) || A + ENTER)
H(A || H(F) + ENTER)
H(H(A) || F + ENTER)
H(F) || H(A) || ENTER
H(A) || H(F) || ENTER
```

ENTER was empty, LF, or CRLF. The script explicitly records when another outer SHA is applied; it does not silently apply the normal password hash to every already-hashed expression.

The post-decrypt pass took **all 2,276 first-pass padding-valid records**, not just printable candidates. For each plaintext P, it tried P, SHA256(P) in raw/hex form, and the corresponding whitespace-trimmed variants as passwords to each other container. Hex decoding was included when the entire stripped plaintext matched a hexadecimal scalar. Thus an unreadable intermediate answer was not automatically rejected.

The command-output pass additionally placed ENTER before the first hash versus after its printed output. It tested lower/uppercase digest text with LF, CRLF, `  -\n`, ` *-\n`, ` *stdin\n`, `(stdin)= `, and `SHA256(stdin)= ` wrappers. These were explicit byte-layout hypotheses; no claim is made that the creator used a particular shell/version. The tested sources included the seven parts, whole accepted answers, poster text, two instruction tokens, the Architect and ownership texts, and the 252 contiguous-partition constructions.

## 2. What the 64–79-byte constraint actually tells us

For either short container, ciphertext length is 80 bytes. With ordinary PKCS#7 padding of 1..16 bytes, the plaintext is 64..79 bytes. **64 hexadecimal characters are a hypothesis, not known plaintext.**

Several concrete layouts fit:

| Plaintext | Length | Padding bytes |
|---|---:|---:|
| Bare 64-character hex scalar/digest | 64 | 16 |
| Hex plus LF | 65 | 15 |
| Hex plus CRLF, or `0x` plus hex | 66 | 14 |
| Digest plus `  -\n` | 68 | 12 |
| Two raw 32-byte quantities | 64 | 16 |
| Raw uncompressed SEC public key | 65 | 15 |
| Raw serialized BIP32 extended private key, before Base58Check | 78 | 2 |

A [BIP39 seed is 64 bytes](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki#from-mnemonic-to-seed). A BIP32 private scalar plus chain code occupies 64 bytes, and its standard serialized structure is 78 bytes before the checksum/Base58 encoding. These are **verified specification facts**, not evidence that the puzzle uses an HD wallet. [BIP32 specification](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#serialization-format).

The binary formats matter because a printability-only filter could discard a real intermediate secret. This pass checked the target directly for binary scalar candidates and tried binary plaintext as a downstream password. There were no 64-byte outputs to interpret as bare seeds or bare key/chain-code pairs, and no 78-byte output passed the standard extended-private-key prefix/type test. A bare WIF or bare raw 32-byte scalar remains incompatible with a single short-container layer under the given padding convention.

Synthetic controls covered a 64-byte hex key, a key with prefix/newline, two raw scalar shares, and a 65-byte SEC public key. All produced 96-byte salted containers and were recovered correctly. These controls were newly constructed; the solved puzzle containers were not decrypted again.

## 3. What “select from” permits—and what length excludes

The new searches treated the seven answers as selectable operands: subsets, reordered subsets, separate group hashes, interleaving and XOR. None succeeded. This excludes those specific constructions from known parts; it does not establish that the seven intended answers are already known.

Seven fully nested salted, padded AES envelopes require at least 224 decoded bytes, even with empty innermost plaintext. They cannot fit either 96-byte container. However, **the length argument does not exclude two layers**:

```
32-byte inner secret
→ 48-byte padded ciphertext + 16-byte Salted__ header = 64 bytes
→ 80-byte padded ciphertext + 16-byte Salted__ header = 96 bytes
```

Therefore a short container could hold a 64-byte inner salted container protecting a raw 32-byte key. By contrast, if the innermost secret is a 64-character hex key, its first salted encryption already uses all 96 bytes, so there is no room for another complete salted envelope. Repeated raw-block encryption without headers or intermediate padding is a different model; the envelope-length argument alone does not exclude it.

No first-pass candidate produced a 64-byte plaintext beginning `Salted__`; consequently no such nested candidate was available to pursue. The cross-container decrypt-then-hash pass is a separate two-stage interpretation and was tested exhaustively for the retained first-stage records.

## Practical conclusion

The useful surviving interpretation is **hash an actual answer, decrypt, then hash/use that result**, not an instruction to stack seven envelopes or necessarily hash the same answer twice. It is still an interpretation, not a recovered workflow. These runs substantially narrow hash-placement variations over the known operands. They provide no reason to prefer further permutations of those same operands over resolving what `matrixsumlist` and the unresolved runs actually supply.

## Reproduction and files

```
python C:\gsmg-puzzle-clean\review_leads\next_tests.py partitions
python C:\gsmg-puzzle-clean\review_leads\hash_scope.py
python C:\gsmg-puzzle-clean\review_leads\hash_scope_followup.py
```

Each refuses to overwrite its existing result JSON. Preserve/rename those output files before rerunning. Existing evidence:

- `next-partitions-results.json` and `next-partitions-padding.jsonl`
- `hash_scope/results.json` and `hash_scope/padding.jsonl`
- `hash_scope/followup-results.json` and `hash_scope/followup-padding.jsonl`
- `hash_scope/length-screen.json`

The hard confirmation condition throughout was a private scalar whose public point equals the supplied target point. No transaction was constructed or broadcast.
