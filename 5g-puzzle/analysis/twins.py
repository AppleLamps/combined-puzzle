#!/usr/bin/env python3
"""Two envelopes of identical shape -- 96 raw bytes, 80 ciphertext bytes, 5 AES
blocks -- sit at the two ends of the unsolved region:

  A  inside the SalPhaseIon letter stream, split in half by the word "enter"
     written in binary                                   salt 3ab585348552415d
  B  closing the phase 3.2 plaintext                     salt b45a5e3d827593ca

64 bytes of plaintext -- one 32-byte secp256k1 key each -- pads with 16 bytes of
0x10. "The private keys belong to half and better half." A pad-16 hit on either
is self-proving at 2**-128; nothing else here is worth reporting.

Sweep both with everything the SalPhaseIon page states in plain text, the seven
ordered phrases, and the derived pipeline values."""
import base64,hashlib,itertools,re
from pathlib import Path
from Crypto.Cipher import AES

FS=Path('/home/user/applelamps/puzle/fresh-start')
h=FS.joinpath('archives/salphaseion_phase3.html').read_text()
s=re.sub(r'\s','',re.findall(r'<textarea[^>]*>(.*?)</textarea>',h,re.S)[0])
i=s.find('U2FsdGVkX18'); tail=s[i:].replace('shabefanstoo','')
m=re.search(r'[ab]{20,}',tail)
A=base64.b64decode(tail[:m.start()]+tail[m.end():])
B=base64.b64decode(re.sub(r'\s','',Path('/tmp/claude-0/final.b64').read_text()))
TARGETS={'salphaseion-inner':(A[8:16],A[16:]),'phase32-terminal':(B[8:16],B[16:])}

def att(pw,salt,ct,dg):
    hf=hashlib.sha256 if dg=='sha256' else hashlib.md5
    d=b'';p=b''
    while len(d)<48: p=hf(p+pw+salt).digest(); d+=p
    b=AES.new(d[:32],AES.MODE_CBC,d[32:48]).decrypt(ct); n=b[-1]
    if not(1<=n<=16) or b[-n:]!=bytes([n])*n: return None
    return n,b[:-n]

PH=[l.split('. ',1)[1].strip() for l in FS.joinpath('artifacts/seven_phrases.txt').read_text().splitlines() if l.strip()]
PAGE=['enter','shabefour','shabefanstoo','firsthintisyourlastcommand',
      'shabefourfirsthintisyourlastcommand','yourlastcommand','firsthint',
      'followthewhiterabbit','gsmg.io/theseedisplanted','theseedisplanted',
      'causality','salphaseion','cosmicduality','halfandbetterhalf',
      'thepvivatekeysbelongtohalfandbetterhalf']
NUM=['479','101','140','1075','F73D92','f73d92']
S91='dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe'
D=lambda t:''.join('0' if c=='o' else str('abcdefghi'.index(c)+1) for c in t)

base=set(PH)|set(PAGE)|set(NUM)|{S91,D(S91)}
cands=set(base)
for a in base:
    for b in base:
        if a!=b: cands.add(a+b)
for p in itertools.permutations(PH):            # the ordered seven, every order
    cands.add(''.join(p))
for x in base:                                   # each, hashed once more
    cands.add(hashlib.sha256(x.encode()).hexdigest())

hits=[];n=0
for c in cands:
    for pw in (c.encode(), hashlib.sha256(c.encode()).hexdigest().encode()):
        for tname,(salt,ct) in TARGETS.items():
            for dg in ('sha256','md5'):
                n+=1
                r=att(pw,salt,ct,dg)
                if r:
                    hits.append((r[0],tname,c))
                    if r[0]>=4: print('!!!',r[0],tname,repr(c[:60]),dg,r[1][:64].hex())
print(f'{len(cands)} candidates, {n} decrypts')
from collections import Counter
print('pads:',sorted(Counter(x[0] for x in hits).items()),'expected@1:',round(n/256,1))
