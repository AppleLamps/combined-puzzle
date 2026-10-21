# Last-words referents and prime sum lists → L5 gate + envelopes — 2026-09-13

**Result: null.**
- **L5 DBBI pattern:** 0 matches in 188,112 digest checks.
- **Envelopes:** 0 notable results in 188,112 trials. Pad counts are at chance: 750 pad=1 vs 731.9 expected, and 5 pad=2 vs ≈2.9 expected.

The reading behind the list is in `09_UNFORESEEN_HINT_AND_LAST_WORDS.md`.

## What was checked

Candidate list: `candidates.jsonl`, sha256 `e73a2be8…31fc`, **15,676 unique strings**. The list was pre-registered in `manifest.json` before the run.

| Group | Passage (exact source wording) | Unique strings* |
|---|---|---|
| P1 | Scott Manning transcript (`rabbit/tools/arch_src2.md`) line 105: the Architect's speech that ends "…she is going to die, and there is nothing that you can do to stop it.", just before _Neo walks to the door on his left_ | 2,140 |
| P1 | Same speech, kedri wording (`reference_texts/…transcript.txt` line 52), cut at "stop it." and in full (that version puts "Hope: …" before the choice) | 1,895 + 2,151 |
| P1 | Neo's last words before the choice: "No!" | 10 |
| P2 | Words before the Architect's "As you adequately put, the problem is choice." (both wordings), and through that sentence | 562 + 458 + 675 |
| P3 | Lines before Neo's "Choice. The problem is choice.": Architect "Precisely. As you are undoubtedly gathering…" and Neo "…either no one told me, or no one knows." (both wordings) | 202 + 119 + 130 + 26 |
| P4 | Puzzle Architect text up to its choice verb: "…REINSERTING THE PRIME BASICS AFTER WHICH YOU WILL BE REQUIRED TO" | 2,936 |
| P5 | Whole puzzle Architect text, ending "…I REALLY HOPE YOURE THE ONE CIAO BELLA O" | 3,558 |
| X | After the choice (control group of ideas already tested elsewhere): "Humph. Hope, it is…" / "If I were you…" / "We won't." | 670 |
| SUM | L1: 479/484 in both orders, 963, the yellow and blue prime lists; L2: prime-matrix row, column and abs-column sums for 7×12 and 12×7; "yellow479blue484", "yellowblueprimes", PRIVATEKEY. Each list with separators none / space / comma / comma-space / `[a, b]`. | 144 |

\* Strings are deduplicated across groups and credited to the first group that produced them.

**Pieces of each passage:**
- every suffix ("last N words") for N = 1 … all
- every sentence
- every clause (split on `, ; : . ! ?`)

**Forms of each piece:**
- as written, lower, upper
- no-whitespace ×3 cases
- alphanumeric lower; letters-only lower/upper
- +LF, lower+LF
- straight and curly apostrophes

**Checks per string:**
- **L5 gate:** sha256 / sha256d / sha256-of-hex / sha3-256 × forward / char-reversed / byte-reversed hex, compared to the DBBI `bg` equality pattern. Chance per digest 2^-211.7.
- **Envelopes:** Terminal, SalPhaseIon short and Cosmic Duality, under the profiles gsmg (proven convention), raw, gsmg-md5 and raw-md5. Every pad-valid plaintext was scanned for Half / Better Half keys (raw 32-byte windows, hex64, WIF, base64). "Notable" means pad ≥ 3 or a key match.

## Controls

- `check_candidate.selftest()`: the envelope code opens the real Phase 3.2 envelope (pad 10, 2,422 B), hash160 of Half's pubkey, EC k=1, WIF and the detectors → PASSED.
- **L5 gate:** a synthetic DBBI-substituted hex matches; the same hex with one nibble changed does not.
- **Key scan:** check_candidate's pure-Python EC costs ~12 ms per 32-byte window (~15 s per pad-valid Cosmic plaintext), so `scalar_hits` was replaced by a `coincurve` version.
  - Before use it was asserted identical to the original on 24 scalars: 1, 2, 3, N−1, 20 random, and a planted k=1 target → passed.

## History of this run (kept honest)

1. **First attempt** (script sha256 `1bec7f62…`, same candidate file) used the pure-Python scan. It was stopped after 30 min with no output written, because it would have needed ≈70 min.
2. **Script change:** only the `coincurve` swap and its equivalence assertion were added. `build` was re-run; `candidates_sha256` was unchanged (`e73a2be8…`); the new script sha256 is `c47fdeb3a83a…`.
3. **Second run:** 36.6 s, and this is the result reported above.

## Scope of this null

- **Covers:** exactly the strings in `candidates.jsonl` under the forms, views and profiles above.
- **Does not cover:**
  - arbitrary word windows that are not suffixes, sentences or clauses
  - other transcripts (subtitle tracks, the shooting script)
  - other hashes or encodings
  - other DBBI token maps
  - using the passages as a *key or selector* on DBBI/FAED rather than as the answer string

## Verification

```
python run_last_words.py build   # 15,676 candidates, candidates_sha256 e73a2be8acb4…, script_sha256 c47fdeb3a83a…
python run_last_words.py run     # SELFTEST PASSED; coincurve == pure-python on 24 scalars; gate_hits [] ; n_notable 0
```

## Files

| File | Contents |
|---|---|
| `run_last_words.py` | `build` / `run` |
| `manifest.json` | candidate and script sha256, source file sha256s, gate and envelope definitions |
| `candidates.jsonl` | `{src, cand}` per line |
| `results.json` | counts, pad histogram, gate hits (none), notable (none) |
| `run_stdout.txt` | console output of the second run |
