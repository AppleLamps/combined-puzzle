from reconstruct import *
import numpy as np,random,itertools
Q=np.fromfile(R/'quadgrams.bin',dtype=np.float64)
digits=np.array([ord(c)-96 for c in faed],dtype=np.int64)
assert int(digits.sum())==2*len(arch)+1
def allscores(text,ds):
    v=np.frombuffer(text.lower().encode(),dtype=np.uint8).astype(np.int64)-97;n=len(v)
    pos=np.cumsum(ds)-1
    indexes=(np.arange(n)[:,None]+pos[None,:])%n
    out=v[indexes]
    scores=Q[out[:,:-3]*26**3+out[:,1:-2]*26**2+out[:,2:-1]*26+out[:,3:]].mean(axis=1)
    best=int(np.argmax(scores));return float(scores[best]),best,''.join(chr(97+x) for x in out[best])
real=[];null=[];rng=np.random.default_rng(20261015)
for name,text in [('architect',arch),('beaufort_ciphertext',ebcdic)]:
    for source_reverse in [False,True]:
        t=text[::-1] if source_reverse else text
        for ds_reverse in [False,True]:
            ds=digits[::-1] if ds_reverse else digits
            sc,start,out=allscores(t,ds)
            real.append(dict(source=name,source_reverse=source_reverse,digits_reverse=ds_reverse,score=sc,start=start,output=out))
    for i in range(20):
        ds=rng.permutation(digits);sc,start,out=allscores(text,ds)
        null.append(dict(source=name,shuffle=i,score=sc,start=start,output=out))
# Arithmetic positive control, independent implementation of cyclic stepping.
t='ABCDEFGHIJKLMNOPQRSTUVWXYZ';ds=np.array([6,1,5,4,7,7,5,5,4]);manual=[];index=-1
for step in ds:index=(index+int(step))%len(t);manual.append(t[index])
assert ''.join(manual)==''.join(t[(int(p)-1)%len(t)] for p in np.cumsum(ds))
# An identity-gap English control must rank above the real streams. It tests
# the detector, not the observed 3079 sum.
control_score,_,control_output=allscores(arch,np.ones(570,dtype=np.int64))
assert control_score>max(x['score'] for x in real)
result=dict(digit_sum=int(digits.sum()),architect_length=len(arch),source_window_relation='sum(digits)=2*1539+1; invariant under shuffling, not ordering evidence',real=real,shuffle_controls=null,english_control_score=control_score,cyclic_index_control=True)
(R/'book_tests.json').write_text(json.dumps(result,indent=2))
print('sum',digits.sum(),'length',len(arch),'real best',max(real,key=lambda x:x['score']));print('null better',sum(x['score']>=max(r['score'] for r in real) for x in null),'/',len(null),'control',control_score)
