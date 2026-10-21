# 83/84-cell DBBI fork: lossless comparison and forward predictions

## Result

**Both poster-guided models reproduce all 91 DBBI characters. Neither endpoint is selected by the
additional data tested in this run.** No password generation, AES decryption, or network access occurred.
The original saved HTML was read for its first textarea; no claim is made that its ciphertext text was
never read as part of the containing page.

This is a bounded forward-model comparison, not a new solver or an exhaustion claim.

## 1. Inputs and source ownership

The original poster was sampled by modal cell colour along the verified spiral. It still produces
`gsmg.io/theseedisplanted`. DBBI and FAED were extracted from the original saved SalPhaseIon textarea and
compared with the clean working copies. Source-file hashes are in `manifest.json`.

| Model | Source rule | Logical cells | Prime tokens | Ordinary payload | Unused schedule |
|---|---|---:|---:|---:|---|
| serial83 | Include all non-black/non-white cells; yellow -> be; blue/off-white -> b | 83 | 23 | 60 characters | b, be |
| perbyte84 | One regular colour marker per URL byte; XOR its blue/yellow flag with the presence of off-white in that byte | 84 | 23 | 61 characters | be |

These are hypotheses about marker interpretation. They are not claims that the off-white cell is visually
blue or that XOR is an author-confirmed operation.

`models.json` preserves every cell's source start/end offset, logical slot, token, prime flag, marker
ordinal, and the original poster coordinates/colours of the schedule. Each original DBBI character belongs
to exactly one cell. Reinserting the recorded markers into each complete ordinary payload reproduces DBBI.
This round trip retains the ordinary payload from DBBI; it does not independently explain that payload.

### Exact shared-prefix relation

The models share the first **82 logical cells**, including their source offsets. They differ only in the
interpretation of the final source `[89,91)` = `be`:

- serial83: one prime token `be` at logical slot 83;
- perbyte84: prime token `b` at slot 83, ordinary `e` at slot 84.

Consequently:

```text
payload84 = payload83 + e
```

The full 60-character payload is:

```text
difhccgihaeeihggegebgehhehhfafdhffcdbfcccgfeggecdcifffgigeea
```

The 84-cell payload appends one `e`. Any experiment using only the shared prefix is incapable of choosing
the endpoint. The shared-prefix and payload-extension observations reconcile existing evidence; no novelty
claim is made for their underlying arithmetic.

## 2. Prior coverage, not repeated as a discovery

The existing off-white and payload60 reports already compare poster row/column sums and many
serializations to the 60-character remainder. The label-model audit also tests direct FAED margins against
literal DBBI, and direct DBBI-derived margins against FAED. This pass does not repeat those searches and
call them new.

The tested composite forward hypothesis is instead:

```text
complete FAED matrix
    -> complete row/column sums
    -> unpadded decimal digit-letter ordinary payload
    -> insert b/be at prime slots using one frozen poster schedule
    -> predict all 91 DBBI characters
```

Thus the target is not a password or fragment. Both the ordinary payload and the full prime-inserted field
must be correct. This is a test of one interpretation of DBBI as encoded matrix sums; it does not establish
that interpretation. No claim is made that every historical workspace omitted this composite hypothesis.

## 3. Forward reconstruction scope and result

Two FAED representations were declared:

1. all 570 letter-digits, a=1 through i=9;
2. unsigned bytes of the complete 570-digit decimal integer (237 bytes).

For each: all exact rectangular factors including degenerate rows/columns, row sums, column sums, both
concatenation orders, forward and reversed lists. Decimal serialization uses no padding, separators,
modulus, sign changes or truncation. Both frozen endpoint models are tested.

**320 model comparisons; zero length-compatible payloads; zero complete DBBI predictions.** Counts include
equivalent cases and both endpoint comparisons, not independent statistical trials.

- Required ordinary payload lengths: **60** or **61**.
- The nearest produced FAED digit-margin length is **57**; others nearby are 45, 77 and 79.
- The complete-decimal byte-matrix margin lengths are **5, 15, 236, 251, 613, 618**.

Length mismatch alone excludes this declared serialization before text/key judging. Changing the field's
representation, adding a transform or using padded/delimited sums would be a different model, not a
correction authorized by this failure.

All 320 proposals and their complete sum lists, payloads, eligibility and predicted fields are retained in
`forward_comparisons.json`; decimal outputs are additionally kept in `forward_outputs.jsonl`. No candidate
was rejected for being non-English. Since no complete DBBI prediction exists in this family, no private-key
or address scan was performed or claimed for these proposals.

## 4. Held-out adjacent-field continuation

The unused marker schedules were continued without inventing new marker values. Results are saved with
the consumed cells and exact mismatch positions in `continuation.json`.

| Endpoint | Next material | First failed logical slot | Offset within next material | Expected | Actual |
|---|---|---:|---:|---|---|
| 83 | binary matrixsumlist label | 97 | 13 | be | aa |
| 84 | binary matrixsumlist label | 89 | 4 | be | bb |
| 83 | FAED, assuming the label is skipped | 89 | 5 | b | g |
| 84 | FAED, assuming the label is skipped | 89 | 4 | be | gg |

The 83-cell label continuation is a regression of a previously recorded failure. The 84-cell comparison
and skipped-label cases make the side-by-side scope explicit. Matching more initial characters in one
case is **not** a success criterion. Neither model explains the complete next field through this grammar.
The fields could use different operations; failure of continuation does not invalidate the DBBI fit.

## 5. Controls and independent checks

Five tests pass in `test_compare_dbbi_forward_models.py`:

- planted 83-endpoint forward recovery: source matrix -> margins -> serialized 60-character payload ->
  complete inserted-marker field; the 84-endpoint rejects its length;
- a source-cell mutation changes that complete prediction;
- planted 84-endpoint recovery using 61 digits; the 83-endpoint rejects its length;
- complete parsing/ownership and no invented schedule continuation;
- sum conservation across every reading order.

The first draft of the 84-endpoint synthetic test accidentally created 62 digits; it failed before
verification. It was corrected to an explicit 61-digit assertion. Production data and comparisons were
unaffected. This correction is retained here rather than portraying the initial test as successful.

`verify_dbbi_forward_comparison.py` independently rebuilds both fields, verifies each source-character
assignment and recomputes all **320** margin proposals from the saved FAED bytes. Results are in
`independent_verification.json`.

## 6. What remains unresolved

No independent downstream relation chooses 83 or 84 here. Both remain live interpretations.

Of the three role hypotheses proposed for DBBI:

- **encoded sum list:** the direct FAED-margin/decimal/prime-insertion version is excluded by length;
- **instructions describing sum-list construction:** not implemented as an unspecified general program;
  no unique instruction decoding was identified in this pass;
- **parameters controlling FAED:** not broadly retested here; earlier bounded tests remain model-specific.

The next discriminating construction must predict the endpoint-dependent information (the final `be` and/or
the remaining poster markers) as well as additional data. Re-hashing the common prefix, counting factors of
60 versus 61, or preferring 84 merely because 23/16/7 appears elsewhere cannot supply that prediction.

The data has not been shown to be missing. The operation relating these fields is still unknown.

## Reproduce with a fresh output directory

```powershell
python E:\rabbit-combined\GSMG-CLEAN\tools\test_compare_dbbi_forward_models.py
python E:\rabbit-combined\GSMG-CLEAN\tools\compare_dbbi_forward_models.py --out E:\rabbit-combined\GSMG-CLEAN\runs\dbbi_forward_replay
python E:\rabbit-combined\GSMG-CLEAN\tools\verify_dbbi_forward_comparison.py E:\rabbit-combined\GSMG-CLEAN\runs\dbbi_forward_replay
```

The output-directory argument refuses an existing directory. Original puzzle files and earlier reports are
unchanged by the comparison tools.