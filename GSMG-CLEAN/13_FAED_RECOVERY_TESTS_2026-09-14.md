# FAED recovery tests — 2026-09-14

**Unsolved. No new locked-stage plaintext or private key was recovered.** This pass tested omitted decoding models; it did not generate AES passwords. Original puzzle sources and previous recovered outputs remain unchanged. At the final checkpoint the goal runner reported `usageLimited`; the objective was not marked complete or blocked.

## 1. Decimal zero/nine ambiguity after Hill decryption

Earlier modulo-9 numerical tests selected one interpretation of each residue. Decimal `0` and `9` coincide modulo 9, so those tests did not cover selective restoration of zeros after a Hill transform. This is a concrete coverage gap, not evidence that this cipher is intended.

The new search covered every invertible affine 2×2 matrix modulo 9, every two-component offset, both input directions, adjacent/half pairing, and adjacent/half output: **2,519,424 model constructions**. The two letter-index conventions are included through the complete offset family. These are model counts, not independent statistical trials.

An exact integer-bound filter retained **655 complete residue streams**. Every decimal position with residue zero was then allowed to be either decimal `0` or `9`. Exact interval search checked all resulting byte lengths for full ASCII, including tab, LF and CR. None yielded full text. The same restoration was applied to 271 previous complete streams from the corrected 3×3 keys and prime-sum Beaufort models. All **926** searches finished without a node-limit cutoff, visiting 8,525 interval nodes in total.

The filter was independently tested with a **236-byte planted message**: decimal encoding, zero padding, affine Hill encryption, the entire exhaustive search, then zero/nine restoration. It recovered the exact complete message and its expected inverse matrix. Python also independently reproduced all 1,908 retained real/control streams and their affine round trips.

This excludes the stated two-by-two/full-ASCII construction. It does not exclude arbitrary binary, Unicode, another numeral system, another transform, or a different stage order.

Evidence: [results](runs/2026-09-14_lossy_hill/restoration_summary.json), [independent verification](runs/2026-09-14_lossy_hill/independent_verification.json), [complete retained streams and restorations](runs/2026-09-14_lossy_hill/restoration_results.json).

## 2. Recovering unknown Hill keys from complete source passages

This test derives an arbitrary affine decryption matrix from an independent set of ciphertext blocks, then demands agreement across the **entire** candidate passage. It does not search only the earlier FEXM/GSGQ keys.

The final test contains **1,569 source passages**, represented by **2,554 numerical templates**: 516 decimal, 985 base-9 and 1,053 bijective-base-9. They use complete word windows within saved Architect/Neo utterances and the readable modified speech. Exact, lowercase, uppercase, connected lowercase and connected uppercase forms are included. The readable modified speech is a supplied rendering, not proof of original spacing or punctuation.

Each template is 567–570 digits, explicitly left-padded with zeros to 570 before the matrix operation. Matrices have dimensions 2, 3, 5, 6, 10 or 15; moduli are 9 or 10; both input directions and adjacent/equal-length-rail layouts are covered. All 96 ciphertext designs had sufficient rank to determine the candidate affine map; none was silently skipped. Across **245,184 full comparisons**, there were **zero complete matches**. The mod-9 decimal interpretation permits zero/nine collisions.

Four layout controls recovered their planted plaintext residues, and changed-ciphertext controls were rejected. This does not exclude other passages, encodings, padding placements, dimensions or nonlinear transformations.

Evidence: [scope](runs/2026-09-14_lossy_hill/manifest.json), [summary](runs/2026-09-14_lossy_hill/summary.json), [full plaintext templates](runs/2026-09-14_lossy_hill/passages.json), [matrix designs](runs/2026-09-14_lossy_hill/models.json).

## 3. Architect words as cipher keys; prime digits before matrix formation

Rather than requiring FAED to contain a quotation, this test used source words as **keys**. It includes every complete-word suffix of individual saved Architect/Neo utterances and the modified speech, plus decoded labels, the demonstrated THEMATRIXHASYOU key, DBBI and the solved seven-part answer. Texts have explicit letter-ordinal, UTF-8-byte, decimal-integer and base-9-integer representations.

It also tested a previously omitted ordering: replace prime markers by their prime values, **serialize those values into decimal digits**, then form the matrix. The complete 83-cell parse becomes **102 digits**; the 84-cell parse becomes **103 digits**. All exact rectangles and both sum axes produce 60 lists across unsigned and the two explicitly hypothetical signed-digit variants. No source character is discarded to force a rectangle.

The 3,371 text keys and matrix lists give 12,618 distinct numerical key vectors. Vigenère, Beaufort and the addition variant were applied to full FAED modulo 9 and modulo 10, with stated index conventions and key reversal. After deduplication there were **273,478 complete transforms**, 546,976 numerical byte readings and 136,749 selective-zero restorations. **Zero full ASCII outputs**, and no incomplete restoration searches. Six planted encryption/decryption controls passed.

These are source-derived classical-cipher trials, not AES/password trials. Unknown keys, other operators, binary intermediates and different ordering remain open.

Evidence: [scope](runs/2026-09-14_source_cipher_keys/manifest.json), [summary](runs/2026-09-14_source_cipher_keys/summary.json), [controls](runs/2026-09-14_source_cipher_keys/controls.json), [all prime-digit sum lists](runs/2026-09-14_source_cipher_keys/decimal_prime_matrices.json), [key vectors and source provenance](runs/2026-09-14_source_cipher_keys/keys.json).

## 4. Complete checkerboard matching with spaces and punctuation

Earlier source-passage searches emphasized letters-only forms and one/two prefix symbols. This pass covered **all 512 subsets** of the nine source symbols as possible two-character-token prefixes, in both orientations. Empty/all-prefix cases are included. **705** of the 1,024 directional constructions consume the entire field.

Those constructions were compared to full character windows within individual saved utterances, using exact text, lowercase, uppercase, letters with spaces, and letters only. A match must supply a complete bijection between tokens and characters; equality of a short prefix is insufficient. Across **671,349 eligible windows**, there were **zero complete matches**.

A held-out control with four prefix symbols, mixed case, punctuation and repeated spaces was recovered exactly at the correct source offset. Its one-character mutation was rejected.

This does not exclude homophonic substitution, a transposition or polyalphabetic layer, different source text, or other token grammars.

Evidence: [scope](runs/2026-09-14_formatted_checkerboard/manifest.json), [summary](runs/2026-09-14_formatted_checkerboard/summary.json), [complete model inventory](runs/2026-09-14_formatted_checkerboard/models.json).

## Consequence for the solve

The demonstrated zero-formatting gap is now covered within explicit, reproducible families. It did not explain the failure to decode FAED. Neither the 83/84 prime structure nor the off-white correspondence has been invalidated, and none of the unresolved fields or recovered decryptions has been classified as unimportant.

The next advance still has to connect the complete prime construction to substantial untouched data or a complete plaintext. These results do not authorize treating HILL, BTCSEED or IFINDO as a solved chain, nor assuming that a quotation must be a standalone AES password.

One arithmetic observation was retained separately rather than discarded or promoted: assigning the first 25 primes to all 25 special poster cells gives B=490, Y=497 and off-white=73. Yellow's RGB sum is also 497, but blue's is 339, so the same rule fails for blue. Other length equalities and the exact conditional subset count are recorded with their dependencies and post-selection caveats in [the observation file](runs/2026-09-14_offwhite_colour_totals/observation.json). They do not yet define a complete operation or a new password.

## Reproduce

Run from GSMG-CLEAN:

```powershell
python tools/solve_faed_lossy_hill.py
g++ -O3 -std=c++17 tools/search_lossy_hill_pairs.cpp -o tools/search_lossy_hill_pairs.exe
.\tools\search_lossy_hill_pairs.exe data/FAED_570.txt runs/2026-09-14_lossy_hill/pair_survivors.jsonl
python tools/restore_lossy_decimal.py
python tools/verify_lossy_hill_search.py prepare
.\tools\search_lossy_hill_pairs.exe runs/2026-09-14_lossy_hill/control_cipher.txt runs/2026-09-14_lossy_hill/control_pair_survivors.jsonl
python tools/verify_lossy_hill_search.py
python tools/solve_faed_source_keys.py
python tools/solve_faed_formatted_checkerboard.py
```

The C++ search reuses the previously controlled integer-bound helpers in `../read/SOLVE/bifid-numeric.cpp`. The independent Python check verifies all retained transforms; the full planted search checks that the prefix filter preserves a real complete message.
