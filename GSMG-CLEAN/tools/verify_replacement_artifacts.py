"""Independent arithmetic/accounting checks of the saved replacement-pipeline run."""
import argparse
import json
import re
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('run',type=Path);args=ap.parse_args()
    out=args.run
    root=Path(__file__).resolve().parents[1]
    tables=json.loads((out/'tables.json').read_text())
    mats=json.loads((out/'matrix_inventory.json').read_text())
    sums=json.loads((out/'sum_lists.json').read_text())
    colors=(root/'data/poster_spiral_bits.txt').read_text().splitlines()[1]
    primes=[n for n in range(2,100) if all(n%d for d in range(2,n))][:24]
    for table in tables.values():
        a=[t['value'] for t in table['source_tokens']];b=[t['value'] for t in table['puzzle_tokens']]
        apos=bpos=0
        for tag,i,j,k,l in table['ops']:
            assert (i,k)==(apos,bpos)
            if tag=='equal': assert a[i:j]==b[k:l]
            apos,bpos=j,l
        assert apos==len(a) and bpos==len(b)
        for r in table['rows']:
            assert r['difference']==[p-s for s,p in zip(r['source_features'],r['replacement_features'])]
    for s in sums:
        if s['schedule']=='edit_rows':
            rs=tables[s['alignment']]['rows'];assert len(rs)==24
            f=['word_count','letter_count','A1Z26_sum'].index(s['feature'])
            expected=[r[s['side']][f]*(p if s['prime_weight'] else 1) if c==s['colour'] else 0
                      for r,p,c in zip(rs,primes,colors)]
            assert expected==s['sums'] and sum(expected)==s['total']
            continue
        m=mats[s['matrix']];h,w=m['shape'];assert len(m['values'])==h*w
        grid=[0]*(h*w)
        for p,c in zip(primes,colors):
            v=m['values'][p-1]*(p if s['prime_weight'] else 1)
            if s['colour']=='yellow_minus_blue': grid[p-1]=v if c=='Y' else -v
            elif s['colour']==('yellow' if c=='Y' else 'blue'): grid[p-1]=v
        expected=([sum(grid[i:i+w]) for i in range(0,len(grid),w)] if s['axis']=='rows'
                  else [sum(grid[j::w]) for j in range(w)])
        assert expected==s['sums']
    targets={n:(root/'data'/n).read_text().strip().encode() for n in
             ['DBBI_91.txt','FAED_570.txt','architect_letters_1539.txt']}
    targets.update({n:n.encode() for n in ['matrixsumlist','lastwordsbeforearchichoice','thispassword',
                                          'followthewhiterabbit']})
    target_hits=[];counts={};eligible={}
    for line,row in enumerate((json.loads(l) for l in (out/'all_outputs.jsonl').read_text().splitlines()),1):
        kind=row['kind'];counts[kind]=counts.get(kind,0)+1
        b=bytes.fromhex(row['raw_hex']) if 'raw_hex' in row else row['output'].encode()
        if kind=='integer_array_bytes':
            width=row['width']; nums=[int.from_bytes(b[i:i+width],row['endian'],signed=row['signed'])
                                     for i in range(0,len(b),width)]
            assert nums==sums[row['sum_id']]['sums']
        if kind=='decimal_integer_bytes':
            assert int.from_bytes(b,'big')==int(''.join(map(str,sums[row['sum_id']]['sums'])))
        for name,t in targets.items():
            if len(b)==len(t): eligible[name]=eligible.get(name,0)+1
            if b==t: target_hits.append(dict(line=line,target=name))
    a=tables['scott/spelled/sequence']['rows'];b=tables['kedri/spelled/sequence']['rows']
    ai={tuple(r['replacement']['letter_range']) for r in a};bi={tuple(r['replacement']['letter_range']) for r in b}
    result=dict(accounting_tables_pass=len(tables),matrix_sum_checks_pass=len(sums),
                serialization_checks_pass=True,output_counts=counts,source_target_matches=target_hits,
                length_eligible_source_comparisons=eligible,shared_edit_intervals=len(ai&bi),
                kedri_extra_edits=[r for r in b if tuple(r['replacement']['letter_range']) not in ai],
                limitation='Exact complete reconstructions only; not a statistical English or intended-matrix test.')
    (out/'independent_verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()