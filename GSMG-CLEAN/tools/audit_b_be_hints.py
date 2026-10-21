"""Source-attributed b/be clue search and exact colour-marker comparison."""
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-13_b_be_hints'
OUT.mkdir(exist_ok=True)
def flat(text):
    return text if isinstance(text,str) else ''.join(x if isinstance(x,str) else x.get('text','') for x in text)
selected=[]; search_hits=[]; counts={}
ids={1710,4104,4105,4107,6884,6911,6912,6913,7528,7529,7960,7961,8000,8035,8036,
     8330,8446,12932,12933,12934,54201,54203,70262,70272,70311}
query=re.compile(r'\bb\s*(?:and|or|/|,|=)\s*be\b|to be or not|\bbee[s]?\b|'
                 r'\bb\s*=\s*2\b|\bbe\s*=\s*25\b|\b25\b.{0,30}\byellow\b|'
                 r'\byellow\b.{0,30}\b25\b|zeroed|reinserting|positive|negative',re.I)
for chat,fn in [('PUZ','ChatExport_2026-09-13_result.json'),('COMM','CommunityGroup_2026-09-10_result.json')]:
    path=ROOT/'telegram'/fn
    messages=json.loads(path.read_text(encoding='utf-8'))['messages']
    count=0
    for m in messages:
        text=flat(m.get('text',''))
        own=m.get('from_id')=='user9815232' and not m.get('forwarded_from')
        forwarded=m.get('forwarded_from')=='Jrk Bgrt'
        rec=dict(chat=chat,id=m['id'],author=m.get('from'),forwarded_from=m.get('forwarded_from'),
                 creator_original=own,creator_forward=forwarded,date=m.get('date'),
                 reply=m.get('reply_to_message_id'),text=text)
        if query.search(text):
            search_hits.append(rec); count+=1
        if (chat=='PUZ' and m['id'] in ids) or (chat=='COMM' and m['id']==28538):
            selected.append(rec)
    counts[chat]=dict(messages=len(messages),query_hits=count,source_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
(OUT/'search_hits.json').write_text(json.dumps(search_hits,indent=2,ensure_ascii=True))
(OUT/'selected_sources.json').write_text(json.dumps(selected,indent=2,ensure_ascii=True))

grammar=json.loads((ROOT/'runs/2026-09-13_dbbi_prime_prefix/grammar_results.json').read_text())
poster=(ROOT/'data/poster_spiral_bits.txt').read_text().splitlines()[1]
comparisons=[]
for p in grammar['parses']:
    markers=[]
    for slot,offset,token,prime in p['parse']:
        if not prime:
            continue
        digits=''.join(str(ord(c)-96) for c in token)
        letter=chr(int(digits)+64)
        assert letter in 'BY'
        markers.append(dict(ordinal=len(markers)+1,logical_prime=slot,source_offset=offset,
                            token=token,digits=digits,letter=letter))
    mapped=''.join(m['letter'] for m in markers)
    differences=[dict(**m,poster_color=poster[i],poster_spiral_bit_index=8*(i+1)-1)
                 for i,m in enumerate(markers) if m['letter']!=poster[i]]
    comparisons.append(dict(cells=p['cells'],mapped=mapped,poster_first23=poster[:23],
                            matched=sum(a==b for a,b in zip(mapped,poster)),differences=differences,
                            markers=markers))
result=dict(corpus=counts,mapping={'b':'2 -> B -> blue','be':'25 -> Y -> yellow'},
            comparisons=comparisons,poster_final_unpaired_color=poster[23],
            offwhite_spiral_index=163,offwhite_character_ordinal=21,
            caution='The B/Y interpretation is source-supported inference. No creator message found directly assigning signed prime values to b/be. '
                    'The mapping does not fix the marker-21 mismatch or explain the unused 24th colour.')
(OUT/'mapping_verified.json').write_text(json.dumps(result,indent=2))
print(json.dumps(dict(corpus=counts,comparisons=[{k:v for k,v in x.items() if k!='markers'} for x in comparisons]),indent=2))
