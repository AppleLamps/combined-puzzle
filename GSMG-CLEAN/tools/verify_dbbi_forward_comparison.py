"""Independently check retained endpoint bookkeeping and forward arithmetic."""
import argparse
import json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('run',type=Path);args=ap.parse_args()
    root=Path(__file__).resolve().parents[1];run=args.run
    models=json.loads((run/'models.json').read_text())
    records=json.loads((run/'forward_comparisons.json').read_text())
    text=(root/'data/DBBI_91.txt').read_text().strip()
    faed=(root/'data/FAED_570.txt').read_text().strip()
    digit_values=[ord(c)-96 for c in faed]
    n=int(''.join(map(str,digit_values)))
    arrays={'digit_values':digit_values,'decimal_integer_bytes':list(n.to_bytes((n.bit_length()+7)//8,'big'))}
    for model in models.values():
        assert ''.join(c['token'] for c in model['cells'])==text
        assert [i for c in model['cells'] for i in range(c['start'],c['end'])]==list(range(91))
        payload=''.join(c['token'] for c in model['cells'] if not c['prime'])
        assert payload==model['payload']
        mi=pi=0;rebuilt=[]
        for slot in range(1,model['logical_cells']+1):
            prime=slot>1 and all(slot%d for d in range(2,slot))
            if prime:rebuilt.append(model['schedule'][mi]['token']);mi+=1
            else:rebuilt.append(payload[pi]);pi+=1
        assert ''.join(rebuilt)==text
    for rec in records:
        values=arrays[rec['representation']];h,w=rec['shape'];assert h*w==len(values)
        rows=[sum(values[i*w+j] for j in range(w)) for i in range(h)]
        cols=[sum(values[i*w+j] for i in range(h)) for j in range(w)]
        expected={'rows':rows,'columns':cols,'rows_columns':rows+cols,'columns_rows':cols+rows}[rec['axis']]
        if rec['reverse']:expected=expected[::-1]
        assert expected==rec['sums']
        assert ''.join(map(str,expected))==rec['digits']
        assert rec['length_compatible']==(len(rec['digits'])==len(models[rec['model']]['payload']))
        if not rec['length_compatible']:assert rec['predicted_dbbi'] is None and not rec['exact_dbbi']
    result=dict(models_roundtrip=2,source_character_ownership=True,margin_records_verified=len(records),
                controls_note='See test_compare_dbbi_forward_models.py for planted 83/84 forward recovery and mutation controls')
    (run/'independent_verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()