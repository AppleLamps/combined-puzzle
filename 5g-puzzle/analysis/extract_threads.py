#!/usr/bin/env python3
"""Extract first/last/count for unresolved topic phrases and key quote windows."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

INP = Path("/tmp/gsmg/messages.jsonl")
OUT = Path("/workspace/analysis/threads.json")

PHRASES = {
    "salphaseion": r"\bsalph(aseion)?\b",
    "phase_3.2": r"\b(3\.2|phase\s*3[.\s]*2)\b",
    "dbbi": r"\bdbbi\b",
    "faed": r"\bfaed\b",
    "meganigma": r"\bmeganigma\b",
    "aes_unsolved": r"\b(aes.{0,20}(unsolved|stuck)|unsolved.{0,20}aes|ciphertext.{0,20}blob|U2FsdGVk)\b",
    "going_in_circles": r"going in circles",
    "still_unsolved": r"still unsolved",
    "stuck_at": r"stuck (at|on|in)",
    "search_the_chat": r"search the (chat|group|history|logs)",
    "already_tried": r"already (tried|discussed|explained|covered|posted|said)",
    "no_progress": r"no progress",
    "need_hint": r"\b(need (a )?hint|jrk.*(hint|help)|give us a hint)\b",
    "ban_request": r"\b(ban him|ban this|please ban|should be banned)\b",
    "troll": r"\btroll(ing|s)?\b",
    "off_topic": r"\b(off[- ]topic|spam)\b",
    "where_to_start": r"\b(where (do i|to) start|new here|just joined|what phase are (we|you))\b",
    "private_key / 1GSMG": r"\b(1GSMG|private key|wallet)\b",
    "website_down": r"\b(website|gsmg\.io|site).{0,30}(down|vanish|gone|offline|disappear)",
    " koordinats / rabbit": r"\b(rabbit|phase 0|phase 1)\b",
}


def load():
    with INP.open(encoding="utf-8") as f:
        return [json.loads(l) for l in f]


def snippets(msgs, pat, limit=8):
    rx = re.compile(pat, re.I)
    hits = []
    for m in msgs:
        if m["service"]:
            continue
        t = m.get("text") or ""
        if rx.search(t):
            hits.append({
                "id": m["id"],
                "ts": m["ts"],
                "author": m["author"],
                "text": t.replace("\n", " ")[:320],
            })
    return {
        "count": len(hits),
        "first": hits[0] if hits else None,
        "last": hits[-1] if hits else None,
        "by_year": dict(Counter(h["ts"][:4] for h in hits)),
        "samples": hits[:3] + hits[-3:] if len(hits) > 6 else hits,
        "mid": hits[len(hits)//2] if hits else None,
    }


def author_concentration(msgs):
    chat = [m for m in msgs if not m["service"]]
    # Cumulative share
    c = Counter(m["uid"] for m in chat)
    n = len(chat)
    running = 0
    thresholds = {}
    for i, (u, k) in enumerate(c.most_common(), 1):
        running += k
        for t in (0.25, 0.50, 0.80):
            if t not in thresholds and running / n >= t:
                thresholds[t] = i
    # Year-to-year top-poster identity churn
    by_year = defaultdict(Counter)
    names = {}
    for m in chat:
        by_year[m["year"]][m["uid"]] += 1
        names[m["uid"]] = m["author"]
    top_ids = {}
    for y, cnt in by_year.items():
        top_ids[y] = [(names.get(u), u, k) for u, k in cnt.most_common(3)]
    return {"n_for_share": thresholds, "yearly_top3": top_ids}


def service_stats(msgs):
    kinds = Counter()
    for m in msgs:
        if not m["service"]:
            continue
        t = (m.get("service_text") or "").lower()
        if "joined" in t:
            kinds["joined"] += 1
        elif "left" in t:
            kinds["left"] += 1
        elif "removed" in t or "kicked" in t:
            kinds["removed_kicked"] += 1
        elif "banned" in t:
            kinds["banned"] += 1
        elif "title" in t or "photo" in t:
            kinds["cosmetic"] += 1
        else:
            kinds["other"] += 1
    return dict(kinds)


def main():
    msgs = load()
    out = {
        "threads": {name: snippets(msgs, pat) for name, pat in PHRASES.items()},
        "concentration": author_concentration(msgs),
        "service": service_stats(msgs),
    }
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    # compact print
    compact = {}
    for k, v in out["threads"].items():
        compact[k] = {
            "count": v["count"],
            "span": [v["first"]["ts"] if v["first"] else None, v["last"]["ts"] if v["last"] else None],
            "by_year": v["by_year"],
        }
    print(json.dumps({
        "threads": compact,
        "concentration": out["concentration"]["n_for_share"],
        "yearly_top3": out["concentration"]["yearly_top3"],
        "service": out["service"],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
