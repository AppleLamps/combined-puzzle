#!/usr/bin/env python3
"""Parse GSMG Telegram yearly transcripts into structured JSONL."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path("/workspace")
OUT = Path("/tmp/gsmg/messages.jsonl")

HEADER_RE = re.compile(
    r"^\[#(\d+)\] (\d{2}:\d{2}:\d{2})(?: \* SERVICE: (.+)| (.+?) \(user(\d+|---)\))?\s*$"
)
DAY_RE = re.compile(r"^## DAY (\d{4}-\d{2}-\d{2})")
REPLY_RE = re.compile(r"^\(reply to #(\d+)")
POLL_RE = re.compile(r"^\(poll:")
FORWARD_RE = re.compile(r"^\(forwarded from")
EDITED_RE = re.compile(r"^\(edited ")
ATTACH_RE = re.compile(r"^\(attachment:")
REACT_RE = re.compile(r"^\(reactions:")
ANNO_RE = re.compile(r"^\(")


def parse_file(path: Path):
    year = path.stem
    day = None
    in_transcript = False
    current = None
    text_lines: list[str] = []
    annotations: list[str] = []

    def flush():
        nonlocal current, text_lines, annotations
        if current is None:
            return
        current["text"] = "\n".join(text_lines).strip()
        current["annotations"] = annotations
        yield current
        current = None
        text_lines = []
        annotations = []

    with path.open(encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if not in_transcript:
                if line.strip() == "TRANSCRIPT":
                    in_transcript = True
                continue
            mday = DAY_RE.match(line)
            if mday:
                for msg in flush():
                    yield msg
                day = mday.group(1)
                continue
            m = HEADER_RE.match(line)
            if m:
                for msg in flush():
                    yield msg
                msg_id, time, service, name, uid = m.groups()
                current = {
                    "id": int(msg_id),
                    "year": year,
                    "date": day,
                    "time": time,
                    "ts": f"{day}T{time}" if day else None,
                    "service": bool(service),
                    "service_text": service or "",
                    "author": name or "",
                    "uid": uid or "",
                    "reply_to": None,
                }
                continue
            if current is None:
                continue
            if not line.strip():
                # blank line can separate blocks; keep collecting until next header
                if text_lines and text_lines[-1] != "":
                    text_lines.append("")
                continue
            if ANNO_RE.match(line):
                annotations.append(line)
                rm = REPLY_RE.match(line)
                if rm:
                    current["reply_to"] = int(rm.group(1))
                continue
            text_lines.append(line)
        for msg in flush():
            yield msg


def main():
    files = sorted(ROOT.glob("20*.txt"))
    n = 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as out:
        for path in files:
            for msg in parse_file(path):
                out.write(json.dumps(msg, ensure_ascii=False) + "\n")
                n += 1
    print(f"parsed {n} messages -> {OUT}")


if __name__ == "__main__":
    main()
