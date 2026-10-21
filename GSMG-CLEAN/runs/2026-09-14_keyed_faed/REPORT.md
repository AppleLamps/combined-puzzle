# DBBI material as cipher keys over FAED — 2026-09-14

**Result: null under controlled judging. Every source-grounded key family leaves FAED unreadable: 93 keyed
decodes at or below the 240-control maximum, 0 exact-oracle hits.** `14_CRITICAL_REVIEW_2026-09-14.md` move 4.

## 1. What was tested

The one sourced reading no run had ever tried as a bounded family (10 §7 / 14 §M5): **DBBI supplies key
material, FAED is the message**, under the puzzle's own demonstrated polyalphabetic cipher (Beaufort, whose
hint and 15-letter key are pinned in phase 3.2) plus Vigenère in both directions, in the native 9-letter and
26-letter alphabets (the 9-letter branch re-encoded through the page's own decimal codec, printable only).
**31 key families**: 6 × 14 and 7 × 12 row/column sum lists under signed, unsigned and colour models; the six
balanced numbers (479/484/5/963/474/489); all 23 primes, the 16 and the 7 colour splits, the 84 cell values in
five conventions, the yellow 9, the blue 15, blue-minus-5, and the poster row/column sums. **93 decoded
outputs**, each judged against **240** shuffle-key and shuffle-message controls (planted round-trip passed,
so the metric has power) and through the exact oracles: the DBBI sha256 pattern and the three marker plus two
prize addresses. No envelope bytes were read; no AES was run.

## 2. Findings

- **0 of 93 outputs score above control** (max real 4 — e.g. `luletiwmrkfylapnibtmanskdwlulrjg`,
  `ymvojktqjxsrwmsskkvogvsvxpurihvn`, `gxzsdjrxigvcsjoouffvdshkryifsapi`; control max 8). The balanced numbers
  as keys (`balanced_474` vig_dec, score 3) sit with the noise.
- **Exact oracles: 0 of 93.** No DBBI-pattern match and no address derivation.
- This covers the Beaufort/Vigenère family that the workspace's 10 §7 left open; it does not cover arbitrary
  block ciphers, transpositions before the polyalphabetic layer, or the tail/FAED material as the *key* rather
  than the message (named leftovers below).

## 3. What this closes, and what it leaves open

**Closed.** DBBI-derived additive/subtractive key material, in 31 source-grounded forms × 3 ciphers × 2
alphabets, does not decode FAED to anything above chance. Combined with moves 1–3, every reading in which the
prime structure acts *directly* — as values, as masks, as pointer answers, as keys — is now a controlled null.

**Left open, in the order the evidence now suggests.**

1. **The 64-letter `DBBI − VIC` tail** as its own 24-symbol cipher object (it names `VIC` at 1/4/21 and
   `YOUWON` at 22–27, so it is the one other artifact in the corpus that self-checks).
2. **The tail/FAED/articles as candidate *keys* over each other in non-additive constructions** (Hill, Bifid
   variants with the fixed L2/L3 errors corrected, rail/transposition hybrids) — bounded, pre-registered,
   controls-first, oracles-only.
3. **The sibling-corpus reconciliation** (`D:\downloads-8.8\puzle-main\`, 14 §M9): the only remaining source of
   genuinely new inputs.

**Executed 2026-09-14 — all three, and the theory's sourced space is now exhausted.**

- **Move 5, the tail as a cipher object** (`runs/2026-09-14_tail_cipher/`): IoC 0.0397 (flat, not English);
  60×400 hill-climber at control level (8 vs 7); 178 keyed/transposed forms at control level (2 vs 2); 0
  exact-oracle hits; planted round-trip passed. The tail is not an English-shaped cipher object. Left open,
  non-English by design and needing their own oracle: substitution+transposition composition, the tail as
  numbers/bytes, the tail as a *key*.
- **Move 4 extended, non-additive constructions**: Vigenère/Beaufort over the *tail* with every sourced key
  (balanced numbers, Architect/transcript windows) was included in move 5's 178 forms — null. The Hill/Bifid
  branch remains genuinely open, bounded and pre-registered but not run here: the L3 Bifid decode requires a
  period assumption on FAED that 03 §4 already flags as forced, so it needs a period-recovery justification
  before it is worth a family.
- **Move 6, the sibling corpus** (same report, §2): read and reconciled against 01–14. Everything evidenced
  outside is represented here or refuted; their `yinyang_*`/`youwon_*` series rest on the retracted Chain-4
  primitives (05-void). One entry stays open, framed as the outside file frames it: the **F-A-E sonata
  mapping is a pre-registered untested hypothesis owned nowhere.**

**The honest state of the theory.** Six pre-registered, controls-first runs (moves 0–6) have now null'd every
sourced mechanism: the balance as answer, as pointer-index, as operand, as key; the prime structure as values,
masks and key material; the tail as an English cipher object. The one *positive* result of the whole programme
is structural, not operational: the balance is unique (1/48), which strengthens the claim that 479 is an
intended pointer and correspondingly weakens any remaining theory in which DBBI's prime structure is meant to
be read directly. The next genuinely new information must come from outside the corpus (the creator's own
words: close friends who recognize how he thinks) or from a non-English representation whose oracle has not
been invented yet.

## 4. Reproduce

```powershell
python tools\audit_keyed_faed.py
```

Writes `manifest.json` (pre-registered scope, key families, ciphers, controls) and `results.json`
(93 outputs, controls, above-control set, oracle hits, top-10). No envelope byte is read by the script.

**Limits.** Polyalphabetic-additive family only (no block cipher, no transposition layer, no period other than
the key's own length, no modular arithmetic beyond 9/26); the A9 branch admits only printable-through-codec
outputs; the 9-letter alphabet treatment is one of several defensible ones (the 09 §5/`runs/2026-09-13_*`
family bounded the others without a key).