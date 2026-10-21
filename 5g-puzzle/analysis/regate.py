#!/usr/bin/env python3
"""Re-run every candidate set from this session through the on-chain gate.

No pad filter, no printability filter. Each decrypt's full 80 bytes get every
32-byte window derived and checked against the two prize hash160s and Half's
known uncompressed public key. Structural signals (EBCDIC, magic, high
printability) are reported alongside but never used to reject anything.
"""
import base64, hashlib, itertools, re, sys, time
from pathlib import Path
from Crypto.Cipher import AES
from gate import fullcheck, structure

FS = Path('/home/user/applelamps/puzle/fresh-start')
h = FS.joinpath('archives/salphaseion_phase3.html').read_text()
s = re.sub(r'\s', '', re.findall(r'<textarea[^>]*>(.*?)</textarea>', h, re.S)[0])
i = s.find('U2FsdGVkX18'); t = s[i:].replace('shabefanstoo', '')
m = re.search(r'[ab]{20,}', t)
A = base64.b64decode(t[:m.start()] + t[m.end():])
B = base64.b64decode(re.sub(r'\s', '', Path('/tmp/claude-0/final.b64').read_text()))
TGT = {'inner': (A[8:16], A[16:]), 'terminal': (B[8:16], B[16:])}

def dec(pw, salt, ct, dg):
    hf = hashlib.sha256 if dg == 'sha256' else hashlib.md5
    d = b''; p = b''
    while len(d) < 48: p = hf(p + pw + salt).digest(); d += p
    return AES.new(d[:32], AES.MODE_CBC, d[32:48]).decrypt(ct)

# ---- every candidate string this session generated -------------------------
PH = [l.split('. ',1)[1].strip() for l in
      FS.joinpath('artifacts/seven_phrases.txt').read_text().splitlines() if l.strip()]
def primes(n):
    o, c = [], 2
    while len(o) < n:
        if all(c % p for p in o if p*p <= c): o.append(c)
        c += 1
    return o
P = primes(400); PSET = set(P)
def reinsert(base, filler):
    out, fi = [], 0
    for idx, ch in enumerate(base):
        if idx in PSET and fi < len(filler): out.append(filler[fi]); fi += 1
        out.append(ch)
    return ''.join(out)
def twine(strs):
    return ''.join(c for row in itertools.zip_longest(*strs, fillvalue='') for c in row)

def candidates():
    yb = PH[0]; digits = ''.join(str(x) for x in P[:24])
    for p in PH: yield p
    yield ''.join(PH)
    for perm in itertools.permutations(range(7)):
        yield ''.join(PH[i] for i in perm)
        yield twine([PH[i] for i in perm])
    for p in PH:
        yield reinsert(p, yb); yield reinsert(p, digits)
    for perm in itertools.permutations(range(1,7)):
        base = ''.join(PH[i] for i in perm)
        yield reinsert(base, yb)
        yield reinsert(twine([PH[i] for i in perm]), yb)
    for n in (479,484,5,101,161,193,24,23,16,7,140,163,20,74):
        for p in PH + [''.join(PH)]:
            yield f'{n}{p}'; yield f'{p}{n}'
    for f in sorted(FS.joinpath('archives').glob('*.html')):
        src = f.read_text(errors='ignore')
        yield src; yield reinsert(src, yb); yield reinsert(src, digits)
        yield ''.join(src[i] for i in P if i < len(src))
    for x in ['Raising the stakes without extra chances of winning. A fubcd-king & oracle-queen, '
              'thingky mvps, on a sad board but as wide as the first one seen.',
              'follow the white rabbit','followthewhiterabbit','gsmg.io/theseedisplanted',
              'theseedisplanted','cryptologicwarningcanyoudigit','causality','enter',
              'shabefour','shabefanstoo','firsthintisyourlastcommand','halfandbetterhalf',
              'f73d92','F73D92','479','163','fefefe','gsmg.io/theseedispla~ted',
              '61087665499787981081087367596 68','yinyang','yingyang']:
        yield x; yield x.lower(); yield re.sub(r'[^A-Za-z0-9]','',x).lower()

def pwforms(c):
    b = c.encode('utf-8','ignore')
    yield b
    yield hashlib.sha256(b).hexdigest().encode()
    d = b
    for _ in range(8):
        d = hashlib.sha256(d).digest()
        yield d; yield d.hex().encode(); yield d.hex().upper().encode()

seen = set(); n = 0; t0 = time.time(); found = []
for c in candidates():
    if c in seen: continue
    seen.add(c)
    for pw in pwforms(c):
        for tn, (salt, ct) in TGT.items():
            for dg in ('sha256','md5'):
                blk = dec(pw, salt, ct, dg)
                n += 1
                hits = fullcheck(blk, f'{tn}/{c[:30]!r}/{dg}')
                if hits:
                    found += hits
                    for x in hits: print('*** ', x, flush=True)
                st = structure(blk)
                if st:
                    print(f'  structure {st} {tn} {c[:40]!r} {dg}', flush=True)
    if n % 20000 < 100:
        print(f'  … {n} decrypts, {len(seen)} candidates, {time.time()-t0:.0f}s', flush=True)
print(f'\n{len(seen)} candidates, {n} decrypts, {time.time()-t0:.0f}s')
print(f'prize-key matches: {len(found)}')
