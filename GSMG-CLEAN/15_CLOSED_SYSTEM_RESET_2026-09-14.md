# 15 — Closed-system reset: everything needed is already present

**Follow-up qualification:** The exact aligned-table experiment is documented at
`E:\rabbit-combined\GSMG-CLEAN\runs\2026-09-14_aligned_replacement_v2\REPORT.md`.
It finds 22 shared edit intervals; a 24-row table is caused by two transcript-dependent extra edits.
The source-to-rewrite layer has **not** been established as the correct operand, and the negative tests
do **not** prove that the current matrix is wrong. They constrain only the declared representations.
Original word boundaries are unavailable: the saved readable speech agrees with the exact 1,539 letters,
but its spacing is editorial. See the complete table and its eight accounting-checked alternatives.

**Correction:** the earlier conclusion that the next information must come from outside the puzzle was wrong.
Creator #9607, replying directly on **2023-08-06** to “is there another URL … otherwise brute force?”, said:
**“No need. You have all the info.”** On **2023-11-24**, #16624 separately answered whether internet was
still required: **“Nope.”** These statements do not solve the operation, but they rule out personal biography,
new URLs, missing media and new hints as required inputs.

No envelope was opened in this reset. The correction changes the search boundary, not the solve status.

**Key-format qualification.** The envelope inspector already checked raw 32-byte windows, hex64, WIF and
base64-to-32 recursively. The new structural audits did not all use that inspector. This gap is now closed by
`runs/2026-09-14_structural_key_formats/REPORT.md`: 38,615 retained outputs → 20,436 recursive byte nodes →
463,290 unique valid scalars, including big/little-endian raw32, one hex64, 35 base64-to-32 values, 42
WIF-shaped tokens and 198 explicit 32+32 half checks. Seven positive controls passed; 0 valid WIFs and 0
marker/prize matches. This rules out keys already present in those outputs, not a transformation not yet found.

## 1. What the negative runs actually establish

Moves 0–6 do **not** exhaust the puzzle. They exhaust declared implementations of one solver model:

- primes/colours as numerical values, masks, indices, literal answers or repeating additive keys;
- DBBI and FAED as independently readable fields under common classical constructions;
- the `DBBI − VIC` tail as an English-shaped monoalphabetic/additive/transposition ciphertext;
- literal last-word referents and existing row/column sum lists.

The nulls say those implementations are wrong. They do not say the required operand is absent.

## 2. The internal instruction that was under-modelled

The modified Architect speech says:

> RETURN TO THE SOURCE CODES ALLOWING A TEMPORARY DISSEMINATION OF THE CODE YOU HOPEFULLY CARRY
> REINSERTING THE PRIME BASICS AFTER WHICH YOU WILL BE REQUIRED TO SELECT …

The earlier source-reinsertion audits did **not** implement the differential meaning of this sentence. They
treated “source codes” as the raw/transliterated/plaintext layers of the *puzzle cipher block*, disseminated
them by XOR, and pasted prime lists at hand-picked anchors. They explicitly left Bitcoin source, HTML source
and the post-reinsertion cipher selection out of scope.

`tools/audit_architect_differential.py` instead aligns the local film source with the puzzle rewrite and
extracts puzzle-only/source-only/replacement/boundary streams. Result: **728 differential outputs**, but the
broad high scores merely reproduce intact English from source dialogue. Prime/colour selections of the actual
puzzle-only edits produce no complete new instruction. This establishes the correct operand class (the rewrite
itself) but not the final operator.

## 3. The exact decoded command chain, retested literally

Creator #8446 decodes in order to:

`yellowblueprimes matrixsumlist lastwordsbeforearchichoice yinyang wewontgiveawaythepassword
itsinfrontofyoureyes butyourenotseeingit verylaststepisatruegiveawaypromised`

The 2026-09-13 pipeline indexed whole words modulo passage length and admitted its word scorer had no power.
It did not test the natural literal grammar: matrix sum list → index the words before “Choice” → take the
selected words’ **last letters**.

`tools/audit_matrixsum_lastwords.py` closes that gap using all 552 saved sum lists, four internal cuts, direct
and modulo indexing, bases 0/1, and whole words / initials / finals / word lengths:

- **34,860 real outputs**;
- **557,760 shuffled-sum controls**;
- control maxima: initials 4, finals 6, length encodings 1;
- **0 real outputs above control**;
- **0 DBBI-pattern hits**.

Therefore the missing reading is not simply “take last letters of words selected by the existing row/column
sum lists.” The decoded command chain remains authoritative; the **matrix sum list itself is wrong or is being
formed from the wrong matrix**, or “last words” describes a different unit than word-final letters.

## 4. The new boundary

The next move must remain entirely inside the authenticated puzzle and must explain these phrases together:

1. **SOURCE CODES** — likely actual source representations, not a synonym for plaintext.
2. **TEMPORARY DISSEMINATION OF THE CODE YOU HOPEFULLY CARRY** — a state transition, not arbitrary XOR.
3. **REINSERTING THE PRIME BASICS** — restoration implies something was removed before the displayed data.
4. **MATRIXSUMLIST → LAST WORDS BEFORE ARCHI CHOICE** — a typed pipeline; current row/column sums are not its list.
5. **YINYANG** — the next phase, not necessarily the 479 balance.
6. **PASSWORD IS IN FRONT OF YOUR EYES / VERY LAST STEP IS A TRUE GIVEAWAY** — predicts a visible,
   self-checking final construction rather than a high-entropy brute-force output.

The highest-value internal object is now the **complete source-to-rewrite edit map**, specifically the source
material removed at the puzzle’s splice points and the exact locations where `CODES`, `HOPEFULLY`, `BASICS`,
the 23/16/7 replacement and `ACTUAL PRIVATE KEY` were inserted. A successful model must reconstruct a
substantial field or explicit instruction before touching AES.

## 5. Reproduce

```powershell
python tools\audit_architect_differential.py
python tools\audit_matrixsum_lastwords.py
```

Evidence:

- `runs/2026-09-14_architect_differential/manifest.json`, `alignments.json`, `results.json`
- `runs/2026-09-14_matrixsum_lastwords/manifest.json`, `results.json`

Both scripts are offline, read zero envelope bytes, and run zero AES decryptions.