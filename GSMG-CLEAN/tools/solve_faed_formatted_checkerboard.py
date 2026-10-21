"""Exact parameterized matching of complete variable-token FAED readings.

All 512 prefix subsets of a..i are covered, including empty/all controls.
Unlike earlier letters-only searches, source spaces/punctuation are retained.
"""
import hashlib
import itertools
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-14_formatted_checkerboard'


def parse_tokens(text,prefix):
    result=[];i=0
    while i<len(text):
        size=2 if text[i] in prefix else 1
        if i+size>len(text):return None
        result.append(text[i:i+size]);i+=size
    assert ''.join(result)==text
    return result


def previous(seq):
    seen={};result=[]
    for i,c in enumerate(seq):result.append(seen.get(c,-1));seen[c]=i
    return result


def matches(pattern,text):
    """Exact bijection, with previous positions relative to each window."""
    n=len(pattern)
    if n>len(text) or len(set(pattern))>len(set(text)):return []
    p=previous(pattern);t=previous(text)
    # Test repeated-symbol constraints first, then first occurrences. Both
    # are necessary: dropping the latter would allow nonbijective matches.
    order=[i for i in range(n) if p[i]>=0]+[i for i in range(n) if p[i]<0]
    found=[]
    for start in range(len(text)-n+1):
        if all((t[start+i]==start+p[i]) if p[i]>=0 else (t[start+i]<start) for i in order):
            window=text[start:start+n]
            mapping={}
            reverse={}
            for code,c in zip(pattern,window):
                assert mapping.setdefault(code,c)==c
                assert reverse.setdefault(c,code)==code
            assert [reverse[c] for c in window]==pattern
            found.append(dict(start=start,text=window,mapping=mapping))
    return found


def sources():
    movie=(ROOT/'reference_texts/matrix_reloaded_architect_scene_scott_manning.md').read_text(encoding='utf-8')
    blocks=[('modified_architect',(ROOT/'data/architect_plaintext_readable.txt').read_text(encoding='utf-8').strip())]
    for i,line in enumerate(movie.splitlines(),1):
        m=re.match(r'\*\*(The Architect|Neo):\*\*\s*(.*)',line)
        if m:blocks.append((f'{m[1]}_line_{i}',m[2]))
    result={}
    for name,text in blocks:
        for normalization,t in [('exact',text),('lower',text.lower()),('upper',text.upper()),
                                 ('letters_spaces',re.sub('[^a-z ]','',text.lower())),
                                 ('letters_only',re.sub('[^a-z]','',text.lower()))]:
            result.setdefault(t,[]).append(dict(source=name,normalization=normalization))
    return result


def main():
    OUT.mkdir(exist_ok=True)
    text=(ROOT/'data/FAED_570.txt').read_text().strip()
    blocks=sources();models=[];hits=[];tested_windows=0
    for mask in range(512):
        prefix=''.join(c for i,c in enumerate('abcdefghi') if mask>>i&1)
        for reverse in (False,True):
            tokens=parse_tokens(text[::-1] if reverse else text,prefix)
            row=dict(prefix=prefix,reverse=reverse,complete=tokens is not None)
            if tokens is not None:
                row.update(tokens=len(tokens),symbols=len(set(tokens)))
                for source,provenance in blocks.items():
                    if len(set(tokens))>len(set(source)):continue
                    tested_windows+=max(0,len(source)-len(tokens)+1)
                    for hit in matches(tokens,source):hits.append(dict(model=len(models),source=provenance,**hit))
            models.append(row)
    # A held-out mixed-case/punctuation control using FOUR prefix symbols.
    sample=('The problem is choice. There are two doors, and only one decision. '*6).strip()
    prefix='abcd';codes=[c for c in 'abcdefghi' if c not in prefix]+[a+b for a in prefix for b in 'abcdefghi']
    alphabet=sorted(set(sample));assert len(alphabet)<=len(codes)
    encoding=dict(zip(alphabet,codes))
    cipher=''.join(encoding[c] for c in sample)
    tokenized=parse_tokens(cipher,prefix)
    planted=matches(tokenized,'X'+sample+'X')
    assert len(planted)==1 and planted[0]['text']==sample and planted[0]['start']==1
    corrupt=sample[:3]+'?'+sample[4:]
    assert matches(tokenized,corrupt)==[]
    # Repeated spaces are symbols in their own right, not discarded padding.
    assert planted[0]['mapping'][encoding[' ']]==' '
    summary=dict(prefix_subsets=512,directional_models=len(models),
                 complete_tokenizations=sum(m['complete'] for m in models),source_views=len(blocks),
                 candidate_source_windows=tested_windows,complete_bijective_matches=len(hits),
                 mixed_case_punctuation_four_prefix_control=True,mutation_rejected=True)
    manifest=dict(model='Nine-column variable-length checkerboard: selected symbols start two-character tokens; others are single characters',
                  scope='Every subset of the nine symbols, both input orientations; all contiguous complete character windows within one saved utterance',
                  source_formatting=['exact','lower','upper','letters plus spaces','letters only'],
                  gate='Full bijective token-to-character equality, not a prefix or English score',
                  limitations='No transposition, homophonic many-to-one substitution, polyalphabetic layer, or unavailable/edited source text is ruled out.',
                  faed_sha256=hashlib.sha256(text.encode()).hexdigest())
    for name,obj in [('manifest.json',manifest),('models.json',models),('matches.json',hits),('summary.json',summary)]:
        (OUT/name).write_text(json.dumps(obj,indent=2))
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
