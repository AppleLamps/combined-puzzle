#!/usr/bin/env python3
"""matrixsumlist as an operation, then enter the resulting lists.

Frozen source: artifacts/salphaseion_letters.txt
  765 a–i letters before the first Salphaseion `z` (README blockquote).
  Prefix 91 = dbbi… ; from index 195 = faed… (570 letters).

Closed shapes (only divisors of those lengths; no 14, no 21):
  dbbi 91:  7×13, 13×7
  faed 570: 10×57, 15×38, 19×30, 30×19, 38×15
  all  765: 9×85, 15×51, 17×45

Closed maps:
  a1i9: a=1…i=9; sum%9==0 → i, else chr('a'+r-1)
  a0i8: a=0…i=8; sum%9 → chr('a'+r)

Outputs hashed. Unique strings are also written to
password_list_synthesis.json for leftover-3.2 *enter* (raw + sha256hex).
Also includes Jrk-named Neo passport date forms and the two Architect door
sentences (exact punctuation). Not FAED/Bifid, not {1,4,21}, not a third
unbounded password chat.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "artifacts" / "salphaseion_letters.txt"
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)

SHAPES = {
    "dbbi": [(7, 13), (13, 7)],
    "faed": [(10, 57), (15, 38), (19, 30), (30, 19), (38, 15)],
    "all": [(9, 85), (15, 51), (17, 45)],
}

PASSPORT = [
    "09112001",
    "09/11/2001",
    "20010911",
    "2001-09-11",
    "9/11/2001",
    "11092001",
    "September112001",
    "11 September 2001",
]

DOORS = [
    "The door to your right leads to the Source, and the salvation of Zion.",
    "The door to your left leads back to the Matrix, to her.",
    "the Source, and the salvation of Zion",
    "back to the Matrix, to her",
    "The door to your right leads to the Source and, through it, the salvation of Zion.",
    "The door to your left leads back to the Matrix, to her and to the end of your species.",
]


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def map_a1i9(n: int) -> str:
    r = n % 9
    return "i" if r == 0 else chr(ord("a") + r - 1)


def map_a0i8(n: int) -> str:
    return chr(ord("a") + (n % 9))


def val_a1i9(ch: str) -> int:
    return ord(ch) - ord("a") + 1


def val_a0i8(ch: str) -> int:
    return ord(ch) - ord("a")


def grid(s: str, rows: int, cols: int) -> list[list[str]]:
    assert len(s) == rows * cols
    return [list(s[i * cols : (i + 1) * cols]) for i in range(rows)]


def sums(g: list[list[str]], val) -> tuple[list[int], list[int], int]:
    rows = [sum(val(c) for c in row) for row in g]
    cols = [sum(val(g[r][c]) for r in range(len(g))) for c in range(len(g[0]))]
    return rows, cols, sum(rows)


def letters(nums: list[int], mapper) -> str:
    return "".join(mapper(n) for n in nums)


def main() -> int:
    raw = SRC.read_text(encoding="utf-8").strip()
    assert all(c in "abcdefghi" for c in raw), "source must be a-i only"
    dbbi, faed = raw[:91], raw[195:]
    assert dbbi.startswith("dbbi") and faed.startswith("faed")
    blocks = {"dbbi": dbbi, "faed": faed, "all": raw}

    derived = []
    recs = []
    for name, s in blocks.items():
        for rows, cols in SHAPES[name]:
            g = grid(s, rows, cols)
            for map_name, val, mapper in (
                ("a1i9", val_a1i9, map_a1i9),
                ("a0i8", val_a0i8, map_a0i8),
            ):
                rs, cs, tot = sums(g, val)
                row_s = letters(rs, mapper)
                col_s = letters(cs, mapper)
                tot_s = mapper(tot)
                rec = {
                    "block": name,
                    "shape": f"{rows}x{cols}",
                    "map": map_name,
                    "row_sums": rs,
                    "col_sums": cs,
                    "total": tot,
                    "row_letters": row_s,
                    "col_letters": col_s,
                    "total_letter": tot_s,
                    "row_sha256": sha256(row_s.encode()),
                    "col_sha256": sha256(col_s.encode()),
                    "looks_like_url": "gsmg.io/" in row_s or "gsmg.io/" in col_s,
                }
                recs.append(rec)
                derived.extend([row_s, col_s, tot_s, row_s + col_s, col_s + row_s])

    passwords = list(dict.fromkeys([p for p in derived if p] + PASSPORT + DOORS))
    spec = {
        "frozen_at": "2026-09-08T20:30:00Z",
        "rule": (
            "Leftover 3.2 only. matrixsumlist row/col letters (a-i, mod 9) plus "
            "Jrk-named Neo passport date forms plus Architect two-door sentences. "
            "No FAED Bifid, no {1,4,21}, no 7-interleave retry."
        ),
        "source_sha256": sha256(raw.encode()),
        "blobs": ["artifacts/phase32_leftover.b64"],
        "passwords": passwords,
    }
    spec_path = ROOT / "password_list_synthesis.json"
    spec_path.write_text(json.dumps(spec, indent=2) + "\n")

    report = {
        "source_sha256": sha256(raw.encode()),
        "n_letters": len(raw),
        "dbbi_len": 91,
        "faed_len": len(faed),
        "n_sum_records": len(recs),
        "n_unique_enter_passwords": len(passwords),
        "any_url": any(r["looks_like_url"] for r in recs),
        "records": recs,
        "password_list_sha256": sha256(spec_path.read_bytes()),
        "note": (
            "mod 9 on a 9-letter alphabet always lands in a-i; that is not by itself a find. "
            "A find would be readable English, a gsmg.io path, or a leftover-3.2 decrypt."
        ),
    }
    (OUT / "matrixsumlist.json").write_text(json.dumps(report, indent=2))
    print(
        json.dumps(
            {
                "source_sha256": report["source_sha256"],
                "n_sum_records": len(recs),
                "n_unique_enter_passwords": len(passwords),
                "any_url": report["any_url"],
                "password_list_sha256": report["password_list_sha256"],
                "sample_dbbi_7x13_a1i9_rows": next(
                    r["row_letters"]
                    for r in recs
                    if r["block"] == "dbbi" and r["shape"] == "7x13" and r["map"] == "a1i9"
                ),
                "sample_dbbi_7x13_a1i9_cols": next(
                    r["col_letters"]
                    for r in recs
                    if r["block"] == "dbbi" and r["shape"] == "7x13" and r["map"] == "a1i9"
                ),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
