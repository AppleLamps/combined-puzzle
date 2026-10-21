# Broader plaintext inspection

Follow-up: `../2026-09-13_recheck_755/REPORT.md` independently verifies all 755 padding triggers and reviews embedded fragments. The zero-format-signals count below refers to this initial whole-message inspection, not absence of all embedded structure. Every output remains unresolved and retained. The inspector was subsequently updated to explicitly label this status and preserve partial decompression bytes.

Implemented `tools/inspect_decrypts.py` as an additive replacement for using the old checker's notable-only output. Existing tools and historical runs are unchanged.

## Usage

From `E:\rabbit-combined\GSMG-CLEAN`:

```powershell
python tools/inspect_decrypts.py --file candidates.txt --profiles all --out runs/new_candidate_inspection
python tools/inspect_decrypts.py --replay runs/2026-09-13_assumption_audit/all_padding_valid.jsonl --out runs/new_replay_inspection
python tools/test_inspect_decrypts.py
```

Use a new output directory each time. Omitting `--profiles all` uses the proven `gsmg` profile. All means the four existing explicit answer/KDF profiles; it does not mean all encryption algorithms. Candidate whitespace is preserved except line endings. Replay accepts JSONL records with `plaintext_hex`, including the prior audit's journal, and retains all original metadata.

## What is wider

- Every padding-valid plaintext is saved completely, including unknown binary output and padding 1 or 2.
- UTF-8, UTF-16 LE/BE, UTF-32 LE/BE, EBCDIC cp037/cp273 and Latin-1 text views.
- Whole-field hex (including spaced hex), standard/URL-safe base64, binary bits, a/b bits, decimal integer-to-bytes, and a–i/o letter-digit integer encoding.
- Bounded gzip, zlib, bzip2 and xz decompression, with completion/error/limit reporting.
- JSON container parsing; nested OpenSSL envelope shape; PDF, ZIP and PNG signature detection.
- Existing raw big-endian, hex, WIF and base64 key checks, plus little-endian raw scalars and decimal scalars. Decoded views are checked too, allowing such cases as UTF-16 hex keys.
- Decoding chains default to two layers, with full bytes and transform paths retained for visited nodes.

`all_results.jsonl` records everything. `manifest.json` records source hash, profiles, backend, limits and counts. Signals, final-address matches, and unknown results are distinct; format signals are not proof of a correct decrypt. No top-N filter discards outputs. Coincurve accelerates key comparisons when installed; pure Python is the fallback.

## Validation and actual result

Nine planted tests passed: pad-1 instruction recognition, text encodings, base64-to-gzip-to-JSON, puzzle-specific encodings, decompression limits/errors, unknown-byte retention, nested envelope detection, transformed key matches, and a live pad-1 decryption journal.

Replayed all 755 preserved outputs from the previous 188,112-trial candidate run:

- 755 retained.
- 0 format signals.
- 0 final-key matches, including the additional scalar layouts.
- 0 limits encountered.

The text heuristic was extended during the run to cover numeric UTF-16/32 hex strings. After completion, all 755 were separately rechecked with the final text-format implementation; still zero format signals. Raw key comparisons were unaffected by that change.

## Limits and next extensions

This widens plaintext recognition, not candidate generation or cipher selection. Live mode still assumes AES-256-CBC with PKCS#7 and the chosen existing profile. No-padding, zero-padding, other ciphers/KDFs, damaged ciphertext and arbitrary cipher transformations need separate explicit experiments.

Text heuristics favor ASCII-letter prose and hex-like text, so arbitrary non-Latin prose may remain unrecognized. It is nevertheless retained. Most structural decoders consume whole fields; arbitrary embedded encodings, ZIP archive extraction, mnemonic dictionaries, DER key parsing, XOR/Beaufort/transposition and arbitrary JSON field extraction are not implemented. The nested-envelope check recognizes shape and does not guess its password.

Limits: 32 unique decoded nodes, 64 KiB per decoded node, 4,096 bytes per node for raw key scanning, default depth 2 (configurable 0–4). Exceeding a limit is recorded, never called a negative. Decompression does not execute content. A signature match is only a signature match; decompression validates the applicable stream's completion, not the correctness of the puzzle answer.

No puzzle envelope has been solved by this run.
