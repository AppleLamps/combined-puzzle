from reconstruct import *
import itertools
textbyte=lambda x:x in [9,10,13] or 32<=x<=126
outputs=[];summary=[]
for mode in ['ring','01','12','22']:
    def add(x,y):return (x+y)%9 if mode=='ring' else (x%3+y%3)%3+3*((x//3+y//3)%3)
    def mul(x,y):
        if mode=='ring':return x*y%9
        b,c=map(int,mode);return ((x%3)*(y%3)-c*(x//3)*(y//3))%3+3*(((x%3)*(y//3)+(x//3)*(y%3)-b*(x//3)*(y//3))%3)
    neg=[next(y for y in range(9) if add(x,y)==0) for x in range(9)]
    models={k:[int(c) for c in v] for k,v in (line.split() for line in (R/f'radix_models_{mode}.txt').read_text().splitlines()) if k!='forward_control'}
    control=json.loads((R/'radix_control.json').read_text());d=control['digits'];models['control2']=[out for i in range(0,570,2) for out in [add(d[i],mul(2,d[i+1])),d[i+1]]]
    for name,v in models.items():
        count=0;hits=[];best=0
        for a,b,c,d in itertools.product(range(9),repeat=4):
            det=add(mul(a,d),neg[mul(b,c)])
            if (det%3==0 if mode=='ring' else det==0):continue
            count+=1;n=0
            for x,y in zip(v[::2],v[1::2]):
                n=n*9+add(mul(a,x),mul(b,y));n=n*9+add(mul(c,x),mul(d,y))
            raw=n.to_bytes((n.bit_length()+7)//8,'big');prefix=next((i for i,x in enumerate(raw) if not textbyte(x)),len(raw));best=max(best,prefix)
            if prefix==len(raw) or raw.startswith(b'Salted__') or len(raw)<=128:
                hits.append(dict(key=[a,b,c,d],hex=raw.hex()))
        if name=='control2':assert any(bytes.fromhex(x['hex']).decode()==control['plaintext'] for x in hits)
        summary.append(dict(mode=mode,name=name,keys=count,full_objects=len(hits),best_prefix=best));outputs.append(dict(mode=mode,name=name,hits=hits))
print(json.dumps(summary,indent=2));(R/'radix2_results.json').write_text(json.dumps(dict(summary=summary,outputs=outputs),indent=2))
