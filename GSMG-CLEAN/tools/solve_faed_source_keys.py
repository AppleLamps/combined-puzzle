"""Test full FAED with source-defined classical keys and numerical decoding."""
import hashlib
import json
import re
import sys
import time
from pathlib import Path

from audit_dbbi_prime_grammar import parse
from restore_lossy_decimal import recover

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-14_source_cipher_keys'
sys.set_int_max_str_digits(20000)


def radix_digits(n,base):
    out=[]
    while n:n,r=divmod(n,base);out.append(r)
    return list(reversed(out or [0]))


def source_keys():
    keys={}
    def add(values,origin):
        t=tuple(values)
        if t:keys.setdefault(t,[]).append(origin)
    movie=(ROOT/'reference_texts/matrix_reloaded_architect_scene_scott_manning.md').read_text(encoding='utf-8')
    blocks=[('modified_speech',(ROOT/'data/architect_plaintext_readable.txt').read_text())]
    for i,line in enumerate(movie.splitlines(),1):
        m=re.match(r'\*\*(The Architect|Neo):\*\*\s*(.*)',line)
        if m:blocks.append((f'{m[1]}_line_{i}',m[2]))
    texts={}
    for name,t in blocks:
        words=list(re.finditer(r'\S+',t))
        for i in range(len(words)):
            last=t[words[i].start():words[-1].end()]
            for form,v in [('exact',last),('lower',last.lower()),('connected',re.sub('[^a-z0-9]','',last.lower()))]:
                texts.setdefault(v,[]).append(dict(source=name,last_words=len(words)-i,form=form))
    for t in ['matrixsumlist','lastwordsbeforearchichoice','thispassword','ourfirsthintisyourlastcommand',
              'followthewhiterabbit','thematrixhasyou','yellowblueprimes','enter','shabef','shabefanstoo']:
        texts.setdefault(t,[]).append(dict(source='demonstrated_key_or_decoded_label'))
    for name in ['DBBI_91.txt','seven_part_phase3_answer.json']:
        t=(ROOT/'data'/name).read_text().strip()
        if name.endswith('.json'):t=''.join(json.loads(t))
        texts.setdefault(t,[]).append(dict(source=name))
    for text,origins in texts.items():
        letters=re.sub('[^a-z]','',text.lower())
        for view,values in [('letters_A0',[ord(c)-97 for c in letters]),
                            ('letters_A1',[ord(c)-96 for c in letters]),
                            ('UTF8_bytes',list(text.encode())),
                            ('decimal_integer',list(map(int,str(int.from_bytes(text.encode(),'big'))))),
                            ('base9_integer',radix_digits(int.from_bytes(text.encode(),'big'),9))]:
            add(values,dict(text=text,source=origins,view=view))
    # Test the untried operation order: restore numeric primes, serialize
    # their decimal digits, THEN form an exact rectangle and sum it.
    db=(ROOT/'data/DBBI_91.txt').read_text().strip()
    digit_matrices=[]
    for p in parse(db,'e'):
        for polarity in ('unsigned','blue_negative','yellow_negative'):
            digits=[]
            for slot,offset,token,prime in p:
                value=slot if prime else ord(token)-96
                sign=-1 if prime and ((polarity=='blue_negative' and token=='b') or (polarity=='yellow_negative' and token=='be')) else 1
                digits.extend(sign*int(c) for c in str(value))
            assert len(digits)==len(p)+19
            for width in range(1,len(digits)+1):
                if len(digits)%width:continue
                for axis,values in [('rows',[sum(digits[i:i+width]) for i in range(0,len(digits),width)]),
                                    ('cols',[sum(digits[i::width]) for i in range(width)])]:
                    source=dict(parse=len(p),polarity=polarity,width=width,axis=axis,sums=values)
                    digit_matrices.append({**source,'mod26_A0':''.join(chr(97+v%26) for v in values)})
                    add(values,dict(source='decimal_prime_digits_before_matrix',**source,view='sum_entries'))
                    if min(values)>=0:add([int(c) for c in ''.join(map(str,values))],dict(source='decimal_prime_digits_before_matrix',**source,view='sum_decimal_digits'))
    return keys,texts,digit_matrices


def ascii_bytes(raw):return bool(raw) and all(32<=c<=126 or c in (9,10,13) for c in raw)


def main():
    OUT.mkdir(exist_ok=True)
    controls=[]
    planted=b'A full message with restored zeros, punctuation, and a newline.\n'
    original=[int(c) for c in str(int.from_bytes(planted,'big'))]
    key=[ord(c)-96 for c in 'matrixsumlist']
    for modulus in (9,10):
        for family,cs,ks in [('vigenere',1,-1),('beaufort',-1,1),('variant',1,1)]:
            enc=[(cs*(p-ks*key[i%len(key)]))%modulus for i,p in enumerate(original)]
            dec=[(cs*c+ks*key[i%len(key)])%modulus for i,c in enumerate(enc)]
            assert dec==[p%modulus for p in original]
            if modulus==9:
                r=recover(''.join(map(str,dec)))
                assert r['complete'] and any(x['hex']==planted.hex() for x in r['hits'])
            else:
                n=int(''.join(map(str,dec)))
                assert n.to_bytes((n.bit_length()+7)//8,'big')==planted
            controls.append(dict(modulus=modulus,family=family,complete_plaintext_recovered=True))
    (OUT/'controls.json').write_text(json.dumps(controls,indent=2))
    keys,texts,matrices=source_keys()
    # Store all origins once; each trial is then exactly reproducible by id.
    catalog=[dict(values=k,origins=origins) for k,origins in keys.items()]
    (OUT/'keys.json').write_text(json.dumps(catalog,indent=2))
    (OUT/'decimal_prime_matrices.json').write_text(json.dumps(matrices,indent=2))
    faed=(ROOT/'data/FAED_570.txt').read_text().strip()
    c=[ord(v)-96 for v in faed]
    seen=set();hits=[];unfinished=[];tests=0;nodes=0;restores=0;integer_views=0
    start=time.monotonic()
    for modulus in (9,10):
        for kid,row in enumerate(catalog):
            values=row['values']
            for reverse in (False,True):
                key=values[::-1] if reverse else values
                key=[v%modulus for v in key]
                repeated=tuple(key[i%len(key)] for i in range(570))
                for family,cs,ks in [('vigenere',1,-1),('beaufort',-1,1),('variant',1,1)]:
                    for input_base in (0,1):
                        out=tuple((cs*(x-1+input_base)+ks*y)%modulus for x,y in zip(c,repeated))
                        identity=bytes(out)
                        tag=(modulus,identity)
                        if tag in seen:continue
                        seen.add(tag);tests+=1
                        meta=dict(modulus=modulus,key_id=kid,reverse_key=reverse,family=family,input_base=input_base)
                        views=[('decimal',10,out)]
                        if modulus==9:views.extend([('base9',9,out),('bijective_base9',9,[v+1 for v in out])])
                        for name,radix,digits in views:
                            n=0
                            for digit in digits:n=n*radix+digit
                            raw=n.to_bytes((n.bit_length()+7)//8,'big');integer_views+=1
                            if ascii_bytes(raw):hits.append(dict(**meta,view=name,text=raw.decode('ascii'),hex=raw.hex()))
                        if modulus==9:
                            residues=''.join(map(str,out))
                            r=recover(residues);restores+=1;nodes+=r['nodes']
                            if not r['complete']:unfinished.append(dict(**meta,residues=residues,**r))
                            for hit in r['hits']:hits.append(dict(**meta,view='selective_zero_nine',**hit))
            if kid and kid%2000==0:print(json.dumps(dict(modulus=modulus,keys_processed=kid,tests=tests,hits=len(hits),seconds=round(time.monotonic()-start))),flush=True)
    summary=dict(source_text_keys=len(texts),numeric_key_vectors=len(keys),decimal_prime_matrix_lists=len(matrices),
                 complete_faed_transforms=tests,integer_views=integer_views,lossy_decimal_restorations=restores,
                 restoration_nodes=nodes,incomplete_restorations=len(unfinished),full_ascii_outputs=len(hits),seconds=round(time.monotonic()-start,2))
    manifest=dict(purpose='Recover a full FAED plaintext when last words serve as a classical cipher key',
                  source_scope='All complete-word suffixes of individual Architect/Neo utterances in the saved Scott Manning transcript and the modified puzzle speech; demonstrated key, labels, DBBI, solved seven-part answer',
                  extra_model='Prime numbers serialized as decimal digits BEFORE rectangular sums; both complete DBBI parses; signed alternatives explicitly hypothetical',
                  cipher_families=['Vigenere','Beaufort','variant'],moduli=[9,10],numeral_views=['decimal','base9','bijective_base9','selective 0/9 restoration'],
                  limits='This searches source keys, not every key. Whole ASCII including whitespace is the stated success format; arbitrary binary and non-ASCII intermediate formats remain unresolved.',
                  faed_sha256=hashlib.sha256(faed.encode()).hexdigest())
    for name,obj in [('manifest.json',manifest),('summary.json',summary),('matches.json',hits),('unfinished.json',unfinished)]:
        (OUT/name).write_text(json.dumps(obj,indent=2))
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
