import sys, random, base64, collections, math
sys.path.insert(0,'.')
from pools import forms
T=open('ta.txt').read().strip()
B64='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
def m_az1(c): return ord(c.lower())-96 if c.isalpha() else (int(c) if c.isdigit() else 0)
def m_az0(c): return ord(c.lower())-97 if c.isalpha() else (int(c) if c.isdigit() else 0)
def m_dig(c): return 0 if c=='o' else (ord(c)-96 if 'a'<=c<='i' else m_az1(c))
def m_b64(c): return B64.index(c) if c in B64 else 0
def m_bit(c): return 0 if c=='a' else 1
def m_asc(c): return ord(c)
MAPS={'az1':m_az1,'az0':m_az0,'dig':m_dig,'b64':m_b64,'bit':m_bit,'asc':m_asc}
def raw(n): return open('b64/%s.b64'%n).read().replace('\n','')
objs={}
blocks={'dbbi':(0,91),'ab':(91,195),'faed':(195,765),'seg1':(766,829),'seg2':(830,859),'lit1':(860,895),'b64a':(895,959),'enter':(959,999),'b64b':(999,1063),'lit2':(1063,1075),
 'top195':(0,195),'top765':(0,765),'all':(0,1075),'tail310':(765,1075),'b64both':None}
for k,v in blocks.items():
    if v: objs[k]=T[v[0]:v[1]]
objs['b64both']=T[895:959]+T[999:1063]
for n in ('phase2','terminal','short','cosmic'): objs['b64_'+n]=raw(n)
arch=open('architect.txt').read(); objs['architect']=arch
objs['checker91']='incaseyoumanagetocrackthistheprivatekeysbelongtohalfandbetterhalfandtheyalsoneedfundstolive'
def divisors(n): return [d for d in range(2,n//2+1) if n%d==0]
def sumlists(V):
    out={}
    n=len(V); out['tot']=[sum(V)]
    for r in divisors(n):
        c=n//r  # r rows, c cols
        rows=[sum(V[i*c:(i+1)*c]) for i in range(r)]
        cols=[sum(V[i*c+j] for i in range(r)) for j in range(c)]
        out['r%dx%d_rows'%(r,c)]=rows; out['r%dx%d_cols'%(r,c)]=cols
        out['r%dx%d_rc'%(r,c)]=rows+cols
        # diagonals
        dg=[sum(V[i*c+(i+k)] for i in range(r) if 0<=i+k<c) for k in range(-r+1,c)]
        out['r%dx%d_diag'%(r,c)]=dg
    return out
def allstrings(V, tag, sink):
    for ln,S in sumlists(V).items():
        for fn,s in forms(S).items():
            for rv in (0,1):
                t=s[::-1] if rv else s
                if 0<len(t)<=600: sink.append((tag+'|'+ln+'|'+fn+('r' if rv else ''),t))
# --- english fit
words=set(w for w in open('words.txt').read().split() if len(w)>=5)
def best_cover(s):
    s=''.join(ch for ch in s.lower() if ch.isalpha())
    n=len(s)
    if n<5: return (0,0)
    best=[0]*(n+1); # longest single word
    lw=0
    # dp coverage with words >=5 letters
    for i in range(n):
        best[i+1]=max(best[i+1],best[i])
        for L in range(5,min(14,n-i)+1):
            if s[i:i+L] in words:
                best[i+L]=max(best[i+L],best[i]+L); lw=max(lw,L)
    return best[n],lw
def run(seed=None):
    res=[]
    for on,s in objs.items():
        for mn,mp in MAPS.items():
            if mn=='b64' and not on.startswith('b64'): continue
            if mn=='bit' and on not in ('ab','enter','top195'): continue
            try: V=[mp(c) for c in s]
            except Exception: continue
            if seed is not None:
                V=V[:]; random.Random(seed).shuffle(V)
            allstrings(V,on+'/'+mn,res)
    return res
if __name__=='__main__':
    real=run()
    print('strings',len(real))
    uniq={}
    for tag,t in real: uniq.setdefault(t,tag)
    print('distinct',len(uniq))
    open('n2_cands.txt','w').write('\n'.join(uniq.keys())+'\n')
    # english fit on letter-ish forms
    def stat(res):
        best=(0,0,'')
        cnt8=0
        for tag,t in res:
            f=tag.split('|')[2]
            if f.rstrip('r') in ('L1','L0','A'):
                cv,lw=best_cover(t)
                if lw>=7: cnt8+=1
                if (lw,cv)>best[:2]: best=(lw,cv,tag+' '+t[:60])
        return cnt8,best
    print('real',stat(real))
    for sd in range(3):
        print('null',sd,stat(run(seed=sd)))
