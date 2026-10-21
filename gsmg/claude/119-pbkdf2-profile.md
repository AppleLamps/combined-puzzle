# Doc 119: the locks under PBKDF2

26 September 2026. The user supplied a 96-byte `Salted__` container that opens with the
password `Password1$`, and asked whether the locked puzzle containers could follow the
same method. It is a Trust Wallet browser-extension private-key export, and its
documented decrypt command is

    openssl enc -d -aes-256-cbc -pbkdf2 -iter 600000 -md sha256 -pass pass:<password> -in encoded.txt -base64

which yields 64 bytes: the hex private key `000...0001`. Two things about it matter.

1. **The shape is exact.** `Salted__` + 8-byte salt + 80 bytes of ciphertext, plaintext
   64 characters padded with a full block. The Terminal and SalPhaseIon short
   containers are byte-for-byte the same shape (dossier section 6.5), so a 64-hex
   private key or password is what they most naturally hold.
2. **The KDF is one no session had tried.** Every harness since 2019 derived key and IV
   with `EVP_BytesToKey` (MD5 or SHA-256, one iteration), which is what `openssl enc`
   does without `-pbkdf2` and what the three opened envelopes used. `-pbkdf2` has
   existed since OpenSSL 1.1.1 (September 2018), before the puzzle, with a default of
   10,000 iterations.

The user's example does not open under EVP_BytesToKey with any digest, nor under
PBKDF2 at 1 to 100,000 iterations; only the documented 600,000 opens it. So the
question was live.

## The profile

`claude/scripts/119/pbkdf2_sweep.py`. Key and IV are the 48 bytes of
PBKDF2-HMAC-md(password, salt, iterations), as `openssl enc -pbkdf2` derives them;
AES-256-CBC; PKCS7; then the doc 110 recogniser on every valid padding. Two password
forms per candidate: as typed, and its sha256 hex (the puzzle's convention). One
planted container per profile, encrypted with the same profile under a candidate from
the middle of the list.

| tier | candidates | profiles | decrypts | valid pads (expected) | controls | flags |
|---|---:|---|---:|---:|---|---:|
| A: 362 grounded strings (the labels, every chain answer and password, the page and poster text, the Architect and checkerboard texts, the soup and its blocks, the creator's hint sentences, the two locked containers' own base64, case and spacing variants) | 362 | sha256 at 1,000, 2,048, 10,000, 100,000 and 600,000; sha1 at 10,000 | 39,096 | 178 (153) | 6 of 6 fired | 0 |
| B: every token in the chat (both cases), every 2- to 6-gram and every whole message of the creator's | 92,248 | sha256 at 10,000 | 737,984 | 3,000 (2,883) | 1 of 1 fired | 0 |

Null. Valid-pad counts sit at the 1-in-256 chance rate; no recogniser flag outside
the controls.

## What this settles

The locked containers do not open under `openssl enc -pbkdf2` at its default
iteration count for anything typed into the chat or any string the chain provides,
nor at the Trust Wallet count for the grounded set. The example's *shape* was already
the dossier's expectation for the two 96-byte containers; its *KDF* is now a closed
profile. The convention proven on three envelopes (section 2 of the dossier) stands as
the working assumption, and the unknown remains the password, not the derivation.

The 600,000-iteration profile costs about a quarter of a second per derivation, so it
cannot be swept at scale; it is closed for the grounded set only. If a candidate ever
earns a run on its own merits, add this profile to its screen.
