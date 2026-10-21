#!/usr/bin/env python3
"""Two hints he restated for years point at the same cell from opposite sides:

  2020-01-14  "Go back to the first puzzle piece ... the rabbits nest may contain
               a whole lot more."
  2021-12-25  "prime numbers ... required to proceed. Furthermore, along the way,
               some characters need to be 'zeroed out'."

The poster's one anomaly, #fefefe at cell (7,4), sits at spiral index 163 -- a
prime -- marking byte 20, bit 3 of the single string the poster encodes. So:
enumerate every way to "zero out" a character or bit of that string, alone and
under prime-indexed selection, and put the results through the on-chain gate.
"""
import base64, hashlib, itertools, re, time
from pathlib import Path
from Crypto.Cipher import AES
from gate import fullcheck, structure

BITS = ('0110011101110011011011010110011100101110011010010110111100101111'
        '0111010001101000011001010111001101100101011001010110010001101001'
        '0111001101110000011011000110000101101110011101000110010101100100'
        '0000')
URL = 'gsmg.io/theseedisplanted'
IDX = 163

FS = Path('/home/user/applelamps/puzle/fresh-start')
h = FS.joinpath('archives/salphaseion_phase3.html').read_text()
s = re.sub(r'\s','',re.findall(r'<textarea[^>]*>(.*?)</textarea>',h,re.S)[0])
i = s.find('U2FsdGVkX18'); t = s[i:].replace('shabefanstoo','')
m = re.search(r'[ab]{20,}', t)
A = base64.b64decode(t[:m.start()] + t[m.end():])
B = base64.b64decode(re.sub(r'\s','',Path('/tmp/claude-0/final.b64').read_text()))
C = base64.b64decode(re.sub(r'\s','',FS.joinpath('ciphertexts/salphaseion_cosmic.b64').read_text()))
# Cosmic Duality is 83 blocks -- 1,297 windows per decrypt against the twins' 49,
# so it dominates runtime by 16x. Gate the two shaped targets here; cosmic separately.
TGT = {'inner':(A[8:16],A[16:]), 'terminal':(B[8:16],B[16:])}

def dec(pw, salt, ct, dg):
    hf = hashlib.sha256 if dg=='sha256' else hashlib.md5
    d=b''; p=b''
    while len(d)<48: p=hf(p+pw+salt).digest(); d+=p
    return AES.new(d[:32], AES.MODE_CBC, d[32:48]).decrypt(ct)

def primes_below(n):
    o=[]; c=2
    while c<n:
        if all(c%q for q in o if q*q<=c): o.append(c)
        c+=1
    return o
PB196 = set(primes_below(196)); PB24 = set(primes_below(24))
def tostr(b): return ''.join(chr(int(b[i:i+8],2)) for i in range(0, len(b)//8*8, 8))

def cands():
    yield URL; yield BITS; yield tostr(BITS)
    # every single-character zeroing of the string, three senses of "zero"
    for i in range(len(URL)):
        yield URL[:i]+URL[i+1:]
        yield URL[:i]+'0'+URL[i+1:]
        yield URL[:i]+'o'+URL[i+1:]
        yield URL[:i]+'\x00'+URL[i+1:]
    # every single-bit zeroing / flip / deletion of the 196-bit field
    for i in range(196):
        for v in (BITS[:i]+'0'+BITS[i+1:], BITS[:i]+'1'+BITS[i+1:], BITS[:i]+BITS[i+1:]):
            yield v; yield tostr(v)
    # the marked position specifically, and its byte
    for v in (BITS[:IDX]+'1'+BITS[IDX+1:], BITS[:IDX]+BITS[IDX+1:],
              BITS[:160]+BITS[168:], BITS[IDX:], BITS[:IDX]):
        yield v; yield tostr(v)
    # prime-indexed selection, both senses, at bit and character level
    for keep in (False, True):
        b=''.join(('0' if (i in PB196)==keep else ch) for i,ch in enumerate(BITS))
        yield b; yield tostr(b)
        d=''.join(ch for i,ch in enumerate(BITS) if (i in PB196)!=keep)
        yield d; yield tostr(d)
        u=''.join(c for i,c in enumerate(URL) if (i in PB24)!=keep)
        yield u
        yield ''.join(('0' if (i in PB24)==keep else c) for i,c in enumerate(URL))
    # the markers and the residual
    yield 'F73D92'; yield 'f73d92'; yield '111101110011110110010010'
    yield '000010001100001001101101'; yield '08C26D'; yield '0000'
    for x in ('gsmg.io/theseedisplated','gsmg.io/theseedispla~ted',
              'gsmg.io/theseedispla0ted','gsmg.io/theseedisplaoted'):
        yield x

BASE = sorted({c for c in cands() if c})
EXTRA = ['','479','163','yellowblueprimes','yinyang','matrixsumlist',
         'lastwordsbeforearchichoice','wewontgiveawaythepassword',
         'itsinfrontofyoureyesbutyourenotseeingit',
         'verylaststepisatruegiveawaypromised','causality','enter']
ALL = set(BASE)
for b in BASE:
    for e in EXTRA:
        if e: ALL.add(b+e); ALL.add(e+b)

def pwforms(c):
    b=c.encode('utf-8','ignore')
    yield b; yield hashlib.sha256(b).hexdigest().encode()
    d=b
    for _ in range(4):
        d=hashlib.sha256(d).digest()
        yield d; yield d.hex().encode()

n=0; t0=time.time(); found=[]
print(f'{len(ALL)} candidate strings', flush=True)
for c in sorted(ALL):
    for pw in pwforms(c):
        for tn,(salt,ct) in TGT.items():
            for dg in ('sha256','md5'):
                blk = dec(pw, salt, ct, dg); n += 1
                hits = fullcheck(blk, f'{tn}/{c[:40]!r}/{dg}')
                if hits:
                    found += hits
                    for x in hits: print('***', x, flush=True)
                st = structure(blk)
                if st: print(f'  structure {st} {tn} {c[:50]!r} {dg}', flush=True)
    if n % 100000 < 200: print(f'  … {n} decrypts {time.time()-t0:.0f}s', flush=True)
print(f'\n{len(ALL)} candidates, {n} decrypts, {time.time()-t0:.0f}s')
print(f'prize-key matches: {len(found)}')
