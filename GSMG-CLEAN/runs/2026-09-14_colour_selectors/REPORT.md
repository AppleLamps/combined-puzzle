# Colours as selectors over DBBI's ordinary cells — 2026-09-14

**Result: null under controlled judging. The one sourced use of the prime structure that no run had ever tried —
the 16 blue / 7 yellow markers as *selectors* over DBBI's 61 ordinary cells — produces nothing above control and
no exact-oracle hit.** `14_CRITICAL_REVIEW_2026-09-14.md` move 3.

## 1. What was tested

The complete 84-cell parse was split into its 61 ordinary a..i cells (material) and its 23 `b`/`be` prime
cells (mask). The prime cells were used only to *select*:

- ordinary cells under the nearest preceding marker (blue side / yellow side / all ordinary);
- colour-bounded segment sums (sums of the ordinary runs between two prime markers, per colour) — the direct
  `matrixsumlist` reading;
- masked lattices (marker cells zeroed / set to 2-or-25 / set to 1) summed by row and column at 6 × 14 and
  7 × 12;
- ordinary cells whose 6 × 14 row contains a marker of a given colour;
- FAED's letters at the DBBI blue / yellow / ordinary slots (which colour does the SalPhaseIon instruction
  apply to?).

**142 letter outputs** through the folder's decode families (mod-26 A0/A1, A1Z26, index into the Architect
letters), each scored by common-English-trigram count and judged against **15,600** control readings of the
same selector structures on shuffled input. Planted control: the phase-1 answer's letter values (max score 3 —
at control level, so the metric has no demonstrated power here; reported, not hidden). Every decoded string
also went through the exact oracles: the DBBI sha256 pattern and the three marker plus two prize addresses.
No envelope bytes were read; no AES was run.

## 2. Findings

- **0 of 142 outputs score above control** (max real 2 — `EUMENNETHEOHGGPEUTETNAL`,
  `FTFAEUBAAAHENTGIFSYRTTALYHPIFIHELIOSHERAAEHIAEUU` — fragments, not language; control max 3).
- **Exact oracles: 0 of 142.** No DBBI-pattern match and no address derivation.
- The colour-bounded segment sums — the most literal reading of `matrixsumlist` — give `entasxzgcdyukqbg`
  and `nverfai`: noise.

## 3. What this closes, and what it leaves open

**Closed.** The prime structure used as a selector/mask over the ordinary cells, under every colour
assignment, shape and decode in this family, does not yield readable text or an exact-oracle hit. Together with
the board-shape run, both sourced readings of "prime + colour + sum" are now on the record as controlled
nulls.

**Left open.**

1. **The balanced numbers as cipher *keys*** (Vigenère/Beaufort key material over FAED) — the M5
   labels-as-transformations reading, never run as a bounded family.
2. **The 64-letter `DBBI − VIC` tail** as its own 24-symbol cipher object.
3. The remaining text of `D:\downloads-8.8\puzle-main\` (14 §M9): the reconciliation that closes the
   F-A-E/`yinyang` bookkeeping is reading work, not computation.

## 4. Reproduce

```powershell
python tools\audit_colour_selectors.py
```

Writes `manifest.json` (selectors, controls, oracles) and `results.json` (142 outputs, 15,600-control
maximum, above-control set, oracle hits, top-10, planted-control score). No envelope byte is read by the
script.

**Limits.** Trigram scoring (one metric, stated); the planted control sits at control level, so this run can
reject only strong (score ≥ 4) outcomes, not faint ones; the selector space covers the colour families named
here, not every combinatorial mask.