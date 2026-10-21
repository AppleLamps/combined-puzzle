# Offline SalPhaseIon investigation — 4 September 2026

**New, reproducible lead:** the first unresolved 91-character block can be parsed into **64 tokens with exactly 16 distinct values**, using **b and g (2 and 7)** as two-character prefixes. This is compatible with a substituted hexadecimal SHA-256 digest. **The digest interpretation is not yet confirmed; no new AES plaintext was recovered.**

Only `All.md` and local computation were used. No website, search engine, API, or other network source was accessed. `All.md` was not edited; its SHA-256 is `cb95f9f0d2a19a7ed2d29ff9d59b0571d25793151841499618bd71648c082365`.

## The concrete step

Take the first unresolved block immediately before the binary `matrixsumlist` clue. Read left to right. When the next character is **b or g**, consume two characters; otherwise consume one. The resulting tokens are:

```text
d bb i bf bh c c be gb i h a be be i h
be gg e ge be bb ge h h e bh h f ba bf d
h be f f c d bb f c c c gb f be e gg
e c be d c i bf bf f gi gb e e e a be
```

There are 64 tokens and these 16 distinct codes:

```text
a ba bb be bf bh c d e f gb ge gg gi h i
```

Among all 36 pairs of distinct prefix letters from a–i, **b/g is the only pair that yields both 64 tokens and 16 distinct codes**. Parsing rejects a trailing prefix without a following character. Both prefix values, 2 and 7, are primes under the mapping used in the nearby decoded decimal clues.

This parsing rule is motivated by the straddling checkerboard cipher used in the earlier puzzle. It does **not** establish which alphabet or table the creator used. In particular, a basic sequential hexadecimal checkerboard does not explain the observed code placement.

As an exploratory check, 10,000 deterministic shuffles preserving the original letter counts produced the same 64/16 property for *some* prefix pair in 30 cases (0.3%); the fixed b/g pair qualified in 5 cases. This makes the structure worth investigating, but it is not a formal significance test: the statistic was selected after inspecting the data and many interpretations were explored.

Reproduce the parsing, uniqueness test, and shuffle comparison:

```sh
python3 prefix_structure_check.py
```

## A candidate check that does not require the substitution key

If the 64 tokens represent a SHA-256 hex digest under a one-to-one substitution, matching and differing token positions must match and differ in exactly the same positions of the digest.

Labeling tokens by their first occurrence gives this equality pattern:

```text
01234556728966286abc61c88b48de3086dd501d5557d6bab5605233df7bbb96
```

Reproduce the pattern:

```sh
python3 - <<'PY'
from hash_pattern_probe import TARGET
print(''.join('0123456789abcdef'[x] for x in TARGET))
PY
```

Test any proposed `matrixsumlist` serialization with:

```sh
python3 - <<'PY'
from hash_pattern_probe import test
test('put the exact candidate string here')
PY
```

A `MATCH` would recover the token-to-hex mapping and give a strong way to validate the proposed matrix operation. The checker currently assumes ordinary SHA-256 and the direct token order. Failure only excludes that exact candidate under those assumptions.

Common grid row/column sums, many prime-valued color assignments, prime-position masks, common list serializations, and local phrase candidates have been checked without a match. There is no justification yet for treating this as the decrypted hash or as an AES password.

## Cryptographic verification

The supplied known answer `causality` successfully decrypts the earlier Phase 2.1 blob with:

1. SHA-256 of the UTF-8 password, represented as lowercase hexadecimal.
2. OpenSSL's legacy `EVP_BytesToKey` derivation with **SHA-256**, one iteration, and the embedded eight-byte salt.
3. AES-256-CBC and PKCS#7 padding.

MD5 key derivation does not reproduce that known plaintext. This distinguishes hashing the password from the separate hash used inside OpenSSL key derivation; both matter.

```sh
python3 offline_crypto.py
```

The three unsolved ciphertexts were extracted and checked for valid Base64 and AES block sizes:

| Blob | Salt, hexadecimal | Ciphertext bytes | Plaintext length before padding |
|---|---|---:|---:|
| Embedded SalPhaseIon | `3ab585348552415d` | 80 | 64–79 bytes |
| Cosmic Duality | `2d3f6fe06dc950e6` | 1328 | 1312–1327 bytes |
| Earlier Phase 3.2 | `b45a5e3d827593ca` | 80 | 64–79 bytes |

The known key derivation is a sensible default for these remaining blobs, not proof that the creator never changed it. Candidate checks also tried MD5. Valid padding alone was never accepted as a solution; readable, meaningful plaintext is required.

## What was ruled out, and what remains open

- Direct whole-integer base-9/base-10 decoding under every injective digit substitution did not produce fully printable text for either unresolved block: 7,983,360 substitutions checked.
- Several explicit zero-replacement models were ruled out using interval constraints, including independently choosing zero or the original digit at occurrences. These results concern the stated whole-integer-to-text models; they do not rule out the creator's zeroing clue in other operations.
- Direct checkerboard parsing followed by ordinary monoalphabetic English substitution has not produced coherent text. The substitution solver was validated against a known encrypted English passage before relying on the negative results.
- Simple matrix sums and chunk arithmetic did not yield a verified decode. Detailed, scoped results are retained in the experiment directories.

The strongest next lead is to determine whether the 64/16 token structure really encodes a digest, and what operation `matrixsumlist` names. The long block and the exact role of `lastwordsbeforearchichoice` remain unresolved.
