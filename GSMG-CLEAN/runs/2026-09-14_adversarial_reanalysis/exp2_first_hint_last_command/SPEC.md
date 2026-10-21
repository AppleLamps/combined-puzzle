# Experiment 2 — "sha256: our first hint is your last command", executed with a validated harness and full retention (pre-registered)

Written before execution. Date: 2026-09-14.

## Source instruction (exact)

SalPhaseIon stream `[860:895]` literal `shabefourfirsthintisyourlastcommand`, immediately followed by the
128-character envelope and then `shabefanstoo`. Under the page's own letter-digits (b=2, e=5, f=6) the
shared prefix `shabef` is `sha256`, so the line reads "sha256 · our first hint is your last command"
(08 §0.3). Creator reply to a request for a hint on exactly this line: #20224 "🤐".

## Why re-run something that was "tested"

The earlier sweep (round 1 Addendum 18, 8,004 decrypts; G2 15,060) is on record as: raw-only key oracle
(04 §G), printable-ASCII judging later admitted to be wrong (round 1 lines 1594-1600), outputs not
retained, Half-only address checks in some runs, and the B1 half-blob bug affecting B1-only sweeps.
No retained output set exists that this reanalysis can re-inspect. The candidate family is small
and source-based, so a bounded re-run with complete retention is cheap and closes a documented weak null.

## Input object

The "first hint" referents that the material itself supports, each with its provenance:

| id | string(s) | provenance |
|---|---|---|
| F1 | `Follow the white rabbit` and case/space variants; `follow_the_white_rabbit` (poster file name) | forward #11248 ("actual first hint"), `originals/poster/follow_the_white_rabbit.png` |
| F2 | `5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75` | #225, the creator's first message that is a hint (a digest to check answers against) |
| F3 | `theflowerblossomsthroughwhatseemstobeaconcretesurface` | the answer whose sha256 is #225 |
| F4 | `giveit = givetit`, `givetit`, `giveit` | #867, the first thing the creator called a 'hint' |
| F5 | the #1710 poem (full, and its first line) | the announced "final hint" (#881/#4096): control referent, not a first hint |
| F6 | `gsmg.io/theseedisplanted`, `theseedisplanted` | the poster's own decode: the first instruction the puzzle gives |
| F7 | `HASHTHETEXT` | listed in 03 §… as a candidate; provenance weak, kept for completeness |

## Representations

For each string `s`: (a) `s` itself as the passphrase; (b) lowercase-hex sha256(s) (the proven
convention); (c) lowercase-hex sha256 of (b) ("sha256 answers too" applied twice). Whitespace and case
variants are explicit rows, not normalisations. Nothing else.

## Operation

OpenSSL `Salted__` AES-256-CBC, key/IV from EVP_BytesToKey with SHA-256, 1 iteration (proven on Phases
2, 3, 3.2) and, as a second declared profile, MD5 (OpenSSL < 1.1.0 default). PKCS#7 unpadding.

Envelopes: `data/locked_salphaseion_short.bin`, `data/locked_terminal_phase3_2_end.bin`,
`data/locked_cosmic_duality.bin`.

## Harness validation (must pass before any locked envelope is touched)

1. Phase 2 ciphertext (from `originals/pages/phase2_choice.html`) with `causality` → bytes equal to
   `data/phase2_plaintext.bin`.
2. Phase 3 ciphertext (same page) with the seven-part sha256 → bytes equal to `data/phase3_plaintext.bin`.
3. Phase 3.2 ciphertext (tail of the Phase 3 plaintext) with sha256 of the three-part answer → bytes
   equal to `data/phase3_2_plaintext.bin`.
4. Negative: each of the three with one hex digit of the password changed must fail padding or
   differ from the plaintext.

## Acceptance and retention

Every decrypt is retained as raw bytes (`outputs/`) whether or not padding is valid. Each output is
recorded with: envelope, string id, representation, KDF, pad validity, pad length, printable ratio,
and the Experiment-1 key recogniser result (sha256/raw32 windows → hash160 vs the five targets) applied to
the raw plaintext bytes. Expected chance rate of a valid PKCS#7 pad on an 80-byte block for a wrong key
is about 1/256 + 1/65536 + …; the count is reported against that expectation.

A "result" requires either an address-oracle hit or a plaintext that a reader can confirm as language or
as a structured key. Pad validity alone is not a result.

## Prediction that can fail

If "our first hint" is one of F1–F7 in one of these forms, one envelope opens to readable text or a key.
Otherwise every output is noise at chance pad rate. A null excludes exactly these strings in these forms
under these two KDF profiles, and nothing more.
