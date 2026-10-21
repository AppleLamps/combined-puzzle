#!/usr/bin/env python3
"""Phrase 3 of the creator's ordered seven is 'lastwordsbeforearchichoice'.
The last words before the Architect Choice are the sentence sitting directly
above this envelope in the phase 3.2 plaintext. Sweep that sentence, in every
plausible normalisation, alone and combined with the phrases either side of it
in the creator's order (yellowblueprimes -> 479, and yinyang)."""
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

S="Raising the stakes without extra chances of winning. A fubcd-king & oracle-queen, thingky mvps, on a sad board but as wide as the first one seen."
PRE="... am I here? Wake up, you... I've designed you a beautiful strategic position. One for one, four for one."
DIG="15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112"
ARCH=Path('/home/user/applelamps/puzle/fresh-start/artifacts/architect_plaintext.txt').read_text().strip()

def forms(s):
    yield s
    yield s.lower()
    yield re.sub(r'[^A-Za-z]','',s).lower()
    yield re.sub(r'[^A-Za-z]','',s).upper()
    yield re.sub(r'[^A-Za-z0-9]','',s).lower()
    yield re.sub(r'\s+','',s)
    yield ' '.join(s.split())

bases=[]
for name,s in [('lastsentence',S),('preamble',PRE),('digits',DIG),
               ('arch-tail-50',ARCH[-50:]),('arch-tail-100',ARCH[-100:]),
               ('ciaobellao','CIAOBELLAO'),
               ('goodluck','GOODLUCKNEVERTHELESSIREALLYHOPEYOURETHEONECIAOBELLAO'),
               ('lastword-seen','seen'),('sent+dig',S+DIG),('dig+sent',DIG+S)]:
    for f in forms(s): bases.append((name,f))

EXTRA=['','479','yinyang','yellowblueprimes','yinyang479','479yinyang',
       'matrixsumlist','lastwordsbeforearchichoice','wewontgiveawaythepassword',
       'itsinfrontofyoureyesbutyourenotseeingit','verylaststepisatruegiveawaypromised']

hits=[];n=0
for name,b in bases:
    for e in EXTRA:
        for cand in ({b+e, e+b} if e else {b}):
            for pwform,pw in (('raw',cand.encode()),('sha256hex',hashlib.sha256(cand.encode()).hexdigest().encode())):
                for dg in ('sha256','md5'):
                    n+=1
                    r=att(pw,dg)
                    if r:
                        hits.append((r[0],name,e,pwform,dg,r[1]))
                        if r[0]>=3: print('!!',r[0],name,e,pwform,dg,r[1][:64])
print(f'{n} decrypts')
from collections import Counter
print('pads:',sorted(Counter(h[0] for h in hits).items()),' expected@1:',round(n/256,1))
