import sys, random, re, collections
sys.path.insert(0,'.')
from pools import *
import n2
from n2 import best_cover, sumlists, objs, MAPS
def letters(b): return re.sub('[^a-z]','',b.decode('latin-1').lower())
pt2=open('pt2.bin','rb').read(); pt3=open('pt3.bin','rb').read(); pt32=open('pt32.bin','rb').read()
TEXTS={'arch':open('architect.txt').read(),'pt2':letters(pt2),'pt3':letters(pt3),'intro':letters(pt32[:447]),'riddle':letters(pt32[2143:2292]),
 'chk':'incaseyoumanagetocrackthistheprivatekeysbelongtohalfandbetterhalfandtheyalsoneedfundstolive'}
print({k:len(v) for k,v in TEXTS.items()})
lists={}
for en,M in E.items():
    for ln,S in matrix_lists(M).items(): lists[('poster',en,ln)]=S
for on,s in objs.items():
    for mn,mp in MAPS.items():
        if mn=='b64' and not on.startswith('b64'): continue
        if mn=='bit' and on not in ('ab','enter','top195'): continue
        try: V=[mp(c) for c in s]
        except Exception: continue
        for ln,S in sumlists(V).items(): lists[(on,mn,ln)]=S
seen=set(); LL=[]
for k,S in lists.items():
    t=tuple(S)
    if t in seen or len(S)<6 or len(S)>400: continue
    seen.add(t); LL.append((k,S))
print('distinct lists',len(LL))
def sel(S,X,mode):
    n=len(X); out=[]
    for s in S:
        if mode=='i1': i=s-1
        elif mode=='i0': i=s
        else: i=s%n
        if 0<=i<n: out.append(X[i])
        else: return None
    return ''.join(out)
def stat(pairs,shuffle=False,rng=None):
    best=(0,0,'');n5=0;cnt=0
    for k,S in pairs:
        S2=S[:]
        if shuffle: rng.shuffle(S2)
        for tn,X in TEXTS.items():
            for mode in ('i1','i0','mod'):
                s=sel(S2,X,mode)
                if not s or len(s)<8: continue
                cnt+=1
                cv,lw=best_cover(s)
                if lw>=6: n5+=1
                if (lw,cv)>best[:2]: best=(lw,cv,str(k)+' '+tn+' '+mode+' '+s[:50])
    return cnt,n5,best
print('real',stat(LL))
rng=random.Random(11)
for sd in range(3): print('null',sd,stat(LL,True,rng))
