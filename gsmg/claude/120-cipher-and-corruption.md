# Doc 120: the cipher itself, and the ciphertext itself

26 September 2026. Two assumptions every harness has carried since 2019 were tested
directly. Harness: doc 115's recogniser, planted controls, every control fired.

## 1. "Select from over twenty three ciphers": every cipher OpenSSL offers

The Architect text rewrites the film's "select from the matrix 23 individuals, 16
female, 7 male" as "SELECT FROM OVER TWENTY THREE CIPHERS SIXTEEN ENCRYPTIONS AND/OR
SEVEN INTERTWINED PASSWORDS" and adds "NOTE THAT ALSO BRUTE FORCING MIGHT BE REQUIRED".
The three opened envelopes were AES-256-CBC and the pages say so for phases 2 and 3;
the SalPhaseIon page says nothing. Every screen to date assumed AES-256-CBC (doc 27's
"eight ciphers" run in section 10.1 of the dossier is the one exception, on the solved
vocabulary only).

`claude/scripts/120/cipher_sweep.py`: the 106 distinct cipher names this OpenSSL 3.0
runs with the legacy provider (AES, ARIA, Camellia, SM4, SEED, Blowfish, CAST5, DES,
3DES, DESX, RC2, RC4, ChaCha20, in CBC, ECB, CFB, CFB1, CFB8, OFB and CTR where each
exists), EVP_BytesToKey with MD5 and SHA-256, the doc 119 grounded set (362 strings:
the labels, every chain answer and password, the page and poster text, the Architect
and checkerboard texts, the soup and its blocks, the creator's hint sentences, the
containers' own base64, case variants) as typed and as sha256 hex, all three locks.
Block modes: OpenSSL's own padding check, then the recogniser with the true pad length
(ciphertext size minus the 16-byte header minus plaintext size), so a pad flag means
pad >= 3 as in every other harness path. Stream modes: the recogniser on the raw
output. Controls: a Camellia-256-CBC container and an RC4 container encrypted under a
grounded candidate; both restored. (The first run passed a constant 16 as the pad
length and so tagged every wrong-key decrypt that happened to pass OpenSSL's padding
check, 597 of them at the 1-in-256 chance rate, as a `pad16` flag, which this doc
then filtered by hand; review caught it, the script was corrected and the sweep
rerun. The nine flags below are the same nine.)

| decrypts | pad >= 3 events (about 0.02 expected) | other flags | reading |
|---:|---:|---:|---|
| 767,440 | 0 | 9 | 6 stream outputs opening with the gzip magic `1f 8b` (about 5 expected at 1 in 65,536; three of them are one event seen through CFB, OFB and CTR, which share their first block), 3 distinct-byte-count flags on random bytes. Null. |

The cipher is closed for the grounded set. The Architect's numbers stay what the film
supplies.

## 2. "Some characters need to be zeroed out": the ciphertext edited

If a locked container were an already-known envelope with a character deliberately
damaged, the fix would be a one-character edit and a password already in hand.
`claude/scripts/120/corrupt_test.py`: every single-character substitution (all 64
base64 values and the padding character `=`; the first run had left `=` out of the
alphabet, review caught it and the test was rerun), deletion and insertion in each
container's base64, under the five known
64-hex passwords (phase 1 hash, phases 2, 3, 3.2, the side-page hash) and both EVP
digests, AES-256-CBC. Control: a container encrypted under the phase-1 hash with one
base64 character changed; restored (3,673 variants open it, which is what CBC error
propagation predicts for edits outside the last two blocks, and is why the control
count is large).

| container | decrypts | flags |
|---|---:|---:|
| SalPhaseIon short | 73,770 | 0 |
| Terminal | 73,770 | 0 |
| Cosmic Duality | 1,122,350 | 0 |

Edits in the salt (which change the key), shifts (which change every block) and edits
in the padding blocks are the informative cases; all null.

## 3. The same hint on the passwords, and the half containers

- The five known 64-hex passwords, the sha256 hex of every label and answer, and the
  answers themselves, with the characters at prime positions zeroed, deleted or kept
  (both index bases, upper and lower case), as passwords and as raw scalars: 420
  candidates, null.
- Each 96-byte container's first 48 bytes as a standalone container (header, salt, two
  blocks) under the known passwords: null.

## 4. Settled

The lock is AES-256-CBC under EVP_BytesToKey for any grounded password, or it is a
password nobody has typed; the ciphertext is intact for any known password; the known
passwords do not become the next one by zeroing primes. Every branch of "the method
is different" that the creator's own words could support is now closed at the
grounded set. What remains open is the password.

## 5. Three more closures from the same session

- **The pages have not changed.** Every Wayback capture of the SalPhaseIon page (eight,
  2023-06-01 to 2026-09-24, five distinct digests) carries the same soup and the same
  Cosmic Duality container character for character; the digests differ only in
  indentation, a Cloudflare beacon script added in 2025, and the relaunch's font
  declaration. The choice page's captures (2020-11-12 to 2026-09-24) differ only in the
  per-session CSRF token and, from 2026-01-05, an HTML comment
  `You made it to the next step! Good luck little bunny hunter ;)`, the twin of the
  rebus page's later comment. `/puzzle` is the poster PNG itself. There is no edit
  channel.
- **faed and dbbi as ciphertext.** Vigenere, Beaufort and reverse Beaufort mod 9 and
  mod 10 under 30 chain keys in three letter mappings, then rule 2: best printable
  0.61 on dbbi (45 bytes), inside the null. Hill 2x2 over Z9 and Z10, every invertible
  key matrix (about 6,500 and 8,400), then rule 2: best 0.71 on dbbi, which is what the
  maximum of that many random trials on 45 bytes looks like. The "matrix cypher"
  reading of `matrixsumlist` as a Hill cipher on the a..i blocks is closed at 2x2.
- **August 2023 in context.** "Actually, the hardest part is done" (#8796, 3 Aug) and
  "Something was solved rather... remarkable" (#9627, 6 Aug) sit in a four-day burst
  of 850 messages after "Are you really looking for just the btc...?" (#8774). Asked
  when the remarkable solve happened, he answered "I have no clue" (#9636). Nothing in
  the burst is a decode; the remark is about the state of the chat, not a step.

## 6. What has still not been tried

Ranked by how much a null would settle, cheapest first. Everything above this
section, and docs 116 to 119, is closed.

1. **faed's pieces under encodings other than rule 2.** Doc 118 established four
   differently composed pieces (cuts near 220, 435, 540). Rule 2, per-piece zero
   letters, Vigenere, Beaufort and Hill 2x2 are closed. Open: each piece as a
   bijective base-9 number, as a base-9 number written in reverse, as A1Z26 with the
   piece's own dominant letter as a separator, and as a keystream (mod 9) over the
   Architect text, the checkerboard message and the phase-3.2 intro. About 200
   decodes, an afternoon.
2. **Hill 3x3 on faed with structured keys.** 570 is divisible by 3. The full 3x3
   space over Z9 (about 3.9e8) is too large blind, but the poster gives structured
   candidates: its 14x14 bit grid cut into 3x3 windows (144 of them), the row and
   column sums, the {2, 5, 7} gardeners. About 500 keys.
3. **The two containers as one object.** Every pairing so far combined bytes (XOR,
   interleave, concatenation of base64). Not tried: decrypting the Terminal with
   SalPhaseIon short's salt and vice versa (swapped salts, both digests, the grounded
   set); the second container's ciphertext as the first's IV; CBC-chaining the two as
   one 160-byte stream under one key. Trivial to run on the grounded set.
4. **The chat's non-creator claims, verified rather than screened.** Doc 117 screened
   every string. Not done: reading the handful of posts where a solver claims to have
   opened SalPhaseIon short or the Terminal (#17374, #17385, #25440, #36759) and
   reproducing exactly what they did, because a half-right method is worth more than
   a wrong string.
5. **The Decentraland side quest, re-heard.** The 2020 second door came from an audio
   clip at (-41, -17) that said HASHTHETEXT. If the clip still exists, every word in it
   is creator-authored primary material and only the one command was ever used.
6. **The song's phase-three opening as an operation, not a string.** Doc 99 spent
   the song as text. Its phase-three structure (the judgement, the red or black
   choice) has never been mapped onto the soup's blocks the way phases one and two map
   onto the URL and the phase-1 password. This is reading, not computing.
7. **The 4 x 14 = 56 alternating bits and the Matrix-rain glyph pool** on the 2026
   farewell page were characterised (doc 108) but not run as keys or as the
   `matrixsumlist` operand. Small.
8. **Large but well defined:** the cipher sweep of section 1 extended from the
   grounded set to every chat token (about 117 million OpenSSL calls; feasible only
   with an in-process implementation of the 8-byte-block ciphers, about a day).

What is *not* on this list, because the creator's words rule it out or the record
already closes it: another URL (#9607), the internet (#16624), the on-chain stream
(#12653, doc 117), the relaunched site (doc 108), the poster's data surfaces (doc
115), PBKDF2 (doc 119), the cipher and the ciphertext for the grounded set (this doc).
