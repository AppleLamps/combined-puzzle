# FAED tail: source provenance and explicit boundary tests

**Outcome: the missing instruction remains unidentified.** The final-region frequency change is present in historical source material, but this investigation does not establish a cipher boundary or recover a plaintext. All intermediate bytes remain available. No passwords were generated and no envelopes were tested.

## What the source establishes

The complete 1075-character wrapper agrees across the clean original, the saved Wayback capture marked **2023-06-01 22:27:52**, `read/salphaseion_page.html`, and the saved `salphaseion_live.html` copy. Some copies have identical file hashes and are not independent evidence. No new live fetch was performed.

The two Telegram exports were searched after removing whitespace and normalizing case. The complete 570-character FAED field appears in **PUZ #7360, 2021-04-16**, with no edit timestamp in this export. It is a solver post, not a creator confirmation. Nineteen messages contain the exact full field or exact 47-character tail. Images and attachments were not searched.

One concrete transcription problem was found: **PUZ #41743, 2025-05-30**, includes a 462-character version. An exact alignment inserts `i` at source offset 267 and deletes source offsets `[268,377)`: 109 omitted characters, for a net loss of 108. Its tail still matches. This demonstrates why a matching prefix/tail is insufficient to validate a copied input. It does not establish that everyone used that damaged copy, and our clean input is unaffected. Other prefix-only hits are retained in `source_trace.json` rather than treated as authoritative alternate originals.

## The statistical split is not an encoded delimiter

All offsets here are zero-based within FAED, with end-exclusive spans.

The maximum two-region symbol-frequency statistic still occurs at offset **523**, leaving 47 source characters. Under the proposed b/g two-character-introducer grammar, this cuts the `gb` token at `[522,524)` in half. Moving to 522 leaves 48 source characters and exactly 40 complete tokens. Moving the cut is an exploratory choice, not an instruction recovered from the page. Source offset 523 corresponds to wrapper offset 718; the original uses the same single-space separator between every character there.

The original test used 1000 character permutations. This follow-up uses **20,000 per null model**, seed 913264, and recomputes the maximum across every allowed split (at least 40 characters on each side) in every control:

| Control | Controls at least as strong | Empirical p | Monte Carlo standard error |
|---|---:|---:|---:|
| Shuffle individual characters, preserving all nine counts | 443 / 20,000 | 0.02220 | 0.00104 |
| Shuffle complete b/g tokens, preserving their counts and internal characters | 482 / 20,000 | 0.02415 | 0.00109 |

The second null is conditional on an unverified tokenization. These are sensitivity checks on the same observed sequence, not two independent discoveries. The larger character-control run remains above the original four-family threshold of 0.0125. Neither p-value is the probability that the puzzle is random, and neither proves the tail unimportant. The lead remains unconfirmed and retained.

## Test the apparent digest length instead of assuming it

DBBI's b/g parse has 64 tokens and exactly 16 distinct codes. An ordinary, consistently cased hex digest under a one-to-one token substitution can use no more than 16 codes. A shared substitution for DBBI and a FAED suffix can likewise use no more than 16 codes in their union.

| Conventional hex length | FAED suffix start | Distinct suffix codes | Distinct codes with DBBI | Result under this model |
|---|---:|---:|---:|---|
| 32, MD5 length | 531 | 12 | 18 | Separate alphabet possible; shared alphabet impossible |
| 40, SHA-1/RIPEMD-160 length | 522 | 13 | 18 | Separate alphabet possible; shared alphabet impossible |
| 56, SHA-224 length | 501 | 17 | 19 | Even a separate hex bijection is impossible |
| 64, SHA-256 length | 490 | 17 | 19 | Even a separate hex bijection is impossible |
| 96, SHA-384 length | 452 | 19 | 21 | Even a separate hex bijection is impossible |
| 128, SHA-512 length | 413 | 19 | 21 | Even a separate hex bijection is impossible |

For the nearby 40-token suffix, the two codes absent from DBBI are **`bi` and `bd`**. DBBI already uses all 16 possible hex identities, so these would require extra identities. This is an exact contradiction of the shared bijection model, not a readability score. Homophones, changing tables, transposition, non-hex representations or additional layers are different models and are not excluded here.

The 32- and 40-token suffixes were also tested as a narrow, independently substituted checksum of either the preceding FAED source or DBBI. Input representations were raw ASCII, the page's a=1 through i=9 decimal string, the corresponding whole decimal integer bytes, and a=0 through i=8 base-9 integer bytes. MD5, SHA-1 and RIPEMD-160 were tested. **24 full digest-pattern comparisons, zero matches.** The full positive checksum control passed. No partial digest matches count as results. The base-9 form is an explicit alternative, not a verified page encoding.

An exact-name search of the previously collected creator-message inventory finds no `SHA1`, `RIPEMD160` or `MD5` mention and one `SHA256` URL. This text search does not exclude indirect clues. The page itself demonstrably supplies `sha256` via `shabef`; the observed 40-token length alone supplies no source instruction to switch algorithms.

## Direct integer readings remain available

At both exploratory cuts, 522 and 523, the suffix was decoded using the page's decimal integer representation and the explicit base-9 alternative. None yields entirely printable ASCII. Some 20-byte decimal results decode strictly as UTF-16; these produce mixed unrelated scripts and private-use characters, with no recovered instruction. Successful Unicode decoding alone does not authenticate a plaintext. The exact hex and all successful strict Unicode decodings are preserved in `integer_outputs.json`.

The earlier verified checkerboard was inspected directly with the page's a=1 through i=9 mapping; it did not produce a coherent full instruction. Its historically unused cells cannot be assumed solved. This inspection is not an exhaustive rejection of modified checkerboards; those require their own justified tables and complete reconstructions.

## What this changes

Do not cut FAED at 523 or relabel its ending as a digest. The complete historical field is still the input to explain. A future model must specify its alphabet and boundary independently, account for every character, and produce a complete verifiable relationship. In particular, a proposed shared DBBI/FAED hex alphabet must address the two excess symbols rather than silently discard or merge them.

This pass does not supply the missing operation for the stronger complete DBBI b/be prime grammar. That remains separate from the weaker digest-shape interpretation.

## Reproduction and retained evidence

- `python tools/audit_faed_tail.py`: source-copy comparison, exact suffix inventories, digest comparisons, integer outputs and 40,000 control maxima.
- `python tools/trace_faed_tail_sources.py`: Telegram provenance and exact-name creator-hint search.
- `summary.json`, `split_profile.json`, `null_scores.json`, `digest_trials.json`, `integer_outputs.json`, `source_trace.json`, `community_copy_diff.json` retain the evidence.

Normalized FAED SHA-256: `066191b4aafc114fbca7f0d168382f40129c4ff18490375b689741081d5ef3c2`.
