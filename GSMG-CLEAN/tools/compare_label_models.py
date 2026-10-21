"""Bounded intermediate-only label audit. No password or AES search."""
import hashlib
import json
import re
from pathlib import Path
from audit_dbbi_prime_grammar import parse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'runs/2026-09-13_label_models'
TR = str.maketrans('abcdefghio', '1234567890')

def unpack(s):
    n = int(s.translate(TR))
    return n.to_bytes((n.bit_length()+7)//8, 'big')

def pack(b):
    return str(int.from_bytes(b, 'big')).translate(str.maketrans('1234567890','abcdefghio'))

def ascii_decimal_paths(s):
    # Exact complete parses as concatenated decimal printable-ASCII codes.
    digits = s.translate(TR)
    ways = [0]*(len(digits)+1)
    ways[0] = 1
    for i in range(len(digits)):
        if not ways[i]:
            continue
        for size in (2,3):
            part = digits[i:i+size]
            if len(part)==size and part[0]!='0' and 32<=int(part)<=126:
                ways[i+size] += ways[i]
    return ways[-1]

def main():
    OUT.mkdir(exist_ok=True)
    paths = ['data/salphaseion_compact_1075.txt','data/DBBI_91.txt',
             'data/FAED_570.txt','data/architect_plaintext_readable.txt',
             'reference_texts/matrix_reloaded_architect_scene_scott_manning.md']
    sources = {p:(ROOT/p).read_text(encoding='utf-8').strip() for p in paths}
    sal, dbbi, faed, puzzle, movie = [sources[p] for p in paths]
    assert sal[:91]==dbbi and sal[195:765]==faed
    labels = [(766,829,'lastwordsbeforearchichoice'),(830,859,'thispassword')]
    for a,b,label in labels:
        assert unpack(sal[a:b])==label.encode()
        assert pack(label.encode())==sal[a:b]
    assert ascii_decimal_paths('gfgg') == 1  # 76 77 -> LM
    # Decide models and success criteria before calculating unknown outputs.
    manifest = {
        'models': [
            {'id':'trailing_labels_direct','claim':'DBBI and FAED encode the phrases immediately following them',
             'test':'Apply the demonstrated whole-decimal byte codec, and compare exact source quotations'},
            {'id':'leading_operation','claim':'matrixsumlist means ordinary row/column sums of FAED produce DBBI',
             'test':'All exact rectangular factors, positive a=1..i=9 values, decimal serialization'},
            {'id':'reverse_operation','claim':'DBBI or its complete prime parse produces FAED by ordinary matrix sums',
             'test':'All exact rectangular factors; retain distinct explicit prime treatments'},
            {'id':'separate_components','claim':'Labels identify two separately derived components',
             'test':'Structural evidence can support DBBI, but needs independent FAED decoding; no AES proxy'},
        ],
        'success':'Exact full-field reconstruction or round-trip readable source text; short fragments do not qualify',
        'source_hashes':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
        'exclusions':'No guessed passphrases, AES, arbitrary matrix permutations, moduli, or sign assignments',
        'quote_scope':'Contiguous windows of at most 300 words, at most 250 UTF-8 bytes; exact, lowercase, lowercase alphanumerics',
    }
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
    codecs = []
    for name,s in [('DBBI',dbbi),('FAED',faed)]:
        b = unpack(s)
        assert pack(b)==s
        texts = {}
        for codec in ('utf-8','ascii','cp037','cp273'):
            try:
                texts[codec]=b.decode(codec)
            except UnicodeError:
                texts[codec]=None
        codecs.append(dict(field=name,source_characters=len(s),byte_length=len(b),
                           hex=b.hex(),decodings=texts,
                           ascii_printable=sum(32<=x<=126 for x in b),
                           concatenated_printable_decimal_parses=ascii_decimal_paths(s)))
    # Every contiguous word window from the two pinned local texts. This is a
    # finite direct-encoding comparison, NOT a semantic claim every window is a clue.
    windows=[]
    target_lengths={target:len(unpack(target)) for target in (dbbi,faed)}
    for name,text in [('puzzle',puzzle),('movie',movie)]:
        # Strip Markdown role markers while keeping punctuation within words.
        text=re.sub(r'\*\*[^\n]*?:\*\*', '',text)
        tokens=list(re.finditer(r'\S+',text))
        for i in range(len(tokens)):
            for j in range(i,min(i+300,len(tokens))):
                value=text[tokens[i].start():tokens[j].end()]
                for form,v in [('exact',value),('lower',value.lower()),
                               ('connected',re.sub('[^a-z0-9]','',value.lower()))]:
                    raw=v.encode()
                    if len(raw)>250:
                        continue
                    for field,target in [('DBBI',dbbi),('FAED',faed)]:
                        # Whole-decimal encoding fixes byte length, a necessary gate.
                        if len(raw)!=target_lengths[target]:
                            continue
                        encoded=pack(raw)
                        windows.append(dict(source=name,first_word=i,last_word=j,form=form,
                                            field=field,text=v,exact_match=encoded==target))
    matrix=[]
    arrays=[('FAED_digits',[int(c.translate(TR)) for c in faed],dbbi),
            ('DBBI_digits',[int(c.translate(TR)) for c in dbbi],faed)]
    parses=parse(dbbi,'e')
    for p in parses:
        for treatment in ('marker_digits','prime_index','prime_zero','prime_remove'):
            vals=[]
            for slot,offset,token,prime in p:
                if prime and treatment=='prime_remove':
                    continue
                vals.append((slot if treatment=='prime_index' else 0 if treatment=='prime_zero'
                             else int(token.translate(TR))) if prime else int(token.translate(TR)))
            arrays.append((f'DBBI_{len(p)}_{treatment}',vals,faed))
    for name,vals,target in arrays:
        for width in range(1,len(vals)+1):
            if len(vals)%width:
                continue
            rows=[sum(vals[i:i+width]) for i in range(0,len(vals),width)]
            cols=[sum(vals[i::width]) for i in range(width)]
            for axis,seq in [('rows',rows),('cols',cols),('rows_then_cols',rows+cols),('cols_then_rows',cols+rows)]:
                digits=''.join(map(str,seq))
                matrix.append(dict(input=name,width=width,height=len(vals)//width,axis=axis,
                                   sums=seq,decimal_length=len(digits),target_length=len(target),
                                   exact_match=digits==target.translate(TR)))
    result=dict(codec_results=codecs,
                quote_comparisons=len(windows),quote_matches=[w for w in windows if w['exact_match']],
                matrix_comparisons=len(matrix),matrix_matches=[m for m in matrix if m['exact_match']],
                matrix_length_matches=[m for m in matrix if m['decimal_length']==m['target_length']],
                parse_summaries=[dict(cells=len(p),prime_cells=sum(t[3] for t in p),
                                     b=sum(t[3] and t[2]=='b' for t in p),be=sum(t[3] and t[2]=='be' for t in p)) for p in parses])
    for file,data in [('results.json',result),('matrix_checks.json',matrix),('quote_checks.json',windows)]:
        (OUT/file).write_text(json.dumps(data,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
