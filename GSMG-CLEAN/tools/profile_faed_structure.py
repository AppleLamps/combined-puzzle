"""Predeclared structure tests with permutation-family controls; no decryption guesses."""
import hashlib
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-13_faed_structure'

def xlog(x):
    return x*np.log(np.maximum(x,1))

def scores(x):
    n=len(x); counts=np.bincount(x,minlength=9)
    ic=sum(counts*(counts-1))/(n*(n-1))
    # Lag family: all lags 1..60; compare maximum in each permuted input.
    lags=np.array([np.mean(x[:-lag]==x[lag:]) for lag in range(1,61)])
    # Period family: same-symbol probability among pairs in the same residue class.
    periods=[]
    for p in range(2,61):
        bins=np.bincount((np.arange(n)%p)*9+x,minlength=p*9).reshape(p,9)
        sizes=bins.sum(axis=1)
        periods.append(float(np.sum(bins*(bins-1))/np.sum(sizes*(sizes-1))))
    # Adjacency dependence, normalized by the actual joint marginals.
    joint=np.bincount(9*x[:-1]+x[1:],minlength=81).reshape(9,9)
    mi=float((xlog(joint).sum()-xlog(joint.sum(0)).sum()-xlog(joint.sum(1)).sum()+xlog(np.array(n-1)))/(n-1))
    cumulative=np.vstack((np.zeros(9,dtype=int),np.eye(9,dtype=int)[x].cumsum(0)))
    cuts=np.arange(40,n-39)
    left=cumulative[cuts]; right=counts-left
    # Likelihood ratio for a frequency change at an unknown cut, without fitting
    # a different alphabet or normalizing away the source's unequal frequencies.
    g=2*(xlog(left).sum(1)+xlog(right).sum(1)-xlog(counts).sum()
         -xlog(cuts)-xlog(n-cuts)+xlog(np.array(n)))
    return dict(lag_max=float(lags.max()),period_max=max(periods),adjacent_mi=mi,split_max=float(g.max())),dict(
        global_ic=float(ic),lag_values=lags.tolist(),period_values=periods,
        best_lag=int(lags.argmax()+1),best_period=int(np.argmax(periods)+2),
        best_split=int(cuts[g.argmax()]),split_values=g.tolist())

def main():
    OUT.mkdir(exist_ok=True)
    path=ROOT/'data/FAED_570.txt'; s=path.read_text().strip()
    x=np.array([ord(c)-97 for c in s]); count=np.bincount(x,minlength=9)
    manifest=dict(input_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),samples=1000,seed=913263,
                  families=['maximum equality at lags 1..60','maximum residue-class IC for periods 2..60',
                            'adjacent-symbol mutual information','maximum symbol-frequency split with >=40 symbols each side'],
                  null='Uniform permutation of original characters, preserving all nine symbol counts',
                  decision='Empirical p=(1+controls>=observed)/(1001); four-family Bonferroni threshold .0125',
                  limitation='Null results do not exclude encryption or long periods; positive results do not identify a cipher')
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
    observed,detail=scores(x); rng=np.random.default_rng(manifest['seed'])
    controls={k:[] for k in observed}
    for _ in range(manifest['samples']):
        sample,_=scores(rng.permutation(x))
        for k,v in sample.items():controls[k].append(v)
    result={k:dict(observed=v,p=(1+sum(z>=v for z in controls[k]))/1001,
                   control_median=float(np.median(controls[k])),control_99=float(np.quantile(controls[k],.99))) for k,v in observed.items()}
    # Controls must demonstrate detection power for deliberately strong examples.
    pc_rng=np.random.default_rng(456)
    planted={'paired_symbols':np.repeat(pc_rng.integers(0,9,285),2),
             'period19':np.resize(pc_rng.integers(0,9,19),570),
             'frequency_change':np.concatenate((pc_rng.integers(0,4,285),pc_rng.integers(4,9,285)))}
    planted_scores={k:scores(v)[0] for k,v in planted.items()}
    assert planted_scores['paired_symbols']['adjacent_mi']>max(controls['adjacent_mi'])
    assert planted_scores['period19']['lag_max']>max(controls['lag_max'])
    assert planted_scores['period19']['period_max']>max(controls['period_max'])
    assert planted_scores['frequency_change']['split_max']>max(controls['split_max'])
    summary=dict(length=len(s),counts=dict(zip('abcdefghi',map(int,count))),tests=result,
                 detail=detail,planted_controls=planted_scores,all_controls_passed=True)
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2))
    (OUT/'permutation_scores.json').write_text(json.dumps(controls))
    print(json.dumps({k:v for k,v in summary.items() if k not in ('detail','planted_controls')}|
                     {'best_lag':detail['best_lag'],'best_period':detail['best_period'],'best_split':detail['best_split']},indent=2))

if __name__=='__main__':main()
