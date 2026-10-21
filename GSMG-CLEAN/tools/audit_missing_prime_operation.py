"""Search original creator messages and preserve source context for the missing operation."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-13_missing_prime_operation'
OUT.mkdir(exist_ok=True)
def flat(t):
    return t if isinstance(t,str) else ''.join(v if isinstance(v,str) else v.get('text','') for v in t)
messages=json.loads((ROOT/'telegram/ChatExport_2026-09-13_result.json').read_text(encoding='utf-8'))['messages']
by={m['id']:m for m in messages}
pattern=re.compile(r'zero|sum|subtract|addition|minus|shift|rotate|reverse|opposite|red|white|blue|yellow|superposition',re.I)
hits=[m for m in messages if m.get('from_id')=='user9815232' and not m.get('forwarded_from') and pattern.search(flat(m.get('text','')))]
selected={1710,4105,6250,6884,6913,7528,7529,8000,8330,8446,23155,23159,32600,32613,32715,
          66907,66916,66917,66931,66938,70258,70262}
for m in hits:
    if m.get('reply_to_message_id') in by:
        selected.add(m['reply_to_message_id'])
(OUT/'creator_operational_search.json').write_text(json.dumps(hits,indent=2,ensure_ascii=True))
(OUT/'contexts.json').write_text(json.dumps([by[i] for i in sorted(selected) if i in by],indent=2,ensure_ascii=True))
url=b'gsmg.io/theseedisplanted'
cases=[]
for mask in (0,1,16,17):
    v=url[20]^mask
    cases.append(dict(mask_hex=hex(mask),before=url[20],after=v,lsb=v&1,
                      display=chr(v) if 32<=v<127 else 'DEL' if v==127 else 'nonprintable'))
assert url[20]==110 and url[20]^17==127 and url[20]^1==111
out=dict(creator_keyword_hits=len(hits),bit_cases=cases,
         distinction='Both masks 0x01 and 0x11 make the marker bit blue/1; only 0x11 also changes the off-white bit.',
         status='No uniquely source-selected correction or signed-prime rule established.')
(OUT/'bit_constraint_check.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
