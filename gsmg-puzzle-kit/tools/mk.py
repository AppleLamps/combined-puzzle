import base64, hashlib, os, random
from Crypto.Cipher import AES
B='b64/'
for n,o in [('phase2','phase2.bin'),('terminal','terminal.bin'),('short','short.bin'),('cosmic','cosmic.bin')]:
    open(o,'wb').write(base64.b64decode(open(B+n+'.b64').read().replace('\n','').strip()))
def evp(pw,salt):
    d=b'';prev=b''
    while len(d)<48:
        prev=hashlib.sha256(prev+pw+salt).digest(); d+=prev
    return d[:32],d[32:48]
def enc(pt,ans,fname,salt=b'12345678',md='hex'):
    pw=hashlib.sha256(ans).hexdigest().encode() if md=='hex' else hashlib.sha256(ans).digest()
    k,iv=evp(pw,salt); p=16-len(pt)%16; pt2=pt+bytes([p])*p
    open(fname,'wb').write(b'Salted__'+salt+AES.new(k,AES.MODE_CBC,iv).encrypt(pt2))
random.seed(5)
enc(b'The quick brown fox jumps over the lazy dog; controls fire on printable text ok!!'[:79],b'plantedone','pl_text.bin')   # 79 bytes pad1
txt=('gsmg planted ebcdic block for the recogniser control 0123456789 abc').encode()
enc(txt.decode().encode('cp273'),b'plantedtwo','pl_ebcdic.bin')
enc(bytes(random.getrandbits(8) for _ in range(77)),b'plantedthree','pl_rand77.bin')   # pad 3
enc('utf16 planted control text here!'.encode('utf-16-le')+b'ab',b'plantedfour','pl_utf16.bin')
# dbbi control: T -> digits with b standing for both 2 and 0
T=b'planted control text'
N=int.from_bytes(T,'big'); ds=str(N)
letters=''.join('b' if c in '02' else chr(96+int(c)) for c in ds)
print(len(ds), ds.count('0')+ds.count('2'), letters)
enc(T+b'!',hashlib.sha256(T).hexdigest().encode() and T,'pl_dbbi.bin')  # note: plaintext T+'!' under answer T
open('ctl_letters.txt','w').write(letters)
print(len(letters), 'b count', letters.count('b'))
