#!/usr/bin/env python3
"""20% extra-door packet: yellow/blue counts on the published first-piece image."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from PIL import Image

IMG = Path(__file__).resolve().parent / "artifacts" / "puzzle.png"
OUT = Path(__file__).resolve().parent / "out" / "extra_door_pixels.json"

# Exact palette of puzzle.png (not HSV). HSV previously counted blue as 96791.
YEL = (255, 242, 0)
BLU = (63, 72, 204)
BLK = (0, 0, 0)
WHT = (255, 255, 255)
GRY = (254, 254, 254)
RED = (237, 28, 36)


def palette_bucket(r, g, b, a):
    p = (r, g, b)
    if a < 200:
        return "transparent"
    if p == YEL:
        return "yellow"
    if p == BLU:
        return "blue"
    if p == BLK:
        return "black"
    if p == WHT:
        return "white"
    if p == GRY:
        return "grey_cell"
    if p == RED:
        return "red"
    return "other"


def main():
    im = Image.open(IMG).convert("RGBA")
    c = Counter()
    for px in im.getdata():
        c[palette_bucket(*px)] += 1
    yellow, blue, red = c["yellow"], c["blue"], c["red"]
    report = {
        "source": "https://raw.githubusercontent.com/puzzlehunt/gsmgio-5btc-puzzle/master/puzzle.png",
        "hint": "Jrk #1710 as quoted 2020-04-08 #3388: Yellow has a number and so does Blue. Go back to the first puzzle piece.",
        "size": list(im.size),
        "counts": dict(c),
        "yellow": yellow,
        "blue": blue,
        "red": red,
        "note": (
            "Exact palette counts of puzzle.png, not a door proof. "
            "Blue is (63,72,204)=83700; an earlier HSV pass reported 96791. "
            "No SHA-256 of a 'find' is claimed here. {1,4,21} not used. "
            "See extra_door_find.py for the hashed grid packet."
        ),
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
