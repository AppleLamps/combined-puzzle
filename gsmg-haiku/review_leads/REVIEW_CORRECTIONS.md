# Review corrections and local handoff — 2026-10-09

Starting checkout: `C:\gsmg-puzzle-clean`, clean at
`7a2dbfbc09abfcf7a83ea8b627462804a1c3e68f` (the reviewed commit).
No applicable AGENTS.md or .agents/skills directory was found in this checkout
or its parent. No unrelated edits were present. Work stayed local; no push,
publication, broad puzzle/password/key search, paid job, transaction or signing
operation occurred. No Telegram-embedded link was opened. The denied live
WhatsOnChain fetch was not repeated or replaced with another fetch route.
Only the user-specified Memo protocol documentation was read online.

## Byte representations and pool fix

Git stored the phase plaintexts with LF, while this Windows checkout originally
had CRLF (`core.autocrlf=true`). Original CRLF hashes matched README. Historical
Windows results are not invalidated by the LF bug. The new attributes explicitly
store/check out these three derived files as LF; their committed content is
unchanged. README gives both representations; STEPS explicitly labels original
CRLF offsets. Canonical encrypted artifacts remain unchanged.

`mywork/candidate_pool.py` now selects the full prose sections by validated
boundaries, keeping `Raising ` and excluding the binary Architect body, digit
block, and Terminal/Phase 3.2 container prefixes. Unexpected section structure
raises ValueError. Both LF and CRLF yield the same candidate pool.
`pool_search.py` has a main guard, and `binary_envelopes.py` explicitly imports
the shared constructor instead of extracting executable statements with AST.
The original candidate-generation rules and nine transformations are preserved.

| Constructor/input | Unique candidate strings |
|---|---:|
| Historical constructor / LF | 40,159 |
| Historical constructor / CRLF | 40,114 |
| Corrected constructor / either | 40,114 |

The corrected set equals the historical CRLF set exactly. Relative to the old
LF set it restores 45 candidates and removes 90. Counts and set fingerprints are
in `evidence/pool_comparison.json`. In addition to the regression fixture, the
exact constructor from the starting commit was independently executed only up
to its first print statement, with LF/CRLF byte fixtures; both counts and the
CRLF set equality matched. No decrypt loop or password sweep ran.
The separate artifacts read by `run_new_leads.py` and the transposition paths
were unaffected. Existing experiment JSON/JSONL results were not rewritten.

## Provenance, protocol and interpretation

The creator review now distinguishes original messages, edits, and forwards.
Local source-kit excerpts confirm #991 (2019-05-31), #1487 (2019-09-26,
edited 2025-04-30), #6250 (2021-03-05, edited 2025-09-08), #6884
(2021-04-01, edited 2025-02-02), and nearby #6895's Cyberpunk-parody reply.
Original timestamps do not date later edited wording. Reposts do not prove new
clues or an undiscovered artifact. Calendar/April Fools remains plausible, not
a proved exclusion; the R/A/B screenshot does not contain the braces clue.
The source-kit commit `00bc7b003140399d6d9a85aa3f7c91ce70a80a7a` is supplied
by the review; the locally available copy is an unpacked archive, whose file
hash and relevant excerpts are recorded without claiming a verified Git identity.

The recovered 819-entry selection contains 492 direct creator messages plus
327 forwards attributed to that account, reproduced against the committed export.
Only selected message IDs and minimal source excerpts were added as evidence.

Memo's documented 6d24/6d04 action codes mean Send money and Like/tip;
9325/1133 convert to those bytes in little-endian form. 5262419 gives SLP,
not PLS; 1145980243 gives SEND. Recovered scripts additionally show SLP-NUL,
SEND and GENESIS pushed fields. Protocol identification alone is not an exclusion
of puzzle meaning or validation of token state.

The original session scratchpad was found under the Windows Temp Claude session
`09a818a2-bd6d-4f8b-a821-24ce852ddf20`. Six existing public transaction JSON
records were preserved byte-for-byte with hashes in `evidence/bsv_manifest.json`.
They confirm the blob's 192 bytes / 83 UTF-8 characters / 24 distinct symbols.
No saved script or output log supports the older list of decoding attempts;
those attempts remain unverified, and exhaustive-exclusion language was removed.

The BTC checkpoint is deterministically reproducible from SHA256 of the public
target-address string using compressed P2PKH, and its 1,000-sat hint payment is
in `mywork2/web/gsmg_txs.json` index 25. Recovered BSV records identify that exact
checkpoint in the spent prevout and change of `7ea6...`. Equality is now supported
within the saved records, exceeding what the truncated label alone supported.
Independent raw-transaction/chain validation remains unperformed. Publicly
derivable checkpoint control cannot authenticate exclusive creator ownership.

Funding-history claims now require pagination evidence and apply only to the
inspected subset. 150,000,000 sat is corrected to 1.5 BTC. The parent-source
percentages describe the 8.65890724 BTC input total, not an attributable split
of the 5 BTC output. Earlier coincidence and nonprintability claims are corrected
in `mywork/report.md`, preserving the bounded historical experiment records.

## Validation

Run from the checkout with the existing system Python 3.13 (pycryptodome and
coincurve available):

```powershell
python -m unittest discover -s tests -v
git diff --check
```

15 tests passed. They check LF/CRLF lengths/hashes and exact prose boundaries,
rejection of changed structure, candidate-set equivalence and fingerprints,
all six decoded encrypted-container hashes, import safety with AES disabled,
protocol integer/amount arithmetic, checkpoint derivation/payment records,
saved BSV evidence hashes and complete Memo push-data layouts (Send money: tag, 20-byte address, message; Like/tip: tag, 32-byte transaction reference), and the creator-selection counts.

The 32 columnar cases match every saved stream and parse exactly: 29 complete,
3 incomplete. R1 counts a3,b25,c8,d4,e18,f10,g10,h8,i5 give invariant bounds
under permutations of the digit stream with the fixed mapping/board: at least
18 U characters, at most 3 combined L/E/T/H/I/N/G/K/Y, and at least 84 decoded
characters in any complete parse. Parsing success is not plaintext recovery.
No AES trials or target-key searches were run. `git diff --check` passed.

## Remaining uncertainties and user action

Unknown: first appearance of edited clue wording; the referenced outside piece;
blob meaning and historical decoding-attempt parameters/results; exclusive
sender authorship; independent BSV transaction/signature/chain/token validation;
complete funding-wallet pagination and ultimate input origins.
No user action is needed to review or run these local deterministic tests.
Publishing/pushing requires separate authorization. Any future live chain fetch
must respect the earlier denial and receive explicit authorization; the saved
records suffice for the checks performed here.
