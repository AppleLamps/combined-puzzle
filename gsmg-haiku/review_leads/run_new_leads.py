"""Bounded, reproducible new GSMG hypotheses; never modifies original artifacts.
Run from any directory: python review_leads/run_new_leads.py
Requires the existing environment's pycryptodome. No network calls.
"""
from pathlib import Path
import base64, hashlib, itertools, json, math, re, time
from collections import Counter
from Crypto.Cipher import AES

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
S = ''.join((ROOT/'files/salphaseion-textarea.txt').read_text().split())
R1 = [ord(c)-96 for c in S[:91]]
R2 = [ord(c)-96 for c in S[195:765]]
GRID = '''WWKKWBWWKWKKWY
KKBKWWKKKWBWKK
KKWKKKWBWWKWWK
WKKWBWWWWKKKWK
WBKWWWKKWYWKKW
KWWKKWYWKWYWKK
KWWBKKWWWKWYWW
BKKWFWWWWWKWYW
WWWKKBWKKKKKWB
KKBKKKYWKKWWWK
KKWKWWWYWKKWKK
KKKKWWKWBWKKWW
WBWKKKWKWYWKKW
WKBWKKWKKWBWKK'''.splitlines()
RAW = {n:base64.b64decode((ROOT/'files'/f'{n}.b64').read_bytes())
       for n in ('terminal','salphaseion-short','cosmic-duality')}
RESULT = {}

def sha(b): return hashlib.sha256(b).digest()

def evp(pw,salt):
    a=sha(pw+salt); b=sha(a+pw+salt)
    return a,b[:16]

def test(label, candidates):
    seen=set(); counts=Counter(); hits=[]; best=0; t=time.monotonic()
    for source,answer in candidates:
        if isinstance(answer,str): answer=answer.encode()
        if answer in seen: continue
        seen.add(answer); pw=sha(answer).hex().encode()
        for name,raw in RAW.items():
            counts['decryptions']+=1
            key,iv=evp(pw,raw[8:16]); ct=raw[16:]
            tail=AES.new(key,AES.MODE_CBC,ct[-32:-16]).decrypt(ct[-16:])
            pad=tail[-1]
            if not 1<=pad<=16 or tail[-pad:]!=bytes([pad])*pad: continue
            counts['padding_valid']+=1
            plain=AES.new(key,AES.MODE_CBC,iv).decrypt(ct)[:-pad]
            ratio=sum(c in (9,10,13) or 32<=c<127 for c in plain)/len(plain)
            best=max(best,ratio)
            # Keep every padding-valid output for binary inspection; do not call it a hit.
            with (OUT/f'{label}-padding.jsonl').open('a') as f:
                f.write(json.dumps(dict(source=source,answer_hex=answer.hex(),container=name,
                                       plaintext_hex=plain.hex(),printable=ratio))+'\n')
            if ratio>=.85 or plain.startswith((b'Salted__',b'\x1f\x8b',b'PK\x03\x04')):
                hits.append(dict(source=source,container=name,answer_hex=answer.hex(),plaintext_hex=plain.hex()))
    result=dict(unique_answers=len(seen),**counts,best_printable=best,
                structured_candidates=hits,seconds=round(time.monotonic()-t,2))
    RESULT[label]=result; print(label,json.dumps(result),flush=True)

def primes(n):
    return [x for x in range(2,n) if all(x%d for d in range(2,math.isqrt(x)+1))]

def spiral():
    r=c=0; dr,dc=1,0; used=set(); out=[]
    for _ in range(196):
        out.append((r,c)); used.add((r,c))
        rr,cc=r+dr,c+dc
        if not(0<=rr<14 and 0<=cc<14) or (rr,cc) in used: dr,dc=-dc,dr
        r,c=r+dr,c+dc
    return out

def weighted():
    pp=primes(1300); orders={
        'row':[(r,c) for r in range(14) for c in range(14)],
        'column':[(r,c) for c in range(14) for r in range(14)], 'spiral':spiral()}
    masks={'Y':{'Y'},'B':{'B'},'YB':{'Y','B'},'KB':{'K','B'},
           'WYF':{'W','Y','F'},'notYB':{'K','W','F'},'all':set('KWBYF')}
    matches=[]; streams={''.join(map(str,R1)):'r1',''.join(map(str,R2)):'r2'}
    for on,path in list(orders.items()):
        for rev in (False,True):
            pth=path[::-1] if rev else path
            for weight in ('nth-prime','prime-position','prime-rank'):
                for mn,mask in masks.items():
                    m=[[0]*14 for _ in range(14)]
                    for i,(r,c) in enumerate(pth,1):
                        v=pp[i-1] if weight=='nth-prime' else (i if i in pp else 0)
                        if weight=='prime-rank': v=pp.index(i)+1 if i in pp else 0
                        if GRID[r][c] in mask: m[r][c]=v
                    rows=list(map(sum,m)); cols=[sum(m[r][c] for r in range(14)) for c in range(14)]
                    lists={'rows':rows,'cols':cols,'rows-cols':rows+cols,'cols-rows':cols+rows,
                           'interleave':list(itertools.chain.from_iterable(zip(rows,cols))),
                           'row+col':[a+b for a,b in zip(rows,cols)],
                           'row-col':[a-b for a,b in zip(rows,cols)]}
                    for ln,nums in lists.items():
                        for lr in (False,True):
                            ns=nums[::-1] if lr else nums
                            lab=f'{on}/reverse={rev}/{weight}/{mn}/{ln}/reverse-list={lr}'
                            for sep in ('',',',' '):
                                val=sep.join(map(str,ns)); yield lab+f'/sep={sep!r}',val
                            digits=''.join(map(str,ns))
                            for variant in (digits,digits.replace('0',''),digits[::-1],digits.replace('0','')[::-1]):
                                if variant in streams: matches.append([lab,streams[variant]])
    RESULT['weighted_exact_stream_matches']=matches

def decimal_views(label,digits):
    yield label+'/digits',digits
    num=int(digits); b=num.to_bytes(max(1,(num.bit_length()+7)//8),'big')
    # Raw reconstructed byte string is a distinct candidate, even when not English.
    yield label+'/decimal-to-bytes',b
    if len(digits)%2==0:
        yield label+'/two-digit-bytes',bytes(int(digits[i:i+2]) for i in range(0,len(digits),2))

def numeric_key():
    keys={'r1':R1,'r1-reversed':R1[::-1],
          'poster-row-sums':[sum(c in 'KB' for c in row) for row in GRID],
          'poster-col-sums':[sum(GRID[r][c] in 'KB' for r in range(14)) for c in range(14)]}
    keys.update({k+'-decimal-digits':[int(c) for c in ''.join(map(str,v))]
                 for k,v in list(keys.items()) if k.startswith('poster')})
    for kn,key in keys.items():
        for phase in range(len(key)):
            seed=key[phase:]+key[:phase]
            for mod in (9,10):
                for mode in ('repeat','chain-add'):
                    stream=seed[:]
                    while len(stream)<570:
                        i=len(stream)-len(seed)
                        stream.append(seed[len(stream)%len(seed)] if mode=='repeat' else (stream[i]+stream[i+1])%mod)
                    for rev,data in [('fwd',R2),('rev',R2[::-1])]:
                        for op in ('subtract-key','key-subtract','add'):
                            vals=[((a-b) if op=='subtract-key' else (b-a) if op=='key-subtract' else (a+b))%mod
                                  for a,b in zip(data,stream)]
                            label=f'{kn}/phase={phase}/mod={mod}/{mode}/{rev}/{op}'
                            digits=''.join(map(str,vals))
                            yield from decimal_views(label,digits)

def constraints():
    out={}; pp=primes(1000000)
    for name,data in [('r1',R1),('r2',R2)]:
        for rev,d in [('fwd',data),('rev',data[::-1])]:
            digits=''.join(map(str,d)); value=int(digits); factors=[]
            for p in pp:
                e=0
                while value%p==0: value//=p; e+=1
                if e: factors.append((p,e))
                if value==1:break
            reach={0}
            for i in range(len(digits)):
                if i in reach:
                    for p in pp[:26]:
                        if digits.startswith(str(p),i):reach.add(i+len(str(p)))
            out[f'{name}/{rev}']=dict(factors_below_million=factors,remaining_decimal_digits=len(str(value)),
                                     prime_alphabet_parse=len(digits) in reach,
                                     farthest_parse=max(reach))
    RESULT['constraints']=out;print('constraints',json.dumps(out),flush=True)

if __name__=='__main__':
    # The output files are specific to this new experiment. Refuse to append duplicate runs.
    if (OUT/'results.json').exists(): raise SystemExit('results.json already exists; preserve it before rerunning')
    constraints()
    test('weighted-primes',weighted())
    test('numeric-key',numeric_key())
    (OUT/'results.json').write_text(json.dumps(RESULT,indent=2))
