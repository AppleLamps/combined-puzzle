from reconstruct import *
class Field:
    def __init__(self,p,b,c):self.p,self.b,self.c=p,b,c
    def add(self,x,y):
        p=self.p;return (x%p+y%p)%p+p*((x//p+y//p)%p)
    def neg(self,x):return self.add(0,(-x%self.p)%self.p+self.p*((-(x//self.p))%self.p))
    def sub(self,x,y):return self.add(x,self.neg(y))
    def mul(self,x,y):
        p=self.p;return ((x%p)*(y%p)-self.c*(x//p)*(y//p))%p+p*(((x%p)*(y//p)+(x//p)*(y%p)-self.b*(x//p)*(y//p))%p)
    def inv(self,x):return next(y for y in range(1,self.p**2) if self.mul(x,y)==1)
    def dot(self,a,b):
        z=0
        for x,y in zip(a,b):z=self.add(z,self.mul(x,y))
        return z
    def matmul(self,A,B):return [[self.dot(row,col) for col in zip(*B)] for row in A]
    def inverse(self,M):
        n=len(M);a=[r.copy()+[int(i==j) for j in range(n)] for i,r in enumerate(M)]
        for j in range(n):
            k=next((i for i in range(j,n) if a[i][j]),None)
            if k is None:return None
            a[j],a[k]=a[k],a[j];q=self.inv(a[j][j]);a[j]=[self.mul(x,q) for x in a[j]]
            for i in range(n):
                if i==j:continue
                q=a[i][j];a[i]=[self.sub(x,self.mul(q,y)) for x,y in zip(a[i],a[j])]
        return [row[n:] for row in a]
def columns(t,n,alpha,base):return [[(alpha.index(t[i*n+j])+base)%25 for i in range(n)] for j in range(n)]
def trans(text,key,F,alpha,base):
    n=len(key);out=''
    for i in range(0,len(text),n):
        v=[(alpha.index(x)+base)%25 for x in text[i:i+n]]
        out+=''.join(alpha[(F.dot(r,v)-base)%25] for r in key)
    return out
results=[]
for b in range(5):
    for c in range(5):
        if any((x*x+b*x+c)%5==0 for x in range(5)):continue
        F=Field(5,b,c)
        # Complete small-field algebra audit, including nonzero inverses.
        for x in range(25):
            assert F.add(x,F.neg(x))==0
            if x:assert F.mul(x,F.inv(x))==1
            for y in range(25):
                for z in range(25):
                    assert F.mul(x,F.add(y,z))==F.add(F.mul(x,y),F.mul(x,z))
        for name,alpha in [('natural25',A),('dbbi25',square)]:
            for base in [0,1]:
                for kind,n,pt,ct in [('example2',2,'fexm','gsgq'),('crib3',3,'ifindoubt',carrier[:9])]:
                    P,C=columns(pt,n,alpha,base),columns(ct,n,alpha,base)
                    pi=F.inverse(P)
                    if pi is None:
                        results.append(dict(poly=[b,c],alphabet=name,base=base,kind=kind,status='singular plaintext matrix; not excluded'))
                        continue
                    K=F.matmul(C,pi);D=F.inverse(K)
                    if D is None:
                        results.append(dict(poly=[b,c],alphabet=name,base=base,kind=kind,status='derived key singular'))
                        continue
                    assert trans(pt,K,F,alpha,base)==ct
                    out=trans(carrier,D,F,alpha,base)
                    assert trans(out,K,F,alpha,base)==carrier
                    results.append(dict(poly=[b,c],alphabet=name,base=base,kind=kind,key=K,inverse=D,output=out,status='roundtrip; full output retained'))
(R/'field25.json').write_text(json.dumps(results,indent=2));print('models',len(results),'complete outputs',sum('output'in x for x in results))
for r in results:
    if 'output'in r:print(r['poly'],r['alphabet'],r['base'],r['kind'],r['output'][:80])
