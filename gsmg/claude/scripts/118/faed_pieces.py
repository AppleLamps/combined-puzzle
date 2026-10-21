#!/usr/bin/env python3
"""Doc 118 s1: faed is not homogeneous. Permutation tests of composition drift, the
searched change points, and rule 2 on each piece.

    python3 faed_pieces.py            # reads the soup from ../115/data/soup.txt
"""
import collections, itertools, math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
soup = open(os.path.join(HERE, '..', '115', 'data', 'soup.txt')).read()
faed = soup[195:765]; assert len(faed) == 570 and faed.startswith('faed')
A = 'abcdefghi'; N = len(faed)

def ll(s):
    c = collections.Counter(s); n = len(s)
    return sum(c[ch] * math.log(c[ch] / n) for ch in A if c[ch])
BASE = ll(faed)
def G(parts): return 2 * (sum(ll(p) for p in parts) - BASE)
def equal(s, k):
    n = len(s) // k; return [s[i * n:(i + 1) * n] for i in range(k)]

def rule2(blk):
    d = ''.join('0' if c == 'o' else str(ord(c) - 96) for c in blk)
    h = hex(int(d))[2:]; h = '0' + h if len(h) % 2 else h
    return bytes.fromhex(h)
def printable(b): return sum(32 <= c < 127 for c in b) / len(b)

r = random.Random(7); L = list(faed)
print('equal parts:')
for k in (2, 3, 4, 5, 6):
    obs = G(equal(faed, k)); sims = []
    for _ in range(4000):
        r.shuffle(L); sims.append(G(equal(''.join(L), k)))
    print(f'  k={k}: G={obs:.1f}  perm p={sum(x >= obs for x in sims) / len(sims):.4f}')

MIN, STEP = 30, 5
grid = range(MIN, N - MIN + 1, STEP)
def best_cuts(s, k):
    bv = None
    for cuts in itertools.combinations(grid, k - 1):
        b = (0,) + cuts + (N,)
        if any(y - x < MIN for x, y in zip(b, b[1:])): continue
        v = sum(ll(s[x:y]) for x, y in zip(b, b[1:]))
        if bv is None or v > bv[0]: bv = (v, cuts)
    return 2 * (bv[0] - ll(s)), bv[1]
print('searched cuts:')
for k, nsim in ((2, 300), (3, 300), (4, 60)):
    g, cuts = best_cuts(faed, k); sims = []
    for _ in range(nsim):
        r.shuffle(L); sims.append(best_cuts(''.join(L), k)[0])
    print(f'  k={k}: cuts {cuts} G={g:.1f}  perm p={sum(x >= g for x in sims) / nsim:.3f} ({nsim} null searches)')
    b = (0,) + cuts + (N,)
    for x, y in zip(b, b[1:]):
        c = collections.Counter(faed[x:y]); pt = rule2(faed[x:y]); ptr = rule2(faed[x:y][::-1])
        print(f'     [{x},{y}) ' + ' '.join(f'{ch}{c[ch]:3d}' for ch in A) +
              f'  rule2 printable {printable(pt):.2f} (rev {printable(ptr):.2f}) head {pt[:12]!r}')
