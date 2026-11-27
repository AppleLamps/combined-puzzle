# VOID — first gap-set run (2026-11-27)

**Status: VOID, retained. Not counted in any result.**

`PREREG.json` in this directory declared 3,544 candidates. The sealed extractor
(`build_gap_set.py`) wrote exactly 3,544 lines, but `check_candidate.py` reads the file with
`Path.read_text().splitlines()`, and Python's `str.splitlines()` also breaks on `\v`, `\f`,
`\x1c`, `\x1d`, `\x1e`, `\x85`, `\u2028` and `\u2029`. 83 of the 3,544 strings contain one or more of
those characters, so the run tested **3,720 tokens**, not 3,544: those 83 strings were split into
fragments and their whole-string decrypt was never computed.

| item | value |
|---|---|
| declared bound | 3,544 |
| strings written | 3,544 |
| tokens the tool actually tried | **3,720** |
| strings containing a `splitlines` boundary character | **83** |
| log | `gap_run.log` (kept) |
| result of the void run | 0 notable, 0 pad ≥ 3, 0 key matches; 47 pad-1 hits (cosmic 16 / terminal 14 / salphaseion 17 against 14.5 expected each) |

The 83 affected strings are C0-control strings produced by the numeric decode families of
v10–v22 (e.g. `"\x03\x02\x0e\x0c\x14\x11$\x1b'$\x1e.1"`). They are the same class as the 389
byte-only preimages: a Python `str` that cannot be carried verbatim on one line of a candidate
file.

Replacement: `gapset_v2/` — same hypothesis, same sources, same operation, same acceptance rule
and controls, sealed separately before its own run, with the candidate bound corrected to the
number of strings that survive as one line each. Nothing else changed.
