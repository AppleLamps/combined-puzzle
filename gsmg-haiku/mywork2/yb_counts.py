"""Recount the yellow and blue poster cells straight from files/puzzle.png.

Checks the claims in mywork2/web/unverified_phase0_yellow_blue_counts.md:
9 yellow, 15 blue, every coloured cell on a spiral index = 7 mod 8, and
blue=1/yellow=0 equal to the low bit of each byte of the Phase 0 URL.
Run from the repo root: python mywork2/yb_counts.py
"""
from collections import Counter
from PIL import Image

PALETTE = {(0, 0, 0): "K", (255, 255, 255): "W", (63, 72, 204): "B",
           (255, 242, 0): "Y", (254, 254, 254): "F"}
CELL = 75  # 14 x 75 = 1050; the image is 1048 wide, so the last column is clipped

with Image.open("files/puzzle.png") as im:
    rgb = im.convert("RGB")
    grid = []
    for row in range(14):
        line = ""
        for col in range(14):
            box = (col * CELL, row * CELL, min((col + 1) * CELL, rgb.width), (row + 1) * CELL)
            cell = rgb.crop(box)
            count, color = max(cell.getcolors(cell.width * cell.height), key=lambda t: t[0])
            line += PALETTE[color]
        grid.append(line)

with open("scratchpad_grid.txt") as f:
    pinned = [l.strip() for l in f if l.strip()]
print("grid matches scratchpad_grid.txt:", grid == pinned)


def spiral(n):
    # top-left, down first, counter-clockwise inward (STEPS.md step 0)
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    seen, out, r, c, d = set(), [], 0, 0, 0
    for _ in range(n * n):
        out.append((r, c))
        seen.add((r, c))
        dr, dc = dirs[d]
        if not (0 <= r + dr < n and 0 <= c + dc < n) or (r + dr, c + dc) in seen:
            d = (d + 1) % 4
            dr, dc = dirs[d]
        r, c = r + dr, c + dc
    return out


coords = spiral(14)
seq = [grid[r][c] for r, c in coords]
bits = "".join("1" if s in "KB" else "0" for s in seq)
url = bytes(int(bits[i:i + 8], 2) for i in range(0, 192, 8)).decode("ascii")
print("spiral decode:", url, "| trailing bits:", bits[192:])

counts = Counter("".join(grid))
print("cell counts:", dict(sorted(counts.items())))
coloured = [(i, s) for i, s in enumerate(seq) if s in "BYF"]
for colour in "BYF":
    idx = [i for i, s in coloured if s == colour]
    print(f"{colour} spiral indices ({len(idx)}):", idx)
by = [(i, s) for i, s in coloured if s in "BY"]
print("all B/Y on index = 7 mod 8:", all(i % 8 == 7 for i, _ in by))
print("one B/Y per byte, bytes covered:", sorted(i // 8 for i, _ in by) == list(range(24)))
colour_bits = "".join("1" if s == "B" else "0" for _, s in by)
low_bits = "".join(str(ord(ch) & 1) for ch in url)
print("B=1/Y=0 along spiral:", colour_bits)
print("URL low bits:        ", low_bits)
print("identical:", colour_bits == low_bits)
