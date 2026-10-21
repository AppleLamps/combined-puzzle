from reconstruct import *
import itertools, random, numpy as np
from fractions import Fraction
Q=np.fromfile(R/'quadgrams.bin',dtype=np.float64)
def score(t):
    v=np.frombuffer(t.encode(),dtype=np.uint8).astype(np.int64)-97
    ids=v[:-3]*26**3+v[1:-2]*26**2+v[2:-1]*26+v[3:]
    return float(Q[ids].mean())
def prefixlen(t,ref):return next((i for i,(a,b) in enumerate(zip(t,ref)) if a!=b),min(len(t),len(ref)))
def ic(t,k=1):
    counts=collections.Counter(t[i:i+k] for i in range(0,len(t)-k+1,k));n=sum(counts.values())
    return sum(v*(v-1) for v in counts.values())/(n*(n-1))
# Exhaust all 9! initial-row arrangements, keeping the existing natural tail fixed.
# Header is only checked, never imposed on a purported decoded continuation.
header_squares=[]
for perm in itertools.permutations('abcdefghi'):
    sq=''.join(perm)+'klmnopqrstuvwxyz';v={c:i for i,c in enumerate(sq)}
    z=''
    for i in range(4):
        rx,cx=divmod(v[faed[i]],5);ry,cy=divmod(v[faed[i+285]],5)
        z+=sq[5*rx+ry]+sq[5*cx+cy]
    if z[:7]=='btcseed':header_squares.append(sq)
assert square in header_squares
# Every Bifid period, preserving every source character and independently roundtripping it.
periods=[];top=[]
fixedkeys=[(2,4,21,9),(1,19,6,3),(5,4,22,11),(6,17,6,15)]
def inverse(k):
    a,b,c,d=k;det=(a*d-b*c)%25
    if math.gcd(det,25)!=1:return None
    inv=pow(det,-1,25);return(d*inv%25,-b*inv%25,-c*inv%25,a*inv%25)
fixedkeys=list(dict.fromkeys(fixedkeys+[inverse(k) for k in fixedkeys]))
fixedkeys=list(dict.fromkeys(fixedkeys+[(a,c,b,d) for a,b,c,d in fixedkeys]))
for p in range(1,571):
    b=bifid(faed,square,p);assert bifid(b,square,p,inverse=True)==faed
    if b.startswith('btcseed'):periods.append(p)
    # Whole stream has even length; alternative streams drop only their final
    # unmatched character for Hill ranking; discarded data retained explicitly.
    streams={'all':b,'even':b[::2],'odd':b[1::2]}
    if b.startswith('btcseed'):streams['after_header_carrier']=b[7::2]
    for name,t in streams.items():
        leftover=t[-1:] if len(t)%2 else '';work=t[:len(t)//2*2]
        for k in fixedkeys:
            z=hill(work,k);sc=score(z)
            top.append(dict(period=p,stream=name,key=k,score=sc,text=z,leftover=leftover))
top.sort(key=lambda x:x['score'],reverse=True)
# Distinguish an invariant short prefix from an extendible message. Under a
# fixed square and fixed key, test all possible second-half source starts.
shifts=[]
for shift in range(len(faed)):
    rotated=faed[shift:]+faed[:shift];b=bifid(rotated,square)
    shifts.append(dict(shift=shift,header_prefix=prefixlen(b,'btcseed'),hill_prefix=prefixlen(hill(b[7::2],hkey),'ifindout'),bifid_head=b[:20],hill_head=hill(b[7::2],hkey)[:20]))
# Exact conditional probability under independent uniform shuffles of each
# half, preserving the observed per-half letter multisets. Tested event is
# fixed BTCSEED followed by carrier decrypt prefix IFINDO, with fixed square/key.
# This does not correct for the historical selection of the recipe.
targetcols=hill('ifindo',(1,19,6,3))
allowed=[]
for i in range(9):
    good=[]
    for x,y in itertools.product('abcdefghi',repeat=2):
        rx,cx=divmod(square.index(x),5);ry,cy=divmod(square.index(y),5)
        r,c=square[5*rx+ry],square[5*cx+cy]
        if i<4 and r!='btcseed'[2*i]:continue
        if i<3 and c!='btcseed'[2*i+1]:continue
        if i>=3 and c!=targetcols[i-3]:continue
        good.append((x,y))
    allowed.append(good)
def eventprob(sets):
    counts=[collections.Counter(faed[:285]),collections.Counter(faed[285:])]
    def rec(i):
        if i==len(sets):return Fraction(1)
        ans=Fraction(0)
        for x,y in sets[i]:
            nx,ny=counts[0][x],counts[1][y]
            if not(nx and ny):continue
            counts[0][x]-=1;counts[1][y]-=1
            ans+=Fraction(nx*ny,(285-i)**2)*rec(i+1)
            counts[0][x]+=1;counts[1][y]+=1
        return ans
    return rec(0)
joint=eventprob(allowed)
headerprob=eventprob([[(x,y) for x,y in itertools.product('abcdefghi',repeat=2) if (lambda r,c:(r=='btcseed'[2*i] and (i==3 or c=='btcseed'[2*i+1])))(square[5*(square.index(x)//5)+square.index(y)//5],square[5*(square.index(x)%5)+square.index(y)%5])] for i in range(4)])
out2=dict(header_squares=header_squares,header_periods=periods,period_models=570,keys=fixedkeys,top_period_outputs=top[:30],rotation_controls=shifts,exact_fixed_recipe_probabilities=dict(header=str(headerprob),header_float=float(headerprob),joint=str(joint),joint_float=float(joint),conditional_ifindo_float=float(joint/headerprob),assumption='Independent uniformly shuffled halves preserving each half histogram; fixed post-selected recipe. NOT a globally corrected significance claim.'),allowed_source_pairs_for_joint_prefix=allowed,carrier_ic=ic(carrier),carrier_digraph_ic=ic(carrier,2),hill_ic=ic(hout),hill_digraph_ic=ic(hout,2))
(R/'structural_tests.json').write_text(json.dumps(out2,indent=2))
print(json.dumps({k:v for k,v in out2.items() if k not in ['rotation_controls','top_period_outputs']},indent=2));print('BEST',top[0]);print('CONTINUATION',hout)
