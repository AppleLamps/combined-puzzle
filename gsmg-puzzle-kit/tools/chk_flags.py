import glob, hashlib, base64, math, sys
from Crypto.Cipher import AES
from candidate_encoding import decode_candidate
def evp(pw,salt,md):
    h=hashlib.sha256 if md==0 else hashlib.md5
    d=b'';p=b''
    while len(d)<48:
        p=h(p+pw+salt).digest(); d+=p
    return d[:32],d[32:48]
C={}
for nm,fn in (('terminal','terminal'),('short','short'),('cosmic','cosmic')):
    raw=base64.b64decode(open('b64/%s.b64'%fn).read())
    C[nm]=(raw[8:16],raw[16:])
def recog(p):
    n=len(p)
    if n<8: return None
    pr=sum(1 for c in p if 32<=c<127 or c in (9,10,13))/n
    if pr>=0.8: return 'printable %.2f'%pr
    sd=math.sqrt(n/4)
    for b in range(8):
        z=(sum(1 for c in p if c>>b&1)-n/2)/sd
        if abs(z)>=6: return 'bitbias'
    nd=len(set(p)); q=1-1/256; E=256*(1-q**n); V=256*255*(1-2/256)**n+256*q**n-65536*q**(2*n)
    if V>0 and (nd-E)/math.sqrt(V)<=-6: return 'distinct'
    if n>=16 and sum(1 for i in range(1,n,2) if p[i]==0)/(n/2)>=0.6: return 'utf16'
    if b'Salted__' in p: return 'nestedsalt'
    if p[:3]==b'\x1f\x8b\x08' or p[:4]==b'PK\x03\x04' or p[:4]==b'\x89PNG' or p[:4]==b'%PDF': return 'magic'
    return None
tot=0;hits=[]
for f in sorted(glob.glob(sys.argv[1] if len(sys.argv)>1 else '*.out')):
    for line in open(f,errors='replace'):
        p=line.rstrip('\n').split('\t')
        if p[0]!='FLAG' or len(p)<9: continue
        cand=p[7]; form=int(p[2][4:]); md=int(p[3][2:])
        cb=decode_candidate(cand)
        d=hashlib.sha256(cb).digest()
        if form==0: pw=d.hex().encode()
        elif form==1: pw=d
        elif form==2: pw=hashlib.sha256(d).hexdigest().encode()
        else: pw=hashlib.sha256(d.hex().encode()).hexdigest().encode()
        salt,ct=C[p[1]]
        k,iv=evp(pw,salt,md)
        pt=AES.new(k,AES.MODE_CBC,iv).decrypt(ct)
        pad=pt[-1]; body=pt[:-pad]
        assert 1 <= pad <= 16 and 'pad%d'%pad==p[4] and pt[-pad:]==bytes([pad])*pad, ('re-decrypt mismatch',f,line[:120])
        tot+=1
        r=recog(body)
        if r: hits.append((f,p[1],cand[:60],r))
print('all retained valid pads content-checked:',tot,'recogniser hits:',hits)
