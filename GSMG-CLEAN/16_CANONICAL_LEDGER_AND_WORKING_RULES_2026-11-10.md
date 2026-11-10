# 16 - Canonical ledger, working rules, and the first runs under them

**Status (2026-11-10): UNSOLVED.** No envelope was opened and no key was found. This file changes how
the work is done, records where the ten research directories disagree and which statement stands, and
reports the first experiments run under the new rules. All three are null.

## 1. This folder is the canonical ledger

`GSMG-CLEAN/` is the single source of truth for the combined repository. The other nine directories
are frozen snapshots of earlier or parallel work. Each of them now carries a `CANONICAL_NOTICE.md`
that lists the places where it disagrees with this folder. Where a snapshot and this folder differ,
this folder stands until a run recorded here says otherwise.

New findings go here: a numbered document for the reasoning, a `runs/<date>_<name>/` directory for the
evidence. Do not open a new ledger in another directory.

## 2. Working rules

1. **No envelope sweeps.** Nothing is tried against Terminal, SalPhaseIon short or Cosmic Duality
   unless it is the output of a derivation that already checked itself without AES.
   `tools/check_candidate.py` enforces this: it refuses to decrypt without `--derivation runs/<dir>`,
   and that directory must hold a sealed statement and a recorded self-check with outcome `passed`.
   The number of candidates is capped by the run's own bound (hard limit 256).
2. **Every experiment predicts a second artifact before it generates anything.** The statement is
   written with `tools/prereg.py new`, sealed with `tools/prereg.py seal` (which refuses if the run
   directory already holds output), and committed before the results. The four artifact types are:

   | type | meaning | checker in `tools/oracles.py` |
   |---|---|---|
   | `readable_text` | the output reads as language, against shuffled-input controls | `english_score` |
   | `known_digest` | sha256 of the output is a digest authenticated in 01 | `known_digest` |
   | `known_address` | the output derives a marker address (01 section 9) or a prize address | `known_address` |
   | `exact_reconstruction` | the output reproduces a held artifact character for character | `longest_common_run` |

3. **A null counts only when its planted control fired.** A run whose control did not fire is void,
   stays in the repository with a `VOID.md`, and is rerun under a new sealed statement.
4. **Padding is not evidence.** A wrong key passes PKCS#7 about once in 256 tries. See 05 section 1
   and 14 section M6.
5. **Measurements are exempt from rule 2** when they generate no candidates (for example the FAED
   statistics in section 5). They still ship a script and a result file.

Why these rules: `gsmg-puzzle-kit` alone records 7.29 billion decrypt tests through its doc 115
(`claude/critical-review-2026-10-03.md:50`) and a further 26.8 billion in doc 116
(`claude/116-coverage-gaps-closed.md:18`). Every one was judged by padding or a recogniser run on
padding-valid output, and none of them moved the solved boundary. The creator's
own framing is that the remaining step is small ("1 microstep", #32579; "in front of your eyes",
#8446). Volume has not been the constraint.

```
python tools/prereg.py new runs/2026-11-10_example
python tools/prereg.py seal runs/2026-11-10_example
python tools/prereg.py record runs/2026-11-10_example --outcome null --evidence runs/2026-11-10_example/results.json
python tools/oracles.py
python tools/check_candidate.py --derivation runs/2026-11-10_example "answer"
```

## 3. Where the directories disagree, and what stands

Every line was checked in the cited file on 2026-11-10.

| Topic | Stated elsewhere | Stands here | Basis |
|---|---|---|---|
| Cosmic Duality "decrypt" `4f7a1e4e...` | `5g-puzzle/packet/RESULTS.md:16` "Reproduced"; `5g-puzzle/AUDIT.md:41` uses it as the harness self-test; `5g-puzzle/SYNTHESIS.md:23` "Cosmic Duality AES is already open" | Not a decrypt. A pad-1 output under MD5 key derivation, retracted | 05 section 1; `5g-puzzle/analysis/FINDINGS.md` Addendum 11 says the same |
| `HILLFEXMGSGQ` then `BTCSEED` then `IFINDO` | `gsmg-haiku/STATUS.md` "Latest result" (2026-10-15) | A tested hypothesis, not a result. The 7x12 shape is chosen, not derived; `btcseed` appears for 4 of 40,320 key orders and `seed` for 480 | 14 section M2; 03 section 4; and section 5 below: FAED has no letter-level structure for a Hill or Bifid layer to act on |
| FAED with `g` as a hidden zero, "2^107, not enumerable" | `gsmg-puzzle-kit/claude/GSMG-PUZZLE-DOSSIER.md:1129` and `:2057`, docs 115:42 and 116:89; `gsmg/GSMG-PUZZLE-DOSSIER.md:1048`; `gsmg-1.2/...:996`; `gsmg-1.2-2/...:1023` | **Closed as text.** The last 32 letters of FAED contain no `g`, and the low four bytes of the integer depend only on the last 32 digits, so they are `c7 bb c0 75` for every choice. As a binary object it cannot be checked without AES, which rule 1 excludes | section 5; `grok-gsmg-puzzle` has the same tail argument; `gsmg-haiku/mywork/LOG.md` entry 8 saw the branch die after one byte |
| FAED homogeneous | The four dossiers: "homogeneous P = 0.45 at 19 blocks, once the last 32 chars are removed ... Carry faed as one object" (kit `:1100`) | **Not homogeneous.** Blind quarters p = 0.001; quarters of the first 538 letters p = 0.004; corrected for choosing the cuts p = 0.005 | section 5. `gsmg/claude/118-contrarian-pass.md` reached the same conclusion; its count of exactly four pieces is not established |
| DBBI parse length | `gsmg/GSMG-PUZZLE-DOSSIER.md:956` "L=83, settled"; `gsmg-puzzle-kit/claude/119-current-evidence-ledger.md:44` "L=83 is preferred"; `gsmg-1.2` and `gsmg-1.2-2` withdraw it for an 84-cell reading | Both complete parses stand (83 and 84 cells). They share 82 cells; neither is selected | `runs/2026-09-14_dbbi_forward_comparison/REPORT.md`; `tools/dbbi_step2.py operands` re-derives exactly these two |
| `Yellowblueprimes:317/557`, `Another door:137/143` | `gsmg-1.2/GSMG-PUZZLE-DOSSIER.md:14-18` and `:1784`, `gsmg-1.2-2/...:14-18` and `:1811`: "recent evidence" from "the user's screenshot", said to support the 84-cell model | **Not evidence.** The numbers are two chat messages from a solver, not the creator (#73708 and #73710, 2026-09-26, `gsmg-haiku/ChatExport_2026-10-08`). Both pairs can be computed from DBBI alone under the 84-cell parse, so agreeing with that parse is circular | section 4 |
| The creator's "zeroed out" hint is unsafe | `5g-puzzle/WHAT_THE_GROUP_MISSED.md:38` and `:180`, `5g-puzzle/NEXT_BEST_MOVE.md:33`: #8000 was edited 2026-02-15 | The wording is safe. It is forwarded verbatim in #29342 (2024-11-10) and pasted with its original date in #30086 (2024-11-14) | 02 "Read this first": most late edit stamps are reaction bumps |
| The answer needs outside or personal knowledge | `puzle/round55.md:40`: the final key is `sha256(X)` for a text the creator's friends know | An unresolved tension, not a conclusion. #9607 "You have all the info" is a direct reply to that question | 02 section 10; 15 |
| The 479 "yin-yang milestone" | `puzle/README.md:26-36` headlines it (and tags it fitted) | A pointer with no payload: 476 literal outputs null on every exact oracle | 14 section M4; `runs/2026-09-14_m4_zeroing_oracles/REPORT.md` |
| Envelope batteries as the live target | `grok-gsmg-puzzle` rounds 1 to 14; harness instructions in `gsmg-puzzle-kit/CLAUDE.md` | Stopped by rule 1 | section 2 |

## 4. The 317/557 and 137/143 numbers

Two forks carry these as a clue. The arithmetic is exact and was reproduced here:

- In the 84-cell parse the primes under `be` (yellow) sum to **317** and the primes under `b` (blue)
  to **557**. The 83-cell parse gives 400 and 474.
- With a=0..i=8 the 61 ordinary cells sum to **280**, and on a 6x14 board the row sums are
  41, 56, 48, 40, 48, 47, so alternate rows give **137** and **143**.

The source is not the creator. `Ugur Keser` posted "Yellowblueprimes : 317/557" (#73708) and "Another
door : 137/143" (#73710) on 2026-09-26, eight days after the same account posted "Dbbbi part is solved"
with a description of the prime-slot parse in its 83-cell form (#72211, #72215). No creator message
follows; the last creator message in any export here is 2026-09-01. Both pairs can be computed from
DBBI alone under the 84-cell parse, so a model that reproduces them has confirmed nothing about itself.

Two side observations, both found after looking and both weak:

- 137 and 143 are not specific to the 6x14 board. Of 20 natural row and column splits, the chance
  that at least one lands on a given pair with that total is about 80%.
- The dossiers note that pixel (317, 557) of the poster lies in the off-white cell. That is about a
  1 in 200 coincidence and has no consumer.

## 5. What FAED's own letters allow

`python tools/faed_surface_statistics.py` writes `runs/2026-11-10_faed_surface/results.json`.

| Measurement | Result | What it rules out |
|---|---|---|
| Letter counts | a54 b49 c52 d49 e69 f57 **g107** h58 i75; `g` is 1.85 times the mean of the others | - |
| Adjacent letters independent | chi2 74.3, permutation p = 0.18 | Any direct letter-for-letter image of English, including many-to-one maps |
| Periodicity, periods 2 to 40 | best 0.127 against a shuffle median of 0.126 | Short repeating keys |
| Checkerboard tokens, every one- and two-letter prefix set | best IC 0.1122 against a shuffle median of 0.1123 | Straddling-checkerboard readings |
| Homogeneity | quarters p = 0.001; first 538 letters in quarters p = 0.004; 19 blocks of 30 p = 0.005; best of 210 cut sets p = 0.005 | One decimal expansion of one number; one stream from one cipher |
| Tail | last 32 letters hold no `e` and no `g`; low four bytes fixed at `c7bbc075` | FAED as text under the page's decimal codec with `g` as zero |
| Any single letter as a hidden zero, both directions | 0 complete printable texts; planted control recovered | The same for the other eight letters |

Read together: FAED has no sequential structure but its letter mix drifts. Short-key classical ciphers
on English (Vigenere, Beaufort, Hill, Bifid, checkerboard, transposition) have nothing to act on and
can be retired as a class rather than variant by variant. A single big number is out as well. What
remains is several objects in a row, something under a long key, or material that is not a message.
None of those can be decided by decoding FAED alone.

## 6. Step two, worked forward from DBBI

The creator's order (#8446) is `yellowblueprimes`, `matrixsumlist`, `lastwordsbeforearchichoice`,
`yinyang`. Step one is the DBBI prime-slot parse. Three hypotheses about what step two does with the
60 or 61 ordinary cells were sealed and committed before any output existed. `tools/dbbi_step2.py`
runs them; none touches an envelope.

| Run | Hypothesis | Predicted artifact | Outcome |
|---|---|---|---|
| `runs/2026-11-10_step2_carried_code` | The ordinary cells are "the code you hopefully carry": a code already held from the solved chain, spread over the non-prime cells | 12 or more consecutive cells equal a registry string, or 20 or more are a one-to-one relabelling of one (269 strings, 24,897 characters) | **Null.** Longest exact run 7 digits (shuffle maximum 8 to 10); longest relabelled window 10 cells (shuffle maximum 13 to 14) |
| `runs/2026-11-10_step2_gap_sums_v2` | `matrixsumlist` names what the cells become: sums over the stretches between markers, or over a board with the prime cells zeroed | A readable reading, a run of the poster's row or column sums, or a digest or address hit | **Null.** Best score -6.76 against a control maximum of -3.87; no exact hit |
| `runs/2026-11-10_step2_sumlist_lastwords_v3` | The sum list counts back from the Architect's choice in the film scene and selects letters or words | A readable selection | **Null.** Best score -5.16 against a control maximum of -4.36 (3,240 selections) |

Planted controls fired in all three. Three earlier attempts are void and kept: the first gap-sum run
(its control could not be built), and the first two last-words runs (one crashed, one read its control
one position off because two labels were swapped). The real outputs of the void runs were null as well,
but they are not counted.

Limits, stated in the sealed statements:

- The gap-sum and last-words tests judge short strings (12 to 24 letters) by a score that an ordinary
  short English phrase does not always beat. The ten best real outputs of each run are saved for
  reading; none is a word sequence.
- The carried-code registry holds what the solved chain gives a solver. A code from outside the
  chain is not covered.
- These runs close three declared readings. They do not show that the ordinary cells are filler.

## 7. What is still open

1. What the ordinary cells are. They have no zeros and only two `b`, which fits neither a plain
   decimal number nor random filler over nine letters (two `b` in 61 cells has probability about 0.03).
2. Which of the two parses is intended. Nothing authenticated selects one.
3. Whether FAED is an operand at all. Its drift says it is not one clean object.
4. What `yinyang` names. The creator calls it the next phase (#39237) and has never tied it to an
   envelope.

## 8. Reproduce

```
python tools/oracles.py
python tools/check_candidate.py --selftest
python tools/faed_surface_statistics.py
python tools/dbbi_step2.py operands
python tools/prereg.py verify runs/2026-11-10_step2_carried_code
```

The three experiments were run with the script versions whose hashes are in each `PREREG.json`
(`method.script_sha256`); those versions are in the git history of this branch. Building the gate
included one live check of the unlocked path: two placeholder answers (`a`, `b`) were run through
`check_candidate.py` under a throwaway derivation. Both failed to decrypt, as expected.

`SHA256SUMS.txt` predates this file and does not list it or the 2026-11-10 tools and runs.

## 9. Snapshot integrity: three plaintext files were damaged on import

The combined snapshot carried `data/phase2_plaintext.bin`, `data/phase3_plaintext.bin` and
`data/phase3_2_plaintext.bin` with their CRLF line ends converted to LF: 642, 4,032 and 2,411 bytes
instead of the authenticated 648, 4,090 and 2,422. Those CRLFs are puzzle bytes. `tools/verify_chain.py`
rebuilds the files from `originals/`; the rebuilt files are committed here and match the hashes in 01
(`e2f9dd65...`, `c4ad9455...`, `b82afeb8...`). `.gitattributes` now marks `data/*.bin` as `-text` so
that no checkout converts them again. The three locked envelopes were not affected.

Of the 152 files listed in `SHA256SUMS.txt`, 91 match, 52 differ only by line endings (text files),
and 9 are documents or tools edited after the list was made.

Consequence for section 6: the carried-code run was made against the damaged copies, so two of its
269 registry strings (the Phase 3.2 introduction and board sentence, cut by byte offset) were a few
bytes off and the Phase 2 and Phase 3 clear text lacked its carriage returns. The measurement on the
real cells was repeated against the restored files with the sealed script version and is identical;
the shuffle controls were not repeated. See `runs/2026-11-10_step2_carried_code/RECHECK.md`.
