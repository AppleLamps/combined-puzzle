# HILL → IFINDO continuation

**Outcome: no new stage opened.** The proposed Hill relationship remains reproducible and worth retaining, but its complete output remains unexplained. This continuation checked the selected construction and one reversible follow-up. It did not start another open-ended password search.

## What the additional checks establish

### IFINDO is not mechanically forced by BTCSEED

The selected chain is:

```text
DBBI prime reinsertion and column sums → HILLFEXMGSGQ
DBBI-keyed Bifid over FAED → BTCSEED + alternating 282/281 streams
FEXM → GSGQ, natural no-J alphabet, A=0, modulo 25
K = [[1,19],[6,3]], K^-1 = [[2,4],[21,9]]
K^-1 applied to the 282-character stream → IFINDONVFRVODTFMDRYQW…
```

The initial six Hill letters come from carrier text `DOMKAH`, which depends on twelve FAED characters at zero-based positions **3–8 and 288–293**. I traced these dependencies directly.

A controlled change at FAED position 3, from d to b, preserves the entire BTCSEED prefix but changes the Hill opening from IFINDO to GKINDO. Thus IFINDO adds a constraint beyond BTCSEED. This distinguishes it from the four-symbol companion alphabet, which is guaranteed by the Bifid setup.

The audit also computes an exact conditional probability under a narrowly defined random-permutation model. The event and method were selected after previous exploration; the number in the JSON is **not** the probability this discovery is accidental and must not be promoted into confidence that the puzzle is solved. No global multiple-testing correction was established.

### Conventional alphabet choices do not extend it into a full instruction

I solved the example's linear congruences directly under twelve specified conventions: natural 26-letter, natural no-J 25-letter, and DBBI-keyed 25-letter alphabets; A=0 or A=1; and both directions of the proposed example.

This includes a genuine implementation distinction: a singular example matrix can still admit invertible Hill keys, so I did not simply discard it when matrix inversion failed. Natural-26/A=1 admits two keys per direction. Natural-26/A=0 admits no invertible key for FEXM → GSGQ. Natural-25/A=0 reproduces the selected IFINDO result. None of the complete outputs forms a readable instruction.

These are checks of the proposed example convention, not exhaustive tests of all Hill constructions. They do not establish that FEXM/GSGQ was intended as a worked example in the first place.

### A simple rearrangement is a weak next move

The full Hill stream's index of coincidence is **0.03899**. After its first six letters it is **0.03918**. For comparison, the decoded Architect and VIC texts in the supplied files give **0.06512** and **0.05910**, with J normalized to I.

Any transposition preserves the complete letter histogram and this statistic exactly. Consequently, more 23x12, spiral, or word-position rearrangements do not remedy the unusually flat distribution if ordinary prose is the proposed output. This does not mathematically exclude every English string, a nonprose password, or another encryption layer. It does remove a reason to keep trying new rectangle dimensions.

## One complete follow-up tested

The full Bifid output consists of coordinate pairs. I tested returning to that coordinate representation after replacing the selected 282-character carrier with its Hill result, preserving BTCSEED and all 281 companion characters. Both the original and modified Bifid round trips pass.

The resulting 570-character object begins `faedccgciikdfkidfcgcahah…`. Its alphabet is a..i plus k. That ten-symbol limit is another algebraic consequence of retained row coordinates, not a fresh clue. The original wrapper's a..i/o decimal mapping cannot encode k; I did not silently equate k with zero.

Three complete representations were checked:

1. The returned letters themselves.
2. The decimal string obtained from their square positions 0–9.
3. That complete decimal integer converted to big-endian bytes, yielding 237 bytes.

The square-index interpretation is explicitly an additional hypothesis, differing from the wrapper's a..i/o mapping. The 237-byte length by itself is not confirmation.

Each representation was used once with the demonstrated SHA256-lowercase-hex → EVP-SHA256 → AES-256-CBC pipeline against SalPhaseIon, terminal, and Cosmic Duality: **nine trials, all failing padding**. Before the trials, the same implementation recovered the exact saved Phase 2 and partly binary Phase 3.2 plaintext hashes. No printable-only acceptance gate was used.

## Current frontier

Retain the complete HILL/IFINDO construction as a candidate. Do not promote IFINDO to `I FIND O`, `IF IN DOUBT`, or a six-character header. Do not infer a seed simply from the other stream's four symbols. The source wording checked so far does not independently establish those meanings.

The missing step is semantic: **what tells the solver to interpret FEXM/GSGQ as a Hill example, and what tells them how to use the complete result?** A new continuation should bring source evidence to that question, or an independently justified whole-output prediction. It should not start by changing the number of characters removed to obtain another convenient dimension.

The direct coordinate-return construction is now a recorded negative under its stated assumptions. The earlier 277-letter film passage, word-ending selectors, 23x12 rearrangements, and base-100/password constructions are also already covered by previous results. Do not repeat them without a changed, source-supported premise.

## Reproduction

```powershell
node .\PUZZLE-REVIEW\hill-continuation-check.cjs
node .\PUZZLE-REVIEW\hill-coordinate-return.cjs
```

The adjacent JSON files contain the full streams, conventions, source-position trace, conditional-control definition, known-stage hashes, and all nine trial results. Earlier source hashes and the independent DBBI reconstruction remain in `session-recovery-check.json`.
