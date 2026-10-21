"""Two SHA markers as decrypt-then-hash, plus complete hash-command output bytes.
Consumes saved padding-valid outputs; does not repeat the preceding AES sweep.
"""
from collections import Counter
import json,re,time
from hash_scope import OUT,ROOT,RAW,N,TARGET,PrivateKey,PublicKey,sha,forms,decrypt,payload_candidates
from next_tests import parts,partitions

def main():
    dest=OUT/'followup-results.json'
    if dest.exists():raise SystemExit('followup-results.json exists; preserve it first')
    stats={};structures=[];hits=[];scalars=set();seen=set();start=time.monotonic()
    def keycheck(label,d):
        if not 0<d<N or d in scalars:return
        scalars.add(d)
        if PrivateKey.from_int(d).public_key.format()==TARGET:hits.append(dict(source=label,private_key_hex=f'{d:064x}'))
    def probe(family,label,pw,names,log):
        counts=stats.setdefault(family,Counter())
        for name in names:
            fp=(name,sha(pw))
            if fp in seen:counts['duplicates']+=1;continue
            seen.add(fp);counts['aes_trials']+=1;p=decrypt(RAW[name],pw)
            if p is None:continue
            counts['padding_valid']+=1
            if name!='cosmic-duality':counts[f'short_length_{len(p)}']+=1
            ratio=sum(c in (9,10,13) or 32<=c<127 for c in p)/len(p)
            rec=dict(family=family,source=label,password_hex=pw.hex(),container=name,plaintext_hex=p.hex(),printable=ratio)
            log.write(json.dumps(rec)+'\n')
            tags=[]
            if ratio>=.85:tags.append('mostly-printable')
            if re.search(rb'[0-9a-fA-F]{64}',p):tags.append('hex64')
            if p.startswith(b'Salted__'):tags.append('nested-Salted')
            if len(p) in (33,65):
                try:PublicKey(p);tags.append('SEC-public-key')
                except ValueError:pass
            for how,d in payload_candidates(p):keycheck(family+'/'+label+'/'+name+'/'+how,d)
            if tags:structures.append({**rec,'tags':tags})
    with (OUT/'followup-padding.jsonl').open('w') as log:
        records=[json.loads(line) for line in (OUT/'padding.jsonl').read_text().splitlines()]
        # Include the five saved outputs from the initial contiguous-partition run.
        prior=ROOT/'review_leads/next-partitions-padding.jsonl'
        for line in prior.read_text().splitlines():
            r=json.loads(line);r['family']='initial-contiguous-partitions';records.append(r)
        for i,r in enumerate(records):
            p=bytes.fromhex(r['plaintext_hex']);others=[n for n in RAW if n!=r['container']]
            variants=[('full',p),('stripped',p.strip())]
            if re.fullmatch(rb'(?:0x)?[0-9a-fA-F]{64}',p.strip()):
                variants.append(('hex-decoded',bytes.fromhex(p.strip().decode().removeprefix('0x'))))
            for vn,v in variants:
                for transform,pw in forms(v):
                    probe('decrypt-then-hash',f'prior-record={i}/{r["container"]}/{vn}/{transform}',pw,others,log)
        print('decrypt-then-hash',json.dumps(stats['decrypt-then-hash']),flush=True)

        sources=[(f'part-{i+1}',p.encode()) for i,p in enumerate(parts())]
        sources += [('whole-phase3',''.join(parts()).encode()),
                    ('phase1',b'theflowerblossomsthroughwhatseemstobeaconcretesurface'),
                    ('phase3.2',b'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple'),
                    ('poster',b'GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'),
                    ('matrixsumlist',b'matrixsumlist'),('thispassword',b'thispassword'),
                    ('architect',(ROOT/'derived/architect-text.txt').read_bytes().strip()),
                    ('ownership',(ROOT/'derived/checkerboard-plaintext.txt').read_bytes().strip())]
        sources += list(partitions())
        for label,b in sources:
            for input_end in (b'',b'\n',b'\r\n'):
                h=sha(b+input_end).hex().encode()
                for case,digest in [('lower',h),('upper',h.upper())]:
                    layouts={
                        'LF':digest+b'\n',
                        'CRLF':digest+b'\r\n',
                        'sum-text-stdin':digest+b'  -\n',
                        'sum-binary-stdin':digest+b' *-\n',
                        'reverse-stdin':digest+b' *stdin\n',
                        'stdin-label':b'(stdin)= '+digest+b'\n',
                        'SHA256-label-no-LF':b'SHA256(stdin)= '+digest,
                        'SHA256-label-LF':b'SHA256(stdin)= '+digest+b'\n'}
                    for layout,v in layouts.items():
                        for outer,pw in forms(v):
                            recipe=f'{label}/input-end={input_end!r}/{case}/{layout}/{outer}'
                            probe('command-output-bytes',recipe,pw,list(RAW),log)
                            keycheck(recipe+'/sha256-password',int.from_bytes(sha(pw),'big'))
                            if len(pw)==32:keycheck(recipe+'/raw-password',int.from_bytes(pw,'big'))
                            if re.fullmatch(rb'[0-9a-fA-F]{64}',pw):keycheck(recipe+'/hex-password',int(pw,16))
        print('command-output-bytes',json.dumps(stats['command-output-bytes']),flush=True)
    result=dict(families=stats,source_padding_records=len(records),private_scalars_checked=len(scalars),
                structured_candidates=structures,target_matches=hits,seconds=round(time.monotonic()-start,2))
    dest.write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':main()
