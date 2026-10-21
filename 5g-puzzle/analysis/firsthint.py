#!/usr/bin/env python3
"""firsthintisyourlastcommand -- the one plain-English instruction in the puzzle
nobody has executed.

Take every candidate for "the first hint" from primary sources and use it as the
final password. The literal sitting immediately before it on the page is
`shabefour`; read as "SHA, be four" that is an iteration count, so every
candidate is also tried under SHA-256 applied 1..8 times, in both hex-string and
raw-digest form (openssl takes the password as text, so hex is the puzzle's own
convention -- phase 2 and 3.2 both use sha256 hex as the -k argument).

Target: the two 5-block envelopes. A pad-16 hit is a 32-byte key; 2**-128."""
import base64,hashlib,itertools,re
from pathlib import Path
from Crypto.Cipher import AES

FS=Path('/home/user/applelamps/puzle/fresh-start')
h=FS.joinpath('archives/salphaseion_phase3.html').read_text()
s=re.sub(r'\s','',re.findall(r'<textarea[^>]*>(.*?)</textarea>',h,re.S)[0])
i=s.find('U2FsdGVkX18'); t=s[i:].replace('shabefanstoo','')
m=re.search(r'[ab]{20,}',t)
A=base64.b64decode(t[:m.start()]+t[m.end():])
B=base64.b64decode(re.sub(r'\s','',Path('/tmp/claude-0/final.b64').read_text()))
TGT={'inner':(A[8:16],A[16:]),'terminal':(B[8:16],B[16:])}

def att(pw,salt,ct,dg):
    hf=hashlib.sha256 if dg=='sha256' else hashlib.md5
    d=b'';p=b''
    while len(d)<48: p=hf(p+pw+salt).digest(); d+=p
    b=AES.new(d[:32],AES.MODE_CBC,d[32:48]).decrypt(ct); n=b[-1]
    if not(1<=n<=16) or b[-n:]!=bytes([n])*n: return None
    return n,b[:-n]

# --- every candidate for "the first hint", from primary sources -------------
FIRST=[
 # the poster: the first thing he ever published, and its decode
 'follow the white rabbit','followthewhiterabbit','follow_the_white_rabbit',
 'gsmg.io/theseedisplanted','https://gsmg.io/theseedisplanted','theseedisplanted',
 'gsmg.io','the seed is planted',
 # the rebus on that page -- the phase 1 answer
 'cryptologic warning can you dig it','cryptologicwarningcanyoudigit',
 'cryptologic warning, can you dig it?','can you dig it','canyoudigit',
 'cryptologic warning','cryptologicwarning',
 # the phase 2 gate and its URL
 'causality','choiceisanillusion','choice is an illusion',
 'choiceisanillusioncreatedbetweenthosewithpowerandthosewithout',
 'iwroteitmyself','i wrote it myself',
 # the page's own neighbours
 'enter','shabefour','shabefanstoo','firsthintisyourlastcommand',
 'first hint is your last command','yourlastcommand','lastcommand',
 # the poster marker word and the checkerboard
 'F73D92','f73d92','halfandbetterhalf','half and better half',
 # the seven, in case the "first hint" is phrase 1
 'yellowblueprimes','479',
]
def norms(x):
    yield x
    yield x.lower()
    yield x.upper()
    yield re.sub(r'[^A-Za-z0-9]','',x).lower()
    yield re.sub(r'\s+','',x)

CANDS=sorted({n for f in FIRST for n in norms(f)})

def pwforms(c):
    b=c.encode()
    yield 'raw',b
    d=b
    for k in range(1,9):                    # "sha be four" -- and its neighbours
        d=hashlib.sha256(d).digest()
        yield f'sha{k}-raw',d
        yield f'sha{k}-hex',d.hex().encode()
        yield f'sha{k}-HEX',d.hex().upper().encode()
    # hex-of-text chained the way the puzzle itself does it
    x=c
    for k in range(1,5):
        x=hashlib.sha256(x.encode()).hexdigest()
        yield f'chain{k}',x.encode()

hits=[];n=0
for c in CANDS:
    for form,pw in pwforms(c):
        for tn,(salt,ct) in TGT.items():
            for dg in ('sha256','md5'):
                n+=1
                r=att(pw,salt,ct,dg)
                if r:
                    hits.append((r[0],tn,c,form))
                    if r[0]>=4: print('!!!',r[0],tn,repr(c),form,dg,r[1].hex())
print(f'{len(CANDS)} first-hint candidates, {n} decrypts')
from collections import Counter
print('pads:',sorted(Counter(x[0] for x in hits).items()),'expected@1:',round(n/256,1))
# Deliberately do NOT list pad-1 rows. A wrong key decrypts to 80 random bytes;
# if the last one happens to be 0x01 that is a *valid* PKCS#7 pad of length 1,
# which happens 1 time in 256 and means nothing. Printing those rows makes noise
# look like a shortlist. Only pad >= 4 is worth a human's attention, and only
# pad 16 -- a 64-byte plaintext, one 32-byte key -- is the answer.
top=[h for h in hits if h[0]>=4]
print('rows worth reading (pad>=4):', top if top else 'none')
