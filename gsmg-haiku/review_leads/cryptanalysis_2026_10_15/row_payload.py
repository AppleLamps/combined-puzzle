from free_rows import *
base_results=json.loads((R/'free_rows.json').read_text())
materials={}
for sq in json.loads((R/'structural_tests.json').read_text())['header_squares']:
 rows=[sq.index(c)//5 for c in faed];cols=[sq.index(c)%5 for c in faed]
 for label,order in orders.items():
  # Full Bifid output header uses row positions 0,2,4,6, i.e. four source pairs.
  free=[rows[i] for i in order if cols[i]!=4 and i%285>=4]
  if len(free)!=504:continue
  for polarity,rev,lsb in itertools.product(range(2),repeat=3):
   bits=[b^polarity for b in free];bits=bits[::-1] if rev else bits
   raw=bytes(sum(b<<(i if lsb else 7-i) for i,b in enumerate(bits[j:j+8])) for j in range(0,504,8))
   name=f'{sq}/{label}/polarity={polarity}/reverse={rev}/lsb={lsb}'
   materials.setdefault(raw,[]).append(name)
roots={master(b):ls[0] for b,ls in materials.items()};checks=0;hits=[]
for root,label in roots.items():
 cache={():root}
 def resolve(p):
  if p not in cache:
   parent=resolve(p[:-1]);cache[p]=child(parent,p[-1]) if parent else None
  return cache[p]
 for p in paths:
  node=resolve(p)
  if node:check(node[0],label+'/'+pathtext(p))
 # Direct SHA256 scalar has a precise meaning, unlike padding to make 64 bytes.
for raw,names in materials.items():check(int.from_bytes(sha(raw),'big'),names[0]+'/sha256')
aes=[];trials=0
for raw,names in materials.items():
 for form,pw in [('raw',raw),('hex',raw.hex().encode()),('sha256hex',hashlib.sha256(raw).hexdigest().encode())]:
  for digest in ['sha256','md5']:
   for name,ct in containers.items():
    body=decrypt(ct,pw,digest);trials+=1
    if body is not None:aes.append(dict(source=names[0],form=form,digest=digest,container=name,plaintext_hex=body.hex(),all_text=all(x in (9,10,13) or 32<=x<=126 for x in body)))
# check() is imported, so its globals remain free_rows globals. Collect exact counter deltas.
import free_rows
result=dict(boundary='Discard four complete row symbols used by the 7-character interleaved BTCSEED header; retain all later row bits except column-forced zeros. No invented padding.',bits=504,materials=[dict(hex=b.hex(),names=ls) for b,ls in materials.items()],distinct_materials=len(materials),paths_per_seed=len(paths),extra_point_checks=free_rows.checks-base_results['point_checks'],prize_hits=free_rows.hits,aes_trials=trials,padding_outputs=aes)
(R/'row_payload.json').write_text(json.dumps(result,indent=2));print('payload504',len(materials),'materials',result['extra_point_checks'],'point checks',len(result['prize_hits']),'hits',len(aes),'padding',sum(x['all_text'] for x in aes),'text')
