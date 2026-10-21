# Unverified assumptions audit — 2026-09-13

No locked envelope was solved. This audit distinguishes documented community practices from hypotheses in this workspace; neither represents a unanimous community view.

## Highest-impact gaps

1. **A correct decrypt starts as printable ASCII.** The archived `../newest-puzzle-9.9.26/files/aesdecodemultiprocessing v5.py`, dated January 2024 in its header, returns at lines 384–385 when its first-block printable check fails, before full decryption and PKCS#7 validation. This excludes binary, many non-ASCII encodings, and even a lone LF in most first-block positions. Its later non-UTF8 output handling cannot recover candidates rejected here. This is evidence of a real historical blind spot, not evidence that a correct password was actually tried. Our 755 recovered outputs remain unresolved and preserved; no successful plaintext has been authenticated.

2. **Decoded labels establish a password recipe.** The community snapshot decodes `matrixsumlist` and `lastwordsbeforearchichoice`, but does not prove their operand, scope, or composition. Source order is `DBBI | matrixsumlist | FAED | lastwordsbeforearchichoice | ...`. A viable competing interpretation is that these are labels following their respective encoded fields. Treating the Architect phrase exclusively as a literal external quotation may bypass an unsolved field. This competing model is not established either. Prior candidate failures only constrain the specific representations tested.

3. **b/be establishes signed primes and a rectangular matrix.** The source-supported chain is b/be -> 2/25 -> B/Y -> blue/yellow. The 84-cell parse yields 23 prime positions, 16 b and 7 be. None of this establishes negative/positive signs, a 7×12 shape, axis, modulus, or cipher. The 83-cell alternative differs only in the treatment of the final source `be`; the textual 23/16/7 correspondence favors 84, but is not a downstream decode.

4. **The colour correspondence is exact, or its discrepancy is already explained.** The favored parse matches 22 of the first 23 poster colours. Marker 21 disagrees, and poster colour 24 remains unpaired. The off-white square shares URL character 21 with the discrepant marker but is a different bit. Treating those positions as identical silently supplies a missing operation. Preserve the discrepancy rather than repair it by assumption.

5. **The three locked blobs form an established sequence.** Original source containment branches. Terminal is in Phase 3.2; SalPhaseIon short and separately headed Cosmic Duality are on the side page. There is no authenticated password dependency between them. A solve priority is not a proven ordering.

6. **Failed searches settle the theory.** Negative results depend on exact source bytes, candidate serialization, hashing, KDF, and output acceptance. Current ciphertext extraction and three earlier-stage positive controls check out. Earlier failures with lossy gates do not exclude every valid plaintext. Likewise the recent workspace DBBI digest criterion (L5) is optional, not an established historical community rule or universal success test.

## What should remain the default

Three full earlier decryptions support SHA256(answer) as a hex-text passphrase, legacy SHA256 EVP_BytesToKey and AES-256-CBC/PKCS#7. This is strong evidence for the default, not proof of the locked stages' settings. Current short-envelope lengths constrain plaintext to 64–79 bytes under this convention: a bare 51/52-character WIF is excluded, while a 64-character hex string fits. Avoid replacing evidence-backed defaults with unrestricted algorithm guessing.

`enter` decodes exactly between two 64-character base64 lines. A line-break instruction is well supported; exclusive meaning is unproven. It is a lower-priority uncertainty than field roles and the colour mismatch.

## Correction to our own interpretation

The community snapshot at line 291 explains “One for one, four for one” as 1141 -> IBM EBCDIC 1141. Our b/be report described it too narrowly in terms of checkerboard rows. The successful encoding interpretation must be included; neither interpretation establishes signs for b/be.

## Best next derivation task

Resolve the roles of DBBI and FAED before expanding guessed passphrases. Compare explicit competing models: independently encoded fields with trailing labels; one field transformed into the other; two password components. Require a reproducible intermediate relation that accounts for source characters, the prime grammar, and any colour exceptions. Keep matrix dimensions, signs, deletions and hashes as separately justified choices. Do not reward a model merely for generating more AES attempts.

Supporting audits: `10_ENVELOPE_CONTEXT_AND_SOLVING_STRATEGY.md`, `runs/2026-09-13_b_be_hints/REPORT.md`, `runs/2026-09-13_missing_prime_operation/REPORT.md`, `runs/2026-09-13_recheck_755/REPORT.md`, and the archived community README and source code cited above.
