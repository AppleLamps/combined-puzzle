import base64,hashlib,re,sys,json
from Crypto.Cipher import AES
doss=open(sys.argv[1]).read()
res=[]
def chk(name,cond,extra=''):
    res.append((name,bool(cond)))
    print(('PASS ' if cond else 'FAIL ')+name+(' '+str(extra) if extra and not cond else ''))
blocks=re.findall(r'```[a-z]*\n(.*?)```',doc:=doss,re.S)
def blk(prefix):
    c=[b for b in blocks if b.startswith(prefix)]
    assert len(c)==1,(prefix,len(c))
    return c[0]
def joined(b): return ''.join(b.split('\n'))
def norm(s): return re.sub(r'\s+','',s)
pt3=open('pt3.bin','rb').read(); pt32=open('pt32.bin','rb').read()
sha=lambda b: hashlib.sha256(b).hexdigest()
# ---- chain hashes
chk('phase3 plaintext sha',sha(pt3)=='c4ad94559a44a927c1032cc0e024515f9510a0806a2d14458dbf4a360af9865f')
chk('phase3.2 plaintext sha',sha(pt32)=='b82afeb86f9e50848220f9b64b744b821400308aea273a1c949b9d2d0e408a34')
chk('phase3.2 len 2422 pad10',len(pt32)==2422)
chk('answers sha (phase1)',hashlib.sha256(b'theflowerblossomsthroughwhatseemstobeaconcretesurface').hexdigest()=='5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75')
chk('causality pw',hashlib.sha256(hashlib.sha256(b'causality').hexdigest().encode()).hexdigest() is not None and hashlib.sha256(b'causality').hexdigest()=='eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf')
for h in ['5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75','eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf','1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5','250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c']:
    chk('hash present in text '+h[:8],h in doc)
# ---- phase-2 plaintext
p2=blk('The ironic 2name')
p2b=p2.rstrip('\n').replace('\n','\r\n').encode()
chk('phase2 plaintext 648 bytes',len(p2b)==648,len(p2b))
chk('phase2 plaintext sha e2f9dd65',sha(p2b)=='e2f9dd65604a3231f8b3301724e8d713a88fffc4b6c7c4aeeb20f58a582b593a')
chk('phase2 six CRLF',p2b.count(b'\r\n')==6)
# ---- riddle head, intro, riddle, digits, message, terminal
chk('riddle head vs phase3 pt',norm(blk('What if the merovingian'))==norm(pt3[:726].decode('latin-1')),len(norm(blk('What if'))))
intro=pt32[:447].decode('latin-1')
chk('intro vs pt32[0:447]',norm(blk("I've been waiting"))==norm(intro))
chk('checkerboard riddle',norm(blk('Raising the stakes'))==norm(pt32[2143:2292].decode('latin-1')))
digs=pt32[1990:2139].decode('latin-1')
chk('149 digits',joined(blk('1516594312'))==digs and len(digs)==149)
chk('pt32 layout CRLFs',pt32[1986:1990]==b'\r\n\r\n' and pt32[2139:2143]==b'\r\n\r\n')
pr=sum(1 for b in pt32 if 32<=b<=126)
chk('strictly printable 1426 (58.9%)',pr==1426 and round(100*pr/len(pt32),1)==58.9,(pr,))
# Architect
seg=pt32[447:1986].decode('latin-1').encode('cp273')
key='THEMATRIXHASYOU'
idx=lambda c:(c-65) if 65<=c<=90 else (c-97)
out=''.join(chr((ord(key[i%len(key)])-65-idx(c)) % 26 + 65) for i,c in enumerate(seg))
arch=joined(blk('YOURLIFEISTHESUMOF'))
chk('architect 1539 letters',len(arch)==1539 and arch.isalpha())
chk('architect decode == dossier block',out==arch)
chk('PRIVATEKEY at 479 and 1238',[m.start() for m in re.finditer('PRIVATEKEY',arch)]==[479,1238],[m.start() for m in re.finditer('PRIVATEKEY',arch)])
chk('PRIVATEKEY[479:]',arch[479:].startswith('PRIVATEKEYYOUVEEARNEDITBUTPLEASE'))
# checkerboard
top='FUBCDORA'; r1='.LETHINGKY'; r4='MVPS/JQZXW'
cols=[0,2,3,5,6,7,8,9]
topmap={str(c):top[i] for i,c in enumerate(cols)}
def dec(s):
    o='';i=0
    while i<len(s):
        d=s[i]
        if d in '14':
            r=r1 if d=='1' else r4; o+=r[int(s[i+1])]; i+=2
        else: o+=topmap[d]; i+=1
    return o
cb=dec(digs)
msg=blk('INCASEYOUMANAGE')
chk('checkerboard decodes to 91 letters',re.sub('[^A-Z]','',cb.replace('.','').replace('/',''))==msg.strip() or cb.replace('.','').replace('/','')==msg.strip(),cb)
chk('checkerboard message length 91',len(msg.strip())==91)
# uniqueness of blank pair (doc 42)
import itertools
cnt=0
for a,b in itertools.combinations(range(10),2):
    cols2=[c for c in range(10) if c not in (a,b)]
    tm={str(c):top[i] for i,c in enumerate(cols2)}
    rr={str(a):r1,str(b):r4}
    try:
        o='';i=0;s=digs
        while i<len(s):
            d=s[i]
            if d in rr: o+=rr[d][int(s[i+1])]; i+=2
            else: o+=tm[d]; i+=1
        if o.replace('.','').replace('/','')==msg.strip(): cnt+=1
    except Exception: pass
chk('only one blank pair reproduces plaintext',cnt==1,cnt)
# terminal
term=joined(blk('U2FsdGVkX1+0Wl49'))
chk('terminal block == pt32 tail',pt32[2292:].decode().replace('\r\n','')==term)
# ---- containers
tab={'b45a5e3d827593ca':('291dfd6f3e759ec2e272b35a00c24907da70c3e7a9291b4c13605c7b0b4f3de9',96),
     '3ab585348552415d':('9e2831e1b34b5f34796df47ccaf6530d48d371c61a6bff84d60db1064fa7a258',96),
     '2d3f6fe06dc950e6':('b18950551a4dd0cb8a9378f0906ba18c03a15f0ee83eb98c6bc90165c5f79805',1344)}
sal=joined(blk('U2FsdGVkX186tYU0'))
cos=joined(blk('U2FsdGVkX18tP2/g'))
for name,b in [('terminal',term),('salphaseion short',sal),('cosmic duality',cos)]:
    raw=base64.b64decode(b); salt=raw[8:16].hex()
    chk('container '+name+' sha/size/salt',salt in tab and tab[salt][0]==sha(raw) and tab[salt][1]==len(raw) and raw[:8]==b'Salted__',(salt,len(raw)))
# ---- textarea
ta=joined([b for b in blocks if b.startswith('dbbibfbhccbegbihabe') and len(b)>1000][0])
chk('textarea 1075 chars',len(ta)==1075,len(ta))
def ab(s): return bytes(int(s[i:i+8].replace('a','0').replace('b','1'),2) for i in range(0,len(s),8)).decode()
def rule2(block):
    d=''.join('0' if c=='o' else str(ord(c)-96) for c in block); n=int(d); h=hex(n)[2:]
    if len(h)%2: h='0'+h
    return bytes.fromhex(h).decode()
chk('a/b run 91:195 = matrixsumlist',ab(ta[91:195])=='matrixsumlist')
chk('z separators',ta[765]=='z' and ta[829]=='z' and ta[859]=='z')
chk('segment1 lastwordsbeforearchichoice',rule2(ta[766:829])=='lastwordsbeforearchichoice')
chk('segment2 thispassword',rule2(ta[830:859])=='thispassword')
chk('literal 860:895',ta[860:895]=='shabefourfirsthintisyourlastcommand')
chk('a/b run 959:999 = enter',ab(ta[959:999])=='enter')
chk('literal 1063:1075',ta[1063:1075]=='shabefanstoo')
chk('sal short == halves joined',ta[895:959]+ta[999:1063]==sal)
dbbi=ta[:91]; faed=ta[195:765]
chk('dbbi block',joined([b for b in blocks if b.startswith('dbbibfbhcc') and len(b)<200][0])==dbbi)
chk('faed block',joined(blk('faedggeedfcb'))==faed and len(faed)==570)
from collections import Counter
cf=Counter(faed)
chk('faed counts',[cf[c] for c in 'abcdefghi']==[54,49,52,49,69,57,107,58,75],[cf[c] for c in 'abcdefghi'])
# parse
def isprime(n):
    if n<2: return False
    return all(n%p for p in range(2,int(n**.5)+1))
prog='BBBBYBBBYYBBBBYBBYYBFYYBY'
pos=0;k=0;hosts=[];resid='';p=1
while pos<len(dbbi):
    if isprime(p):
        s=prog[k];k+=1
        n=2 if s=='Y' else 1
        hosts.append(dbbi[pos:pos+n]);pos+=n
    else:
        resid+=dbbi[pos];pos+=1
    p+=1
chk('parse consumes 91, last position 83',pos==91 and p-1==83,(pos,p-1))
chk('23 hosts, all b, 8 be',len(hosts)==23 and all(h[0]=='b' for h in hosts) and sum(h=='be' for h in hosts)==8,(len(hosts),Counter(hosts)))
chk('residue 60 == block',resid==blk('difhccgihaeeihgg').strip() and len(resid)==60,resid)
cr=Counter(resid)
chk('residue counts',[cr[c] for c in 'abcdefghi']==[3,2,8,4,10,10,10,8,5],[cr[c] for c in 'abcdefghi'])
# ---- spiral / poster
sp=joined(blk('0110011101110011'))
chk('spiral 196 bits',len(sp)==196)
chk('spiral decodes to URL + 0000',bytes(int(sp[i:i+8],2) for i in range(0,192,8)).decode()=='gsmg.io/theseedisplanted' and sp[192:]=='0000')
# ---- addresses and hash160
A='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def b58d(s):
    n=0
    for c in s: n=n*58+A.index(c)
    b=n.to_bytes(25,'big')
    return b
def b58e(b):
    n=int.from_bytes(b,'big');s=''
    while n: n,r=divmod(n,58);s=A[r]+s
    return '1'*(len(b)-len(b.lstrip(b'\0')))+s
def h160(b): return hashlib.new('ripemd160',hashlib.sha256(b).digest()).digest()
addrs=set(re.findall(r'\b([13][1-9A-HJ-NP-Za-km-z]{25,34})\b',doc))
bad=[]
for a in sorted(addrs):
    try:
        raw=b58d(a)
        ok=hashlib.sha256(hashlib.sha256(raw[:21]).digest()).digest()[:4]==raw[21:]
    except Exception as e: ok=False
    print('  addr',a,'checksum',ok, 'h160',raw[1:21].hex() if ok else '')
    if not ok: bad.append(a)
chk('all full addresses pass base58check',not bad,bad)
# hash160 in text corresponds to address
pairs=[('1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe','a9553269572a317e39f0f518cb87c1a0ee1dbae4'),
       ('17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa','4bc468447fe1b048ad030a2f9a125478eabc4ed6'),
       ('1cc6xayvqpeetixmuXDRsGug7GKyoRdxP','06bbdc66fda09110435c79a86656a604c2d5c69b')]
for a,h in pairs:
    chk('address->hash160 '+a[:10],a in doc and h in doc and b58d(a)[1:21].hex()==h,(a in doc,h in doc))
pub_u='04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a4649c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559'
pub_c='03f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464'
compact=re.sub(r'\s+','',re.search(r'uncompressed\s+(04[0-9a-f\s]+?)\n\s*compressed',doc).group(1))
chk('uncompressed pub text == known',compact==pub_u,compact)
cc=re.search(r'compressed\s+(03[0-9a-f]+)',doc).group(1)
chk('compressed pub text',cc==pub_c)
chk('hash160(uncompressed)=a9553269',h160(bytes.fromhex(pub_u)).hex()=='a9553269572a317e39f0f518cb87c1a0ee1dbae4')
chk('hash160(compressed)=06bbdc66',h160(bytes.fromhex(pub_c)).hex()=='06bbdc66fda09110435c79a86656a604c2d5c69b')
# on curve
P=2**256-2**32-977
x=int(pub_u[2:66],16); y=int(pub_u[66:],16)
chk('prize point on curve',(y*y-x**3-7)%P==0)
chk('y odd -> 03 prefix',y%2==1)
# win test code
ns={}
code=blk('import hashlib, coincurve')
exec(code,ns)
NEI=ns['NEIGHBOURS']; TG=ns['TARGETS']
import coincurve
k1=coincurve.PrivateKey((1).to_bytes(32,'big')).public_key.format(True)
chk('key 1 -> 751e76e8...',h160(k1).hex()=='751e76e8199196d454941c45d1b3a323f1433bd6' and '751e76e8199196d454941c45d1b3a323f1433bd6' in doc)
X='selftest'
priv=hashlib.sha256(X.encode()).digest()
pk=coincurve.PrivateKey(priv).public_key
chk('win() control fires',ns['win'](X,targets={h160(pk.format(True)).hex()}) and not ns['win'](X))
# neighbour prefixes in text
for pre in re.findall(r'`(1[1-9A-HJ-NP-Za-km-z]{8,12})\.\.\.`',doc):
    m=[h for h in NEI if b58e(b'\x00'+bytes.fromhex(h)+hashlib.sha256(hashlib.sha256(b'\x00'+bytes.fromhex(h)).digest()).digest()[:4]).startswith(pre)]
    print('  prefix',pre,'->',len(m),'neighbour(s)' if m else 'not a neighbour')
chk('four neighbour hash160 in text',all(h in doc for h in NEI) and len(NEI)==4)
# summary
fails=[n for n,o in res if not o]
print('\n%d checks, %d failed'%(len(res),len(fails)))
if fails: print(fails)
sys.exit(1 if fails else 0)
