"""Independent exact-arithmetic checks of retained results and accelerator bounds."""
from reconstruct import *
import random
rng=random.Random(20261015);receipts=[]
# Alternative explicit coordinate decoder / encoder.
coords=[divmod(square.index(c),5) for c in faed]
row=[square[coords[i][0]*5+coords[i+285][0]] for i in range(285)]
col=[square[coords[i][1]*5+coords[i+285][1]] for i in range(285)]
assert ''.join(a+b for a,b in zip(row,col))==bif
assert ''.join(row)==bif[::2] and ''.join(col)==bif[1::2]
assert ''.join(col).startswith('tsedom') and bif.startswith('btcseed')
assert ''.join(row[:4])=='bced'
receipts.append('BTCSEED is interleaved; it is NOT a prefix of the column stream alone')
# First eight free row bits in paired order are the fixed header byte 0x6c.
q=[coords[i][0] for j in range(285) for i in (j,j+285) if coords[i][1]!=4]
assert len(q)==512 and q[:8]==[0,1,1,0,1,1,0,0]
assert len(q[8:])==504
receipts.append('512 alphabet-free row bits include eight BTCSEED header bits; payload is 504 bits')
# 3x3 linear obstruction independent of search/scorer.
C1=[A.index(c) for c in carrier[:3]];C3=[A.index(c) for c in carrier[6:9]]
assert all((b-4*a)%5==0 for a,b in zip(C1,C3))
assert [4*A.index(c)%5 for c in 'ifi']!=[A.index(c)%5 for c in 'ubt']
receipts.append('IFINDOUBT impossible under any linear 3x3 natural25 A0 key, by mod5 invariant')
# Exact-arithmetic audit of all C++ retained radix outputs (not a fresh exhaustive run).
coef=int((R/'radix_coef.txt').read_text());num=9**550;den=256**219
assert coef==num*(1<<64)//den
bound_cases=0
for p in [0,1,9**20-2,9**20-1]+[rng.randrange(9**20) for _ in range(5000)]:
 lo=p*coef>>64;hi=((p+1)*coef>>64)+1
 for tail in [0,num-1,rng.randrange(num)]:
  actual=(p*num+tail)//den
  assert lo<=actual<=hi
  bound_cases+=1
assert 9**20<2**64 and 9**570<2**(29*64)
receipts.append(f'Conservative C++ prefix bounds: proof constants and {bound_cases} exact boundary/random cases')
retained=0;real_complete=[];controls=[]
for mode in ['ring','01','12','22']:
 def add(x,y):return (x+y)%9 if mode=='ring' else (x%3+y%3)%3+3*((x//3+y//3)%3)
 def mul(x,y):
  if mode=='ring':return x*y%9
  b,c=map(int,mode);x0,x1=x%3,x//3;y0,y1=y%3,y//3
  return (x0*y0-c*x1*y1)%3+3*((x0*y1+x1*y0-b*x1*y1)%3)
 models=dict(line.split() for line in (R/f'radix_models_{mode}.txt').read_text().splitlines())
 for line in (R/f'radix_scan_{mode}.tsv').read_text().splitlines():
  name,key,prefix,size,hx=line.split('\t');v=list(map(int,models[name]));k=list(map(int,key));ds=[]
  for i in range(0,570,3):
   for j in range(3):
    z=0
    for a,b in zip(k[j*3:j*3+3],v[i:i+3]):z=add(z,mul(a,b))
    ds.append(z)
  n=0
  for d in ds:n=9*n+d
  raw=n.to_bytes((n.bit_length()+7)//8,'big');assert raw.hex()==hx and len(raw)==int(size)
  p=0
  for x in raw:
   if not(x in (9,10,13) or 32<=x<=126):break
   p+=1
  assert p==int(prefix)
  if p==len(raw):
   if name=='forward_control':
    assert raw.decode()==json.loads((R/'radix_control.json').read_text())['plaintext'];controls.append(mode)
   else:real_complete.append(line)
  retained+=1
assert set(controls)=={'ring','01','12','22'} and not real_complete
receipts.append(f'{retained} retained accelerated outputs exactly reproduced with Python arbitrary-precision arithmetic; four forward controls recovered')
# Cryptographic test ledgers must retain every padding-only output and report zero exact matches.
fr=json.loads((R/'free_rows.json').read_text());rp=json.loads((R/'row_payload.json').read_text())
assert not fr['prize_hits'] and not rp['prize_hits']
for output in fr['aes_padding_outputs']+rp['padding_outputs']:
 assert not output['all_text'];assert bytes.fromhex(output['plaintext_hex'])
result=dict(passed=True,receipts=receipts,radix_retained_outputs=retained,radix_bound_cases=bound_cases,free_row_full=dict(materials=fr['distinct_materials'],roots=fr['distinct_roots'],paths=fr['paths_per_root'],checks=fr['point_checks'],aes=fr['aes_trials']),free_row_payload=dict(materials=rp['distinct_materials'],checks=rp['extra_point_checks'],aes=rp['aes_trials']))
(R/'audit.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
