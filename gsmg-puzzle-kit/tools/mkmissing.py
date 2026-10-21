#!/usr/bin/env python3
"""Scripted re-derivations of the doc 115 pools that had no script.

The pools run on 29 September were built by one-off snippets that were not kept. This
script builds each one from the written definition in tools/README-tools.md. The sets are
re-derivations, not byte copies: compare sizes against the doc 115 figures in brackets.
Run after setup.py (needs ta.txt, architect.txt, arch_words.txt).

  msl_adj.txt   [5,709]  sum lists of dbbi alone and joined to head/tail slices of faed
  lw_adj.txt    [3,935]  head and tail windows of faed and the dbbi residue
  msl_walk.txt  [411]    the walk numbers in several writings, and the 23 host positions
  lw_walk.txt   [2,116]  Architect windows anchored at the walk numbers
  cards.txt     [13,319] playing-card strings for the New Year dots and the gardeners
  msl_rem_ext.txt        the remainder lists read as base-m integers (the part of
                         msl_rem that mkrem_approx.py does not rebuild, by its own note)
"""
import itertools, sys
sys.path.insert(0, '.')
from pools import E, matrix_lists, forms, isprime

T = open('ta.txt').read().strip()
A = open('architect.txt').read().strip()
dbbi, faed = T[0:91], T[195:765]
assert dbbi.startswith('dbbibfbh') and faed.startswith('faedggee') and len(A) == 1539


def save(name, s, ref=None):
    s = sorted(x for x in s if x)
    open(name, 'w').write('\n'.join(s) + '\n')
    print(name, len(s), '' if ref is None else '(doc 115: %d)' % ref)


# ---- the dbbi parse (dossier 6.3): host positions and residue
PROG = 'BBBBYBBBYYBBBBYBBYYBFYYBY'
pos, k, i, hosts, resid = 1, 0, 0, [], []
while i < len(dbbi):
    if isprime(pos):
        n = 2 if PROG[k] == 'Y' else 1
        hosts.append((pos, i, dbbi[i:i + n])); i += n; k += 1
    else:
        resid.append(dbbi[i]); i += 1
    pos += 1
resid = ''.join(resid)
assert len(hosts) == 23 and pos - 1 == 83 and i == 91, (len(hosts), pos, i)
assert resid == 'difhccgihaeeihggegebgehhehhfafdhffcdbfcccgfeggecdcifffgigeea'
yellow = sum(p for p, _, h in hosts if len(h) == 2)
blue = sum(p for p, _, h in hosts if len(h) == 1)
assert (yellow, blue) == (400, 474)

dig = {c: i + 1 for i, c in enumerate('abcdefghi')}


def vals(s, g=7):
    return [g if c == 'g' else dig[c] for c in s]


# ---- msl_adj: matrixsumlist acting on the text next to it
def grid_lists(v):
    out = {}
    n = len(v)
    for r in range(2, n):
        if n % r == 0 and 2 <= n // r:
            M = [v[j * (n // r):(j + 1) * (n // r)] for j in range(r)]
            try:
                L = matrix_lists(M)
            except IndexError:  # grids under 8 wide: the basic lists only
                R, C = len(M), len(M[0])
                rs = [sum(x) for x in M]; cs = [sum(M[a][b] for a in range(R)) for b in range(C)]
                L = {'rows': rs, 'cols': cs, 'rowscols': rs + cs, 'colsrows': cs + rs,
                     'rows_prime1': [rs[q - 1] for q in range(1, R + 1) if isprime(q)],
                     'cols_prime1': [cs[q - 1] for q in range(1, C + 1) if isprime(q)],
                     'diags': [sum(M[a][a + d] for a in range(R) if 0 <= a + d < C) for d in range(-R + 1, C)]}
            for ln, S in L.items():
                out[(r, ln)] = S
    return out


adj = set()
objs = [('dbbi', dbbi), ('resid', resid)]
for L in (7, 9, 14, 21, 35, 49, 63, 91):
    objs += [('dh%d' % L, dbbi + faed[:L]), ('td%d' % L, faed[-L:] + dbbi),
             ('fh%d' % L, faed[:L]), ('ft%d' % L, faed[-L:])]
for nm, s in objs:
    for g in (7, 0):
        if g == 0 and 'g' not in s: continue
        for key, S in grid_lists(vals(s, g)).items():
            f = forms(S)
            for fn in ('D', 'Dc', 'Ds', 'L1', 'A'):
                if fn in f:
                    for t in (f[fn], f[fn][::-1]):
                        if 0 < len(t) <= 400: adj.add(t)
save('msl_adj.txt', adj, 5709)

# ---- lw_adj: head and tail windows of faed and the residue
lwa = set()
for s in (faed, resid):
    for L in range(3, min(150, len(s)) + 1):
        for w in (s[:L], s[-L:]):
            d7 = ''.join(str(x) for x in vals(w, 7))
            d0 = ''.join(str(x) for x in vals(w, 0))
            for t in (w, d7, d0):
                lwa.update((t, t[::-1]))
            lwa.add(w.encode().hex())
            n = int(d0) if d0.lstrip('0') else 0
            if n: lwa.add('%x' % n)
save('lw_adj.txt', lwa, 3935)

# ---- msl_walk: the walk numbers
WN = [400, 474, 874, 420, 494, 317, 557]
mw = set()
for x in WN:
    for t in (str(x), '%04d' % x, str(x)[::-1], '%x' % x, '%X' % x, bin(x)[2:]):
        mw.add(t)
for r in (2, 3):
    for combo in itertools.permutations([400, 474, 874], r):
        for sep in ('', ',', ' ', '-', '+', '.'):
            mw.add(sep.join(map(str, combo)))
for combo in itertools.permutations([317, 557], 2):
    for sep in ('', ',', ' ', '-', '+', '.'):
        mw.add(sep.join(map(str, combo)))
hp = [p for p, _, _ in hosts]
ho = [o for _, o, _ in hosts]
for L in (hp, ho, [o + 1 for o in ho]):
    for t in (''.join('%02x' % v for v in L), ','.join(map(str, L)), ''.join(map(str, L)),
              ' '.join(map(str, L)), ','.join('%x' % v for v in L)):
        mw.update((t, t[::-1]))
save('msl_walk.txt', mw, 411)

# ---- lw_walk: Architect windows anchored at the walk numbers
lww = set()
for x in WN:
    for o in (x - 1, x, x + 1):
        for k in range(3, 53):
            if 0 <= o - k and o <= len(A): lww.add(A[o - k:o])
            if 0 <= o and o + k <= len(A): lww.add(A[o:o + k])
save('lw_walk.txt', lww, 2116)

# ---- cards
words = {1: ['ace', 'one'], 2: ['two'], 3: ['three'], 4: ['four'], 5: ['five'], 7: ['seven']}
seqs = set()
r5 = [1, 2, 3, 4, 5]
for a in range(5):
    for b in range(a + 1, 5):
        seqs.add(tuple(r5[a:b + 1])); seqs.add(tuple(r5[a:b + 1][::-1]))
for r in (1, 2, 3):
    for p in itertools.permutations([2, 5, 7], r): seqs.add(p)
suits = ['club', 'diamond', 'heart', 'spade']
suits += [s + 's' for s in suits]
cards = set()
for sq in seqs:
    for asword in (False, True):
        for acename in (['ace', 'one'] if 1 in sq and asword else [None]):
            def rank(v):
                if not asword: return str(v)
                return acename if v == 1 else words[v][0]
            ranks = [rank(v) for v in sq]
            for sep in ('', ' ', ',', '_', '-'):
                cards.add(sep.join(ranks))
                for st in suits:
                    for of in ('', 'of'):
                        j = (sep + of + sep) if of else sep
                        cards.add(sep.join(ranks) + j + st)
                        cards.add(sep.join(r + j + st for r in ranks))
save('cards.txt', cards, 13319)

# ---- msl_rem extension: remainder lists read as base-m integers
ext = set()
for en, M in E.items():
    for ln, S in matrix_lists(M).items():
        for m in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13):
            R = [s % m for s in S]
            for RR in (R, R[::-1]):
                n = 0
                for v in RR: n = n * m + v
                if n:
                    for t in ('%x' % n, str(n)):
                        if len(t) <= 400: ext.add(t)
save('msl_rem_ext.txt', ext)
