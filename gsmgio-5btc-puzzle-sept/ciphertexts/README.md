# Ciphertexts

The published ciphertexts, extracted from the sources in this repo so the `openssl` commands in the
[main README](../README.md) can be run from the project root without pasting anything by hand.

Every file is plain `openssl enc` output: base64 of a `Salted__` AES-256-CBC blob (8 byte magic,
8 byte salt, then the ciphertext), with key and IV derived from the password by EVP_BytesToKey using
SHA-256. That is why `-md sha256` is passed explicitly below: OpenSSL 1.1.0 and newer default to it,
older versions default to MD5 and fail.

| file | published on | password | status |
|---|---|---|---|
| `phase2.txt` | PHASE 2 textarea of the choice page | sha256 of `causality` = `eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf` | decrypts (verified) |
| `phase3.txt` | PHASE 3 textarea of the choice page | sha256 of the 7 concatenated parts (see the hints) = `1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5` | decrypts (verified) |
| `phase3.2.txt` | main hints, after the phase 3 result | sha256 of `jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple` = `250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c` | decrypts (verified) |
| `phase3.2-revealed-blob.txt` | revealed inside the phase 3.2 plaintext | not published | unsolved |
| `salphaseion.txt` | main hints, `### AES Blob` (SalPhaseIon) | not published | unsolved |
| `cosmic-duality.txt` | Cosmic Duality textarea of the saved SalPhaseIon snapshot | not published | unsolved |

## Running them

```
openssl enc -aes-256-cbc -d -a -md sha256 -in ciphertexts/phase2.txt -pass pass:eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf
openssl enc -aes-256-cbc -d -a -md sha256 -in ciphertexts/phase3.txt -pass pass:1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5
openssl enc -aes-256-cbc -d -a -md sha256 -in ciphertexts/phase3.2.txt -pass pass:250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c
```

OpenSSL 3 prints `*** WARNING : deprecated key derivation used.` while decrypting. That is expected
(the blobs use the legacy EVP_BytesToKey derivation) and the decrypted output is still correct.

## Decrypted plaintexts

`plaintext/` holds the output of the three verified decryptions, copied verbatim from `openssl` so that
later results can be diffed against them. Two things are worth knowing:

- `openssl enc -out` writes CRLF line endings on Windows, so these files use CRLF while the rest of the
  repo is LF. `plaintext/phase3.2.txt` is deliberately kept byte for byte: it contains the phase 3.2.1
  blob, whose bytes are not valid UTF-8 (the main hints render that blob through a legacy codepage, which
  is why it shows up there as box-drawing characters).
- The phase 3 plaintext embeds the phase 3.2 ciphertext (byte-identical to `phase3.2.txt`), and the
  phase 3.2 plaintext embeds the unsolved `phase3.2-revealed-blob.txt`, the phase 3.2.1 blob and the
  numeric input of the phase 3.2.2 VIC step.

## Provenance

- `phase2.txt` and `phase3.txt` were lifted from the two `<textarea>` elements of the saved PHASE 2 /
  PHASE 3 page in `assets/pages/choice-is-an-illusion/choice-is-an-illusion.html`; whitespace was
  stripped and the line order kept as published.
- `phase3.2.txt` and `salphaseion.txt` were lifted from the base64 blocks quoted in the main hints
  (the SalPhaseIon blob is spaced out there as `U 2 F s d G V k X ...`; the spaces are removed here).
- `phase3.2-revealed-blob.txt` is the second blob that the phase 3.2 decryption itself reveals, quoted in
  the main hints directly after the `Raising the stakes without extra chances of winning...` line.
  No password has been published for it.
- `cosmic-duality.txt` was lifted from the Cosmic Duality `<textarea>` of the saved snapshot
  `assets/pages/salphaseion-cosmic-duality/salphaseion-cosmic-duality.html` (whitespace stripped).

All six were checked to be valid base64 with the `Salted__` header and a ciphertext length that is a
multiple of 16 bytes. The three known passwords were verified with OpenSSL 3.2.4, decrypting to the
plaintexts quoted in the main hints.