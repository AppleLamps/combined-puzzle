#!/usr/bin/env python3
"""Candidate second-door URLs, built strictly from what the creator specified.

  "Go back to the first puzzle piece ... it might have shown you only ONE door,
   beware that the rabbits nest may contain a whole lot more."          2020-01-14
  "prime numbers ... definitely an aspect which is required to proceed.
   Furthermore, along the way, some characters need to be 'zeroed out'." 2021-12-26

The first puzzle piece encodes exactly one string. If a second door exists as a
page, it is that string transformed -- and the two named operations are PRIMES and
ZEROING. So enumerate the string under every combination of those two, with no
invented steps, and keep only results that are valid URL paths.

The resulting list is checkable against the Wayback CDX index for gsmg.io (414
unique captured URLs), which this environment cannot reach.
"""
import re
URL  = 'gsmg.io/theseedisplanted'
PATH = 'theseedisplanted'
FEFEFE_CHAR = 20          # #fefefe marks byte 20 of the 192-bit payload
def primes_below(n):
    o=[]; c=2
    while c<n:
        if all(c%q for q in o if q*q<=c): o.append(c)
        c+=1
    return o

cands = {}
def add(v, why):
    v = v.strip('/')
    if v and re.fullmatch(r'[A-Za-z0-9._~-]+', v):
        cands.setdefault(v, why)

for base, bn in ((PATH,'path'), (URL,'full')):
    P = set(primes_below(len(base)))
    # zeroing sense 1: delete the character
    add(''.join(c for i,c in enumerate(base) if i not in P), f'{bn}: delete prime-index chars')
    add(''.join(c for i,c in enumerate(base) if i in P),     f'{bn}: keep only prime-index chars')
    # 1-indexed, since "characters" are usually counted from 1
    P1 = set(p-1 for p in primes_below(len(base)+1))
    add(''.join(c for i,c in enumerate(base) if i not in P1), f'{bn}: delete prime-index chars (1-indexed)')
    add(''.join(c for i,c in enumerate(base) if i in P1),     f'{bn}: keep only prime-index chars (1-indexed)')
    # zeroing sense 2: replace with '0', and with 'o' (the puzzle's own o=0)
    for ch, nm in (('0','digit zero'), ('o','letter o = 0 in the puzzle encoding')):
        add(''.join(ch if i in P else c for i,c in enumerate(base)), f'{bn}: prime-index -> {nm}')
        add(''.join(ch if i in P1 else c for i,c in enumerate(base)), f'{bn}: prime-index -> {nm} (1-indexed)')
    # the single marked character
    if len(base) > FEFEFE_CHAR:
        k = FEFEFE_CHAR if bn=='full' else FEFEFE_CHAR-8
        if 0 <= k < len(base):
            add(base[:k]+base[k+1:], f'{bn}: delete the #fefefe-marked character')
            add(base[:k]+'0'+base[k+1:], f'{bn}: #fefefe char -> 0')
            add(base[:k]+'o'+base[k+1:], f'{bn}: #fefefe char -> o')
    # every single-character deletion, as the exhaustive superset
    for i in range(len(base)):
        add(base[:i]+base[i+1:], f'{bn}: delete char {i} ({base[i]!r})')
    # remove all instances of a zero-ish character
    for ch in 'o0':
        add(base.replace(ch,''), f'{bn}: remove every {ch!r}')

print(f"{len(cands)} candidate paths\n")
for v,w in sorted(cands.items()):
    print(f"  https://gsmg.io/{v:26s}  {w}")
