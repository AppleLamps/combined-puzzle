"""Rank new board outputs for inspection; no substitution solving or AES rerun."""
import heapq,json,re,sys,time
from pathlib import Path
import numpy as np
from mapping_boards import mapping_candidates,board_candidates,OUT
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'mywork2'))
from subsolve import score_arr

def score(b):
    letters=re.sub(rb'[^a-z]',b'',b.lower())
    if len(letters)<4:return -100
    x=np.frombuffer(letters,dtype=np.uint8).astype(np.int64)-97
    return float(score_arr(x)/(len(x)-3))

def main():
    dest=OUT/'language-ranking.json'
    if dest.exists():raise SystemExit('ranking exists')
    start=time.monotonic();heaps={};counts={}
    for family,gen in [('digit-map',mapping_candidates),('boards',board_candidates)]:
        counts[family]=0
        for label,b in gen():
            if not label.endswith('upper'):continue
            run='r1' if '/r1/' in label else 'r2' if '/r2/' in label else None
            if run is None:continue
            counts[family]+=1;key=family+'/'+run;h=heaps.setdefault(key,[])
            item=(score(b),label,b.decode('ascii'))
            if len(h)<8:heapq.heappush(h,item)
            elif item[0]>h[0][0]:heapq.heapreplace(h,item)
    result=dict(scored=counts,seconds=round(time.monotonic()-start,2),
        note='Mean interpolated English character-4-gram log score from existing local model. Ranking only; not a language identification or proof of a plaintext.',
        top={key:[dict(score=s,source=l,text=b) for s,l,b in sorted(h,reverse=True)] for key,h in heaps.items()})
    dest.write_text(json.dumps(result,indent=2))
    print(json.dumps(dict(scored=counts,seconds=result['seconds'],best={key:rows[:2] for key,rows in result['top'].items()})),flush=True)

if __name__=='__main__':main()
