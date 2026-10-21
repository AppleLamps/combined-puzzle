# GSMG puzzle solve-attempt harness

Actual candidate-testing scripts against the three locked containers
(Terminal, SalPhaseIon-short, Cosmic Duality), building on the verified
primitives in `../gsmg_verify/lib.py`. See `../../SESSION-LOG-135.md` for
the write-up of what these tested and found (records 135–140: all null).

`harness.py` is self-contained — it re-derives the phase 1→2→3→3.2 chain
and all three container blobs directly from `source/` on import, and
exposes:

- `test_candidate(answer)` — tries an answer under the two established
  password profiles (`sha256(answer)` as 64 lowercase hex ASCII, and the
  raw UTF-8 bytes directly), each under **both EVP-SHA256 and EVP-MD5**
  key derivation, against all three containers, and content-checks any
  valid-padding plaintext with `recognize()` (printable-ASCII, EBCDIC
  across 6 codepages, UTF-16 zero-byte alternation, magic headers,
  bit-position bias, distinct-byte deficit, and a scan of every 32-byte
  window as a raw private key against both the prize and sentinel HASH160
  targets, plus four mathematically related, unauthenticated on-chain addresses). Related-key hits
  are labeled separately and normalized to a prize-key candidate; this is
  applied to raw 32-byte windows and 64-character hex scalars, never to
  arbitrary password text. Every valid-padding hit is automatically **chained** — tried
  as a candidate password (raw bytes / hex-of-bytes / sha256-hex, both
  digests) against the *other* two containers, up to depth 2 — since a
  correct short binary intermediate can look exactly like random noise
  until it opens the next lock.
- `run_positive_control()` / `run_negative_control()` / `run_recognizer_controls()` /
  `run_chaining_control()` — must all pass before trusting any candidate
  result. Every `attempt_*.py` script calls all four at the top.
  `print_chain_summary()` reports what chaining found; call it at the end
  of an attempt script (all seven already do).

**Gotcha this session hit once**: the phase-3 answer's part 6 (the
byte-reversed Bitcoin genesis message, hex-encoded) must use **uppercase**
hex letters — it feeds into a `sha256` of the literal answer string, so
`0x73...` and `0x736B...`'s lowercase equivalent hash to different
passwords even though they're the same bytes. `harness.py` gets this right
(`.hex().upper()`); if you re-derive it yourself, don't drop the `.upper()`.

## Running

```
python3 harness.py              # controls only, no candidates
python3 attempt_select.py       # record 135
python3 attempt_matrix.py       # record 136
python3 attempt_keyed.py        # record 137
python3 attempt_faed_matrix.py  # record 138 (likely overlaps dossier doc 96)
python3 attempt_labels.py       # record 139
python3 attempt_filmchoice.py   # record 140
python3 attempt_lastcommand.py  # record 141 (see ../../SESSION-LOG-141.md)
```

Each script prints every valid-padding hit it finds (container, profile,
digest, candidate, pad length, recognizer findings), then a chaining
summary, then a final NULL/hit summary. `test_candidate` deduplicates on
exact candidate bytes across a script run and `report()` prints both the
invocation count and the smaller "distinct candidates actually tested"
figure — the latter is the number to quote. As of this session (after fixing
the digest/recognizer/chaining gaps a PR review caught), all seven report
NULL: every primary hit was pad-1 (one pad-2), the handful of chained
secondary decrypts (3 total, across records 137/138) were themselves
unstructured pad-1 noise, and the recognizer found nothing in any of them.

Decryptions are cached across runs in `out/decrypt-cache.sqlite3`, keyed by
container SHA256, candidate-byte SHA256, password profile and EVP digest.
The cache retains valid-padding plaintext for rescanning after recognizer
changes, but never stores password bytes. Set `GSMG_CACHE_PATH` to an alternate
path, or to the empty string to disable persistence. The pre-existing attempt
scripts can be rerun to warm this cache; historical log summaries alone do
not preserve every plaintext and therefore cannot be rescanned losslessly.
