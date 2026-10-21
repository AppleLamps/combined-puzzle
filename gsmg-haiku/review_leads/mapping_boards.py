"""Bounded alternative digit alphabets and ten-column straddling boards.
python review_leads/mapping_boards.py digit-map
python review_leads/mapping_boards.py boards
No readability filter before AES. No solved-stage decryptions.
"""
import argparse,collections,itertools,json,math,re,time
from pathlib import Path
from next_tests import S,board
from hash_scope import sha,RAW,decrypt,N,TARGET,PrivateKey,payload_candidates
from binary_envelopes import structures
OUT=Path(__file__).resolve().parent/'mapping_boards'
META=collections.Counter()
STREAMS=[(n+('/reverse' if rev else '/forward'),s[::-1] if rev else s) for n,s in [('r1',S[:91]),('r2',S[195:765])] for rev in (False,True)]

def mapping_candidates():
    for values in itertools.permutations('0134789',6):
        mp={'b':'2','e':'5','f':'6',**dict(zip('acdghi',values))};META['digit_maps']+=1
        tag=''.join(mp[c] for c in 'abcdefghi')
        for name,s in STREAMS:
            d=''.join(mp[c] for c in s);label=f'map={tag}/{name}';META['stream_decodings']+=1
            yield label+'/digits',d.encode()
            v=int(d);raw=v.to_bytes(max(1,(v.bit_length()+7)//8),'big')
            yield label+'/integer-bytes',raw
            if len(d)%2==0:yield label+'/paired-decimal',bytes(int(d[i:i+2]) for i in range(0,len(d),2))
            text=board(d)
            if text is not None:
                META['complete_fixed_board_parses']+=1
                yield label+'/fixed-board-upper',text.encode()
                yield label+'/fixed-board-lower',text.lower().encode()

def unique(s):return ''.join(dict.fromkeys(s))

def alphabets():
    base='ABCDEFGHIJKLMNOPQRSTUVWXYZ./'
    seeds=['', 'FUBCDORACLETHINGKYMVPS','MATRIXSUMLIST','THEMATRIXHASYOU',
           'LASTWORDSBEFOREARCHICHOICE','OURFIRSTHINTISYOURLASTCOMMAND','YINYANG','THISPASSWORD',
           'ESTONIAR','ATONESIR']
    out={'FUBCDORA.LETHINGKYMVPS/JQZXW':'established-board-fill'}
    for seed in seeds:out.setdefault(unique(seed+base),seed or 'alphabetical')
    for a,label in list(out.items()):out.setdefault(a[::-1],label+'/reverse-fill')
    assert all(len(a)==28 and set(a)==set(base) for a in out)
    return out

def parse(d,selectors):
    out=[];i=0
    while i<len(d):
        width=2 if d[i] in selectors else 1
        if i+width>len(d):return None
        out.append(d[i:i+width]);i+=width
    return out

def board_candidates():
    digits=[(name,s.translate(str.maketrans('abcdefghi','123456789'))) for name,s in STREAMS]
    orders=sorted({('0123456789'[i:]+'0123456789'[:i])[::direction] for i in range(10) for direction in (1,-1)})
    aa=alphabets();META['alphabets']=len(aa);META['column_orders']=len(orders)
    for first,second in itertools.permutations('0123456789',2):
        selectors=first+second;META['ordered_prefix_pairs']+=1
        parsed=[(name,parse(d,selectors)) for name,d in digits]
        for columns in orders:
            slots=[d for d in columns if d not in selectors]+[r+c for r in selectors for c in columns]
            index={s:i for i,s in enumerate(slots)}
            ids=[(name,[index[t] for t in p] if p is not None else None) for name,p in parsed]
            for alphabet,aname in aa.items():
                META['boards']+=1;label=f'prefixes={selectors}/columns={columns}/alphabet={aname}'
                outputs={}
                for name,indices in ids:
                    META['stream_decodings']+=1
                    if indices is None:continue
                    text=''.join(alphabet[i] for i in indices);outputs[name]=text;META['complete_parses']+=1
                    yield label+'/'+name+'/upper',text.encode()
                    yield label+'/'+name+'/lower',text.lower().encode()
                # Require the same board for both runs; test both concatenation orders.
                for direction in ('forward','reverse'):
                    a,b=outputs.get('r1/'+direction),outputs.get('r2/'+direction)
                    if a is None or b is None:continue
                    for order,text in [('r1-r2',a+b),('r2-r1',b+a)]:
                        yield label+'/'+direction+'/'+order+'/upper',text.encode()
                        yield label+'/'+direction+'/'+order+'/lower',text.lower().encode()

def controls():
    alpha=next(iter(alphabets()));cols='7654321098';selectors='25'
    slots=[d for d in cols if d not in selectors]+[r+c for r in selectors for c in cols]
    enc=dict(zip(alpha,slots));dec=dict(zip(slots,alpha))
    text='THISISATESTOFANOTHERBOARD'
    ciphertext=''.join(enc[c] for c in text)
    assert ''.join(dec[t] for t in parse(ciphertext,selectors))==text
    assert parse('2','25') is None

def main(mode):
    controls();folder=OUT/mode;folder.mkdir(parents=True,exist_ok=True)
    if (folder/'results.json').exists():raise SystemExit('results exist')
    gen=mapping_candidates if mode=='digit-map' else board_candidates
    counts=collections.Counter();seen=set();checked=set();hits=[];signals=[];lengths=collections.Counter();start=time.monotonic()
    def keycheck(label,d):
        if not 0<d<N or d in checked:return
        checked.add(d);counts['target_point_comparisons']+=1
        if PrivateKey.from_int(d).public_key.format()==TARGET:hits.append(dict(source=label,private_key_hex=f'{d:064x}'))
    with (folder/'padding.jsonl').open('w') as log:
        for label,b in gen():
            counts['generated_answers']+=1;h=sha(b)
            if h in seen:continue
            seen.add(h);counts['unique_answers']+=1;keycheck(label+'/sha256-answer',int.from_bytes(h,'big'))
            if len(b)<=32:
                for endian in ('big','little'):keycheck(label+'/raw/'+endian,int.from_bytes(b,endian))
            pw=h.hex().encode()
            for name,raw in RAW.items():
                counts['aes_trials']+=1;p=decrypt(raw,pw)
                if p is None:continue
                counts['padding_valid']+=1
                if name!='cosmic-duality':lengths[len(p)]+=1
                row=dict(source=label,answer_hex=b.hex(),container=name,plaintext_hex=p.hex())
                log.write(json.dumps(row)+'\n')
                tags=[kind for kind,_ in structures(p)]
                if p and sum(c in (9,10,13) or 32<=c<127 for c in p)/len(p)>=.85:tags.append('mostly-printable')
                if tags:signals.append(dict(**row,tags=tags))
                for how,d in payload_candidates(p):keycheck(label+'/'+name+'/'+how,d)
            if counts['unique_answers']%50000==0:print(json.dumps(dict(mode=mode,unique_answers=counts['unique_answers'],aes_trials=counts['aes_trials'],seconds=round(time.monotonic()-start,1))),flush=True)
    result=dict(mode=mode,**counts,generation=dict(META),short_plaintext_lengths=dict(lengths),target_matches=hits,structural_candidates=signals,seconds=round(time.monotonic()-start,2))
    (folder/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['digit-map','boards']);main(ap.parse_args().mode)
