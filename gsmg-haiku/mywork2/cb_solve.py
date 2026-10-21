"""Test the hypothesis that the SalPhaseIon a-i runs are straddling-checkerboard text.
For every selector set, parse the digits into symbols and hill-climb a symbol->letter
substitution against an English quadgram model. Includes a positive control."""
import sys, re, itertools, random, pydoc_data.topics as T
import numpy as np
random.seed(7); rng = np.random.default_rng(7)
corpus = ' '.join(T.topics.values()) + open('matrix-reloaded.txt', encoding='utf-8').read() * 3 \
    + open('mywork/wikiquote_reloaded.txt', encoding='utf-8', errors='ignore').read() * 3 \
    + open('derived/architect-text.txt').read() * 3
L = np.frombuffer(re.sub('[^a-z]', '', corpus.lower()).encode(), dtype=np.uint8).astype(np.int64) - 97
q = np.ones(26 ** 4)
np.add.at(q, L[:-3] * 17576 + L[1:-2] * 676 + L[2:-1] * 26 + L[3:], 1)
Q = np.log(q / q.sum())

def score(a):
    return Q[a[:-3] * 17576 + a[1:-2] * 676 + a[2:-1] * 26 + a[3:]].sum() / (len(a) - 3)

def parse(d, sel):
    i = 0; out = []
    while i < len(d):
        if d[i] in sel:
            if i + 1 >= len(d): return None
            out.append(d[i:i + 2]); i += 2
        else:
            out.append(d[i]); i += 1
    return out

def solve(sym, restarts=4, iters=12000, T0=0.06):
    """simulated annealing over symbol->letter assignments (injective unless >26 symbols)"""
    ids = {s: i for i, s in enumerate(sorted(set(sym)))}
    x = np.array([ids[s] for s in sym]); n = len(ids)
    pool0 = np.tile(np.arange(26), 2 if n > 26 else 1)
    best = (-99, None)
    for _ in range(restarts):
        pool = rng.permutation(pool0); cur = score(pool[:n][x])
        R = rng.random(iters); I = rng.integers(0, n, iters); J = rng.integers(0, len(pool), iters)
        for k in range(iters):
            i, j = I[k], J[k]
            if pool[i] == pool[j]: continue
            pool[i], pool[j] = pool[j], pool[i]
            s = score(pool[:n][x]); T = T0 * (1 - k / iters) + 1e-4
            if s > cur or R[k] < np.exp((s - cur) / T): cur = s
            else: pool[i], pool[j] = pool[j], pool[i]
        if cur > best[0]: best = (cur, ''.join(chr(97 + c) for c in pool[:n][x]))
    return best

def encode(text, sel):
    cells = [d for d in '123456789' if d not in sel] + [s + d for s in sel for d in '123456789']
    al = list('abcdefghijklmnopqrstuvwxyz'); random.shuffle(al)
    mp = {c: cells[i % len(cells)] for i, c in enumerate(al[:len(cells)])}
    return ''.join(mp[c] for c in text if c in mp)

if __name__ == '__main__':
    CONTROL_ONLY = len(sys.argv) > 1
    t = open('files/salphaseion-textarea.txt').read().strip().translate(str.maketrans('abcdefghi', '123456789'))
    r1, r2 = t[:91], t[195:765]
    eng = re.sub('[^a-z]', '', open('derived/checkerboard-plaintext.txt').read().lower() +
                 "itwasthebestoftimesitwastheworstoftimesitwastheageofwisdomitwastheageoffoolishnessitwastheepochofbeliefitwastheepochofincredulityitwastheseasonoflightitwastheseasonofdarknessitwasthespringofhopeitwasthewinterofdespairwehadeverythingbeforeuswehadnothingbeforeuswewereallgoingdirecttoheavenwewereallgoingdirecttheotherwayinshorttheperiodwassofarlikethepresentperiodthatsomeofitsnoisiestauthoritiesinsistedonitsbeingreceivedforgoodorforevilinthesuperlativedegreeofcomparisononly")
    print('english reference score %.2f' % score(np.frombuffer(eng.encode(), dtype=np.uint8).astype(np.int64) - 97))
    ctl = encode(eng, '37')[:570]
    print('CONTROL (true sel 37):')
    for sel in ('37', '26', '15', '378'):
        s, pt = solve(parse(ctl, sel) or parse(ctl[:-1], sel)); print('  sel', sel, '%.2f' % s, pt[:90])
    if CONTROL_ONLY: sys.exit()
    for name, r in (('r2', r2), ('r1+r2', r1 + r2), ('r2+r1', r2 + r1)):
        res = []
        for k in (1, 2, 3):
            for sel in itertools.combinations('123456789', k):
                sym = parse(r, sel)
                if not sym: continue
                s, pt = solve(sym, restarts=3)
                res.append((s, ''.join(sel), len(sym), pt))
        res.sort(reverse=True)
        print(name)
        for s, sel, n, pt in res[:6]: print('  %.2f sel=%s n=%d %s' % (s, sel, n, pt[:100]))
        print('  worst %.2f' % res[-1][0])
