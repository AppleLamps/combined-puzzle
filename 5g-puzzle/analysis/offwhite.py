#!/usr/bin/env python3
"""One cell of the 196 in the poster is #FEFEFE, not #FFFFFF: row 7, column 4,
all 625 of its pixels, perfectly cell-aligned, in an RGBA image with no palette
and a uniform alpha. Five colours where the decode only ever uses four.

It is invisible on screen and invisible to the grid reader, which majority-samples
each cell and buckets it as white. Phrase 6 of the creator's ordered seven is
`itsinfrontofyoureyesbutyourenotseeingit`.

Establish what it indexes, then use it."""
import base64,hashlib,re
from pathlib import Path
from Crypto.Cipher import AES
import sys
sys.path.insert(0,'/home/user/applelamps/puzle/fresh-start/tools')
from poster_spiral import spiral, SIZE, ONE_BITS
from png import read_rgb
from _paths import IMAGES

CELL=25
_,_,rows=read_rgb(IMAGES/'poster'/'follow_the_white_rabbit.png')
grid=[[rows[r*CELL+12][c*CELL+12] for c in range(SIZE)] for r in range(SIZE)]
order=spiral(SIZE)
RC=(7,4); IDX=order.index(RC)
bits=''.join('1' if grid[r][c] in ONE_BITS else '0' for r,c in order)
msg=''.join(chr(int(bits[i:i+8],2)) for i in range(0,192,8))
flip=bits[:IDX]+('1' if bits[IDX]=='0' else '0')+bits[IDX+1:]
fmsg=''.join(chr(int(flip[i:i+8],2)) for i in range(0,192,8))
print(f'cell {RC}  spiral index {IDX}  byte {IDX//8} bit {IDX%8}')
print(f'  as read : {msg}')
print(f'  bit flip: {fmsg}')
print(f'  char {IDX//8}: {msg[IDX//8]!r} -> {fmsg[IDX//8]!r}')
print(f'  163 prime? {all(163%k for k in range(2,13))}   marker indices are 7,15..191; 163 is {"" if (IDX-7)%8==0 else "not "}one')

FS=Path('/home/user/applelamps/puzle/fresh-start')
h=FS.joinpath('archives/salphaseion_phase3.html').read_text()
s=re.sub(r'\s','',re.findall(r'<textarea[^>]*>(.*?)</textarea>',h,re.S)[0])
i=s.find('U2FsdGVkX18'); t=s[i:].replace('shabefanstoo','')
m=re.search(r'[ab]{20,}',t)
A=base64.b64decode(t[:m.start()]+t[m.end():])
B=base64.b64decode(re.sub(r'\s','',Path('/tmp/claude-0/final.b64').read_text()))
C=base64.b64decode(re.sub(r'\s','',FS.joinpath('ciphertexts/salphaseion_cosmic.b64').read_text()))
TGT={'inner':(A[8:16],A[16:]),'terminal':(B[8:16],B[16:]),'cosmic':(C[8:16],C[16:])}
def att(pw,salt,ct,dg):
    hf=hashlib.sha256 if dg=='sha256' else hashlib.md5
    d=b'';p=b''
    while len(d)<48: p=hf(p+pw+salt).digest(); d+=p
    b=AES.new(d[:32],AES.MODE_CBC,d[32:48]).decrypt(ct); n=b[-1]
    if not(1<=n<=16) or b[-n:]!=bytes([n])*n: return None
    return n,b[:-n]

V=['163','20','74','47','7,4','74','85','fefefe','FEFEFE','254','0xfe','fe',
   msg,fmsg,msg[IDX//8],fmsg[IDX//8],bits,flip,
   'gsmg.io/theseedispla~ted','itsinfrontofyoureyesbutyourenotseeingit']
EX=['','479','yellowblueprimes','yinyang','itsinfrontofyoureyesbutyourenotseeingit',
    'wewontgiveawaythepassword','verylaststepisatruegiveawaypromised',
    'enter','firsthintisyourlastcommand','halfandbetterhalf']
cands={v for v in V}
for v in V:
    for e in EX:
        if e: cands|={v+e, e+v}
hits=[];n=0
for c in sorted(cands):
    for pw in (c.encode(), hashlib.sha256(c.encode()).hexdigest().encode(), hashlib.sha256(c.encode()).digest()):
        for tn,(salt,ct) in TGT.items():
            for dg in ('sha256','md5'):
                n+=1
                r=att(pw,salt,ct,dg)
                if r:
                    hits.append((r[0],tn,c))
                    if r[0]>=4: print('!!!',r[0],tn,repr(c[:60]),dg,r[1].hex())
print(f'\n{len(cands)} candidates, {n} decrypts')
from collections import Counter
print('pads:',sorted(Counter(x[0] for x in hits).items()),'expected@1:',round(n/256,1))
