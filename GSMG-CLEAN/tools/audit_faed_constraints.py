"""Derive necessary keystreams from full source passages, not guessed keys."""
import hashlib
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-13_faed_constraints'

def shortest_period(s):
    pi=[0]*len(s)
    for i in range(1,len(s)):
        j=pi[i-1]
        while j and s[i]!=s[j]:j=pi[j-1]
        if s[i]==s[j]:j+=1
        pi[i]=j
    return len(s)-pi[-1] if s else 0

def main():
    OUT.mkdir(exist_ok=True)
    faed=(ROOT/'data/FAED_570.txt').read_text().strip()
    c=[ord(x)-96 for x in faed]
    movie=(ROOT/'reference_texts/matrix_reloaded_architect_scene_scott_manning.md').read_text(encoding='utf-8')
    puzzle=(ROOT/'data/architect_plaintext_readable.txt').read_text(encoding='utf-8')
    blocks=[('puzzle_speech',puzzle)]
    for line_number,line in enumerate(movie.splitlines(),1):
        m=re.match(r'\*\*The Architect:\*\*\s*(.*)',line)
        if m:blocks.append((f'movie_architect_line_{line_number}',m.group(1)))
    # Only complete word windows within one Architect utterance; no navigation,
    # Markdown headers, or mixed speakers. Source text remains unchanged.
    quotes={}
    for source,block in blocks:
        words=list(re.finditer(r'\S+',block))
        for i in range(len(words)):
            for j in range(i,len(words)):
                t=block[words[i].start():words[j].end()]
                variants=[('exact',t),('lower',t.lower()),('connected',re.sub('[^a-z0-9]','',t.lower()))]
                if all(len(v.encode())>237 for _,v in variants):break
                for form,v in variants:
                    if len(v.encode()) in (236,237):
                        quotes.setdefault(v,[]).append(dict(source=source,first_word=i,last_word=j,form=form))
    old=json.loads((ROOT/'runs/2026-09-13_prime_control_faed/outputs.json').read_text())
    max_key=max(len(k['key']) for r in old for k in r['key_sources'])
    manifest=dict(task='Test necessary repeated-key periodicity for 236/237-byte Architect passages',
                  primary='Natural decimal plaintext and ciphertext lengths must agree',
                  explicit_alternatives=['Left-pad shorter decimal plaintext to 570 digits',
                                         'Restore one omitted leading zero to ciphertext for 571-digit plaintext'],
                  operators=['Beaufort K=C+P mod10','Vigenere K=C-P mod10'],
                  target_lengths=[236,237],source_scope='Within single Architect utterances and modified puzzle speech, complete word boundaries',
                  comparison_key_length_limit=max_key,
                  limitations='No claim other byte lengths, transcripts, ciphers, or nontext outputs are excluded; these two cipher families are hypotheses',
                  sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['data/FAED_570.txt','data/architect_plaintext_readable.txt','reference_texts/matrix_reloaded_architect_scene_scott_manning.md']})
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
    records=[]; digit_counts={}; zero_counts=[]
    for text,provenance in quotes.items():
        digits=str(int.from_bytes(text.encode(),'big')); p=[int(x) for x in digits]
        digit_counts[len(digits)]=digit_counts.get(len(digits),0)+1
        zero_counts.append(digits.count('0'))
        if len(p)==570:cases=[('natural',c,p)]
        elif len(p)<570:cases=[('left_padded_plaintext',c,[0]*(570-len(p))+p)]
        elif len(p)==571:cases=[('omitted_ciphertext_zero',[0]+c,p)]
        else:continue
        for mode,cv,pv in cases:
            for family,sign in [('beaufort',1),('vigenere',-1)]:
                k=[(x+sign*y)%10 for x,y in zip(cv,pv)]
                period=shortest_period(k)
                assert all(k[i]==k[i%period] for i in range(len(k)))
                records.append(dict(text=text,provenance=provenance,decimal_length=len(p),
                                    mode=mode,family=family,required_key=''.join(map(str,k)),
                                    minimum_key_period=period,within_prior_key_limit=period<=max_key))
    # Known non-dividing periods and an independent full encrypt/decrypt control.
    assert shortest_period([1,2,3,1,2])==3 and shortest_period([7]*8)==1
    p=[int(x) for x in str(int.from_bytes(b'thispassword','big'))]; k=[2,5,6]
    ct=[(k[i%3]-v)%10 for i,v in enumerate(p)]
    inferred=[(x+y)%10 for x,y in zip(ct,p)]
    assert shortest_period(inferred)==3
    summary=dict(unique_source_passages=len(quotes),natural_decimal_lengths=digit_counts,
                 minimum_zero_digits=min(zero_counts),all_passages_use_ten_digits=all(len(set(str(int.from_bytes(t.encode(),'big'))))==10 for t in quotes),
                 first_byte_upper_bound_570_digits_237_bytes=(10**570-1)//256**236,
                 inferred_keystreams=len(records),maximum_prior_derived_key_length=max_key,
                 smallest_required_period=min(r['minimum_key_period'] for r in records),
                 short_period_matches=[r for r in records if r['within_prior_key_limit']],
                 positive_controls_passed=True,
                 verdict='Scope is specific plaintext windows and repeating decimal arithmetic, not all possible DBBI-to-FAED mechanisms')
    (OUT/'required_keystreams.json').write_text(json.dumps(records,indent=2))
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
