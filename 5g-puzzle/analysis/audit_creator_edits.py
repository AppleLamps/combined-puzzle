#!/usr/bin/env python3
"""
Audit: how often were messages retroactively edited, creator vs everyone else?

Reads the 2019-2022 transcripts and compares each message's day-header year to
the year in its "(edited YYYY-MM-DD ...)" annotation.

Run from the repo root: python3 analysis/audit_creator_edits.py
"""
import re, collections, sys, os

CREATOR = "user9815232"          # Jrk Bgrt
FILES = ["2019.txt", "2020.txt", "2021.txt", "2022.txt"]

hdr = re.compile(r'^\[#(\d+)\] \d\d:\d\d:\d\d (.*) \((user\d+)\)$')
day = re.compile(r'^## DAY (\d{4})-')


def main():
    stats = collections.defaultdict(lambda: [0, 0, 0])   # total, edited, edited >=2y later
    for f in FILES:
        if not os.path.exists(f):
            sys.exit(f"run from the repo root; missing {f}")
        year, cur, buf = None, None, []

        def flush():
            if cur:
                uid, y = cur
                s = stats[uid]
                s[0] += 1
                m = re.search(r'\(edited (\d{4})-', ''.join(buf))
                if m:
                    s[1] += 1
                    if int(m.group(1)) - int(y) >= 2:
                        s[2] += 1

        for line in open(f, errors='replace'):
            l = line.rstrip('\n')
            d = day.match(l)
            if d:
                year = d.group(1)
            h = hdr.match(l)
            if h:
                flush()
                cur, buf = (h.group(3), year), []
            elif cur:
                buf.append(l)
        flush()

    print(f"{'user':16s} {'msgs':>6s} {'edited':>7s} {'late(>=2y)':>11s}  late%")
    for uid, (t, e, l) in sorted(stats.items(), key=lambda kv: -kv[1][0])[:15]:
        tag = "  <-- CREATOR" if uid == CREATOR else ""
        print(f"{uid:16s} {t:6d} {e:7d} {l:11d}  {100*l/t:5.1f}%{tag}")

    tot = sum(v[0] for v in stats.values())
    late = sum(v[2] for v in stats.values())
    c = stats[CREATOR]
    print(f"\nall users 2019-2022 : {tot} msgs, {late} edited >=2y later ({100*late/tot:.1f}%)")
    print(f"creator             : {c[0]} msgs, {c[2]} edited >=2y later ({100*c[2]/c[0]:.1f}%)")
    print(f"\ncreator is {(c[2]/c[0])/(late/tot):.1f}x the baseline rate.")
    print("NOTE: an edit flag says a message changed, not what changed. Compare")
    print("against external archives (GitHub write-ups, Reddit quotes, old exports)")
    print("before treating any specific hint text as original.")


if __name__ == "__main__":
    main()
