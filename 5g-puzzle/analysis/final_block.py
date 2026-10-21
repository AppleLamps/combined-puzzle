#!/usr/bin/env python3
"""Attack the 80-byte envelope that closes the phase 3.2 plaintext.

Shape argument for why this target is worth a sweep:
  80 ciphertext bytes = 5 AES blocks. A 64-byte plaintext padded with 16 bytes
  of 0x10 is the "half and better half" shape -- two 32-byte secp256k1 keys.
  P(a wrong key producing valid pad 16) = 2**-128, so a pad-16 hit is the answer,
  not a coincidence.  Lower pad values are reported but are noise: P(pad k)=256**-k.
"""
import base64, hashlib, itertools, re, sys
from pathlib import Path
from Crypto.Cipher import AES

BLOB = base64.b64decode(re.sub(r'\s', '', Path('/tmp/claude-0/final.b64').read_text()))
SALT, CT = BLOB[8:16], BLOB[16:]

def evp(pw: bytes, digest: str):
    h = hashlib.sha256 if digest == 'sha256' else hashlib.md5
    d = b''; prev = b''
    while len(d) < 48:
        prev = h(prev + pw + SALT).digest(); d += prev
    return d[:32], d[32:48]

def attempt(pw: bytes, digest: str):
    k, iv = evp(pw, digest)
    body = AES.new(k, AES.MODE_CBC, iv).decrypt(CT)
    p = body[-1]
    if not (1 <= p <= 16) or body[-p:] != bytes([p]) * p:
        return None
    return p, body[:-p]

PHRASES = [l.split('. ', 1)[1].strip()
           for l in Path('/home/user/applelamps/puzle/fresh-start/artifacts/seven_phrases.txt')
           .read_text().splitlines() if l.strip()]

def primes(n):
    out, c = [], 2
    while len(out) < n:
        if all(c % p for p in out if p * p <= c): out.append(c)
        c += 1
    return out
P = primes(400)

def reinsert(base: str, filler: str) -> str:
    """Insert filler chars at prime *positions* -- insert, never replace."""
    out, fi = [], 0
    for i, ch in enumerate(base):
        if i in PSET and fi < len(filler):
            out.append(filler[fi]); fi += 1
        out.append(ch)
    return ''.join(out)
PSET = set(P)

def intertwine(strs):
    """Round-robin character interleave of several strings."""
    return ''.join(c for row in itertools.zip_longest(*strs, fillvalue='')
                   for c in row)

def gen():
    """Yield (label, password-string) candidates."""
    yb = PHRASES[0]                      # yellowblueprimes -- 'the prime basics'
    rest = PHRASES[1:]

    # 0. the phrases themselves, and the plain concatenation
    for i, p in enumerate(PHRASES):
        yield f'phrase{i+1}', p
    yield 'concat-in-order', ''.join(PHRASES)

    # 1. every ordering of all seven, concatenated  (7! = 5040)
    for perm in itertools.permutations(range(7)):
        yield 'perm:' + ''.join(str(i+1) for i in perm), ''.join(PHRASES[i] for i in perm)

    # 2. INTERTWINED: round-robin character interleave, every ordering
    for perm in itertools.permutations(range(7)):
        yield 'twine:' + ''.join(str(i+1) for i in perm), intertwine([PHRASES[i] for i in perm])

    # 3. REINSERT THE PRIME BASICS: yellowblueprimes inserted at prime indices
    #    into each of the other six, into their concatenation, and into every
    #    ordering of the other six.
    for i, p in enumerate(PHRASES):
        yield f'reinsert-into-{i+1}', reinsert(p, yb)
    for perm in itertools.permutations(range(1, 7)):
        base = ''.join(PHRASES[i] for i in perm)
        yield 'reinsert:' + ''.join(str(i+1) for i in perm), reinsert(base, yb)
        yield 'reinsert-twine:' + ''.join(str(i+1) for i in perm), \
              reinsert(intertwine([PHRASES[i] for i in perm]), yb)

    # 4. the prime numbers themselves reinserted, as digits
    digits = ''.join(str(x) for x in P[:24])          # first 24 primes -- the 479 basis
    for i, p in enumerate(PHRASES):
        yield f'primedigits-into-{i+1}', reinsert(p, digits)
    yield 'primedigits-into-concat', reinsert(''.join(PHRASES), digits)

    # 5. prime-derived numbers attached to each phrase and to the concatenation
    for n in (479, 484, 5, 101, 161, 193, 24, 23, 16, 7, 140):
        for i, p in enumerate(PHRASES + [''.join(PHRASES)]):
            yield f'{n}-pre-{i+1}', f'{n}{p}'
            yield f'{n}-post-{i+1}', f'{p}{n}'

    # 6. THE SOURCE CODES: each archived page, with the prime basics reinserted
    arch = Path('/home/user/applelamps/puzle/fresh-start/archives')
    for f in sorted(arch.glob('*.html')):
        src = f.read_text(errors='ignore')
        yield f'src:{f.name}', src
        yield f'src-reinsert:{f.name}', reinsert(src, yb)
        yield f'src-primedigits:{f.name}', reinsert(src, digits)
        # characters standing at prime offsets of the source
        yield f'src-atprimes:{f.name}', ''.join(src[i] for i in P if i < len(src))

def main():
    hits, n = [], 0
    for label, s in gen():
        b = s.encode('utf-8', 'ignore')
        for pwform, pw in (('raw', b), ('sha256hex', hashlib.sha256(b).hexdigest().encode())):
            for digest in ('sha256', 'md5'):
                n += 1
                r = attempt(pw, digest)
                if r:
                    pad, body = r
                    hits.append((pad, label, pwform, digest, body))
                    if pad >= 4:
                        print(f'!! pad={pad:2d} {label} [{pwform}/{digest}] {body[:80]!r}', flush=True)
    print(f'\n{n} decrypts')
    from collections import Counter
    print('pad distribution:', sorted(Counter(h[0] for h in hits).items()))
    print(f'expected at pad 1: {n/256:.0f}  observed: {sum(1 for h in hits if h[0]==1)}')

main()
