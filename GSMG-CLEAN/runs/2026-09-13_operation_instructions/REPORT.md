# Search for an instruction specifying the missing operation

**Result:** explicit operation language exists, but this review did not find an instruction that uniquely maps DBBI to FAED, identifies the characters to zero, or supplies a complete matrix recipe. No new cipher, password, or envelope result is claimed.

## The strongest instructions, with their actual limits

1. **Original decrypted Architect text:** `RETURN TO THE SOURCE CODES ... REINSERTING THE PRIME BASICS AFTER WHICH ... SELECT FROM OVER TWENTY-THREE CIPHERS SIXTEEN ENCRYPTIONS AND OR SEVEN INTERTWINED PASSWORDS`. Reinsertion and selection are explicit verbs. Prime-number replacement in DBBI is a supported hypothesis because the complete 84-cell parse has the corresponding 23/16/7 structure. The passage does not identify signs, grid dimensions, sum axis, or FAED as the target. Even “reinsert prime numbers” is an interpretation of “prime basics,” not an exact quotation.

2. **PUZ #8000, creator, 2021-12-26:** `some characters need to be 'zeroed out'`. This is an explicitly announced hint (#7998), alongside the statement that primes are required. It is the clearest remaining transformation instruction. However, “furthermore, along the way” does not assert that the prime markers are those characters or specify ordering relative to reinsertion. Replacement by numeric zero, digit o, NUL, deletion, and masking are distinct models. Zero is an operator clue; its operand and representation are missing.

3. **PUZ #1710:** `Go back to the first puzzle piece`. Together with `Yellow has a number and so does Blue`, this points to an earlier source rather than authorizing arbitrary new arithmetic. It does not specify a matrix operation on FAED.

4. **SalPhaseIon:** `ourfirsthintisyourlastcommand`. The creator-attributed forward #11248 answers a question about the actual first hint with `Follow the white rabbit`. Original COMM messages #28522, #35283 and #36714 independently establish his use of that instruction. This strengthens the referent, but does not establish whether the command means following the poster's path, returning to an image, extracting by colour, or supplying literal text. It cannot yet choose a FAED operation.

5. **Original Phase 3.2:** `Raising the stakes without extra chances of winning ... on a sad board but as wide as the first one seen`. This occurs immediately beside the checkerboard material. Its unresolved wording should be retained, but transferring its width or interpreting “raising” as exponentiation requires evidence. It is not a uniquely specified next FAED instruction.

## Context checks that prevent false instructions

- **PUZ #1837, `Only -41,-17 matters`:** the preceding messages #1835–1836 explicitly ask about a parcel and interactive mode in a game. This is contextual evidence for coordinates, not a rule assigning negative signs to the b/be primes. There is no reply link, so context is the basis for this reading.
- **COMM #26083/#26108:** the creator really does specify reversing the second binary code. But he explicitly explains the already solved April 1 side puzzle. This is a genuine operator with an identified operand in a different puzzle, not evidence to reverse FAED.
- **PUZ #66961:** `Give yourself yourself and yourself will be given yourself` immediately follows a request for one bitcoin. #66962's NOTES message replies explicitly to a solver asking for a NOTE hint. Neither specifies self-XOR or a music cipher.
- Checked comments/script tags in all six saved original page HTML files. No additional FAED operator appeared in the puzzle comments. Wayback scripts and the trading site's application configuration must not be treated as puzzle instructions merely because their text contains arithmetic vocabulary. External script/media contents were not exhaustively decoded in this pass.

## Consequence

The missing instruction is not established. The strongest bounded research question is now **which characters the explicit zeroing instruction refers to, and in which representation**, rather than which arbitrary cipher to try. DBBI's prime structure supplies candidate positions but does not authenticate them as the zeroing mask. A proposed mask must explain an additional exact relation or plaintext, including its treatment of the b/be colour discrepancy; producing a convenient word after freely chosen signs/moduli is insufficient.

The prior label comparison already tested prime-zero ordinary matrix sums and found no reconstruction of FAED. Repeating that construction without a new source constraint is not progress. A complete operator may itself be hidden in an unsolved intermediate; keyword searches cannot exclude that possibility.

## Reproducibility and coverage

`python tools/find_operation_instructions.py` writes hashes, source comments, full contexts, the creator-message inventory and keyword hits. The inventory contains 492 original creator messages plus 325 forwards in PUZ, and 5,412 original creator messages plus six forwards in COMM. Search selected 155 PUZ and 81 COMM records; forwards contain duplicates. PUZ creator text was also read beyond keyword hits. This is a text/source review, not an exhaustive media review or live-web search.

Evidence files: `coverage.json`, `creator_inventory.json`, `search_hits.json`, `contexts.json`, `source_checks.json`. The original decrypted passage is `data/architect_plaintext_readable.txt`; original surrounding instruction bytes are in `data/phase3_2_plaintext.bin`.
