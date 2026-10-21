"""Extract the original poster and compare whole marker schedules to DBBI."""
import hashlib
import json
from collections import Counter
from pathlib import Path

from PIL import Image
from audit_dbbi_prime_grammar import parse

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-13_offwhite_alignment'
PALETTE={(0,0,0):'K',(255,255,255):'W',(63,72,204):'B',(255,242,0):'Y',(254,254,254):'F'}


def prime(n):
    return n>1 and all(n%d for d in range(2,int(n**.5)+1))


def extract():
    path=ROOT/'originals/poster/puzzle.png'
    im=Image.open(path).convert('RGB')
    order=[]; seen=set(); row=col=direction=0
    directions=((1,0),(0,1),(-1,0),(0,-1))
    for index in range(196):
        box=(75*col,75*row,min(75*(col+1),1047),min(75*(row+1),1047))
        crop=im.crop(box)
        counts=Counter(crop.get_flattened_data())
        rgb,count=counts.most_common(1)[0]
        assert rgb in PALETTE
        order.append(dict(index=index,row=row,column=col,box=box,rgb=rgb,color=PALETTE[rgb],
                          modal_pixels=count,total_pixels=crop.width*crop.height,
                          center_rgb=im.getpixel((75*col+37,75*row+37))))
        seen.add((row,col))
        nr,nc=row+directions[direction][0],col+directions[direction][1]
        if not(0<=nr<14 and 0<=nc<14) or (nr,nc) in seen:
            direction=(direction+1)%4
            nr,nc=row+directions[direction][0],col+directions[direction][1]
        row,col=nr,nc
    assert len(seen)==196
    return order,hashlib.sha256(path.read_bytes()).hexdigest()


def guided_parse(s, schedule):
    """No b/be branching: the independently supplied schedule specifies tokens."""
    at=0; slot=1; marker=0; cells=[]
    while at<len(s):
        is_prime=prime(slot)
        if is_prime:
            if marker==len(schedule):
                return dict(complete=False,reason='schedule exhausted',slot=slot,offset=at,cells=cells)
            token='b' if schedule[marker]=='B' else 'be'
            if not s.startswith(token,at):
                return dict(complete=False,reason='token disagreement',slot=slot,offset=at,
                            ordinal=marker+1,expected=token,actual=s[at:at+len(token)],cells=cells)
            marker+=1
        else:
            token=s[at]
        cells.append(dict(slot=slot,offset=at,token=token,prime=is_prime))
        at+=len(token);slot+=1
    return dict(complete=True,logical_cells=len(cells),source_chars=at,markers_used=marker,
                remaining_schedule=schedule[marker:],cells=cells)


def main():
    OUT.mkdir(exist_ok=True)
    grid,image_hash=extract()
    bits=''.join('1' if x['color'] in 'KB' else '0' for x in grid)
    decoded=bytes(int(bits[i:i+8],2) for i in range(0,192,8))
    assert decoded==b'gsmg.io/theseedisplanted' and bits[192:]=='0000'
    assert bits==(ROOT/'data/poster_spiral_bits.txt').read_text().splitlines()[0]
    marked=[dict(**x,ordinal=i+1) for i,x in enumerate(x for x in grid if x['color'] not in 'KW')]
    original=''.join(x['color'] for x in marked if x['color']!='F')
    specials=''.join(x['color'] for x in marked)
    offwhite=[x for x in grid if x['color']=='F']
    assert len(marked)==25 and len(offwhite)==1
    f=offwhite[0]
    assert f['index']==163 and f['modal_pixels']==f['total_pixels']==5625
    assert f['center_rgb']==(254,254,254)
    assert marked[20]['color']=='F' and marked[20]['index']==163
    assert marked[21]['color']=='Y' and marked[21]['index']==167
    assert all(tuple(x['rgb'])==tuple(x['center_rgb']) for x in marked)
    dbbi=(ROOT/'data/DBBI_91.txt').read_text().strip()
    parses=parse(dbbi,'e')
    expected={len(p):''.join('B' if t=='b' else 'Y' for _,_,t,pr in p if pr) for p in parses}
    byte_override=''.join(('B' if color=='Y' else 'Y') if i==f['index']//8 else color for i,color in enumerate(original))
    schedules={'ignore_offwhite':original,'serial_offwhite_B':specials.replace('F','B'),
               'serial_offwhite_Y':specials.replace('F','Y'),
               'per_byte_xor_offwhite_flag':byte_override}
    blue_component_schedule=''.join('B' if cell['rgb'][2]>0 else 'Y' for cell in marked)
    assert blue_component_schedule==schedules['serial_offwhite_B']
    comparisons=[]
    guided={}
    for rule,schedule in schedules.items():
        guided[rule]=guided_parse(dbbi,schedule)
        for length,target in expected.items():
            differences=[i+1 for i,(a,b) in enumerate(zip(schedule,target)) if a!=b]
            comparisons.append(dict(rule=rule,logical_cells=length,schedule=schedule,compared=len(target),
                                    matched=len(target)-len(differences),mismatch_ordinals=differences,
                                    unmatched_poster_suffix=schedule[len(target):]))
    exact=guided['serial_offwhite_B']
    assert exact['complete'] and exact['logical_cells']==83 and exact['markers_used']==23
    assert exact['remaining_schedule']=='BY'
    assert guided['per_byte_xor_offwhite_flag']['complete'] and guided['per_byte_xor_offwhite_flag']['logical_cells']==84
    assert not guided['ignore_offwhite']['complete'] and not guided['serial_offwhite_Y']['complete']
    payload=''.join(c['token'] for c in exact['cells'] if not c['prime'])
    assert len(payload)==60
    rebuilt=[]; index=0; marker=0
    for slot in range(1,84):
        if prime(slot):
            rebuilt.append('b' if schedules['serial_offwhite_B'][marker]=='B' else 'be');marker+=1
        else:
            rebuilt.append(payload[index]);index+=1
    assert ''.join(rebuilt)==dbbi and index==60 and marker==23
    ownership=[i for cell in exact['cells'] for i in range(cell['offset'],cell['offset']+len(cell['token']))]
    assert ownership==list(range(91))
    wrapper=(ROOT/'data/salphaseion_compact_1075.txt').read_text().strip()
    continuation=guided_parse(wrapper[:195],schedules['serial_offwhite_B'])
    assert not continuation['complete'] and continuation['slot']==97 and continuation['offset']==104
    # Transfer test for this exact rule, with original colours held fixed:
    # a hypothetical extra blue marker elsewhere need not fit; save all positions
    # rather than claim the selected location is uniquely identified by the text.
    possible_insertions=[]
    for i in range(len(original)+1):
        for value in 'BY':
            result=guided_parse(dbbi,original[:i]+value+original[i:])
            if result['complete']:
                possible_insertions.append(dict(before_regular_marker=i+1,value=value,logical_cells=result['logical_cells']))
    # Check the simplest actual-poster sum-list bridge, using the new marker
    # interpretation, and compare entire payloads. No passwords or score gates.
    ps=[n for n in range(2,101) if prime(n)]
    sums=[]
    target_digits=payload.translate(str.maketrans('abcdefghi','123456789'))
    for used in (23,25):
        for mode in ('unsigned','blue_negative','yellow_negative','blue_only','yellow_only'):
            board=[[0]*14 for _ in range(14)]
            for i,cell in enumerate(marked[:used]):
                color=schedules['serial_offwhite_B'][i]
                v=ps[i]
                if mode=='blue_negative' and color=='B' or mode=='yellow_negative' and color=='Y':v=-v
                if mode=='blue_only' and color!='B' or mode=='yellow_only' and color!='Y':v=0
                board[cell['row']][cell['column']]=v
            rows=[sum(row) for row in board]
            cols=[sum(board[r][c] for r in range(14)) for c in range(14)]
            for name,values in [('rows',rows),('columns',cols),('rows_columns',rows+cols),('columns_rows',cols+rows)]:
                digits=''.join(map(str,values))
                sums.append(dict(markers=used,mode=mode,axis=name,values=values,digits=digits,
                                 equals_complete_payload=digits==target_digits))
    summary=dict(status='Exact serial-marker alignment found; intended rule and next operation not established',
                 image_sha256=image_hash,dbbi_sha256=hashlib.sha256(dbbi.encode()).hexdigest(),
                 grid_census=dict(Counter(x['color'] for x in grid)),url=decoded.decode(),
                 full_special_stream=specials,original_color_stream=original,offwhite=f,
                 comparisons=comparisons,serial_rule='In the proven spiral order, keep every cell whose modal RGB is neither pure black nor pure white; encode yellow as be and the other marked cells as b.',
                 inference='F -> b is hypothesized, not a statement that FEFEFE is visually blue.',
                 consistent_rgb_rule='After excluding pure black/white cells, positive blue channel maps to b; zero blue channel maps to be. This yields the same schedule, but intent is unproven.',
                 chosen_parse=dict(logical_cells=83,source_characters=91,prime_cells=23,b=15,be=8,
                                   payload_characters=60,payload=payload,payload_digits=target_digits,
                                   final_token=exact['cells'][-1],roundtrip=True),
                 remaining_markers=marked[23:],next_primes=ps[23:25],
                 alternative_complete_rule='The earlier per-byte XOR of the off-white flag also matches, but selects 84 cells. The alignment alone cannot distinguish the two.',
                 hypothetical_insertion_matches=possible_insertions,
                 sum_bridge_models=len(sums),sum_bridge_matches=[r for r in sums if r['equals_complete_payload']],
                 controls_passed=True)
    for name,data in [('summary.json',summary),('grid.json',grid),('marked_cells.json',marked),
                      ('guided_parses.json',guided),('poster_sum_bridge.json',sums),('continuation_check.json',continuation)]:
        (OUT/name).write_text(json.dumps(data,indent=2),encoding='utf-8')
    # Preserve the payload as a distinct derived artifact; do not rename it a key.
    (OUT/'payload_60.txt').write_text(payload+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('offwhite','remaining_markers')},indent=2))
    print(json.dumps(dict(offwhite=f,remaining_markers=marked[23:]),indent=2))


if __name__=='__main__':
    main()
