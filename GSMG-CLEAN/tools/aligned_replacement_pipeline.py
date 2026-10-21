"""Lossless, anchor-constrained local transcript comparison; no AES or network.

Alignment is a declared model, not a reconstruction of the author's edit history.
Word tokenization retains numeric tokens and internal apostrophes (normalized away).
Raw spans and exact puzzle letter offsets are retained separately.
"""
import argparse
import csv
import difflib
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*|[0-9]+")
NUMBER_WORDS = {'23': ['TWENTY', 'THREE'], '16': ['SIXTEEN'],
                '7': ['SEVEN'], '99': ['NINETY', 'NINE']}
ANCHORS = [
    'YOUR LIFE IS THE SUM OF A REMAINDER OF AN UNBALANCED EQUATION',
    'THE PROGRAMMING OF', 'YOU ARE THE EVENTUALITY OF AN ANOMALY',
    'WHILE IT REMAINS A BURDEN', 'IT IS NOT UNEXPECTED',
    'WHICH HAS LED YOU INEXORABLY HERE', 'YOU HAVENT ANSWERED MY QUESTION',
    'QUITE RIGHT INTERESTING', 'THE OTHERS',
    'DENIAL IS THE MOST PREDICTABLE OF ALL HUMAN RESPONSES',
    'BUT REST ASSURED THIS WILL', 'HAVE DESTROYED',
    'HAVE BECOME EXCEEDINGLY EFFICIENT AT IT', 'THE FUNCTION OF THE',
    'IS NOW TO RETURN TO THE SOURCE',
    'ALLOWING A TEMPORARY DISSEMINATION OF THE CODE YOU',
    'CARRY REINSERTING THE PRIME', 'AFTER WHICH YOU WILL BE REQUIRED TO SELECT FROM',
    'FAILURE TO COMPLY WITH THIS PROCESS WILL RESULT IN A CATACLYSMIC SYSTEM CRASH KILLING',
    'WHICH COUPLED WITH THE EXTERMINATION OF',
    'WILL ULTIMATELY RESULT IN THE EXTINCTION OF THE',
]

def digest(data):
    return hashlib.sha256(data).hexdigest()

def tokenize(text, number_mode='literal'):
    out = []
    letter_offset = 0
    for m in TOKEN.finditer(text):
        raw = m.group()
        value = re.sub("['’]", '', raw).upper()
        values = NUMBER_WORDS.get(value, [value]) if number_mode == 'spelled' else [value]
        nletters = len(re.sub('[^A-Za-z]', '', raw))
        for v in values:
            out.append(dict(value=v, raw=raw, start=m.start(), end=m.end(),
                            letter_start=letter_offset, letter_end=letter_offset+nletters))
        letter_offset += nletters
    return out

def dialogue(path):
    records, excluded = [], []
    for line_no, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        m = re.match(r'^(?:\*\*)?(The Architect|Architect|Neo):(?:\*\*)?\s*(.*)$', line)
        if m:
            records.append(dict(speaker=m[1], text=m[2], line=line_no))
        elif line.strip():
            excluded.append(dict(line=line_no, text=line, reason='not a labeled dialogue line'))
    assert records, path
    return records, excluded

def source_excerpt(records):
    start = next(i for i, r in enumerate(records) if r['text'].startswith('Your life'))
    end = next(i for i in range(start, len(records)) if 'entire human race' in records[i]['text'])
    chosen = records[start:end+1]
    # Speaker labels and stage descriptions are metadata, not encrypted speech words.
    return ' '.join(r['text'] for r in chosen), chosen

def positions(seq, needle):
    return [i for i in range(len(seq)-len(needle)+1) if seq[i:i+len(needle)] == needle]

def local_ops(a, b, method):
    if method == 'sequence':
        return difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes()
    # Exact shortest insert/delete script via LCS; ties explicitly prefer deletion.
    n, m = len(a), len(b)
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n-1, -1, -1):
        for j in range(m-1, -1, -1):
            dp[i][j] = 1+dp[i+1][j+1] if a[i] == b[j] else max(dp[i+1][j], dp[i][j+1])
    matches, i, j = [], 0, 0
    while i < n and j < m:
        if a[i] == b[j]:
            matches.append((i,j)); i += 1; j += 1
        elif dp[i+1][j] >= dp[i][j+1]: i += 1
        else: j += 1
    ops, ai, bj = [], 0, 0
    for i,j in matches + [(n,m)]:
        if ai < i or bj < j:
            tag = 'replace' if ai < i and bj < j else 'delete' if ai < i else 'insert'
            ops.append((tag, ai, i, bj, j))
        if i < n:
            ops.append(('equal', i, i+1, j, j+1))
        ai, bj = i+1, j+1
    return ops

def align(a, b, method='sequence'):
    anchor_hits, lasta, lastb = [], 0, 0
    for phrase in ANCHORS:
        needle = phrase.split()
        aa, bb = positions(a, needle), positions(b, needle)
        assert len(aa) == len(bb) == 1, (phrase, aa, bb)
        i,j = aa[0],bb[0]
        assert i >= lasta and j >= lastb
        anchor_hits.append((i,j,len(needle),phrase))
        lasta,lastb = i+len(needle),j+len(needle)
    ops, ai,bj = [],0,0
    for i,j,size,phrase in anchor_hits + [(len(a),len(b),0,'END')]:
        # The large narrative replacement is one explicit block. Do not let common
        # words inside unrelated long paragraphs create arbitrary microscopic edits.
        if phrase == 'DENIAL IS THE MOST PREDICTABLE OF ALL HUMAN RESPONSES':
            if ai < i or bj < j: ops.append(('replace',ai,i,bj,j))
        else:
            ops.extend((t,x+ai,y+ai,u+bj,v+bj)
                       for t,x,y,u,v in local_ops(a[ai:i],b[bj:j],method))
        if size: ops.append(('equal',i,i+size,j,j+size))
        ai,bj = i+size,j+size
    # Coalesce adjacent equal blocks, never lose or arbitrarily pair unequal edits.
    merged = []
    for row in ops:
        if merged and row[0] == merged[-1][0] == 'equal' and merged[-1][2] == row[1] and merged[-1][4] == row[3]:
            old = merged.pop(); merged.append(('equal',old[1],row[2],old[3],row[4]))
        else: merged.append(row)
    verify_ops(a,b,merged)
    return merged, anchor_hits

def verify_ops(a,b,ops):
    ai,bj = 0,0
    for tag,x,y,u,v in ops:
        assert (x,u) == (ai,bj) and y >= x and v >= u
        if tag == 'equal': assert a[x:y] == b[u:v]
        ai,bj = y,v
    assert ai == len(a) and bj == len(b)
    assert [t for _,x,y,_,_ in ops for t in a[x:y]] == a
    assert [t for _,_,_,u,v in ops for t in b[u:v]] == b

def span(tokens, x, y, text):
    if x == y:
        p = tokens[x]['start'] if x < len(tokens) else len(text)
        l = tokens[x]['letter_start'] if x < len(tokens) else tokens[-1]['letter_end']
        return dict(word_range=[x,y], char_range=[p,p], letter_range=[l,l], raw='', words=[])
    return dict(word_range=[x,y], char_range=[tokens[x]['start'],tokens[y-1]['end']],
                letter_range=[tokens[x]['letter_start'],tokens[y-1]['letter_end']],
                raw=text[tokens[x]['start']:tokens[y-1]['end']],
                words=[t['value'] for t in tokens[x:y]])

def features(ws):
    alphabetic = ''.join(re.sub('[^A-Z]','',w) for w in ws)
    return [len(ws),len(alphabetic),sum(ord(c)-64 for c in alphabetic)]

def table(st,pt,sraw,praw,ops):
    out = []
    for tag,x,y,u,v in ops:
        if tag == 'equal': continue
        s,p = span(st,x,y,sraw),span(pt,u,v,praw)
        fs,fp = features(s['words']),features(p['words'])
        out.append(dict(row=len(out)+1, operation=tag, source=s, replacement=p,
                        source_features=fs, replacement_features=fp,
                        difference=[v-u for u,v in zip(fs,fp)],
                        feature_names=['word_count','letter_count','A1Z26_sum']))
    return out

def rectangles(n):
    return [(r,n//r) for r in range(2,n) if n % r == 0]

def matrices(rows):
    out = []
    # The table itself supplies these dimensions; gap features are the sum/count of
    # an empty span (zero), not padding to make a rectangle fit.
    for f,name in enumerate(['word_count','letter_count','A1Z26_sum']):
        a = [r['source_features'][f] for r in rows]
        b = [r['replacement_features'][f] for r in rows]
        for label,vals,h,w in [('paired_rows',sum(([x,y] for x,y in zip(a,b)),[]),len(rows),2),
                               ('paired_columns',a+b,2,len(rows))]:
            out.append(dict(name=f'{label}/{name}',values=vals,shape=[h,w],
                            basis='source/replacement table',exploratory=False))
    for side in ['source','replacement']:
        ws = [w for row in rows for w in row[side]['words']]
        # Literal numerical tokens retained in tables; letter-value views declare
        # ineligible literal-number streams instead of deleting their numbers.
        if not all(w.isalpha() for w in ws): continue
        streams = {'word_lengths':[len(w) for w in ws],
                   'letters_A1Z26':[ord(c)-64 for w in ws for c in w]}
        for name,vals in streams.items():
            for shape in rectangles(len(vals)):
                out.append(dict(name=f'{side}/{name}',values=vals,shape=list(shape),
                                basis='exact factorization only; not author-specified',exploratory=True))
    for f,name in enumerate(['word_count','letter_count','A1Z26_sum']):
        vals = [r['difference'][f] for r in rows]
        for shape in rectangles(len(vals)):
            out.append(dict(name=f'difference/{name}',values=vals,shape=list(shape),
                            basis='exact factorization of edit rows',exploratory=True))
    return out

def isprime(n):
    return n > 1 and all(n%d for d in range(2,int(n**.5)+1))

PRIMES = [p for p in range(2,100) if isprime(p)][:24]

def sum_pipeline(mat, colors):
    vals = mat['values']; h,w = mat['shape']
    assert h*w == len(vals) and len(colors) == 24
    if len(vals) < PRIMES[-1]: return []  # no partial colour schedule
    pairs = dict(zip(PRIMES,colors))
    result = []
    for weighted in [False,True]:
        y = [v*(i if weighted else 1) if pairs.get(i) == 'Y' else 0 for i,v in enumerate(vals,1)]
        b = [v*(i if weighted else 1) if pairs.get(i) == 'B' else 0 for i,v in enumerate(vals,1)]
        for label,grid in [('yellow',y),('blue',b),('yellow_minus_blue',[x-z for x,z in zip(y,b)])]:
            rr = [sum(grid[i*w:(i+1)*w]) for i in range(h)]
            cc = [sum(grid[i*w+j] for i in range(h)) for j in range(w)]
            assert sum(rr) == sum(cc) == sum(grid)
            for axis,nums in [('rows',rr),('columns',cc)]:
                result.append(dict(colour=label,prime_weight=weighted,axis=axis,sums=nums))
    return result

def row_colour_pipeline(rows, colors):
    """Alternative: one colour/prime pair per edit row; all 24 pairs or none."""
    if len(rows) != len(colors): return []
    out = []
    for f,feature in enumerate(['word_count','letter_count','A1Z26_sum']):
        for side in ['source_features','replacement_features','difference']:
            for weighted in [False,True]:
                for colour in ['Y','B']:
                    values=[r[side][f]*(p if weighted else 1) if c == colour else 0
                            for r,p,c in zip(rows,PRIMES,colors)]
                    out.append(dict(feature=feature,side=side,colour=colour,prime_weight=weighted,
                                    sums=values,total=sum(values),
                                    basis='one colour/prime per edit row; only when there are exactly 24 rows'))
    return out

def extract_words(ws, nums, mode):
    if not nums: return None
    if mode == 'start0':
        if not all(0 <= n < len(ws) for n in nums): return None
        idx = nums
    else:
        if not all(1 <= n <= len(ws) for n in nums): return None
        idx = [n-1 if mode == 'start1' else len(ws)-n for n in nums]
    chosen = [ws[i] for i in idx]
    return dict(indices=idx,words=chosen,joined=''.join(chosen),spaced=' '.join(chosen),
                initials=''.join(w[0] for w in chosen),finals=''.join(w[-1] for w in chosen))

def target_passages(records,pt):
    start = next(i for i,r in enumerate(records) if r['text'].startswith('Your life'))
    choice = next(i for i,r in enumerate(records) if r['speaker']=='Neo' and r['text'].startswith('Choice'))
    arch = [r['text'] for r in records[start:choice] if 'Architect' in r['speaker']]
    door = next(r['text'] for r in records if r['text'].startswith('Which brings us'))
    # Both saved versions contain this end phrase, but only one explicitly puts Hope
    # after the physical choice. Use the common cut; do not move Hope silently.
    door = door[:door.lower().index('stop it.')+len('stop it.')]
    select_idx = next(i for i,t in enumerate(pt) if t['value']=='SELECT')
    return {'before_neo_choice':[t['value'] for t in tokenize(' '.join(arch),'spelled')],
            'last_architect_before_neo_choice':[t['value'] for t in tokenize(arch[-1],'spelled')],
            'before_physical_door_choice':[t['value'] for t in tokenize(door,'spelled')],
            'puzzle_before_select':[t['value'] for t in pt[:select_idx]]}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,required=True)
    args = ap.parse_args(); out = args.out.resolve(); out.mkdir(parents=True,exist_ok=False)
    files = {name:ROOT/'reference_texts'/file for name,file in [
        ('scott','matrix_reloaded_architect_scene_scott_manning.md'),
        ('kedri','matrix_reloaded_architect_scene_transcript.txt')]}
    pf = ROOT/'data/architect_plaintext_readable.txt'
    exactf = ROOT/'data/architect_letters_1539.txt'
    praw = pf.read_text(encoding='utf-8'); pt=tokenize(praw)
    assert ''.join(re.findall('[A-Z]',praw.upper())) == exactf.read_text().strip()
    colors=(ROOT/'data/poster_spiral_bits.txt').read_text().splitlines()[1]
    manifest=dict(inputs={str(p):digest(p.read_bytes()) for p in [*files.values(),pf,exactf,ROOT/'data/poster_spiral_bits.txt']},
                  anchors=ANCHORS,number_modes=['literal','spelled'],methods=['sequence','lcs'],
                  schedule='first 24 prime indices, 1-based, all colours used exactly once; no rotation/repetition',
                  alternate_schedule='one colour/prime per edit row, eligible only for exactly 24 rows',
                  matrices='paired edit table; exact rectangular factors of word/letter/difference streams',
                  serializations=['comma-separated signed sums','nonnegative decimal integer bytes',
                                  '1/2/4-byte integers when representable, signed/unsigned, both endiannesses'],
                  acceptance='full source reconstruction or exact target key; no English-score rejection',
                  caveats=['anchors and narrative block boundary are analyst models','readable puzzle word boundaries are editorial',
                           'matrix factorization alone is not evidence','zero sums retained; no abs, modulo or dropped indices'],
                  aes_decryptions=0,network=False)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    summaries,all_tables,all_matrices,all_sums,outputs = [],{},[],[],[]
    for name,path in files.items():
        records,excluded=dialogue(path); sraw,chosen=source_excerpt(records)
        (out/f'{name}_source.json').write_text(json.dumps(dict(dialogue=records,excluded=excluded,excerpt=sraw,selected=chosen),indent=2),encoding='utf-8')
        targets=target_passages(records,pt)
        for number_mode in ['literal','spelled']:
            st=tokenize(sraw,number_mode); a=[t['value'] for t in st]; b=[t['value'] for t in pt]
            for method in ['sequence','lcs']:
                key=f'{name}/{number_mode}/{method}'
                ops,anchors=align(a,b,method); rows=table(st,pt,sraw,praw,ops)
                all_tables[key]=dict(source_tokens=st,puzzle_tokens=pt,ops=ops,rows=rows,anchors=anchors)
                sm=dict(alignment=key,source_tokens=len(st),puzzle_tokens=len(pt),edit_rows=len(rows),
                        removed_words=sum(len(r['source']['words']) for r in rows),
                        replacement_words=sum(len(r['replacement']['words']) for r in rows),
                        removed_letters=sum(r['source_features'][1] for r in rows),
                        replacement_letters=sum(r['replacement_features'][1] for r in rows),roundtrip=True)
                summaries.append(sm)
                for row_sum in row_colour_pipeline(rows,colors):
                    sid=len(all_sums)
                    row_sum.update(id=sid,matrix=None,alignment=key,schedule='edit_rows')
                    all_sums.append(row_sum)
                    outputs.append(dict(kind='sum_decimal',sum_id=sid,output=','.join(map(str,row_sum['sums']))))
                    # Report both side totals, too: no selection removes the zero rows.
                    outputs.append(dict(kind='sum_total',sum_id=sid,output=str(row_sum['total'])))
                    for tname,ws in targets.items():
                        for mode in ['start0','start1','end1']:
                            ex=extract_words(ws,row_sum['sums'],mode)
                            if ex is None: continue
                            for reading in ['joined','spaced','initials','finals']:
                                outputs.append(dict(kind='word_selection',sum_id=sid,target=f'{name}/{tname}',
                                                    mode=mode,reading=reading,selected=ex['words'],
                                                    indices=ex['indices'],output=ex[reading]))
                for mat in matrices(rows):
                    mid=len(all_matrices); mat.update(id=mid,alignment=key); all_matrices.append(mat)
                    for summed in sum_pipeline(mat,colors):
                        sid=len(all_sums); summed.update(id=sid,matrix=mid,schedule='prime_positions'); all_sums.append(summed)
                        outputs.append(dict(kind='sum_decimal',sum_id=sid,output=','.join(map(str,summed['sums']))))
                        for tname,ws in targets.items():
                            for mode in ['start0','start1','end1']:
                                ex=extract_words(ws,summed['sums'],mode)
                                if ex is None: continue
                                for reading in ['joined','spaced','initials','finals']:
                                    outputs.append(dict(kind='word_selection',sum_id=sid,target=f'{name}/{tname}',
                                                        mode=mode,reading=reading,selected=ex['words'],
                                                        indices=ex['indices'],output=ex[reading]))
    for fname,obj in [('tables.json',all_tables),('matrix_inventory.json',all_matrices),('sum_lists.json',all_sums)]:
        (out/fname).write_text(json.dumps(obj,indent=1),encoding='utf-8')
    # Additional serializations are explicit hypotheses, not text-score gates.
    # Retain signed values losslessly instead of folding them through abs().
    for row in all_sums:
        nums=row['sums']
        if all(n >= 0 for n in nums):
            digits=''.join(map(str,nums))
            n=int(digits)
            raw=n.to_bytes(max(1,(n.bit_length()+7)//8),'big')
            outputs.append(dict(kind='decimal_integer_bytes',sum_id=row['id'],raw_hex=raw.hex()))
        for width in [1,2,4]:
            for signed in [False,True]:
                lo,hi=(-(1<<(8*width-1)),1<<(8*width-1)) if signed else (0,1<<(8*width))
                if not all(lo <= n < hi for n in nums): continue
                for endian in ['big','little']:
                    raw=b''.join(n.to_bytes(width,endian,signed=signed) for n in nums)
                    outputs.append(dict(kind='integer_array_bytes',sum_id=row['id'],width=width,
                                        signed=signed,endian=endian,raw_hex=raw.hex()))
    (out/'stability.json').write_text(json.dumps({
        'source_spelled_puzzle_edit_intervals': {
            k:[r['replacement']['letter_range'] for r in t['rows']]
            for k,t in all_tables.items() if '/spelled/' in k},
        'identical_spelled_method_tables': {
            name:all_tables[f'{name}/spelled/sequence']['rows']==all_tables[f'{name}/spelled/lcs']['rows']
            for name in files},
        'source_sensitive':summaries[2]['edit_rows'] != summaries[6]['edit_rows']
    },indent=2),encoding='utf-8')
    with (out/'all_outputs.jsonl').open('w',encoding='utf-8') as f:
        for row in outputs: f.write(json.dumps(row)+'\n')
    with (out/'replacement_table.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.writer(f);writer.writerow(['alignment','row','operation','source_word_range','puzzle_word_range',
                                            'puzzle_letter_range','source_exact_span','puzzle_exact_span','source_features',
                                            'replacement_features','signed_difference'])
        for key,t in all_tables.items():
            for r in t['rows']:
                writer.writerow([key,r['row'],r['operation'],r['source']['word_range'],r['replacement']['word_range'],
                                 r['replacement']['letter_range'],r['source']['raw'],r['replacement']['raw'],
                                 r['source_features'],r['replacement_features'],r['difference']])
    md=['# Exact replacement table (Scott, spelled numbers, sequence alignment)',
        '', 'This is exact under the declared anchors/tokenization, not a uniquely proven author edit history.',
        'Full source spans, token offsets, alternatives and complete accounting are in tables.json and replacement_table.csv.',
        '', '| Row | Puzzle letter interval [start,end) | Source span | Replacement span | Words S/P | Letters S/P |',
        '|---:|---|---|---|---|---|']
    for r in all_tables['scott/spelled/sequence']['rows']:
        s,p=r['source'],r['replacement']
        clean=lambda x:x.replace('|','\\|').replace('\n',' ')
        md.append(f"| {r['row']} | {p['letter_range']} | {clean(s['raw']) or '∅'} | {clean(p['raw']) or '∅'} | {r['source_features'][0]}/{r['replacement_features'][0]} | {r['source_features'][1]}/{r['replacement_features'][1]} |")
    (out/'REPLACEMENT_TABLE.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    summary=dict(alignments=summaries,matrices=len(all_matrices),
                 table_dimensions=sorted(set(tuple(m['shape']) for m in all_matrices if not m['exploratory'])),
                 prime_schedule_eligible=sum(len(m['values'])>=89 for m in all_matrices),sum_lists=len(all_sums),
                 output_records=len(outputs),unique_outputs=len(set(o.get('output',o.get('raw_hex')) for o in outputs)),
                 valid_extractions=sum(o['kind']=='word_selection' for o in outputs),
                 natural_matrix_established=False,
                 conclusion='Exact-factor and paired-table candidates tested; none is established as intended by dimensions alone.')
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__ == '__main__': main()