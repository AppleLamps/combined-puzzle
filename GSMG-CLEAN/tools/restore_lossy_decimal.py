"""Exact zero/nine restoration for full ASCII, including whitespace.

An interval contains a possible text iff its lexicographic ASCII successor
does not exceed the upper bound. This only prunes impossible branches.
"""
import bisect
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-14_lossy_hill'
ALLOWED=bytes([9,10,13]+list(range(32,127)))
ALLOWED_SET=set(ALLOWED)


def next_text(lo,length):
    if lo>=1<<(8*length):return None
    b=list(max(lo,0).to_bytes(length,'big'))
    i=next((i for i,v in enumerate(b) if v not in ALLOWED_SET),length)
    if i==length:return lo
    while i>=0:
        j=bisect.bisect_right(ALLOWED,b[i])
        if j<len(ALLOWED):
            return int.from_bytes(bytes(b[:i]+[ALLOWED[j]]+[ALLOWED[0]]*(length-i-1)),'big')
        i-=1
    return None


def recover(residues,node_cap=1000000):
    assert set(residues)<=set('012345678')
    floor=int(residues)
    weights=[9*10**(len(residues)-i-1) for i,c in enumerate(residues) if c=='0']
    ceiling=floor+sum(weights)
    tail=[0]*(len(weights)+1)
    for i in range(len(weights)-1,-1,-1):tail[i]=tail[i+1]+weights[i]
    hits=[];nodes=0
    for length in range(max(1,(floor.bit_length()+7)//8),(ceiling.bit_length()+7)//8+1):
        stack=[(0,floor)]
        while stack:
            i,lo=stack.pop();nodes+=1
            if nodes>node_cap:return dict(complete=False,nodes=nodes,hits=hits)
            nv=next_text(lo,length)
            if nv is None or nv>lo+tail[i]:continue
            if i==len(weights):
                text=lo.to_bytes(length,'big')
                digits=str(lo).zfill(len(residues))
                assert ''.join(str(int(c)%9) for c in digits)==residues
                hits.append(dict(text=text.decode('ascii'),hex=text.hex(),restored_digits=digits))
            else:
                stack.append((i+1,lo+weights[i]));stack.append((i+1,lo))
    return dict(complete=True,nodes=nodes,hits=hits)


def main():
    for text in [b'thispassword',b'lastwordsbeforearchichoice',b'Restore the zeros before deciding that this is not a message.\n']:
        original=str(int.from_bytes(text,'big'))
        residues=''.join(str(int(c)%9) for c in original).zfill(len(original)+3)
        r=recover(residues)
        assert r['complete'] and any(x['hex']==text.hex() for x in r['hits'])
    records=[];inputs=[]
    p=OUT/'pair_survivors.jsonl'
    if p.exists():
        for line in p.read_text().splitlines():
            r=json.loads(line);inputs.append(('exhaustive_pairs',r,r['residues']))
    # Bounded existing 3x3 keys, plus source-derived Beaufort keys, now checked
    # with selective 0/9 restoration rather than a single one-based numeral.
    q=ROOT/'runs/2026-09-13_dbbi_accounting/reserved_e_results.json'
    for i,r in enumerate(json.loads(q.read_text())):
        if r['modulus']==9:inputs.append(('corrected_3x3',i,''.join(str(v) for v in r['residues'])))
    for i,r in enumerate(json.loads((ROOT/'runs/2026-09-13_prime_control_faed/outputs.json').read_text())):
        if r['modulus']==9:inputs.append(('prime_sum_beaufort',i,''.join(str(int(c)%9) for c in r['digits'])))
    seen={}
    for source,model,residues in inputs:
        if residues not in seen:seen[residues]=dict(residues=residues,models=[],**recover(residues))
        seen[residues]['models'].append(dict(source=source,model=model))
    records=list(seen.values())
    summary=dict(source_models=len(inputs),unique_residue_streams=len(records),
                 complete_searches=sum(r['complete'] for r in records),incomplete_searches=sum(not r['complete'] for r in records),
                 interval_nodes=sum(r['nodes'] for r in records),full_ascii_recoveries=sum(len(r['hits']) for r in records),controls_passed=3)
    (OUT/'restoration_results.json').write_text(json.dumps(records,indent=2))
    (OUT/'restoration_summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
