#!/usr/bin/env python3
"""140 as a length or a skip — not as an AES password.

Closed takes only: first 140, last 140, skip-140-then-140, and the one
exact arithmetic cut (drop the 7-char 'gsmg.io' prefix = 56 spiral cells,
leaving 140). Scores URL / printable ASCII / in-channel SHA-256 / prize
pubkey. Does not feed the takes back into leftover 3.2.
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
OUT = ROOT / "out"
ART = ROOT / "artifacts"
OUT.mkdir(exist_ok=True)

MAIN_DOOR = "gsmg.io/theseedisplanted"
KNOWN_SHA = {
    "5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75",
    "89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32",
    "eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf",
    "4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081",
    "db14474e9c8f",  # prefix only, filled below from files if present
}
VIC = "15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112"
assert len(VIC) == 149

N, CELL = 14, 25
M = {(0, 0, 0): "K", (255, 255, 255): "W", (63, 72, 204): "B", (255, 242, 0): "Y", (254, 254, 254): "G"}


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def spiral_majority() -> list[str]:
    im = Image.open(ART / "original" / "follow_the_white_rabbit.png").convert("RGB")
    grid = []
    for r in range(N):
        row = []
        for c in range(N):
            pix = [im.getpixel((c * CELL + x, r * CELL + y)) for y in range(CELL) for x in range(CELL)]
            row.append(M[Counter(pix).most_common(1)[0][0]])
        grid.append(row)
    vis = [[False] * N for _ in range(N)]
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    r = c = d = 0
    out = []
    for _ in range(N * N):
        out.append(grid[r][c])
        vis[r][c] = True
        nr, nc = r + dirs[d][0], c + dirs[d][1]
        if not (0 <= nr < N and 0 <= nc < N and not vis[nr][nc]):
            d = (d + 1) % 4
            nr, nc = r + dirs[d][0], c + dirs[d][1]
        r, c = nr, nc
    return out


def bits_main(cells: list[str]) -> str:
    return "".join("1" if ch in "KB" else "0" for ch in cells)


def bits_extra(cells: list[str]) -> str:
    # B=1 Y=0, others None-as-0
    return "".join("1" if ch == "B" else "0" for ch in cells)


def ascii_from_bits(bits: str) -> tuple[str | None, str]:
    n = (len(bits) // 8) * 8
    raw = bytes(int(bits[i : i + 8], 2) for i in range(0, n, 8))
    extra = bits[n:]
    try:
        s = raw.decode("ascii")
        if all(32 <= ord(c) < 127 for c in s):
            return s, extra
    except UnicodeDecodeError:
        pass
    return None, extra


def twobit(cells: list[str]) -> str:
    # main as MSB, chroma as LSB: Y=01 B=11 K=10 W/G=00  (the 86+15*3+9*1=140 weights)
    m = {"W": "00", "G": "00", "Y": "01", "K": "10", "B": "11"}
    return "".join(m[ch] for ch in cells)


def prize_windows(b: bytes) -> list[str]:
    """Labels of every shared-gate hit in ``b`` (tools/prize_gate.py)."""
    hits, _ = prize_gate.gate_plaintext(b, windows=len(b) >= 32)
    return [f"{h['kind']}@{h['offset']}:{','.join(h['matches'])}" for h in hits]


def score(name: str, payload) -> dict:
    if isinstance(payload, str):
        raw = payload.encode("ascii", "replace")
        text = payload
    else:
        raw = payload
        text = payload.decode("ascii") if all(32 <= c < 127 for c in payload) else None
    rec = {
        "name": name,
        "n": len(payload),
        "sha256": sha256(raw),
        "printable": text if text is not None and all(32 <= ord(c) < 127 for c in text) else None,
        "url": None,
        "known_sha": sha256(raw) in KNOWN_SHA,
        "prize": prize_windows(raw),
        "ascii_from_bits": None,
    }
    if rec["printable"] and "gsmg.io/" in rec["printable"]:
        rec["url"] = rec["printable"]
    return rec


def windows_140(s: str, prefix: str) -> list[tuple[str, str]]:
    """first, last, and skip-140-then-140 (non-overlapping). Exact 140 only."""
    out = [(f"{prefix}[:140]", s[:140]), (f"{prefix}[-140:]", s[-140:])]
    i = 140
    n = 1
    while i + 140 <= len(s):
        out.append((f"{prefix}[{i}:{i+140}]", s[i : i + 140]))
        i += 140
        n += 1
        if n > 12:
            break
    return out


def main() -> int:
    letters = (ART / "salphaseion_letters.txt").read_text().strip()
    faed = letters[195:]
    dbbi = letters[:91]
    assert len(faed) == 570 and dbbi.startswith("dbbi")
    sp = spiral_majority()
    assert len(sp) == 196
    assert Counter(sp)["K"] == 86
    cd_pt = (OUT / "cosmic_xor7.bin").read_bytes()
    assert len(cd_pt) == 1327

    takes: list[tuple[str, object]] = []

    # --- the exact arithmetic cut ---
    # 'gsmg.io' is 7 chars = 56 cells. 196-56=140.
    drop56 = sp[56:]
    assert len(drop56) == 140
    takes.append(("spiral_drop_gsmg.io_56cells", "".join(drop56)))
    bm = bits_main(drop56)
    be = bits_extra(drop56)
    b2 = twobit(drop56)
    takes.append(("spiral_drop56_main_bits", bm))
    takes.append(("spiral_drop56_extra_bits", be))
    takes.append(("spiral_drop56_2bit", b2))
    ascii_m, extra_m = ascii_from_bits(bm)
    ascii_2, extra_2 = ascii_from_bits(b2)

    # first/last 140 of the full spiral
    takes.append(("spiral[:140]", "".join(sp[:140])))
    takes.append(("spiral[-140:]", "".join(sp[-140:])))
    takes.append(("spiral[:140]_main_bits", bits_main(sp[:140])))
    takes.append(("spiral[-140:]_main_bits", bits_main(sp[-140:])))
    takes.append(("spiral[:140]_2bit", twobit(sp[:140])))
    takes.append(("spiral[-140:]_2bit", twobit(sp[-140:])))

    # leftover 4 cells after the 192 URL bits — not length 140, but they are
    # what the 140-cut isolates at the end of drop56
    leftover4 = sp[192:]
    takes.append(("spiral[192:196]_leftover4", "".join(leftover4)))
    takes.append(("spiral[192:196]_main_bits", bits_main(leftover4)))

    for name, s in windows_140(letters, "letters"):
        takes.append((name, s))
    for name, s in windows_140(faed, "faed"):
        takes.append((name, s))
    for name, s in windows_140(VIC, "vic"):
        takes.append((name, s))
    for name, s in windows_140(cd_pt.hex(), "cdpt_hex"):
        takes.append((name, s))
    takes.append(("cdpt[:140]bytes", cd_pt[:140]))
    takes.append(("cdpt[-140:]bytes", cd_pt[-140:]))
    takes.append(("cdpt[140:280]bytes", cd_pt[140:280]))

    # Architect clause that names 140, first 140 chars of that clause
    clause = "HUNDRED FORTY OF THE INVESTMENT THATS WHAT US GUYS AT GSMG ARE TRYING TO ACCOMPLISH IN THE END"
    takes.append(("architect_140clause[:140]", (clause + " " * 140)[:140].strip() if False else clause[:140] if len(clause) >= 140 else clause))
    # the 140 chars of HASHTHETEXT-style concatenated stage token if long enough — skip if not

    results = {
        "rule": "140 as length/skip. No AES. Exact 140 or the leftover-4 the 140-cut isolates.",
        "vic_len": len(VIC),
        "vic_zeros": VIC.count("0"),
        "spiral_census": dict(Counter(sp)),
        "drop56_main_ascii": ascii_m,
        "drop56_main_extra_bits": extra_m,
        "drop56_2bit_ascii": ascii_2,
        "drop56_2bit_extra_bits": extra_2,
        "leftover4_cells": "".join(leftover4),
        "leftover4_main_bits": bits_main(leftover4),
        "takes": [],
        "urls": [],
        "prize_hits": [],
        "known_sha_hits": [],
        "printable": [],
    }

    seen = set()
    for name, payload in takes:
        rec = score(name, payload)
        key = (name, rec["sha256"])
        if key in seen:
            continue
        seen.add(key)
        results["takes"].append(rec)
        if rec["url"]:
            results["urls"].append(rec)
        if rec["prize"]:
            results["prize_hits"].append(rec)
        if rec["known_sha"]:
            results["known_sha_hits"].append(rec)
        if rec["printable"] and rec["n"] >= 8:
            results["printable"].append({"name": name, "text": rec["printable"][:160]})

    (OUT / "results_140_length.json").write_text(json.dumps(results, indent=2))
    print("takes", len(results["takes"]))
    print("drop56 main ASCII:", ascii_m, "extra bits", extra_m)
    print("drop56 2bit ASCII:", ascii_2, "extra bits", extra_2)
    print("leftover4", "".join(leftover4), bits_main(leftover4))
    print("urls", [u["name"] for u in results["urls"]])
    print("prize", len(results["prize_hits"]))
    print("known sha", len(results["known_sha_hits"]))
    print("printable:")
    for p in results["printable"]:
        print(" ", p["name"], repr(p["text"][:80]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
