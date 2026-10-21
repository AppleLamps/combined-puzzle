#!/usr/bin/env python3
"""
The earliest orphan in the GSMG puzzle: the Phase 2 block

    # X 2 S H 4 Y 0 Q B 15 #

Phase 2's plaintext defines riddles for four of its ten tokens and nothing
else. The block is never consumed by any later step -- the Phase 3 password is
the seven concatenated clue-parts, and none of them is X2SH. Six years on,
the group was still arguing about it on the last day of the export.

Run from anywhere: python3 analysis/x2sh.py
"""

BLOCK = "X 2 S H 4 Y 0 Q B 15".split()

SOLVED = {
    "S": (32, "cha' + (vagh * jav) -- Klingon 2 + (5*6). Unambiguous."),
    "H": (-42, '"(Answer to only this puzzle but nothing else) * -1" -- '
               "Hitchhiker's 42, negated. Sign still argued: 42 vs -42."),
    "Q": (82, '"extend the name of a hackers\' swordless fish, the I and W are '
              'below" -- Qwerty is Elliot\'s fish in Mr. Robot; extend to '
              "QWERTYUIOP under the digit row; I sits under 8, W under 2."),
    "B": (-16, "((BV80605001911AP) - sqrt(-1))^2 -- that part number is an "
               "Intel Core i5-750, so (5i - i)^2 = (4i)^2. Sign still argued: "
               "-16 vs 25."),
}

WIDTHS = [
    ("rabbit matrix (phase 1)", 14),
    ("chess position (phase 2, part 7)", 8),
    ("QWERTYUIOP over the digit row (phase 2, the Q riddle)", 10),
    ("the X2SH block itself (phase 2)", 10),
    ("VIC straddling checkerboard (phase 3.2.2)", 10),
]


def main():
    print("THE BLOCK\n")
    print("   #", ' '.join(BLOCK), "#\n")
    print(f"   {len(BLOCK)} tokens.\n")

    print("WHAT IS SOLID\n")
    for k in "SHQB":
        v, why = SOLVED[k]
        print(f"   {k} = {v:>4}   {why}")
    print()
    print("   substituted: #", ' '.join(str(SOLVED.get(t, (t,))[0]) for t in BLOCK), "#")
    print()
    print("   X and Y are the ONLY tokens the puzzle never gives a riddle for.")
    print("   It defines exactly what it wants substituted and leaves two unknowns.\n")

    print("WHY IT IS AN ORPHAN\n")
    print("   The Phase 3 password is the seven clue-parts concatenated and hashed:")
    print("   causality / Safenet / Luna / HSM / 11110 / genesis-block hex / chess FEN.")
    print("   X2SH is not among them. Nothing downstream has ever consumed it.")
    print("   2021: 'it is still uncertain what that is for'")
    print("   2023: 'X 2 S H 4 Y 0 Q B 15 doesn't seem useful as well to go to phase 3'")
    print("   2026: still being argued on the final day of the export.\n")

    print("THE TWO READINGS TRIED, AND HOW BOTH MISS\n")
    print("   (a) Coordinates of the ex-SafeNet building, Rotterdam.")
    print("       2023: 'several hundred meters off ... assuming the coordinates go")
    print("       down to seconds we should have a match down to a meter accuracy.'")
    print("   (b) Decentraland parcels, pairing the block into (2,0) (32,82)")
    print("       (-42,-16) (4,15). GSMG's estate is at (-41,-16) and (-41,-17).")
    print("       The block gives (-42,-16). One parcel east.")
    print("       2026, the solver's own verdict: 'jrk didn't make the coordinates")
    print("       land directly on the old safenet address either ... strong argument")
    print("       for we got our interpretation wrong thinking we are right here.'\n")
    print("   Two independent readings, two near-misses. In a puzzle where every")
    print("   other answer lands exactly, a near-miss is a wrong reading.\n")

    print("THE THREAD THAT WAS DROPPED\n")
    print("   Phase 3.2's VIC-cipher hint reads:")
    print('     "A fubcd-king & oracle-queen, thingky mvps, on a sad board')
    print('      but AS WIDE AS THE FIRST ONE SEEN."')
    print()
    print("   In 2023 one member asked what that first board is, ruled out the")
    print("   rabbit matrix and the chess board, and named X2SH as a candidate.")
    print("   The reply was 'I don't think we've figured that out yet'. Nothing since.\n")
    print("   Widths in the puzzle, in the order you meet them:")
    for name, w in WIDTHS:
        star = "  <--" if w == 10 else ""
        print(f"      {w:>3}   {name}{star}")
    print()
    print("   The X2SH block is 10 tokens, and the Q riddle inside it builds a")
    print("   10-wide board out of QWERTYUIOP and the digit row -- the first")
    print("   10-wide objects in the puzzle, and the VIC checkerboard is 10 wide.")
    print("   That is a lead, not a solution: the VIC decode already succeeded")
    print("   without it. But nobody has ever tested whether X2SH is the board")
    print("   the hint is pointing at.")


if __name__ == "__main__":
    main()
