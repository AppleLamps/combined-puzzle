# Doc 121: the three cheapest untried items, run

26 September 2026. Items 1 to 3 of doc 120 section 6, in one sitting.
`claude/scripts/121/pieces_and_pairs.py`. All null.

## 1. faed's pieces under encodings other than rule 2

Eleven piece definitions (the doc 118 likelihood cuts 220/435/540, the window cuts
250/315/405/465, the 32-character tail, and faed whole), each:

| reading | result |
|---|---|
| bijective base 9 (digits 1..9), forward and reversed, as bytes | printable 0.23 to 0.50 against a null median 0.36, max 0.52 |
| the same integers as raw private scalars (mod N, and the low 256 bits) | 44 keys, 0 hits |
| A1Z26 with the piece's dominant letter as the separator | 1 to 20 letters land in 1..26 per piece, English score at the random baseline |
| the piece as a keystream mod 26 (a..i as 0..8 and as 1..9, add and subtract) over the Architect text, the checkerboard message and the phase-3.2 intro | best English score -3.41 against random -3.94 and English -2.93; no reading rises above the noise |

## 2. Hill 3x3 on faed with keys the poster supplies

152 key matrices: every 3x3 window of the 14x14 bit grid, every run of nine
consecutive row and column sums, the gardeners' primes in six arrangements, the
April 2021 numbers, the identity; each as the encryption and as the decryption matrix
over Z9, Z10 and Z26; outputs through rule 2 (Z9, Z10) or as letters (Z26).
Best printable 0.46 (null median 0.37); best English score at random. Null.

## 3. The two 96-byte containers as one object

The doc 119 grounded set (362 strings, four password profiles, both digests) against
eight synthetic containers: each small container's ciphertext under the other's salt;
Cosmic Duality's ciphertext under either small salt; the two ciphertexts chained in
both orders under one key; each under the XOR of the two salts; and each decrypted
with the other's first block as the IV. 31,856 decrypts, 0 recogniser flags.

## 4. The solver claims, read for a method

Every claim of having opened a small container is, by its author's own account, a
valid-padding decrypt of random bytes. Zil, 12 Dec 2023: "I also have decrypted the
small AES'es" (#17370), then "due to openssl these AES'es can be decrypted without an
error but they'll still yield unreadable rubbish" (#17383) and "that means nothing to
me" (#17387). Minase the same day claimed Cosmic Duality with "a five part vigenere":
1,328 bytes, "Plaintext 0" (#17359 to #17365). #25440 is a guess about what the
Terminal holds, not a decrypt. #36759 is a joke photo. No claim carries a method.
Closed.

## 5. The Decentraland audio: blocked on the file

The 2020 side quest at (-41, -17) was an audio file whose "apparent solution is three
words" (#2943), HASH THE TEXT; solvers said "you need to manipulate the audio file"
(#3195) and heard "bird songs" in it (#3164). The file was shared on a Discord, never
in this chat, and it is not in the repository. Nothing here can re-hear it. If a copy
exists, every word in it is creator-authored and only the one command was ever used.

## Settled

faed's pieces do not read under any simple positional encoding the chain has used or
named, the poster does not supply a Hill key that reads faed, the two locks are not
one object, and no solver claim carries a method. Items 5 (needs the audio file), 6,
7 and 8 of doc 120 section 6 remain.
