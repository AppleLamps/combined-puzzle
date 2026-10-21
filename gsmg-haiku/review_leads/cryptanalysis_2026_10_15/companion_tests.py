from reconstruct import *
import itertools,random,numpy as np
from coincurve import PrivateKey
Q=np.fromfile(R/'quadgrams.bin',dtype=np.float64)
def score(t):
    v=np.array([ord(x)-97 for x in t],dtype=np.int64)
    return float(Q[v[:-3]*26**3+v[1:-2]*26**2+v[2:-1]*26+v[3:]].mean())
def inv(k,n):
    a,b,c,d=k;det=(a*d-b*c)%n
    if math.gcd(det,n)!=1:return None
    q=pow(det,-1,n);return(d*q%n,-b*q%n,-c*q%n,a*q%n)
def applybase(text,k,alpha,base):
    n=len(alpha);v=[(alpha.index(x)+base)%n for x in text];a,b,c,d=k
    return ''.join(alpha[(a*x+b*y-base)%n]+alpha[(c*x+d*y-base)%n] for x,y in zip(v[::2],v[1::2]))
# Exact obstruction: side information cannot restore a preimage of a value
# outside a singular Hill map's image.
alpha='abcdefghijklmnopqrstuvwxyz';pp=[alpha.index(x) for x in 'fexm'];cc=[alpha.index(x) for x in 'gsgq']
rows=[[(a,b) for a,b in itertools.product(range(26),repeat=2) if all((a*pp[i]+b*pp[i+1])%26==cc[i+j] for i in [0,2])] for j in [0,1]]
lossy=[]
for row0,row1 in itertools.product(*rows):
    k=(*row0,*row1);image={hill(x+y,k,alpha) for x,y in itertools.product(alpha,repeat=2)}
    fails=[dict(offset=i,pair=carrier[i:i+2]) for i in range(0,len(carrier),2) if carrier[i:i+2] not in image]
    lossy.append(dict(key=k,image_size=len(image),outside_image=len(fails),first_failures=fails[:10]))
assert len(lossy)==4 and all(x['outside_image'] for x in lossy)
# If a downstream companion-controlled Caesar correction preserves IFINDO,
# all four companion symbols must encode zero. This is an exact six-position test.
prefix_constraints={c:sorted(set((A.index(hout[i])-A.index('ifindo'[i]))%25 for i in range(6) if companion[i]==c)) for c in 'bcde'}
assert all(v==[0] for v in prefix_constraints.values())
# Literal four-symbol -> two-bit stream. No dropped trailing data: every
# tested output records both the prefix and suffix not included in full bytes.
binary=[]
for name,t in [('full_row_stream',bif[::2]),('post_header',companion)]:
    for perm in itertools.permutations(range(4)):
        mapping=dict(zip('bcde',perm));bits=''.join(f'{mapping[c]:02b}' for c in t)
        for rev in (False,True):
            b=bits[::-1] if rev else bits
            for width in (7,8):
                for offset in range(width):
                    end=offset+(len(b)-offset)//width*width
                    raw=bytes(int(b[i:i+width],2) for i in range(offset,end,width))
                    printable=all(32<=v<127 for v in raw)
                    binary.append(dict(name=name,mapping=mapping,reverse=rev,width=width,offset=offset,unused_prefix=b[:offset],unused_suffix=b[end:],hex=raw.hex(),all_printable=printable))
assert not any(x['all_printable'] for x in binary)
# A positive control runs exactly the same two-bit mapping path.
control=b'read the entire message and preserve every bit'
cbits=''.join(f'{v:08b}' for v in control);ct=''.join('bcde'[int(cbits[i:i+2],2)] for i in range(0,len(cbits),2))
cb=''.join(f'{"bcde".index(c):02b}' for c in ct)
assert bytes(int(cb[i:i+8],2) for i in range(0,len(cb),8))==control
# Alternate the two explicitly printed matrices; also check the complementary
# key assigned by each of the two source row bits. These are limited fixed
# schedules, not a free adaptive key per character.
keys=[tuple(A.index(c) for c in t) for t in ['fexm','gsgq']]
variants=list(dict.fromkeys(keys+[inv(k,25) for k in keys]+[hkey,inv(hkey,25)]))
outputs=[]
for k0,k1 in itertools.product(variants,repeat=2):
    for schedule in ['alternating','period3','companion_first','companion_second']:
        for flip in (0,1):
            z=''
            for i in range(0,len(carrier),2):
                if schedule=='alternating':which=(i//2)%2
                elif schedule=='period3':which=(i//6)%2
                else:
                    symbol=companion[min(i,len(companion)-1)]
                    row,col=divmod(square.index(symbol),5)
                    which=row if schedule=='companion_first' else col
                z+=hill(carrier[i:i+2],[k0,k1][which^flip])
            outputs.append(dict(k0=k0,k1=k1,schedule=schedule,flip=flip,score=score(z),text=z))
outputs.sort(key=lambda x:x['score'],reverse=True)
(R/'companion_tests.json').write_text(json.dumps(dict(singular_hill=lossy,caesar_preserve_prefix=prefix_constraints,binary=binary,scheduled_hill_top=outputs[:20],scheduled_models=len(outputs),controls=['invented two-bit byte stream round-trip']),indent=2))
print('singular keys',[(r['key'],r['outside_image']) for r in lossy]);print('Caesar constraints',prefix_constraints);print('base4 models',len(binary),'printable',sum(x['all_printable'] for x in binary));print('scheduled models',len(outputs),'best',outputs[0])
