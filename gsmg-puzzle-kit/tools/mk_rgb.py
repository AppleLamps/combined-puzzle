import sys
sys.path.insert(0,'.')
from pools import *
import numpy as np
from PIL import Image
a=np.array(Image.open('puzzle.png').convert('RGB')).astype(np.int64)
RGB={'K':(0,0,0),'W':(255,255,255),'B':(63,72,204),'Y':(255,242,0),'F':(254,254,254)}
EE={}
def encf(f): return [[f(cell[r][c],r,c) for c in range(N)] for r in range(N)]
EE['rgb24']=encf(lambda k,r,c:(RGB[k][0]<<16)|(RGB[k][1]<<8)|RGB[k][2])
EE['bgr24']=encf(lambda k,r,c:(RGB[k][2]<<16)|(RGB[k][1]<<8)|RGB[k][0])
for i,nm in enumerate('RGB'): EE['chan'+nm]=encf(lambda k,r,c,i=i:RGB[k][i])
EE['lum']=encf(lambda k,r,c:sum(RGB[k]))
def cellpix(r,c): return a[r*75:min(r*75+75,1047), c*75:min(c*75+75,1047)]
EE['pixsum']=encf(lambda k,r,c:int(cellpix(r,c).sum()))
EE['pixsumR']=encf(lambda k,r,c:int(cellpix(r,c)[:,:,0].sum()))
EE['red_ink']=encf(lambda k,r,c:int(((cellpix(r,c)==(237,28,36)).all(axis=2)).sum()))
EE['black_px']=encf(lambda k,r,c:int(((cellpix(r,c)==(0,0,0)).all(axis=2)).sum()))
EE['white_px']=encf(lambda k,r,c:int(((cellpix(r,c)==(255,255,255)).all(axis=2)).sum()))
def forms2(S):
    out=forms(S)
    if not S: return out
    out['X']=''.join('%x'%s for s in S)
    out['XB']=''.join(('%x'%s if len('%x'%s)%2==0 else '0%x'%s) for s in S)
    out['Xc']=','.join('%x'%s for s in S)
    return out
strs=set()
cnt=0
for en,M in EE.items():
    for ln,S in matrix_lists(M).items():
        cnt+=1
        for fn,s in forms2(S).items():
            for rv in (0,1):
                t=s[::-1] if rv else s
                if 3<=len(t)<=400: strs.add(t)
        # remainder forms
        for p in (2,5,7,10,26):
            r=[x%p for x in S]; d=''.join(map(str,r)); strs.add(d)
            strs.add(''.join(chr(97+x%26) for x in r)); strs.add(''.join('o' if x==0 else chr(96+x) for x in r if x<10))
strs={s for s in strs if len(s)>=3}
print('lists',cnt,'strings',len(strs))
open('msl_rgb.txt','w').write('\n'.join(sorted(strs))+'\n')
