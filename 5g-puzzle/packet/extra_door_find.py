#!/usr/bin/env python3
"""Piece-1 extra-door packet (hashed find, not AES).

Contemporaneous instructions (quoted 2020-04-08 #3388, unedited #4590 / #7914):
  Yellow has a number and so does Blue.
  Go back to the first puzzle piece.
  It might have shown you only one door; the rabbit nest may contain more.
  Hush hush.
  Do not use {1,4,21}.

Closed operations (written down before hashing):
  1. Reproduce the published main door (CCW spiral, K/B=1, Y/W/G=0).
  2. Exact palette pixel counts (not HSV).
  3. Cell counts and 1-based (row,col) of Y/B/G.
  4. CCW 1-based spiral indices of Y/B/G.
  5. Extra channel: Y vs B on the 24 spiral positions that are multiples of 8
     (the LSB of each main-door ASCII byte). Hash the 3-byte payloads.
  6. Alternate 1-bit / 2-bit spirals from a frozen list — record ASCII + sha256.
  7. PNG chunks + raster LSB prefix (stego scan, not a new cipher).
  8. Rabbit = impure black/white cells; bbox only.

Success: a second gsmg.io-style path, or any candidate whose sha256 is claimed
as the find. This script does not retry leftover 3.2 / Cosmic Duality AES.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
IMG = ROOT / "artifacts" / "puzzle.png"
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)

YEL = (255, 242, 0)
BLU = (63, 72, 204)
BLK = (0, 0, 0)
WHT = (255, 255, 255)
GRY = (254, 254, 254)
RED = (237, 28, 36)
N, CELL, GRID_H, IMG_W = 14, 75, 1047, 1048
MAIN_DOOR = "gsmg.io/theseedisplanted"
HASHTHETEXT = "GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def center(r: int, c: int) -> tuple[int, int]:
    cy = r * CELL + CELL // 2 if r < N - 1 else 975 + (GRID_H - 975) // 2
    cx = c * CELL + CELL // 2 if c < N - 1 else 975 + (IMG_W - 975) // 2
    return cx, cy


def classify(p: tuple[int, int, int]) -> str:
    if p == YEL:
        return "Y"
    if p == BLU:
        return "B"
    if p == GRY:
        return "G"
    if p == BLK:
        return "K"
    if p == WHT:
        return "W"
    cols = {"Y": YEL, "B": BLU, "K": BLK, "W": WHT, "G": GRY}
    best, bd = "W", 10**18
    for n, c in cols.items():
        d = sum((a - b) ** 2 for a, b in zip(p, c))
        if d < bd:
            best, bd = n, d
    return best


def walk_ccw(grid: list[list[str]]) -> list[tuple[int, int, int, str]]:
    vis = [[False] * N for _ in range(N)]
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    r = c = di = 0
    out = []
    for i in range(N * N):
        out.append((i, r, c, grid[r][c]))
        vis[r][c] = True
        nr, nc = r + dirs[di][0], c + dirs[di][1]
        if not (0 <= nr < N and 0 <= nc < N and not vis[nr][nc]):
            di = (di + 1) % 4
            nr, nc = r + dirs[di][0], c + dirs[di][1]
        r, c = nr, nc
    return out


def bits_to_ascii(bits: list[int]) -> str:
    s = "".join(str(int(b)) for b in bits)
    chars = []
    for i in range(0, len(s) - len(s) % 8, 8):
        chars.append(chr(int(s[i : i + 8], 2)))
    return "".join(chars)


def rec_ascii(name: str, bits: list[int]) -> dict:
    text = bits_to_ascii(bits)
    n_print = sum(32 <= ord(ch) < 127 for ch in text)
    raw = text.encode("latin-1")
    return {
        "name": name,
        "n_bits": len(bits),
        "ascii_latin1": text,
        "printable": n_print,
        "len": len(text),
        "looks_like_url": "gsmg.io/" in text or text.startswith("http"),
        "sha256": sha256(raw),
    }


def png_chunks(data: bytes) -> list[dict]:
    pos, chunks = 8, []
    while pos + 8 <= len(data):
        ln = int.from_bytes(data[pos : pos + 4], "big")
        typ = data[pos + 4 : pos + 8].decode("ascii", "replace")
        payload = data[pos + 8 : pos + 8 + ln]
        rec = {"type": typ, "len": ln}
        if typ in {"tEXt", "zTXt", "iTXt", "tIME", "eXIf"}:
            rec["payload_sha256"] = sha256(payload)
        chunks.append(rec)
        pos += 12 + ln
        if typ == "IEND":
            break
    return chunks


def main() -> int:
    png = IMG.read_bytes()
    im = Image.open(IMG).convert("RGB")
    grid = [[classify(im.getpixel(center(r, c))) for c in range(N)] for r in range(N)]
    spiral = walk_ccw(grid)
    colors = "".join(ch for *_, ch in spiral)

    main_bits = [1 if ch in "KB" else 0 for *_, ch in spiral]
    main_ascii = bits_to_ascii(main_bits)

    y_cells = [(r + 1, c + 1) for r in range(N) for c in range(N) if grid[r][c] == "Y"]
    b_cells = [(r + 1, c + 1) for r in range(N) for c in range(N) if grid[r][c] == "B"]
    g_cells = [(r + 1, c + 1) for r in range(N) for c in range(N) if grid[r][c] == "G"]
    y_spiral = [i + 1 for i, _, _, ch in spiral if ch == "Y"]
    b_spiral = [i + 1 for i, _, _, ch in spiral if ch == "B"]
    g_spiral = [i + 1 for i, _, _, ch in spiral if ch == "G"]

    byte_lsbs = list(range(8, N * N + 1, 8))
    by_index = {i + 1: ch for i, _, _, ch in spiral}
    lsb_colors = [by_index[p] for p in byte_lsbs]
    extra_b1 = [1 if ch == "B" else 0 for ch in lsb_colors]
    extra_y1 = [1 if ch == "Y" else 0 for ch in lsb_colors]
    extra_bytes_b1 = bytes(
        int("".join(str(b) for b in extra_b1[i : i + 8]), 2) for i in range(0, 24, 8)
    )
    extra_bytes_y1 = bytes(
        int("".join(str(b) for b in extra_y1[i : i + 8]), 2) for i in range(0, 24, 8)
    )

    counts = Counter(im.getdata())
    cell_counts = Counter(ch for row in grid for ch in row)

    rabbit_cells = []
    for r in range(N):
        for c in range(N):
            x0, y0 = c * CELL, r * CELL
            x1, y1 = min(x0 + CELL, IMG_W), min(y0 + CELL, GRID_H)
            cnt = Counter(im.getpixel((x, y)) for y in range(y0, y1) for x in range(x0, x1))
            tot = (x1 - x0) * (y1 - y0)
            _col, n = cnt.most_common(1)[0]
            if n / tot < 0.95 and c != N - 1:
                rabbit_cells.append({"row": r + 1, "col": c + 1, "purity": round(n / tot, 4)})

    alternates = [
        rec_ascii("main_KB=1", main_bits),
        rec_ascii("invert", [1 - b for b in main_bits]),
        rec_ascii("yellow=1", [1 if ch == "Y" else 0 for *_, ch in spiral]),
        rec_ascii("blue=1", [1 if ch == "B" else 0 for *_, ch in spiral]),
        rec_ascii("YB=1", [1 if ch in "YB" else 0 for *_, ch in spiral]),
        rec_ascii("Y=0_B=1_skip_KW", [1 if ch == "B" else 0 for *_, ch in spiral if ch in "YB"]),
        rec_ascii("Y=1_B=0_skip_KW", [1 if ch == "Y" else 0 for *_, ch in spiral if ch in "YB"]),
        rec_ascii("grey=1", [1 if ch == "G" else 0 for *_, ch in spiral]),
        rec_ascii("extra_B=1_Y=0_on_byte_LSBs", extra_b1),
        rec_ascii("extra_Y=1_B=0_on_byte_LSBs", extra_y1),
    ]
    two_bit_maps = [
        {"W": "00", "K": "01", "Y": "10", "B": "11", "G": "00"},
        {"W": "00", "K": "01", "Y": "10", "B": "11", "G": "01"},
        {"W": "00", "K": "11", "Y": "01", "B": "10", "G": "00"},
    ]
    for i, enc in enumerate(two_bit_maps):
        bits = []
        for *_, ch in spiral:
            bits.extend(int(x) for x in enc[ch])
        alternates.append(rec_ascii(f"2bit_{i}", bits))

    lsb_prefix = {}
    pixels = list(im.getdata())
    for name, idx in (("R", 0), ("G", 1), ("B", 2)):
        bits = [(p[idx] & 1) for p in pixels[: 32 * 8]]
        lsb_prefix[name] = rec_ascii(f"raster_lsb_{name}_first32", bits)

    second_urls = [
        a["name"] for a in alternates if a["looks_like_url"] and a["ascii_latin1"] != MAIN_DOOR
    ]

    report = {
        "hint": (
            "Jrk #1710 as quoted 2020-04-08 #3388. Unedited #4590 extra door unfound; "
            "unedited #7914 another DOOR. {1,4,21} not used. Not an AES packet."
        ),
        "png_sha256": sha256(png),
        "png_size": list(im.size),
        "png_chunks": png_chunks(png),
        "palette_pixel_counts": {
            "yellow_255_242_0": counts[YEL],
            "blue_63_72_204": counts[BLU],
            "black": counts[BLK],
            "white": counts[WHT],
            "grey_254_254_254": counts[GRY],
            "red_237_28_36": counts[RED],
        },
        "hsv_heuristic_blue_was": 96791,
        "hsv_note": (
            "extra_door_pixels.py counted extra bluish pixels. Exact palette blue is 83700. "
            "Leftover-3.2 list that used 96791 stays frozen; not retried."
        ),
        "grid": ["".join(row) for row in grid],
        "cell_counts": dict(cell_counts),
        "yellow_cells_1indexed": y_cells,
        "blue_cells_1indexed": b_cells,
        "grey_cells_1indexed": g_cells,
        "yellow_ccw_spiral_1indexed": y_spiral,
        "blue_ccw_spiral_1indexed": b_spiral,
        "grey_ccw_spiral_1indexed": g_spiral,
        "all_YB_on_multiples_of_8": all(p % 8 == 0 for p in y_spiral + b_spiral),
        "main_door": MAIN_DOOR,
        "main_door_reproduced": main_ascii == MAIN_DOOR,
        "main_door_sha256": sha256(MAIN_DOOR.encode()),
        "spiral_color_string": colors,
        "spiral_color_string_sha256": sha256(colors.encode()),
        "byte_lsb_spiral_positions": byte_lsbs,
        "byte_lsb_colors": "".join(lsb_colors),
        "extra_channel": {
            "rule": "24 CCW spiral positions that are multiples of 8; B=1 Y=0 or Y=1 B=0",
            "B1_hex": extra_bytes_b1.hex(),
            "Y1_hex": extra_bytes_y1.hex(),
            "B1_sha256": sha256(extra_bytes_b1),
            "Y1_sha256": sha256(extra_bytes_y1),
            "B1_hex_string_sha256": sha256(extra_bytes_b1.hex().encode()),
            "Y1_hex_string_sha256": sha256(extra_bytes_y1.hex().encode()),
        },
        "HASHTHETEXT_footer_sha256": sha256(HASHTHETEXT.encode()),
        "HASHTHETEXT_note": (
            "Known Salph-entry hash of the piece-1 title+address. "
            "Not the extra door: Jrk still named another door after Salph was a reached stage."
        ),
        "alternates": alternates,
        "second_gsmg_paths": second_urls,
        "raster_lsb_prefix": lsb_prefix,
        "rabbit_impure_cells_1indexed": rabbit_cells,
        "find_claimed": False,
        "verdict": (
            "Main door reproduced. No second gsmg.io path from the frozen encodings. "
            "Yellow/blue occupy exactly the 24 byte-LSB spiral slots (9 Y + 15 B). "
            "That extra channel hashes to sha256(bytes.fromhex('f73d92')) / "
            "sha256(bytes.fromhex('08c26d')). That is a hashed observation, not a hashed "
            "door opening. Grey cell (8,5) is leftover. {1,4,21} unused."
        ),
    }
    (OUT / "extra_door_find.json").write_text(json.dumps(report, indent=2))
    print(
        json.dumps(
            {
                "png_sha256": report["png_sha256"],
                "main_door_reproduced": report["main_door_reproduced"],
                "palette": report["palette_pixel_counts"],
                "cell_counts": report["cell_counts"],
                "all_YB_on_multiples_of_8": report["all_YB_on_multiples_of_8"],
                "extra_B1_hex": report["extra_channel"]["B1_hex"],
                "extra_Y1_hex": report["extra_channel"]["Y1_hex"],
                "extra_B1_sha256": report["extra_channel"]["B1_sha256"],
                "second_gsmg_paths": second_urls,
                "find_claimed": False,
                "n_alternates": len(alternates),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
