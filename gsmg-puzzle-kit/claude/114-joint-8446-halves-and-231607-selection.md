# 114 - The joint #8446 password, the halves, and the 23/16/7 selection space (all null)

**6 October 2026 interpretation notice.** This is a dated research record.
Its candidate counts and original logs are preserved, not freshly rerun.
Read [doc 118](118-correctness-audit-remediation.md) for detector/coverage
limits and [doc 119](119-current-evidence-ledger.md) for current findings.
A null applies only to its complete tested tuple.

Joint concatenation and outside-page operands are hypotheses. “No surviving combination” refers only to named tested sets, not every possible assembly or every reading.

Date: 2026-09-25. Works the three open puzzle-side leads. Fixed-convention screen (`lean.py`):
password = sha256(answer) as 64 hex, sha256 EVP, per section 2 of the dossier; flags pad >= 2 and
runs the doc-110 recogniser on any valid pad; win test on the answer against the prize, 17ucy and
the four EC-neighbour addresses. Controls (causality, key 1, planted EBCDIC, and a planted joint
plaintext) fired on every run.

## 1. The literal #8446 joint password

#8446 reads `...matrixsumlist enter lastwordsbeforearchichoice thispassword...`, i.e. the SalPhaseIon
password is `matrixsumlist_output` + `lastwordsbeforearchichoice_output`, optionally + `thispassword`.
Neither operand is known, so both were drawn from pools:

- matrixsumlist pool: 2,500 poster sum-list strings (digit-concat form; the resistor/palette/consume
  encodings and {2,5,7} operations of doc 111, joined as decimal).
- lastwordsbeforearchichoice pool: 1,620 strings, the last 3-27 letters before the Architect's
  choice points (offset 472 take/build, the two PRIVATEKEY offsets, the end) and located by every
  sum-list total.

Cross-product, with and without `thispassword`: **8,100,000 joint passwords, 24,300,000 decrypts,
0 flags.** Bounded: the msl pool was restricted to its digit-concat form; letter and mod-10 forms
were not crossed (that would be ~3x more and is the obvious extension if a reason appears).

## 2. The halves

Every ordered pair of the 23 chain atoms concatenated (plain, `_`, space); the two 80-byte
container base64 halves as the two halves of one key (both orders); and the "half / better half"
phrases alone and crossed with each atom. **1,757 candidates, 0 flags.** With doc 107 (byte-level
XOR/interleave of the two ciphertexts) and doc 111 (string halves), the halves reading has no
surviving untested form at the password level; what is missing remains an actual operand, not a way
to combine two.

## 3. The 23/16/7 selection space

"select from over twenty three ciphers sixteen encryptions and/or seven intertwined passwords."
Read as selection + interleave over the 23 atoms: round-robin interleave and plain concat of every
ordered 2- and 3-atom selection (the "intertwined passwords" literal), and the first 7, 16 and 23
atoms concatenated, interleaved and reversed (the film's own counts). **22,221 candidates, 0 flags.**
This complements doc 50 (7 password-grade operands interleaved) and doc 96 (4-part orderings): the
new part is the interleave at group sizes 2 and 3 over the full atom set. Null.

## 4. Status

All three leads null under the fixed convention. The wall is unchanged and now sharper: the two
operations `matrixsumlist` and `lastwordsbeforearchichoice` are not reachable by combining known
objects, however selected, interleaved or split. A correct solve needs the *operand* each operation
acts on, which lies outside the SalPhaseIon page, not another arrangement of what is already decoded.

Scripts (scratchpad): `lean.py` (fixed-convention screen + controls), `pools.py` (operand pools),
`run_joint.py`, `run_sel.py`, `run_halves.py`.
