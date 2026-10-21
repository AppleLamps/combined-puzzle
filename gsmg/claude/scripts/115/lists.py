"""Closed family of poster-derived integer lists (the 'matrix sum list' candidates)."""
import os
import numpy as np, itertools
g = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'grid.npy'))

from lists_spiral import spiral

SP = spiral(14)

def matrices():
    """Operand matrices: bit matrix with F as 0/1; colour-valued matrices under number schemes."""
    out = {}
    for fv in (0, 1):
        out[f'bits_F{fv}'] = np.array([[1 if x in 'KB' or (x == 'F' and fv) else 0 for x in row] for row in g])
    schemes = {  # (K, W, B, Y, F)
        'gard': (1, 0, 2, 5, 7),      # gardeners: blue Two, yellow Five, painted Seven
        'gard2': (1, 0, 2, 5, 2),     # F forced blue
        'resist': (0, 9, 6, 4, 9),    # resistor code: black 0, white 9, blue 6, yellow 4
        'consume': (1, 0, 1, 2, 1),   # dbbi consumption
        'onlycol': (0, 0, 1, 2, 1),
        'a1z26': (11, 23, 2, 25, 6),  # k, w, b, y, f
    }
    for name, (K, W, B, Y, F) in schemes.items():
        m = {'K': K, 'W': W, 'B': B, 'Y': Y, 'F': F}
        out['col_' + name] = np.array([[m[x] for x in row] for row in g])
    return out

def ring_of(r, c, n=14): return min(r, c, n - 1 - r, n - 1 - c)

def sum_lists(M):
    n = M.shape[0]; L = {}
    L['rows'] = list(M.sum(1)); L['cols'] = list(M.sum(0))
    L['diag'] = [int(np.trace(M, k)) for k in range(-(n - 1), n)]
    L['adiag'] = [int(np.trace(M[:, ::-1], k)) for k in range(-(n - 1), n)]
    rings = [0] * (n // 2)
    for r in range(n):
        for c in range(n): rings[ring_of(r, c)] += int(M[r, c])
    L['rings'] = rings
    B2 = M.reshape(7, 2, 7, 2).sum(axis=(1, 3))
    L['b2row'] = list(B2.flatten()); L['b2col'] = list(B2.T.flatten())
    L['b2spiral'] = [int(B2[r, c]) for r, c in spiral(7)]
    B7 = M.reshape(2, 7, 2, 7).sum(axis=(1, 3)); L['b7'] = list(B7.flatten())
    L['spiralvals'] = [int(M[r, c]) for r, c in SP]
    L['rowmajor'] = list(M.flatten())
    # prime-indexed rows/cols (1-based primes <=14 and 0-based)
    P1 = [2, 3, 5, 7, 11, 13]
    L['prow1'] = [int(M[p - 1].sum()) for p in P1]; L['pcol1'] = [int(M[:, p - 1].sum()) for p in P1]
    L['prow0'] = [int(M[p].sum()) for p in P1]; L['pcol0'] = [int(M[:, p].sum()) for p in P1]
    L['g257rows'] = [int(M[p - 1].sum()) for p in (2, 5, 7)] + [int(M[:, p - 1].sum()) for p in (2, 5, 7)]
    return {k: [int(x) for x in v] for k, v in L.items()}

def run_lengths(seq):
    out = []; cur = seq[0]; n = 0
    for v in seq:
        if v == cur: n += 1
        else: out.append(n); cur = v; n = 1
    out.append(n); return out

def all_lists():
    res = {}
    for mn, M in matrices().items():
        for ln, lst in sum_lists(M).items():
            res[f'{mn}:{ln}'] = lst
            res[f'{mn}:{ln}:rev'] = lst[::-1]
        bits = [int(M[r, c]) for r, c in SP]
        res[f'{mn}:spiralruns'] = run_lengths(bits)
        res[f'{mn}:rowruns'] = run_lengths(list(M.flatten()))
    res['rabbit_spiral'] = [4, 2, 9, 4, 6, 3, 9]
    res['rabbit_rowmajor'] = [4, 9, 6, 3, 9, 4, 2]
    colpos = [i for i, (r, c) in enumerate(SP) if g[r, c] in 'BYF']
    res['colour_spiralpos'] = colpos
    res['colour_gaps'] = [b - a for a, b in zip([-1] + colpos, colpos)]
    # dedupe
    seen = {}; out = {}
    for k, v in res.items():
        t = tuple(v)
        if t in seen: continue
        seen[t] = k; out[k] = v
    return out

if __name__ == '__main__':
    A = all_lists(); print(len(A))
    for k in list(A)[:12]: print(k, A[k][:20])
