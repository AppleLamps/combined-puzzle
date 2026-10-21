"""Bounded genesis transaction slices as passwords, scalars, or AES key/IV.
Primary source: https://raw.githubusercontent.com/bitcoin/bitcoin/master/src/kernel/chainparams.cpp
No solved-stage decrypts. Run: python review_leads/genesis_slices.py
"""
import json,re,time
from collections import Counter
from pathlib import Path
from Crypto.Cipher import AES
from coincurve import PrivateKey
from hash_scope import sha,RAW,N,TARGET,decrypt,payload_candidates
from binary_envelopes import structures,old_candidates
OUT=Path(__file__).resolve().parent/'genesis_slices'

def sources():
    headline=b'The Times 03/Jan/2009 Chancellor on brink of second bailout for banks'
    pub=bytes.fromhex('04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f')
    sig=bytes.fromhex('04ffff001d0104')+bytes([len(headline)])+headline
    outscript=b'\x41'+pub+b'\xac'
    tx=bytes.fromhex('0100000001')+bytes(32)+bytes.fromhex('ffffffff')+bytes([len(sig)])+sig+bytes.fromhex('ffffffff01')+(5000000000).to_bytes(8,'little')+bytes([len(outscript)])+outscript+bytes(4)
    txid=sha(sha(tx))[::-1]
    assert len(tx)==204 and txid.hex()=='4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b'
    return {'transaction':tx,'txid-displayed':txid,'scriptSig':sig,'output-script':outscript,'output-public-key':pub}

def clips(s,cap,widths):
    # Include every bounded prefix/suffix, plus exact-width sliding windows.
    for n in range(1,min(len(s),cap)+1):
        yield f'prefix/{n}',s[:n]
        yield f'suffix/{n}',s[-n:]
    for n in widths:
        for i in range(len(s)-n+1):yield f'window/{i}/{n}',s[i:i+n]

def candidates(src):
    for name,b in src.items():
        for direction,v in [('forward',b),('reverse-bytes',b[::-1])]:
            label=name+'/'+direction
            for how,c in clips(v,64,(32,48,64)):yield label+'/bytes/'+how,c
            h=v.hex()
            for how,c in clips(h,64,(32,64,96,128)):
                yield label+'/hex-lower/'+how,c.encode()
                yield label+'/hex-upper/'+how,c.upper().encode()
                yield label+'/hex-0x/'+how,('0x'+c).encode()
                if len(c)%2==0:yield label+'/hex-decoded/'+how,bytes.fromhex(c)
            for decimal_name,d in [('integer-decimal',str(int.from_bytes(v,'big'))),('hex-digits-only',''.join(x for x in h if x.isdigit()))]:
                for how,c in clips(d,78,(32,64,77,78)):
                    yield label+'/'+decimal_name+'/'+how,c.encode()
                    n=int(c)
                    if n.bit_length()<=256:yield label+'/'+decimal_name+'/integer-bytes/'+how,n.to_bytes(32,'big')

def main():
    OUT.mkdir(exist_ok=True)
    if (OUT/'results.json').exists():raise SystemExit('results already exist')
    start=time.monotonic();src=sources();counts=Counter();hits=[];signals=[];keys=set();seen=set();lengths=Counter()
    (OUT/'sources.json').write_text(json.dumps({n:b.hex() for n,b in src.items()},indent=2))
    old=old_candidates();next(old);previous={sha(pw) for _,pw in old}
    def keycheck(label,d):
        if not 0<d<N or d in keys:return
        keys.add(d);counts['target_point_comparisons']+=1
        if PrivateKey.from_int(d).public_key.format()==TARGET:hits.append(dict(source=label,private_key_hex=f'{d:064x}'))
    def examine(label,name,p,log):
        counts['padding_valid']+=1
        if name!='cosmic-duality':lengths[len(p)]+=1
        row=dict(source=label,container=name,plaintext_hex=p.hex())
        log.write(json.dumps(row)+'\n')
        tags=[kind for kind,_ in structures(p)]
        if p and sum(c in (9,10,13) or 32<=c<127 for c in p)/len(p)>=.85:tags.append('mostly-printable')
        if tags:signals.append(dict(**row,tags=tags))
        for how,d in payload_candidates(p):keycheck(label+'/'+name+'/'+how,d)
    with (OUT/'padding.jsonl').open('w') as log, (OUT/'candidates.jsonl').open('w') as inputs:
        answers={}
        for label,b in candidates(src):answers.setdefault(b,label)
        counts['distinct_answer_bytes']=len(answers)
        for b,label in answers.items():
            inputs.write(json.dumps(dict(source=label,answer_hex=b.hex()))+'\n')
            if len(b)<=32:
                for endian in ('big','little'):keycheck(label+'/raw-scalar/'+endian,int.from_bytes(b,endian))
            if re.fullmatch(rb'(?:0x)?[0-9a-fA-F]{1,64}',b):keycheck(label+'/hex-scalar',int(b,16))
            if re.fullmatch(rb'[0-9]{1,78}',b):keycheck(label+'/decimal-scalar',int(b))
            for how,pw in [('raw',b),('sha256-hex',sha(b).hex().encode()),('sha256-raw',sha(b)),('double-sha256-hex',sha(sha(b)).hex().encode())]:
                fp=sha(pw)
                if fp in seen:continue
                seen.add(fp);keycheck(label+'/'+how+'/sha256-scalar',int.from_bytes(fp,'big'))
                if fp in previous:counts['old_passwords_skipped']+=1;continue
                counts['new_passwords']+=1
                for name,raw in RAW.items():
                    counts['password_aes_trials']+=1;p=decrypt(raw,pw)
                    if p is not None:examine(label+'/'+how,name,p,log)
        # Explicit fixed-width alternative: 32 raw AES key bytes plus 16 IV bytes.
        seen_direct=set()
        for name,b in src.items():
            for direction,v in [('forward',b),('reverse-bytes',b[::-1])]:
                for i in range(len(v)-47):
                    c=v[i:i+48]
                    for how,k,iv in [('key-then-iv',c[:32],c[32:]),('iv-then-key',c[16:],c[:16])]:
                        if (k,iv) in seen_direct:continue
                        seen_direct.add((k,iv));label=f'{name}/{direction}/direct/{i}/{how}'
                        for container,raw in RAW.items():
                            counts['direct_aes_trials']+=1;p=AES.new(k,AES.MODE_CBC,iv).decrypt(raw[16:]);pad=p[-1]
                            if 1<=pad<=16 and p[-pad:]==bytes([pad])*pad:examine(label,container,p[:-pad],log)
    result=dict(**counts,short_lengths=dict(lengths),target_matches=hits,structural_candidates=signals,seconds=round(time.monotonic()-start,2))
    (OUT/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':main()
