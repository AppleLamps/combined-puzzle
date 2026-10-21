# Additional key review

Reviewed the address dossier, original community and puzzle Telegram exports, local HTML/encrypted artifacts, and both existing literal-key hunt scripts. No prize key or definitive generator/seed was found. The strongest additional evidence concerns how the puzzle may reveal the key and which earlier exclusions can be trusted.

## 1. The creator never confirmed a complete key in the last ciphertext

Two unedited messages, absent from the address dossier, are particularly useful:

- PUZZLE #2910, 2020-03-24: in reply to a question asking whether the complete private key is in the final chapter or is divided across the puzzle, the creator said: **“Answering that would be too much of a hint.”**
- PUZZLE #2918, 2020-03-24: asked to confirm that the private key is in the last decoded cipher of 3.2, he replied: **“There must at least be something hidden in there.”**

These are not confirmations of splitting. They do undermine treating “one final AES plaintext equals the complete private key” as an established requirement. Keep whole-key recovery, fragment assembly, and a final instruction that transforms earlier material as separate hypotheses. Splitting a stored secret is also distinct from using a split-key vanity-generation service; there is no proof of the latter.

Raw messages and reply context: `key-review-evidence.json`, IDs 2910/2918. Source export: `E:/rabbitv4/newest-telegram-export_2026-09-12/result.json`.

## 2. A reproducible encryption-workflow clue

The first encrypted textarea in `live_phase23.html` decrypts with:

1. `causality` encoded as UTF-8.
2. SHA-256, represented as **64 lowercase hexadecimal ASCII characters**.
3. Those characters used as an OpenSSL-style passphrase in legacy EVP_BytesToKey with **SHA-256**, the stored 8-byte salt, and one digest iteration.
4. AES-256-CBC with ordinary block padding.

The result is 648 bytes, beginning “The ironic 2name of the keymakers”. Among the six tested combinations of raw password / hex digest / binary digest and MD5 / SHA-256 EVP derivation, this was the only valid-padding result. It reproduces the meaningful known plaintext, rather than merely passing a padding test.

PUZZLE #765, an unedited community message by Alex from 2019-05-10, also gives `openssl enc -aes-256-cbc -d -in base64file -a -md sha256 -p`. This is community evidence, not a creator confession about software.

Practical inference: prioritize this exact established pipeline for other password-gated envelopes, while retaining alternatives where their instructions differ. It identifies a demonstrated encryption workflow, not the Bitcoin private-key generator. OpenSSL 1.1.1 documents SHA-256 as the default passphrase digest, but explicit flags and compatible implementations prevent inferring an exact program/version: https://docs.openssl.org/1.1.1/man1/enc/

## 3. Earlier “all ruled out” key tests contained false-negative bugs

Both `hunt_literal_key.py` and `hunt_literal_key2.py` use an address encoder that appends a checksum of HASH160 alone, omitting the `0x00` version byte from the checksum input. Bitcoin Base58Check hashes the entire versioned payload. Source: https://github.com/bitcoin/bitcoin/blob/master/src/base58.cpp

Demonstration with private scalar 1 and an uncompressed public key:

- Correct: `1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm`
- Existing scripts: `1EHNa6Q4Jz2uvNExL497mE43ikXhx2Suvu`

For the target, this means even the right public-key hash would not produce the target address string under the faulty encoder. Other issues:

- Windows labeled `hex64` are parsed by `int(window)` in base 10, never base 16.
- The byte-pair loop requires 128 remaining digits although it reads only 64, skipping valid offsets near the end.
- The WIF regex allows 51 total characters for K/L keys, which require 52. The decoder likewise only accepts the uncompressed total byte length; its compression test reads a checksum byte.

I independently rechecked the bounded candidate families with `review-key-candidates.cjs`. It validates scalar 1 and the dossier public key against their correct addresses, then compares candidate public keys directly with the target to avoid address-format ambiguity.

Result: **31,957 candidate submissions, 22,424 distinct valid scalars, zero matches.** This covers the existing pure/all/saved digit streams; forward, reversed, pi-subtracted, and reversed pi-subtracted variants; decimal64, actual hex64, corrected byte-pair windows, and whole-stream modulo-n forms. It also checks 168 distinct literal hex candidates and 37 checksum-valid WIF candidates, including compressed WIFs, from the same eight local artifacts used in the prior regex pass. These WIFs do not match the target; valid formatting is not evidence that they are puzzle solutions.

This replaces the faulty negative result only for these explicitly tested families. It does not exhaust encodings, passphrases, fragment combinations, or derivation methods. The address-checksum defect does not itself invalidate the separate AES trial code. Original files were retained.

Run from `C:/Users/lucas/Desktop/read`:

```powershell
node .\ADDRESS-INFO\review-key-candidates.cjs
```

Machine-readable output: `candidate-recheck-results.json`.

## 4. The short blob is correctly reconstructed, but its contents remain unknown

The notes miscount the Base64 fragments. The first is 64 characters **when the boundary `z` is retained**; the second is 64 characters. Together their 128 characters decode to the existing 96-byte `embedded_blob_salted.bin`:

- 8 bytes: `Salted__`
- 8 bytes: salt `3ab585348552415d`
- 80 bytes: ciphertext

Removing that `z` leaves only 127 Base64 characters and breaks the expected AES block alignment. The suspected extra-character issue was therefore a counting/extraction mistake, not demonstrated corruption in the saved blob.

Under AES-CBC with PKCS#7 padding, 80 ciphertext bytes permit **64–79 plaintext bytes**. A 64-character hex private key fits, but so do instructions, a URL, a labeled key, or a fragment. Ciphertext length does not select among them. A bare 51-character WIF, including an ordinary trailing newline, does not fit that ciphertext length under these assumptions.

The Cosmic textarea has 1,792 Base64 characters, 1,344 decoded bytes, and 1,328 ciphertext bytes after its header and salt. The older state file's “~4000 b64 chars” note is incorrect.

## 5. Generation clues still have important limits

- The key's uncompressed public serialization independently hashes to the stated prize address. This is a strong constraint on candidate checking, not a generator fingerprint unique to vanitygen.
- The creator's unedited “few seconds” and “Only 4 chars...” messages remain the clearest direct generation evidence.
- Funding dates establish that a key existed by those dates; they do not establish when it was generated. The two GSMG keys could have been generated separately or earlier in one batch. Neither case is proven.
- Ordinary vanitygen starts from a random base key and walks public points; knowing an address prefix does not reveal that base key or search offset. Source: https://github.com/samr7/vanitygen/blob/master/vanitygen.c
- Later community posts naming VanitySearch or seed workflows are not creator admissions. In particular, PUZZLE #25506 describes another participant's generated addresses; #28471 copies split-key usage instructions.
- The neighbor/half/double address deposits in the dossier can be constructed from the public key exposed in 2020. Their 2021 creation therefore does not establish possession of the secret or prove that the puzzle uses arithmetic key splitting.

The most useful remaining direction is to establish what the last puzzle outputs represent before constraining them to a literal full key. The creator's unedited replies explicitly leave that question open. There is presently no evidence-backed timestamp seed, weak RNG, exact generator command, or private-key range to pursue.
