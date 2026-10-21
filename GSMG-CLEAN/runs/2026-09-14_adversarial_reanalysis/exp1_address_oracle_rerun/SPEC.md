# Experiment 1 — re-run of the voided address oracle (pre-registered)

Written before execution. Date: 2026-09-14.

## Why

Six 2026-09-14 audit scripts build `TARGET_H160 = {address: hash160}` and then test
`if computed_hash160 in TARGET_H160`. That membership test is against the dictionary **keys**
(Base58 addresses), so it can never be true. Their "0 marker/prize address hits" statements are
therefore not results of a test that could fail. Affected (file : dict line / test line):

- `tools/audit_m4_zeroing_oracles.py` : 86-87 / 252-256
- `tools/audit_pointer_selectors.py` : 157 / 218
- `tools/audit_board_shape_sums.py` : 127 / 162
- `tools/audit_colour_selectors.py` : 164-167 / 200
- `tools/audit_keyed_faed.py` : 139-142 / 175
- `tools/audit_tail_cipher.py` : 160-163 / 194

Each script's self-test reproduces the marker addresses through a *different* code path
(`addresses(k)['compressed'] == MARKER_ADDRS[i]`), so the self-tests pass while the production
loop is dead. `tools/audit_structural_key_formats.py` later rescanned the same retained outputs with a
correct dictionary, but it derives scalars only from raw bytes / hex64 / WIF / base64 / decimal
tokens: it never hashes a candidate string. So the oracle that produced the three solved marker
addresses (sha256(answer) → scalar → compressed P2PKH) has never validly run over these
38,615 retained candidates.

## Inputs (exact)

| file | rows | field |
|---|---:|---|
| `runs/2026-09-14_m4_zeroing_oracles/candidates.jsonl` | 476 | `candidate` |
| `runs/2026-09-14_pointer_selectors/candidates.jsonl` | 2,119 | `candidate` |
| `runs/2026-09-14_board_shape_sums/all_outputs.jsonl` | 744 | `output` |
| `runs/2026-09-14_colour_selectors/all_outputs.jsonl` | 142 | `output` |
| `runs/2026-09-14_keyed_faed/all_outputs.jsonl` | 93 | `output` |
| `runs/2026-09-14_tail_cipher/all_outputs.jsonl` | 181 | `output` |
| `runs/2026-09-14_matrixsum_lastwords/all_outputs.jsonl` | 34,860 | `output` |

SHA-256 of every input file is recorded in `manifest.json` at run time.

## Scalar derivations per candidate string `s` (UTF-8 bytes `b`)

1. `sha256(b)`  (the proven marker convention)
2. `sha256(sha256(b))` (sha256d)
3. `sha3_256(b)`
4. `sha256(lowercase hex of sha256(b))` — "sha256 answers too" applied to the hex passphrase
5. `sha256(b.lower())` when `s` has upper-case letters
6. raw decimal integer when `s` is all digits
7. raw 32 bytes big/little-endian when `len(b) == 32`
8. `sha256(bytes.fromhex(s))` and `int(s, 16)` when `s` is 64 hex characters
9. every overlapping 32-byte window of `b`, big- and little-endian (covers binary outputs)

No recursive decoding (that was done correctly by `audit_structural_key_formats.py`).
No concatenation across rows. No AES, no envelope bytes.

## Oracle

For every scalar `k` in `[1, N)`: compressed and uncompressed secp256k1 public keys →
`hash160 = RIPEMD160(SHA256(pub))` → membership in a set whose **elements are hash160 hex strings**
(never addresses), built from:

- markers `18CchrjA3Uzfrzy4DFqao9ric6YfK4hjdc`, `1AD2wfwXukZ1kUAy848hTQQ72aSBZPB75r`,
  `13HGhjkmKUkP8sk9k63BLmhkxRjy7uK4Rp`
- prize `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` (Half), `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` (Better Half)
- plus a Base58 address-prefix check for the partial marker `1GyT5W` (compressed form only, as
  in the earlier scripts; uncompressed also recorded).

Every scalar that hits is retained with the source file, line, field, derivation and pubkey form.

## Controls (executed by the same production loop, on planted copies of the real corpus files)

Positive rows appended to a copy of each corpus file, using the real field name of that file:

- P1 `theflowerblossomsthroughwhatseemstobeaconcretesurface` → derivation 1 must hit `1AD2wf…`
- P2 the 149 checkerboard digits → derivation 1 must hit `18Cchrj…`
- P3 decimal integer of the bit-reversed poster URL bits → derivation 6 must hit `13HGhjk…`
- P4 64-hex of sha256(P1) → derivation 8 (`int(s,16)`) must hit `1AD2wf…`
- P5 the prize address string `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` → derivation 1 must produce a
  compressed address with prefix `1GyT5W`
- P6 `THEFLOWERBLOSSOMS…` upper-case → derivation 5 must hit `1AD2wf…`

Negative rows: P1 with its last letter changed; P4 with one nibble changed; P2 with one digit
changed. These must produce no hit.

Acceptance: on the planted corpora the hit list must be exactly the six positive rows (by line
number) and nothing else; then the real corpora are scanned with the identical function. Any
discrepancy voids the run.

## Result recording

`results.json` (counts, controls, hits), `hits.jsonl` (every hit, if any), `manifest.json`
(input hashes, code hash), `run.log`. The experiment is complete when all seven files have been
scanned; unfinished files are listed explicitly if the run is interrupted.

## What a null does and does not mean

A null means: none of these 38,615 strings, under derivations 1-9, is a private key for the two prize
addresses or the three full marker addresses. It does not mean the underlying constructions are wrong
as intermediates, and it says nothing about the AES envelopes.
