#!/usr/bin/env python3
"""
Copy ONLY the media / files / attachments that were sent by the chat creator
("jrk" = "Jrk Bgrt" = user9815232) out of a Telegram Desktop export.

The creator is selected by from_id (never by display-name string), so renamed
accounts cannot be picked up by mistake.

What counts as an attachment: the message keys that reference a file inside the
export folder - "photo", "file" (documents / animations / video / audio /
voice / stickers) and "thumbnail" (an auto-generated preview, tagged as such in
the manifest, not a file the creator sent).

Layout of the output folder mirrors the export (photos/, video_files/,
stickers/, ...) so every copied name still matches the path in result.json.
A tab-separated manifest indexes every copied file back to its message.

Usage:
    python extract_creator_attachments.py
    python extract_creator_attachments.py --json <path> --out <folder>
    python extract_creator_attachments.py --no-thumbnails
"""

import argparse
import json
import os
import shutil
import sys

CREATOR_ID = "user9815232"      # jrk
CREATOR_NAME = "Jrk Bgrt"
REF_KEYS = ("photo", "file", "thumbnail")


def render_text(msg):
    """Flatten Telegram's text / text_entities pair into one plain string."""
    text = msg.get("text", "")
    if isinstance(text, str):
        return text
    parts = []
    for chunk in text:
        if isinstance(chunk, str):
            parts.append(chunk)
        elif isinstance(chunk, dict):
            parts.append(chunk.get("text", ""))
    return "".join(parts)


def refs_of(msg, with_thumbnails=True):
    """Yield (role, relative_path) for every attachment reference on a message."""
    for key in REF_KEYS:
        rel = msg.get(key)
        if not isinstance(rel, str) or not rel or rel.startswith("("):
            continue            # "(File not included...)" placeholder
        role = "thumbnail" if key == "thumbnail" else "attachment"
        if role == "thumbnail" and not with_thumbnails:
            continue
        yield role, rel


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=os.path.join(here, "result.json"))
    ap.add_argument("--out", default=r"D:\newest-puzzle-9.9.26-creator-attachments")
    ap.add_argument("--creator-id", default=CREATOR_ID)
    ap.add_argument("--no-thumbnails", action="store_true",
                    help="skip the auto-generated *_thumb.jpg previews")
    args = ap.parse_args()

    source_root = os.path.dirname(os.path.abspath(args.json))
    with open(args.json, encoding="utf-8") as fh:
        data = json.load(fh)

    rows = []
    copied = 0
    bytes_total = 0
    missing = []
    for msg in data["messages"]:
        if msg.get("type") != "message" or msg.get("from_id") != args.creator_id:
            continue
        for role, rel in refs_of(msg, not args.no_thumbnails):
            src = os.path.join(source_root, rel.replace("/", os.sep))
            dst = os.path.join(args.out, rel.replace("/", os.sep))
            if not os.path.exists(src):
                missing.append(rel)
                continue
            if not os.path.exists(dst):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)          # copy2 keeps mtime
                copied += 1
            bytes_total += os.path.getsize(src)
            rows.append({
                "id": msg["id"],
                "date": msg["date"],
                "media_type": msg.get("media_type") or ("photo" if "photo" in msg else "file"),
                "role": role,
                "bytes": os.path.getsize(src),
                "export_path": rel,
                "copied_path": os.path.relpath(dst, args.out).replace(os.sep, "/"),
                "file_name": msg.get("file_name", ""),
                "duration_s": msg.get("duration_seconds", ""),
                "caption": " ".join(render_text(msg).split()),
            })

    rows.sort(key=lambda r: (r["id"], r["role"], r["export_path"]))
    man_path = os.path.join(args.out, "creator_attachments.tsv")
    if rows:
        os.makedirs(args.out, exist_ok=True)
        cols = list(rows[0].keys())
        with open(man_path, "w", encoding="utf-8", newline="\r\n") as fh:
            fh.write("\t".join(cols) + "\n")
            for r in rows:
                fh.write("\t".join(str(r[c]).replace("\t", " ").replace("\n", " ") for c in cols) + "\n")

    msgs = {r["id"] for r in rows if r["role"] == "attachment"}
    att = [r for r in rows if r["role"] == "attachment"]
    thm = [r for r in rows if r["role"] == "thumbnail"]
    print("creator            : %s (%s)" % (CREATOR_NAME, args.creator_id))
    print("source export      : %s" % args.json)
    print("output folder      : %s" % args.out)
    print("attachment files   : %d (%d bytes) across %d messages" % (
        len(att), sum(r["bytes"] for r in att), len(msgs)))
    print("thumbnail previews : %d (%d bytes)%s" % (
        len(thm), sum(r["bytes"] for r in thm),
        " [skipped]" if args.no_thumbnails else ""))
    print("files written      : %d" % copied)
    print("manifest           : %s" % man_path)
    if missing:
        print("MISSING ON DISK    : %d -> %s" % (len(missing), missing[:5]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
