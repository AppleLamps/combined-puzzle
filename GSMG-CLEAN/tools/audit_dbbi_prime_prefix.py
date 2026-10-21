"""Verify the old remove-g claim with a predeclared small transformation family."""
import hashlib
import json
import random
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-13_dbbi_prime_prefix'
S=(ROOT/'data/DBBI_91.txt').read_text().strip()
PRIMES=[p for p in range(2,101) if all(p%d for d in range(2,int(p**.5)+1))]
# Include every possible single-letter deletion except b (which erases the measured marker), plus identity.
FAMILY=['']+list('acdefghi')

def score(s, deleted):
    positions=[i+1 for i,c in enumerate(s.replace(deleted,'') if deleted else s) if c=='b']
    run=0
    for a,b in zip(positions,PRIMES):
        if a!=b:
            break
        run+=1
    return run,positions

def best(s):
    return max(score(s,d)[0] for d in FAMILY)

def main():
    OUT.mkdir(exist_ok=False)
    assert score('abbab', '')[0]==3
    real={d or 'identity':dict(prefix_count=score(S,d)[0],positions=score(S,d)[1]) for d in FAMILY}
    threshold=best(S)
    assert real['g']['prefix_count']==9 and real['identity']['prefix_count']==5
    N=20000
    manifest=dict(input_sha256=hashlib.sha256(S.encode()).hexdigest(),family=FAMILY,
                  statistic='maximum consecutive initial b positions equal to primes across identity/all single-letter deletions',
                  iterations=N,seed=913755,conditional_prefix_length=13,
                  rationale='The claim and deletion g were already known. Include other deletions in the null maximum. '
                            'Conditional control preserves the first 13 source characters, including the known first five prime b positions.',
                  limitation='This does not correct for every historical transform, marker choice, or hypothesis searched.')
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
    rng=random.Random(manifest['seed'])
    results={}
    for name,fixed in [('whole_shuffle',0),('prefix13_fixed',13)]:
        hist=Counter()
        tail=list(S[fixed:])
        for _ in range(N):
            rng.shuffle(tail)
            hist[best(S[:fixed]+''.join(tail))]+=1
        k=sum(v for s,v in hist.items() if s>=threshold)
        results[name]=dict(histogram=dict(sorted(hist.items())),at_least_real=k,trials=N,
                           plus_one_tail_fraction=(k+1)/(N+1))
    result=dict(real=real,real_max=threshold,controls=results,
                status='Verified old clue; statistical comparison is restricted to the stated nulls. No plaintext or password derived.')
    (OUT/'results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
