"""Do poster sum lists, read as gaps or positions, land on one marker letter in a textarea block?
Analogue of the dbbi test (23/23 hosts start with b). Scored by binomial tail; nulled by shuffles."""
import math, os, random, sys, collections
from lists import all_lists

soup = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'soup.txt')).read()
BLOCKS = {'faed': soup[195:765], 'dbbi': soup[:91], 'dbbi+faed': soup[:91] + soup[195:765],
          'residue': 'difhccgihaeeihggegebgehhehhfafdhffcdbfcccgfeggecdcifffgigeea'}

LISTS = all_lists()

def lbinom_tail(k, n, p):
    # log10 P(X>=k), X~Bin(n,p)
    s = 0.0
    for j in range(k, n + 1):
        s += math.comb(n, j) * p ** j * (1 - p) ** (n - j)
    return math.log10(max(s, 1e-300))

def configs():
    for name, lst in LISTS.items():
        if len(lst) < 5: continue
        for a in (1, 2, 3):
            for b in range(0, 8):
                gaps = [a * v + b for v in lst]
                if min(gaps) < 1: continue
                yield f'{name}|gap={a}v+{b}', gaps, 'gap'
        if sorted(lst) == lst and len(set(lst)) == len(lst):
            yield f'{name}|pos', lst, 'pos'

CFG = list(configs())

def scan(s, starts=range(0, 25), keep=5):
    freq = collections.Counter(s); n = len(s)
    best = []
    for name, seq, kind in CFG:
        for st in starts:
            if kind == 'gap':
                pos = []; p = st
                for gp in seq:
                    if p >= n: break
                    pos.append(p); p += gp
            else:
                pos = [st + v for v in seq if st + v < n]
            if len(pos) < 5: continue
            cnt = collections.Counter(s[i] for i in pos)
            ch, h = cnt.most_common(1)[0]
            if h < 4: continue
            lp = lbinom_tail(h, len(pos), freq[ch] / n)
            best.append((lp, name, st, ch, h, len(pos)))
    best.sort()
    return best[:keep]

def planted_control(seed=3):
    """faed-like filler (faed's non-g letters plus 55 g, drawn with replacement) with g
    markers written at gaps 2v+1 of the bit grid's row sums, from position 11."""
    faed = BLOCKS['faed']; r = random.Random(seed)
    alph = [c for c in faed if c != 'g'] + ['g'] * 55
    s = [r.choice(alph) for _ in range(570)]
    p = 11
    for v in LISTS['bits_F0:rows']:
        if p < 570: s[p] = 'g'; p += 2 * v + 1
    return ''.join(s)

if __name__ == '__main__':
    print('configs', len(CFG))
    ctl = scan(planted_control(), keep=2)
    print('== planted control (bits_F0:rows|gap=2v+1 from 11):')
    for row in ctl: print('   ', row)
    for bn, s in BLOCKS.items():
        obs = scan(s)
        r = random.Random(7); nulls = []
        for _ in range(int(sys.argv[1]) if len(sys.argv) > 1 else 30):
            l = list(s); r.shuffle(l); nulls.append(scan(''.join(l), keep=1)[0][0])
        nulls.sort()
        p = sum(x <= obs[0][0] for x in nulls) / len(nulls)
        print(f'== {bn}: best log10P {obs[0][0]:.2f}  null median {nulls[len(nulls)//2]:.2f} min {nulls[0]:.2f}  empirical p={p:.2f}')
        for row in obs: print('   ', row)
