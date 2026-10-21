# Leftover 3.2 packet results (2026-09-08)

> **Correction (audit, 2026-09-08). This packet tested the wrong blue.** The frozen list used `blue = 96791`, produced by an HSV classifier that also erased the FEFEFE cell. The exact-palette blue is **83700** — the number the channel itself named at `2026.txt` #56159. 12 of the 20 strings below involved blue, so the verdict "yellow/blue pixel-count encodings do not decrypt leftover 3.2" was not earned by this run. It has since been earned: `packet/run_kdf_audit.py` re-ran these plus the corrected 83700 operands under four KDFs (4776 attempts) with no decrypt. Note also that this packet's exclusion of "a second colour heuristic (in-channel blue 83700)" excluded the *correct* value. See `AUDIT.md`.

Closed list SHA-256: `c558330fd5a2f0b8cb5c1738148b580bea60280aec8d7969512510ab5ff15e71`  
(`packet/password_list_leftover32.json`, 20 unique strings × raw + sha256hex = **40** OpenSSL attempts)

Blob: leftover phase-3.2 only (`phase32_leftover.b64`). Cosmic Duality was not retried (already decrypted via published 7-XOR in packet 1).

## Verdict

**Yellow/blue pixel-count encodings do not decrypt leftover 3.2.** Zero PKCS#7 successes, zero `1GSMG` pubkey matches.

| Hypothesis | Result |
|------------|--------|
| Decimal / concat / comma / space forms of 50400 and 96791 as OpenSSL password | **Closed — no decrypt** |
| Unpadded hex (`c4e0`, `17a17`) and `0x` prefixes | **Closed — no decrypt** |
| Concatenated hex (`c4e017a17`, `17a17c4e0`) | **Closed — no decrypt** |
| XOR of the two counts (114423 / `1bef7`) or their sum (147191) | **Closed — no decrypt** |
| SHA-256 hex of any of the above as the KDF password | **Closed — no decrypt** |

Packet 1 already closed leftover 3.2 against yinyang / roadmap / `reinserting the prime basics` as *strings*. This packet closed the *numbers* from the 20% extra-door reading.

Neither 50400 nor 96791 is prime. This was a test of “yellow has a number and so does blue” as an AES password, not a proof that those counts are “prime basics.”

## What was not tried (on purpose)

- A second color heuristic (in-channel `blue 83700` vs this repo’s `96791`). That would be a new unbounded list.
- Red-ish 18606. The poem names yellow and blue only.
- `{1,4,21}`, FAED slices, `0x7B9ECC`.
- Growing the list after the frozen hash.

## After this packet

Stop inventing leftover-3.2 passwords. The remaining unhashed object is still the extra door (`#4590`, `#7914`) as a **find with an in-channel SHA-256**, not another ciphertext consumer.

Machine log: `packet/out/results_leftover32.json`.
