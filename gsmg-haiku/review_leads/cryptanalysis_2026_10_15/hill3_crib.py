from reconstruct import *
import numpy as np,itertools,random
Q=np.fromfile(R/'quadgrams.bin',dtype=np.float64)
def scan(text,alphabet,base,crib='ifindo'):
    n=len(alphabet);cs=np.array([(alphabet.index(c)+base)%n for c in text],dtype=np.int64).reshape(-1,3)
    pv=np.array([(alphabet.index(c)+base)%n for c in crib],dtype=np.int64).reshape(-1,3)
    rows=np.array(list(itertools.product(range(n),repeat=3)),dtype=np.int64)
    preds=(rows@cs[:len(pv)].T)%n
    choices=[rows[np.all(preds==pv[:,i],axis=1)] for i in range(3)]
    if any(len(x)==0 for x in choices):return dict(rows=list(map(len,choices)),keys=0,top=[])
    lookup=np.array([ord(alphabet[(i-base)%n])-97 for i in range(n)])
    keycount=0;best=[];nine=0;nine_outputs=[]
    for first in choices[0]:
        keys=np.array([(first,b,c) for b,c in itertools.product(choices[1],choices[2])])
        a,b,c=keys[:,0,:],keys[:,1,:],keys[:,2,:]
        det=a[:,0]*(b[:,1]*c[:,2]-b[:,2]*c[:,1])-a[:,1]*(b[:,0]*c[:,2]-b[:,2]*c[:,0])+a[:,2]*(b[:,0]*c[:,1]-b[:,1]*c[:,0])
        keys=keys[np.gcd(det,n)==1];keycount+=len(keys)
        if not len(keys):continue
        out=np.einsum('kij,bj->kbi',keys,cs)%n;out=lookup[out].reshape(len(keys),-1)
        # Rank only unseen continuation; the six fixed letters receive no credit.
        tail=out[:,len(crib):]
        sc=Q[tail[:,:-3]*26**3+tail[:,1:-2]*26**2+tail[:,2:-1]*26+tail[:,3:]].mean(axis=1)
        for i in np.argsort(sc)[-5:]:
            t=''.join(chr(97+x) for x in out[i]);best.append(dict(key=keys[i].tolist(),score=float(sc[i]),text=t))
        for i,p in enumerate(out):
            if ''.join(chr(97+x) for x in p[:9])=='ifindoubt':
                nine+=1;nine_outputs.append(dict(key=keys[i].tolist(),text=''.join(chr(97+x) for x in p),score=float(sc[i])))
    best.sort(key=lambda x:x['score'],reverse=True)
    return dict(rows=list(map(len,choices)),keys=keycount,ifindoubt_keys=nine,ifindoubt_outputs=nine_outputs,top=best[:10])
result=[]
# A source-derived invariant precedes any key search: C3 = 4*C1 mod5.
v=np.array([A.index(c) for c in carrier[:9]]).reshape(3,3)
assert np.all(v[2]%5==(4*v[0])%5)
expected=np.array([A.index(c) for c in 'ifindoubt']).reshape(3,3)
assert not np.all(expected[2]%5==(4*expected[0])%5)
for name,alpha in [('natural25',A),('dbbi25',square),('natural26','abcdefghijklmnopqrstuvwxyz')]:
    for base in [0,1]:
        res=scan(carrier,alpha,base);result.append(dict(alphabet=name,base=base,**res))
        print(name,base,'row choices',res['rows'],'keys',res['keys'],'IFINDOUBT',res.get('ifindoubt_keys'),'best',res['top'][:1],flush=True)
# Forward-generated 3x3 positive control, same length and fixed crib.
plain=('ifindoubtreadthecompleteinstructionandcheckeverycharacterbeforeyouaccepttheresultthecorrectkeymustexplaintherestofthemessagewithoutchangingthealphabetorintroducinganotherruleonlyafteryouhaverecoveredthefullinstructionshouldyouattempttoopenthefinalencryptedcontainer')
plain=(plain+'preservealltheunusedcharactersandtheoriginalorder')[:282];assert len(plain)==282
K=np.array([[1,2,3],[0,1,4],[0,0,1]],dtype=np.int64);pv=np.array([A.index(x) for x in plain]).reshape(-1,3)
cv=(pv@K.T)%25;ct=''.join(A[x] for x in cv.flat)
control=scan(ct,A,0);assert control['top'][0]['text']==plain
rng=random.Random(20261015);null=[];blocks=[carrier[i:i+3] for i in range(0,len(carrier),3)]
for i in range(12):
    tail=blocks[2:].copy();rng.shuffle(tail);t=''.join(blocks[:2]+tail);res=scan(t,A,0)
    null.append(dict(shuffle=i,**res))
(R/'hill3_crib.json').write_text(json.dumps(dict(models=result,control=dict(plaintext=plain,ciphertext=ct,result=control),nulls=null,acceptance='Complete coherent continuation, not fixed IFINDO or the fitted IFINDOUBT alone; ranks exclude fixed crib.'),indent=2))
print('control recovered',control['top'][0]['score'],'null best',[x['top'][0]['score'] for x in null])
