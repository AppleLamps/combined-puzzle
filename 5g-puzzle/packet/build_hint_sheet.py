#!/usr/bin/env python3
"""Build unedited-hint sheet from parsed Jrk messages + source .txt edit lines."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/workspace")
def load_jrk_from_txt() -> dict[int, dict]:
    rx_h = re.compile(r"^\[#(\d+)\] (\d{2}:\d{2}:\d{2}) Jrk Bgrt")
    rx_day = re.compile(r"^## DAY (\d{4}-\d{2}-\d{2})")
    out = {}
    current = None
    day = None
    buf = []
    collecting = False
    for path in sorted(ROOT.glob("20*.txt")):
        in_t = False
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.strip() == "TRANSCRIPT":
                in_t = True
                continue
            if not in_t:
                continue
            dm = rx_day.match(line)
            if dm:
                if collecting and current:
                    out[current] = {"id": current, "ts": f"{day}T{out.get(current,{}).get('time','')}", "text": "\n".join(buf).strip()}
                day = dm.group(1)
                collecting = False
                current = None
                buf = []
                continue
            m = rx_h.match(line)
            if m:
                if collecting and current:
                    out[current]["text"] = "\n".join(buf).strip()
                current = int(m.group(1))
                out[current] = {"id": current, "ts": f"{day}T{m.group(2)}", "time": m.group(2), "text": ""}
                collecting = True
                buf = []
                continue
            if collecting and current:
                if line.startswith("[#"):
                    out[current]["text"] = "\n".join(buf).strip()
                    collecting = False
                    current = None
                    buf = []
                    # fall through: this line might be another header handled next loop
                    m2 = rx_h.match(line)
                    if m2:
                        current = int(m2.group(1))
                        out[current] = {"id": current, "ts": f"{day}T{m2.group(2)}", "time": m2.group(2), "text": ""}
                        collecting = True
                        buf = []
                    continue
                if line.startswith("(") or line.startswith("*"):
                    continue
                if line.strip() == "":
                    continue
                buf.append(line)
        if collecting and current:
            out[current]["text"] = "\n".join(buf).strip()
            collecting = False
    return out

KEEP_IDS = [
    225, 226, 257, 851, 866, 867, 881, 898,
    1710, 2017, 2023, 2026, 3338, 4590, 4688, 4694,
    5717, 5966, 6491, 6497, 6884, 7529, 7914, 8000,
    8330, 8352, 8354, 8491, 8774, 8795, 8796, 9599, 9607, 9621,
    16624, 39224, 39237, 60314, 63957,
]


def edits_from_txt() -> dict[int, str]:
    rx_h = re.compile(r"^\[#(\d+)\]")
    rx_e = re.compile(r"^\(edited (.+)\)$")
    found = {}
    current = None
    for path in sorted(ROOT.glob("20*.txt")):
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            m = rx_h.match(line)
            if m:
                current = int(m.group(1))
                continue
            if current is None:
                continue
            em = rx_e.match(line.strip())
            if em:
                found[current] = em.group(1)
    return found


def main():
    edits = edits_from_txt()
    by_id = load_jrk_from_txt()
    lines = [
        "# Unedited-hint sheet",
        "",
        "Only Jrk messages used as direction for the Cosmic Duality packet.",
        "`unsafe` = edited in this 2026 export with no independent same-day quote check in this row.",
        "",
        "| Id | Date | Edited? | Text (truncated) | Use |",
        "|----|------|---------|------------------|-----|",
    ]
    notes = {
        1710: "quoted identically 2020-04-08 #3388 — poem original",
        2026: "quoted same day 2020 — original",
        4590: "no edit line — original",
        6884: "April 1; Jrk #7529 implies joke; edited 2025-02-02 — do not use coordinates",
        7529: "edited 2026-07-22; still answers April Fools question",
        7914: "no edit line — original",
        8000: "edited 2026-02-15; only opening confirmed same-day — primes/zeroing unsafe",
        8352: "no edit line — original",
        8774: "quoted 2023-08-05 — phrase original",
        8796: "quoted 2023-08-10 — phrase original",
        9599: "same-day 2023 thread — phrase original",
        39224: "edited +14s — treat as contemporaneous",
        16624: "edited same morning 2023-11-24 — likely typo",
    }
    for i in KEEP_IDS:
        m = by_id.get(i)
        text = (m["text"] if m else "").replace("\n", " / ")[:180]
        ts = (m["ts"][:10] if m else "?")
        ed = edits.get(i, "")
        use = notes.get(i, "ok" if not ed else "unsafe canon unless quoted")
        flag = ed or "no"
        lines.append(f"| `{i}` | {ts} | {flag} | {text} | {use} |")
    Path("/workspace/packet/HINT_SHEET.md").write_text("\n".join(lines) + "\n")
    print("wrote packet/HINT_SHEET.md", "edits", len(edits))


if __name__ == "__main__":
    main()
