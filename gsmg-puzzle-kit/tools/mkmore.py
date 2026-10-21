#!/usr/bin/env python3
"""Pools that mkpools.py does not build. Run after setup.py and seg.py.

lw_words.txt   the last 1 to 20 words of the Architect text at every word boundary
               (arch_words.txt from seg.py; 334 words), joined with no spaces. 6,341 strings.
subs.txt       every substring of length 4 to 120 of the textarea (forward and reversed) in
               letter form, plus the digit form (a..i = 1..9, o = 0) of each substring made only
               of the letters a..i and o; plus the ascii-hex, ascii-binary, ascii-decimal,
               a1z26 and reversed a1z26 forms of the six label words. 404,796 strings.
"""
T = open('ta.txt').read().strip()
aw = open('arch_words.txt').read().split()
out = set()
for i in range(1, len(aw) + 1):
    for k in range(1, 21):
        if i - k >= 0:
            out.add(''.join(aw[i - k:i]))
open('lw_words.txt', 'w').write('\n'.join(sorted(out)) + '\n')
print('lw_words', len(out))

dm = {c: str(i + 1) for i, c in enumerate('abcdefghi')}
dm['o'] = '0'
allowed = set('abcdefghio')
subs = set()
for base in (T, T[::-1]):
    n = len(base)
    for L in range(4, 121):
        for i in range(n - L + 1):
            s = base[i:i + L]
            subs.add(s)
            if set(s) <= allowed:
                subs.add(''.join(dm[c] for c in s))
labels = ['enter', 'matrixsumlist', 'thispassword', 'yellowblueprimes', 'lastwordsbeforearchichoice', 'yinyang']
for wd in labels:
    b = wd.encode()
    a1 = ''.join(str(ord(c) - 96) for c in wd)
    subs.update([b.hex(), ''.join(format(x, '08b') for x in b), ''.join(str(x) for x in b), a1, a1[::-1]])
open('subs.txt', 'w').write('\n'.join(sorted(subs)) + '\n')
print('subs', len(subs))
