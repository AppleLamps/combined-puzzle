# Move 1: the balanced pointer as an operand on the unread fields — 2026-09-14

**Result: null with real coverage. No readable message and no exact-oracle hit. This also closes the
folder's own untested "next idea" recorded at 03 §1.** `14_CRITICAL_REVIEW_2026-09-14.md` move 1.

## 1. What was tested

Selectors 5 (the zeroed prime), 479 (balanced), 484 (blue), 963 (total) and six derivatives
(474, 489, 91, 86, 95, 100) were applied as *operands* rather than answers:

- **Exhaustive window decode** through the page's own demonstrated codec (a..i/o → decimal integer → bytes)
  over every window of FAED (570), DBBI (91), the 149 checkerboard digits, the 1,075-character SalPhaseIon
  stream, the Architect letters, both VIC-difference strings and the colour word: 3,675 source characters,
  **107 printable windows**, **0 readable messages**. The only windows above chance length are the two known
  labels (`lastwordsbeforearchichoice`, `thispassword`) that the codec was already demonstrated on — the page
  codec round-trips its own evidence, and finds nothing new.
- **Prime and zeroing selectors** (03 §1's untested idea): characters at prime positions, prime positions
  zeroed, non-prime positions zeroed, and the blue/yellow poster-colour prime positions zeroed or removed —
  all decoded through the same codec: nothing readable.
- **2,119 selector-window candidates** (1–32 characters from each selector, both indexings, both cases, plus
  the selector-decode bytes) × **6,738 scalar forms** against the exact oracles — the three chain digests,
  part-replacement against `250f3772…`/`1a57c572…`, five addresses, the DBBI token pattern: **0 hits**.
  The oracle machinery passed its control first (sha256 of the 149 digits reproduces `18CchrjA3U…`).

## 2. What this closes, and what it leaves open

**Closed.** Indexing the unread fields with the balanced pointer and reading through the page codec is not
where the reading is. The 661 SalPhaseIon characters and the 64-letter tail stay unread under this codec.

**Left open.** The selector families not covered: the balanced numbers used as *cipher keys* (Vigenère/Beaufort
keys over FAED, exactly the 10 §7 / 14 §M5 reading of the labels-as-instructions); off-page selectors such as
the colour *selectors*; and the seeded-text comparisons already bounded by the 09 §5/`runs/2026-09-13_*` family.

## 3. Reproduce

```powershell
python tools\audit_pointer_selectors.py
```

Writes `manifest.json` (controls, selectors, oracle definitions), `window_scan.json` (all 107 printable
windows with offsets), `prime_selector_decodes.json`, `candidates.jsonl` and `results.json`. No envelope byte
is read by the script.

**Limits.** Literal answers only; windows for the address oracle capped at 32 characters; the balanced numbers
as cipher keys and the tail/FAED as polyalphabetic objects are named leftovers, not tested here.