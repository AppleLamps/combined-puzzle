#!/usr/bin/env python3
"""The creator's seven phrases are ordered. Treat them as a pipeline and feed
each step's actual derived value into the 80-byte terminal envelope.

  1 yellowblueprimes  -> 479          (24 markers on the first 24 primes, balanced)
  2 matrixsumlist     -> the poster's row and column sums (derived below)
  3 lastwordsbeforearchichoice -> the sentence directly above this envelope
  4 yinyang           -> unknown; the creator calls this the gate
"""
import base64,hashlib,itertools,re
from pathlib import Path
from Crypto.Cipher import AES
B=base64.b64decode(re.sub(r'\s','',Path('/tmp/claude-0/final.b64').read_text()))
SALT,CT=B[8:16],B[16:]
def evp(pw,dg):
    h=hashlib.sha256 if dg=='sha256' else hashlib.md5
    d=b'';p=b''
    while len(d)<48: p=h(p+pw+SALT).digest(); d+=p
    return d[:32],d[32:48]
def att(pw,dg):
    k,iv=evp(pw,dg); b=AES.new(k,AES.MODE_CBC,iv).decrypt(CT); n=b[-1]
    if not(1<=n<=16) or b[-n:]!=bytes([n])*n: return None
    return n,b[:-n]

RS=[6,10,8,7,6,6,5,4,9,9,7,8,7,9]
CS=[8,10,8,10,8,7,3,6,7,5,9,6,6,8]
def joins(xs):
    return {''.join(map(str,xs)), '-'.join(map(str,xs)), ','.join(map(str,xs)),
            ' '.join(map(str,xs)), str(sum(xs))}
M=set()
for xs in (RS,CS,RS+CS,CS+RS,sorted(RS),sorted(CS),RS[::-1],CS[::-1]):
    M|=joins(xs)
M|={''.join(map(str,a))+''.join(map(str,b)) for a,b in ((RS,CS),(CS,RS))}
M|={'101','479','484'}
LAST="Raising the stakes without extra chances of winning. A fubcd-king & oracle-queen, thingky mvps, on a sad board but as wide as the first one seen."
L={LAST, LAST.lower(), re.sub(r'[^A-Za-z]','',LAST).lower(), re.sub(r'\s+','',LAST)}
PH=['yellowblueprimes','matrixsumlist','lastwordsbeforearchichoice','yinyang',
    'wewontgiveawaythepassword','itsinfrontofyoureyesbutyourenotseeingit',
    'verylaststepisatruegiveawaypromised']
P1={'479'}
P4={'yinyang','yingyang','yinandyang','','halfandbetterhalf'}

cands=set()
for m in M:
    cands.add(m)
    for a in P1:
        cands|={a+m, m+a}
        for l in L:
            for y in P4:
                cands.add(a+m+l+y); cands.add(a+m+y); cands.add(m+l+y)
for m in M:
    for ph in PH: cands|={ph+m, m+ph}
for l in L:
    for y in P4: cands|={l+y, y+l}
cands|=set(PH)

hits=[];n=0
for c in sorted(cands):
    for pwform,pw in (('raw',c.encode()),('hex',hashlib.sha256(c.encode()).hexdigest().encode())):
        for dg in ('sha256','md5'):
            n+=1
            r=att(pw,dg)
            if r:
                hits.append((r[0],c))
                if r[0]>=3: print('!!',r[0],repr(c[:70]),pwform,dg,r[1][:64])
print(f'{len(cands)} candidates, {n} decrypts')
from collections import Counter
print('pads:',sorted(Counter(h[0] for h in hits).items()),'expected@1:',round(n/256,1))
