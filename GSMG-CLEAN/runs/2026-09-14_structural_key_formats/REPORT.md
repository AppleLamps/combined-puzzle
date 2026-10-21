# Recursive hex / raw key / WIF / base64 / Half–Better-Half audit — 2026-09-14

**Result: complete recursive key-format inspection of the retained 2026-09-14 structural outputs found zero
valid WIFs and zero exact target-key matches.** No envelope bytes were read and no AES decryption was run.

## 1. What was and was not checked previously

The envelope tooling was already comprehensive:

- `tools/check_candidate.py::find_keys` scans every padding-valid AES plaintext for every overlapping
  32-byte big-endian scalar, isolated 64-hex scalars, valid uncompressed/compressed WIFs, and base64 strings
  decoding to 32 bytes.
- `tools/inspect_decrypts.py` adds little-endian 32-byte windows and recursively decodes hex, binary,
  base64/base64url and decimal-integer representations before scanning again.

However, several new **pre-AES structural audits** checked only `sha256(output)` and/or a whole-output scalar.
They did not uniformly run every retained output through the recursive key recognizers. This was a real
coverage gap.

## 2. Corpus and recognizers

Every output was first persisted from seven structural sources. The five result-generating runs were rerun so
their `all_outputs.jsonl` record counts exactly match their reported counts:

| source | retained records |
|---|---:|
| M4 literal candidates | 476 |
| balanced-pointer selector candidates | 2,119 |
| board-shape values | 744 |
| colour selectors | 142 |
| DBBI-derived keys over FAED | 93 |
| tail cipher | 181 (3 substitution + 178 layered) |
| matrix sums → last words | 34,860 |
| **total** | **38,615** |

`tools/audit_structural_key_formats.py` recursively decodes each retained UTF-8 output to depth two as
applicable: hex, binary/a-b binary, base64, base64url and decimal integer. Every resulting byte node is then
checked for:

- every overlapping 32-byte scalar, **big- and little-endian**;
- isolated 64-character hexadecimal scalars;
- syntactically valid and Base58Check-valid 51/52-character WIF;
- base64 tokens decoding to exactly 32 bytes;
- decimal scalars;
- explicit **32 + 32** splitting for every 64-byte node;
- compressed and uncompressed P2PKH comparison against the three full marker addresses and both prize
  addresses.

## 3. Positive controls

All seven controls use the known phase-1 marker scalar and pass before the corpus is accepted:

| format | control |
|---|---|
| uncompressed WIF | detected and decoded to the known scalar |
| compressed WIF | detected and decoded to the known scalar |
| hex64 | decoded to the known scalar |
| base64 → 32 bytes | decoded to the known scalar |
| first 32-byte half | decoded to the known scalar |
| second 32-byte half | decoded to the known scalar |
| address gate | known scalar matches its marker address |

This proves that a real target in any named representation would be reported.

## 4. Results

| observation | count |
|---|---:|
| source records | 38,615 |
| unique recursive byte nodes | 20,436 |
| big-endian raw32 windows | 259,193 |
| little-endian raw32 windows | 259,193 |
| explicit first halves of 64-byte nodes | 99 |
| explicit second halves of 64-byte nodes | 99 |
| base64 tokens decoding to 32 bytes | 35 |
| isolated hex64 tokens | 1 |
| WIF-shaped regex tokens | 42 |
| **Base58Check-valid WIFs** | **0** |
| unique valid secp256k1 scalars checked | **463,290** |
| **exact marker/prize matches** | **0** |

The one isolated hex64 is
`0afbf9ffc864848a9ad39612705e0d557129024a6487ff113534bed090db8575`, retained from the pointer-selector
run. It is a valid scalar shape but derives neither prize nor marker address. The 42 WIF-shaped substrings are
alphabetic noise that begins with 5/K/L; none has a valid WIF checksum. All 35 base64-to-32 values and all 198
named halves are included in the 463,290 checked scalars.

## 5. Answer to “half WIF?”

A WIF is an encoding of one 32-byte private scalar. If a 64-byte structural output represents “Half” and
“Better Half” as two raw scalars, converting either half to WIF does not create a new key: the scalar is
unchanged. Both offsets 0 and 32 are explicitly checked, and every overlapping 32-byte window is checked too.

A different hypothesis—a **textual WIF deliberately split across separate output records**—is not included,
because the records are alternative model outputs, not adjacent pieces of one source stream. Concatenating
unrelated alternatives would create an unbounded cross-product. If an internal construction supplies a
specific adjacency/order, that exact concatenation should be added as a new source-grounded operation.

## 6. Consequence

Yes, the retained outputs have now been checked for raw keys, hexadecimal keys, valid WIF, base64-encoded
keys, little-endian keys, and explicit Half/Better-Half raw splits. None matches. This does **not** reject an
unknown transformation that has not yet produced its output; it prevents us from overlooking a key already
present in the structural results we generated.

## 7. Reproduce

```powershell
python tools\audit_structural_key_formats.py
```

Evidence: `manifest.json`, `results.json`, `run.log`. The run uses `coincurve`; all controls are recorded in
both manifest and results.