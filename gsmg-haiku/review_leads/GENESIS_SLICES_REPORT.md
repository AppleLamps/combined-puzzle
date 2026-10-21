# Genesis transaction, using bounded slices

**Result: no remaining container opened and no target private key matched.**

The genesis coinbase transaction was reconstructed from the transaction fields in [Bitcoin Core's primary source](https://raw.githubusercontent.com/bitcoin/bitcoin/master/src/kernel/chainparams.cpp). Its 204-byte serialization hashes to the source's stated transaction ID:

```
4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b
```

This source/data check concerns the new transaction input, not the already solved genesis-headline answer. No solved-stage containers were decrypted.

## Exact interpretation of “only enough digits”

There is no fixed AES passphrase length: the supplied password hashing and EVP derivation accept arbitrary-length input. A private scalar can be represented in 32 bytes or at most 64 hex digits; a candidate still has to match the target. Length alone does not unlock anything.

Inputs were the raw transaction, displayed transaction ID, coinbase scriptSig, output script, and output public key. Their exact bytes are saved in `genesis_slices/sources.json`. Each was also reversed by bytes.

For each input:

- Raw bytes: every prefix and suffix of length 1–64 bytes, plus every contiguous window of 32, 48 and 64 bytes when available.
- Hex: every prefix and suffix of length 1–64 hex digits, plus every contiguous window of 32, 64, 96 and 128 hex digits. Each was tested as lowercase text, uppercase text, lowercase `0x`-prefixed text, and decoded bytes for even-length slices. Sliding hex windows include odd-nibble starting offsets.
- Decimal: both the integer's decimal representation and the heuristic of retaining only 0–9 characters from its hex representation. Test prefixes/suffixes of length 1–78 digits and every window of 32, 64, 77 and 78 digits. Also serialize each resulting integer into 32 bytes when it fits.

For each distinct candidate C, EVP password inputs were C, lowercase hexadecimal SHA256(C), raw SHA256(C), and lowercase hexadecimal SHA256(SHA256(C)), where the inner digest in the last form is raw bytes. All three remaining containers were tested. Sixty transformed passwords already present in the old sweep were skipped; this is a transaction-slice test, not a repeat of the whole headline as a password.

Direct scalar checks covered raw candidates of at most 32 bytes in either byte order; hex text of at most 64 digits; decimal text of at most 78 digits; SHA256 of each transformed password; and the existing binary scalar/share checks on every padding-valid output. Invalid scalars were rejected rather than reduced modulo the curve order.

A separate fixed-length AES interpretation used every raw 48-byte window as either `key32 || IV16` or `IV16 || key32`, bypassing EVP and using the existing ciphertext after its salt header. This is explicitly an alternative to the accepted salted-password protocol.

## Completed counts

| Test | Count |
|---|---:|
| Distinct candidate byte strings | 33,834 |
| New transformed passwords | 135,276 |
| Password-based AES trials across three containers | 405,828 |
| Direct AES key/IV trials | 1,884 |
| Target public-point comparisons | 293,580 |
| Structural candidates | 0 |
| Target matches | 0 |

The combined AES total was **407,712**. There were 1,577 incidental valid-padding outputs. The short containers produced only 79-byte outputs (1,047) and 78-byte outputs (5), with none of length 64–77. Binary structure and scalar tests were used; readability was not a requirement. Valid padding alone was not counted as an unlock.

These negatives apply to the recorded slices and transforms. They do not exclude an unknown position-selection rule, noncontiguous extraction, or a different use of genesis data.

## Reproduction

Exact generator and test code: `review_leads/genesis_slices.py`.

```powershell
python review_leads/genesis_slices.py
```

The script refuses to overwrite existing results; set a fresh OUT directory to rerun. `genesis_slices/candidates.jsonl` records every distinct input and its first derivation label; `padding.jsonl` records all padding-valid outputs; `results.json` records completed counts. Dependencies are the already available pycryptodome and coincurve packages.
