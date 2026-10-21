# Creator hints and complete plaintext review

10 September 2026 — supplied Telegram export through 9 September 2026.

**Current assessment: the decoded instructions have not yet been connected to a verified envelope password.** This is the current interpretive report. Start with [current findings](E:/rabbitv3/rabbit/FINDINGS.md) for the short status; use the sourcebooks linked below for the complete evidence.

The strongest solving diagnosis is that several decoded clues have been treated as completed steps even though their instructions have never produced a verified result. We can read `matrixsumlist`, `lastwordsbeforearchichoice`, `thispassword`, and `enter`. We cannot yet demonstrate the matrix, the selected text, and the exact password construction that make those instructions open a remaining envelope. That missing connection deserves more attention than another collection of possible final keys.

This review recovered the full creator corpus, checked context, reproduced the established plaintexts, and examined how the instructions fit together. **It did not unlock a new envelope.** I cannot substantiate that any particular idea here has never been considered by another solver. The contribution is a complete, auditable evidence set and a clearer account of what is established, what was overinterpreted, and what remains unfinished.

## Current focus: the SalPhaseIon envelope

The selected target is the 80-byte ciphertext with salt `3ab585348552415d`. The complete original envelope is 96 bytes including its OpenSSL header and salt. **It remains locked.** This focused pass checks the interpretation of its own wrapper and tests exact password constructions against that ciphertext.

### Review of the supplied NotebookLM assessment

**The recommended sum-list/Architect experiment has already been performed.** The script constructs eight sum lists, five serializations (raw bytes, joined decimal digits, spaces, commas, and JSON), and 25 distinct Architect passage strings. Each list alone and followed by each passage gives 1,040 distinct materials. This includes all three serializations requested in NotebookLM's concrete test. Repeating that subset would add no coverage. [Implementation](E:/rabbitv3/rabbit/analysis/dbbi_faed_transform_2026_09_10.py:315), [saved results](E:/rabbitv3/rabbit/analysis/out/dbbi_faed_transform_2026_09_10/results.json).

The inventory is useful, but several conclusions exceed the evidence:

- **No delimiters does not mean one cipher.** The source leaves the relationship between DBBI and FAED unresolved. Separate ciphers need not carry headers.
- **Path A assigns the disputed roles again.** Zeroing DBBI, choosing 60 values, making a grid, taking sums and appending a quotation are hypotheses. Label order does not establish this recipe or justify “high” evidence strength. FAED's unexplained role is a gap in the proposal.
- **The reversibility column is incorrect.** Zero replacement, sums, text selection and SHA-256 generally discard information. AES is reversible with the correct key and IV.
- **Validation heuristics are not source facts.** SalPhaseIon has no established plaintext header, language or compression format. Text and decompression are useful checks; unfamiliar binary data alone does not falsify a candidate. The observed approximately 53% maximum printable fraction is a prior result, not a puzzle threshold. Padding alone does not verify success.
- **Finite failure does not force FAED processing or a different KDF.** It rejects the exact completed inputs under that convention. Different operands, parsing, selection, serialization or assembly remain possible. The SHA-256 EVP convention is reproduced for opened stages; SalPhaseIon has not confirmed it through an opening. Its 128 Base64 characters encode the full 96-byte envelope, including 80 ciphertext bytes.
- **Both DBBI parses already exist.** Demonstrating the 84-token branch does not falsify the 83-token branch; an independent constraint must distinguish them. Path B also needs an exact modulus, alignment, byte conversion and appended text before it is a reproducible recipe. Some arithmetic models were tested; transformed FAED combined with every possible text component was not.

The next useful question is **what relationship `matrixsumlist` specifies between the surrounding data**. A list might select positions from text or FAED rather than become literal password text; FAED might supply matrix data. These are interpretations to investigate, not findings or a solved recipe. This review adds no AES trials and no new plaintext.

### Latest reassessment: where the reasoning went beyond the evidence

**The main mistake in my approach was choosing the roles of the clues before demonstrating those roles.** The earlier Bifid correction fixed a testing defect. It did not answer the more important question: are these fields encrypted messages, matrix data, lookup data, selectors, or components of a later input? The source does not identify DBBI and FAED as independent encryption containers. No newly opened envelope is claimed in this reassessment.

Tracing the solved path shows a branching structure:

| Step | Demonstrated result | What it does not establish |
|---|---|---|
| Poster spiral → seed page → rebus answer | The URL, answer hash, and form route are captured | That every poster feature has been consumed |
| Causality → Phase 2; seven answer parts → Phase 3 | Exact known AES plaintexts reproduced | That every part is itself an envelope password |
| Three Phase 3 answers → Phase 3.2 | Exact outer plaintext, Architect message and checkerboard message reproduced | An opening of the nested terminal envelope |
| Phase 2 coordinate reading → Decentraland side clue | Strongly supported interpretation; creator names a nearby parcel | A fully reproduced four-stop route or the original audio decode |
| `HASHTHETEXT` → poster-caption hash → SalPhaseIon page | Exact hash matches the captured page address | The referent of every later hashing instruction |
| SalPhaseIon wrapper → readable labels | Reproducible binary/integer decoding | The operation that connects its unresolved data to an envelope password |

The two branches can carry information into each other. Reaching the SalPhaseIon page does not prove that the terminal envelope has been opened; reading an instruction there does not prove that the operation it names has been performed.

**1. An earlier clue already has a plausible navigational role.** I previously described X and Y in `# X 2 S H 4 Y 0 Q B 15 #` as unbound. Reading them as coordinate-axis labels gives four pairs, including `(-42,-16)`, near the creator's directly specified `(-41,-17)` parcel. Solvers described that relationship in 2021. The coordinate mismatch remains visible, but it is not sound to assume this strip must supply two missing final-cipher values. The full reconstruction and attribution limits are in section 4 below. [creator #1837](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:636>).

**2. The zeroing hint does not say “zero prime positions in DBBI.”** The creator says primes are required, then adds that some characters must be zeroed out “along the way.” That does not bind the operation to a particular phase, string, alphabet or index. My earlier prime masks were explicit experiments, but combining those clauses into a mandatory single operation was an unsupported inference. Both instructions remain important; their relationship is still unresolved. [creator #8000](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:1881>).

**3. The 60-value matrix construction depends on a prior choice.** The complete DBBI parser has two branches: 83 logical tokens leave 60 non-prime symbols; 84 tokens leave 61. Both account for every source character. The 60-value case was preferred because its marker prefix fits a special interpretation of the near-white poster cell. Therefore its attractive 2 × 30 and 4 × 15 dimensions are conditional evidence, not an independently established matrix size. Neither the 83-token reading nor the 84-token reading is a complete decode.

**4. The source does not put separators around “DBBI” and “FAED.”** The first 765 characters form one uninterrupted `a`–`i` field. The readable binary instruction `matrixsumlist` lies inside it at offsets 91–194. The first literal `z` comes after FAED. The 91/104/570 partition is useful and reproducible, but its existence does not identify two separate ciphers. `matrixsumlist` might act on preceding data, introduce following data, or direct an operation between them. The same prime parser does not simply extend across the whole field, nor across DBBI+FAED with the binary instruction removed. That rejects those two simple continuations; it leaves a missing operation or a change of representation, rather than providing a reason to reset a cipher automatically.

**5. Rejecting components by testing them as complete passwords can reject correct information.** I checked this against the puzzle itself. All seven real Phase 3 answer parts fail to reproduce its plaintext when hashed and tested individually; their exact ordered concatenation opens it. The three real Phase 3.2 answer parts behave the same way. That is **ten known-correct components that fail the isolated-password test**. Consequently, a failed AES attempt cannot distinguish a wrong DBBI/FAED derivation from a correct intermediate assigned the wrong role or combined incorrectly. The previous pass did test its eight sum lists with selected Architect passages, but that covers only those declared constructions, not every dependency implied by the wrapper.

I also checked for a simpler explanation: a copied character error. The export contains **56 full DBBI copies and 18 full FAED copies** matching the current strings under the declared prefix search. The one DBBI variant is explicitly described by its author as a rearrangement of `e` characters to force the matrix match. It is not evidence of a different original ciphertext. This supports our transcription without proving that the creator's original construction contains no error.

**The revised working model is an instruction-driven construction:** determine what the first field represents and what `matrixsumlist` produces; identify which text or data the next selector acts on; preserve the required serialization; then test the completed input. This is a research model, not a solved recipe. I am no longer treating a complete 83-token poster placement, a 60-value matrix, or “zero all prime positions” as mandatory prerequisites. The creator's 2023 hint still favors investigating colors/primes, the matrix sum list, and the Architect selector in that sequence, but it does not supply their operands or combination rule. [creator #8446](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:2208>).

The [source/dependency audit](E:/rabbitv3/rabbit/analysis/out/step_dependency_audit_2026_09_10.json) preserves the original messages with creator/solver attribution, both parser branches, field boundaries, full-copy witnesses and the solved-stage controls. [Reproduction script](E:/rabbitv3/rabbit/analysis/step_dependency_audit_2026_09_10.py).

### Previous transformation pass

**The concrete new finding is a defect in our earlier testing, not a recovered password.** The historical classical-cipher pass counted 412 transformations but made **zero AES attempts**. Its English-word screen ran before the nine-symbol intermediate data was converted into numerical bytes. None of that screen's target words can be spelled using only `a` through `i`, so those intermediates could never pass. A negative result from that log did not test the complete decoding chain. The [original log](E:/rabbitv3/rabbit/analysis/out/dbbi_classical.txt) is retained, and the [historical script](E:/rabbitv3/rabbit/analysis/dbbi_classical.py) now explicitly identifies this coverage gap.

The same script's `bifid9` function applies the **forward** Bifid operation: concatenate the coordinate rows and columns, then pair adjacent coordinates. The inverse instead splits the interleaved coordinate stream into two halves and pairs corresponding positions. This was checked against [GCHQ CyberChef's decoder](https://raw.githubusercontent.com/gchq/CyberChef/master/src/core/operations/BifidCipherDecode.mjs) and [encoder](https://raw.githubusercontent.com/gchq/CyberChef/master/src/core/operations/BifidCipherEncode.mjs), then verified with round trips. This is an implementation finding; it does not prove Bifid is the intended cipher.

**The corrected pass tested 58,292 distinct passphrases against the original SalPhaseIon envelope. No verified opening was found.** The test carried every generated numerical result through SHA-256 and the demonstrated AES convention; it did not require intermediate English and did not run a final Bitcoin-key search. Thus the old coverage error is real, but correcting it has not supplied the password.

### What the prime/color pattern does and does not establish

The 83-token DBBI parse still has its independently measured 23-marker prefix correspondence. I then tested a stronger necessary condition: could *all* poster color markers occur in order in the complete DBBI string, with `b` representing blue, `be` yellow, and other symbols retained as payload? The 48 declared models cover rotations, reflection, either traversal direction, and the near-white cell omitted or assigned either marker role. **None matched completely.**

This matters because **adding zero cells alone cannot repair a mismatch in marker order**. The old six-tokens/four-cells contradiction was not merely a reason to pad more cells. An intended complete correspondence would require a different transformation, marker rule, or interpretation of the data. This result does not reject arbitrary transpositions, alternative marker alphabets, or a later continuation. It does reject treating the present order-preserving prefix correspondence as an already reconstructed whole poster.

### A specific `matrixsumlist` connection was tested

Removing the 23 prime-position marker tokens from the 83-token parse leaves **60 one-symbol values**. That supports a bounded dimensional hypothesis:

| DBBI-derived arrangement | Output list | Possible FAED arrangement |
|---|---:|---|
| 2 rows × 30 columns | 30 column sums | 570 symbols = 19 rows × 30 columns |
| 4 rows × 15 columns | 15 column sums | 570 symbols = 285 adjacent pairs = 19 rows × 15 pairs |

This gives the intervening `matrixsumlist` a possible operation between DBBI and FAED. It is a hypothesis from the captured data, not a creator-confirmed matrix, and removing markers is not automatically the creator's zeroing operation. For example, filling the 4 × 15 matrix row by row with `a=1` through `i=9` gives the complete sum list:

```text
22,27,22,23,11,23,20,29,25,16,25,27,26,19,21
```

The pass constructed eight explicit matrices: two widths, two fill directions, with the two non-prime `b` values either retained or zeroed. It used their lists as repeating arithmetic keys and column-order keys for FAED. It also tested DBBI's raw values, the 60-value payload, the full 83-token values, and the prime-zeroed 83-token values as repeating keys. Adjacent and split-half FAED pairings received the 15-value keys in base 81. Each reversible operation passed an inverse check.

Finally, these eight sum lists were tested as password material, alone and followed by the nine previously recorded Architect text selections: five list serializations and 25 distinct passage strings produced **1,040 distinct inputs**. This tests the proposed wrapper composition for these matrices as well as the proposed DBBI-to-FAED transformation. None produced a verified opening. The archive contains every matrix, sum, key, byte string, and derivation.

### Corrected test coverage and result limits

| Completed family | Exact scope |
|---|---|
| Proper inverse 3 × 3 Bifid | DBBI, FAED, and the 60-symbol payload; forward/reversed source; all block periods from 1 through each source's length; three declared squares |
| Numerical decoding | Natural `abcdefghi` order and DBBI first-occurrence order `dbifhcega`; zero-based base 9, one-based decimal, and bijective base 9 |
| Zero operations | On raw/full-period streams: replace at prime/non-prime positions or prime/non-prime values; delete prime positions; insert zeros at prime output positions or before prime input positions. One/zero-based controls are specified in the archive |
| DBBI-to-FAED arithmetic | 12 explicit keys, addition/subtraction/Beaufort, moduli 9 and 10, two ordinal offsets and both key directions: 288 inverse-checked cases |
| Column ordering | Eight sum keys, both key/source directions, forward/inverse controls: 64 cases, also checked on a ragged example with tied key values |
| Paired FAED | Adjacent/split-half pairs, either coordinate order, four 15-value keys in either direction, three arithmetic operations: 96 inverse-checked cases |
| Envelope convention | ASCII lowercase SHA-256 hex passphrase; EVP_BytesToKey with SHA-256; AES-256-CBC; generated bytes and their byte-reversal control |

There were **4,474 distinct symbolic streams** and **29,146 distinct input byte strings**. All 221 padding-valid AES outputs had one padding byte. None was valid UTF-8, had one of the tested document/envelope headers, or successfully decompressed under zlib, raw deflate, or gzip. The maximum printable fraction was about 53%. One-byte padding is expected to occur by chance in this many wrong-key trials; it is not an opening.

The numerical review also distinguishes supplied text from recovered text: decimal lists, selected passages and the ASCII-offset pair control look printable by construction. One other 18-byte output crossed the permissive 80% printable threshold, but contains nontext bytes and no identified instruction; its exact bytes and failed envelope test are retained. It has not been labeled decoded plaintext.

Implementation controls passed: 63 Bifid round-trip cases, reproduction and inverse verification of the complete existing 5 × 5 `btcseed…` candidate, both established decimal-letter wrapper decodes, and the known Phase 2 AES plaintext hash and encryption round trip. These check the machinery. They do not prove the puzzle's intended square, numerical representation, zeroing rule, password composition, or later KDF.

**What this pass established:** corrected coverage for the declared Bifid, numeric and sum-key families. It did not establish that a whole-poster reconstruction or a DBBI-to-FAED transformation is mandatory. A further model must identify its operands and account for the data it uses; it need not satisfy the particular one-to-one marker model tested here unless it claims that model.

Reproduce this pass with `python rabbit/analysis/dbbi_faed_transform_2026_09_10.py`. The [script](E:/rabbitv3/rabbit/analysis/dbbi_faed_transform_2026_09_10.py), [results and controls](E:/rabbitv3/rabbit/analysis/out/dbbi_faed_transform_2026_09_10/results.json), [all symbolic intermediates](E:/rabbitv3/rabbit/analysis/out/dbbi_faed_transform_2026_09_10/symbol_streams.jsonl.gz), and [all input bytes and origins](E:/rabbitv3/rabbit/analysis/out/dbbi_faed_transform_2026_09_10/numeric_materials.jsonl.gz) preserve the exact scope. This section supersedes the interim counts from earlier runs of this pass; the separate 7,265-trial wrapper pass below remains a historical result.

### What the creator actually supports

- The creator explicitly describes progress in “salphation” and says that breaking it should give the feeling of the phase's name. That identifies it as a substantive stage. It does not establish the format of its output or the password. [creator #6497](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:1478>).
- The color poem sends solvers back to the first puzzle piece. Later wording explicitly requires prime numbers and says some characters need to be “zeroed out.” The creator does not identify their representation or positions there. [creator #1710](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:543>), [creator #8000](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:1881>), [creator #8330](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:2055>).
- The decoded 2023 binary repeats `yellowblueprimes`, `matrixsumlist`, `lastwordsbeforearchichoice`, then `yinyang` in that order. Its line breaks and division into steps are our interpretation. The creator points back to the community decode. [creator #8446](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:2208>), [creator #8483](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:2222>).
- “Hush hush” occurs after a question connecting SalPhaseIon to the color poem. This makes that referent worth examining, but there is no reply link and the question was edited later. [creator #6514](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:1506>). The AES-specific question behind the later “next phase” reply also has a later edit, so it does not settle which envelope must open first. [creator #39237](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:3748>).

These are the currently exported messages, including their edits. They support prioritizing the source data, primes and zeroing; they do not authenticate a completed `btcseed` decode or a particular collection of final passwords.

### Read the wrapper as instructions before choosing password bytes

There are paired encoding styles: `matrixsumlist` and `enter` are binary; `lastwordsbeforearchichoice` and `thispassword` are decimal integers encoded as letters; two partially decoded SHA expressions bracket the AES text. This is evidence of organization, not proof of seven password fields.

**`enter` has a precise local explanation:** it occupies the gap between two 64-character Base64 lines. Substituting a line break reconstructs the original envelope exactly; removing Base64 whitespace gives the same bytes. A formatting instruction is therefore a well-supported reading. This does not prove it has no additional role.

The final `sha256anstoo` can reasonably be read as “hash the answer too,” after the envelope has produced an answer. Under that reading, the first SHA expression prepares a password and the last prepares the result for its next use. This remains a hypothesis; the text does not prove that the next use is a URL. It gives no direct reason to invent a new salt-to-IV formula.

One testable recipe is therefore: obtain the matrix-derived material; select the intended words before the Architect's choice; concatenate the resulting answer material in source order; apply the demonstrated SHA-256 password convention; decrypt; then interpret the instruction to hash the answer. **The missing inputs cannot be replaced merely by the English names of their clues.** A further FAED-derived component may be required.

### Earlier wrapper-input pass

The test used nine named text boundaries, including the full sentence before “There are two doors,” its final clause, the phrase “beginning, and end,” the literal `choice` boundary, the Hope speech before Neo's last reply, and the puzzle rewrite's source-code/prime-basics clause. Each selected text is checked against its recorded source. Film passages come from the saved transcript and are possible referents, not creator-confirmed answers. “We won't” is retained only as a literal control; it comes after the presented choice.

Nine matrix models supplied 144 exact list byte strings: the observed binary poster and eight explicitly conditional prime-marker models already measured in the geometry audit. Word normalization produced 25 distinct byte strings. Selected words were tested alone and after those lists, using the earlier stages' ordered-concatenation/SHA-256 convention. A separate double-hex-hash variant tested an alternative reading of the suffix; five raw literal controls were also included.

**Result: 7,265 SalPhaseIon AES attempts; no verified opening.** All 21 padding-valid outputs had one padding byte. None was valid UTF-8 or had a tested document/envelope header or a successful zlib, raw-deflate or gzip decode. Every output and its derivation is retained; the absence of readable text alone does not prove that binary output is wrong. The known Phase 2 plaintext and encryption round trip passed as controls. No final Bitcoin-key search was used.

There is also a useful negative structural result. The existing community observation `91 = 7 × 13` and `570 = 15 × 38` suggests grids whose output lengths match the following labels. For four explicit row/column and direction arrangements, those labels **cannot both result from a shared weighted column sum modulo 26**, even allowing arbitrary values for all nine source symbols plus a common offset. The equations are inconsistent modulo 2 and 13; the ranks were independently checked with SymPy. This rules out that specific shared-sum model, including globally zeroing any chosen symbols within it. It does not rule out positional zeroing or another role for the labels. The dimensional observation and paired-encoding observation were already made by solver RB in export messages #12482 and #12501; they are not new creator hints.

The [exact source evidence, selected passages, matrix lists and all results](E:/rabbitv3/rabbit/analysis/out/salphaseion_focus_2026_09_10.json) and [reproduction script](E:/rabbitv3/rabbit/analysis/salphaseion_focus_2026_09_10.py) preserve this pass.

## What is now captured

The supplied JSON contains **61,418 messages**. Stable account ID `user9815232` identifies **492 direct creator messages**, all retained without dropping jokes, short replies, emojis, dot sequences, links, or media-only posts. Eighteen account service events are recorded separately. The catalog includes the July 2026 remarks as direct creator messages. There are also **324 creator-attributed forwards**; 36 distinct forwarded texts are absent from the direct-message corpus. These are preserved separately with their attribution limits.

| Evidence | Capture and verification |
|---|---|
| 492 creator messages | Original JSON objects, verbatim readable catalog, reply ancestors, and four neighboring messages on either side |
| 324 creator-attributed forwards | All retained, with a crosswalk of 139 distinct texts; 36 absent from the direct corpus; forward dates kept distinct from original dates |
| 18 creator attachments | Every file exists and was hashed; stills and animation frames were rendered and visually reviewed, including the animated fish sticker |
| 5 attachments in creator reply ancestry | Included separately, preserving the distinction between creator material and a solver's material |
| 6 forwarded media messages | Four distinct files, three additional to the previous media set, rendered and reviewed |
| 2 creator binary messages | Decoded and round-tripped: 161 ASCII bytes in #8446; 77 in #53342 |
| Original puzzle text | Poster URL; rebus/form information; every Phase 2 page riddle; exact known answer parts; decoded genesis headline |
| 3 opened AES envelopes | Fresh decryption from archived ciphertext, expected plaintext hashes, and encryption round trips |
| Inner classical ciphers | All 1,539 Architect letters and all 91 checkerboard letters independently reproduced |
| SalPhaseIon | All 1,075 non-whitespace characters assigned to 13 contiguous segments; exact reconstruction checked |
| Unresolved material | Full DBBI, FAED, three locked ciphertexts, full `btcseed…` candidate, and full `…YOUWON…` candidate |

The sourcebooks preserve the evidence even when this report gives a low priority to an interpretation. The source export SHA-256 is `829cfb0144a6030d5d9678e3a102f2177266f2abb55ff298492ae8392582234e`.

Forward attribution is weaker than direct-account attribution: only one forward includes the source account ID; 323 preserve only the display name `Jrk Bgrt`. Their original questions, dates and source chat are usually missing. Two forwards from a different account called “Double shot of Jameson for Jrk” were explicitly excluded. The forwarding user's surrounding remarks are not the creator's original conversation.

There are important limits to “all”: this covers this export, not deleted posts, private exchanges, or previous versions of edited messages. **244 creator messages carry edit timestamps; 22 immediate reply parents were edited after the creator's reply; eight immediate parents are missing.** These cases are listed, not silently reconstructed. UTC dates come from Unix timestamps, avoiding the old blanket five-hour conversion.

The established Decentraland transcription `HASHTHETEXT` is included but is marked inherited: I located the creator's screenshot and reproduced the caption hash/archived route, not the original audio decoding. Three video audio streams are digitally silent. The tumbleweed clip has nonzero audio; an automatic transcription was unreliable and has not been promoted to puzzle plaintext. Visual review is not an exhaustive steganographic examination.

## What the forwarded posts contribute

| Preserved statement | Connection and limit |
|---|---|
| “Same software was used in every phase.” | Relevant to encryption compatibility. A solver forwarded it when asked whether all AES blobs used standard CBC. This supports prioritizing the demonstrated software convention, but **same software does not guarantee the same mode, KDF or preprocessing**, and the original question is absent. [creator-attributed forward #33445](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/FORWARDED_CREATOR_POSTS.md:1129>) |
| “Checked the script for you today… I forgot the last details on how to solve it exactly…” | Testing a private solution script is different from proving that a stranger can reconstruct every step from the published clues. Together with the admitted `giveit/givetit` error, this means the creator's solvability assurances should not be treated as a proof of a complete public recipe. It does not demonstrate a second bug. [creator-attributed forward #24156](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/FORWARDED_CREATOR_POSTS.md:423>) |
| “No puzzle hints here, except maybe a tiny one in the music channel on slack for the rabbit phase.” | A real missing reference in the direct-only catalog. The named rabbit phase makes the already-required Logic song a natural connection; it does not establish that new music or an inaccessible Slack message is required now. [creator-attributed forward #28293](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/FORWARDED_CREATOR_POSTS.md:773>) |
| “Follow the white rabbit.” | Now captured as a forwarded statement, not silently assumed to be a direct post in this export. Its original scope is unavailable. [creator-attributed forward #11248](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/FORWARDED_CREATOR_POSTS.md:98>) |
| “It's hinted where it would be impossible to solve but you're not there yet.” | Retain this conditional wording. Without the original question and date it cannot prove either that today's frontier is impossible or that a particular envelope has already been solved. [creator-attributed forward #15783](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/FORWARDED_CREATOR_POSTS.md:150>) |

The missed hex message decodes exactly to **`Surebutwewontgiveitaway`**. That echoes “we won't give away the password” in the later reversed-bit hint and supports reading that portion as an encoded refusal/commentary, rather than automatically as another secret component. It is still not a demonstrated password. [creator-attributed forward #50656](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/FORWARDED_CREATOR_POSTS.md:2904>).

The older binary puzzle is also fully decoded now: join the two forwarded binary chunks, decode ASCII, reverse its opening question, apply Caesar -3 to the body, reverse the inner bitstream as `esrever` instructs, then decode the labeled Base64. It ends at the familiar Rickroll URL. The surrounding discussion identifies it as the preceding April Fools puzzle. **Its “second binary” instruction must not silently become a rule for the remaining AES envelopes.** The creator directly distinguishes the April 1 puzzle in [creator #325](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:105>); the related later forward admits the next puzzle would contain an actual private key. [creator-attributed forward #28033](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/FORWARDED_CREATOR_POSTS.md:705>), [creator-attributed forward #47269](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/FORWARDED_CREATOR_POSTS.md:2625>).

There is nevertheless a concrete reused technique: **whole-bitstream reversal works in both that earlier inner binary and the creator's 2023 binary hint.** More generally, the earlier puzzle teaches a pattern of decoding a wrapper, reading its instruction, then applying that instruction to the inner object. That is a grounded reason to investigate the SalPhaseIon wrapper as a sequence of operations. It does not justify reversing an AES ciphertext without a clue identifying it as the operand.

One forwarded company retrospective mentions the creator knowing “a bit of Pascal.” That is the **programming language in a coding-skills list**, not an explicit reference to Pascal's triangle or Harlan Brothers. It is relevant context for the recent link, but it does not connect the article's theorem to a lock. [creator-attributed forward #61385](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/FORWARDED_CREATOR_POSTS.md:3535>).

## 1. The SalPhaseIon text should first be read as instructions with referents

Its relevant sequence is:

```text
[DBBI, 91 letters]
matrixsumlist
[FAED, 570 letters]
z
lastwordsbeforearchichoice
z
thispassword
z
sha256ourfirsthintisyourlastcommand
[64 Base64 characters]
enter
[64 Base64 characters]
sha256anstoo
```

This is a normalized display, not an invented decryption of DBBI or FAED. Only the known binary/integer decodes and `bef → 256` in the SHA fragments have been substituted.

**The repeated error to avoid is turning each readable phrase into an independent password.** `This password` points to something. `Last words before…` selects something. `Matrix sum list` describes a structure or an operation. `Enter` occurs exactly where the two 64-character Base64 lines join. Those roles need resolving before concatenating or XORing hashes of the labels.

The adjacent `lastwordsbeforearchichoice` and `thispassword` make it reasonable to test whether the selected words supply a password. That is a grammatical inference, not a confirmed formula. The earlier `matrixsumlist` could label the preceding DBBI data, introduce the following FAED data, or describe a transformation between them. The current source does not settle that binding.

Two precise details matter:

- The text is **`ourfirsthintisyourlastcommand`**, not `yourfirsthint…`. Dropping `our` changes the referent. `HASHTHETEXT` is a plausible candidate for an earlier command, but the source has not identified it conclusively as *the* first hint intended here.
- There are **two SHA references**, with the second saying `anstoo`. A working interpretation should explain both: for example, hashing input material and later hashing an answer. That is a useful two-step model to test, not proof of a second hash or a URL. Treating `anstoo` as “answer too” remains an interpretation.

There is a more specific context link than simple word association: [creator #6514](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:1506>) says “Hush hush” after a participant asks whether SalPhaseIon relates to the “Roses are…” hint. That repeats the poem's final line. It makes the color poem / Hush-hush connection worth prioritizing when resolving `our first hint`. However, the creator did not use a reply link there, the response is hours later, and the question was edited years afterward. This is supporting context, not a verified instruction to hash the literal words twice. The useful distinction is **execute the hinted hashing instruction on its intended object**, rather than assume the English description itself is the password.

The `z` at the end of the first Base64 line must stay in the ciphertext. The embedded 40-symbol binary string decodes to `enter` and is removed from the Base64 reconstruction. This exact reconstruction is verified against the known SalPhaseIon ciphertext.

**Missing result:** one explicit chain specifying which data the labels refer to, what operation is performed, and the exact bytes delivered to an envelope. A set of familiar words is not yet that chain.

## 2. “Seven passwords” is less firmly established than it has been treated

The 2023 reversed-bit hint yields a continuous 161-letter string. An understandable reading is:

```text
yellow blue primes
matrix sum list
last words before archi choice
yin yang
we won't give away the password
it's in front of your eyes but you're not seeing it
very last step is a true giveaway promised
```

Those line breaks are editorial. The creator did not encode seven separated password fields. The first three expressions resemble intermediate operations or selectors; the fourth names a destination; the rest read naturally as commentary about solving. [creator #8446](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:2208>); the creator later points to the correct community decode in [creator #8483](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:2222>).

There is a separate “7 parts right?” message, but its conversation began with a question about the Phase 2 AES password. It fits the already-solved seven-part Phase 3 construction; it does not establish a seven-password formula for the final envelopes. [creator #1461](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:417>), [creator #1465](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:435>).

The Architect rewrite really does mention twenty-three ciphers, sixteen encryptions, and seven intertwined passwords. However, **23/16/7 already occur in the underlying film speech** as the people selected to rebuild Zion. The puzzle changes their roles while retaining the numbers. They are possible constraints, but not three independent mathematical discoveries and not an instruction to XOR seven hashes.

This also explains why the published Cosmic XOR claim cannot settle the puzzle: its recipe repeats `matrixsumlist`, so that term cancels under XOR. The 1,327-byte result is reproducible but has no independently verified meaning or continuation. A filename containing “verified,” a hash of that same output, and successful re-encryption do not establish that its password was intended.

**Missing result:** the puzzle must identify the actual components and combination operation. Neither the seven-line editorial segmentation nor the inherited film numbers supplies that operation.

## 3. The prime/color connection is substantial; the completed matrix remains missing

The strongest direct mechanical statements are the 2020 color poem, the later explicit statement that primes are required, and the instruction that some characters must be “zeroed out.” [creator #1710](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:543>), [creator #5966](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:1398>), [creator #8000](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:1881>), [creator #8330](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:2055>). These deserve more weight than isolated jokes about numbers.

The prior local audit found a useful, limited correspondence. A prime-position-aware reading of DBBI has two complete parses, of 83 and 84 logical tokens. Treating the poster's near-white `#FEFEFE` cell as an additional blue-role marker makes the **83-token parse match all 23 represented prime-marker colors**, leaving two poster markers. This is more specific evidence than a short accidental English substring.

But it does **not** complete `matrixsumlist`. The simplest placement rule—one token per cell in order, with only zero cells inserted between matching markers—fails at prime 79: six tokens must fit into four cells. That rules out that exact placement, not the entire prime/color connection. It also means the correspondence must not be advertised as a reconstructed board.

The next interpretation must distinguish:

| Role | Question that remains open |
|---|---|
| Index | Do primes identify logical positions, spatial positions, or values? |
| Marker | Are `b` and `be` blue/yellow labels at those positions, rather than numerical payload? |
| Payload | What happens to non-prime data, including the two non-prime `b` characters? |
| Zeroing | Which exact characters become zero, at what stage, and by what rule? |
| Sum list | Are the required totals rows, columns, regions, or another structure explicitly identified by the puzzle? |

A strong candidate should answer all five using the same input convention. Replacing `b` globally, choosing an eight-by-eight board merely because a greedy split produces 64 tokens, or adding arbitrary padding can destroy the prime-position evidence it was supposed to explain.

The Pascal connection remains a secondary geometry hypothesis. The two 91-letter strings fit a 13-row triangle; the known `YOUWON` substring starts at the seventh row boundary under that layout. Those are reproducible observations. The full row is `YOUWONX`, and the full left edge is `VOIDBOYCXVARX`; neither is a complete instruction. The [Harlan Brothers article](https://www.cut-the-knot.org/arithmetic/algebra/HarlanBrothers.shtml) concerns ratios of products of Pascal rows approaching *e*. It has not supplied a puzzle-derived finite password. Pascal row p also has zero interior coefficients modulo p when p is prime, a mathematically coherent connection to primes and zeroing. The puzzle still needs to identify the data and operation. Raw DBBI and its VIC difference are not ordinary Pascal coefficients under a fixed substitution; the poster also failed the 32 tested standard Pascal parity layouts (closest: 88 mismatches in 196 cells). These bounded results are retained below.

**Missing result:** a reproducible matrix construction with a defined zeroing rule, followed by the requested sum list. This is the most concrete unfinished operation to prioritize.

## 4. The original plaintext tells us to carry information forward

The known decryptions show that the original puzzle regularly combines outputs from earlier stages. Phase 3 opens using seven ordered answers, including mixed-case `SafenetLunaHSM`, the exact hexadecimal integer, and a FEN string that retains spaces. Phase 3.2 then uses three different answers. There is no universal “lowercase everything and remove all spaces” rule.

The Architect message then explicitly asks the solver to return to **“the source codes,”** carry code, and reinsert **“the prime basics.”** That language argues for reusing an existing artifact. It does not identify whether the carried object is the poster, an earlier numerical block, the classical plaintext, or a combination. We should require a proposed solution to name the object, instead of treating “return to source” as permission to try every film quote.

The Phase 2 numeric strip needs a correction to its assigned role:

```text
# X 2 S H 4 Y 0 Q B 15 #
...
Ok kid, on the highway, let put it in the worst gear.
```

Using the conventional riddle values `S=32`, `H=-42`, `B=-16`, and `Q=82`, the strip divides naturally into two equally sized rows: `X | 2,32,-42,4` and `Y | 0,82,-16,15`. **X and Y can be axis labels, not two missing numbers.** The four column pairs are `(2,0)`, `(32,82)`, `(-42,-16)`, and `(4,15)`. Solvers described this Decentraland route in 2021, including #5826, #5828 and #6608; it is not a new discovery. Their messages are preserved in the [dependency audit](E:/rabbitv3/rabbit/analysis/out/step_dependency_audit_2026_09_10.json).

The creator directly names `(-41,-17)` in [creator #1837](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:636>), in a Decentraland parcel conversation. That supports the geographic reading but leaves a real discrepancy from the calculated third pair `(-42,-16)`. The historical scene metadata in solver #16634 lists `(-41,-16)` and `(-41,-17)`, adjacent to that candidate point. The other destination descriptions vary between posts and have not been independently reconstructed here. **The coordinate interpretation is supported; a precise four-stop route is not verified.** Treating X/Y as necessarily unsolved scalar values, or this entire strip as necessarily unused final-password material, was unjustified.

The Q riddle also constructs the ten-column keyboard row `QWERTYUIOP` under digits `1234567890`, with I and W reading 8 and 2. That supplies a possible connection to the later checkerboard's “as wide as the first one seen.” This could give the same earlier riddle a second role. It does not turn the axis labels into unknown cipher keys.

There is also a useful caution about the highway wording. The creator's seed and highway emojis appeared while a solver was discussing the Logic song and the planted-flower answer. They may simply recall that earlier theme; they do not independently authenticate a reverse-gear cipher instruction in Phase 2. [creator #1210](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:389>), [creator #1211](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:396>).

**Current limit:** the coordinates and side-route interpretation deserve priority over inventing X/Y values, while the exact location discrepancy and the highway sentence remain unconfirmed. This block should not be used as evidence that a mandatory final cipher input has been skipped.

## 5. Read the Architect's meaning as well as its numbers

The text changes from a puzzle challenge into an appeal about what deserves effort: the thinker above, building something, and the relative value of the monetary prize. That makes the earlier Jacque Fresco answer part of the message's meaning, not merely a disposable password. The creator later distinguishes the BTC from other information and says the coins were only a small part of what he wanted to convey. [creator #9592](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:2480>), [creator #66592](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:4202>), [creator #66593](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:4216>). This establishes the creator's framing, not the truth of any claimed secret.

There are therefore two layers of interpretation to keep separate:

- **Actionable wording:** source codes, carry, reinsert primes, select, hash, enter. These require inputs and observable outputs.
- **Narrative purpose:** choice versus causality, uncertainty, the value of the prize, partnership, and the creator's broader interests. These may identify references, but a thematic match does not select a cipher automatically.

Some edits to the film are clearly worth retaining: speaker-like `YOU` and `ME`, “the function of the YOU,” “source CODES,” “prime BASICS,” and the added `SELF` near the end. They are more substantial than a misspelling. July's unusual “Give yourself yourself…” message echoes that vocabulary, but it answered a request for a bitcoin; it does not specify an extraction rule. [creator #66961](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:4477>).

Conversely, `FOURTY` has a direct creator reply calling it a typo. It should not be treated as a newly discovered 104/140 instruction because it differs from modern spelling. [creator #5960](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:1383>). The general typo disclaimer also exists. [creator #1806](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:629>). This does not require erasing deliberate substitutions, or treating every typo as deliberate.

The July 2026 “close friends” remark is now directly verified, followed 22 seconds later by “NOTE: that is a hint.” [creator #66573](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:4125>), [creator #66574](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:4132>). Read alongside the self-contained-solving statements, the restrained interpretation is that familiarity with the creator's interests or intended references can help recognize something already present. The claim does **not** establish that personal data absent from the puzzle is required. His 2026 “episode 3.5” remark is also retained; the series is not named there, so I have not silently converted it into a specific episode title or new key. [creator #60324](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:3971>).

**Missing result:** a selection rule for the deliberate substitutions and references. Their existence supports careful comparative reading; it does not validate a particular pronoun-based URL, book cipher, or private-key recipe.

## 6. “Ying yang” is a checkpoint, not a picture already found

The creator says that reaching it should make the remainder solvable the same day, later shortening that estimate to about two hours. [creator #9599](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:2522>), [creator #39224](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:3713>). The broad implication is that it is a recognizable transition or recovered stage. It is not evidence that merely noticing duality or a yin-yang cover completes that transition.

The book cover posted by barrystyle deserves retention: it visibly combines **Cosmic Duality** and a yin-yang image; the creator calls it specific and later says barrystyle supplied a specific hint. [creator #8311](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:2026>), [creator #8328](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:2048>). It is strong thematic evidence connecting the label and symbol. No cited creator message supplies a page/line/word indexing rule, so it is not yet a validated book cipher.

A frequently repeated stronger claim needs qualification: #39237 says it is the next phase, replying to a question whose current text asks whether it follows AES decryption. **That question was edited months after the reply.** We can quote the current exchange, but cannot prove that the AES-specific question had that exact wording when the creator answered.

That leaves the most defensible working expectation: open or otherwise reach a coherent next stage and look for a recognizable yin-yang transition. Do not discard a genuine-looking document, further ciphertext, or binary structure merely because it is not immediately a Bitcoin key. Equally, do not call random padding-valid bytes the checkpoint.

## 7. Context removes several attractive rabbit holes

| Fragment | What its conversation actually supports |
|---|---|
| “Would be nice, not required” | Fixing misspellings, not permission to omit a mathematical step. [creator #1729](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:577>) |
| “42” | An answer to how much math the creator put into the puzzle; not a fresh, fully specified operation. [creator #8385](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:2187>) |
| “ASCII 127” | A wordplay answer to which *character* to imagine being. DEL remains a testable interpretation, not a command with an identified operand. [creator #32613](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:3396>) |
| “ELI4.5 is meta” | Banter following an AI/ELI5 exchange; no basis for sending 4.5 through every cipher. [creator #66913](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:4393>) |
| “I'm working with many NOTES” | A reply to someone waiting for a “NOTE: that is a hint” moment. A musical or notebook interpretation is possible, not specified. [creator #66962](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:4484>) |
| “Couple hours, and no” | A reply asking how long creation took and whether he worked alone; not a promised solving time. [creator #70336](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:4600>) |
| “Some already found it” | In context, discussion of the claimed broader prize/information; not independent evidence of an opened AES envelope. [creator #66600](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:4244>) |
| Blockchain messages | The creator explicitly affirms they are not his and not part of the puzzle. [creator #12653](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:2727>) |

The creator himself agrees that ordinary jokes keep being interpreted as clues. [creator #32644](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:3424>). That is a reason to preserve context, not to discard all banter on sight.

The New Year sequence is preserved as five distinct dot messages, then the binary greeting containing “tiny hint.” A progression, triangle, countdown, or text-arrangement interpretation remains open. It is not a creator-confirmed Pascal instruction. The five-dot message also has a later edit.

## What is critically missing before an unlock can be claimed

The three remaining targets are intact:

| Target | Salt | Ciphertext bytes | Current status |
|---|---|---:|---|
| Phase 3.2 nested / terminal | `b45a5e3d827593ca` | 80 | Locked |
| SalPhaseIon embedded AES | `3ab585348552415d` | 80 | Locked |
| Cosmic Duality | `2d3f6fe06dc950e6` | 1,328 | Locked |

The verified earlier convention is AES-256-CBC, an OpenSSL `Salted__` envelope, and EVP_BytesToKey with SHA-256, using the lowercase hexadecimal SHA-256 of the answer as the passphrase. Known-answer reproduction establishes that convention for the opened stages; it does not independently prove every later stage uses identical preprocessing.

All three locked envelopes are valid targets for a clue-supported candidate. Their required opening order has not been established. The following is a proposed research sequence, not a demonstrated dependency chain:

1. **A fully specified interpretation of the prime/color/zeroing instructions.** State the input, logical positions, special-cell handling, exact zeroing operation, and how every relevant source character is accounted for. Reject a construction when it needs an unexplained exception, such as the failed six-tokens/four-cells placement.
2. **The resulting matrix and sum list.** Publish the actual board and totals. Do not mark this task complete because a cipher output begins with an English label.
3. **A justified referent for “last words before archi choice.”** Specify whether the source is the film dialogue, the puzzle's rewritten speech, or another supplied text; identify the exact occurrence of choice and the range selected. “The last words” is still ambiguous until that is done.
4. **A password construction that explains the wrapper.** Account for `thispassword`, the first-hint/last-command phrase, `enter`, and `sha256anstoo`; document which parts are instructions and which are data. If FAED is involved, verify the complete transformation rather than its seven-letter prefix.
5. **A coherent envelope result.** Preserve all bytes. Look for a readable next stage, a recognizable encoded object, or another independently checkable structure. PKCS#7 padding alone is insufficient; a Bitcoin-key-shaped result is not the only acceptable outcome.

The creator's “you have all the info,” repeated no-internet statements, and confirmation that the puzzle remained valid after the site went down favor work on the captured material. [creator #9607](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:2552>), [creator #9639](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:2671>), [creator #16624](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:2799>), [creator #63957](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md:3999>). They do not prove that our present interpretation of that material is correct.

**My current assessment:** the immediate gap is assigning the instructions to the correct objects and establishing their dependencies. The prime/color pattern is useful evidence, but a required full-poster reconstruction, an obligatory DBBI-to-FAED cipher chain, and prime-position zeroing are still model choices. Testing those choices did not establish them. The next interpretation must state which operation acts on which data, which output is carried forward, and how the complete password is assembled.

## Tested interpretations

These are completed, bounded experiments. Their negative results do not eliminate every interpretation of a clue. The current transformation pass is documented in the SalPhaseIon focus section above; earlier experiments remain below with their original scopes.

| Tested family | Scope | Result and preserved record |
|---|---|---|
| Prime/color marker sums and residual DBBI payload | 163 materials; 489 password byte strings; 978 AES trials per locked envelope, 2,934 total | No verified opening. Ten padding-valid outputs retained, including one two-byte-padding SalPhaseIon result. [Exact geometry, methods and outputs](E:/rabbitv3/rabbit/analysis/out/instruction_chain_audit_2026_09_10.json) |
| Triangular rows, Pascal weights, sums/products, edges and row-product ratios | 117 materials; 351 password byte strings; 702 trials per locked envelope, 2,106 total | Nine one-byte-padding outputs; no verified opening. [Full calculations and outputs](E:/rabbitv3/rabbit/analysis/out/pascal_link_review_2026_09_10.json) |
| FAED pairs selecting a 19 by 81 source-text layout, related matrix materials, and the DBBI/VIC difference | 4,832 materials; 29,184 direct AES trials, then 1,488 envelope-continuation trials | No verified opening. This tested a proposed layout, not an established cipher. [All derivations and padding-valid bytes](E:/rabbitv3/rabbit/analysis/out/sourcebook_envelopes_2026_09_10.json) |
| Checkerboard/Bifid bridge | 72 materials; 432 AES trials | No verified opening. [Measurements under `checkerboard_bifid_bridge`](E:/rabbitv3/rabbit/analysis/out/connection_audit_2026_09_10.json) |

The `btcseed` Bifid prefix is reproducible and remains an unresolved candidate. The shuffled-square experiment is conditional on its particular search family; its frequency is not the probability that the intended solution has been found. Neither dismissing the entire result as coincidence nor calling it solved is supported. The [complete candidate and its method](E:/rabbitv3/rabbit/evidence_review_2026-09-10/PLAINTEXT_SOURCEBOOK.md) remain available.

The numerical `479/484` imbalance and a chosen zeroing of 5 do not establish a solved yin-yang stage or a universal password rule. The DEL construction is also a hypothesis with an unidentified operand. Older experiment scripts may encode these assumptions; their output is historical test data, not current solving instructions.

## Evidence files

- [All 492 creator messages, with immediate reply context](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/CREATOR_MESSAGES.md>)
- [Complete plaintext sourcebook](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/PLAINTEXT_SOURCEBOOK.md>)
- [All 324 creator-attributed forwarded posts](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/FORWARDED_CREATOR_POSTS.md>)
- [36 forwarded texts absent from the direct corpus](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/FORWARDED_ONLY_TEXTS.md>)
- [Decoded hex sentence and complete earlier binary-puzzle chain](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/FORWARDED_DECODED_TEXT.md>)
- [Forward attribution and deduplication manifest](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/forwarded_manifest.json>)
- [Export manifest and missing/edited reply audit](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/manifest.json>)
- [Original creator JSON objects](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/creator_messages_raw.json>)
- [All reply ancestors and neighboring-message contexts](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/creator_contexts.json>)
- [Plaintext methods, byte counts, hashes, and AES parameters](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/plaintext_manifest.json>)
- [Full New Year dot/binary sequence](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/NEW_YEAR_SEQUENCE.md>)
- [Media descriptions, captions, and limits](<E:/rabbitv3/rabbit/evidence_review_2026-09-10/MEDIA_REVIEW.md>)
- [Prime/color geometry and bounded envelope checks](<E:/rabbitv3/rabbit/analysis/out/instruction_chain_audit_2026_09_10.json>)
- [Pascal calculations and bounded envelope checks](<E:/rabbitv3/rabbit/analysis/out/pascal_link_review_2026_09_10.json>)
- [Sourcebook extraction script](<E:/rabbitv3/rabbit/analysis/build_creator_sourcebook_2026_09_10.py>)
- [Plaintext reproduction script](<E:/rabbitv3/rabbit/analysis/build_plaintext_sourcebook_2026_09_10.py>)
