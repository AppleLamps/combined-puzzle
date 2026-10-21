"""Lossless full-wrapper reconstruction and explicit boundary/grammar tests."""
import base64
import hashlib
import json
import re
from pathlib import Path
from collections import deque

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-13_salphaseion_construction'
TO_DIGIT=str.maketrans('abcdefghio','1234567890')
FROM_DIGIT=str.maketrans('1234567890','abcdefghio')
prime=lambda n:n>1 and all(n%d for d in range(2,int(n**.5)+1))

def prime_states(s,start_slot=1):
    # Every reachable (source offset, logical slot); dynamic prime range, not a
    # fixed list of primes below 100, because the tested streams are long.
    seen={(0,start_slot)}; queue=deque(seen); stalled=[]
    while queue:
        i,slot=queue.popleft()
        if i==len(s): continue
        options=[t for t in ('b','be') if s.startswith(t,i)] if prime(slot) else [s[i]]
        if not options:
            stalled.append(dict(offset=i,logical_slot=slot,actual=s[i],expected='b or be'))
        for t in options:
            state=(i+len(t),slot+1)
            if state not in seen: seen.add(state); queue.append(state)
    return dict(complete_slots=sorted(slot-start_slot for i,slot in seen if i==len(s)),
                maximum_consumed=max(i for i,slot in seen),input_length=len(s),
                states=len(seen),furthest_stalls=sorted(stalled,key=lambda r:r['offset'],reverse=True)[:5])

def main():
    OUT.mkdir(exist_ok=True)
    p=ROOT/'originals/pages/salphaseion_phase3.html'
    html=p.read_text(encoding='utf-8')
    bodies=re.findall(r'<textarea[^>]*>(.*?)</textarea>',html,re.S)
    raw=bodies[0]; s=re.sub(r'\s+','',raw)
    assert s==(ROOT/'data/salphaseion_compact_1075.txt').read_text().strip()
    assert raw==' '.join(s)
    definition=[(0,91,'unknown','DBBI'),(91,195,'binary','matrixsumlist'),
                (195,765,'unknown','FAED'),(765,766,'separator','z1'),
                (766,829,'decimal','lastwordsbeforearchichoice'),(829,830,'separator','z2'),
                (830,859,'decimal','thispassword'),(859,860,'separator','z3'),
                (860,895,'literal','before_cipher'),(895,959,'base64_piece','cipher_line1'),
                (959,999,'binary','enter'),(999,1063,'base64_piece','cipher_line2'),
                (1063,1075,'literal','after_cipher')]
    segments=[]; rebuilt=[]
    for a,b,kind,label in definition:
        t=s[a:b]; encoded=t; decoded=None
        if kind=='binary':
            bit=t.translate(str.maketrans('ab','01'))
            assert len(bit)%8==0
            decoded=bytes(int(bit[i:i+8],2) for i in range(0,len(bit),8)).decode('ascii')
            encoded=''.join(f'{x:08b}' for x in decoded.encode()).translate(str.maketrans('01','ab'))
            assert decoded==label
        elif kind=='decimal':
            n=int(t.translate(TO_DIGIT)); byte=n.to_bytes((n.bit_length()+7)//8,'big')
            decoded=byte.decode('ascii'); assert decoded==label
            encoded=str(int.from_bytes(byte,'big')).translate(FROM_DIGIT)
        assert encoded==t
        rebuilt.append(encoded)
        segments.append(dict(start=a,end_exclusive=b,length=b-a,kind=kind,label=label,
                             raw=t,decoded=decoded,roundtrip=True))
    assert ''.join(rebuilt)==s and ' '.join(''.join(rebuilt))==raw
    assert all(definition[i][1]==definition[i+1][0] for i in range(len(definition)-1))
    runs=[]
    for m in re.finditer('[ab]{16,}',s):
        runs.append(dict(start=m.start(),end=m.end(),length=len(m.group())))
    assert [(r['start'],r['end']) for r in runs]==[(91,195),(959,999)]
    cipher=s[895:959]+s[999:1063]
    blob=base64.b64decode(cipher,validate=True)
    assert base64.b64encode(blob).decode()==cipher
    assert blob==(ROOT/'data/locked_salphaseion_short.bin').read_bytes()
    # Enumerate ends past the second-half start; preserve all input in each prefix.
    endings=[]
    for end in range(1000,len(s)+1):
        b64=s[895:959]+s[999:end]
        try:
            b=base64.b64decode(b64,validate=True)
        except ValueError:
            continue
        if base64.b64encode(b).decode()==b64 and b.startswith(b'Salted__') and (len(b)-16)%16==0:
            endings.append(dict(end=end,base64_length=len(b64),raw_bytes=len(b)))
    assert [r['end'] for r in endings]==[1063]
    cosmic=re.sub(r'\s+','',bodies[1]); cosmicbytes=base64.b64decode(cosmic,validate=True)
    assert cosmicbytes==(ROOT/'data/locked_cosmic_duality.bin').read_bytes()
    dbbi=s[:91]; faed=s[195:765]
    grammar={name:prime_states(value,slot) for name,value,slot in [
        ('DBBI',dbbi,1),('whole_initial_765',s[:765],1),
        ('DBBI_FAED_label_removed',dbbi+faed,1),('FAED_restart',faed,1),
        ('FAED_continuing_after83',faed,84),('FAED_continuing_after84',faed,85)]}
    assert grammar['DBBI']['complete_slots']==[83,84]
    assert prime_states('x' * 110)['complete_slots']==[]
    # Full-range control: slot 101 is prime and cannot consume x.
    assert prime_states('x',101)['maximum_consumed']==0
    summary=dict(source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                 original_whitespace='Exactly one ASCII space between all 1075 characters, no other grouping',
                 compact_length=len(s),lossless_original_textarea_roundtrip=True,
                 long_binary_runs=runs,literal_z_offsets=[i for i,c in enumerate(s) if c=='z'],
                 separator_z_offsets=[765,829,859],ciphertext_z_offset=958,
                 full_short_cipher_valid_endings=endings,
                 accounting=dict(unknown_fields=661,encoded_labels=236,separators=3,literals=47,short_base64=128),
                 prime_grammar=grammar,cosmic=dict(base64_length=len(cosmic),raw_bytes=len(cosmicbytes)),
                 undecoded_fraction=661/1075,
                 conclusion='Wrapper fully reconstructed; unknown fields preserved verbatim, not explained cryptographically')
    assert sum(summary['accounting'].values())==1075
    (OUT/'segments.json').write_text(json.dumps(segments,indent=2))
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2))
    (OUT/'reconstructed_original_textarea.txt').write_text(' '.join(''.join(rebuilt)))
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
