"""Decode the phase 3.2 149-digit block with every ordered pair of top-row blanks.

Alphabet `FUBCDORA.LETHINGKYMVPS/JQZXW` (phase 3.2 riddle). The top row holds the
eight digits that are not blanks; the two blank digits head rows 2 and 3.
Prints how many of the 90 ordered pairs give a complete parse and which ones
contain the crib words of the accepted plaintext.

Usage:  python3 src/checkerboard_pairs.py
"""

from __future__ import annotations

import itertools
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALPHA = "FUBCDORA.LETHINGKYMVPS/JQZXW"
CRIBS = ("CRACK", "PRIVATEKEYS", "HALFANDBETTERHALF", "FUNDSTOLIVE")


def decode(digits: str, blanks: tuple[int, int]) -> str | None:
    top = [d for d in range(10) if d not in blanks]
    table = {str(d): ALPHA[i] for i, d in enumerate(top)}
    i = len(top)
    for r in blanks:
        for d in range(10):
            table[f"{r}{d}"] = ALPHA[i]
            i += 1
    out, j = [], 0
    while j < len(digits):
        if int(digits[j]) in blanks:
            if j + 1 >= len(digits):
                return None
            out.append(table[digits[j:j + 2]])
            j += 2
        else:
            out.append(table[digits[j]])
            j += 1
    return "".join(out)


def main() -> int:
    pt = (ROOT / "artifacts" / "phase32.bin").read_bytes()
    digits = pt[1990:2139].decode()
    assert len(digits) == 149 and digits.isdigit()
    parsed, crib_hits = 0, []
    for pair in itertools.permutations(range(10), 2):
        s = decode(digits, pair)
        if s is None:
            continue
        parsed += 1
        if all(c in s for c in CRIBS):
            crib_hits.append((pair, s))
    print(f"ordered pairs 90, complete parses {parsed}, pairs containing all cribs {len(crib_hits)}")
    for pair, s in crib_hits:
        print(pair, s)
    return 0 if [p for p, _ in crib_hits] == [(1, 4)] else 1


if __name__ == "__main__":
    raise SystemExit(main())
