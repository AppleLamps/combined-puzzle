# Individual recheck of all 755 padding-valid outputs

**All 755 remain UNRESOLVED_RETAINED. None is labelled unimportant, eliminated, or a confirmed incorrect password.** No authenticated new puzzle answer was found.

## What actually triggered them

The original trigger was PKCS#7 padding, not a format detector:

| Exact decrypted suffix | Outputs | Meaning |
|---|---:|---|
| `01` | 750 | A syntactically valid one-byte padding tail |
| `02 02` | 5 | A syntactically valid two-byte padding tail |

I independently rebuilt the key derivation and decrypted every candidate/envelope/profile combination using `cryptography` instead of the original PyCryptodome AES implementation. All 755 reproduce exactly, including every saved plaintext byte and padding suffix. The plaintexts are all distinct. This verifies computation and provenance; it does not authenticate a candidate password.

`reviewed_outputs.jsonl` contains a record for every output, including original candidate and source, envelope/profile, full plaintext, final decrypted block, exact padding bytes, envelope hash, fragments with offsets, embedded decoder outcomes, and unresolved status. No top-N retention or discard threshold is used.

## Why padding alone is expected to trigger

For uniformly random wrong-key output, `01` has probability 1/256, and `02 02` has probability 1/65,536. Across the original 188,112 trials, expected counts are 734.8125 and 2.87036 respectively; expected total padding-valid outputs is 737.694. Observed counts 750 and 5 are compatible with that baseline. A Poisson approximation gives about 16.3% probability of at least five pad-2 outputs at this trial count.

Correction: some earlier scripts used `255/256/256` for pad=1 expectation. Exact PKCS#7 pad=1 only requires the last byte to be `01`; the preceding byte is unrestricted. The expected pad-1 count here is **734.8**, not 731.9. This correction does not change any decrypted bytes or trigger counts.

These are aggregate model comparisons. They cannot certify that each output is noise, and do not exclude a correct intermediate result among them. A genuine 79-byte plaintext in a short envelope would necessarily trigger pad=1 too. Correlated candidate trials also limit statistical interpretations based on independence.

## What the previous whole-message review missed

The earlier zero-format-signals result concerned whole-message recognition. It did not mean there were no short embedded fragments.

This pass scanned ASCII and EBCDIC cp037/cp273 fragments, UTF-16 ASCII-range fragments in both endiannesses and both byte alignments, embedded file/compression signatures, possible zlib headers at every byte offset, and supported encodings within sufficiently long extracted text fragments.

- **374 outputs contain printable fragments of at least six characters** in the scanned views: 1,814 fragment records, including repeated readings under related encodings.
- Longest ASCII run is 12 characters; longest scanned EBCDIC run is also 12. The longest ASCII example is `bc3drH9dB5;(` at output 347, offset 1153. It is recorded, not discarded.
- **232 outputs contain compression-like matches.** There are 375 possible zlib headers: 369 fail validation and six are incomplete. Four gzip signatures also fail validation. No complete compressed stream was found.
- No additional supported embedded encoding was decoded from the extracted text fragments.

The six incomplete zlib cases are explicitly retained:

| Output id | Offset | Bytes remaining | Partial decoded hex |
|---:|---:|---:|---|
| 247 | 1324 | 3 | empty |
| 400 | 71 | 8 | `28` |
| 559 | 74 | 5 | empty |
| 564 | 75 | 4 | empty |
| 621 | 75 | 4 | empty |
| 733 | 1323 | 4 | `ab` |

These are incomplete decoder attempts, not decoded messages. Failure of an embedded gzip/zlib interpretation rejects only that specific stream interpretation, not the surrounding plaintext or candidate.

## Controlled comparison of text-like appearance

Generated 100 deterministic control batches with the same 755 plaintext lengths using uniform random bytes. Compared batch-wide maxima, thereby accounting for looking across the whole set:

- Observed maximum ASCII fraction: 55.6962%. 50/100 control batches reach or exceed it.
- Observed longest ASCII run: 12. 80/100 control batches reach or exceed it.

These metrics reveal no unusually text-like result across this set. They are descriptive checks, not gates; they do not assess every possible language, classical cipher, binary structure, or steganographic encoding.

## The five pad-2 outputs received individual accounting

Full candidates, plaintexts and observations are separately available in `pad2_review.json`:

| Output id | Envelope | Profile | Longest ASCII run |
|---:|---|---|---:|
| 203 | Cosmic | gsmg-md5 | 6 |
| 218 | SalPhaseIon | gsmg-md5 | 4 |
| 283 | Cosmic | raw-md5 | 7 |
| 672 | Cosmic | gsmg | 5 |
| 754 | Cosmic | gsmg-md5 | 5 |

No additional positive evidence emerged for those five from this inspection. They remain unresolved alongside the other 750.

## Changes and verification

`tools/inspect_decrypts.py` now explicitly returns `UNRESOLVED_RETAINED` unless a final target key matches. It also retains partial bytes produced by incomplete or size-limited decompression, instead of dropping them. This fixed an actual inspection blind spot. Limits still remain visible.

All 10 inspector tests pass, including a new truncated-gzip control that yields useful partial plaintext. This recheck also passes controls for mixed binary/ASCII content, odd-offset UTF-16, an embedded zlib stream, and fragments from the actual solved Phase 3.2 plaintext. Thus the fragment scanner demonstrably recognizes content that a whole-message printable gate could overlook.

Reproduce:

```powershell
python tools/test_inspect_decrypts.py
python runs/2026-09-13_assumption_audit/recheck_755.py
```

The recheck deterministically rewrites only its derived files in this directory. Source journal and prior reports are preserved. The prior 755-output key scan is not rerun here: this pass independently verifies AES/padding and extends structural inspection. It does not test arbitrary transforms, other cipher/KDF families, no-padding interpretations, missing bytes, or arbitrary password constructions. Those remain separate hypotheses.
