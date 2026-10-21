import itertools, random
from collections import Counter
t = open('files/salphaseion-textarea.txt').read().strip(); r1 = t[:91]
def parse(r, sel):
    out = []; i = 0
    while i < len(r):
        if r[i] in sel:
            if i+1 >= len(r): return None
            out.append(r[i:i+2]); i += 2
        else: out.append(r[i]); i += 1
    return out
def ic(sym):
    n = len(sym); c = Counter(sym); return sum(v*(v-1) for v in c.values())/(n*(n-1))
random.seed(3)
for k in (1, 2, 3):
    for sel in itertools.combinations('abcdefghi', k):
        for nm, r in (('fwd', r1), ('rev', r1[::-1])):
            s = parse(r, sel)
            if not s: continue
            null = []
            for _ in range(300):
                sh = list(r); random.shuffle(sh); p = parse(''.join(sh), sel)
                if p: null.append(ic(p))
            null.sort(); pct = sum(x < ic(s) for x in null)/len(null)
            if pct > 0.97 or sel == ('b', 'e'):
                print(sel, nm, 'symbols', len(s), 'distinct', len(set(s)), 'IC %.4f' % ic(s), 'null median %.4f' % null[len(null)//2], 'pct %.2f' % pct, Counter(s).most_common(8))
