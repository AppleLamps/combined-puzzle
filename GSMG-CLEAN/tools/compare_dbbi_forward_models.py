"""Two lossless DBBI endpoint models and full-field forward predictions. Offline.

Fresh outputs only. No AES, password generation, or readability acceptance.
Model under test: FAED matrix margins -> decimal digit letters -> ordinary payload
-> poster-guided prime-marker insertion -> exact DBBI. Intent remains hypothetical.
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
PALETTE={(0,0,0):'K',(255,255,255):'W',(63,72,204):'B',(255,242,0):'Y',(254,254,254):'F'}
DIG=str.maketrans('abcdefghio','1234567890')
LET=str.maketrans('1234567890','abcdefghio')

def sha(b): return hashlib.sha256(b).hexdigest()
def prime(n): return n>1 and all(n%d for d in range(2,int(n**.5)+1))

def poster(path):
    im=Image.open(path).convert('RGB'); seen=set();r=c=d=0;grid=[]
    dirs=((1,0),(0,1),(-1,0),(0,-1))
    for i in range(196):
        crop=im.crop((75*c,75*r,min(75*(c+1),1047),min(75*(r+1),1047)))
        pixels=crop.get_flattened_data() if hasattr(crop,'get_flattened_data') else crop.getdata()
        rgb=Counter(pixels).most_common(1)[0][0]
        grid.append(dict(spiral=i,row=r,column=c,rgb=list(rgb),colour=PALETTE[rgb]))
        seen.add((r,c));nr,nc=r+dirs[d][0],c+dirs[d][1]
        if not(0<=nr<14 and 0<=nc<14) or (nr,nc) in seen:
            d=(d+1)%4;nr,nc=r+dirs[d][0],c+dirs[d][1]
        r,c=nr,nc
    return grid

def schedules(grid):
    specials=[g for g in grid if g['colour'] not in 'KW']
    regular=[g for g in specials if g['colour']!='F']
    flags={g['spiral']//8 for g in specials if g['colour']=='F'}
    serial=[dict(**g,token='be' if g['colour']=='Y' else 'b') for g in specials]
    perbyte=[]
    for g in regular:
        blue=(g['colour']=='B') ^ (g['spiral']//8 in flags)
        perbyte.append(dict(**g,offwhite_flag=g['spiral']//8 in flags,token='b' if blue else 'be'))
    return {'serial83':serial,'perbyte84':perbyte}

def parse(text,schedule,start_slot=1,start_marker=0):
    at=0;slot=start_slot;mi=start_marker;cells=[]
    while at<len(text):
        p=prime(slot)
        if p and mi>=len(schedule):
            return dict(complete=False,reason='schedule exhausted',slot=slot,offset=at,cells=cells,marker=mi)
        token=schedule[mi]['token'] if p else text[at]
        if not text.startswith(token,at):
            return dict(complete=False,reason='marker disagreement',slot=slot,offset=at,
                        expected=token,actual=text[at:at+len(token)],cells=cells,marker=mi)
        cell=dict(slot=slot,start=at,end=at+len(token),token=token,prime=p,
                  marker_ordinal=mi+1 if p else None)
        cells.append(cell);at+=len(token);slot+=1;mi+=p
    return dict(complete=True,cells=cells,logical_cells=slot-start_slot,marker=mi,
                payload=''.join(c['token'] for c in cells if not c['prime']),remaining=schedule[mi:])

def insert(payload,schedule,endpoint):
    needed=sum(not prime(i) for i in range(1,endpoint+1))
    if len(payload)!=needed: return None
    out=[];j=mi=0
    for slot in range(1,endpoint+1):
        if prime(slot):
            if mi>=len(schedule): return None
            out.append(schedule[mi]['token']);mi+=1
        else:out.append(payload[j]);j+=1
    assert j==len(payload)
    return ''.join(out)

def margins(vals,width):
    assert len(vals)%width==0
    rows=[sum(vals[i:i+width]) for i in range(0,len(vals),width)]
    cols=[sum(vals[i::width]) for i in range(width)]
    assert sum(rows)==sum(cols)==sum(vals)
    return rows,cols

def proposals(vals):
    for width in range(1,len(vals)+1):
        if len(vals)%width:continue
        rows,cols=margins(vals,width)
        for axis,nums in [('rows',rows),('columns',cols),('rows_columns',rows+cols),('columns_rows',cols+rows)]:
            for reverse in [False,True]:
                seq=nums[::-1] if reverse else nums
                digits=''.join(map(str,seq))
                yield dict(shape=[len(vals)//width,width],axis=axis,reverse=reverse,
                           sums=seq,payload=digits.translate(LET),digits=digits)

def build_models(text,ss):
    models={}
    for name,schedule in ss.items():
        p=parse(text,schedule)
        assert p['complete']
        assert [i for c in p['cells'] for i in range(c['start'],c['end'])]==list(range(len(text)))
        assert insert(p['payload'],schedule,p['logical_cells'])==text
        p['schedule']=schedule
        models[name]=p
    return models

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',required=True,type=Path)
    args=ap.parse_args();out=args.out.resolve();out.mkdir(parents=True,exist_ok=False)
    paths=[ROOT/'originals/poster/puzzle.png',ROOT/'originals/pages/salphaseion_phase3.html',
           ROOT/'data/DBBI_91.txt',ROOT/'data/FAED_570.txt']
    manifest=dict(inputs={str(p):sha(p.read_bytes()) for p in paths},
        primary_test='complete FAED-derived margins -> prime insertion -> 91-character DBBI',
        representations=['FAED a=1..i=9 values','FAED whole-decimal-integer unsigned bytes'],
        scope='all exact rectangular factors, rows/columns/both orders, forward/reverse; unpadded decimal serialization',
        controls='planted forward full-field recovery and terminal mutation',
        exclusions=['no selected ciphertext edits','no arbitrary dimensions/padding/moduli','no AES/password generation'],
        prior_overlap=['poster sums -> payload already tested; not rerun here',
                       'FAED sums -> literal DBBI already tested; new target is ordinary payload plus explicit insertion',
                       'marker continuation regression is not a new discovery'],network=False,aes_decryptions=0)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    grid=poster(paths[0]);bits=''.join('1' if g['colour'] in 'KB' else '0' for g in grid)
    assert bytes(int(bits[i:i+8],2) for i in range(0,192,8))==b'gsmg.io/theseedisplanted'
    bodies=re.findall(r'<textarea[^>]*>(.*?)</textarea>',paths[1].read_text(encoding='utf-8'),re.S)
    s=re.sub(r'\s+','',bodies[0]);dbbi=s[:91];faed=s[195:765]
    assert dbbi==paths[2].read_text().strip() and faed==paths[3].read_text().strip()
    ss=schedules(grid);models=build_models(dbbi,ss)
    assert models['serial83']['logical_cells']==83 and models['perbyte84']['logical_cells']==84
    # Exact endpoint relation, with all shared cells compared including source offsets.
    left,right=models['serial83'],models['perbyte84']
    shared=0
    for a,b in zip(left['cells'],right['cells']):
        if a!=b:break
        shared+=1
    assert shared==82 and right['payload']==left['payload']+'e'
    literal_digits=[int(c.translate(DIG)) for c in faed]
    n=int(faed.translate(DIG));raw=n.to_bytes((n.bit_length()+7)//8,'big')
    comparisons=[]
    for rep,vals in [('digit_values',literal_digits),('decimal_integer_bytes',list(raw))]:
        for p in proposals(vals):
            for name,m in models.items():
                predicted=insert(p['payload'],m['schedule'],m['logical_cells'])
                comparisons.append(dict(representation=rep,model=name,**p,
                    required_payload_length=len(m['payload']),length_compatible=len(p['payload'])==len(m['payload']),
                    predicted_dbbi=predicted,exact_dbbi=predicted==dbbi,
                    exact_payload=p['payload']==m['payload']))
    # Adjacent material is held out of model construction. Regression tests retain
    # both original label and the alternative that skips its known encoded span.
    continuation={}
    for name,m in models.items():
        continuation[name]={label:parse(text,m['schedule'],m['logical_cells']+1,m['marker'])
                            for label,text in [('binary_label',s[91:195]),('FAED_label_skipped',faed)]}
    report=dict(models={name:dict(cells=m['logical_cells'],payload_length=len(m['payload']),
                  payload=m['payload'],prime_markers=m['marker'],remaining_tokens=[c['token'] for c in m['remaining']])
                  for name,m in models.items()},shared_prefix_cells=shared,
                endpoint_relation='84-cell ordinary payload = 83-cell payload + e; equality holds exactly',
                comparisons=len(comparisons),length_compatible=sum(r['length_compatible'] for r in comparisons),
                full_field_matches=[r for r in comparisons if r['exact_dbbi']],
                consequence='No preference follows from a shared-prefix test or an identical success/failure on held-out data.',
                ordinary_bytes_retained=True)
    for file,obj in [('models.json',models),('grid.json',grid),('forward_comparisons.json',comparisons),
                     ('continuation.json',continuation),('summary.json',report)]:
        (out/file).write_text(json.dumps(obj,indent=2),encoding='utf-8')
    with (out/'forward_outputs.jsonl').open('w',encoding='utf-8') as f:
        for i,r in enumerate(comparisons):
            f.write(json.dumps(dict(comparison=i,output=r['digits']))+'\n')
            if r['predicted_dbbi'] is not None:f.write(json.dumps(dict(comparison=i,output=r['predicted_dbbi']))+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()