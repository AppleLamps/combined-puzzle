"""Doc 115 s3: g-specific periodicity in faed. For every period 2..200 and offset, the
binomial z of g's at positions = offset (mod period); the best z, against 200 seeded
shuffles. Control: a string with g forced at every 7th position from offset 3."""
import math, random
from gapwalk import BLOCKS

def best_period(s, ch='g', pmax=200):
    pos = [i for i, c in enumerate(s) if c == ch]; n = len(s); rate = len(pos) / n
    best = (0, None)
    for p in range(2, pmax + 1):
        cnt = [0] * p; tot = [0] * p
        for i in range(n): tot[i % p] += 1
        for i in pos: cnt[i % p] += 1
        for o in range(p):
            if tot[o] < 5: continue
            z = (cnt[o] - tot[o] * rate) / math.sqrt(tot[o] * rate * (1 - rate))
            if z > best[0]: best = (z, (p, o, cnt[o], tot[o]))
    return best

if __name__ == '__main__':
    faed = BLOCKS['faed']
    r0 = random.Random(5); l = list(faed); r0.shuffle(l)
    for i in range(3, 570, 7): l[i] = 'g'
    print('control (g at every 7th from 3):', best_period(''.join(l)))
    obs = best_period(faed); print('observed best', obs)
    r = random.Random(1); null = []
    for _ in range(200):
        l = list(faed); r.shuffle(l); null.append(best_period(''.join(l))[0])
    null.sort()
    print('null quantiles 50/90/99 %.2f %.2f %.2f  p=%.2f' % (null[100], null[180], null[198],
          sum(x >= obs[0] for x in null) / len(null)))
