"""Two CBC passes, one outer Salted__ header, PKCS7 only before inner pass.
Run: python review_leads/double_cbc.py
This explicitly differs from two independently padded Salted__ envelopes.
"""
import json,time
from collections import Counter
from pathlib import Path
from Crypto.Cipher import AES
from coincurve import PrivateKey
from hash_scope import parts,partitions,sha,evp,RAW,N,TARGET
from binary_envelopes import structures
OUT=Path(__file__).resolve().parent/'double_cbc'

def passwords():
    bodies=[p.encode() for p in parts()]+[b for _,b in partitions()]
    bodies.extend([b'causality',b'theflowerblossomsthroughwhatseemstobeaconcretesurface',
        b'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple',
        ''.join(parts()).encode(),b'GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe',
        b'gsmg.io/theseedisplanted',b'matrixsumlist',b'lastwordsbeforearchichoice',
        b'thispassword',b'ourfirsthintisyourlastcommand',b'enter',b'yinyang',
        b'oneforonefourforone',b'theproblemischoice'])
    return sorted({p for b in bodies for p in (b,sha(b),sha(b).hex().encode())})

def controls():
    p=bytes(range(64));pad=p+bytes([16])*16
    for si in (b'innerslt',b'outerslt',b''):
        ki,vi=evp(b'inner',si);ko,vo=evp(b'outer',b'outerslt')
        inner=AES.new(ki,AES.MODE_CBC,vi).encrypt(pad)
        outer=b'Salted__outerslt'+AES.new(ko,AES.MODE_CBC,vo).encrypt(inner)
        assert len(outer)==96
        mid=AES.new(ko,AES.MODE_CBC,vo).decrypt(outer[16:])
        tail=bytes(a^b for a,b in zip(AES.new(ki,AES.MODE_ECB).decrypt(mid[-16:]),mid[-32:-16]))
        assert tail==bytes([16])*16
        assert AES.new(ki,AES.MODE_CBC,vi).decrypt(mid)[:-16]==p

def main():
    controls();OUT.mkdir(exist_ok=True)
    if (OUT/'results.json').exists():raise SystemExit('results already exist')
    pws=passwords();start=time.monotonic();counts=Counter();lengths=Counter();hits=[];matches=[]
    (OUT/'passwords.json').write_text(json.dumps([p.hex() for p in pws]))
    with (OUT/'padding.jsonl').open('w') as log:
        for name,other in [('terminal','salphaseion-short'),('salphaseion-short','terminal')]:
            blob=RAW[name]
            inner=[]
            for mode,salt in [('same',blob[8:16]),('other',RAW[other][8:16]),('none',b'')]:
                for i,pw in enumerate(pws):
                    k,iv=evp(pw,salt);inner.append((mode,i,k,iv,AES.new(k,AES.MODE_ECB)))
            for oi,pw in enumerate(pws):
                k,iv=evp(pw,blob[8:16]);mid=AES.new(k,AES.MODE_CBC,iv).decrypt(blob[16:]);counts['outer_decryptions']+=1
                prev=int.from_bytes(mid[-32:-16],'big');last=mid[-16:]
                for mode,ii,ki,vi,ecb in inner:
                    tail=(int.from_bytes(ecb.decrypt(last),'big')^prev).to_bytes(16,'big');counts['pair_trials']+=1
                    pad=tail[-1]
                    if not 1<=pad<=16 or tail[-pad:]!=bytes([pad])*pad:continue
                    p=AES.new(ki,AES.MODE_CBC,vi).decrypt(mid)[:-pad];counts['padding_valid']+=1;lengths[len(p)]+=1
                    row=dict(container=name,outer_password_index=oi,inner_password_index=ii,inner_salt=mode,plaintext_hex=p.hex())
                    log.write(json.dumps(row)+'\n')
                    for kind,b in structures(p):hits.append(dict(**row,kind=kind,payload_hex=b.hex()))
                    vals={int.from_bytes(sha(p),'big'),int.from_bytes(sha(p.strip()),'big')}
                    for b in (p[:32],p[-32:]):
                        for endian in ('big','little'):vals.add(int.from_bytes(b,endian))
                    for d in vals:
                        if not 0<d<N:continue
                        counts['target_point_comparisons']+=1
                        if PrivateKey.from_int(d).public_key.format()==TARGET:matches.append(dict(**row,private_key_hex=f'{d:064x}'))
            print(json.dumps(dict(completed=name,**counts)),flush=True)
    result=dict(unique_passwords=len(pws),**counts,short_lengths=dict(lengths),structural_candidates=hits,
                target_matches=matches,seconds=round(time.monotonic()-start,2))
    (OUT/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':main()
