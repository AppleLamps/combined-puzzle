"""Reproduce stage connections and locate gaps; no new password search."""
import base64
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
import check_candidate as cc

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-13_whole_puzzle'
sha=lambda b:hashlib.sha256(b).hexdigest()
def areas(p):
    return [re.sub(r'\s+','',s) for s in re.findall(r'<textarea[^>]*>(.*?)</textarea>',p.read_text(encoding='utf-8'),re.S)]

def main():
    OUT.mkdir(exist_ok=True)
    page=areas(ROOT/'originals/pages/phase2_choice.html')
    seven=json.loads((ROOT/'data/seven_part_phase3_answer.json').read_text())
    three=['jacquefresco','giveitjustonesecond','heisenbergsuncertaintyprinciple']
    p3=(ROOT/'data/phase3_plaintext.bin').read_bytes()
    stages=[('phase2',base64.b64decode(page[0]),['causality']),
            ('phase3',base64.b64decode(page[1]),seven),
            ('phase3_2',base64.b64decode(p3[p3.index(b'U2FsdGVk'):]),three)]
    opened=[]; negative_controls=[]
    for name,env,parts in stages:
        pad,pt=cc.try_envelope(env,''.join(parts),'gsmg')
        assert pad and pt==(ROOT/f'data/{name}_plaintext.bin').read_bytes()
        opened.append(dict(stage=name,parts=len(parts),plaintext_bytes=len(pt),sha256=sha(pt)))
        if len(parts)>1:
            for i,part in enumerate(parts):
                testpad,testpt=cc.try_envelope(env,part,'gsmg')
                assert testpt!=pt
                negative_controls.append(dict(stage=name,part=i+1,padding=testpad,
                                              reproduces_expected_plaintext=False))
    p32=(ROOT/'data/phase3_2_plaintext.bin').read_bytes()
    ct=p32[447:1986].decode('latin1').encode('cp273').decode('ascii')
    key='THEMATRIXHASYOU'
    arch=''.join(chr(65+(ord(key[i%len(key)])-ord(c.upper()))%26) for i,c in enumerate(ct))
    assert arch==(ROOT/'data/architect_letters_1539.txt').read_text().strip()
    digits=re.match(rb'[0-9]+',p32[1990:]).group().decode()
    codes=[str(i) for i in range(10) if i not in (1,4)]+['1'+str(i) for i in range(10)]+['4'+str(i) for i in range(10)]
    table=dict(zip(codes,'FUBCDORA.LETHINGKYMVPS/JQZXW'))
    used=[]; i=0
    while i<len(digits):
        size=2 if digits[i] in '14' else 1
        used.append(digits[i:i+size]); i+=size
    vic=''.join(table[c] for c in used)
    assert vic==(ROOT/'data/checkerboard_vic_91.txt').read_text().splitlines()[0]
    assert ''.join(used)==digits
    sal,cosmic=areas(ROOT/'originals/pages/salphaseion_phase3.html')
    assert sal==(ROOT/'data/salphaseion_compact_1075.txt').read_text().strip()
    binary=lambda s:bytes(int(s[i:i+8].translate(str.maketrans('ab','01')),2) for i in range(0,len(s),8)).decode()
    def decimal(s):
        n=int(s.translate(str.maketrans('abcdefghio','1234567890')))
        return n.to_bytes((n.bit_length()+7)//8,'big').decode()
    labels=dict(matrixsumlist=binary(sal[91:195]),lastwords=decimal(sal[766:829]),
                thispassword=decimal(sal[830:859]),enter=binary(sal[959:999]))
    assert labels==dict(matrixsumlist='matrixsumlist',lastwords='lastwordsbeforearchichoice',thispassword='thispassword',enter='enter')
    locked=dict(terminal_phase3_2_end=base64.b64decode(p32[p32.index(b'U2FsdGVk'):]),
                salphaseion_short=base64.b64decode(sal[895:959]+sal[999:1063]),
                cosmic_duality=base64.b64decode(cosmic))
    for name,b in locked.items(): assert b==cc.ENVELOPES[name]
    caption='GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
    assert sha(caption.encode()) in (ROOT/'originals/cdx_wayback_gsmg.json').read_text()
    assert sha(b'theflowerblossomsthroughwhatseemstobeaconcretesurface')=='5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75'
    entity=json.loads((ROOT/'evidence/decentraland/entity.json').read_text())
    result=dict(opened_stages=opened,correct_components_failing_alone=negative_controls,
                architect=dict(length=len(arch),sha256=sha(arch.encode())),
                checkerboard=dict(digit_count=len(digits),plaintext=vic,used_codes=sorted(set(used)),
                                  unused_codes=[c for c in codes if c not in used]),
                side_route=dict(caption_hash=sha(caption.encode()),scene_parcels=entity['pointers'],
                                navigation_candidate_coordinates=[[2,0],[32,82],[-42,-16],[4,15]],
                                candidate_route_is_not_exact=True),
                labels=labels,first_z=sal.index('z'),
                uninterrupted_initial_ai_length=len(re.match('[a-i]+',sal).group()),
                fields={name:dict(length=len(s),counts=dict(Counter(s))) for name,s in [('DBBI',sal[:91]),('FAED',sal[195:765])]},
                locked={n:dict(bytes=len(b),sha256=sha(b)) for n,b in locked.items()},
                verdict='Solved transitions reproduced; ten correct components fail as standalone passwords; no locked transition established')
    (OUT/'verified_connections.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
