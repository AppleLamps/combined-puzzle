# Assumption audit, 2026-09-13

No envelope opened. No private key found. This audit establishes a methodological false negative, not the cause of every solver's failure.

## 1. The current success rule can miss an intermediate answer (demonstrated)

`tools/check_candidate.py:check` treats a plaintext as notable only if padding is at least 3 bytes or a detected scalar matches Half/Better Half. In quiet mode, a correct plaintext with padding 1 or 2 and no final key produces no output and returns False.

`audit.py` constructs an 80-byte AES ciphertext using the existing GSMG profile and a known, readable 79-byte instruction. Decryption is byte-exact, with padding 1. The checker silently rejects it as non-notable. This is a synthetic control, NOT puzzle plaintext.

The same success condition appears in the recent last-words and matrixsum pipeline runs. Their aggregate reports retain neither full plaintext nor candidate provenance for those rejected outputs. Running the default checker without quiet does display previews, but still returns False and does not save these plaintexts.

Why this matters: the next envelope might hold instructions, another password, a transformed key, or another encoded stage. Matching the final addresses authenticates a terminal answer, but is not a complete detector of intermediate progress. The actual solved Phase 3.2 plaintext already demonstrates layered encoding. Creator message #39237 also calls yingyang the *next phase*, although that does not establish a particular envelope order.

A one-byte pad alone is not evidence of a correct answer. It is equally wrong to infer that a one-byte pad makes an answer incorrect. Padding length follows plaintext length, not correctness. A 79-byte plaintext in either short envelope necessarily has padding 1.

## 2. Bounded recovery of an actual run (completed)

I reran the existing `2026-09-13_last_words_referents/candidates.jsonl` through all four existing profiles and all three complete envelopes. No new candidates were generated.

- 188,112 decryptions.
- 750 pad-1 outputs and 5 pad-2 outputs, reproducing the prior report.
- All 755 retained in `all_padding_valid.jsonl`, with candidate, source, profile, envelope, and complete plaintext hex.
- Maximum ASCII/control-whitespace fraction: 0.556962. No output reaches 90%.

This recovers the information the report dropped. It does NOT expose a straightforward ASCII instruction in this set. No exhaustive decoding of these binary outputs was performed; ASCII fraction is descriptive and was not used to discard anything. Prior key-check results were not independently repeated here. There is no basis to claim that the missing solution was among these candidates.

Reproduce: `python runs/2026-09-13_assumption_audit/audit.py`. The existing checker self-test passes first, followed by the planted false-negative demonstration and the full bounded recovery.

## 3. An optional hash hypothesis is becoming a compulsory checkpoint

DBBI's bg parse yielding 64 tokens and 16 distinct symbols is an interesting, explicitly unproven hypothesis. An exact SHA-256 repeat-pattern match would be exceptionally strong evidence for a relationship. However:

- No match rejects that candidate under the particular digest/substitution model.
- It does not reject the candidate as an envelope password under other models.
- A billion unsuccessful checks do not establish that the assumed hash model is correct.

`08_SALPHASEION_RECIPE.md` goes further than this evidence supports when it makes the L5 relationship a prediction of the broader recipe reading and calls that reading falsified for a candidate with no match. The broad reading does not logically require DBBI to be a substituted digest. Keep L5 as a parallel check, not a prerequisite for progress.

The current `check_candidate.py` does test envelopes regardless of L5; this is a problem in the research interpretation, not an L5 early-return bug in that tool.

## 4. The source does not assign primes and zeroing to DBBI/FAED specifically

I reread original export messages #8000 and #8330. #8000 says prime numbers are required to proceed and that, "along the way," some characters need to be zeroed out. It opens by referring to the other-door hint. It does not name DBBI, FAED, a matrix size, an operation order, or deletion rather than replacement. #8330 likewise gives no operand.

Applying this advice to DBBI/FAED is a legitimate hypothesis, not an established instruction. Repeatedly exploring variants within that assumption does not test whether the assumed operand is wrong. Likewise, `matrixsumlist` does not by itself establish which adjacent block labels which operand or result.

## 5. What follows

The defensible diagnosis is that parts of the research measure final-key discovery while attempting to find an intermediate step, and promote plausible interpretations into constraints. This can make broad-looking searches much narrower than their trial counts suggest.

For subsequent runs:

1. Preserve every padding-valid plaintext with full provenance. Report padding validity, recognizable structure, and final-key matches separately. Do not promote padding alone to a solve.
2. State the actual operand and transform assumed by each hint interpretation. A negative result closes only that explicit model and candidate set.
3. Run L5 alongside envelope checks; do not require it.
4. Require a new proposed mechanism to explain substantial source material coherently, preferably by round-trip reconstruction or an independent downstream check, before expanding a sweep.

There is no evidence here that everyone shares one mistake, that these issues explain the entire multi-year stall, or that the puzzle must be sound because the creator says so. His #66589 explicitly acknowledges earlier rushed mistakes and the possibility he is still wrong. That possibility remains open, but this audit does not demonstrate a defective puzzle.

Scope: local clean-set documentation, relevant source code, selected original Telegram messages, one bounded candidate replay. Earlier ledgers and every historical run were not exhaustively reaudited. Existing puzzle sources and prior reports were left unchanged.
