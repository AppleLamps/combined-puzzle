"""Binary puzzle material as a BIP32 seed or private-key/chain-code pair.
No transactions; compare derived public points directly to the puzzle target.
Bounded paths; official BIP32 test-vector controls precede the hypothesis test.
"""
import hashlib,hmac,itertools,json,re,time
from pathlib import Path
from hash_scope import ROOT,N,TARGET,PrivateKey,sha,group_hashes,selected_hashes,scoped_commands
from next_tests import parts
OUT=Path(__file__).resolve().parent/'binary_hd'
HARD=1<<31

def master(seed):
    h=hmac.new(b'Bitcoin seed',seed,hashlib.sha512).digest();d=int.from_bytes(h[:32],'big')
    if not 0<d<N:return None
    return d,h[32:]

def child(node,i,pub=None):
    d,c=node
    data=(b'\0'+d.to_bytes(32,'big')) if i&HARD else (pub or PrivateKey.from_int(d).public_key.format())
    h=hmac.new(c,data+i.to_bytes(4,'big'),hashlib.sha512).digest();a=int.from_bytes(h[:32],'big')
    k=(a+d)%N
    if a>=N or not k:return None
    return k,h[32:]

def b58decode(s):
    alphabet='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';n=0
    for c in s:n=n*58+alphabet.index(c)
    b=n.to_bytes((n.bit_length()+7)//8,'big');b=b'\0'*(len(s)-len(s.lstrip('1')))+b
    assert sha(sha(b[:-4]))[:4]==b[-4:]
    return b[:-4]

def controls():
    # BIP32 test vector 1: root, hardened child, then non-hardened child.
    vectors=[
       'xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi',
       'xprv9uHRZZhk6KAJC1avXpDAp4MDc3sQKNxDiPvvkX8Br5ngLNv1TxvUxt4cV1rGL5hj6KCesnDYUhd7oWgT11eZG7XnxHrnYeSvkzY7d2bhkJ7',
       'xprv9wTYmMFdV23N2TdNG573QoEsfRrWKQgWeibmLntzniatZvR9BmLnvSxqu53Kw1UmYPxLgboyZQaXwTCg8MSY3H2EU4pWcQDnRnrVA1xe8fs']
    node=master(bytes(range(16)))
    for j,s in enumerate(vectors):
        if j:node=child(node,HARD if j==1 else 1)
        b=b58decode(s)
        assert b[45]==0 and node==(int.from_bytes(b[46:78],'big'),b[13:45])

def materials():
    # Same bytes were previously tried as passwords; now they are typed binary key material.
    for fn in (group_hashes,selected_hashes,scoped_commands):
        for label,b in fn():
            if len(b)==64 and not re.fullmatch(rb'[0-9a-fA-F]{64}',b):yield fn.__name__+'/'+label,b
    texts={
        'phase1':b'theflowerblossomsthroughwhatseemstobeaconcretesurface',
        'phase2':b'causality',
        'phase3':''.join(parts()).encode(),
        'phase3.2':b'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple',
        'poster-text':b'GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe',
        'poster-url':b'gsmg.io/theseedisplanted'}
    for name in ('checkerboard-digits','checkerboard-plaintext','architect-text'):
        texts[name]=(ROOT/'derived'/f'{name}.txt').read_bytes().strip()
    for name,b in texts.items():
        if 16<=len(b)<=64:yield name+'/raw',b
        yield name+'/sha256',sha(b)
        yield name+'/sha512',hashlib.sha512(b).digest()
    s=(ROOT/'files/salphaseion-textarea.txt').read_text().strip()
    for name,r in [('r1',s[:91]),('r2',s[195:765])]:
        for rev in (False,True):
            digits=(r[::-1] if rev else r).translate(str.maketrans('abcdefghi','123456789'))
            n=int(digits);b=n.to_bytes((n.bit_length()+7)//8,'big')
            for endian,blob in [('big',b),('little',b[::-1])]:
                label=f'{name}/reverse-digits={rev}/{endian}'
                if 16<=len(blob)<=64:yield label+'/raw-integer',blob
                yield label+'/sha256-integer-bytes',sha(blob)
                yield label+'/sha512-integer-bytes',hashlib.sha512(blob).digest()

def paths():
    out={(): 'root'}
    prefixes=[(),(0,),(HARD,),(HARD,0),(HARD,1),(44+HARD,HARD,HARD,0),(44+HARD,HARD,HARD,1)]
    for prefix in prefixes:
        out[prefix]='standard-family'
        for i in range(32):out[prefix+(i,)]='standard-family'
    for i in range(32):out[(i+HARD,)]='standard-family'
    for numbers in [(23,16,7),(14,14),(1,1,4,1)]:
        for bits in itertools.product((0,HARD),repeat=len(numbers)):
            out[tuple(n+b for n,b in zip(numbers,bits))]='clue-indexed'
    for i in (11110,227,149,1539):
        out[(i,)]=out[(i+HARD,)]='clue-indexed'
    return out

def pathtext(p):return 'm'+''.join('/'+str(i&0x7fffffff)+("'" if i&HARD else '') for i in p)

def main():
    controls();OUT.mkdir(exist_ok=True)
    if (OUT/'results.json').exists():raise SystemExit('results.json exists')
    t=time.monotonic();blobs={}
    for label,b in materials():blobs.setdefault(b,label)
    roots={}
    for b,label in blobs.items():
        node=master(b)
        if node:roots.setdefault(node,label+'/BIP32-seed')
        if len(b)==64:
            for swap,v in [(False,b),(True,b[32:]+b[:32])]:
                d=int.from_bytes(v[:32],'big')
                if 0<d<N:roots.setdefault((d,v[32:]),label+f'/private-chain-pair/swap={swap}')
    todo=paths();hits=[];checks=0;ckd=0;invalid=0
    for idx,(root,label) in enumerate(roots.items(),1):
        cache={():root};pubs={}
        def resolve(p):
            nonlocal ckd,invalid
            if p in cache:return cache[p]
            parent=resolve(p[:-1])
            if parent is None:cache[p]=None;return None
            pk=pubs.setdefault(parent,PrivateKey.from_int(parent[0]).public_key.format()) if not p[-1]&HARD else None
            node=child(parent,p[-1],pk);ckd+=1
            if node is None:invalid+=1
            cache[p]=node;return node
        for p,family in todo.items():
            node=resolve(p)
            if node is None:continue
            checks+=1
            pub=pubs.get(node)
            if pub is None:pub=PrivateKey.from_int(node[0]).public_key.format();pubs[node]=pub
            if pub==TARGET:hits.append(dict(source=label,path=pathtext(p),private_key_hex=f'{node[0]:064x}'))
        if idx%250==0:print('roots completed',idx,'of',len(roots),flush=True)
    result=dict(distinct_materials=len(blobs),distinct_roots=len(roots),paths_per_root=len(todo),
                paths={pathtext(p):f for p,f in todo.items()},child_derivations=ckd,invalid_children=invalid,
                target_point_comparisons=checks,target_matches=hits,seconds=round(time.monotonic()-t,2))
    (OUT/'results.json').write_text(json.dumps(result,indent=2))
    (OUT/'materials.json').write_text(json.dumps([dict(source=l,material_hex=b.hex()) for b,l in blobs.items()],indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='paths'}),flush=True)

if __name__=='__main__':main()
