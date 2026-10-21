#!/usr/bin/env python3
"""Loader and query tool for the Telegram export in by-year/*.json.

Usage (from the repo root):
    python3 claude/scripts/telegram/tg.py get 8446 53342        # print messages by id
    python3 claude/scripts/telegram/tg.py thread 60312           # message with its reply chain
    python3 claude/scripts/telegram/tg.py creator                # every creator message, one per line
    python3 claude/scripts/telegram/tg.py audit GSMG-PUZZLE-DOSSIER.md   # check every #id the dossier cites
    python3 claude/scripts/telegram/tg.py inventory              # per-year counts and id ranges

Importable: load() -> dict id -> message; text(m) -> flattened text.
"""
import collections
import glob
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
EXPORT_GLOB = os.path.join(ROOT, 'by-year', '*.json')
CREATOR_ID = 'user9815232'          # "Jrk Bgrt" in the export; SoWut on the site
CREATOR_NAME = 'Jrk Bgrt'


def text(m):
    """Flatten a Telegram export text field (str or list of str/entity) to str."""
    t = m.get('text', '')
    if isinstance(t, list):
        return ''.join(x if isinstance(x, str) else x.get('text', '') for x in t)
    return t or ''


def load():
    """Return an ordered dict id -> message across every by-year file."""
    byid = collections.OrderedDict()
    for f in sorted(glob.glob(EXPORT_GLOB)):
        for m in json.load(open(f, encoding='utf-8'))['messages']:
            byid[m['id']] = m
    return byid


def who(m):
    return m.get('from') or m.get('actor') or m.get('from_id') or m.get('actor_id') or '?'


def fmt(m, width=None):
    t = text(m).replace('\n', ' / ')
    if width:
        t = t[:width]
    extra = ''
    if 'reply_to_message_id' in m:
        extra += f' (reply to {m["reply_to_message_id"]})'
    if m.get('photo'):
        extra += ' [photo]'
    if m.get('file'):
        extra += f' [file {m.get("file_name", "")}]'.rstrip()
    if m['type'] == 'service':
        extra += f' [service: {m.get("action")}]'
    return f'#{m["id"]} {m["date"]} {who(m)}{extra}: {t}'


def creator_messages(byid):
    return [m for m in byid.values() if m['type'] == 'message' and m.get('from_id') == CREATOR_ID]


def cmd_get(byid, ids):
    for i in ids:
        m = byid.get(int(i))
        print(fmt(m) if m else f'#{i} NOT IN EXPORT')


def cmd_thread(byid, ids):
    for i in ids:
        chain = []
        m = byid.get(int(i))
        while m is not None:
            chain.append(m)
            m = byid.get(m.get('reply_to_message_id'))
        for m in reversed(chain):
            print(fmt(m))
        print()


def cmd_creator(byid):
    for m in creator_messages(byid):
        print(fmt(m))


def cmd_inventory(byid):
    per = collections.OrderedDict()
    for m in byid.values():
        y = m['date'][:4]
        d = per.setdefault(y, {'n': 0, 'msg': 0, 'svc': 0, 'creator': 0, 'lo': m['id'], 'hi': m['id'],
                               'first': m['date'][:10], 'last': m['date'][:10]})
        d['n'] += 1
        d['msg' if m['type'] == 'message' else 'svc'] += 1
        d['creator'] += m['type'] == 'message' and m.get('from_id') == CREATOR_ID
        d['hi'] = m['id']
        d['last'] = m['date'][:10]
    print('year  total  messages  service  creator  first_id  last_id  first_date  last_date')
    for y, d in per.items():
        print(f"{y}  {d['n']:5d}  {d['msg']:8d}  {d['svc']:7d}  {d['creator']:7d}  {d['lo']:8d}  {d['hi']:7d}  {d['first']}  {d['last']}")
    ids = list(byid)
    print(f'total {len(ids)} rows, ids {min(ids)}..{max(ids)}, '
          f'{max(ids) - min(ids) + 1 - len(ids)} ids absent (deleted messages)')


def cmd_audit(byid, path):
    """Every #NNNN in the file must exist in the export."""
    src = open(path, encoding='utf-8').read()
    cited = sorted({int(x) for x in re.findall(r'#(\d{2,6})\b', src)})
    missing = [i for i in cited if i not in byid]
    svc = [i for i in cited if i in byid and byid[i]['type'] == 'service']
    print(f'{len(cited)} distinct ids cited; {len(missing)} not in export; {len(svc)} are service rows')
    for i in missing:
        print('  MISSING', i)
    for i in svc:
        print('  SERVICE', fmt(byid[i], 80))
    return cited, missing


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    byid = load()
    cmd, args = argv[1], argv[2:]
    if cmd == 'get':
        cmd_get(byid, args)
    elif cmd == 'thread':
        cmd_thread(byid, args)
    elif cmd == 'creator':
        cmd_creator(byid)
    elif cmd == 'inventory':
        cmd_inventory(byid)
    elif cmd == 'audit':
        cmd_audit(byid, args[0] if args else os.path.join(ROOT, 'GSMG-PUZZLE-DOSSIER.md'))
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
