"""Bounded field-role experiment. Saves source-derived candidates before testing.

Usage: python tools/test_salphaseion_roles.py
No claims that role assignments or exact composite constructions are proven.
"""
import base64
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
import check_candidate as cc
import inspect_decrypts as inspect

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'runs/2026-09-13_salphaseion_roles'
sha = lambda b: hashlib.sha256(b).hexdigest()

def sums(values, width):
    assert len(values) % width == 0
    return [sum(values[i:i+width]) for i in range(0,len(values),width)], [sum(values[i::width]) for i in range(width)]

def digit_letters(text):
    return text.translate(str.maketrans('1234567890', 'abcdefghio'))

def build():
    OUT.mkdir(exist_ok=False)
    dbbi = (ROOT/'data/DBBI_91.txt').read_text().strip()
    faed = (ROOT/'data/FAED_570.txt').read_text().strip()
    lead = json.loads((ROOT/'data/leads_reproduced.json').read_text())
    # Structural role check: exact reconstruction, all nontrivial rectangular shapes.
    structural = []
    for name, source, target in [('FAED_to_DBBI',faed,dbbi),('DBBI_to_FAED',dbbi,faed)]:
        values = [ord(c)-96 for c in source]
        for width in range(2,len(values)):
            if len(values)%width:
                continue
            for axis, seq in zip(('rows','cols'), sums(values,width)):
                text = digit_letters(''.join(map(str,seq)))
                structural.append(dict(model=name, width=width, axis=axis, sums=seq,
                                       encoded=text, target_length=len(target), exact_match=text==target))
    assert sums([1,2,3,4,5,6],3)==([6,15],[5,7,9])
    assert digit_letters(''.join(map(str,sums([1,2,3,4,5,6],3)[0])))=='fae'
    (OUT/'structural_results.json').write_text(json.dumps(structural,indent=2))

    # A: source-order matrix/sum component. Unmodified fields are explicit alternate role models.
    a = dict(DBBI_literal=dbbi, FAED_literal=faed,
             DBBI_decimal=''.join(str(ord(c)-96) for c in dbbi),
             FAED_decimal=''.join(str(ord(c)-96) for c in faed))
    lists = {'L1_yellow_blue_totals':[479,484]}
    pairs=lead['L1_color_primes']['pairs'].split()
    lists['L1_yellow_primes']=[int(p[:-1]) for p in pairs if p.endswith('Y')]
    lists['L1_blue_primes']=[int(p[:-1]) for p in pairs if p.endswith('B')]
    lists['L1_yellow_then_blue']=lists['L1_yellow_primes']+lists['L1_blue_primes']
    for name, text, width in [('DBBI_7x13',dbbi,13),('FAED_19x30',faed,30),('FAED_30x19',faed,19)]:
        for axis, seq in zip(('rows','cols'),sums([ord(c)-96 for c in text],width)):
            lists[name+'_'+axis]=seq
    for axis, seq in zip(('rows','cols'),sums(lead['L2_prime_matrix']['values_84'],12)):
        lists['L2_7x12_'+axis]=seq
    # Actual poster geometry: spiral bits mapped back into their source coordinates.
    bits=(ROOT/'data/poster_spiral_bits.txt').read_text().splitlines()[0]
    board=[[0]*14 for _ in range(14)]
    directions=[(1,0),(0,1),(-1,0),(0,-1)]
    visited=set(); r=c=d=0
    for bit in bits:
        board[r][c]=int(bit); visited.add((r,c))
        nr,nc=r+directions[d][0],c+directions[d][1]
        if not(0<=nr<14 and 0<=nc<14) or (nr,nc) in visited:
            d=(d+1)%4; nr,nc=r+directions[d][0],c+directions[d][1]
        r,c=nr,nc
    lists['poster_rows']=[sum(row) for row in board]
    lists['poster_cols']=[sum(row[c] for row in board) for c in range(14)]
    assert sum(lists['poster_rows'])==101
    for name, seq in lists.items():
        for sepname, sep in [('joined',''),('commas',','),('spaces',' ')]:
            a[name+'/'+sepname]=sep.join(map(str,seq))
        if min(seq)>=0:
            a[name+'/page_digits']=digit_letters(''.join(map(str,seq)))

    # B: pinned endings at the choice/cut, not every arbitrary suffix of the scene.
    transcript=(ROOT/'reference_texts/matrix_reloaded_architect_scene_scott_manning.md').read_text(encoding='utf-8')
    speech=transcript.splitlines()[104]
    puzzle=(ROOT/'data/architect_plaintext_readable.txt').read_text(encoding='utf-8')
    assert 'An emotion that' in speech and '_Neo walks to the door on his left_' in transcript
    p4='REINSERTING THE PRIME BASICS'
    p5='GOOD LUCK NEVERTHELESS I REALLY HOPE YOURE THE ONE CIAO BELLA O'
    assert p4 in puzzle and p5 in ' '.join(puzzle.split())
    b={
        'P1_final_sentence':speech[speech.index('An emotion that'):],
        'P1_final_clause':speech[speech.index('she is going to die'):],
        'P1_neo':'No!',
        'P2_before_choice_sentence':'The door to the left leads back to the matrix, to her, and to the end of your species.',
        'P2_problem_is_choice':'the problem is choice',
        'P4_prime_basics':p4,
        'P5_final_sentence':p5,
        'P5_farewell':'CIAO BELLA O',
    }
    assert b['P2_before_choice_sentence'] in speech
    # Restrict normalization to exact source text, lowercase, and lowercase alphanumerics.
    bf={name+'/'+form:value for name,text in b.items() for form,value in
        [('exact',text),('lower',text.lower()),('connected',re.sub('[^a-z0-9]','',text.lower()))]}
    candidates={}
    def add(value, provenance):
        candidates.setdefault(value,[]).append(provenance)
    for an,av in a.items():
        add(av,dict(family='A_literal_control',A=an))
    for bn,bv in bf.items():
        add(bv,dict(family='B_literal_control',B=bn))
    for an,av in a.items():
        for bn,bv in bf.items():
            # Common outer SHA is handled by cc's gsmg profile; hashes here are deliberate inner hashes.
            for mode,x,y in [('A+B',av,bv),('hashA+B',sha(av.encode()),bv),
                             ('A+hashB',av,sha(bv.encode())),('hashA+hashB',sha(av.encode()),sha(bv.encode()))]:
                for sep in ('',' '):
                    add(x+sep+y,dict(family='composite',A=an,B=bn,construction=mode,separator=sep))
    records=[dict(candidate=value,provenance=prov) for value,prov in candidates.items()]
    (OUT/'candidates.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in records),encoding='utf-8')
    sourcefiles=['data/DBBI_91.txt','data/FAED_570.txt','data/leads_reproduced.json','data/poster_spiral_bits.txt',
                 'data/architect_plaintext_readable.txt','reference_texts/matrix_reloaded_architect_scene_scott_manning.md']
    manifest=dict(hypothesis='Source-order A then B: matrix/sum component plus last-words component. '
                            'Inner component hashing is an explicit anstoo hypothesis; no arbitrary permutations.',
                  primary_profile='gsmg', secondary_profiles=['raw','gsmg-md5','raw-md5'],
                  source_hashes={p:sha((ROOT/p).read_bytes()) for p in sourcefiles},
                  candidate_hash=sha((OUT/'candidates.jsonl').read_bytes()),
                  script_hash=sha(Path(__file__).read_bytes()),n_candidates=len(records),
                  A_components=a,B_components=bf,structural_cases=len(structural),
                  limitations='No new prime masks; matrix shapes for composite test are hypotheses. '
                              'No solved relation or claim all candidates are historically new. '
                              'Single-field sums are controls. No shuffle significance inferred from padding.')
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    return records,structural

def main():
    records,structural=build()
    print(f'Pre-registered {len(records)} candidates and {len(structural)} structural checks',flush=True)
    inspect.enable_fast_keys()
    cc.selftest()
    counts=Counter(); profiles={p:Counter() for p in cc.PROFILES}; findings=[]; l5=[]
    with (OUT/'all_padding_valid.jsonl').open('w',encoding='utf-8') as journal, (OUT/'inspections.jsonl').open('w',encoding='utf-8') as scans:
        for index,row in enumerate(records):
            value=row['candidate']
            if cc.eq_pattern(sha(value.encode()))==cc.DBBI_PATTERN:
                l5.append(row)
            for profile in cc.PROFILES:
                for name,env in cc.ENVELOPES.items():
                    counts['trials']+=1; profiles[profile]['trials']+=1
                    pad,pt=cc.try_envelope(env,value,profile)
                    if not pad:
                        continue
                    result=dict(**row,profile=profile,envelope=name,pad=pad,plaintext_hex=pt.hex(),
                                status='UNRESOLVED_RETAINED')
                    journal.write(json.dumps(result)+'\n'); journal.flush()
                    review=inspect.inspect(pt)
                    scans.write(json.dumps(dict(source=result,inspection=review))+'\n'); scans.flush()
                    counts['retained']+=1; profiles[profile]['pad'+str(pad)]+=1
                    if any(n['signals'] or n['key_matches'] for n in review['nodes']) or pad>=3:
                        findings.append(dict(source=result,inspection=review))
            if (index+1)%2000==0:
                print(f"{index+1}/{len(records)} candidates; {counts['retained']} outputs retained",flush=True)
    summary=dict(counts=dict(counts),profiles={k:dict(v) for k,v in profiles.items()},
                 structural_matches=[r for r in structural if r['exact_match']],l5_matches=l5,
                 format_or_key_or_pad3plus_findings=findings,
                 conclusion='Every padding-valid result retained; no negative inferred solely from lack of format signals.')
    (OUT/'results.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k!='format_or_key_or_pad3plus_findings'}|
                     {'n_findings':len(findings)},indent=2))

if __name__=='__main__':
    main()
