"""Source-attributed instruction search, without password generation."""
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-13_operation_instructions'
OUT.mkdir(exist_ok=True)

def flat(t):
    return t if isinstance(t,str) else ''.join(x if isinstance(x,str) else x.get('text','') for x in t)

pattern=re.compile(r'prime|zero|matrix|cipher|hint|rabbit|rotat|subtract|reverse|insert|multiply|divide|column|sumlist|salph|transpose|command|source|\benter\b',re.I)
stats={}; hits=[]; contexts=[]; inventories=[]
selected={'PUZ':{1710,1837,5966,5969,6509,8000,8330,8446,11248,66961,66962},
          'COMM':{26065,26083,26108,26113,28522,35283,36714}}
for chat,fn in [('PUZ','ChatExport_2026-09-13_result.json'),('COMM','CommunityGroup_2026-09-10_result.json')]:
    path=ROOT/'telegram'/fn
    ms=json.loads(path.read_text(encoding='utf-8'))['messages']
    by={m['id']:m for m in ms}
    own=[m for m in ms if m.get('from_id')=='user9815232' and not m.get('forwarded_from')]
    forwarded=[m for m in ms if m.get('forwarded_from')=='Jrk Bgrt']
    records=[]
    for m in own+forwarded:
        r=dict(chat=chat,id=m['id'],date=m.get('date'),edited=m.get('edited'),
               provenance='forward' if m.get('forwarded_from') else 'original',
               reply=m.get('reply_to_message_id'),text=flat(m.get('text','')))
        records.append(r)
        if pattern.search(r['text']):
            hits.append(r)
    inventories.extend(records)
    wanted=set()
    for i in selected[chat]:
        wanted.update(range(i-3,i+4))
        if i in by:
            wanted.add(by[i].get('reply_to_message_id',-1))
    contexts.extend(dict(chat=chat,message=m) for m in ms if m['id'] in wanted)
    stats[chat]=dict(original_creator_messages=len(own),forwarded_creator_messages=len(forwarded),
                     search_hits=sum(pattern.search(r['text']) is not None for r in records),
                     sha256=hashlib.sha256(path.read_bytes()).hexdigest())
source_checks=[]
for p in sorted((ROOT/'originals/pages').glob('*.html')):
    text=p.read_text(encoding='utf-8')
    source_checks.append(dict(file=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                             comments=re.findall(r'<!--(.*?)-->',text,re.S),
                             script_tags=re.findall(r'<script\b[^>]*>',text,re.I)))
for name,data in [('creator_inventory.json',inventories),('search_hits.json',hits),
                  ('contexts.json',contexts),('source_checks.json',source_checks),('coverage.json',stats)]:
    (OUT/name).write_text(json.dumps(data,indent=2,ensure_ascii=True),encoding='utf-8')
print(json.dumps(stats,indent=2))
