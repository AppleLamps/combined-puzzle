# 118 - Correctness audit remediation (5 October 2026)

Base: upstream main `c5fe2ab89aa3758370be0055282d2c57ab9a9e62`, checked before edits.
This is source remediation and non-encrypted regression verification. No puzzle
searches, encrypted runtime checks, spending or live-wallet operations were run.

## Results

- `rt.py`, `ct.py`, `ms.py` and `h3.c` preserve padding-valid plaintexts independently
  of heuristic ranking. Padding 1 and 2 are legal even for unmarked binary data.
  Each invocation retains the first 1,000 complete records in traversal order,
  with candidate, container, form, cipher/KDF, padding and full plaintext bytes.
  Totals and omitted counts are explicit; overflow returns status 2 and makes
  review incomplete. Padding alone does not validate a password or solution.
- Python solved controls require the known plaintext hashes; cipher controls
  require exact planted plaintexts under the intended configuration. Retaining
  unranked results cannot turn random wrong-key padding into a passing control.
- Common-flaw assembly is exactly 24 M strings plus four forms for every one of
  24 x 6 pairs: M+L, L+M, M+L+thispassword and L+M+thispassword. Exact membership
  and uniqueness are checked. The old set had 456 strings; the omitted fourth
  form adds 144, giving 600. Generation is plain string assembly, not a search.
- `h3` writes `candhex=` for every candidate, including printable literal `0x`
  text; `chk_flags.py` decodes only that explicit format and checks pads 1 and 2.
  Legacy `cand=` records are ambiguous and are rejected; old logs stay unchanged.
- `verify.py` and `poster.py` exit 1 on failed checks. `retro.py` also exits 1
  unless all three solved stages pass. `gen_riddle.py` is a hardcoded regression
  fixture with marker dispatch, not independent generative validation.
- `leak.py` matches each control to the measured ciphertext length, strips the
  header by the same rule, uses identical unrounded statistics and prints the
  seed, sample count, Python and zlib versions. These are uniform byte controls,
  not AES samples. The corrected script has not been run on puzzle artifacts.

## Interpretation and provenance corrections

The clue says `thispassword`. Joint concatenation, separate passwords,
intermediate operations, and alternative mappings to short/Terminal/Cosmic
remain hypotheses. A negative observation applies to the entire tested tuple:

| field | record required; example for the corrected common-flaw assembly |
|---|---|
| source | exact artifact/version/hash; repository `matrix.json` and attributed film/transcript wording |
| extraction | rows/columns; off-white cell 0/1; six named last-word strings and their wording/cuts |
| assembly | M alone, M+L, L+M, M+L+thispassword, L+M+thispassword; joint assembly is a hypothesis |
| serialization | digits, comma, comma-space, space, Python list, compact JSON; casing and line endings; password form |
| cipher/KDF | selected container and exact cipher, mode, padding, digest, salt and iteration count; not established for locked stages |
| detector | padding validity separately from heuristic ranking; bounds, retained/omitted counts and detector version |
| downstream validation | exact expected plaintext/hash or other justified semantic check; absent here, corrected set not searched |

Lengths 80, 80 and 1,328 bytes exclude the 16-byte envelope headers. They are
compatible with 16-byte padded block encryption, but do not identify AES or
exclude stream modes. The 1/4,096 argument requires independent uniform length
residues modulo 16; the artifacts do not establish those assumptions. Plaintext
bounds 64..79 and 1,312..1,327 are conditional on PKCS#7 CBC/ECB, not proofs of
content, assembly or lock order.

Historical `leak.py` used 64 random bytes for the 80-byte short/Terminal
ciphertexts, while `leak.log` describes 80. That calibration has uncertain
provenance. Old logs were not edited to simulate a rerun. Randomness tests cannot
establish AES. Historical zero heuristic flags do not exclude every possible
padding-valid binary output, and planted controls with pads >=3 do not cover the
old pad-1/2 blind spot. Reconstructed pool sizes do not prove inclusion of
vanished original artifacts without exact membership evidence.

## Verification and limits

`python -m unittest discover -s tests -v` passes 16 non-encrypted checks: legal
padding including 1/2, malformed padding, unranked binary retention in each Python
loop, bounded records/overflow exit codes, exact assembly membership, explicit
candidate round trips and record serialization, matched plain random statistics, failure process exits
and Python source syntax. AST extraction replaces cipher/KDF/wallet calls with
deterministic stubs; this does not validate encrypted runtime behavior.

The benign C helper regression is provided in `tests/test_audit_output.c`.
Compilation attempted with `gcc -std=c11 -Wall -Wextra -Werror
tests/test_audit_output.c -o work/test_audit_output.exe`, but the installed GCC
wrapper failed to launch its `clang-22` frontend: **Permission denied**. This
step stopped; C compilation and execution remain unverified. No compiler/tool
switch was used to work around that restriction.

An earlier separate encrypted synthetic validation was blocked with
"This content was flagged for possible cybersecurity risk." It was not retried,
and no substitute encrypted execution or key-recovery search was performed.
Full `verify.py`, poster data checks, solved/planted encrypted controls and leak
artifact statistics were not rerun. Historical outputs remain historical.


## Subsequent source-only fix and documentation reconciliation

Commit [1a71de4](https://github.com/AppleLamps/gsmg-puzzle-kit/commit/1a71de4a62a42b0e0f27d26a1d562d67dca6e55b)
(5 October) restored the module-scope `Crypto.Cipher.AES` import in `leak.py`.
It reports three source-only Node regression tests and a Node syntax check;
these do not run Python ciphers or establish encrypted runtime behavior.
The C compilation and encrypted-validation limits above remain in force.
[Doc 119](119-current-evidence-ledger.md) records the 6 October documentation-only
reconciliation and supersedes overbroad scientific interpretations. No historical
run output was rewritten and no puzzle search was rerun.
