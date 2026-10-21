# M4 zeroing construction against the exact oracles — 2026-09-14

**Result: the zeroing balance is structurally unique and passes two independent self-checks, but none of the
construction's literal outputs satisfies any exact oracle. No envelope byte was read and no AES decryption was
run.** `14_CRITICAL_REVIEW_2026-09-14.md` §M4 / move 1.

## 1. What was pre-registered

- **Construction:** the 24 poster colour markers on consecutive primes; yellow sum 479, blue sum 484; the
  difference 5 is itself a blue prime; #8000 "some characters need to be 'zeroed out'" removes it; the two
  colour lists then balance at 479, and 0-based Architect letters `[479:489]` = `PRIVATEKEY`.
- **Conventions scanned:** 24 rotations × 2 directions of the prime assignment (48), three text conventions
  (letters-only 1,539 at 0- and 1-based; whitespace-stripped 1,544 at 0-based), and the zeroing operand "the
  prime equal to the colour-sum difference".
- **Oracles only (no envelope work):** the three known answer digests; those digests recomputed with the
  candidate substituted for one known part; the four solved marker addresses plus both prize addresses
  (sha256 / sha256d / sha3-256 / raw decimal / raw 32 bytes / sha256-of-hex × compressed and uncompressed
  P2PKH); the DBBI sha256 equality pattern (L5).
- **Out of scope, declared:** the construction used as a selector/key rather than as a literal answer; any
  sign, matrix or FAED continuation.

## 2. The oracle machinery is controlled

All seven controls pass before any candidate is tested (`manifest.json → selftest`):

| control | result |
|---|---|
| sha256 of the 149 checkerboard digits → compressed P2PKH = `18CchrjA3U…` | pass |
| sha256 of the phase-1 answer → `1AD2wfwX…` | pass |
| bit-reversed 192-bit URL integer, raw scalar → `13HGhjkm…` | pass |
| sha256 of the prize address → `1GyT5W…` (prefix) | pass |
| phase-1 answer digest `5ac40783…` | pass |
| phase-2 seven-part digest `1a57c572…` | pass |
| phase-3.2 three-part digest `250f3772…` | pass |

So a null below is a null about the candidates, not about the code.

## 3. The balance condition is unique — this is the part that got stronger

Across all 48 prime assignments:

| measure | value |
|---|---|
| colour-sum differences \|B − Y\| | `5, 33, 37, 57, 85, 93, 107, … 475` |
| assignments whose difference is ≤ 89 (necessary: every assigned prime is ≤ 89) | 5 of 48 |
| assignments where the difference is actually one of the larger colour's primes (zeroable) | **1 of 48** |
| distinct balanced values produced | **1** — `479` |
| assignments whose balanced index selects `PRIVATEKEY` | **1** |
| assignments whose balanced index selects any of ten notable words (`PRIVATEKEY`, `REINSERTING`, `SELECT`, `BRUTEFORCING`, `INTERTWINED`, `SOURCECODES`, `PRIMEBASICS`, `YOUWON`, `PRIVATE`, `CIPHERS`) | **1** |

The authenticated rotation is the only one that balances, and the balance condition itself therefore selects
the convention instead of the solver choosing it. That removes the main objection recorded in 03 §1
("484 − 479 = 5 holds only for the authenticated spiral rotation"): **no other rotation balances at all.** The
construction now has two independent self-checks (unique balance; the balanced index lands on `PRIVATEKEY`).

## 4. Oracle results: null

476 candidates (5 families) × 1,464 scalar forms → **0 hits on every oracle**:

| family | candidates | what it was |
|---|---:|---|
| `index_window` | 384 | Architect windows of length 1–48 starting at 478/479/480 in both text conventions, upper and lower case |
| `prime_list` | 30 | yellow list, blue list, blue with 5 zeroed / removed, both orders, five separators |
| `balanced_number` | 28 | 479, 484, 5, 963, paired and joined forms, `blue479`-style, `zero5` |
| `poster_matrix_sums` | 26 | poster row/column sums before and after zeroing marker 3, four serialisations each |
| `zeroed_marker` | 8 | the colour stream and the poster URL with marker 3 zeroed, replaced by `0`/`Z`, or removed |

Specifically: no candidate **is** a known answer; no candidate **replaces** any of the three phase-3.2 parts or
the seven phase-2 parts while reproducing `250f3772…` / `1a57c572…`; no candidate's hash or raw form derives
any marker or prize address; and no candidate's sha256 carries the DBBI token pattern.

## 5. What this closes, and what it leaves open

**Closed.** The M4 construction, taken as a *literal answer generator*, is null against every exact oracle in
the corpus. It does not re-derive an earlier-stage answer, and it is not itself a key. Any future attempt to
use `479`, the Architect windows at 479, the prime lists or the zeroed URL as an AES password can be skipped —
they are now covered by an exact rather than a padding test.

**Left open, in priority order.**

1. **The construction is a pointer, not a payload.** Its self-checks (unique balance → `PRIVATEKEY`) point at
   Architect offset 479 the way `HASHTHETEXT` pointed at the poster caption. The next question is what the
   *balanced* value 479 and the zeroed operand 5 do to the unread material: index 479/484 into FAED (570
   letters) and into the 149-digit checkerboard string, and 479/5 as operands on the DBBI 84-cell values.
2. **Composition with the page's own labels** (M5): `shabef our first hint is your last command` and
   `shabef ans too` name hashes; whether the balanced construction supplies the *object* of those hashes is
   untested.
3. The 661 unexplained SalPhaseIon characters and the `DBBI − VIC` 64-symbol tail are untouched by this run.

## 6. Reproduce

```powershell
python tools\audit_m4_zeroing_oracles.py
```

Writes `manifest.json` (pre-registered scope, input hashes, oracle definitions, self-tests),
`assignment_scan.json` (all 48 assignments with their differences, zeroability, balanced values and selected
windows), `candidates.jsonl` (every candidate with family and provenance) and `results.json` (oracle
coverage and hits). No envelope byte is read by the script.