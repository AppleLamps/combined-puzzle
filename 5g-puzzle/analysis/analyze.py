#!/usr/bin/env python3
"""Quantitative analysis of GSMG Puzzle Solvers chat (2019-2026)."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

INP = Path("/tmp/gsmg/messages.jsonl")
OUTD = Path("/workspace/analysis")
OUTD.mkdir(parents=True, exist_ok=True)

# Topic / stall markers
TOPIC_PATTERNS = {
    "phase_3_2": re.compile(r"\b(3\.2|phase\s*3[.\s]*2|phase3_3\.2)\b", re.I),
    "salphaseion": re.compile(r"\bsalph(aseion)?\b", re.I),
    "aes_blob": re.compile(r"\b(aes|ciphertext|cyphertext|blob)\b", re.I),
    "dbbi": re.compile(r"\bdbbi\b", re.I),
    "faed": re.compile(r"\bfaed\b", re.I),
    "meganigma": re.compile(r"\bmeganigma\b", re.I),
    "seed_phrase": re.compile(r"\b(seed|mnemonic|btcseed|bip39)\b", re.I),
    "hint_request": re.compile(r"\b(hint|jrk|tiny hint)\b", re.I),
    "progress_claim": re.compile(r"\b(i (found|solved|cracked)|progress|breakthrough)\b", re.I),
    "stuck": re.compile(r"\b(stuck|unsolved|going in circles|still unsolved|dead end)\b", re.I),
    "scam_warning": re.compile(r"\b(scam|phishing|impersonat|fake)\b", re.I),
    "ban_moderation": re.compile(r"\b(ban|banned|admin|moderat)\b", re.I),
    "offtopic": re.compile(r"\b(off[- ]topic|spam|gif|meme)\b", re.I),
}

CONFLICT = re.compile(
    r"\b(idiot|stupid|shut up|bullshit|bs\b|waste of time|nobody cares|"
    r"toxic|troll|spam|ban him|ban this|you are wrong|you're wrong|"
    r"stop spamming|nonsense|gibberish|delusional|cope|"
    r"fuck|fucking|asshole|moron|clown)\b",
    re.I,
)
PASSIVE_AGG = re.compile(
    r"\b(good luck with that|sure jan|whatever\b|i guess nobody|"
    r"as usual|same as always|here we go again|nobody reads|"
    r"search the (chat|history|logs)|already (been )?(discussed|tried|said))\b",
    re.I,
)
INDECISION = re.compile(
    r"\b(maybe we should|not sure|i don't know|idk|could be|"
    r"what do you (all )?think|poll\b|should we|let's vote|"
    r"no consensus|undecided|who decides)\b",
    re.I,
)
STALL = re.compile(
    r"\b(going in circles|same (place|stage|phase)|years? (later|now)|"
    r"still (here|stuck|unsolved)|no progress|nothing new|"
    r"already tried|we already|dead end|looping)\b",
    re.I,
)
NEWCOMER = re.compile(
    r"\b(new here|just joined|where (do i|to) start|can someone (explain|catch me up)|"
    r"what's the (current|status)|what phase)\b",
    re.I,
)
KNOWLEDGE_LOSS = re.compile(
    r"\b(search the (chat|group|history)|read the (logs|history|pinned)|"
    r"already (explained|discussed|covered|posted)|look (it )?up|"
    r"this was (already|discussed))\b",
    re.I,
)


def load():
    msgs = []
    with INP.open(encoding="utf-8") as f:
        for line in f:
            msgs.append(json.loads(line))
    return msgs


def gini(counts):
    xs = sorted(c for c in counts if c > 0)
    if not xs:
        return 0.0
    n = len(xs)
    tot = sum(xs)
    acc = 0
    for i, x in enumerate(xs, 1):
        acc += i * x
    return (2 * acc) / (n * tot) - (n + 1) / n


def main():
    msgs = load()
    chat = [m for m in msgs if not m["service"]]
    svc = [m for m in msgs if m["service"]]

    by_year = defaultdict(list)
    by_month = defaultdict(list)
    by_uid = Counter()
    uid_name = {}
    uid_years = defaultdict(set)
    uid_first = {}
    uid_last = {}
    replies = 0
    reply_targets = Counter()

    for m in chat:
        by_year[m["year"]].append(m)
        month = (m["date"] or "")[:7]
        by_month[month].append(m)
        uid = m["uid"]
        by_uid[uid] += 1
        if m["author"]:
            uid_name[uid] = m["author"]
        uid_years[uid].add(m["year"])
        if uid not in uid_first:
            uid_first[uid] = m["ts"]
        uid_last[uid] = m["ts"]
        if m["reply_to"]:
            replies += 1
            reply_targets[m["reply_to"]] += 1

    # Service events
    joins = leaves = 0
    join_years = Counter()
    leave_years = Counter()
    for m in svc:
        t = (m.get("service_text") or "").lower()
        y = m["year"]
        if "joined" in t or "invited" in t:
            joins += 1
            join_years[y] += 1
        if "left" in t or "removed" in t or "kicked" in t or "banned" in t:
            leaves += 1
            leave_years[y] += 1

    # Yearly stats
    yearly = []
    all_n = len(chat)
    for y in sorted(by_year):
        ym = by_year[y]
        uids = Counter(m["uid"] for m in ym)
        n = len(ym)
        top5 = sum(c for _, c in uids.most_common(5))
        top10 = sum(c for _, c in uids.most_common(10))
        yearly.append({
            "year": y,
            "messages": n,
            "unique_posters": len(uids),
            "top1_share": round(uids.most_common(1)[0][1] / n, 3),
            "top5_share": round(top5 / n, 3),
            "top10_share": round(top10 / n, 3),
            "gini": round(gini(uids.values()), 3),
            "reply_rate": round(sum(1 for m in ym if m["reply_to"]) / n, 3),
            "joins": join_years[y],
            "leaves": leave_years[y],
            "top5": [
                {"name": uid_name.get(u, u), "uid": u, "n": c, "share": round(c / n, 3)}
                for u, c in uids.most_common(5)
            ],
        })

    # Retention: users posting in year Y who also posted in Y+1
    years = sorted(by_year)
    retention = []
    for i, y in enumerate(years[:-1]):
        a = set(m["uid"] for m in by_year[y])
        b = set(m["uid"] for m in by_year[years[i + 1]])
        retention.append({
            "from": y,
            "to": years[i + 1],
            "cohort": len(a),
            "returned": len(a & b),
            "rate": round(len(a & b) / len(a), 3) if a else 0,
        })

    # Multi-year veterans vs one-year
    year_span = Counter(len(ys) for ys in uid_years.values())
    veterans = [u for u, ys in uid_years.items() if len(ys) >= 4]
    one_year = [u for u, ys in uid_years.items() if len(ys) == 1]
    vet_msgs = sum(by_uid[u] for u in veterans)
    one_msgs = sum(by_uid[u] for u in one_year)

    # Topic hits by year
    topic_year = {k: Counter() for k in TOPIC_PATTERNS}
    topic_total = Counter()
    conflict_year = Counter()
    pagg_year = Counter()
    stall_year = Counter()
    indec_year = Counter()
    newc_year = Counter()
    know_year = Counter()
    conflict_examples = []
    stall_examples = []
    know_examples = []
    newc_examples = []
    stuck_examples = []

    for m in chat:
        text = m["text"] or ""
        y = m["year"]
        if not text:
            continue
        for k, pat in TOPIC_PATTERNS.items():
            if pat.search(text):
                topic_year[k][y] += 1
                topic_total[k] += 1
        if CONFLICT.search(text):
            conflict_year[y] += 1
            if len(conflict_examples) < 40:
                conflict_examples.append({
                    "id": m["id"], "ts": m["ts"], "author": m["author"],
                    "text": text[:240]
                })
        if PASSIVE_AGG.search(text):
            pagg_year[y] += 1
        if STALL.search(text):
            stall_year[y] += 1
            if len(stall_examples) < 40:
                stall_examples.append({
                    "id": m["id"], "ts": m["ts"], "author": m["author"],
                    "text": text[:280]
                })
        if INDECISION.search(text):
            indec_year[y] += 1
        if NEWCOMER.search(text):
            newc_year[y] += 1
            if len(newc_examples) < 25:
                newc_examples.append({
                    "id": m["id"], "ts": m["ts"], "author": m["author"],
                    "text": text[:240]
                })
        if KNOWLEDGE_LOSS.search(text):
            know_year[y] += 1
            if len(know_examples) < 25:
                know_examples.append({
                    "id": m["id"], "ts": m["ts"], "author": m["author"],
                    "text": text[:240]
                })
        if TOPIC_PATTERNS["stuck"].search(text) and len(stuck_examples) < 30:
            stuck_examples.append({
                "id": m["id"], "ts": m["ts"], "author": m["author"],
                "text": text[:280]
            })

    # Monthly volume
    monthly = [{"month": k, "n": len(v), "users": len({m["uid"] for m in v})}
               for k, v in sorted(by_month.items()) if k]

    # Overall concentration
    n = len(chat)
    top_overall = [
        {
            "name": uid_name.get(u, u),
            "uid": u,
            "n": c,
            "share": round(c / n, 4),
            "years": sorted(uid_years[u]),
            "span": len(uid_years[u]),
        }
        for u, c in by_uid.most_common(20)
    ]

    # Users who dominate then vanish
    vanish = []
    for u, c in by_uid.most_common(80):
        ys = sorted(uid_years[u])
        last = ys[-1]
        if last <= "2024" and c >= 80:
            vanish.append({
                "name": uid_name.get(u, u),
                "uid": u,
                "n": c,
                "years": ys,
                "last": last,
            })

    # Polls
    polls = []
    for m in chat:
        for a in m.get("annotations") or []:
            if a.startswith("(poll:"):
                polls.append({"id": m["id"], "ts": m["ts"], "author": m["author"], "poll": a[:300]})

    summary = {
        "corpus": {
            "total_blocks": len(msgs),
            "chat_messages": len(chat),
            "service_events": len(svc),
            "unique_authors": len(by_uid),
            "reply_rate": round(replies / n, 3),
            "date_range": [chat[0]["ts"], chat[-1]["ts"]],
            "joins": joins,
            "leaves": leaves,
        },
        "yearly": yearly,
        "retention": retention,
        "year_span_histogram": dict(sorted(year_span.items())),
        "veterans_4plus_years": {"users": len(veterans), "messages": vet_msgs, "share": round(vet_msgs / n, 3)},
        "one_year_users": {"users": len(one_year), "messages": one_msgs, "share": round(one_msgs / n, 3)},
        "top20_overall": top_overall,
        "top5_overall_share": round(sum(x["n"] for x in top_overall[:5]) / n, 3),
        "top20_overall_share": round(sum(x["n"] for x in top_overall) / n, 3),
        "gini_overall": round(gini(by_uid.values()), 3),
        "topic_totals": dict(topic_total),
        "topic_by_year": {k: dict(v) for k, v in topic_year.items()},
        "conflict_by_year": dict(conflict_year),
        "passive_agg_by_year": dict(pagg_year),
        "stall_by_year": dict(stall_year),
        "indecision_by_year": dict(indec_year),
        "newcomer_by_year": dict(newc_year),
        "knowledge_loss_by_year": dict(know_year),
        "conflict_rate_by_year": {
            y: round(conflict_year[y] / len(by_year[y]), 4) for y in sorted(by_year)
        },
        "stall_rate_by_year": {
            y: round(stall_year[y] / len(by_year[y]), 4) for y in sorted(by_year)
        },
        "early_dominators_who_left": vanish[:25],
        "poll_count": len(polls),
    }

    (OUTD / "stats.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    (OUTD / "monthly.json").write_text(json.dumps(monthly, indent=2))
    (OUTD / "examples.json").write_text(json.dumps({
        "conflict": conflict_examples,
        "stall": stall_examples,
        "knowledge_loss": know_examples,
        "newcomer": newc_examples,
        "stuck": stuck_examples,
        "polls": polls[:40],
    }, indent=2, ensure_ascii=False))

    print(json.dumps({
        "chat_messages": len(chat),
        "unique_authors": len(by_uid),
        "top5_share": summary["top5_overall_share"],
        "gini": summary["gini_overall"],
        "topic_totals": summary["topic_totals"],
        "yearly_messages": {y["year"]: y["messages"] for y in yearly},
        "retention": retention,
        "conflict_rate": summary["conflict_rate_by_year"],
        "stall_rate": summary["stall_rate_by_year"],
        "polls": len(polls),
        "veterans": summary["veterans_4plus_years"],
        "one_year": summary["one_year_users"],
    }, indent=2))


if __name__ == "__main__":
    main()
