from pathlib import Path
import base64, hashlib, json, math, re, collections
from Crypto.Cipher import AES
from PIL import Image
R=Path(__file__).resolve().parent
A='abcdefghiklmnopqrstuvwxyz'
def isprime(n): return n>1 and all(n%d for d in range(2,math.isqrt(n)+1))
def bifid(text,square,period=None,inverse=False):
    period=period or len(text);out=''
    for j in range(0,len(text),period):
        t=text[j:j+period];rc=[divmod(square.index(c),5) for c in t]
        if inverse:
            q=[r for r,c in rc]+[c for r,c in rc]
            out+=''.join(square[q[i]*5+q[i+1]] for i in range(0,len(q),2))
        else:
            q=[x for p in rc for x in p];n=len(t)
            out+=''.join(square[5*q[i]+q[i+n]] for i in range(n))
    return out
def hill(text,k,A=A):
    v=[A.index(c) for c in text];a,b,c,d=k;n=len(A)
    assert len(v)%2==0
    return ''.join(A[(a*x+b*y)%n]+A[(c*x+d*y)%n] for x,y in zip(v[::2],v[1::2]))
def decrypt(raw,pw,digest='sha256'):
    assert raw[:8]==b'Salted__';salt=raw[8:16];key=b'';prev=b''
    while len(key)<48:
        prev=hashlib.new(digest,prev+pw+salt).digest();key+=prev
    p=AES.new(key[:32],AES.MODE_CBC,key[32:48]).decrypt(raw[16:]);pad=p[-1]
    return p[:-pad] if 1<=pad<=16 and p[-pad:]==bytes([pad])*pad else None
def parse(s):
    def rec(i,c):
        if i==len(s):yield c;return
        n=len(c)+1
        for tok in (['b','be'] if isprime(n) else [s[i]]):
            if s.startswith(tok,i):yield from rec(i+len(tok),c+[tok])
    return list(rec(0,[]))
html=(R/'inputs/salphaseion_phase3.html').read_text()
rawareas=re.findall(r'<textarea[^>]*>(.*?)</textarea>',html,re.S)
s=''.join(rawareas[0].split());assert s==(R/'inputs/salphaseion-textarea.txt').read_text().strip()
db=s[:91];faed=s[195:765];square=''.join(dict.fromkeys(db+A))
bif=bifid(faed,square);assert bifid(bif,square,inverse=True)==faed
carrier=bif[7::2];companion=bif[8::2];hkey=(2,4,21,9);hout=hill(carrier,hkey)
def decnum(t):
    digits=''.join('0' if c=='o' else str(ord(c)-96) for c in t)
    n=int(digits);return n.to_bytes((n.bit_length()+7)//8,'big').decode()
labels={'matrix':bytes(int(s[i:i+8].translate(str.maketrans('ab','01')),2) for i in range(91,195,8)).decode(),'lastwords':decnum(s[766:829]),'thispassword':decnum(s[830:859])}
assert labels=={'matrix':'matrixsumlist','lastwords':'lastwordsbeforearchichoice','thispassword':'thispassword'}
# Forward encoders reproduce every character of the three decoded label fields.
assert ''.join(f'{c:08b}' for c in labels['matrix'].encode()).translate(str.maketrans('01','ab'))==s[91:195]
for key,span in [('lastwords',(766,829)),('thispassword',(830,859))]:
    encoded=str(int.from_bytes(labels[key].encode(),'big')).translate(str.maketrans('0123456789','oabcdefghi'))
    assert encoded==s[slice(*span)]
short=base64.b64decode(s[895:959]+s[999:1063]);assert short==base64.b64decode((R/'inputs/salphaseion-short.b64').read_text())
assert base64.b64decode(rawareas[1])==base64.b64decode((R/'inputs/cosmic-duality.b64').read_text())
answer=b'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple'
phase=decrypt(base64.b64decode((R/'inputs/phase3.2.b64').read_text()),hashlib.sha256(answer).hexdigest().encode())
assert phase and len(phase)==2422
ebcdic=phase[447:1986].decode('latin1').encode('cp273').decode().upper();key='THEMATRIXHASYOU'
arch=''.join(chr(65+(ord(key[i%len(key)])-ord(c))%26) for i,c in enumerate(ebcdic))
back=''.join(chr(65+(ord(key[i%len(key)])-ord(c))%26) for i,c in enumerate(arch))
assert back==ebcdic
(R/'inputs/phase32-exact.bin').write_bytes(phase);(R/'inputs/architect.txt').write_text(arch)
ps=parse(db);assert sorted(map(len,ps))==[83,84];p=next(p for p in ps if len(p)==84)
vals=[(-i if t=='b' else i) if isprime(i) else ord(t)-96 for i,t in enumerate(p,1)]
sums=[sum(vals[i::12]) for i in range(12)];hs=''.join(chr(65+v%26) for v in sums)
assert hs=='HILLFEXMGSGQ'
# Source-letter pairs are the exact source of the alternating Bifid channels.
pairs=[]
for i in range(285):
    x,y=faed[i],faed[i+285];rx,cx=divmod(square.index(x),5);ry,cy=divmod(square.index(y),5)
    assert bif[2*i]==square[rx*5+ry] and bif[2*i+1]==square[cx*5+cy]
    pairs.append({'i':i,'source':x+y,'rows':square[rx*5+ry],'columns':square[cx*5+cy]})
out=dict(square=square,labels=labels,parses=ps,values=vals,sums=sums,hill_instruction=hs,bifid=bif,carrier=carrier,companion=companion,hill_output=hout,pairs=pairs,source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'inputs').iterdir()},controls=['label forward round trips','known AES phase32 2422 bytes','Beaufort round trip','full Bifid round trip','pair-by-pair Bifid decomposition'])
if __name__=='__main__':
    (R/'reconstruction.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k not in ['pairs','source_hashes','bifid','carrier','companion','parses','values']},indent=2))
