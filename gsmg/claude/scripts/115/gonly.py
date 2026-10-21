"""Doc 115 s3: the gap/position scan restricted to landings on `g` in faed, with the
planted control from gapwalk.py and a seeded shuffle null."""
import random
import gapwalk as G

def scan_g(s, ch='g', starts=range(0, 25)):
    n = len(s); pch = s.count(ch) / n; best = (0, None)
    for name, seq, kind in G.CFG:
        for st in starts:
            if kind == 'gap':
                pos = []; p = st
                for gp in seq:
                    if p >= n: break
                    pos.append(p); p += gp
            else:
                pos = [st + v for v in seq if st + v < n]
            if len(pos) < 5: continue
            h = sum(s[i] == ch for i in pos)
            lp = G.lbinom_tail(h, len(pos), pch)
            if lp < best[0]: best = (lp, (name, st, h, len(pos)))
    return best

if __name__ == '__main__':
    print('planted control, g-only best', scan_g(G.planted_control()))
    faed = G.BLOCKS['faed']
    obs = scan_g(faed); print('faed g-only best', obs)
    r = random.Random(11); nl = []
    for _ in range(40):
        l = list(faed); r.shuffle(l); nl.append(scan_g(''.join(l))[0])
    nl.sort()
    print('null median %.2f min %.2f p=%.2f' % (nl[20], nl[0], sum(x <= obs[0] for x in nl) / len(nl)))
