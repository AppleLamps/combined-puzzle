from reconstruct import *
import itertools
im=Image.open(R/'inputs/puzzle.png').convert('RGB');pal={(0,0,0):'K',(255,255,255):'W',(63,72,204):'B',(255,242,0):'Y',(254,254,254):'F'}
grid=[]
for r in range(14):
    row=[]
    for c in range(14):
        pix=im.crop((75*c,75*r,min(75*(c+1),im.width),75*(r+1))).getdata()
        row.append(pal[collections.Counter(pix).most_common(1)[0][0]])
    grid.append(row)
coords=[];r=c=0;direction=0;steps=[(1,0),(0,1),(-1,0),(0,-1)];seen=set()
for i in range(196):
    coords.append((r,c));seen.add((r,c));dr,dc=steps[direction];nr,nc=r+dr,c+dc
    if not(0<=nr<14 and 0<=nc<14) or (nr,nc) in seen:direction=(direction+1)%4;dr,dc=steps[direction]
    r,c=r+dr,c+dc
assert len(set(coords))==196
bits=''.join('1' if grid[r][c] in 'KB' else '0' for r,c in coords)
url=bytes(int(bits[i:i+8],2) for i in range(0,192,8)).decode();assert url=='gsmg.io/theseedisplanted' and bits[192:]=='0000'
events=[dict(index=i,row=r,col=c,color=grid[r][c],byte=i//8+1,bit=i%8) for i,(r,c) in enumerate(coords) if grid[r][c] in 'BYF']
colored=[x for x in events if x['color']!='F'];assert len(colored)==24 and all(x['bit']==7 for x in colored)
primes=[x for x in range(2,100) if isprime(x)]
sums={c:sum(primes[i] for i,x in enumerate(colored) if x['color']==c) for c in ['B','Y']}
branches=[]
for p in ps:
    pattern=''.join('Y' if t=='be' else 'B' for i,t in enumerate(p,1) if isprime(i))
    for kept in itertools.combinations(range(25),23):
        col=''.join('Y' if events[i]['color']=='Y' else 'B' for i in kept)
        if col!=pattern:continue
        selected=[events[i] for i in kept]
        branches.append(dict(cells=len(p),omitted=[events[i] for i in range(25) if i not in kept],no_duplicate_byte=len({x['byte'] for x in selected})==len(selected),first23_bytes=sorted(x['byte'] for x in selected)==list(range(1,24))))
assert len(branches)==5
outp=dict(url=url,grid=[''.join(row) for row in grid],counts=dict(collections.Counter(''.join(''.join(row) for row in grid))),events=events,color_prime_sums=sums,parses=branches,information_scope='24 blue/yellow cells are fixed by the least-significant bits of the URL once that marking rule is known. The off-white F is an additional event. Identifying F with blue, omitting two of 25 events, and selecting a preferred branch are hypotheses, not literal source instructions.')
(R/'poster_check.json').write_text(json.dumps(outp,indent=2));print(json.dumps({k:v for k,v in outp.items() if k not in ['grid','events']},indent=2))
