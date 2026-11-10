"""Bounded FAED-anchor operands over complete DBBI logical-cell parses.

The 84-cell parse has 61 ordinary cells; the 83-cell control has 60.  This
script never edits raw DBBI offsets.  It replaces/transforms only prime logical
cells and proves that every ordinary logical cell survives byte-for-byte.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
from collections import Counter
from pathlib import Path

from audit_dbbi_prime_grammar import parse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "runs/2026-09-15_faed_anchor_dbbi"
ANCHORS = (5, 479, 484)


def val(ch: str) -> int:
    assert ch in "abcdefghi"
    return ord(ch) - 96


def char(n: int) -> str:
    return chr(97 + ((n - 1) % 9))


def primes(n: int) -> list[int]:
    return [x for x in range(2, n + 1)
            if all(x % d for d in range(2, int(math.sqrt(x)) + 1))]


def colour(token: str) -> str:
    assert token in ("b", "be")
    return "B" if token == "b" else "Y"


def neighborhood(s: str, index: int, radius: int, reverse: bool) -> str:
    # Circular windows avoid an arbitrary boundary special case at anchor 5.
    offsets = range(-radius, radius + 1)
    text = "".join(s[(index + d) % len(s)] for d in offsets)
    return text[::-1] if reverse else text


def transform(base: int, operand: int, mode: str) -> int:
    if mode == "replace":
        return operand
    if mode == "add":
        return ((base - 1 + operand) % 9) + 1
    if mode == "subtract":
        return ((base - 1 - operand) % 9) + 1
    if mode == "reverse_subtract":
        return ((operand - 1 - base) % 9) + 1
    if mode == "xor":
        return ((base ^ operand) % 9) + 1
    raise ValueError(mode)


def token_base(token: str) -> int:
    # b=2; be=25, reduced to the page's a..i digit alphabet.
    return 2 if token == "b" else ((25 - 1) % 9) + 1


def english_score(s: str) -> int:
    grams = ("the", "and", "ing", "ion", "key", "btc", "seed", "private",
             "matrix", "sum", "list", "pass", "word", "zero", "prime")
    return sum(s.count(g) * len(g) for g in grams)


def bifid_decode(cipher: str, key_material: str) -> str:
    alphabet = "abcdefghiklmnopqrstuvwxyz"
    square = "".join(dict.fromkeys(key_material.replace("j", "i") + alphabet))
    assert len(square) == 25 and set(cipher) <= set(square)
    coordinates = [divmod(square.index(c), 5) for c in cipher]
    stream = list(itertools.chain.from_iterable(coordinates))
    return "".join(square[5 * stream[i] + stream[i + len(cipher)]]
                   for i in range(len(cipher)))


def sum_renderings(sums: dict) -> dict:
    out = {}
    for shape, axes in sums.items():
        out[shape] = {}
        for axis, nums in axes.items():
            out[shape][axis] = {
                "decimal": "".join(str(n) for n in nums),
                "mod26_A0": "".join(chr(97 + n % 26) for n in nums),
                "mod26_A1": "".join(chr(97 + (n - 1) % 26) for n in nums),
                "mod9": "".join(char(n) for n in nums),
            }
    return out


def build() -> tuple[dict, list[dict]]:
    dbbi = (DATA / "DBBI_91.txt").read_text().strip()
    faed = (DATA / "FAED_570.txt").read_text().strip()
    poster = (DATA / "poster_spiral_bits.txt").read_text().splitlines()[1]
    parses = {len(p): p for p in parse(dbbi, "e")}
    assert set(parses) == {83, 84}
    rows: list[dict] = []

    anchor_data = {}
    for base in (0, 1):
        anchor_data[str(base)] = {
            str(p): {"index": p - base, "char": faed[p - base], "value": val(faed[p - base])}
            for p in ANCHORS
        }

    for cell_count, cells in sorted(parses.items()):
        ordinary = [(slot, token) for slot, _, token, prime in cells if not prime]
        markers = [(slot, token) for slot, _, token, prime in cells if prime]
        assert len(markers) == 23
        assert len(ordinary) == cell_count - 23
        original_ordinary = [token for _, token in ordinary]

        # Two declared schedules: the DBBI token labels, and poster's first 23.
        schedules = {
            "dbbi_tokens": [colour(token) for _, token in markers],
            "poster_first23": list(poster[:23]),
        }
        for schedule_name, schedule in schedules.items():
            assert len(schedule) == len(markers)
            for indexing_base in (0, 1):
                idx = {p: p - indexing_base for p in ANCHORS}
                for radius in range(0, 13):
                    for reverse in (False, True):
                        windows = {p: neighborhood(faed, idx[p], radius, reverse) for p in ANCHORS}
                        for mode in ("replace", "add", "subtract", "reverse_subtract", "xor"):
                            values = []
                            marker_no = 0
                            applied = []
                            for slot, _, token, is_prime in cells:
                                if not is_prime:
                                    values.append(val(token))
                                    continue
                                c = schedule[marker_no]
                                # Natural mapping: yellow sum -> 479; blue sum -> 484.
                                anchor = 479 if c == "Y" else 484
                                # Difference-prime 5 receives the FAED[5] operand.
                                if slot == 5:
                                    anchor = 5
                                w = windows[anchor]
                                operand = val(w[marker_no % len(w)])
                                out = transform(token_base(token), operand, mode)
                                values.append(out)
                                applied.append({"slot": slot, "token": token, "colour": c,
                                                "anchor": anchor, "operand": operand, "output": out})
                                marker_no += 1

                            rendered = "".join(char(x) for x in values)
                            got_ordinary = [rendered[slot - 1] for slot, _ in ordinary]
                            assert got_ordinary == original_ordinary
                            assert len(values) == cell_count
                            # Natural complete rectangles only.
                            sums = {}
                            for h in range(1, cell_count + 1):
                                if cell_count % h:
                                    continue
                                w = cell_count // h
                                sums[f"{h}x{w}"] = {
                                    "rows": [sum(values[r*w:(r+1)*w]) for r in range(h)],
                                    "columns": [sum(values[r*w+c] for r in range(h)) for c in range(w)],
                                }
                            rendered_sums = sum_renderings(sums)
                            bifid = bifid_decode(faed, rendered)
                            rows.append({
                                "parse_cells": cell_count,
                                "ordinary_count": len(ordinary),
                                "schedule": schedule_name,
                                "indexing_base": indexing_base,
                                "radius": radius,
                                "reverse_window": reverse,
                                "mode": mode,
                                "windows": windows,
                                "applied": applied,
                                "rendered": rendered,
                                "sha256": hashlib.sha256(rendered.encode()).hexdigest(),
                                "english_score": english_score(rendered),
                                "sums": sums,
                                "sum_renderings": rendered_sums,
                                "bifid_faed": bifid,
                                "bifid_english_score": english_score(bifid),
                                "ordinary_roundtrip": True,
                            })

    manifest = {
        "model": "FAED[5/479/484] neighborhoods operate only on DBBI prime logical cells",
        "anchors": anchor_data,
        "mapping": {"Y": 479, "B": 484, "difference_prime_slot": {"slot": 5, "anchor": 5}},
        "indexing": ["zero-based", "one-based"],
        "neighborhood_radii": list(range(13)),
        "window_direction": ["forward", "reverse"],
        "prime_modes": ["replace", "add", "subtract", "reverse_subtract", "xor"],
        "schedules": ["DBBI token b/be labels", "poster first 23 colours"],
        "parse_accounting": {"84": {"prime": 23, "ordinary": 61},
                             "83_control": {"prime": 23, "ordinary": 60}},
        "ordinary_policy": "preserve exactly; no deletion, replacement, or arithmetic",
        "candidate_count": len(rows),
        "input_sha256": {
            "DBBI": hashlib.sha256(dbbi.encode()).hexdigest(),
            "FAED": hashlib.sha256(faed.encode()).hexdigest(),
            "poster_colours": hashlib.sha256(poster.encode()).hexdigest(),
        },
    }
    return manifest, rows


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest, rows = build()
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    with (OUT / "candidates.jsonl").open("w") as f:
        for row in rows:
            f.write(json.dumps(row, separators=(",", ":")) + "\n")
    unique = {r["rendered"] for r in rows}
    all_strings = set(unique)
    for r in rows:
        all_strings.add(r["bifid_faed"])
        for axes in r["sum_renderings"].values():
            for forms in axes.values():
                all_strings.update(forms.values())
    top = sorted(rows, key=lambda r: (-max(r["english_score"], r["bifid_english_score"]),
                                      r["rendered"]))[:20]
    counts = Counter((r["parse_cells"], r["ordinary_count"]) for r in rows)
    # Null calibration: preserve the same 84-cell ordinary payload, randomize only
    # its 23 prime cells, and send it through the identical Bifid continuation.
    dbbi = (DATA / "DBBI_91.txt").read_text().strip()
    faed = (DATA / "FAED_570.txt").read_text().strip()
    p84 = next(p for p in parse(dbbi, "e") if len(p) == 84)
    rng = random.Random(9152026)
    controls = []
    for _ in range(20000):
        material = "".join(token if not prime else char(rng.randrange(1, 10))
                           for _, _, token, prime in p84)
        controls.append(english_score(bifid_decode(faed, material)))
    real_max = max(r["bifid_english_score"] for r in rows)
    summary = {
        "candidates": len(rows),
        "unique_rendered": len(unique),
        "accounting": {f"{a}_cells_{b}_ordinary": n for (a, b), n in counts.items()},
        "ordinary_roundtrip_failures": sum(not r["ordinary_roundtrip"] for r in rows),
        "max_rendered_english_score": max(r["english_score"] for r in rows),
        "max_bifid_english_score": max(r["bifid_english_score"] for r in rows),
        "bifid_control": {"samples": len(controls), "seed": 9152026,
                          "maximum": max(controls),
                          "p95": sorted(controls)[int(.95 * len(controls))],
                          "at_or_above_real_max": sum(x >= real_max for x in controls),
                          "real_above_control_max": sum(r["bifid_english_score"] > max(controls)
                                                        for r in rows)},
        "exact_known_strings": [s for s in all_strings if s in {
            "matrixsumlist", "lastwordsbeforearchichoice", "thispassword",
            "privatekey", "btcseed"}],
        "top": [{k: r[k] for k in ("parse_cells", "schedule", "indexing_base", "radius",
                                           "reverse_window", "mode", "rendered", "english_score",
                                           "bifid_english_score")}
                for r in top],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k != "top"}, indent=2))


if __name__ == "__main__":
    main()
