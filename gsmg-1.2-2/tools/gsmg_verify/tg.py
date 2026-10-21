import json, glob, sys, html, re
from pathlib import Path

REPO = str(Path(__file__).resolve().parent.parent.parent / 'gsmg-group-telegram-by-year')
_idx = None

def load():
    global _idx
    if _idx is not None:
        return _idx
    idx = {}
    for fn in sorted(glob.glob(REPO + '/*.json')):
        d = json.load(open(fn, encoding='utf-8'))
        for m in d['messages']:
            idx[m['id']] = m
    _idx = idx
    return idx

def text_of(m):
    t = m.get('text', '')
    if isinstance(t, list):
        out = []
        for part in t:
            if isinstance(part, str):
                out.append(part)
            elif isinstance(part, dict):
                out.append(part.get('text', ''))
        return ''.join(out)
    return t or ''

def show(mid, indent=''):
    idx = load()
    m = idx.get(mid)
    if not m:
        print(f'{indent}#{mid}: NOT FOUND in export')
        return
    author = m.get('from', m.get('actor', '<unknown>'))
    date = m.get('date', '')
    txt = text_of(m)
    reply = m.get('reply_to_message_id')
    # A forwarded message's `from` is the forwarder, not the author. Showing
    # forwarded_from is essential for attribution -- omitting it once caused a
    # creator-authored line to be misread as a solver's (SESSION-LOG-141).
    fwd = m.get('forwarded_from')
    fwd_note = f'  [FORWARDED FROM {fwd!r}]' if fwd else ''
    print(f'{indent}#{mid} [{date}] {author}{fwd_note}: {txt!r}' + (f'  (reply_to=#{reply})' if reply else ''))
    return m

def show_with_parent(mid, indent=''):
    m = show(mid, indent)
    if m and m.get('reply_to_message_id'):
        show(m['reply_to_message_id'], indent + '  <- ')

def near(mid, before=1, after=1):
    idx = load()
    ids = sorted(idx.keys())
    pos = ids.index(mid) if mid in ids else None
    if pos is None:
        print(f'#{mid} not found'); return
    for i in ids[max(0,pos-before):pos+after+1]:
        show(i)

if __name__ == '__main__':
    for mid in sys.argv[1:]:
        show_with_parent(int(mid))
        print()
