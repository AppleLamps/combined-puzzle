"""Test whether an omitted affine offset repairs the linear Hill obstruction."""
from reconstruct import *
import numpy as np,itertools
Q=np.fromfile(R/'quadgrams.bin',dtype=np.float64)
def solve(text,alphabet,block,crib):
 n=len(alphabet);cs=np.array([alphabet.index(c) for c in text],dtype=np.int64).reshape(-1,block)
 plain=np.array([alphabet.index(c) for c in crib],dtype=np.int64).reshape(-1,block)
 rows=np.array(list(itertools.product(range(n),repeat=block+1)),dtype=np.int64)
 pred=(rows[:,:block]@cs[:len(plain)].T+rows[:,block,None])%n
 choices=[rows[np.all(pred==plain[:,i],axis=1)] for i in range(block)]
 count=math.prod(map(len,choices));records=[];tested=0
 if count>2000000:return dict(row_choices=list(map(len,choices)),combinations=count,status='too large; not tested')
 for rr in itertools.product(*choices):
  k=np.array(rr);m=k[:,:block];offset=k[:,block]
  if block==2:det=m[0,0]*m[1,1]-m[0,1]*m[1,0]
  else:
   a,b,c=m;det=a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
  if math.gcd(int(det),n)!=1:continue
  tested+=1;v=(cs@m.T+offset)%n;t=''.join(alphabet[x] for x in v.flat)
  z=np.array([ord(c)-97 for c in t[len(crib):]])
  score=float(Q[z[:-3]*26**3+z[1:-2]*26**2+z[2:-1]*26+z[3:]].mean())
  records.append(dict(key=k.tolist(),score=score,text=t))
 records.sort(key=lambda x:x['score'],reverse=True)
 return dict(row_choices=list(map(len,choices)),combinations=count,tested=tested,top=records[:10])
res=[]
for alphabet in [A,square,'abcdefghijklmnopqrstuvwxyz']:
 for block,crib in [(2,'ifindo'),(3,'ifindoubt')]:
  r=solve(carrier,alphabet,block,crib);res.append(dict(alphabet=alphabet,block=block,crib=crib,result=r));print(alphabet,block,r.get('tested'),r['combinations'],[(x['score'],x['text'][:45]) for x in r.get('top',[])[:2]],flush=True)
# Forward affine positive controls. Test data chosen independently of actual carrier.
plain=('ifindoubtreconstructthecompleteencodingandpreserveallcharactersbeforeacceptinganyprefixasproof'+'theproceduremustexplaintherestofthemessage'*8)[:282]
assert len(plain)==282
controls=[]
for block in [2,3]:
 if block==2:plain2='ifindo'+plain[6:];m=np.array([[1,2],[0,1]]);off=np.array([3,7]);crib='ifindo'
 else:plain2=plain;m=np.array([[1,2,3],[0,1,4],[0,0,1]]);off=np.array([3,7,11]);crib='ifindoubt'
 p=np.array([A.index(c) for c in plain2]).reshape(-1,block);ct=''.join(A[x] for x in ((p@m.T+off)%25).flat)
 result=solve(ct,A,block,crib);assert any(x['text']==plain2 for x in result['top']);controls.append(dict(block=block,plaintext=plain2,result=result))
(R/'affine_hill.json').write_text(json.dumps(dict(models=res,controls=controls,scope='All invertible affine 2x2 keys consistent with IFINDO and affine 3x3 keys consistent with IFINDOUBT, in three stated alphabets. The supplied crib is an assumption, not evidence; only continuation is scored.'),indent=2))
