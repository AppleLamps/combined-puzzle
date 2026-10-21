"""Hash placement and selection tests prompted by the two SalPhaseIon SHA markers.
No solved-stage decrypts or flat text dictionary sweeps. Exact candidates and
padding-valid binary outputs are recorded. Requires pycryptodome and coincurve.
Run: python review_leads/hash_scope.py
"""
from pathlib import Path
from collections import Counter
import base64, hashlib, itertools, json, re, time
from Crypto.Cipher import AES
from coincurve import PrivateKey, PublicKey
from next_tests import parts, partitions
from run_new_leads import ROOT, RAW, GRID, sha, evp

OUT=Path(__file__).resolve().parent/'hash_scope'
N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
TARGET=bytes.fromhex('03f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464')

def forms(b):
    return [('as-password',b),('outer-sha256-hex',sha(b).hex().encode()),('outer-sha256-raw',sha(b))]

def weave(pieces):
    return bytes(c for col in itertools.zip_longest(*pieces,fillvalue=None) for c in col if c is not None)

def block_partitions(seq):
    if not seq:
        yield []
        return
    for grouping in block_partitions(seq[1:]):
        yield [[seq[0]]]+grouping
        for i in range(len(grouping)):
            yield grouping[:i]+[[seq[0]]+grouping[i]]+grouping[i+1:]

def group_hashes():
    """All set partitions, not merely contiguous cuts; group order canonical/reversed."""
    p=[s.encode() for s in parts()]
    for groups in block_partitions(list(range(7))):
        if len(groups)<2:continue
        groups=sorted((sorted(g) for g in groups),key=lambda g:g[0])
        ds=[sha(b''.join(p[i] for i in g)) for g in groups]
        for reverse in (False,True):
            digests=ds[::-1] if reverse else ds
            for form in ('hex','raw'):
                pieces=[d.hex().encode() if form=='hex' else d for d in digests]
                for join in ('concat','interleave'):
                    body=b''.join(pieces) if join=='concat' else weave(pieces)
                    label=f'groups={groups}/reverse={reverse}/{form}/{join}'
                    for outer,pw in forms(body):yield label+'/'+outer,pw

def selected_hashes():
    """All ordered subsets of >=2 original parts; every selected part hashed first."""
    ds=[sha(p.encode()) for p in parts()]
    for k in range(2,8):
        for ids in itertools.permutations(range(7),k):
            for form in ('hex','raw'):
                pieces=[ds[i].hex().encode() if form=='hex' else ds[i] for i in ids]
                for join in ('concat','interleave'):
                    body=b''.join(pieces) if join=='concat' else weave(pieces)
                    for outer,pw in forms(body):yield f'parts={ids}/{form}/{join}/{outer}',pw

def selective_hashes():
    """Keep order, hash some operands and leave the others literal."""
    families={'phase3':parts(),'phase3.2':['jacquefresco','giveitjustonesecond','heisenbergsuncertaintyprinciple']}
    for family,p in families.items():
        for mask in range(1,(1<<len(p))-1):
            for form in ('hex','raw'):
                pieces=[]
                for i,s in enumerate(p):
                    b=s.encode()
                    if mask>>i&1:b=sha(b).hex().encode() if form=='hex' else sha(b)
                    pieces.append(b)
                for join in ('concat','interleave'):
                    body=b''.join(pieces) if join=='concat' else weave(pieces)
                    for outer,pw in forms(body):yield f'{family}/mask={mask}/{form}/{join}/{outer}',pw

def scoped_commands():
    """Distinct first-hint/answer operands, two SHA scopes, and ENTER at scope boundaries."""
    firsts={
        'poster-text':'GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe',
        'poster-url':'gsmg.io/theseedisplanted',
        'phase1-answer':'theflowerblossomsthroughwhatseemstobeaconcretesurface',
        'first-decoded-instruction':'matrixsumlist'}
    answers={f'phase3-part-{i+1}':s for i,s in enumerate(parts())}
    answers.update({'phase3.2-answer':'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple',
                    'last-before-choice':'theproblemischoice',
                    'last-before-doors':'andtheanomalyrevealedasbothbeginningandend',
                    'last-before-archi':'oneforonefourforone',
                    'literal-answer':'thispassword',
                    'ownership':(ROOT/'derived/checkerboard-plaintext.txt').read_text().strip()})
    for name,values in [('row',[sum(c in 'KB' for c in row) for row in GRID]),
                        ('column',[sum(GRID[r][c] in 'KB' for r in range(14)) for c in range(14)])]:
        for sep in ('',',',' '):answers[f'{name}-sums/{sep!r}']=sep.join(map(str,values))
    for fn,f in firsts.items():
        for an,a in answers.items():
            for form in ('hex','raw'):
                H=(lambda b:sha(b).hex().encode()) if form=='hex' else sha
                for end in (b'',b'\n',b'\r\n'):
                    F,A=f.encode(),a.encode()
                    recipes={
                        'H(F)||H(A+enter)':H(F)+H(A+end),
                        'H(A+enter)||H(F)':H(A+end)+H(F),
                        'H(F||H(A)+enter)':H(F+H(A)+end),
                        'H(H(F)||A+enter)':H(H(F)+A+end),
                        'H(A||H(F)+enter)':H(A+H(F)+end),
                        'H(H(A)||F+enter)':H(H(A)+F+end),
                        'H(F)||H(A)||enter':H(F)+H(A)+end,
                        'H(A)||H(F)||enter':H(A)+H(F)+end}
                    for recipe,pw in recipes.items():
                        label=f'first={fn}/answer={an}/{form}/enter={end!r}/{recipe}'
                        # Already-hashed forms are passed to EVP verbatim, or explicitly rehashed.
                        yield label,pw
                        if recipe.startswith('H(F)||') or recipe.startswith('H(A') and '||H(F)' in recipe:
                            yield label+'/outer-hex',sha(pw).hex().encode()

def xor_selection():
    """Seven original parts, not the four whole-stage answers from the old XOR test."""
    ds=[sha(p.encode()) for p in parts()]
    for mask in range(1,128):
        if mask.bit_count()<2:continue
        selected=[ds[i] for i in range(7) if mask>>i&1]
        n=0
        for d in selected:n^=int.from_bytes(d,'big')
        b=n.to_bytes(32,'big')
        for outer,pw in forms(b):yield f'subset-mask={mask}/xor/{outer}',pw
        yield f'subset-mask={mask}/xor/hex',b.hex().encode()

def decrypt(raw,pw):
    # Last-block check uses K only: IV is irrelevant at block 5 and later.
    key=sha(pw+raw[8:16]);ct=raw[16:]
    tail=AES.new(key,AES.MODE_ECB).decrypt(ct[-16:])
    tail=bytes(a^b for a,b in zip(tail,ct[-32:-16]))
    pad=tail[-1]
    if not 1<=pad<=16 or tail[-pad:]!=bytes([pad])*pad:return None
    iv=sha(key+pw+raw[8:16])[:16]
    return AES.new(key,AES.MODE_CBC,iv).decrypt(ct)[:-pad]

def payload_candidates(p):
    """Hypotheses include a hex scalar, two raw scalar shares, or hash(answer)."""
    yield 'sha256-plaintext',int.from_bytes(sha(p),'big')
    if p.strip()!=p:yield 'sha256-stripped-plaintext',int.from_bytes(sha(p.strip()),'big')
    for m in re.finditer(rb'(?<![0-9a-fA-F])[0-9a-fA-F]{64}(?![0-9a-fA-F])',p):
        h=m.group();yield 'hex64',int(h,16)
        a,b=int(h[:32],16),int(h[32:],16)
        for label,d in [('sum',a+b),('difference',a-b),('xor',a^b),('product',a*b)]:
            yield 'hex-half-'+label,d%N
    if len(p)<=79:
        for i in range(len(p)-31):
            for endian in ('big','little'):
                yield f'raw-window/{i}/{endian}',int.from_bytes(p[i:i+32],endian)
        for offset in sorted({0,len(p)-64}):
            if offset<0:continue
            for endian in ('big','little'):
                a=int.from_bytes(p[offset:offset+32],endian);b=int.from_bytes(p[offset+32:offset+64],endian)
                for label,d in [('sum',a+b),('difference',a-b),('xor',a^b),('product',a*b)]:
                    yield f'raw-shares/{offset}/{endian}/{label}',d%N

def controls():
    password=b'scope-control';salt=b'newscope';k,iv=evp(password,salt)
    examples=[f'{123456789:064x}'.encode(),b'0x'+f'{123456789:064x}'.encode()+b'\r\n',
              b'\x00'*31+b'\x01'+b'\x00'*31+b'\x02',
              PrivateKey.from_int(123456789).public_key.format(compressed=False)]
    for p in examples:
        pad=16-len(p)%16;raw=b'Salted__'+salt+AES.new(k,AES.MODE_CBC,iv).encrypt(p+bytes([pad])*pad)
        assert len(raw)==96 and decrypt(raw,password)==p
    assert ('hex64',123456789) in list(payload_candidates(examples[0]))
    assert any(d==3 and 'raw-shares' in label for label,d in payload_candidates(examples[2]))
    assert decrypt(raw,b'wrong-control-password') is None

def main():
    controls()
    OUT.mkdir(exist_ok=True)
    if (OUT/'results.json').exists():raise SystemExit('results.json exists; preserve the previous run first')
    # Do not rerun the 756 contiguous-partition decryptions just completed.
    seen={sha(sha(body).hex().encode()) for _,body in partitions()}
    key_seen=set();stats={};hits=[];structures=[];same_plain={};t=time.monotonic()
    def keycheck(label,d):
        if not 0<d<N or d in key_seen:return
        key_seen.add(d)
        if PrivateKey.from_int(d).public_key.format()==TARGET:
            hits.append(dict(source=label,private_key_hex=f'{d:064x}'))
            print('TARGET MATCH',label,flush=True)
    with (OUT/'padding.jsonl').open('w') as log:
        for family,gen in [('group-partitions',group_hashes),('selected-parts',selected_hashes),
                           ('selective-hashing',selective_hashes),('scoped-commands',scoped_commands),('xor-selection',xor_selection)]:
            counts=Counter();lengths=Counter();maxprint=0;start=time.monotonic()
            for label,pw in gen():
                counts['generated']+=1;fingerprint=sha(pw)
                if fingerprint in seen:counts['duplicate_or_previous']+=1;continue
                seen.add(fingerprint);counts['unique_passwords']+=1
                # Covers SHA256(ans) as a final private scalar, and literal raw/hex digests.
                keycheck(family+'/'+label+'/sha256-password',int.from_bytes(fingerprint,'big'))
                if len(pw)==32:keycheck(family+'/'+label+'/raw-password',int.from_bytes(pw,'big'))
                if re.fullmatch(rb'[0-9a-fA-F]{64}',pw):keycheck(family+'/'+label+'/hex-password',int(pw,16))
                for name,raw in RAW.items():
                    counts['aes_trials']+=1;p=decrypt(raw,pw)
                    if p is None:continue
                    counts['padding_valid']+=1
                    if name!='cosmic-duality':lengths[str(len(p))]+=1
                    ratio=sum(c in (9,10,13) or 32<=c<127 for c in p)/len(p);maxprint=max(maxprint,ratio)
                    rec=dict(family=family,source=label,password_hex=pw.hex(),container=name,
                             plaintext_hex=p.hex(),length=len(p),printable=ratio)
                    log.write(json.dumps(rec)+'\n')
                    for how,d in payload_candidates(p):keycheck(family+'/'+label+'/'+name+'/'+how,d)
                    tags=[]
                    if re.search(rb'[0-9a-fA-F]{64}',p):tags.append('hex64')
                    if ratio>=.85:tags.append('mostly-printable')
                    if p.startswith(b'Salted__'):tags.append('nested-Salted')
                    if len(p) in (33,65):
                        try:PublicKey(p);tags.append('SEC-public-key')
                        except ValueError:pass
                    other=same_plain.get(p)
                    if other and other['container']!=name:tags.append('same-plaintext-in-two-containers')
                    same_plain[p]={'container':name,'source':label}
                    if tags:structures.append({**rec,'tags':tags})
            stats[family]=dict(counts,short_plaintext_lengths=dict(lengths),max_printable=maxprint,seconds=round(time.monotonic()-start,2))
            print(family,json.dumps(stats[family]),flush=True)
    result=dict(families=stats,private_scalars_checked=len(key_seen),target_matches=hits,
                structured_candidates=structures,seconds=round(time.monotonic()-t,2),
                previous_contiguous_partition_passwords_skipped=252)
    (OUT/'results.json').write_text(json.dumps(result,indent=2))
    print('FINAL',json.dumps({k:v for k,v in result.items() if k!='families'}),flush=True)

if __name__=='__main__':main()
