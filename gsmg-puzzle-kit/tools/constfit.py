import sys; sys.set_int_max_str_digits(0)
import sys, math
from decimal import Decimal, getcontext
getcontext().prec=30050
T=open('ta.txt').read().strip()
faed=T[195:765]; dbbi=T[:91]
res='difhccgihaeeihggegebgehhehhfafdhffcdbfcccgfeggecdcifffgigeea'
# dbbi host chars removed already = residue
def g_of(s):
    m={'1':'a','2':'b','3':'c','4':'d','5':'e','6':'f','7':'g','8':'h','9':'i','0':'g'}
    return ''.join(m[c] for c in s if c in m)
targets={'faed':faed,'faed_rev':faed[::-1],'residue':res,'dbbi':dbbi}
K=8
ix={}
for n,t in targets.items():
    d={}
    for i in range(len(t)-K+1): d.setdefault(t[i:i+K],[]).append(i)
    ix[n]=d
def best(cg):
    b=(0,None)
    for n,d in ix.items():
        t=targets[n]
        for i in range(len(cg)-K+1):
            w=cg[i:i+K]
            if w in d:
                for j in d[w]:
                    L=K
                    while i+L<len(cg) and j+L<len(t) and cg[i+L]==t[j+L]: L+=1
                    if L>b[0]: b=(L,(n,i,j))
    return b
corp={}
D=Decimal
def digs(x,n=30000):
    s=format(x,'f').replace('.','')
    return s[:n]
# pi (Machin)
def arctan_inv(x,prec):
    getcontext().prec=prec
    x=D(x); t=1/x; s=t; x2=x*x; k=1; sign=-1
    eps=D(10)**-(prec-5)
    while True:
        t=t/x2; term=t/(2*k+1)
        if term<eps: break
        s+=sign*term; sign=-sign; k+=1
    return s
def pi_digits(n=20000):
    getcontext().prec=n+40
    p=4*(4*arctan_inv(5,n+40)-arctan_inv(239,n+40))
    return digs(p,n)
def econst(n=20000):
    getcontext().prec=n+40
    s=D(0); f=D(1); k=0
    eps=D(10)**-(n+35)
    while True:
        term=1/f
        s+=term
        k+=1; f*=k
        if term<eps: break
    return digs(s,n)
N=8000
getcontext().prec=N+50
corp['pi']=pi_digits(N); corp['e']=econst(N)
getcontext().prec=N+50
corp['phi']=digs((1+D(5).sqrt())/2,N)
for n in range(2,30):
    r=int(math.isqrt(n))
    if r*r!=n: corp['sqrt%d'%n]=digs(D(n).sqrt(),N)
for n in range(2,14): corp['ln%d'%n]=digs(D(n).ln(),N)
for n in (2,3,5):
    corp['cbrt%d'%n]=digs(D(n)**(D(1)/3),N)
corp['pi2']=digs(D(corp['pi'][0]+'.'+corp['pi'][1:N])**2,N)
# zeta(3) Apery
getcontext().prec=2500
z=D(0); c=D(1)  # 1/C(2n,n)
from math import comb
for n in range(1,1400):
    z+=D((-1)**(n-1))/(D(n)**3*D(comb(2*n,n)))
corp['zeta3']=digs(z*D(5)/2,2000)
getcontext().prec=N+50
# concatenation sequences
def primes_upto(n):
    sv=bytearray([1])*(n+1); sv[0]=sv[1]=0
    for i in range(2,int(n**.5)+1):
        if sv[i]: sv[i*i::i]=bytearray(len(sv[i*i::i]))
    return [i for i in range(n+1) if sv[i]]
P=primes_upto(200000)
corp['primes']=''.join(map(str,P))[:N]
corp['naturals']=''.join(str(i) for i in range(1,6000))[:N]
corp['squares']=''.join(str(i*i) for i in range(1,4000))[:N]
corp['cubes']=''.join(str(i**3) for i in range(1,2500))[:N]
a,b=1,1;fs=[]
for _ in range(6000): fs.append(a); a,b=b,a+b
corp['fib']=''.join(map(str,fs))[:N]
corp['pow2']=''.join(str(2**i) for i in range(1,3000))[:N]
corp['pow3']=''.join(str(3**i) for i in range(1,2000))[:N]
f=1;fl=[]
for i in range(1,1500): f*=i; fl.append(f)
corp['fact']=''.join(map(str,fl))[:N]
corp['tri']=''.join(str(i*(i+1)//2) for i in range(1,4000))[:N]
corp['primes_rev']=''.join(str(p)[::-1] for p in P)[:N]
corp['semiprimes']=''.join(str(i) for i in range(4,20000) if sum(1 for p in P[:100] if i%p==0 and p*p<=i)>0)[:N]
# integer forms of puzzle objects
import base64
def rawb(n): return base64.b64decode(open('b64/%s.b64'%n).read())
for nm in ('phase2','terminal','short','cosmic'):
    corp['int_'+nm]=str(int.from_bytes(rawb(nm),'big'))
    corp['int_'+nm+'_rev']=str(int.from_bytes(rawb(nm)[::-1],'big'))
for nm,fn in (('pt3','pt3.bin'),('pt32','pt32.bin')):
    d=open(fn,'rb').read()
    corp['int_'+nm]=str(int.from_bytes(d,'big'))
arch=open('architect.txt').read()
corp['a1z26_arch']=''.join(str(ord(c)-96) for c in arch)
corp['a1z26_arch_rev']=''.join(str(ord(c)-96) for c in arch[::-1])
corp['ascii_arch']=''.join(str(ord(c)) for c in arch)
corp['ascii_arch_up']=''.join(str(ord(c)) for c in arch.upper())
msg='incaseyoumanagetocrackthistheprivatekeysbelongtohalfandbetterhalfandtheyalsoneedfundstolive'
corp['a1z26_msg']=''.join(str(ord(c)-96) for c in msg)
corp['ascii_msg']=''.join(str(ord(c)) for c in msg)
corp['ascii_msg_up']=''.join(str(ord(c)) for c in msg.upper())
# checkerboard digits
cb='15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112'
corp['checker149']=cb
import json
res_=[]
for name,s in corp.items():
    cg=g_of(s)
    for rv,tag in ((cg,''),(cg[::-1],'_rev')):
        b=best(rv)
        res_.append((b[0],name+tag,b[1],len(cg)))
res_.sort(reverse=True)
print('corpora',len(corp),'total digits',sum(len(s) for s in corp.values()))
for r in res_[:12]: print(r)
