"""Independent Python reproduction and an end-to-end planted search fixture."""
import json
import sys
from pathlib import Path
from restore_lossy_decimal import recover

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-14_lossy_hill'


def transform(source,matrix,bias,halves_in,halves_out):
    half=len(source)//2
    blocks=[(source[i],source[i+half]) for i in range(half)] if halves_in else list(zip(source[::2],source[1::2]))
    transformed=[((matrix[0]*a+matrix[1]*b+bias[0])%9,(matrix[2]*a+matrix[3]*b+bias[1])%9) for a,b in blocks]
    return [p[j] for j in range(2) for p in transformed] if halves_out else [v for p in transformed for v in p]


def main():
    if sys.argv[-1]=='prepare':
        msg=(b'This is the complete planted control. The zero and nine digits share one residue, '
             b'but the search must still recover every byte of this message. ')
        msg=(msg*2)[:236]
        digits=str(int.from_bytes(msg,'big')).zfill(570)
        assert len(digits)==570 and '0' in digits and '9' in digits
        c=transform(list(map(int,digits)),[1,2,3,4],[5,7],False,False)
        (OUT/'control_cipher.txt').write_text(''.join(chr(96+(v or 9)) for v in c))
        (OUT/'control_expected.json').write_text(json.dumps(dict(text=msg.decode(),digits=digits,
                                                               inverse_matrix=[7,1,6,4],inverse_bias=[3,5]),indent=2))
        print('Prepared 236-byte full-plaintext control with a 570-digit padded decimal input.')
        return
    checked=0
    for source_file,result_file in [(ROOT/'data/FAED_570.txt',OUT/'pair_survivors.jsonl'),
                                    (OUT/'control_cipher.txt',OUT/'control_pair_survivors.jsonl')]:
        source=[(ord(c)-96)%9 for c in source_file.read_text().strip()]
        for line in result_file.read_text().splitlines():
            r=json.loads(line)
            actual=transform(source[::-1] if r['reverse'] else source,r['matrix'],r['bias'],r['halvesIn'],r['halvesOut'])
            assert ''.join(map(str,actual))==r['residues']
            a,b,c,d=r['matrix'];q=pow((a*d-b*c)%9,-1,9)
            inv=[q*v%9 for v in (d,-b,-c,a)]
            invbias=[-(inv[0]*r['bias'][0]+inv[1]*r['bias'][1])%9,
                     -(inv[2]*r['bias'][0]+inv[3]*r['bias'][1])%9]
            roundtrip=transform(actual,inv,invbias,r['halvesOut'],r['halvesIn'])
            assert roundtrip==(source[::-1] if r['reverse'] else source)
            checked+=1
    expected=json.loads((OUT/'control_expected.json').read_text())
    survivors=[json.loads(line) for line in (OUT/'control_pair_survivors.jsonl').read_text().splitlines()]
    native=[r for r in survivors if r['matrix']==expected['inverse_matrix'] and r['bias']==expected['inverse_bias']
            and not r['reverse'] and not r['halvesIn'] and not r['halvesOut']]
    assert len(native)==1
    r=recover(native[0]['residues'])
    assert r['complete'] and any(h['text']==expected['text'] for h in r['hits'])
    result=dict(independently_reproduced_streams=checked,all_affine_roundtrips=True,
                planted_key_survived_exhaustive_search=True,planted_full_plaintext_recovered=True,
                planted_plaintext_bytes=len(expected['text']),restoration_nodes=r['nodes'])
    (OUT/'independent_verification.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
