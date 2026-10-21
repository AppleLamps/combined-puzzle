#!/usr/bin/env python3
"""Doc 116 extra families (small, single process):
  opret     every OP_RETURN string paid to the prize address (opret.tsv), alone and joined
  cjoins    2- to 6-grams across runs of consecutive creator messages (within 15 min),
            spaced and joined, both cases: "he says everything twice"
  pairs     each creator endorsement's parent text joined with the creator reply
"""
import hashlib, os, re, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '115'))
import harness as H, prun
from controls import planted_container, planted_target
from tg import load, text, CREATOR_ID
from sweep import uniq, STRIP, run_family

def on_chain():
    """The OP_RETURN strings paid to the prize address, from the checked-in transaction
    table opret.tsv (paged from the mempool.space address API; doc 117 s3). The data hex
    is decoded here and checked against the table's text column, so a transcription
    error in either column fails loudly."""
    out = []
    for line in open(os.path.join(HERE, 'opret.tsv'), encoding='utf-8'):
        if line.startswith('#') or not line.strip(): continue
        h, d, txid, k, spk, datahex, txt = line.rstrip('\n').split('\t')
        data = bytes.fromhex(datahex)
        assert spk.startswith('6a') and data.hex() in spk, txid
        assert data.decode('utf-8', 'replace') == txt, txid
        out.append(txt)
    return out

# Strings the sweep also carries that are not OP_RETURN outputs on the prize address:
# cuts of the on-chain strings a reader would try, the film line in its own words, and
# "Good job Neo", which a 2020 message (#4652) asks about and which is not on the address.
DERIVED = ['Everything That Has A Beginning Has An End', 'Everything That Has A Beginnin Has An End',
           'FromN0EHalfABetterHalfBuiltItBellaCiao1', 'HalfABetterHalfBuiltIt', 'BellaCiao',
           '5 BTC', 'Good job Neo', 'happy xmas!', 'Everything That Has A Beginnin Has An End']
OPRET = sorted(set(on_chain()) | set(DERIVED))

def fam_opret():
    out = []
    forms = set()
    for s in OPRET:
        for v in (s, s.lower(), s.replace(' ', ''), s.lower().replace(' ', ''), re.sub(r'[^A-Za-z0-9]', '', s).lower()):
            forms.add(v)
    for a in forms:
        out.append(('op', a.encode()))
        for b in forms:  # every ordered pair, self-pairs included
            out.append(('op2', (a + b).encode()))
    return uniq(out)

def fam_cjoins(b):
    C = [m for m in b.values() if m['type'] == 'message' and m.get('from_id') == CREATOR_ID and text(m)]
    runs = []; cur = []
    for m in C:
        if cur and int(m['date_unixtime']) - int(cur[-1]['date_unixtime']) > 900:
            runs.append(cur); cur = []
        cur.append(m)
    if cur: runs.append(cur)
    out = []
    for r in runs:
        if len(r) < 2: continue
        toks = []
        for m in r: toks += [STRIP.sub('', x) for x in text(m).split()]
        toks = [x for x in toks if x]
        for n in range(2, 7):
            for i in range(len(toks) - n + 1):
                g = toks[i:i + n]
                for v in (' '.join(g), ''.join(g), ' '.join(g).lower(), ''.join(g).lower()):
                    out.append((f'cj{n}', v.encode()))
        # whole run joined
        for v in (' '.join(text(m) for m in r), ''.join(toks), ''.join(toks).lower()):
            out.append(('cjrun', v.encode()))
    return uniq(out)

def fam_pairs(b):
    ids = list(b); out = []
    for m in b.values():
        if m['type'] != 'message' or m.get('from_id') != CREATOR_ID: continue
        t = text(m)
        if not t or len(t) > 60: continue
        p = b.get(m.get('reply_to_message_id'))
        if p is None:
            k = ids.index(m['id']) - 1
            while k >= 0 and (b[ids[k]].get('from_id') == CREATOR_ID or b[ids[k]]['type'] != 'message'): k -= 1
            p = b[ids[k]] if k >= 0 else None
        if p is None or not text(p): continue
        pt = text(p)
        ptoks = ''.join(STRIP.sub('', x) for x in pt.split()); ttoks = ''.join(STRIP.sub('', x) for x in t.split())
        for v in (pt + t, pt + ' ' + t, t + pt, ptoks + ttoks, (ptoks + ttoks).lower(), (ttoks + ptoks).lower(), pt, pt.lower(), ptoks.lower()):
            out.append(('pair', v.encode()))
    return uniq(out)

if __name__ == '__main__':
    b = load()
    fams = sys.argv[1:] or ['opret', 'cjoins', 'pairs']
    for i, name in enumerate(fams):
        items = {'opret': lambda: fam_opret(), 'cjoins': lambda: fam_cjoins(b), 'pairs': lambda: fam_pairs(b)}[name]()
        print(f'[{name}] {len(items)} candidates', flush=True)
        run_family(name, items, seed=200 + i)
