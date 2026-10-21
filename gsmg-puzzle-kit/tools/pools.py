import itertools, re, sys
cell=['WWKKWBWWKWKKWY','KKBKWWKKKWBWKK','KKWKKKWBWWKWWK','WKKWBWWWWKKKWK','WBKWWWKKWYWKKW','KWWKKWYWKWYWKK','KWWBKKWWWKWYWW','BKKWFWWWWWKWYW','WWWKKBWKKKKKWB','KKBKKKYWKKWWWK','KKWKWWWYWKKWKK','KKKKWWKWBWKKWW','WBWKKKWKWYWKKW','WKBWKKWKKWBWKK']
bit=['00110100101100','11110011101011','11011101001001','01101000011101','01100011000110','10011000100011','10011100010000','11100000001000','00011101111101','11111100110001','11010000011011','11110010101100','01011101000110','01101101101011']
N=14
def isprime(k): return k>1 and all(k%p for p in range(2,int(k**.5)+1))
# ---- encodings of the poster: dict name -> 14x14 int matrix
def enc(f): return [[f(cell[r][c],bit[r][c]) for c in range(N)] for r in range(N)]
E={}
E['bit_F0']=enc(lambda k,b:int(b))
E['bit_F1']=enc(lambda k,b:1 if k=='F' else int(b))
for nm,fv in (('white',9),('red',2),('blue',6)):
    E['res_F'+nm]=enc(lambda k,b,fv=fv:{'K':0,'Y':4,'B':6,'W':9,'F':fv}[k])
E['consume']=enc(lambda k,b:{'K':0,'W':0,'B':1,'Y':2,'F':1}[k])
E['idx_kbyw']=enc(lambda k,b:{'K':1,'B':2,'Y':3,'W':4,'F':4}[k])
E['idx_wkyb']=enc(lambda k,b:{'W':1,'K':2,'Y':3,'B':4,'F':1}[k])
E['pal1']=enc(lambda k,b:{'K':1,'W':11,'B':9,'Y':6,'F':11}[k])
E['pal0']=enc(lambda k,b:{'K':0,'W':10,'B':8,'Y':5,'F':10}[k])
E['w1_F0']=enc(lambda k,b:1 if k=='W' else 0)
E['w1_F1']=enc(lambda k,b:1 if k in 'WF' else 0)
E['painted']=enc(lambda k,b:1 if k=='F' else 0)
E['colour_only']=enc(lambda k,b:1 if k in 'BY' else 0)
E['blue_only']=enc(lambda k,b:1 if k=='B' else 0)
E['yellow_only']=enc(lambda k,b:1 if k=='Y' else 0)
E['dark']=enc(lambda k,b:1 if k in 'KB' else 0)
def sp_order(n):
    seen=set();r=c=0;dr,dc=1,0;out=[]
    for _ in range(n*n):
        out.append((r,c));seen.add((r,c))
        nr,nc=r+dr,c+dc
        if not(0<=nr<n and 0<=nc<n) or (nr,nc) in seen:
            dr,dc={(1,0):(0,1),(0,1):(-1,0),(-1,0):(0,-1),(0,-1):(1,0)}[(dr,dc)]
            nr,nc=r+dr,c+dc
        r,c=nr,nc
    return out
SP=sp_order(N)
def matrix_lists(M, gard=(2,5,7)):
    R=len(M); C=len(M[0]); L={}
    rs=[sum(r) for r in M]; cs=[sum(M[r][c] for r in range(R)) for c in range(C)]
    L['rows']=rs; L['cols']=cs
    L['rows_rev']=rs[::-1]; L['cols_rev']=cs[::-1]
    L['rowscols']=rs+cs
    L['colsrows']=cs+rs
    pr=[i for i in range(1,R+1) if isprime(i)]; pc=[i for i in range(1,C+1) if isprime(i)]
    L['rows_prime1']=[rs[i-1] for i in pr]; L['cols_prime1']=[cs[i-1] for i in pc]
    L['rows_prime0']=[rs[i] for i in pr if i<R]; L['cols_prime0']=[cs[i] for i in pc if i<C]
    for g in (gard,(2,),(5,),(7,),(2,5),(2,7),(5,7)):
        L['rows_g1_%s'%(g,)]=[rs[i-1] for i in g]; L['cols_g1_%s'%(g,)]=[cs[i-1] for i in g]
        L['rows_g0_%s'%(g,)]=[rs[i] for i in g]; L['cols_g0_%s'%(g,)]=[cs[i] for i in g]
        L['rowsmul_%s'%(g,)]=[sum(rs[i] for i in range(R) if (i+1)%p==0) for p in g]
        L['colsmul_%s'%(g,)]=[sum(cs[i] for i in range(C) if (i+1)%p==0) for p in g]
    dg=[sum(M[r][r+k] for r in range(R) if 0<=r+k<C) for k in range(-R+1,C)]
    ad=[sum(M[r][k-r] for r in range(R) if 0<=k-r<C) for k in range(R+C-1)]
    L['diags']=dg; L['antidiags']=ad
    L['maindiag']=[sum(M[i][i] for i in range(min(R,C)))]; L['antidiag']=[sum(M[i][C-1-i] for i in range(min(R,C)))]
    for b in (2,7):
        if R%b==0 and C%b==0:
            L['blk%d'%b]=[sum(M[r+i][c+j] for i in range(b) for j in range(b)) for r in range(0,R,b) for c in range(0,C,b)]
    flat=[M[r][c] for r in range(R) for c in range(C)]
    spf=[M[r][c] for r,c in SP] if (R==N and C==N) else flat
    for nm,seq in (('flat',flat),('spiral',spf)):
        for w in (2,5,7):
            L[nm+'_chunk%d'%w]=[sum(seq[i:i+w]) for i in range(0,len(seq),w)]
            L[nm+'_win%d'%w]=[sum(seq[i:i+w]) for i in range(0,len(seq)-w+1)]
            for p in (2,5,7):
                pass
        for p in (2,5,7):
            L[nm+'_mod%d'%p]=[sum(seq[i] for i in range(k,len(seq),p)) for k in range(p)]
        cum=[];s=0
        for x in seq: s+=x; cum.append(s)
        L[nm+'_cum_g']=[cum[g-1] for g in gard]
        L[nm+'_cum_prime']=[cum[i-1] for i in range(1,len(seq)+1) if isprime(i)]
        L[nm+'_at_prime']=[seq[i-1] for i in range(1,len(seq)+1) if isprime(i)]
        L[nm+'_at_prime0']=[seq[i] for i in range(len(seq)) if isprime(i)]
        L[nm+'_at_g']=[seq[g-1] for g in gard]
        L[nm+'_total']=[sum(seq)]
    sub=[[M[r-1][c-1] for c in gard] for r in gard]
    L['gsub_rows']=[sum(r) for r in sub]; L['gsub_cols']=[sum(sub[r][c] for r in range(3)) for c in range(3)]; L['gsub_tot']=[sum(map(sum,sub))]
    return L
# ---- forms
def forms(S):
    out={}
    if not S: return out
    out['D']=''.join(str(s) for s in S)
    out['Dc']=','.join(str(s) for s in S)
    out['Ds']=' '.join(str(s) for s in S)
    out['L1']=''.join(chr(96+((s-1)%26)+1) for s in S)
    out['L0']=''.join(chr(97+(s%26)) for s in S)
    out['M10']=''.join(str(s%10) for s in S)
    if all(32<=s<127 for s in S): out['A']=''.join(chr(s) for s in S)
    if all(0<=s<256 for s in S): out['H']=''.join('%02x'%s for s in S)
    if sum(S)>=0: out['T']=str(sum(S))
    return out
if __name__=='__main__':
    lists={}
    for en,M in E.items():
        for ln,S in matrix_lists(M).items():
            lists[(en,ln)]=S
    print(len(lists),'lists')
    import collections
    seen=collections.OrderedDict()
    for k,S in lists.items():
        for fn,s in forms(S).items():
            for rv in (0,1):
                t=s[::-1] if rv else s
                if 0<len(t)<=400: seen.setdefault((fn,rv),set()).add(t)
    tot=0
    for k,v in sorted(seen.items()): print(k,len(v)); tot+=len(v)
    print('total distinct',tot)
