"""Prepared during the initial review. Partitions was run in the hash-scope follow-up.
Transpose has now run; see TRANSPOSE_REPORT.md. The digit-map hypothesis has
now run without the printable filter in mapping_boards.py; see MAPPING_BOARDS_REPORT.md.
python review_leads/next_tests.py transpose
python review_leads/next_tests.py partitions
python review_leads/next_tests.py digit-map
"""
import argparse,itertools,json
from run_new_leads import ROOT,OUT,S,RESULT,test,sha,decimal_views

def columnar(text,key,decrypt):
    width=len(key); order=sorted(range(width),key=lambda i:(key[i],i))
    if not decrypt:return ''.join(text[i::width] for i in order)
    columns={};at=0
    for i in order:
        length=len(range(i,len(text),width));columns[i]=text[at:at+length];at+=length
    return ''.join(columns[i%width][i//width] for i in range(len(text)))

def board(digits):
    cells={
        '0':'F','2':'U','3':'B','5':'C','6':'D','7':'O','8':'R','9':'A'}
    cells.update({'1'+str(i):c for i,c in enumerate('.LETHINGKY')})
    cells.update({'4'+str(i):c for i,c in enumerate('MVPS/JQZXW')})
    out=[];i=0
    while i<len(digits):
        n=2 if digits[i] in '14' else 1
        token=digits[i:i+n]
        if token not in cells:return None
        out.append(cells[token]);i+=n
    return ''.join(out)

def transposition():
    keys=('matrixsumlist','thematrixhasyou','lastwordsbeforearchichoice','fubcdoraclethingkymvps')
    for name,text in [('r1',S[:91]),('r2',S[195:765])]:
        for rev in (False,True):
            source=text[::-1] if rev else text
            for key in keys:
                for decrypt in (False,True):
                    moved=columnar(source,key,decrypt)
                    digits=moved.translate(str.maketrans('abcdefghi','123456789'))
                    label=f'{name}/reverse={rev}/key={key}/decrypt={decrypt}'
                    yield from decimal_views(label,digits)
                    decoded=board(digits)
                    if decoded:
                        for v in (decoded,decoded.lower()):yield label+'/known-board',v

def parts():
    return ['causality','Safenet','Luna','HSM','11110',
            '0x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854',
            'B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1']

def partitions():
    p=parts()
    # Each nonzero six-bit mask divides the seven answers into >=2 contiguous groups.
    # The one-group mask would just repeat an already-tested whole-answer double hash.
    for mask in range(1,64):
        groups=[p[0]]
        for i,part in enumerate(p[1:]):
            if mask>>i&1:groups.append(part)
            else:groups[-1]+=part
        digests=[sha(g.encode()) for g in groups]
        for form in ('raw','hex'):
            pieces=[d if form=='raw' else d.hex().encode() for d in digests]
            for weave in (False,True):
                candidate=(bytes(v for col in zip(*pieces) for v in col) if weave else b''.join(pieces))
                yield f'cut-mask={mask:06b}/{form}/interleave={weave}',candidate

def digit_map():
    # Preserve only the mappings actually spelled out by shabef=sha256.
    # a,c,d,g,h,i map injectively to remaining six of seven decimal digits.
    free='acdghi';available='0134789';counts={'maps':0,'whole_number_decodes':0};readable=[]
    for values in itertools.permutations(available,6):
        mp={'b':'2','e':'5','f':'6',**dict(zip(free,values))};counts['maps']+=1
        label=''.join(mp[c] for c in 'abcdefghi')
        for name,source in [('r1',S[:91]),('r2',S[195:765])]:
            for rev in (False,True):
                digits=''.join(mp[c] for c in (source[::-1] if rev else source))
                n=int(digits);b=n.to_bytes(max(1,(n.bit_length()+7)//8),'big');counts['whole_number_decodes']+=1
                if all(32<=c<127 or c in (9,10,13) for c in b):
                    readable.append(dict(mapping=mp,run=name,reverse=rev,text=b.decode('ascii')))
                    yield f'{label}/{name}/reverse={rev}',b
    RESULT['digit_map_constraints']=dict(**counts,printable_decodings=readable)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['transpose','partitions','digit-map']);args=ap.parse_args()
    dest=OUT/f'next-{args.mode}-results.json'
    if dest.exists():raise SystemExit(f'{dest.name} already exists; preserve it before rerunning')
    gen={'transpose':transposition,'partitions':partitions,'digit-map':digit_map}[args.mode]
    test('next-'+args.mode,gen())
    dest.write_text(json.dumps(RESULT,indent=2))
