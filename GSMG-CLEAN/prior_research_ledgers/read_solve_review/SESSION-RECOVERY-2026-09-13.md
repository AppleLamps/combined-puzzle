# Puzzle session recovery — 13 September 2026

**Continuation update:** see [HILL-CONTINUATION-2026-09-13.md](HILL-CONTINUATION-2026-09-13.md) for the subsequent convention audit, source-dependency control, and nine negative coordinate-return trials. Those checks are completed; the puzzle remains unsolved.

The best restart point is the reproducible **DBBI prime construction → HILLFEXMGSGQ → candidate Hill relation → IFINDO…** chain. No complete new stage or private key was verified. Its calculations survive independent reproduction; its intended meaning remains a hypothesis. The late session's many confident interpretations should not be inherited as established findings.

## Sessions reviewed and why progress was lost

- **Analyze ADDRESS-INFO key generation**, thread `01a09848-c951-7881-985b-fb05bee5ff34`: address evidence, verification bugs, DBBI/VIC review, and broad cipher-family searches.
- **Analyze ADDRESS-INFO key generation (2)**, thread `01a098f4-2dbd-7300-9b3b-88adc2a0e986`: a fork containing earlier history plus the latest hint synthesis and continuation. Shared inherited turns are not independent corroboration.
- The later thread's actual local log is `C:/Users/lucas/.codex/sessions/2026/09/13/rollout-2026-09-13T00-08-54-01a098f4-2dbd-7300-9b3b-88adc2a0e986.jsonl`. The app's thread reader omitted the contents of its two latest turns, so I read that log directly.
- The final continuation began September 13 at **12:33 a.m. Eastern** and ended **3:27 a.m.**, approximately 2 hours 53 minutes later. It ended with a context-compaction error reporting `content_filter`, without a final answer. This is the recorded technical ending, not evidence that a key was discovered.

The behavioral loop was hypothesis churn: an attractive fragment or dimension was called decisive, a test failed, and a new interpretation was immediately called the strongest or only remaining one. Examples include treating IFINDO as `IFIND`, then `IF IN DOUBT`, then `I FIND O`; trimming different headers to obtain 277 or 276 characters; and using a lone z as an orientation marker without establishing that role. Distinct tests were often performed, but the assumptions were continually adjusted after seeing their outputs.

`SOLVE/STATUS.md` mostly describes earlier broad searches. `SOLVE/HINT-SYNTHESIS.md` captures the 479 idea but predates the late HILL/IFINDO work. Neither is a sufficient restart record alone.

## Best findings to retain

### 1. Prime reinsertion gives HILLFEXMGSGQ

I reparsed DBBI from the saved SalPhaseIon HTML, without importing the previous parse trace. Under the rule that prime-numbered logical slots contain `b` or `be` and other slots contain single letters, there are two complete parses:

| Logical cells | Prime markers | b | be | Nonprime values |
|---|---:|---:|---:|---:|
| 84 | 23 | 16 | 7 | 61 |
| 83 | 23 | 15 | 8 | 60 |

The 84-cell version agrees with the puzzle's 23/16/7 numbers. For that branch:

1. Preserve each nonprime letter as A=1 through I=9.
2. Replace a prime-slot `b` with minus its slot number and `be` with plus its slot number.
3. Fill seven rows of twelve in source order; sum each column.
4. Render those sums modulo 26 using A=0.

The sums are `[-45,34,37,37,-73,30,49,38,32,44,-124,42]`, yielding **HILLFEXMGSGQ** exactly. All 91 source letters are accounted for, including the final e=5.

This is more useful than arbitrary password guesses because the source explicitly supplies primes, `matrixsumlist`, and the 23/16/7 partition. However, the polarity, matrix dimensions, and mixed input/output numbering conventions are still chosen interpretations. Reproduction does not prove creator intent.

### 2. A specific Hill interpretation gives IFINDO…

The first 13 DBBI characters deduplicate to `dbifhceg`. Append unused letters of the no-J alphabet to obtain the 25-character square `dbifhcegaklmnopqrstuvwxyz`.

Bifid-decoding all 570 FAED characters as one block reproduces the historical candidate beginning `btcseed`. After those seven characters, the alternating streams have lengths 282 and 281.

Treating **FEXM → GSGQ** as a proposed Hill plaintext/ciphertext example, with digraphs as column vectors over the natural no-J alphabet modulo 25, gives:

```text
K     = [[1,19],[6,3]]
K^-1  = [[2, 4],[21,9]]
```

Applying K^-1 to the complete 282-character stream gives:

```text
IFINDONVFRVODTFMDRYQWBLXSFNPTCXLCLZDTTYCYKNCRBPKFAMZDXXESRTWTBGOQSCYHHFESFSXKHEQ...
```

I reproduced the full stream and verified the inverse round trip. The full result is saved in `session-recovery-check.json`.

**IFINDO is a literal prefix, not a verified instruction.** The proposed known-plaintext relation, alphabet choice, and stream choice need to remain explicit. The rest does not currently form a readable instruction. `LOVEGAAM`, derived through another chosen matrix, similarly does not establish a LOVE instruction or a mapping for the remaining data.

### 3. Keep DBBI minus VIC as a separate, weaker lead

Independent arithmetic reproduces a 91-character output consisting of 21 letters, `YOUWON`, then 64 letters. Neither those 64 letters nor the readable fragment has opened a verified stage. Previous work already tested extensive constrained hex, matrix, and source-text-key families. Do not restart those searches merely because the length resembles a key.

### 4. Retain the earlier evidence-quality fixes

- `phase3_plaintext.txt` in the workspace is misleading; use `PUZZLE-REVIEW/phase3-verified.txt` or the exact sourcebook copy.
- The original literal-key scripts had address-checksum and candidate-parsing bugs. The bounded corrected recheck found no matching candidate. See `ADDRESS-INFO/KEY-REVIEW-2026-09-13.md` for exact coverage.
- Some AES recognizers fail to recognize a known partly binary stage. Their negative results exclude only their stated acceptance classes. Conversely, valid padding is not authentication or proof of a correct password.
- The 1,327-byte Cosmic result from `hillfexmgsgq` has no verified downstream interpretation. Its one-byte padding and binary length are insufficient evidence of a successful opening. Random-looking bytes or a mismatch with an unverified external hash are also insufficient to prove a specific binary candidate impossible.

## Corrections that change the restart strategy

### The four-symbol stream is guaranteed by the Bifid setup

This is the most useful correction from this review. FAED uses only a..i, and all those letters occupy rows 0 and 1 of the chosen square. With an even-length, single-block Bifid decode, every even-indexed output character combines two row coordinates. It therefore must be one of square positions 0, 1, 5, 6: **d, b, c, e**.

Consequently the alternating b/c/d/e stream appears even for reordered source text. A fixed rotation control reproduced this restriction. It is not independent proof of a deliberately embedded base-4 seed, control stream, or yin-yang pair. This fact was also acknowledged in the older `btcseed_stats.py` analysis but was lost in the late session's reasoning. The exact BTCSEED prefix remains a separate observation; the algebra does not dismiss it.

### The 277-letter passage belongs to a different source

The supplied movie transcript contains 277 letters and 65 words from “the moment of truth” through “choice.” The decoded puzzle Architect text has 1,539 letters and contains **no literal `choice`**. The late session briefly noticed this, then resumed describing the film passage as an exact source-selected alignment.

The movie may still be relevant to `lastwordsbeforearchichoice`. What is missing is an independently justified choice of passage, starting point, tokenization, and stream-header removal. The numerical match alone cannot supply those decisions.

### 479 is a secondary clue, not a mandatory checkpoint

The saved color/primes construction sums to yellow 479 and blue 484; removing the blue contribution 5 balances them. I separately confirmed that zero-based letter 479 of the normalized puzzle Architect text begins `PRIVATEKEY`.

However, this review has not independently redone the poster pixel extraction. More fundamentally, first-24-prime assignment, removal of 5 to force equality, letters-only normalization, and zero-based indexing are selected operations. The prior synthesis overstates the claim as an intended route and required checkpoint. Retain it as a candidate observation, without forcing future work to pass through it. `Hush hush → hash/hash` likewise remains wordplay with unresolved operands and hashing conventions.

## How to continue without recreating the loop

The first continuation step has already been done: independently reproduce the strongest late chain, expose its assumptions, and save the complete output. The reproduction command is:

```powershell
node .\PUZZLE-REVIEW\session-recovery-check.cjs
```

It performs no password or private-key search. Its JSON records input hashes, both complete DBBI parses, the prime construction, Bifid result, full Hill stream, round-trip verification, structural control, and text-source mismatch.

The next unit of work should answer **one question: is HILL FEXM GSGQ genuinely an instruction for the FAED-derived stream?**

1. Trace the exact source basis for treating FEXM/GSGQ as a worked plaintext/ciphertext example. Record alphabet, direction, and column convention before judging new outputs. If another interpretation is proposed, state what source evidence selects it.
2. Preserve the full 282/281 streams. Do not discard IFIND, IFINDO, EECE, EECED, z, or a final e to manufacture dimensions. Any removal needs its own reason and must account for the removed data.
3. Examine whether IFINDO survives a properly scoped control for the selected construction, with the earlier variant search acknowledged. Do not multiply naive word probabilities across dependent observations.
4. Use `lastwordsbeforearchichoice` only with an explicit choice between puzzle plaintext and film transcript. Derive the complete selector before testing it. The existing 277-letter running-key, word-end, base-100, 23x12, THISPASSWORD-columnar, and interwoven 16/7 families have already returned no verified continuation.
5. Apply the established SHA-256-hex / EVP-SHA256 / AES-CBC workflow only once a complete candidate object is justified. Preserve full binary output where padding is valid, but require independent structure or a verified next stage before calling it solved.

At the end of that bounded investigation, either record a complete improvement or explicitly downgrade this branch. An unsuccessful interpretation is not evidence for whatever reinterpretation comes next.

### Ready-to-use continuation brief

> Read this recovery note and session-recovery-check.json first. Continue the GSMG puzzle from the reproducible HILLFEXMGSGQ / IFINDO candidate chain. The puzzle remains unsolved. Do not treat the four-symbol Bifid stream as independent evidence; it follows algebraically from the square. Do not silently switch the puzzle Architect plaintext for the supplied film transcript. Preserve every source character and label all chosen conventions. First establish whether the Hill relation is intended, then derive a complete next operation from source evidence. Consult existing SOLVE results before any test and stop expanding a failed interpretation without new evidence. Report calculations separately from inferred meaning.
