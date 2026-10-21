#!/usr/bin/env python3
"""APPROXIMATE rebuild of the remainder pool (msl_rem.txt in doc 115).
The pool actually run held 19,913 strings, built by a one-off snippet that was not kept.
This script rebuilds the part that can be reconstructed: the poster sum lists (pools.py)
reduced mod 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 and 13, in the forms of pools.forms plus the
rule-2 letter form (0 as `o`, 1..9 as a..i), forward and reversed, length <= 400.
Against the archived file this reproduces 14,823 of its 19,913 strings (74%). The rest are
hex-looking strings whose construction is not known (probably the lists read as base-m integers).
"""
import sys
sys.path.insert(0, '.')
from pools import E, matrix_lists, forms

lists = {}
for en, M in E.items():
    for ln, S in matrix_lists(M).items():
        lists[(en, ln)] = S
out = set()
for k, S in lists.items():
    for m in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13):
        R = [s % m for s in S]
        cand = list(forms(R).values())
        if all(0 <= s <= 9 for s in R):
            cand.append(''.join('o' if s == 0 else chr(96 + s) for s in R))
        for s in cand:
            for t in (s, s[::-1]):
                if 0 < len(t) <= 400:
                    out.add(t)
open('msl_rem_approx.txt', 'w').write('\n'.join(sorted(out)) + '\n')
print('msl_rem_approx', len(out))
try:
    have = set(l.rstrip('\n') for l in open('msl_rem.txt') if l.strip())
    print('archived msl_rem', len(have), 'reproduced', len(have & out))
except FileNotFoundError:
    pass
