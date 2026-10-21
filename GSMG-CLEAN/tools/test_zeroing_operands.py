"""Finite source-grounded masks; intermediate evidence only, no AES/passwords."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from PIL import Image
from audit_dbbi_prime_grammar import parse

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-13_zeroing_operands'
TR=str.maketrans('abcdefghio','1234567890')
prime=lambda n:n>1 and all(n%d for d in range(2,int(n**.5)+1))

def run():
    OUT.mkdir(exist_ok=True)
    files=['data/DBBI_91.txt','data/FAED_570.txt','data/poster_spiral_bits.txt',
           'data/architect_letters_1539.txt','originals/poster/puzzle.png']
    dbbi,faed=[(ROOT/p).read_text().strip() for p in files[:2]]
    bits,colors=(ROOT/files[2]).read_text().splitlines()
    arch=(ROOT/files[3]).read_text().strip()
    manifest=dict(hint='PUZ #8000: some characters need to be zeroed out',
                  masks='One symbol class; raw prime positions; first-24 primes split by poster colour; logical DBBI prime markers by colour; poster pixel classes',
                  treatments='numeric zero per cell; zero per source digit; delete selected cells; retain selected cells; poster decoded characters NUL/ASCII-zero/deletion',
                  decodes='Whole decimal integer to big-endian bytes; complete decimal printable-ASCII segmentation; existing poster bit convention',
                  success='Complete readable output is review-only; exact full-field reconstruction or independent source relation needed for confirmation',
                  exclusions='No arbitrary subsets, shifted masks, repeating colour masks, moduli, signs, passwords or AES',
                  hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files})
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
    records=[]; prime24=[n for n in range(2,100) if prime(n)][:24]
    def record(name,vals,maskname,mask,mode):
        if mode=='cell_zero':
            seq=['0' if i in mask else v for i,v in enumerate(vals)]
        elif mode=='digit_zero':
            seq=['0'*len(v) if i in mask else v for i,v in enumerate(vals)]
        elif mode=='delete':
            seq=[v for i,v in enumerate(vals) if i not in mask]
        else:
            seq=[v for i,v in enumerate(vals) if i in mask]
        digits=''.join(seq)
        raw=(int(digits).to_bytes((int(digits).bit_length()+7)//8,'big') if digits else b'')
        # Retain leading-zero count: integer conversion loses it by definition.
        printable=bool(raw) and all(32<=b<=126 or b in (9,10,13) for b in raw)
        # Exact DP, retaining one witness but counting all complete parses.
        count=[0]*(len(digits)+1); witness=['']*(len(digits)+1); count[0]=1
        for i in range(len(digits)):
            if not count[i]: continue
            for n in (2,3):
                s=digits[i:i+n]
                if len(s)==n and s[0]!='0' and 32<=int(s)<=126:
                    count[i+n]+=count[i]; witness[i+n]=witness[i]+chr(int(s))
        records.append(dict(field=name,mask=maskname,indices_zero_based=sorted(mask),mode=mode,
                            digits=digits,leading_zeroes=len(digits)-len(digits.lstrip('0')),
                            bytes_hex=raw.hex(),ascii_printable=printable,
                            text=raw.decode('ascii') if printable else None,
                            complete_ascii_decimal_parses=count[-1] if digits else 0,
                            decimal_ascii_witness=witness[-1],
                            exact_other_field=digits==(faed if name.startswith('DBBI') else dbbi).translate(TR),
                            exact_architect_substring=bool(printable and len(raw)>=12 and raw.decode('ascii').upper() in arch)))
    for name,s in [('DBBI',dbbi),('FAED',faed)]:
        vals=list(s.translate(TR))
        masks={f'symbol_{c}':{i for i,v in enumerate(s) if v==c} for c in sorted(set(s))}
        masks['raw_prime_positions']={i for i in range(len(s)) if prime(i+1)}
        for color in 'BY':
            masks[f'poster_{color}_first24_primes']={p-1 for p,c in zip(prime24,colors) if c==color and p<=len(s)}
        for label,mask in masks.items():
            for mode in ('cell_zero','delete','retain'):
                record(name,vals,label,mask,mode)
    for p in parse(dbbi,'e'):
        vals=[t.translate(TR) for slot,offset,t,pr in p]
        masks={'logical_primes':{i for i,t in enumerate(p) if t[3]},
               'logical_blue_b':{i for i,t in enumerate(p) if t[3] and t[2]=='b'},
               'logical_yellow_be':{i for i,t in enumerate(p) if t[3] and t[2]=='be'}}
        for label,mask in masks.items():
            for mode in ('cell_zero','digit_zero','delete','retain'):
                record(f'DBBI_{len(p)}',vals,label,mask,mode)
    # Poster: reproduce the existing spiral, then apply masks in the representation
    # where colours have an actual independently verified bit meaning.
    im=Image.open(ROOT/files[-1]).convert('RGB')
    r=c=d=0; seen=set(); classes=[]; ds=[(1,0),(0,1),(-1,0),(0,-1)]
    names={(0,0,0):'black',(255,255,255):'white',(254,254,254):'offwhite',
           (63,72,204):'blue',(255,242,0):'yellow'}
    for _ in range(196):
        crop=im.crop((75*c,75*r,min(75*(c+1),1047),min(75*(r+1),1047)))
        px=crop.get_flattened_data() if hasattr(crop,'get_flattened_data') else crop.getdata()
        classes.append(names[Counter(px).most_common(1)[0][0]])
        seen.add((r,c)); nr,nc=r+ds[d][0],c+ds[d][1]
        if not(0<=nr<14 and 0<=nc<14) or (nr,nc) in seen:
            d=(d+1)%4; nr,nc=r+ds[d][0],c+ds[d][1]
        r,c=nr,nc
    assert ''.join('1' if c in ('black','blue') else '0' for c in classes)==bits
    poster=[]
    for label,mask in [(c,{i for i,v in enumerate(classes) if v==c}) for c in names.values()]+[
            ('all_coloured',{i for i,v in enumerate(classes) if v in ('blue','yellow')})]:
        for mode in ('zero','delete','retain'):
            out=''.join(('0' if i in mask else b) for i,b in enumerate(bits)) if mode=='zero' else ''.join(b for i,b in enumerate(bits) if (i in mask)==(mode=='retain'))
            n=len(out)//8*8; raw=bytes(int(out[i:i+8],2) for i in range(0,n,8))
            poster.append(dict(mask=label,indices_zero_based=sorted(mask),mode=mode,bits=out,
                               leftover_bits=out[n:],bytes_hex=raw.hex(),
                               text=raw.decode('ascii') if all(32<=b<=126 for b in raw) else None,
                               changed=out!=bits))
    # Keep a bit operation distinct from zeroing the decoded character containing it.
    url=bytes(int(bits[i:i+8],2) for i in range(0,192,8))
    byte_cases=[]
    for label in ('blue','yellow','offwhite'):
        positions={i//8 for i,v in enumerate(classes[:192]) if v==label}
        for mode in ('NUL','ASCII_zero','delete'):
            raw=(bytes(b for i,b in enumerate(url) if i not in positions) if mode=='delete'
                 else bytes((0 if mode=='NUL' else 48) if i in positions else b for i,b in enumerate(url)))
            byte_cases.append(dict(mask=label,byte_positions_zero_based=sorted(positions),mode=mode,
                                   bytes_hex=raw.hex(),escaped_ascii=raw.decode('ascii'),
                                   caveat='Readable surviving URL pieces are inherited text, not independent evidence'))
    assert next(r for r in byte_cases if r['mask']=='offwhite')['byte_positions_zero_based']==[20]
    # Existing known decode serves as a positive control; synthetic zero removal
    # verifies that preserving vs deleting zero characters are not conflated.
    assert bytes(int(bits[i:i+8],2) for i in range(0,192,8))==b'gsmg.io/theseedisplanted'
    record('CONTROL',['6','0','5','6','6'],'remove_zero',{1},'delete')
    assert records[-1]['decimal_ascii_witness']=='AB'
    control=records.pop()
    summary=dict(field_cases=len(records),poster_cases=len(poster),poster_character_cases=len(byte_cases),
                 readable_field_outputs=[r for r in records if r['ascii_printable'] or r['complete_ascii_decimal_parses']],
                 exact_matches=[r for r in records if r['exact_other_field'] or r['exact_architect_substring']],
                 printable_poster_outputs=[r for r in poster if r['text'] is not None],
                 positive_control=control,
                 status='All outputs retained; readability and unchanged outputs do not authenticate a mask')
    for name,data in [('field_outputs.json',records),('poster_outputs.json',poster),
                      ('poster_character_outputs.json',byte_cases),('summary.json',summary)]:
        (OUT/name).write_text(json.dumps(data,indent=2))
    print(json.dumps(summary,indent=2))

if __name__=='__main__': run()
