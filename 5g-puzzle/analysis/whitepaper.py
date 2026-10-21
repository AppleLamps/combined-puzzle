#!/usr/bin/env python3
"""The Bitcoin whitepaper as puzzle material.

Forensics first (see FINDINGS Addendum 27): the file is the canonical paper,
sha256 b1674191a88ec5cdd733e4240a81803105dc412d6c6708d53ab94fc248f4f553 -- the
same bytes embedded in the blockchain. Structurally clean: 23 streams, all
decoding exactly as their dictionaries declare, no embedded files, no JavaScript,
no metadata stream, nothing appended past %%EOF.

So if it is puzzle material it is by its VALUES, not by hidden content. Sweep
them."""
import base64, hashlib, re, time
from pathlib import Path
from Crypto.Cipher import AES
from gate import fullcheck, structure

D = Path('wp.pdf').read_bytes()
SHA, SHA1, MD5 = hashlib.sha256(D).hexdigest(), hashlib.sha1(D).hexdigest(), hashlib.md5(D).hexdigest()

FS = Path('/home/user/applelamps/puzle/fresh-start')
h = FS.joinpath('archives/salphaseion_phase3.html').read_text()
s = re.sub(r'\s','',re.findall(r'<textarea[^>]*>(.*?)</textarea>',h,re.S)[0])
i = s.find('U2FsdGVkX18'); t = s[i:].replace('shabefanstoo','')
m = re.search(r'[ab]{20,}', t)
A = base64.b64decode(t[:m.start()] + t[m.end():])
B = base64.b64decode(re.sub(r'\s','',Path('/tmp/claude-0/final.b64').read_text()))
C = base64.b64decode(re.sub(r'\s','',FS.joinpath('ciphertexts/salphaseion_cosmic.b64').read_text()))
TGT = {'inner':(A[8:16],A[16:]), 'terminal':(B[8:16],B[16:]), 'cosmic':(C[8:16],C[16:])}

def dec(pw, salt, ct, dg):
    hf = hashlib.sha256 if dg=='sha256' else hashlib.md5
    d=b''; p=b''
    while len(d)<48: p=hf(p+pw+salt).digest(); d+=p
    return AES.new(d[:32], AES.MODE_CBC, d[32:48]).decrypt(ct)

BASE = set()
for v in [SHA, SHA.upper(), '0x'+SHA, SHA1, MD5, str(len(D)), '184292', '9',
          'D:20090324113315-06\'00\'', '20090324113315', '20090324', '2009-03-24',
          'OpenOffice.org 2.4', 'Writer',
          'Bitcoin: A Peer-to-Peer Electronic Cash System',
          'bitcoinapeertopeerelectroniccashsystem',
          'A Peer-to-Peer Electronic Cash System', 'Satoshi Nakamoto',
          'satoshinakamoto', 'satoshi', 'nakamoto', 'bitcoin.pdf', 'bitcoin',
          'We define an electronic coin as a chain of digital signatures',
          'proof-of-work', 'proofofwork', 'onecpuonevote', 'one CPU one vote']:
    BASE.add(v)
EXTRA = ['','479','yellowblueprimes','yinyang','matrixsumlist','lastwordsbeforearchichoice',
         'wewontgiveawaythepassword','itsinfrontofyoureyesbutyourenotseeingit',
         'verylaststepisatruegiveawaypromised','causality','enter','halfandbetterhalf','140','1616']
ALL=set(BASE)
for b in BASE:
    for e in EXTRA:
        if e: ALL.add(b+e); ALL.add(e+b)

def pwforms(c):
    b=c.encode('utf-8','ignore')
    yield b; yield hashlib.sha256(b).hexdigest().encode()
    d=b
    for _ in range(4):
        d=hashlib.sha256(d).digest(); yield d; yield d.hex().encode()
# the raw file itself, and its digest bytes, as passwords
RAWPW = [D, bytes.fromhex(SHA), bytes.fromhex(MD5)]

print(f'whitepaper sha256 {SHA}')
print(f'{len(ALL)} candidate strings + {len(RAWPW)} raw-byte passwords\n')
n=0; found=[]; t0=time.time()
for pw in RAWPW:
    for tn,(salt,ct) in TGT.items():
        for dg in ('sha256','md5'):
            blk=dec(pw,salt,ct,dg); n+=1
            hits=fullcheck(blk, f'{tn}/rawbytes/{dg}')
            if hits: found+=hits; [print('***',x,flush=True) for x in hits]
for c in sorted(ALL):
    for pw in pwforms(c):
        for tn,(salt,ct) in TGT.items():
            for dg in ('sha256','md5'):
                blk=dec(pw,salt,ct,dg); n+=1
                hits=fullcheck(blk, f'{tn}/{c[:36]!r}/{dg}')
                if hits: found+=hits; [print('***',x,flush=True) for x in hits]
                st=structure(blk)
                if st: print(f'  structure {st} {tn} {c[:40]!r} {dg}', flush=True)
print(f'\n{len(ALL)} candidates, {n} decrypts, {time.time()-t0:.0f}s')
print(f'prize-key matches: {len(found)}')
