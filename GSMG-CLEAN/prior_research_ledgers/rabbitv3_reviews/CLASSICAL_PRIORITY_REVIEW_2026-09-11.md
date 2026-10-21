The prioritized classical-cipher pass did not finish DBBI or FAED and did not open an unresolved envelope. It did produce a reusable stage screen, reproduce the disputed Cosmic output as a padding-only candidate, and test explicit color/prime/DBBI-derived constructions against whole-output language scores.

The complete run is in [results.json](E:/rabbitv3/rabbit/analysis/out/classical_priority_2026_09_11_complete/results.json). It supersedes the preliminary `classical_priority_2026_09_11` output for this experiment. Earlier files and other experiments are preserved. These are finite negative results, not a disproof of keyed fractionation.

**Measurements and corrections.** Fresh extraction from the native poster reproduces the 24-character URL and its 15 Blue / 9 Yellow least-significant bits. Under one-based byte numbering:

| Operand | Reproduced value |
|---|---|
| Blue byte indices | 1, 2, 3, 4, 6, 7, 8, 11, 12, 13, 14, 16, 17, 20, 23 |
| Yellow byte indices | 5, 9, 10, 15, 18, 19, 21, 22, 24 |
| Blue=1, Yellow=0 sequence | 111101110011110110010010 |
| URL characters at one-based prime positions | `sm.oeesle` |
| URL characters at zero-based prime indices | `mgi/sepad` |

The indexing distinction changes the prime claim. All colored cells occupy one-based positions 8, 16, …, 192, none prime. FEFEFE occupies **zero-based index 163, one-based position 164**. If zero-based indices make FEFEFE prime, eleven colored cells also have prime indices: 7, 23, 31, 47, 71, 79, 103, 127, 151, 167, 191. “No colored cells are prime but FEFEFE is” mixes conventions. This pass records both and does not select a convention from the desired result.

FAED's IC is 0.1180896001; g occurs 107 times in 570 symbols, giving z=5.8198 under an iid uniform nine-symbol model. Period-2-through-11 coincidence values are recorded; they range from 0.11783 to 0.12131. These measurements do not identify a cipher, exclude every substitution/checkerboard construction, or rule out a biased random source. The proposed keyed fractionation remains a hypothesis.

Both short envelopes contain 96 bytes total: 16 bytes of OpenSSL header/salt and 80 ciphertext bytes. PKCS#7 allows **64 through 79 plaintext bytes**. Exactly 64 ASCII hex characters is a useful review shape; length alone does not establish a digest or a pair of halves. Random valid padding has probability sum(256^-k, k=1..16), approximately 1/255. A single final 01 byte accounts for the 1/256 leading term.

The exported creator chronology also differs from the supplied timing claim. Message 4096 points to the poem at 2020-05-20 23:36:55 UTC; message 4105 says “First or zero” at 2020-05-21 06:12:59 UTC, 6 hours 36 minutes 4 seconds later. Both were subsequently edited in December 2025. This supports examining their relationship, but does not authenticate the present wording as contemporaneous. [Source context](E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:1061).

**What ran.** The [runner](E:/rabbitv3/rabbit/analysis/classical_priority_2026_09_11.py) records 33 source-derived numeric keys and 106 distinct 3x3, 5x5 and 6x6 boards. Inputs include parity, color counts and byte sets, both prime URL selections, `dbifhcega`, DBBI with prime-index replacement under both conventions, and the previously recorded full 61-value matrix constructions. Poster 3x8/8x3 matrices are declared hypotheses. All values, including the final e=5 in the conditional 84-token construction, remain represented upstream. [Inputs and board recipes](E:/rabbitv3/rabbit/analysis/out/classical_priority_2026_09_11_complete/inputs.json).

| Family | Cases | Scope and result |
|---|---:|---|
| Inverse Bifid | 16,544 | Raw DBBI, raw FAED, their concatenation, and keyed mod9/columnar FAED preprocessing; 15 bounded period choices, with duplicates removed. Every result re-encodes to its full input. |
| Numeric bridge, included in Bifid total | 5,500 | Three-by-three outputs become complete decimal-integer bytes before screening. Zero entirely printable results. |
| Nine-by-nine coordinate pairs | 1,064 | Adjacent/half pairing and two coordinate orders, mapped to ASCII 32–112. Printable by construction; no coherent text. |
| Ternary coordinate planes | 14,352 | Two trits per FAED symbol, then triples/periodic planes into a 27-symbol alphabet; 35 boards and 12 periods. All reverse checks pass. No coherent text. |
| Triangle row schedules | 148 | DBBI minus checkerboard with source-derived row shifts or within-row checkerboard rotations. |
| Triangle Pascal operations | 6 | Signed binomial coefficients, alternating coefficients and powers-of-two row sums. |
| Total classical transform cases | **32,114** | Counts include equivalent outputs from different recipes; they are not counts of independent hypotheses. |

DBBI serves as key material for the ternary family. FAED's 570 symbols give exactly 1,140 trits and 380 output symbols. DBBI's 182 trits do not divide into triples; this pass does not trim or pad them to force that packing.

Whole-output trigrams were trained on long alphabetic creator messages, excluding poem 1710 and without importing proposed plaintexts. Full candidates and their letter fractions are retained. The best Bifid FAED score was -4.3966, and the best ternary score -4.7312, versus -3.4574 for the held-out poem and -3.3589 for the readable checkerboard text. Inspection found no coherent instruction. Two hundred frequency-preserving shuffles per family produced scores exceeding each family's leader. These are post-selection diagnostics, not search-wide p-values. Encoded material in a genuine stage can also score poorly; there is no universal score cutoff here.

The triangle still has `YOUWONX` as row seven. None of the scheduled operators made the full 91-character output readable. All 26 Caesar shifts of each row are saved as diagnostics. Selecting a separate favorable shift per row has 26^13 freedom and would require independent evidence. Short rows also make an absolute claim that “no other row reads” ill-defined.

**Stage verification and exact assemblies.** The [stage verifier](E:/rabbitv3/rabbit/analysis/stage_verifier_2026_09_11.py) uses the existing frozen UTF-8 → SHA256 hex → EVP-SHA256 → AES-256-CBC profile. It distinguishes padding from review signals: exact 64 ASCII hex bytes, entirely printable text requiring language review, and a nested OpenSSL marker requiring parsing. None automatically means verified. No prize-address condition is imposed on intermediate stages. Every padding-valid byte string remains available to the caller.

Keeping binary data is necessary: the known 2,422-byte Phase 3.2 plaintext is only 59.8% printable and contains a nested envelope. A universal “English or 64 hex” gate would miss it. Printable gibberish also needs review rather than automatic acceptance.

The final AES pass used 56 distinct exact answers against SalPhaseIon, the Phase 3.2 nested Terminal envelope, and Cosmic Duality: **168 attempts, zero valid padding, zero review candidates**. Materials include the five full leaders from each classical family, exact already-solved page answers, and these explicit assembly diagnostics:

- Complete Phase 3.2 sections in source order: Architect plus checkerboard; introductory text plus those two; and introductory text plus Architect plus the full numeric checkerboard/instruction section. Separators were empty, LF or double LF; a separate lowercase-letter form was also tested.
- The exact exported poem, plus CRLF and final-newline variants. No phrase was silently normalized. Missing page answers were not invented; concatenating source sections is not proof those sections are intended answers.

The exact poem is 234 UTF-8 bytes, with no added final newline. Its SHA256 is `0499da8d2eb85062b529a71eb7ab305a4c8c87e830538b14d1f2b42953fb5c69`. The exported message was edited in April 2024, so this is a test of the current export, not authenticated original January 2020 bytes. [Exact poem](E:/rabbitv3/rabbit/analysis/out/classical_priority_2026_09_11_complete/exact_poem1710.txt), [all exact AES materials](E:/rabbitv3/rabbit/analysis/out/classical_priority_2026_09_11_complete/aes_materials.json).

Five [verifier tests](E:/rabbitv3/rabbit/analysis/test_stage_verifier_2026_09_11.py) pass. They check exact hex boundaries, non-verification of printable gibberish, newline-sensitive password bytes, all three known plaintext hashes, and the actual disputed Cosmic recipe. That recipe reproduces the 1,327-byte output using EVP-MD5 and the raw XOR password, including cancellation of the repeated matrixsumlist term. The new screen rejects it as a review candidate. This supports treating it as an unverified padding-only result; it does not logically prove that every possible binary interpretation is impossible.

Reproduction, from E:/rabbitv3, with a fresh output directory:

```powershell
python -m unittest discover -s rabbit/analysis -p test_stage_verifier_2026_09_11.py -v
python rabbit/analysis/classical_priority_2026_09_11.py --out rabbit/analysis/out/classical_priority_rerun
```

The prior repository already contained corrected inverse Bifid, numeric decoding, exact-hex/printable screens, and Pascal aggregate experiments. The new coverage is the explicitly enumerated boards, whole-output ranking and controls, row-dependent triangle operators, ternary packing, and the exact-byte poem/page assembly pass. Neither a completed classical stage nor the next required transformation has been established.
