# DBBI prime structure: reproduced and narrowed

This strengthens and reconciles existing leads. It is not a new decryption or a derived password.

## The old remove-g claim is correct

Removing every `g` from the 91-character DBBI string makes its first nine `b` positions, 1-based:

`2, 3, 5, 7, 11, 13, 17, 19, 23`.

The next `b` is at 27, not 29. Thus this is an initial-prefix relation, not a complete prime-position encoding after deleting g.

Tested the maximum prime-prefix run over identity and deletion of each single non-b letter, for every control too. The observed maximum is 9, attained by g deletion. On 20,000 whole-string letter-count-preserving shuffles, zero reach 9. On 20,000 shuffles preserving the first 13 source characters (including the already-known initial prime positions), 31 reach 9. The latter empirical tail count is 0.155%, or 0.160% using a plus-one estimate.

This accounts for the tested deletion family, not the puzzle's enormous historical space of tried hypotheses. The result supports further structural investigation, not a global probability that the clue is intentional.

## A complete grammar is more useful than the prefix

Tested this existing prime-cell interpretation:

- Logical cells are numbered starting at 1.
- At a prime-numbered cell, consume `b` or `b` followed by one fixed optional suffix letter.
- At every other cell, consume one letter.
- Require the parse to consume the entire input without leftovers or edits.

Among all nine suffix letters a..i, **only e permits complete parses**. It gives two:

| Cells | Prime cells | Prime `b` tokens | Prime `be` tokens |
|---:|---:|---:|---:|
| 84 | 23 | 16 | 7 |
| 83 | 23 | 15 | 8 |

Both reconstruct the complete original string exactly. The first 82 logical cells are identical. The only ambiguity is the **final two source characters** at zero-based offset 89:

- 84-cell reading: cell 83 is prime token `b`; cell 84 is ordinary `e`.
- 83-cell reading: cell 83 is prime token `be`.

This resolves the clean grammar's 83-versus-84 discrepancy without changing a byte. It does not independently validate every external ZERO/FE implementation; those may impose additional conventions.

The 84-cell reading has the 23/16/7 counts present in the modified Architect text. That is a source-grounded reason to prioritize it while retaining the other parse. Those numbers are inherited from the film and the exact wording says “over twenty-three”; the correspondence is supporting evidence, not a formally stated specification.

The complete-parse property is also unusual under a targeted control: **0 of 5,000** shuffles that preserve the first 13 characters permit any complete parse across the nine-suffix family. This is a finite Monte Carlo result under a specified null, not zero probability or proof of authorship.

## What this establishes and what remains unknown

Established: prime-slot structure can explain every DBBI character with only one final token-boundary ambiguity. It goes beyond recognizing a short word in a transformed output.

Still hypotheses: interpreting `b` as minus the cell's prime and `be` as plus; selecting row-major 7x12 rather than other factor shapes; treating column sums as modulo-26 letters; treating `HILLFEXMGSGQ` as a Hill-cipher instruction; or using the resulting values on FAED. None of these follows from the grammar alone. Previous tests of those continuations remain relevant.

**Next priority:** derive the numeric meaning and use of the 84 logical cells from the adjacent `matrixsumlist` and colour/prime clues. Keep the complete parse as an input constraint, preserve the alternate final parse as a control, and require the next operation to explain substantial material. Do not restart arbitrary password sweeps or assume deleting g is itself the full solution.

## Reproduction

`tools/audit_dbbi_prime_prefix.py` writes the deletion-family manifest and control results. `tools/audit_dbbi_prime_grammar.py` writes the full parses and conditional control results. The prefix script expects its output directory not to exist; the grammar script writes its own derived files within that directory. Manifests record seeds, source hash, family definitions and sample counts before the controls run. The grammar assertions require both complete reconstructions and the expected parse lengths.
