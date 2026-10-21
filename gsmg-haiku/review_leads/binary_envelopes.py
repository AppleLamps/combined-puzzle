"""New binary-output hypothesis using the old pool, not an English-output replay.
Detect nested raw/base64 containers, 64-byte seeds, binary wallets, compact SEC1,
and validated compressed streams. Also examine the full outer plaintext for
no-padding and zero-padding variants. No original solved containers are opened.
"""
import base64,gzip,json,re,sys,time,zlib
from collections import Counter
from pathlib import Path
from Crypto.Cipher import AES
from coincurve import PublicKey,PrivateKey
from hash_scope import ROOT,RAW,N,TARGET,sha,evp
OUT=Path(__file__).resolve().parent/'binary_envelopes'

def old_candidates():
    # Import the shared constructor explicitly; importing it cannot run a search.
    sys.path.insert(0, str(ROOT))
    from mywork.candidate_pool import build_pool, trans
    pool = build_pool(ROOT)
    yield len(pool)
    for s in sorted(pool):
        for how, pw in trans(s):
            yield {'answer': s, 'transform': how}, pw


def structures(p,allow_seed=True):
    out=[]
    if allow_seed and len(p)==64:out.append(('raw64',p))
    pos=p.find(b'Salted__')
    if pos>=0:
        for length in range(32,len(p)-pos+1,16):out.append((f'nested-Salted/offset={pos}/length={length}',p[pos:pos+length]))
    q=p.strip()
    if q.startswith(b'U2FsdGVkX1'):
        try:
            b=base64.b64decode(q,validate=True)
            if b.startswith(b'Salted__') and len(b)>=32 and len(b)%16==0:out.append(('nested-base64',b))
        except ValueError:pass
    if len(p)==78 and p[:4] in (bytes.fromhex('0488ade4'),bytes.fromhex('04358394')) and p[45]==0:
        d=int.from_bytes(p[46:78],'big')
        if 0<d<N:out.append(('serialized-xprv',p))
    if len(p)==78 and p[:4] in (bytes.fromhex('0488b21e'),bytes.fromhex('043587cf')):
        try:PublicKey(p[45:]);out.append(('serialized-xpub',p))
        except ValueError:pass
    # Compact SEC1 shape, omitting named-curve parameters; curve is fixed here.
    if len(p)==77 and p[:7]==bytes.fromhex('304b0201010420') and p[39:44]==bytes.fromhex('a124032200'):
        d=int.from_bytes(p[7:39],'big')
        if 0<d<N and PrivateKey.from_int(d).public_key.format()==p[44:77]:out.append(('compact-SEC1',p))
    if len(p) in (33,65):
        try:PublicKey(p);out.append(('SEC-public-key',p))
        except ValueError:pass
    if re.fullmatch(rb'(?:0x)?[0-9a-fA-F]{64}',q):out.append(('hex64',q))
    if p.startswith(b'\x1f\x8b') or len(p)>1 and p[0]==0x78 and int.from_bytes(p[:2],'big')%31==0:
        try:
            dz=zlib.decompressobj(47);decoded=dz.decompress(p,65536)
            if dz.eof and not dz.unconsumed_tail:out.append(('compressed-validated',decoded))
        except zlib.error:pass
    return out

def encrypt(p,pw,salt=b'newlayer',padding=True):
    k,iv=evp(pw,salt)
    if padding:
        pad=16-len(p)%16;p+=bytes([pad])*pad
    return b'Salted__'+salt+AES.new(k,AES.MODE_CBC,iv).encrypt(p)

def controls():
    secret=(123456789).to_bytes(32,'big');inner=encrypt(secret,b'inner');outer=encrypt(inner,b'outer')
    assert len(inner)==64 and len(outer)==96
    k,iv=evp(b'outer',outer[8:16]);raw=AES.new(k,AES.MODE_CBC,iv).decrypt(outer[16:])
    assert ('nested-Salted/offset=0/length=64',inner) in structures(raw[:-16])
    assert len(encrypt(bytes(range(64))+bytes(16),b'outer',padding=False))==96
    pub=PrivateKey.from_int(123456789).public_key.format()
    der=bytes.fromhex('304b0201010420')+secret+bytes.fromhex('a124032200')+pub
    assert structures(der)==[('compact-SEC1',der)]
    seed=bytes(range(64));assert ('raw64',seed) in structures(seed)
    xprv=bytes.fromhex('0488ade4')+bytes(9)+bytes(range(32))+b'\0'+secret
    assert ('serialized-xprv',xprv) in structures(xprv)
    compressed=gzip.compress(b'control binary payload',mtime=0)
    assert ('compressed-validated',b'control binary payload') in structures(compressed)

def main():
    controls();OUT.mkdir(exist_ok=True)
    if (OUT/'results.json').exists():raise SystemExit('results.json already exists')
    candidates=old_candidates();pool_size=next(candidates);seen=set();counts=Counter();lengths=Counter();hits=[];start=time.monotonic()
    with (OUT/'padding.jsonl').open('w') as log:
        for label,pw in candidates:
            counts['generated_passwords']+=1
            fp=sha(pw)
            if fp in seen:continue
            seen.add(fp)
            for name in ('terminal','salphaseion-short'):
                blob=RAW[name];k,iv=evp(pw,blob[8:16]);p=AES.new(k,AES.MODE_CBC,iv).decrypt(blob[16:]);counts['aes_trials']+=1
                variants=[('outer-no-padding',p)]
                pad=p[-1]
                if 1<=pad<=16 and p[-pad:]==bytes([pad])*pad:
                    unpadded=p[:-pad];variants.append(('outer-PKCS7',unpadded));lengths[len(unpadded)]+=1;counts['padding_valid']+=1
                    log.write(json.dumps(dict(**label,password_hex=pw.hex(),container=name,plaintext_hex=unpadded.hex()))+'\n')
                if p[-16:]==bytes(16):variants.append(('outer-zero-padding-16',p[:64]))
                if p[-2:]==bytes(2):variants.append(('outer-zero-padding-2',p[:78]))
                for mode,b in variants:
                    for kind,payload in structures(b,allow_seed=mode!='outer-no-padding'):
                        hits.append(dict(**label,password_hex=pw.hex(),container=name,outer_mode=mode,kind=kind,payload_hex=payload.hex()))
    result=dict(source_pool_strings=pool_size,unique_passwords=len(seen),**counts,short_lengths=dict(lengths),
                structural_candidates=hits,seconds=round(time.monotonic()-start,2))
    (OUT/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':main()
