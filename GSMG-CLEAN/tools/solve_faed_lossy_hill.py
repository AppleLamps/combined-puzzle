"""Recover arbitrary affine Hill keys for complete source quotations.

Unlike earlier numerical decoders, plaintext decimal 0 and 9 may coincide
modulo 9. No password guesses, truncated plaintext gates, or source edits.
"""
import hashlib
import json
import math
import random
import re
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'runs/2026-09-14_lossy_hill'


def inverse(a, modulus):
    a = [list(map(int, row)) + [int(i == j) for j in range(len(a))]
         for i, row in enumerate(a)]
    size = len(a)
    for col in range(size):
        pivot = next((i for i in range(col, size) if math.gcd(a[i][col], modulus) == 1), None)
        if pivot is None:
            return None
        a[col], a[pivot] = a[pivot], a[col]
        q = pow(a[col][col], -1, modulus)
        a[col] = [x*q % modulus for x in a[col]]
        for i in range(size):
            if i != col:
                q = a[i][col]
                a[i] = [(x-q*y) % modulus for x, y in zip(a[i], a[col])]
    return np.asarray([row[size:] for row in a], dtype=np.int64)


def basis(matrix, modulus):
    """A mod-3 basis lifts to Z/9Z; CRT handles mod 10 separately."""
    prime = 3 if modulus == 9 else modulus
    rows = []
    selected = []
    for i, row in enumerate(matrix):
        v = np.array(row, dtype=np.int64) % prime
        for pivot, reduced in rows:
            v = (v-v[pivot]*reduced) % prime
        nonzero = np.flatnonzero(v)
        if not len(nonzero):
            continue
        pivot = int(nonzero[0])
        v = v*pow(int(v[pivot]), -1, prime) % prime
        rows.append((pivot, v))
        selected.append(i)
        if len(rows) == matrix.shape[1]:
            inv = inverse(matrix[selected], modulus)
            assert inv is not None
            assert np.array_equal(inv @ matrix[selected] % modulus, np.eye(len(rows), dtype=np.int64))
            return selected, inv
    return None


def arrange(v, size, layout):
    return v.reshape(-1, size) if layout == 'adjacent' else v.reshape(size, -1).T


def recover(cipher, plains, size, cipher_layout, plain_layout, modulus):
    c = arrange(np.asarray(cipher), size, cipher_layout)
    design = np.column_stack((c, np.ones(len(c), dtype=np.int64)))
    factors = (9,) if modulus == 9 else (2, 5)
    bases = [basis(design, p) for p in factors]
    if any(b is None for b in bases):
        return None, []
    p = (plains.reshape(-1, len(c), size) if plain_layout == 'adjacent'
         else plains.reshape(-1, size, len(c)).transpose(0, 2, 1))
    survivors = np.arange(len(plains))
    keys = []
    for factor, (selected, inv) in zip(factors, bases):
        candidate_keys = np.einsum('ij,kjl->kil', inv, p[:, selected]) % factor
        # Test held-out blocks before allocating any complete predictions.
        held = [i for i in range(len(c)) if i not in selected]
        for start in range(0, len(held), 8):
            if not len(survivors):
                break
            ix = held[start:start+8]
            predicted = np.einsum('ij,kjl->kil', design[ix], candidate_keys[survivors]) % factor
            valid = np.all(predicted == p[survivors][:, ix] % factor, axis=(1, 2))
            survivors = survivors[valid]
        keys.append(candidate_keys)
    matches = []
    for index in survivors:
        key = keys[0][index] if modulus == 9 else (5*keys[0][index]+6*keys[1][index]) % 10
        assert np.array_equal(design @ key % modulus, p[index] % modulus)
        matches.append(dict(index=int(index),inverse_affine_key=key.tolist(),
                            plaintext_collision_positions=np.flatnonzero(plains[index] == 0).tolist()))
    return [b[0] for b in bases], matches


def main():
    OUT.mkdir(exist_ok=True)
    faed = (ROOT/'data/FAED_570.txt').read_text().strip()
    movie=(ROOT/'reference_texts/matrix_reloaded_architect_scene_scott_manning.md').read_text(encoding='utf-8')
    blocks=[('modified_architect',(ROOT/'data/architect_plaintext_readable.txt').read_text(encoding='utf-8'))]
    for i,line in enumerate(movie.splitlines(),1):
        match=re.match(r'\*\*(The Architect|Neo):\*\*\s*(.*)',line)
        if match:blocks.append((f'{match[1]}_line_{i}',match[2]))
    texts={}
    for source,block in blocks:
        words=list(re.finditer(r'\S+',block))
        for i in range(len(words)):
            for j in range(i,len(words)):
                raw=block[words[i].start():words[j].end()]
                connected=re.sub('[^a-z0-9]','',raw.lower())
                variants=[('exact',raw),('lower',raw.lower()),('upper',raw.upper()),
                          ('connected',connected),('connected_upper',connected.upper())]
                if min(len(t.encode()) for _,t in variants)>237:break
                for form,t in variants:
                    if len(t.encode()) in (225,226,236,237):
                        texts.setdefault(t,[]).append(dict(source=source,first_word=i,last_word=j,form=form))
    quotes={}
    for t,provenance in texts.items():
        n=int.from_bytes(t.encode(),'big')
        for view in ('decimal','base9','bijective_base9'):
            if view=='decimal':digits=str(n)
            else:
                v=n;ds=[]
                while v:
                    if view=='bijective_base9':v,d=divmod(v-1,9);ds.append(str(d+1))
                    else:v,d=divmod(v,9);ds.append(str(d))
                digits=''.join(reversed(ds))
            if 567<=len(digits)<=570:
                quotes.setdefault((t,view),dict(text=t,provenance=provenance,numeral_view=view,
                                               original_digit_length=len(digits),digits=digits.zfill(570)))
    passages = list(quotes.values())
    plaintexts = np.asarray([[int(c) for c in r['digits']] for r in passages], dtype=np.int64)
    source = np.asarray([ord(c)-96 for c in faed], dtype=np.int64)
    # Recover a planted affine key after a deliberately lossy decimal step.
    control_p = plaintexts[0]
    k = np.asarray([[1,2,3],[0,1,4],[0,0,1]], dtype=np.int64)
    offset = np.asarray([2,5,6])
    control_c = (control_p.reshape(-1,3) @ k + offset).flatten() % 9
    control_c[control_c == 0] = 9
    assert 0 in control_p and 9 in control_p
    for cl in ('adjacent','rails'):
        for pl in ('adjacent','rails'):
            cp = arrange(control_p,3,pl)
            cc = (cp @ k + offset) % 9
            encoded = cc.flatten() if cl == 'adjacent' else cc.T.flatten()
            encoded[encoded == 0] = 9
            selected, found = recover(encoded, plaintexts[:1],3,cl,pl,9)
            assert selected is not None and len(found) == 1
            corrupted = encoded.copy()
            corrupted[-1] = corrupted[-1] % 9 + 1
            assert recover(corrupted, plaintexts[:1],3,cl,pl,9)[1] == []
    manifest = dict(hypothesis='FAED is an affine Hill transform of a full decimal-encoded Architect quotation; mod9 deliberately identifies decimal zero and nine',
                    moduli=[9,10],block_sizes=[2,3,5,6,10,15],input_reversal=True,
                    layouts=['adjacent','rails'],unknown_keys='All affine matrices, including singular ones, when the ciphertext design has full rank',
                    normalization='Exact/lower/upper/connected/connected_upper complete-word windows from one utterance; bigint big endian; decimal/base9/bijective_base9; left zero padding to 570 digits only',
                    sources={'FAED_570.txt':hashlib.sha256(faed.encode()).hexdigest()},
                    limits='A full-text match is required. Rank-deficient models are reported as untested. Other plaintexts, padding placements, dimensions and nonlinear transforms remain open.')
    models = []
    hits = []
    for modulus in manifest['moduli']:
        for size in manifest['block_sizes']:
            for reverse in (False,True):
                for cl in manifest['layouts']:
                    for pl in manifest['layouts']:
                        selected, found = recover(source[::-1] if reverse else source, plaintexts, size, cl, pl, modulus)
                        model = dict(modulus=modulus,size=size,reverse=reverse,cipher_layout=cl,plain_layout=pl,
                                     basis_rows=selected,complete_matches=len(found),status='tested' if selected is not None else 'rank_deficient')
                        for row in found:
                            hits.append(dict(model=len(models),**row,passage=passages[row['index']]))
                        models.append(model)
    summary = dict(source_passages=len(set(r['text'] for r in passages)),numerical_plaintext_templates=len(passages),
                   templates_by_numeral_view={view:sum(r['numeral_view']==view for r in passages) for view in ('decimal','base9','bijective_base9')},
                   models=len(models),tested_models=sum(r['status']=='tested' for r in models),
                   rank_deficient_models=sum(r['status']=='rank_deficient' for r in models),
                   full_quotation_comparisons=len(passages)*sum(r['status']=='tested' for r in models),
                   complete_matches=len(hits),control_layouts=4,zero_nine_collision_control=True,mutation_controls=True)
    for name, obj in [('manifest.json',manifest),('passages.json',passages),('models.json',models),('matches.json',hits),('summary.json',summary)]:
        (OUT/name).write_text(json.dumps(obj,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()
