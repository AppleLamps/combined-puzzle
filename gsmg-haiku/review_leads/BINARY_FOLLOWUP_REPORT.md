# Binary payload and nested-container follow-up

No key, confirmed binary payload, or inner container was recovered. The tests below do not use readability as an acceptance requirement. All counts are from completed runs, not estimates. Existing solved stages were not decrypted again.

## The size constraint, stated precisely

Accept the supplied 96-byte decoded length, 16-byte `Salted__` header, AES block size 16, and ordinary PKCS#7 padding. The ciphertext occupies 80 bytes. Its plaintext can therefore be **any bytes** of length 64–79. Text is not implied.

For a plaintext of length n, a complete raw salted envelope has length:

```
E(n) = 16 + 16 * (floor(n/16) + 1)
```

This gives these exact possibilities for a 96-byte outer envelope, with no extra metadata:

| Construction | Innermost plaintext length | Implication |
|---|---:|---|
| One envelope | 64–79 | Could be binary seed, paired values, serialized wallet data, or text |
| Two raw envelopes | 32–47 | A raw 32-byte private scalar fits exactly |
| Three raw envelopes | 0–15 | A short command or passphrase fits; a bare 32-byte scalar does not |
| Two envelopes, inner envelope base64 encoded | 16–31 | A short seed or command fits; a bare 32-byte scalar does not |

For example: a 32-byte scalar produces a 64-byte inner envelope, which produces a 96-byte outer envelope. A 0–15-byte message produces lengths 32, 64, 96 under three raw envelopes. Seven raw envelopes require at least 224 bytes, even for an empty message. These are arithmetic deductions, not historical or recalled facts.

For **bare raw nesting**, the outer plaintext must be 64 bytes and start with `Salted__`. Its last decrypted block must consequently be sixteen `0x10` bytes. This gives a strong test even when every earlier plaintext byte is arbitrary binary. A fully padded 64-byte seed has the same last-block requirement without the header requirement. None of the tested passwords produced that padding pattern.

## Ranked hypotheses and completed tests

### 1. The previous text filter discarded a valid binary payload or inner envelope

**Plausibility:** highest of these follow-ups. It addresses a specific acceptance-filter gap; it does not assert that any old rejection was actually a solution.

**Inputs and difference from earlier work:** reuse the exact 40,114-string source pool and its nine existing password transformations from `mywork/pool_search.py`, but replace the text gate with binary structure checks. The historical run loaded the generator through its AST. The corrected code now imports `mywork.candidate_pool` explicitly, without running a decrypt loop or solved controls. Offline comparison confirms its 40,114-string pool equals the historical constructor on CRLF inputs; LF inputs to the old constructor instead produce 40,159 strings. This does not invalidate the recorded Windows run; see REVIEW_CORRECTIONS.md. There are 361,002 distinct transformed password byte strings. The KDF remains the supplied SHA-256 EVP construction.

For both short containers, inspect all 80 decrypted bytes and these interpretations:

- Ordinary PKCS#7 unpadding, accepting every 64-byte output regardless of contents.
- No outer padding, searching the full 80 bytes for recognizable structures.
- A 64-byte payload followed by sixteen zero bytes, or a 78-byte payload followed by two zero bytes.
- Raw/base64 `Salted__` envelopes; raw 78-byte mainnet/testnet BIP32 serialization; compact 77-byte SEC1-style private/public data with the curve fixed externally; SEC public keys; hexadecimal scalars; checksum-validated gzip/zlib streams.

The compact SEC1-style test is a proposed custom encoding, not a claim that a 77-byte object is a universally compliant standalone EC private-key file. A recognizable public key or nested header would be an intermediate lead, not proof of the target private key.

**Cost actually run:** 722,004 AES-CBC decryptions.

**Result:** no structural candidates. There were 2,883 valid padding results: 2,869 of length 79 and 14 of length 78. There were zero outputs of length 64–77. All padding-valid bytes were retained in the log. Valid padding alone is expected occasionally for wrong passwords and was not counted as success.

**Confirmation criterion:** a structurally valid inner envelope, validated binary wallet object, or candidate seed/scalar whose derived public key equals the supplied target point. An arbitrary 64-byte result would trigger further seed/share/chain-code tests rather than being called solved.

Script: `binary_envelopes.py`; results: `binary_envelopes/results.json`; complete padding records: `binary_envelopes/padding.jsonl`.

### 2. The two hashes form binary HD-wallet material

**Plausibility:** moderate. The two hash markers make two 32-byte pieces worth testing. Interpreting those pieces as a seed or key/chain-code pair is a hypothesis; the puzzle has not explicitly identified BIP32.

**Exact input construction:** take 64-byte non-hex binary outputs from `group_hashes()`, `selected_hashes()`, and `scoped_commands()` in `hash_scope.py`. These preserve the already accepted seven answer parts, including case, spaces and `0x`. Previously these bytes were passwords. Here they are wallet material. Also include the exact solved-answer/poster/derived strings listed in `binary_hd.py:materials()`, using raw bytes when 16–64 bytes long, SHA-256 bytes, and SHA-512 bytes. Include the a–i digit runs interpreted as decimal integers after a–i → 1–9, both digit directions and byte orders, as specified in that generator.

For each material B:

```
I = HMAC-SHA512(key=b"Bitcoin seed", message=B)
root_private = int_big_endian(I[:32])
root_chain_code = I[32:]
```

For each 64-byte B, also test direct `(private, chain_code) = (B[:32], B[32:])` and the reversed pair. Reject invalid scalars. Deduplicate materials and roots.

Derive the exact 295 paths recorded in `binary_hd/results.json`. The bounded path set includes m, m/i, m/0/i, m/0'/i, m/0'/0/i, m/0'/1/i, m/44'/0'/0'/0/i, and m/44'/0'/0'/1/i for i=0..31, plus their listed parent paths; m/i' for i=0..31; all hardened/unhardened combinations of the clue-index sequences (23,16,7), (14,14), (1,1,4,1); and single indices 11110, 227, 149, 1539, hardened and unhardened. These clue indices are speculative. No meaning for them is asserted by the test.

**Cost actually run:** 834 distinct materials, 1,828 distinct roots, 572,164 child derivations, and 539,260 public-point comparisons.

**Result:** no target match; no invalid child derivations. The implementation passed the official BIP32 test-vector-1 root, hardened-child and subsequent non-hardened-child controls.

**Confirmation criterion:** exact equality with the supplied target public point. This does not exclude other materials or arbitrary derivation paths.

The 32-byte private value plus 32-byte chain code, the 78-byte extended-key serialization, master HMAC, and child derivation are **verified from the primary BIP32 specification**, not recalled facts: [BIP32 specification and test vectors](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki).

Script: `binary_hd.py`; exact materials: `binary_hd/materials.json`; results and paths: `binary_hd/results.json`.

### 3. Two CBC passes use one header and padding only before the inner pass

**Plausibility:** lower. This requires a departure from two independently padded, independently wrapped envelopes. It is still a concrete two-layer construction that the 96-byte size does not exclude.

**Construction tested:**

```
inner_ct = AES_CBC(inner_key, inner_iv, PKCS7(payload))
outer_ct = AES_CBC(outer_key, outer_iv, inner_ct)  # no extra padding
stored = b"Salted__" + outer_salt + outer_ct
```

The inner `Salted__` header is absent. The inner EVP salt is independently selected from the actual outer salt, the other short container's salt, or empty bytes. Both KDFs use the supplied SHA-256 EVP algorithm.

**Exact password pool:** the seven accepted Phase 3 parts; the 252 bodies from `next_tests.py:partitions()`; and these fourteen bodies:

```
causality
theflowerblossomsthroughwhatseemstobeaconcretesurface
jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple
<exact concatenation of the seven accepted Phase 3 parts>
GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
gsmg.io/theseedisplanted
matrixsumlist
lastwordsbeforearchichoice
thispassword
ourfirsthintisyourlastcommand
enter
yinyang
oneforonefourforone
theproblemischoice
```

For every body C, use C, SHA256(C) raw, and lowercase-hex SHA256(C) as EVP password bytes. This yields 816 distinct passwords, each allowed at either layer. The exact bytes are saved in `double_cbc/passwords.json` and the exact generation code is in `double_cbc.py:passwords()`.

**Cost actually run:** 2 × 816 × 816 × 3 = **3,995,136 pair trials**, using a final-block padding check; 1,632 full outer decryptions; 15,538 full inner decryptions after valid padding. Also 78,434 target-point comparisons, testing SHA256(payload), SHA256(stripped payload), and first/last 32-byte scalars in both byte orders, deduplicated within each payload.

**Result:** no structural candidate and no target match. Padding-valid lengths were 79 bytes (15,466 cases) and 78 bytes (72 cases), with none of length 64–77. Synthetic controls confirmed recovery for all three inner-salt cases.

**Confirmation criterion:** a coherent binary payload or exact target public point, followed by reproduction from the recorded password pair. Padding alone is insufficient.

Script: `double_cbc.py`; results: `double_cbc/results.json`; all padding-valid pairs: `double_cbc/padding.jsonl`.

## Reproduction and limits

Commands used, from `C:\gsmg-puzzle-clean`:

```powershell
python review_leads/binary_envelopes.py
python review_leads/binary_hd.py
python review_leads/double_cbc.py
```

Dependencies are pycryptodome and coincurve, already available in this environment. Each script deliberately refuses to overwrite an existing `results.json`; choose a new OUT directory in the script for a fresh run. The existing JSON results can be inspected without running anything again.

The supplied target public point and solved puzzle inputs were accepted as background; no chain data or historical claims were re-verified. None of these negatives proves that the remaining plaintext is text, that it contains no seed, or that two/three layers are impossible. They exclude the specified password/material/construction combinations. Unknown passwords, opaque 78/79-byte formats, arbitrary 80-byte no-padding payloads, other cipher compositions, and other HD paths remain outside these bounds.
