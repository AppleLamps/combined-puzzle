# Whole-puzzle review — 13 September 2026

The review found no new verified puzzle stage, private key, or opened lock. It did find a reproducible acceptance-filter blind spot, a mislabeled local plaintext, and several useful distinctions between real clues and conclusions added by earlier analyses. The best remaining work is to derive a complete intermediate result from the original instructions, with the three remaining ciphertexts available as checks. Repeating large lists of guessed passwords is weak evidence of progress.

## Scope and source order

I reviewed the active original-artifact reference, the older desktop findings and their retractions, the creator/forward/plaintext/media sourcebooks, the September 12 creator-context and workstream reports, the archive/Decentraland recovery report, the address review, the original poster and rebus images, selected original Telegram threads, and substantive recent solver messages. I inspected relevant test implementations where their reported conclusions mattered. This is not a claim to have manually read every line of every historical program output or independently searched every media attachment for hidden data.

The primary research copies are in `E:/rabbitv3/rabbit`, `E:/rabbitv4/rabbit`, `E:/rabbitv5/rabbit`, `C:/Users/lucas/Desktop/rabbit`, `C:/Users/lucas/Desktop/read`, and `C:/Users/lucas/Desktop/gsmo-links`. These are overlapping copies, not independent corroborating sources. The older desktop FINDINGS file contains explicit retractions; the September 12 workstreams include completed tests that earlier recommendation lists still describe as future work.

Authoritative starting points:

- [Original artifact reference](E:/rabbitv3/rabbit/GSMG_COMPLETE_PUZZLE_REFERENCE_2026-09-10.txt)
- [Exact plaintexts and segments](E:/rabbitv3/rabbit/evidence_review_2026-09-10/PLAINTEXT_SOURCEBOOK.md)
- [September 12 completed workstreams](E:/rabbitv4/rabbit/analysis/leads_2026_09_12/RESULTS.md)
- [Archive and recovered audio report](C:/Users/lucas/Desktop/gsmo-links/deep-research-2026-09-12/REPORT.md)
- [This pass's executable audit](C:/Users/lucas/Desktop/read/PUZZLE-REVIEW/audit-puzzle.cjs) and [results with original message contexts](C:/Users/lucas/Desktop/read/PUZZLE-REVIEW/audit-results.json)

## 1. A real blind spot in the latest decryption reports

The September 12 `harness.py` labels a candidate a hit only when its post-first-block plaintext is over 90% printable or meets a lowercase-hex shape. Its known Phase 3.2 self-test merely asserts `cls is not None`. Any valid padding classification satisfies that assertion, including a result that would not count as a hit.

I independently decrypted all three known envelopes from the local page and nested ciphertext using the established answer inputs. All three plaintexts exactly match the original-artifact reproduction and its hashes:

| Known stage | Plaintext bytes | Newer harness classification | Counted as hit? |
|---|---:|---|---|
| Phase 2 | 648 | PRINTABLE | Yes |
| Phase 3 | 4,090 | PRINTABLE | Yes |
| Phase 3.2 | 2,422 | **pad10** | **No** |

The real Phase 3.2 result is only 59.52% printable under that harness's post-first-block metric. It contains an actual mixed binary/text stage. The claimed positive control therefore checks padding, not successful recognition of a genuine stage.

Relevant implementation: [classification](E:/rabbitv4/rabbit/analysis/leads_2026_09_12/harness.py:33), [hit/retention gate](E:/rabbitv4/rabbit/analysis/leads_2026_09_12/harness.py:81), [weak self-test assertion](E:/rabbitv4/rabbit/analysis/leads_2026_09_12/harness.py:118).

Consequences are limited but important:

- “Zero hits” means no accepted printable/hex outputs under those assumptions; it does not exclude every correct binary intermediate.
- Non-hit padding lengths of at least two are saved, so the known pad10 control is not wholly lost. Non-hit pad1 outputs are discarded, and the saved candidate material is truncated to 200 bytes.
- This does not establish that a discarded candidate is correct. Random padding is common and must not be promoted into a discovery.
- The older September 11 stage verifier already explicitly retains binary candidates and documents this concern. The newer harness does not carry that distinction through to its reported positive control.

**Worth checking next:** use the existing binary-aware verifier for any evidence-led candidate, retain exact password bytes and complete plaintext, and require a nested structure, reversible decode, known digest, or dependent-stage check. Do not rerun millions of guesses merely because this filter has a blind spot.

## 2. The local Phase 3 plaintext is not the verified plaintext

`C:/Users/lucas/Desktop/read/phase3_plaintext.txt` contains 4,095 bytes and begins with non-text bytes. It is not the actual 4,090-byte Phase 3 plaintext. I did not infer how this file was produced.

The reproduced plaintext begins “What if the merovingian is wrong.” Its SHA-256 is:

`c4ad94559a44a927c1032cc0e024515f9510a0806a2d14458dbf4a360af9865f`

An exact verified copy is saved as [phase3-verified.txt](C:/Users/lucas/Desktop/read/PUZZLE-REVIEW/phase3-verified.txt). The existing file was retained as evidence. This matters for any future hash, character-position, or source-text analysis; the filename alone was misleading.

## 3. DBBI–VIC remains a concrete structural lead

Using the exact 91-character DBBI stream and the exact 91-character decoded checkerboard message, subtract letters modulo 26 with A=0. The result is:

```text
VOZIJBDTIQBRGVEOMZNBCYOUWONXCPKWGBNAXDGJGDUNNVMPABTAFPAAXMJYLZBUWERDNXYDESKUOBXCAMVDJLQTSGA
```

Reproduced facts:

- Positions 1, 4, 21 spell VIC.
- Positions 22–27 spell YOUWON.
- There are exactly 64 letters after YOUWON.
- Their concatenated A1Z26 values contain 103 digits, matching the 103-letter source-order instruction concatenation. The five digits opposite `enter` are 13224.
- Among 364 simple models (91 rotations, forward/reversed checkerboard, add/subtract), only the natural unrotated subtraction contains YOUWON.

This is established community material, not a newly discovered payload. The fresh contribution is the independent direction/alignment check and a narrower interpretation of the statistical claim.

The selected-word frequency-preserving null gives approximately 3.38e-6 for the required six source letters at the compatible position. That is **conditional on having selected YOUWON and the model after observing it**. It does not account for the historical search over words, operators, transformations, or interpretations. The earlier wording “not chance” is unjustified. The {1,4,21} hint's April Fools context also cannot be ignored.

**Worth checking next:** a single reproducible operation that explains the whole 91-character object or the complete tail and then yields a verifiable next object. Require the method, orientation, and parameters to come from the source. Do not cherry-pick six good letters or turn 64 alphabetic letters into hex through an arbitrary alphabet. Existing zeroing, prime selection, letter maps, and direct key/password uses have already returned negative results.

The creator's “Pfff. Coincidence.” (#70307) follows the later 103-digit/Executive Order argument. It is not a clear confirmation of that argument; neither is it an explicit disproof of every DBBI–VIC relationship. Keep those claims separate.

## 4. The source gives an operation-and-input problem, not a proven password list

SalPhaseIon's exact source order is:

```text
DBBI (91 unresolved characters)
matrixsumlist (decoded binary label)
FAED (570 unresolved characters)
lastwordsbeforearchichoice (decoded decimal-integer label)
thispassword (decoded decimal-integer label)
sha256 our first hint is your last command
[two Base64 lines separated by the decoded word enter]
sha256 ans too
```

The creator's #8446, independently decoded here by reversing the entire bitstream, starts:

`yellowblueprimes → matrixsumlist → lastwordsbeforearchichoice → yinyang`

The order of the text is real. It does not by itself prove an execution order, tell us what constitutes the matrix, identify the last-word boundary, or equate yinyang with the Cosmic ciphertext.

The 84-token DBBI prime/color hypothesis is still a candidate with multiple constraints: 23 markers partition into 16/7, and all 61 remaining values must survive, including the final e=5. This is stronger than simply noticing a convenient rectangle, but color meanings and parsing are still assumptions. The final value must not be dropped to force a 60-cell board. The near-white/marker bit changes produce DEL only under a specified operation; DEL does not automatically instruct a deletion. These are existing, explicitly qualified findings in the [reinsertion review](E:/rabbitv3/rabbit/analysis/out/reinsertion_constraints_2026_09_11/REPORT.txt).

**Worth checking next:** derive a complete sum list from an independently justified parse/geometry, then use it as a selector into a precisely fixed source for `lastwordsbeforearchichoice`. Preserve every source symbol, fix index base before looking at the output, and make the full extracted result the test. A new source-selected rule is valuable; another arbitrary matrix orientation plus a password hash repeats old work.

## 5. The terminal block is not confirmed as the SalPhaseIon gateway

Unedited creator #8569 answers three consecutive questions with “Correct / No / Can't say anything about this.” In context, the natural point-by-point reading is:

1. The final Phase 3.2 block is not decrypted: correct.
2. That is where the requested SalPhaseIon hint is: no.
3. Norton and the X/Y strip are pointless: cannot say.

This is useful evidence against requiring the terminal lock to supply the missing SalPhaseIon hint. It does **not** prove the branches have no later dependency or that the terminal is irrelevant to the prize.

**Worth checking:** keep a separate dependency record for the terminal's nearby checkerboard/“half and better half” text and the SalPhaseIon wrapper. An output from either can later connect them, but do not assume they form a linear queue. Literal Norton/X-Y phrases, pairs and selected triples have already been tested extensively.

## 6. Looking Forward is a plausible referent, not an authenticated book-cipher recipe

The March 2026 exchange links Fresco, a participant's suggestion to read Looking Forward, gnomad, the phrase about seeing what is in front of one's eyes, and the creator's “Bingo.” However, “Bingo” has no explicit reply pointer, the intermediate gnomad message was edited the next day, and the relevant X message was edited months later. The current text supports attention to the discussion; it does not uniquely pin the book as a character-index source or a password.

The previous workstreams already tried book sentences, chapter endings, text before choice words, and roughly 1.35 million n-gram materials. Their no-hit result has the filter qualifications above, but repeating the same title/phrase guesses would add little.

**Worth checking only with a new selector:** an exact edition and a source-grounded rule selecting its text. The broader source also presents social/philosophical material as a prize, so a recommended book need not be a mechanical cipher instruction.

## Leads to keep low priority

- **661 → 121 → 91:** the counts are correct; the creator said “I don't know right now,” not yes. Prime selection, 11×11 sums, comparisons with DBBI/VIC and subsequent transforms were already tested.
- **13224 and the passport date:** the string alignment is real; the Executive Order interpretation is not independently required and was met with “Coincidence.” Date and order-derived trials are already extensive.
- **MS Paint palette / mixed colors:** pixel colors can identify an editing convention without identifying a decoding instruction. The existing tests cover many recoloring and traversal variants. Those negatives do not prove no other visual use exists.
- **BIFID btcseed, BE MODEST → BULLSHIT, and short readable fragments:** a chosen key or selected prefix can manufacture plausible words. Demand source provenance for the key and a full-output explanation. The recent BE MODEST post itself asks where its Vigenère key came from.
- **SalPhaseIon naming/salt wordplay:** possible wordplay does not select a cipher or KDF. A recent claim that “zout” is German is an obvious provenance warning (it is Dutch); no cryptographic operation follows from it.
- **New Year dots, ASCII 127, {1,4,21}, color jokes:** retain exact context and edited dates. Do not combine individually ambiguous remarks into a supposedly confirmed recipe.
- **Salts and cipher mode:** Salted__ is a container signature. Neither that prefix nor a length divisible by 16 proves a particular AES mode, KDF, randomness source, or that salt bytes cannot be intentional. The opened stages strongly support a conventional pipeline; the locked stages remain hypotheses until opened.

## What is already resolved and should not be re-searched as missing

- Three opened envelopes are reproducible from exact answer inputs. This pass checked their complete hashes, not just padding.
- The prior missing Decentraland-audio bridge was recovered in the later September 12 archive work: channel subtraction exposes HASHTHETEXT, and the normalized poster text hashes to the known 89727c… route. The older September 10 reference's missing-audio note is stale relative to that package. This pass reviewed the recovery evidence; it did not independently redo the spectrogram experiment.
- Historical HTTP 200 responses at arbitrary paths often contain the same generic app shell. They are not verified new puzzle pages.
- The earlier local key-check checksum errors were corrected in the prior review's independent candidate recheck. That does not invalidate the separate, correctly implemented HASH160-based oracle in older research copies.

## Suggested next investigation

Prioritize a source-defined, reversible DBBI/FAED operation that explains the entire result and yields a selector or instruction. Keep the DBBI–VIC alignment and the fully retained 84-token/color hypothesis as distinct candidates, not two proven steps of one chain. Test any resulting exact answer with a verifier that retains binary stages. Keep the terminal dependency open but do not require it to provide the SalPhaseIon hint. Only return to the book, dates, palette, or alternate KDFs when a newly derived instruction selects them.

No new puzzle solution is claimed. The demonstrated changes in this pass are improved evidence boundaries, an independently reproduced structural relation, a real test-gate defect, and a verified replacement copy for a misleading local plaintext file.
