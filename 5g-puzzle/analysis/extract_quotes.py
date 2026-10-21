#!/usr/bin/env python3
"""Targeted qualitative extracts for the comms report."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

INP = Path("/tmp/gsmg/messages.jsonl")
OUT = Path("/workspace/analysis/quotes.json")


def load():
    with INP.open(encoding="utf-8") as f:
        return [json.loads(l) for l in f]


def find(msgs, pred, limit=12):
    hits = []
    for m in msgs:
        if m["service"]:
            continue
        if pred(m):
            hits.append({
                "id": m["id"], "ts": m["ts"], "author": m["author"],
                "text": (m.get("text") or "").replace("\n", " ")[:400],
            })
            if len(hits) >= limit:
                break
    return hits


def main():
    msgs = load()
    chat = [m for m in msgs if not m["service"]]

    # Jrk activity
    jrk = [m for m in chat if m["uid"] == "9815232"]
    jrk_years = Counter(m["year"] for m in jrk)
    jrk_hint = [m for m in jrk if re.search(r"hint", m.get("text") or "", re.I)]

    # 2022 sample of all unique posters / tone of collapse
    y2022 = [m for m in chat if m["year"] == "2022"]

    patterns = {
        "circles_or_loop": r"going in circles|looping|same place for years|stuck for (many )?years|years sometimes",
        "admin_vacuum": r"admin (doesn'?t|does not) care|nobody cares|channel is doomed|no moderat",
        "current_task_unclear": r"current task|where are we|what (phase|stage) are we|confirm that this is still unsolved",
        "competing_paths": r"salph|3\.2",  # handled separately
        "creator_dependence": r"\bjrk\b.{0,80}(hint|post|share)|wait(ing)? for (a )?hint|need jrk",
        "wiki_or_docs": r"\b(wiki|github|writeup|document(ation)?|pinned|faq)\b",
        "hypothesis_reject": r"already tried|doesn'?t work|none of them work|dead end|not the way",
        "share_or_secret": r"\b(dm me|i solved|i have the (key|answer)|won'?t share|secret)\b",
    }

    out = {
        "jrk": {
            "messages": len(jrk),
            "by_year": dict(jrk_years),
            "hint_msgs": len(jrk_hint),
            "first": jrk[0]["ts"] if jrk else None,
            "last": jrk[-1]["ts"] if jrk else None,
            "sample_hints": [
                {"id": m["id"], "ts": m["ts"], "text": (m.get("text") or "")[:300]}
                for m in jrk_hint[:8]
            ],
        },
        "y2022_n": len(y2022),
        "y2022_sample": [
            {"id": m["id"], "ts": m["ts"], "author": m["author"],
             "text": (m.get("text") or "")[:240]}
            for m in y2022 if (m.get("text") or "").strip()
        ][:15] + [
            {"id": m["id"], "ts": m["ts"], "author": m["author"],
             "text": (m.get("text") or "")[:240]}
            for m in y2022 if (m.get("text") or "").strip()
        ][-8:],
        "quotes": {},
        "wiki_count": 0,
    }

    for name, pat in patterns.items():
        rx = re.compile(pat, re.I)
        hits = []
        for m in chat:
            t = m.get("text") or ""
            if rx.search(t):
                hits.append({
                    "id": m["id"], "ts": m["ts"], "author": m["author"],
                    "text": t.replace("\n", " ")[:380],
                })
        out["quotes"][name] = {
            "count": len(hits),
            "first_last": [hits[0] if hits else None, hits[-1] if hits else None],
            "samples": (hits[:4] + hits[-4:]) if len(hits) > 8 else hits,
        }

    # High-signal exact-ish quotes we already saw
    keys = [
        "Does anyone have a solution to any of the publicly unsolved",
        "everyone is stuck at 3.2",
        "going in circles for years",
        "admin doesn't care",
        "channel is doomed",
        "P.S. The puzzle is still unsolved",
        "This was fun a few years ago",
        "Has any progress been made so far",
        "confirm that this is still unsolved",
        "We already have dozens of suggestions, and none of them work",
        "probably we will get to the next halving",
        "where to start",
        "blob dbbi",
        "unsolved parts of this puzzle that remain",
        "Nobody understood the phrase",
        "I'm going to retire from this chat",
        "Here we go again with Bob",
        "Please ban him",
        "website vanishes",
        "community-maintained",
    ]
    keyed = {}
    for k in keys:
        rx = re.compile(re.escape(k), re.I)
        for m in chat:
            t = m.get("text") or ""
            if rx.search(t):
                keyed.setdefault(k, []).append({
                    "id": m["id"], "ts": m["ts"], "author": m["author"],
                    "text": t.replace("\n", " ")[:450],
                })
    out["keyed"] = {k: v[:3] for k, v in keyed.items()}

    # Monthly 2021-2023 to show collapse
    months = Counter()
    for m in chat:
        if m["date"] and m["date"][:4] in {"2021", "2022", "2023"}:
            months[m["date"][:7]] += 1
    out["monthly_2021_2023"] = dict(sorted(months.items()))

    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print("jrk", out["jrk"]["messages"], out["jrk"]["by_year"], "last", out["jrk"]["last"])
    print("wiki/docs mentions", out["quotes"]["wiki_or_docs"]["count"])
    print("circles", out["quotes"]["circles_or_loop"]["count"])
    print("admin", out["quotes"]["admin_vacuum"]["count"])
    print("creator dep", out["quotes"]["creator_dependence"]["count"])
    print("keyed hits", {k: len(v) for k, v in keyed.items() if v})


if __name__ == "__main__":
    main()
