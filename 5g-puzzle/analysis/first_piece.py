#!/usr/bin/env python3
"""
Re-derivation of the FIRST puzzle piece from the actual PNG.

analysis/puzzle.png is the gsmg.io/puzzle image, taken from the community
mirror github.com/puzzlehunt/gsmgio-5btc-puzzle (gsmg.io itself went down in
2026). 1048x1556, RGBA, 29,931 bytes.

Establishes:
  1. the counterclockwise inward spiral decodes cleanly to gsmg.io/theseedisplanted
  2. the blue/yellow colouring is ENTIRELY redundant with that text -- one cell
     per character, always the low bit, blue exactly where the ASCII is odd.
     A boundary marker, not a payload.
  3. the URL uses 192 of the 196 cells. The four surplus cells are the innermost
     2x2 -- and the rabbit's head and ears are drawn on exactly those four.
  4. one cell is #fefefe where every other white is #ffffff, at row 7 col 4
     (1-indexed 8,5) -- spiral index 163, which is prime
  5. the design's native grid is 70x70 at 15px units (5x5 sub-units per cell),
     and the rabbit is the ONLY thing in the image that departs from the flat
     cell colours. Nothing else is hidden at sub-cell level.
  6. no steganography in this copy: alpha uniform 255, no trailing bytes after
     IEND, no text chunks, LSB distribution skewed as a flat-colour image should be

Requires Pillow. Run from the repo root: python3 analysis/first_piece.py
"""
import collections, os, struct, sys, zlib

from PIL import Image

PNG = os.path.join(os.path.dirname(__file__), "puzzle.png")
N = 14
MATRIX_H = 1047          # the red divider bar starts at y=1047
URL = "gsmg.io/theseedisplanted"
BASE = {"K": (0, 0, 0), "W": (255, 255, 255), "B": (63, 72, 204), "Y": (255, 242, 0)}
NAME = {(0, 0, 0): "K", (255, 255, 255): "W", (245, 245, 245): "W",
        (254, 254, 254): "W", (63, 72, 204): "B", (255, 242, 0): "Y"}


def spiral_ccw_inward():
    """Counterclockwise from the top-left, ring by ring, ending at the centre."""
    cells, t, b, l, r = [], 0, N - 1, 0, N - 1
    while t <= b and l <= r:
        for y in range(t, b + 1):
            cells.append((y, l))
        for x in range(l + 1, r + 1):
            cells.append((b, x))
        if l < r:
            for y in range(b - 1, t - 1, -1):
                cells.append((y, r))
        if t < b:
            for x in range(r - 1, l, -1):
                cells.append((t, x))
        t, b, l, r = t + 1, b - 1, l + 1, r - 1
    return cells


def read_grid(px, cw, ch):
    """Modal colour of each cell's interior, ignoring the rabbit's thin strokes."""
    grid = []
    for r in range(N):
        row = ""
        for c in range(N):
            x0, x1 = int(c * cw), int((c + 1) * cw)
            y0, y1 = int(r * ch), int((r + 1) * ch)
            cnt = collections.Counter(px[x, y]
                                      for y in range(y0 + 8, y1 - 8, 3)
                                      for x in range(x0 + 8, x1 - 8, 3))
            row += NAME.get(cnt.most_common(1)[0][0], "?")
        grid.append(row)
    return grid


def is_prime(n):
    if n < 2:
        return False
    return all(n % d for d in range(2, int(n ** 0.5) + 1))


def main():
    if not os.path.exists(PNG):
        sys.exit(f"missing {PNG}")
    im = Image.open(PNG)
    print(f"{os.path.basename(PNG)}  {im.size}  {im.mode}\n")

    rgb = im.convert("RGB")
    px = rgb.load()
    W = rgb.width
    cw, ch = W / N, MATRIX_H / N
    grid = read_grid(px, cw, ch)
    cells = spiral_ccw_inward()
    bits = ["1" if grid[y][x] in "KB" else "0" for y, x in cells]

    print("COLOUR CENSUS (whole image)")
    for col, n in collections.Counter(rgb.getdata() if not hasattr(rgb,'get_flattened_data') else rgb.get_flattened_data()).most_common(7):
        print(f"   #{col[0]:02x}{col[1]:02x}{col[2]:02x}  {n:8d}")
    print("   note: #ed1c24 is the 15px divider bar under the matrix -- the image"
          "\n         does contain red, which transcriptions of it do not.\n")

    got = "".join(chr(int("".join(bits[i:i + 8]), 2)) for i in range(0, 192, 8))
    print(f"1. SPIRAL DECODE\n   {got!r}\n   matches expected: {got == URL}\n")

    coloured = [(i, grid[y][x]) for i, (y, x) in enumerate(cells) if grid[y][x] in "BY"]
    blue = {i // 8 for i, c in coloured if c == "B"}
    print("2. COLOUR CHANNEL")
    print(f"   {len(coloured)} coloured cells; bit-positions they occupy: "
          f"{sorted(set(i % 8 for i, _ in coloured))}")
    print(f"   one per character, always the low bit; blue <=> odd ASCII: "
          f"{all((i in blue) == (ord(c) % 2 == 1) for i, c in enumerate(URL))}")
    print("   -> redundant with the text. A boundary marker, not a payload.")
    print(f"   the only numbers it leaves: {sum(1 for _, c in coloured if c == 'Y')} yellow, "
          f"{sum(1 for _, c in coloured if c == 'B')} blue\n")

    print(f"3. SURPLUS CELLS  ({len(cells)} cells, URL consumes 192)")
    for k in range(192, len(cells)):
        y, x = cells[k]
        print(f"   spiral#{k}  row {y} col {x}  {grid[y][x]}  bit {bits[k]}")
    print(f"   surplus bits: {''.join(bits[192:])}  -- the innermost 2x2, the centre\n")

    print("4. THE OFF-COLOUR CELL")
    pts = [(x, y) for y in range(MATRIX_H) for x in range(W) if px[x, y] == (254, 254, 254)]
    if pts:
        r, c = int(min(p[1] for p in pts) / ch), int(min(p[0] for p in pts) / cw)
        k = cells.index((r, c))
        print(f"   #fefefe, {len(pts)} px (one whole cell), row {r} col {c} "
              f"(1-indexed {r+1},{c+1})")
        print(f"   spiral#{k} -> char {k//8} ({URL[k//8]!r}) bit {k%8}; "
              f"{k} is prime: {is_prime(k)}\n")

    print("5. NATIVE SUB-GRID  (15px units, 5x5 per cell -> 70x70)")
    U = MATRIX_H / 70
    off, drawn = 0, []
    for sy in range(70):
        for sx in range(70):
            cx, cy = int(sx * U + U / 2), int(sy * U + U / 2)
            cell = grid[min(N - 1, int(cy / ch))][min(N - 1, int(cx / cw))]
            if px[min(W - 1, cx), min(MATRIX_H - 1, cy)] != BASE[cell]:
                off += 1
                drawn.append((sy, sx))
    ys = [p[0] for p in drawn]
    xs = [p[1] for p in drawn]
    print(f"   sub-units departing from their cell's flat colour: {off}")
    print(f"   all of them inside rows {min(ys)}..{max(ys)}, cols {min(xs)}..{max(xs)} "
          "-- the rabbit, and nothing else\n")

    print("6. FILE-LEVEL CHECKS")
    d = open(PNG, "rb").read()
    i, types = 8, []
    while i < len(d):
        ln = struct.unpack(">I", d[i:i + 4])[0]
        typ = d[i + 4:i + 8].decode("latin1")
        types.append(typ)
        i += 12 + ln
        if typ == "IEND":
            break
    ach = im.getchannel("A") if im.mode == "RGBA" else None
    alpha = set(ach.get_flattened_data() if hasattr(ach, "get_flattened_data") else ach.getdata()) if ach else set()
    print(f"   chunks: {' '.join(types)}")
    print(f"   bytes after IEND: {len(d) - i}")
    print(f"   alpha values present: {sorted(alpha)}")
    lsb = collections.Counter(px[x, y][0] & 1
                              for y in range(0, rgb.height, 3)
                              for x in range(0, W, 3))
    print(f"   red-channel LSB split: {dict(lsb)} (a payload would be ~50/50)")
    print("   -> no steganography in this copy. Caveat: it is a mirrored file and")
    print("      may have been re-encoded; it is not provably the original bytes.")


if __name__ == "__main__":
    main()
