"""Lossless 512-bit row-channel extraction and bounded exact cryptographic tests."""
from reconstruct import *
import hmac,itertools,random
from coincurve import PrivateKey
import sys as _sys
_sys.path.insert(0, str(R.parents[1] / 'tools'))
import prize_gate  # shared gate: Half and Better Half, both serializations
N=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
Q=bytes.fromhex('04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a4649c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559')
H=1<<31
sha=lambda x:hashlib.sha256(x).digest()
def master(seed):
 h=hmac.new(b'Bitcoin seed',seed,hashlib.sha512).digest();d=int.from_bytes(h[:32],'big')
 return (d,h[32:]) if 0<d<N else None
def child(node,i):
 d,c=node;data=b'\0'+d.to_bytes(32,'big') if i&H else PrivateKey.from_int(d).public_key.format()
 h=hmac.new(c,data+i.to_bytes(4,'big'),hashlib.sha512).digest();v=int.from_bytes(h[:32],'big');k=(v+d)%N
 return (k,h[32:]) if v<N and k else None
def b58(s):
 n=0
 for c in s:n=n*58+'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'.index(c)
 b=n.to_bytes((n.bit_length()+7)//8,'big');b=b'\0'*(len(s)-len(s.lstrip('1')))+b
 assert sha(sha(b[:-4]))[:4]==b[-4:];return b[:-4]
# Independent BIP32 published test-vector checks.
vectors=['xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi','xprv9uHRZZhk6KAJC1avXpDAp4MDc3sQKNxDiPvvkX8Br5ngLNv1TxvUxt4cV1rGL5hj6KCesnDYUhd7oWgT11eZG7XnxHrnYeSvkzY7d2bhkJ7','xprv9wTYmMFdV23N2TdNG573QoEsfRrWKQgWeibmLntzniatZvR9BmLnvSxqu53Kw1UmYPxLgboyZQaXwTCg8MSY3H2EU4pWcQDnRnrVA1xe8fs']
node=master(bytes(range(16)))
for i,s in enumerate(vectors):
 if i:node=child(node,H if i==1 else 1)
 v=b58(s);assert node==(int.from_bytes(v[46:78],'big'),v[13:45])
assert b58('1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe')==b'\0'+hashlib.new('ripemd160',sha(Q)).digest()

orders={'source':list(range(570)), 'paired':[j for i in range(285) for j in (i,i+285)]}
materials={};factorizations=[]
for sq in json.loads((R/'structural_tests.json').read_text())['header_squares']:
 rows=[sq.index(c)//5 for c in faed];cols=[sq.index(c)%5 for c in faed]
 for label,order in orders.items():
  free=[rows[i] for i in order if cols[i]!=4];assert all(rows[i]==0 for i in range(570) if cols[i]==4)
  # Decode free bits using unchanged column stream, restoring forced zero rows.
  rr=[None]*570;it=iter(free)
  for i in order:rr[i]=0 if cols[i]==4 else next(it)
  assert list(it)==[] and ''.join(sq[5*r+c] for r,c in zip(rr,cols))==faed
  rec=dict(square=sq,order=label,free_bits=len(free),ones=sum(free),forced_positions=[i for i in range(570) if cols[i]==4])
  if len(free)==512:
   for polarity,rev,lsb in itertools.product(range(2),repeat=3):
    bits=[b^polarity for b in free];bits=bits[::-1] if rev else bits
    raw=bytes(sum(b<<(i if lsb else 7-i) for i,b in enumerate(bits[j:j+8])) for j in range(0,512,8))
    name=f'{sq}/{label}/polarity={polarity}/reverse={rev}/lsb={lsb}'
    materials.setdefault(raw,[]).append(name)
    if not(polarity or rev or lsb):rec['hex']=raw.hex()
  factorizations.append(rec)
# Exact lossless encoder control on randomly chosen free bits and these columns.
rng=random.Random(512)
cols=[square.index(c)%5 for c in faed];bits=[rng.randrange(2) for _ in range(512)];it=iter(bits)
encoded=''.join(square[5*(0 if c==4 else next(it))+c] for c in cols)
assert [square.index(c)//5 for c in encoded if square.index(c)%5!=4]==bits
assert bifid(encoded,square)[1::2]==bif[1::2]
paths={()}
for prefix in [(),(0,),(H,),(H,0),(H,1),(44+H,H,H,0),(44+H,H,H,1)]:
 paths.add(prefix)
 for i in range(32):paths.add(prefix+(i,))
for i in range(32):paths.add((i+H,))
for ns in [(23,16,7),(14,14),(1,1,4,1)]:
 for bs in itertools.product((0,H),repeat=len(ns)):paths.add(tuple(a+b for a,b in zip(ns,bs)))
for i in (11110,227,149,1539):paths.update({(i,),(i+H,)})
def pathtext(p):return 'm'+''.join('/'+str(i&0x7fffffff)+("'" if i&H else '') for i in p)
checks=0;hits=[];direct=set();roots={}
def check(d,label):
 global checks
 if not 0<d<N:return
 checks+=1
 if prize_gate.gate_scalar(d):hits.append(dict(source=label,scalar=f'{d:064x}'))
for raw,names in materials.items():
 label=names[0];roots.setdefault(master(raw),label+'/BIP32-seed')
 for swap in (False,True):
  b=raw[32:]+raw[:32] if swap else raw;d=int.from_bytes(b[:32],'big')
  if 0<d<N:roots.setdefault((d,b[32:]),label+f'/private-chain/swap={swap}')
 for name,b in [('first',raw[:32]),('last',raw[32:]),('xor',bytes(x^y for x,y in zip(raw[:32],raw[32:]))),('sha256',sha(raw))]:
  d=int.from_bytes(b,'big');direct.add(d);check(d,label+'/'+name)
 for mod in [int.from_bytes(raw,'big')%N]:direct.add(mod);check(mod,label+'/512-mod-n')
for root,label in roots.items():
 if root is None:continue
 cache={():root}
 def resolve(p):
  if p not in cache:
   parent=resolve(p[:-1]);cache[p]=child(parent,p[-1]) if parent else None
  return cache[p]
 for p in sorted(paths):
  node=resolve(p)
  if node:check(node[0],label+'/'+pathtext(p))
# Exact OpenSSL-format decryption tests; padding is recorded, not accepted as evidence.
containers={n:base64.b64decode((R/'inputs'/f'{n}.b64').read_bytes()) for n in ['terminal','salphaseion-short','cosmic-duality']}
aes=[];trials=0
for raw,names in materials.items():
 for form,pw in [('raw',raw),('hex',raw.hex().encode()),('sha256hex',hashlib.sha256(raw).hexdigest().encode()),('first-half',raw[:32]),('last-half',raw[32:])]:
  for digest in ['sha256','md5']:
   for name,ct in containers.items():
    body=decrypt(ct,pw,digest);trials+=1
    if body is not None:aes.append(dict(source=names[0],form=form,digest=digest,container=name,plaintext_hex=body.hex(),all_text=all(x in (9,10,13) or 32<=x<=126 for x in body)))
result=dict(factorizations=factorizations,distinct_materials=len(materials),materials=[dict(hex=b.hex(),names=ls) for b,ls in materials.items()],distinct_roots=len(roots),paths_per_root=len(paths),paths=list(map(pathtext,sorted(paths))),direct_scalars=len(direct),point_checks=checks,prize_hits=hits,aes_trials=trials,aes_padding_outputs=aes,controls=['512-bit lossless random encoder preserving complete column stream','BIP32 official vector1 root, hardened and nonhardened children','prize pubkey hash matches Base58Check address'],scope='Four BTCSEED-producing squares with 512 free bits; source and paired order; both polarity, whole-bit reversal, byte bit direction. BIP32 full64 seed or two halves as scalar/chain in both orders. 295 documented paths. Direct halves, XOR, SHA256, 512-bit value mod n. OpenSSL passwords raw, hex, SHA256hex, both raw halves, EVP SHA256/MD5 on three containers.')
(R/'free_rows.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ['factorizations','materials','paths','aes_padding_outputs']},indent=2));print('Padding-only:',len(aes),'all text:',sum(a['all_text'] for a in aes))
