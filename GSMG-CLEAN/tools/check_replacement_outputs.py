"""Inspect retained replacement-pipeline bytes, without importing AES tooling."""
import argparse
import base64
import hashlib
import json
import re
from collections import Counter, deque
from pathlib import Path
from coincurve import PrivateKey

N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
B58='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
PAT='01234556728966286abc61c88b48de3086dd501d5557d6bab5605233df7bbb96'
TARGETS={'a9553269572a317e39f0f518cb87c1a0ee1dbae4':'Half',
         '4bc468447fe1b048ad030a2f9a125478eabc4ed6':'Better Half'}

def sha(b): return hashlib.sha256(b).digest()
def pattern(s):
    mapping={}
    return tuple(mapping.setdefault(c,len(mapping)) for c in s)

def candidates(raw):
    for i in range(max(0,len(raw)-31)):
        for endian in ['big','little']:
            yield f'raw32-{endian}@{i}',int.from_bytes(raw[i:i+32],endian)
    text=raw.decode('latin1')
    for m in re.finditer(r'(?<![0-9a-fA-F])[0-9a-fA-F]{64}(?![0-9a-fA-F])',text):
        yield f'hex64@{m.start()}',int(m[0],16)
    # Both lengths, at every eligible start: greedy regex must not hide a 51-char WIF.
    for m in re.finditer(r'[5KL]',text):
        for size in [51,52]:
            token=text[m.start():m.start()+size]
            if len(token)!=size or any(c not in B58 for c in token): continue
            n=0
            for c in token: n=n*58+B58.index(c)
            b=n.to_bytes((n.bit_length()+7)//8,'big')
            if len(b) not in (37,38) or sha(sha(b[:-4]))[:4]!=b[-4:]: continue
            if b[0]!=128 or (len(b)==38 and b[-5]!=1): continue
            yield f'WIF@{m.start()}',int.from_bytes(b[1:33],'big')
    for m in re.finditer(r'(?<!\d)\d{1,78}(?!\d)',text):
        yield f'decimal@{m.start()}',int(m[0])

def children(raw):
    try: s=re.sub(r'\s+','',raw.decode('ascii'))
    except UnicodeError: return
    h=s.removeprefix('0x')
    if len(h)>=2 and len(h)%2==0 and re.fullmatch('[0-9a-fA-F]+',h):
        yield 'hex',bytes.fromhex(h)
    if len(s)>=8 and len(s)%8==0 and re.fullmatch('[01]+',s):
        yield 'binary',bytes(int(s[i:i+8],2) for i in range(0,len(s),8))
    if 1<=len(s)<=4000 and re.fullmatch('[0-9]+',s):
        n=int(s); yield 'decimal',n.to_bytes(max(1,(n.bit_length()+7)//8),'big')
    for alt in [None,b'-_']:
        if len(s)<16: continue
        try:
            b=base64.b64decode(s+'='*(-len(s)%4),altchars=alt,validate=True)
            if base64.b64encode(b,altchars=alt).decode().rstrip('=')==s.rstrip('='):
                yield 'base64',b
        except ValueError: pass

def check_scalar(k,targets):
    if not 1<=k<N: return []
    p=PrivateKey(k.to_bytes(32,'big')).public_key
    return [(targets[h],compressed) for compressed in [False,True]
            if (h:=hashlib.new('ripemd160',sha(p.format(compressed=compressed))).hexdigest()) in targets]

def controls():
    k=1; raw=k.to_bytes(32,'big')
    target={'751e76e8199196d454941c45d1b3a323f1433bd6':'planted k=1'}
    assert check_scalar(k,target) and not check_scalar(2,target)
    for test in [raw,b'x'*32+raw,raw+b'x'*32,raw.hex().encode()]:
        assert any(v==k for _,v in candidates(test))
    token=b'5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf'
    assert any(kind.startswith('WIF') and v==k for kind,v in candidates(token))
    assert any(b==raw for _,b in children(base64.b64encode(raw)))
    assert not any(kind.startswith('WIF') for kind,_ in candidates(token[:-1]+b'g'))
    return True

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('corpus',type=Path)
    args=ap.parse_args(); assert controls()
    seen_nodes,seen_scalars=set(),set(); counts=Counter();hits=[];pattern_hits=[]
    with args.corpus.open(encoding='utf-8') as f:
        for line_no,line in enumerate(f,1):
            row=json.loads(line);raw=bytes.fromhex(row['raw_hex']) if 'raw_hex' in row else row['output'].encode()
            counts['records']+=1
            q=deque([('raw',raw,0)])
            while q:
                route,b,depth=q.popleft()
                if b in seen_nodes: continue
                seen_nodes.add(b);counts['nodes']+=1
                if pattern(sha(b).hex())==pattern(PAT): pattern_hits.append(dict(line=line_no,route=route))
                for kind,k in candidates(b):
                    counts[kind.split('@')[0]]+=1
                    if not 1<=k<N or k in seen_scalars: continue
                    seen_scalars.add(k)
                    found=check_scalar(k,TARGETS)
                    if found: hits.append(dict(line=line_no,route=route,kind=kind,targets=found,scalar=f'{k:064x}'))
                if depth<2:
                    q.extend((route+'/'+name,child,depth+1) for name,child in children(b) if child!=b)
            if line_no%5000==0: print('scanned',line_no,'unique scalars',len(seen_scalars),flush=True)
    result=dict(corpus=str(args.corpus.resolve()),sha256=sha(args.corpus.read_bytes()).hex(),
                controls_passed=True,counts=dict(counts),unique_scalars=len(seen_scalars),hits=hits,
                optional_dbbi_pattern_hits=pattern_hits,
                limits=['two recursive decoding levels','two prize targets, both public-key encodings',
                        'no arbitrary concatenation, brute force, AES or target implication for intermediate outputs'])
    (args.corpus.parent/'key_format_check.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__': main()