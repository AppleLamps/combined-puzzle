# SalPhaseIon: complete framing, unresolved inner construction

**The wrapper is now reconstructed character-for-character, but its two unknown fields are not decrypted.** They contain 661 of 1075 characters (61.49%). This report does not label those fields explained merely because their boundaries can be located. No candidate passwords or AES searches were generated.

## 1. Lossless layout

Offsets are zero-based, end-exclusive. The actual first textarea has exactly one space between every character, without any extra grouping. Decoding and then re-encoding every known field reconstructs that original spacing and every original character.

| Span | Length | Source role | Complete interpretation |
|---|---:|---|---|
| 0–91 | 91 | DBBI | Unknown; admits the two complete prime parses |
| 91–195 | 104 | Binary a/b | `matrixsumlist` |
| 195–765 | 570 | FAED | Unknown |
| 765–766 | 1 | `z` | Separator |
| 766–829 | 63 | Decimal a–i/o integer | `lastwordsbeforearchichoice` (26 letters) |
| 829–830 | 1 | `z` | Separator |
| 830–859 | 29 | Decimal a–i/o integer | `thispassword` (12 letters) |
| 859–860 | 1 | `z` | Separator |
| 860–895 | 35 | Literal text | `shabefourfirsthintisyourlastcommand` |
| 895–959 | 64 | Base64 | First half of short envelope; final `z` is data |
| 959–999 | 40 | Binary a/b | `enter` |
| 999–1063 | 64 | Base64 | Second half of short envelope |
| 1063–1075 | 12 | Literal text | `shabefanstoo` |

Accounting: 661 unknown + 236 encoded labels + 3 separators + 47 literal characters + 128 base64 characters = **1075**, without overlaps or discarded characters. Cosmic Duality is in a separately headed second textarea: 1792 base64 characters, 1344 decoded bytes. It is not an unassigned tail of the first stream.

The faithful partially decoded reading is:

```text
[DBBI: 91 unknown] matrixsumlist [FAED: 570 unknown]
z lastwordsbeforearchichoice
z thispassword
z shabefourfirsthintisyourlastcommand
[64-character ciphertext half] enter [64-character ciphertext half]
shabefanstoo
```

Spaces and line breaks in this display are editorial. Reading `shabef` as `sha256` is supported by the letter-digit layer and the repeated prefix, but the surrounding words' instruction scope remains unresolved.

## 2. Which boundaries are independently constrained?

**Binary fields:** scanning the complete stream finds exactly two maximal a/b runs of at least 16 characters: the 104- and 40-character fields above. Both consume all their bits in complete bytes and round-trip to the source. Their ends are not chosen to stop after a promising word prefix.

**Separators:** there are four literal `z` characters, at offsets 765, 829, 859 and 958. Only the first three act as separators in the verified parse. Offset 958 belongs to the first base64 half. Splitting globally on z loses real ciphertext.

**Envelope end:** after preserving the first half, consuming the encoded `enter` separately and including at least one character from the second half, every possible end through the end of the source was checked. Only **1063** gives canonical base64, `Salted__` framing and a block-aligned ciphertext. The remaining `shabefanstoo` is therefore genuinely outside this envelope under the established container convention. This is a framing result, not a key/password validation.

**First region:** the first z occurs after the uninterrupted 765-character a–i region. The embedded binary label creates a well-supported local boundary; it does not prove that the unknown portions are independent ciphertexts. Conversely, sharing the alphabet a–i does not prove a shared cipher state.

## 3. Does DBBI's grammar continue across the boundary?

A fresh state-based parser tests every b/be choice at prime logical positions, preserving one source character at every other position. Primality is computed for the full tested range. No arbitrary resets, discarded characters or shifted starts are added.

| Input/model | Result |
|---|---|
| DBBI alone | Complete 83- and 84-cell parses |
| Entire initial 765-character region | No complete parse; furthest branch consumes 104 characters and fails at logical prime 97 |
| DBBI + FAED, with the binary label removed | No complete parse; furthest branch consumes 96 characters and fails at logical prime 89 |
| FAED with numbering restarted at 1 | Fails on its second character: prime slot 2 requires b/be, actual a |
| FAED continuing after 83 DBBI cells | Fails after five characters, at prime slot 89 |
| FAED continuing after 84 DBBI cells | Fails after four characters, at prime slot 89 |

The simple claim that these fields share the same unmodified prime grammar is therefore false. A shared higher-level construction can still transform DBBI into a key, matrix, mask or instruction for a different FAED operation. These tests do not determine which.

## 4. The source itself requires changes of representation

The known fields already switch conventions:

- Binary labels: a=0, b=1.
- Decimal labels: a=1, b=2, … i=9, o=0, interpreted as one large decimal integer before converting to bytes.
- Literal hashing phrase: `sha` stays literal while `bef` is read as 256.
- Ciphertext: original case, digits, plus and slash are retained as base64 data.

Consequently, a global substitution, a global z split, or a single numerical meaning for every b in the entire source cannot reproduce the known wrapper. A valid construction must identify when the representation changes. This also limits the b/be colour interpretation to its supported token context; it is not a universal decoding rule for FAED.

## 5. What the competing explanations now have to satisfy

| Model | Constraint from the complete source |
|---|---|
| Two independently encoded answers with trailing labels | Must decode the entire 91- and 570-character regions, not just recognizable prefixes; must explain whether `thispassword` belongs with the preceding label or the following command |
| DBBI supplies a transformation/key for FAED | Best accommodates a change of operation, but needs a derivation specifying the key's representation and a complete reversible FAED decode |
| One cipher over the first 765 characters | Must explain why its embedded binary section decodes completely as a local instruction; the simple common prime grammar has failed |
| Data transformed directly into its following labels | Note that matrixsumlist is 13 characters; lastwordsbeforearchichoice is **26**, not 38. The 38-character target used in an earlier matrix model combines it with the separately delimited `thispassword`; that combination is an explicit assumption. Earlier shared weighted-sum tests failed their declared 13/38-target models |

At present none meets the complete-construction requirement. The strongest remaining model class is **DBBI-derived material used in a different FAED operation**, because it respects the genuine prime structure without forcing that grammar onto incompatible data. This ranks a class of models; it does not establish an algorithm or password recipe.

## 6. Complete sum-key model tested

To test an actual construction rather than merely propose one, `tools/test_sum_key_faed.py` implements raw DBBI -> ordinary matrix sums -> repeated Beaufort key on the full FAED a–i alphabet -> the page's decimal-integer byte decoding. It uses all four exact DBBI rectangle widths (1, 7, 13, 91), both axes and two declared numeric conventions. These are **16 cases, 12 distinct full outputs**.

All 570-character Beaufort results re-encrypt exactly. None yields a wholly printable ASCII or valid UTF-8 byte output through the declared final layer. Every full letter stream, numeric string, byte output and key is saved in `sum_key_outputs.json`. This does not authenticate Beaufort, and a reversible round trip alone is not evidence of correct plaintext. It finds no complete readable result for this specific sum-key construction; other alphabets, key derivations and additional layers remain outside its scope. No AES or word-prefix screen was used.

## 7. What remains genuinely unexplained

- The numerical meaning of the b/be prime labels and the final 83/84-cell ambiguity.
- The full 570-character FAED payload.
- Whether matrixsumlist names an output, an operation or an input representation.
- The operand of the Architect selector and the scope of `thispassword`.
- The exact ordering and scope of hashing and the “first hint / last command” instruction.
- The poster's unmatched colour and the b/be colour discrepancy if that connection is used.

No meaningful character has been dropped to make the layout fit. Preserving the unknowns is not equivalent to solving them.

## Reproduce

Run `python tools/reconstruct_salphaseion.py`. `segments.json` retains every raw field, decoded label and exact span. `summary.json` contains source hash, accounting, valid envelope ends and grammar failures. `reconstructed_original_textarea.txt` is the exact regenerated first textarea body. Controls verify all known encoding round trips, source equality, the two DBBI parses, and enforcement of prime slot 101 in long-stream parsing.
