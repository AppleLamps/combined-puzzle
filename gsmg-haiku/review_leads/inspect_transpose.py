"""Record every fixed-board transposition and inspect saved binary outputs.
This does not repeat AES decryptions. Run after next_tests.py transpose.
"""
import json,re
from collections import Counter
from next_tests import S,OUT,columnar,board,transposition
from hash_scope import sha,N,TARGET,PrivateKey,payload_candidates
from binary_envelopes import structures

def main():
    dest=OUT/'transpose-inspection.json'
    if dest.exists():raise SystemExit('inspection exists')
    rows=[];checks=set();hits=[];binary=[];counts=Counter()
    def check(label,d):
        if not 0<d<N or d in checks:return
        checks.add(d)
        if PrivateKey.from_int(d).public_key.format()==TARGET:hits.append(dict(source=label,private_key_hex=f'{d:064x}'))
    for name,text in [('r1',S[:91]),('r2',S[195:765])]:
        for reverse in (False,True):
            for key in ('matrixsumlist','thematrixhasyou','lastwordsbeforearchichoice','fubcdoraclethingkymvps'):
                for inverse in (False,True):
                    moved=columnar(text[::-1] if reverse else text,key,inverse)
                    digits=moved.translate(str.maketrans('abcdefghi','123456789'))
                    decoded=board(digits)
                    rows.append(dict(run=name,reverse=reverse,key=key,inverse=inverse,digits=digits,decoded=decoded))
                    counts['complete_board_parses' if decoded is not None else 'incomplete_board_parses']+=1
    answers={}
    for label,b in transposition():
        b=b.encode() if isinstance(b,str) else b
        answers.setdefault(b,label)
    for b,label in answers.items():
        check(label+'/sha256-answer',int.from_bytes(sha(b),'big'))
        if len(b)<=32:
            for endian in ('big','little'):check(label+'/raw/'+endian,int.from_bytes(b,endian))
        if re.fullmatch(rb'[0-9a-fA-F]{64}',b):check(label+'/hex',int(b,16))
    with (OUT/'next-transpose-padding.jsonl').open() as stream:
        for line in stream:
            row=json.loads(line);p=bytes.fromhex(row['plaintext_hex'])
            for kind,payload in structures(p):binary.append(dict(source=row['source'],container=row['container'],kind=kind,payload_hex=payload.hex()))
            for how,d in payload_candidates(p):check(row['source']+'/'+row['container']+'/'+how,d)
    result=dict(cases=len(rows),**counts,distinct_answers=len(answers),target_point_comparisons=len(checks),target_matches=hits,binary_candidates=binary,cases_detail=rows)
    dest.write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='cases_detail'}))
    for row in rows:print(row['run'],row['reverse'],row['key'],row['inverse'],row['decoded'])

if __name__=='__main__':main()
