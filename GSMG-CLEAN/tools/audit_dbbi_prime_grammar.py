"""Test a complete prime-slot grammar rather than promoting an initial prefix."""
import hashlib
import json
import random
from functools import lru_cache
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-13_dbbi_prime_prefix'
S=(ROOT/'data/DBBI_91.txt').read_text().strip()
PRIMES={n for n in range(2,100) if all(n%d for d in range(2,int(n**.5)+1))}

def parse(s,suffix):
    @lru_cache(None)
    def walk(i,slot):
        if i==len(s):
            return ((),)
        if slot in PRIMES:
            choices=[t for t in ('b','b'+suffix) if s.startswith(t,i)]
        else:
            choices=[s[i]]
        return tuple(((slot,i,t,slot in PRIMES),)+tail for t in choices
                     for tail in walk(i+len(t),slot+1))
    return walk(0,1)

def main():
    manifest=dict(model='Prime-numbered logical cells must be b or b+one fixed suffix; other cells consume one character.',
                  suffix_family=list('abcdefghi'),control='First 13 input characters fixed; shuffle remaining multiset.',
                  samples=5000,seed=9132027,
                  input_sha256=hashlib.sha256(S.encode()).hexdigest(),
                  caveat='The b/be construction is an existing lead. This compares its full-coverage property, not its proposed numerical signs or Hill reading.')
    (OUT/'grammar_manifest.json').write_text(json.dumps(manifest,indent=2))
    results={suffix:parse(S,suffix) for suffix in 'abcdefghi'}
    assert [suffix for suffix,ps in results.items() if ps]==['e']
    assert sorted(len(p) for p in results['e'])==[83,84]
    for p in results['e']:
        assert ''.join(t for slot,i,t,prime in p)==S
    rng=random.Random(manifest['seed']); tail=list(S[13:]); hits=0
    for _ in range(manifest['samples']):
        rng.shuffle(tail)
        sample=S[:13]+''.join(tail)
        hits+=any(parse(sample,suffix) for suffix in 'abcdefghi')
    summaries=[]
    for p in results['e']:
        summaries.append(dict(cells=len(p),prime_cells=sum(pr for _,_,_,pr in p),
                              b_prime=sum(pr and t=='b' for _,_,t,pr in p),
                              be_prime=sum(pr and t=='be' for _,_,t,pr in p),parse=p))
    result=dict(qualifying_suffixes=['e'],parses=summaries,
                conditional_controls_with_any_complete_parse=hits,controls=manifest['samples'],
                status='Full DBBI structural fit verified; arithmetic meaning and subsequent password remain unknown.')
    (OUT/'grammar_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({**result,'parses':[{k:v for k,v in p.items() if k!='parse'} for p in summaries]},indent=2))
    a,b=results['e']
    different=[(x,y) for x,y in zip(a,b) if x!=y]
    print('first differing cells:',different[:3])

if __name__=='__main__':
    main()
