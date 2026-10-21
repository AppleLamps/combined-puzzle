# 120. The two 80-byte envelopes under a full-padding gate, and one shared prize gate

21 October 2026. Run at the owner's direct request. Null with live controls.

## 1. Why these two envelopes, and why this gate

Terminal (the block that closes phase 3.2, after "Raising the stakes") and
SalPhaseIon-short are both 96 bytes: the 16-byte `Salted__` header and 80 bytes
of ciphertext. A plaintext is therefore 64 to 79 bytes. The creator confirmed on
2023-06-10 (#8569) that 3.2 "is not totally solved, as the final block hasn't been
decrypted": "Correct." The same reply answered "No" to the hint for SalPhaseIon being
inside it, and "Can't say anything about this" to the phase-2 `X 2 S H` line.

A 64-character hex private key fills 80 bytes with a full block of padding (pad 16),
or pad 15 if a newline follows it. A bare WIF (51 or 52 characters) would give a
64-byte ciphertext, so these two envelopes do not hold a bare WIF. Pad 15 or 16 by
chance is about 2^-120 per attempt, so for these envelopes the padding byte
authenticates a hit by itself. Every valid pad was still decrypted in full, run
through the `chk_flags.py` recogniser, and through the shared prize gate (section 5).

A correction to the review that prompted this run: `X 2 S H 4 Y 0 Q B 15` is a
**phase-2** leftover, not a 3.2 leftover. Both are in the candidate list.

## 2. Preregistration

`tools/envelope_campaign.py prereg` generated the list from repository files and
wrote `claude/doc120-runs/candidates.json`, sha256
`5429a22a66cf178ad4b3eaee518671c3c93c0ef832847423d58654715df632ae`. That file was
committed (c39de82) before `run`, and `run` refuses to start if the digest differs.

| Group | Strings | Source |
| --- | ---: | --- |
| G1 literals | 368 | `matrixsumlist`, `enter` (a/b binary) and `lastwordsbeforearchichoice`, `thispassword` (z-fields), decoded by the script from `salphaseion-textarea.txt`; every ordered selection of 1 to 4, joined by nothing, space or newline, lower and upper case |
| G2 textarea | 12 | `shabefourfirsthintisyourlastcommand`, `shabefanstoo`, both without the `sha` prefix; the phase-1 answer and its hash (#225, "our first hint") |
| G3 phase 2 | 43 | every phase-2 line after the first, the braces text, the X2SH template, its substituted and reversed digit strings with H = 42 and H = -42 (the unresolved sign), and the coordinate in seven written forms |
| G4 phase 3.2 | 34 | the 3.2 plaintext outside the Architect block, sentence by sentence, the 149-digit line, "Raising the stakes…", and the checkerboard message |
| G5 pairs | 296 | each literal joined to each lower-case G2 to G4 string, both orders; listed in `pair_ledger.tsv` |

Each text appears as written, lower alphanumeric and upper alphanumeric.

Every string was tried under 17 password and KDF forms on both envelopes:

- forms 0 to 3 of `chk_flags.py` (sha256 hex, raw digest, sha256 of the digest, sha256 of the hex);
- upper-case sha256 hex (the passwordsgenerator.net output the creator linked, #234);
- sha256 hex of the string plus a newline (`echo | sha256sum`);
- the raw string;
- each of those under EVP-SHA256 and EVP-MD5, and raw, hex and HEX under PBKDF2-SHA256 with 10,000 iterations (`openssl enc -pbkdf2`).

Only puzzle text is in the list. A list built from the creator's personal remarks
was considered and not built.

## 3. Controls (all required before the run)

| Control | Result |
| --- | --- |
| Retrodiction: phase 2 (`causality`), phase 3 (seven parts from section 3.3), phase 3.2, opened by the same `derive()` and password code; plaintext hashes `e2f9dd65`, `c4ad9455`, `b82afeb8` | pass |
| The campaign's own one-block padding path opens all three | pass |
| Planted 96-byte envelope, hex key + pad 16, sha256 hex, EVP-SHA256 | flagged, key hit planted Better Half slot |
| Planted envelope, hex key + newline (pad 15), upper hex, EVP-MD5 | flagged, key hit |
| Planted envelope, upper hex key, raw password, PBKDF2 | flagged, key hit |
| `prize_gate.py selftest` (55 planted checks) | pass |

## 4. Result

| | |
| --- | --- |
| Decrypt attempts | 25,602 |
| Valid pads | 97 (expected 100.4) |
| Pad histogram | 97 at pad 1; none at 2 to 16 |
| Recogniser hits | 0 of 97 |
| Prize-gate hits over the 97 plaintexts | 0 |
| Flags (pad ≥ 15, recogniser or prize) | 0 |

By envelope and KDF the 97 split 23/19/10 (Terminal: EVP-SHA256, EVP-MD5, PBKDF2) and
13/18/14 (short), consistent with chance. All 97 plaintexts are in
`claude/doc120-runs/results.json`.

**Scope.** This kills the exact tuples above: these 753 strings, these 17 forms,
these two envelopes. It does not touch other readings of the literals, other
partners for a joint password, or Cosmic Duality. Much of G1 to G4 overlaps the
riddle rounds of doc 117 (about 2,500 hand-justified strings, 14 ciphers and 5
KDFs). What is new here is the full-padding gate on these two envelopes, the
retention and full gating of every pad-1 output (doc 118 recorded pad-1/2
retention limits in older runs), and both prize targets on every plaintext.

## 5. The shared prize gate, and the rescan of stored outputs

`tools/prize_gate.py` is now byte-identical in every GSMG repository. It gates Half
and Better Half under both serializations, and it parses raw windows, hex, WIF, mini
keys, base64, decimal and sha256(text) out of any plaintext. Several sibling
repositories gated against Half's public key only, which silently rejects every
correct Better Half key. This kit's `wintest.py` already listed Better Half; its
`win()` always hashes the candidate first, which suits word lists but cannot
recognise a raw key stored as data. `prize_gate.py` covers that case.

Rescan of this repository plus the rebuilt phase 2, 3 and 3.2 plaintexts
(`setup.py` output): 292 files, 94,046 unique scalars, **0 prize hits** (prize_gate 1.0.1). Summary:
`claude/doc120-runs/prize_gate_rescan.json`.

## 6. Reproduce

```
pip install pycryptodome coincurve
python3 tools/prize_gate.py selftest
python3 tools/envelope_campaign.py run      # about 30 s
```
