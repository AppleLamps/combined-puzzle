import sys, collections
sys.path.insert(0,'.')
from pools import *
A=open('architect.txt').read()
lists={}
for en,M in E.items():
    for ln,S in matrix_lists(M).items(): lists[(en,ln)]=S
new=set(); old=set(); Ts=set()
for k,S in lists.items():
    Ts.add(sum(S))
    for fn,s in forms(S).items():
        for rv in (0,1):
            t=s[::-1] if rv else s
            if not (0<len(t)<=400): continue
            (new if fn in ('L1','L0','M10') else old).add(t)
old-=new
print('msl new',len(new),'old',len(old),'T distinct',len(Ts))
open('msl_new.txt','w').write('\n'.join(sorted(new))+'\n')
open('msl_old.txt','w').write('\n'.join(sorted(old))+'\n')
core_off=[341,371,472,479,1238,1483,1539]
lw_core=set(); lw_loc=set()
for o in core_off:
    for k in range(3,28):
        if o-k>=0: lw_core.add(A[o-k:o])
for T in Ts:
    for o in (T,):
        if 3<=o<=1539:
            for k in range(3,28):
                if o-k>=0: lw_loc.add(A[o-k:o])
lw_loc-=lw_core
print('lw core',len(lw_core),'lw loc',len(lw_loc))
open('lw_core.txt','w').write('\n'.join(sorted(lw_core))+'\n')
open('lw_loc.txt','w').write('\n'.join(sorted(lw_loc))+'\n')
# all msl alone
open('msl_all.txt','w').write('\n'.join(sorted(new|old))+'\n')
