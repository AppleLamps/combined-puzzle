"""Test complete variable-length token streams against full source passages."""
import hashlib
import itertools
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-13_faed_structure'

def tokenize(s,prefixes):
    tokens=[]; spans=[]; i=0
    while i<len(s):
        n=2 if s[i] in prefixes else 1
        if i+n>len(s):return None
        tokens.append(s[i:i+n]);spans.append([i,i+n]);i+=n
    assert ''.join(tokens)==s
    return tokens,spans

def match(tokens,text):
    forward={};reverse={}
    for a,b in zip(tokens,text):
        if a in forward and forward[a]!=b:return None
        if b in reverse and reverse[b]!=a:return None
        forward[a]=b;reverse[b]=a
    return forward

def main():
    faed=(ROOT/'data/FAED_570.txt').read_text().strip()
    dbbi=(ROOT/'data/DBBI_91.txt').read_text().strip()
    movie=(ROOT/'reference_texts/matrix_reloaded_architect_scene_scott_manning.md').read_text(encoding='utf-8')
    utterances=re.findall(r'^\*\*(?:The Architect|Neo):\*\*\s*(.*)$',movie,re.M)
    sources={'puzzle':(ROOT/'data/architect_letters_1539.txt').read_text(),
             'film_dialogue':' '.join(utterances),
             'film_architect_only':' '.join(re.findall(r'^\*\*The Architect:\*\*\s*(.*)$',movie,re.M))}
    forms={}
    for name,text in sources.items():
        normal=re.sub('[^A-Z]','',text.upper())
        forms[name+'/letters']=normal
        forms[name+'/IJmerged']=normal.replace('J','I')
    manifest=dict(model='Two a..i symbols introduce two-character tokens; other symbols are single-character tokens',
                  motivation='bg is the prior DBBI 64-token/16-symbol lead; nine columns with two row prefixes allow 25 codes, a possible modified checkerboard',
                  families='All 36 prefix pairs; full normal and reversed token order; source plaintext letters and I/J merged',
                  criterion='One-to-one token substitution must reproduce an entire source window, with no omissions',
                  warning='Changing to a nine-column board is a hypothesis; all-25 coverage in long FAED is not independent evidence',
                  source_hashes={n:hashlib.sha256((ROOT/'data'/n).read_bytes()).hexdigest() for n in ('DBBI_91.txt','FAED_570.txt')})
    (OUT/'token_manifest.json').write_text(json.dumps(manifest,indent=2))
    parsed=[];matches=[];checks=0
    for pair in itertools.combinations('abcdefghi',2):
        result=tokenize(faed,pair)
        if result is None:continue
        tokens,spans=result; d=tokenize(dbbi,pair)
        row=dict(prefixes=''.join(pair),faed_tokens=len(tokens),faed_symbols=len(set(tokens)),tokens=tokens,spans=spans,
                 dbbi_tokens=len(d[0]) if d else None,dbbi_symbols=len(set(d[0])) if d else None)
        parsed.append(row)
        for direction,sequence in [('forward',tokens),('reverse',tokens[::-1])]:
            for source,text in forms.items():
                for start in range(len(text)-len(sequence)+1):
                    checks+=1; window=text[start:start+len(sequence)]
                    mapping=match(sequence,window)
                    if mapping:
                        assert ''.join(mapping[t] for t in sequence)==window
                        matches.append(dict(prefixes=row['prefixes'],direction=direction,source=source,start=start,
                                            plaintext=window,mapping=mapping))
    # Token repeat constraints reject both inconsistent reuse and non-bijective mappings.
    assert match(['b','a','b'],'ABA')=={'b':'A','a':'B'}
    assert match(['b','a','b'],'ABC') is None and match(['b','a'],'AA') is None
    bg=next(r for r in parsed if r['prefixes']=='bg')
    summary=dict(complete_prefix_families=len(parsed),full_window_comparisons=checks,matches=matches,
                 bg_summary={k:v for k,v in bg.items() if k not in ('tokens','spans')},
                 controls_passed=True,status='No inference from short words; entire token streams retained')
    (OUT/'token_parses.json').write_text(json.dumps(parsed,indent=2))
    (OUT/'token_summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
