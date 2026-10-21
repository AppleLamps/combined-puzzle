#!/usr/bin/env python3
"""FEFEFE as a read instruction, not a password.

Grey sits at CCW spiral 164 = midpoint of 160 and 168 = byte group 21,
offset 4. Closed encodings only. Score URL / in-channel SHA-256 / prize
pubkey. No AES. No {1,4,21} as coordinates. No sliding windows.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import prize_gate  # noqa: E402  both targets, both serializations

ROOT = Path(__file__).resolve().parent
ART = ROOT / "artifacts"
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)

KNOWN_SHA = {
    "5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75",
    "89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32",
    "eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf",
    "4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081",
}
MAIN_DOOR = "gsmg.io/theseedisplanted"
N, CELL = 14, 25
PAL = {
    (0, 0, 0): "K",
    (255, 255, 255): "W",
    (63, 72, 204): "B",
    (255, 242, 0): "Y",
    (254, 254, 254): "G",
}
YEL, BLU, GRY = (255, 242, 0), (63, 72, 204), (254, 254, 254)


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def classify(p: tuple[int, int, int]) -> str:
    if p in PAL:
        return PAL[p]
    best, bd = "W", 10**18
    for col, name in PAL.items():
        d = sum((a - b) ** 2 for a, b in zip(p, col))
        if d < bd:
            best, bd = name, d
    return best


def majority_grid(im) -> list[list[str]]:
    g = []
    for r in range(N):
        row = []
        for c in range(N):
            pix = [im.getpixel((c * CELL + x, r * CELL + y)) for y in range(CELL) for x in range(CELL)]
            row.append(PAL[Counter(pix).most_common(1)[0][0]])
        g.append(row)
    return g


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


def bits_to_ascii(bits: str) -> tuple[str | None, str]:
    n = (len(bits) // 8) * 8
    extra = bits[n:]
    if n == 0:
        return None, extra
    try:
        raw = bytes(int(bits[i : i + 8], 2) for i in range(0, n, 8))
        s = raw.decode("ascii")
        if all(32 <= ord(c) < 127 for c in s):
            return s, extra
    except (UnicodeDecodeError, ValueError):
        pass
    return None, extra


def prize_of(b: bytes) -> list[str]:
    """Labels of every shared-gate hit in ``b`` (tools/prize_gate.py)."""
    hits, _ = prize_gate.gate_plaintext(b, windows=len(b) >= 32)
    return [f"{h['kind']}@{h['offset']}:{','.join(h['matches'])}" for h in hits]


def score(name: str, payload) -> dict:
    if isinstance(payload, str):
        raw = payload.encode("ascii", "replace")
        text = payload
    else:
        raw = payload
        text = raw.decode("ascii") if all(32 <= c < 127 for c in raw) else None
    rec = {
        "name": name,
        "n": len(payload),
        "sha256": sha256(raw),
        "printable": text if text is not None and all(32 <= ord(c) < 127 for c in text) else None,
        "url": None,
        "known_sha": sha256(raw) in KNOWN_SHA,
        "prize": prize_of(raw),
    }
    if rec["printable"] and ("gsmg.io/" in rec["printable"] or rec["printable"].startswith("http")):
        rec["url"] = rec["printable"] if "gsmg.io/" in rec["printable"] else rec["printable"][:80]
    return rec


def main_bits(cells: list[str]) -> str:
    return "".join("1" if ch in "KB" else "0" for ch in cells)


def gather(s: str, idxs_1based: list[int]) -> str:
    return "".join(s[i - 1] for i in idxs_1based if 1 <= i <= len(s))


def main() -> int:
    im = Image.open(ART / "original" / "follow_the_white_rabbit.png").convert("RGB")
    grid = majority_grid(im)
    sp = walk_ccw(grid)
    cells = [ch for *_, ch in sp]
    assert len(cells) == 196
    assert cells[163] == "G"
    letters = (ART / "salphaseion_letters.txt").read_text().strip()
    faed = letters[195:]
    dbbi = letters[:91]
    assert len(faed) == 570 and dbbi.startswith("dbbi")

    yel = [i + 1 for i, ch in enumerate(cells) if ch == "Y"]
    blu = [i + 1 for i, ch in enumerate(cells) if ch == "B"]
    events25 = sorted(yel + blu + [164])

    takes: list[tuple[str, object]] = []

    # --- 1. insert / flip at offset 4 of byte 21 ---
    mb = main_bits(cells)
    assert len(mb) == 196
    # insert grey's 0 as an extra bit at 0-based 163 (already there); insert a 1 instead
    takes.append(("insert_0_at_164", mb[:163] + "0" + mb[163:]))
    takes.append(("insert_1_at_164", mb[:163] + "1" + mb[163:]))
    flipped = mb[:163] + ("1" if mb[163] == "0" else "0") + mb[164:]
    takes.append(("flip_bit_164", flipped))
    url_flip = list(MAIN_DOOR)
    n = ord(url_flip[20]) ^ (1 << (7 - 3))  # offset 4 MSB-first = bit 3 from MSB
    url_flip[20] = chr(n)
    takes.append(("url_flip_char21_bit4", "".join(url_flip)))
    # drop bit 164, read 195 bits
    takes.append(("drop_bit_164", mb[:163] + mb[164:]))

    for name, bits in [
        ("insert_0_at_164", mb[:163] + "0" + mb[163:]),
        ("insert_1_at_164", mb[:163] + "1" + mb[163:]),
        ("flip_bit_164", flipped),
        ("drop_bit_164", mb[:163] + mb[164:]),
        ("main_196", mb),
    ]:
        ascii_, extra = bits_to_ascii(bits)
        if ascii_:
            takes.append((name + "_ascii", ascii_ + (f"+{extra}" if extra else "")))

    # --- 2. half-step: midpoint between consecutive spiral cell centres ---
    pix = im.load()
    half_cols = []
    for a, b in zip(sp, sp[1:]):
        _, r0, c0, _ = a
        _, r1, c1, _ = b
        y0, x0 = r0 * CELL + CELL // 2, c0 * CELL + CELL // 2
        y1, x1 = r1 * CELL + CELL // 2, c1 * CELL + CELL // 2
        mx, my = (x0 + x1) // 2, (y0 + y1) // 2
        half_cols.append(classify(pix[mx, my]))
    takes.append(("halfstep_195_colors", "".join(half_cols)))
    takes.append(("halfstep_195_main_bits", main_bits(half_cols)))
    a195, e195 = bits_to_ascii(main_bits(half_cols))
    if a195:
        takes.append(("halfstep_195_ascii", a195 + (f"+{e195}" if e195 else "")))
    # interleave cell, midpoint, cell, midpoint... (391)
    inter = []
    for i, ch in enumerate(cells):
        inter.append(ch)
        if i < len(half_cols):
            inter.append(half_cols[i])
    takes.append(("interleave_cell_half_391", "".join(inter)))
    takes.append(("interleave_391_main_bits", main_bits(inter)))
    a391, e391 = bits_to_ascii(main_bits(inter))
    if a391:
        takes.append(("interleave_391_ascii", a391 + (f"+{e391}" if e391 else "")))

    # --- 3. stride spiral by 4, four phases ---
    for phase in range(4):
        seq = cells[phase::4]
        takes.append((f"stride4_phase{phase}_colors", "".join(seq)))
        bits = main_bits(seq)
        takes.append((f"stride4_phase{phase}_bits", bits))
        a, e = bits_to_ascii(bits)
        if a:
            takes.append((f"stride4_phase{phase}_ascii", a + (f"+{e}" if e else "")))
    # stride 4 starting at 164 (1-based) forward and backward
    fwd = cells[163::4]
    bak = cells[163::-4]
    takes.append(("stride4_from164_fwd", "".join(fwd)))
    takes.append(("stride4_from164_back", "".join(bak)))
    for label, seq in (("fwd", fwd), ("back", bak)):
        bits = main_bits(seq)
        a, e = bits_to_ascii(bits)
        if a:
            takes.append((f"stride4_from164_{label}_ascii", a + (f"+{e}" if e else "")))

    # --- 4. read-heads into letter streams ---
    for src_name, src in (("letters", letters), ("faed", faed), ("dbbi", dbbi)):
        for idx in (164, 21, 4):
            if idx <= len(src):
                takes.append((f"{src_name}[{idx}:]_1based", src[idx - 1 :]))
                takes.append((f"{src_name}[:{idx}]_1based", src[:idx]))
            if idx < len(src):
                takes.append((f"{src_name}[{idx}:]_0based", src[idx:]))
        # 24-letter window at 164 (possible URL length)
        if 164 - 1 + 24 <= len(src):
            takes.append((f"{src_name}[164:188]_1based_24", src[163 : 163 + 24]))
        if 21 - 1 + 24 <= len(src):
            takes.append((f"{src_name}[21:45]_1based_24", src[20 : 20 + 24]))
        # stride 4 from 164
        if 164 <= len(src):
            takes.append((f"{src_name}_stride4_from164", src[163::4]))
            takes.append((f"{src_name}_stride4_from21", src[20::4]))
            takes.append((f"{src_name}_stride4_from4", src[3::4]))

    # dbbi 7x13 row/col named by 4 and by 21 mod shape
    g713 = [list(dbbi[i * 13 : (i + 1) * 13]) for i in range(7)]
    g137 = [list(dbbi[i * 7 : (i + 1) * 7]) for i in range(13)]
    takes.append(("dbbi_7x13_row4_1based", "".join(g713[3])))
    takes.append(("dbbi_7x13_col4_1based", "".join(g713[r][3] for r in range(7))))
    takes.append(("dbbi_13x7_row4_1based", "".join(g137[3])))
    takes.append(("dbbi_13x7_col4_1based", "".join(g137[r][3] for r in range(13))))
    # 21 1-based in 7x13: index 20 -> row 1, col 7
    takes.append(("dbbi_7x13_row21mod7", "".join(g713[20 % 7])))
    takes.append(("dbbi_7x13_col21mod13", "".join(g713[r][20 % 13] for r in range(7))))
    # faed 15x38 at index 164 -> row 4 col 11 (0-based 163)
    g1538 = [list(faed[i * 38 : (i + 1) * 38]) for i in range(15)]
    takes.append(("faed_15x38_row_of_164", "".join(g1538[163 // 38])))
    takes.append(("faed_15x38_col_of_164", "".join(g1538[r][163 % 38] for r in range(15))))
    takes.append(("faed_15x38_row21_1based", "".join(g1538[20]) if 20 < 15 else ""))
    takes.append(("faed_15x38_row4_1based", "".join(g1538[3])))
    takes.append(("faed_15x38_col4_1based", "".join(g1538[r][3] for r in range(15))))
    takes.append(("faed_15x38_col21_1based", "".join(g1538[r][20] for r in range(15))))

    # 25-event gather (positional, not password)
    takes.append(("letters_at_25events_1based", gather(letters, events25)))
    takes.append(("faed_at_25events_1based", gather(faed, events25)))
    takes.append(("letters_at_25events_0based", gather(letters, [i + 1 for i in events25 if i < len(letters)])))

    # skip-KW spiral starting at 164 (Y/B/G only from 164)
    ybg = [(i + 1, ch) for i, ch in enumerate(cells) if ch in "YBG"]
    from164 = [ch for i, ch in ybg if i >= 164]
    takes.append(("YBG_from164", "".join(from164)))

    results = {
        "rule": (
            "FEFEFE at spiral 164 = group 21 offset 4 as a read instruction. "
            "Half-step midpoints, bit insert/flip/drop at 164, stride-4, "
            "letter-stream heads at 164/21/4, dbbi/faed row/col named by those. "
            "No AES. No sliding windows. No {1,4,21} as coordinates."
        ),
        "grey_cell": "G",
        "spiral_164_1based": 164,
        "events25": events25,
        "halfstep_census": dict(Counter(half_cols)),
        "halfstep_n": len(half_cols),
        "takes": [],
        "urls": [],
        "new_urls": [],
        "prize_hits": [],
        "known_sha_hits": [],
        "printable_non_ai": [],
    }

    seen = set()
    for name, payload in takes:
        if payload == "" or payload is None:
            continue
        rec = score(name, payload)
        key = (name, rec["sha256"])
        if key in seen:
            continue
        seen.add(key)
        results["takes"].append(rec)
        if rec["url"]:
            results["urls"].append({"name": name, "url": rec["url"]})
            if rec["printable"] and MAIN_DOOR not in rec["printable"] and rec["printable"] != MAIN_DOOR:
                # still count if it's a different path
                if rec["printable"] != MAIN_DOOR and not rec["printable"].startswith(MAIN_DOOR + "+"):
                    results["new_urls"].append({"name": name, "text": rec["printable"][:120]})
            if rec["printable"] not in (MAIN_DOOR, MAIN_DOOR + "+0000") and "gsmg.io/" in rec["printable"]:
                if rec["printable"] != MAIN_DOOR:
                    pass
        if rec["prize"]:
            results["prize_hits"].append(rec)
        if rec["known_sha"]:
            results["known_sha_hits"].append(rec)
        p = rec["printable"]
        if p and len(p) >= 8 and not set(p) <= set("abcdefghiKWBYG01+"):
            results["printable_non_ai"].append({"name": name, "text": p[:160]})

    # tighter new-url check
    new = []
    for rec in results["takes"]:
        p = rec["printable"] or ""
        if "gsmg.io/" in p:
            path = p.split("+")[0]
            if path != MAIN_DOOR:
                new.append({"name": rec["name"], "text": p[:120]})
    results["new_urls"] = new

    (OUT / "results_fefefe_read.json").write_text(json.dumps(results, indent=2))
    print("takes", len(results["takes"]))
    print("halfstep census", results["halfstep_census"])
    print("urls (any gsmg.io):", results["urls"])
    print("NEW urls:", results["new_urls"])
    print("prize", len(results["prize_hits"]))
    print("known sha", len(results["known_sha_hits"]))
    print("printable non a-i/KWBYG:")
    for p in results["printable_non_ai"]:
        print(" ", p["name"], repr(p["text"][:100]))
    # show bit-ascii decodes even if url-like
    for rec in results["takes"]:
        if rec["name"].endswith("_ascii") or rec["name"].startswith("url_"):
            print(" DECODE", rec["name"], repr((rec["printable"] or "")[:80]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
