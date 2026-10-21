"""Bounded correction of the historical 'leftover e' Hill-key hypothesis."""
import json
from math import gcd
from pathlib import Path
from audit_dbbi_accounting import signed, summed
from audit_dbbi_prime_grammar import parse

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-13_dbbi_accounting'


def determinant(a):
    return a[0]*(a[4]*a[8]-a[5]*a[7])-a[1]*(a[3]*a[8]-a[5]*a[6])+a[2]*(a[3]*a[7]-a[4]*a[6])


def inverse(a,n):
    if gcd(determinant(a),n)!=1:
        return None
    q=pow(determinant(a),-1,n)
    return [q*v%n for v in (a[4]*a[8]-a[5]*a[7],a[2]*a[7]-a[1]*a[8],a[1]*a[5]-a[2]*a[4],
                             a[5]*a[6]-a[3]*a[8],a[0]*a[8]-a[2]*a[6],a[2]*a[3]-a[0]*a[5],
                             a[3]*a[7]-a[4]*a[6],a[1]*a[6]-a[0]*a[7],a[0]*a[4]-a[1]*a[3])]


def transform(values,matrix,n,layout):
    if layout=='adjacent':
        blocks=[values[i:i+3] for i in range(0,len(values),3)]
    else:
        width=len(values)//3
        blocks=[[values[i],values[i+width],values[i+2*width]] for i in range(width)]
    out=[[sum(matrix[3*r+c]*v[c] for c in range(3))%n for r in range(3)] for v in blocks]
    return [v for block in out for v in block] if layout=='adjacent' else [block[r] for r in range(3) for block in out]


def main():
    dbbi=(ROOT/'data/DBBI_91.txt').read_text().strip()
    faed=(ROOT/'data/FAED_570.txt').read_text().strip()
    p=next(p for p in parse(dbbi,'e') if len(p)==84)
    values=signed(p)
    sums,word=summed(values[:-1])
    assert word=='hillfexmgsgl' and values[-1]==5
    key_text=word[4:]+dbbi[-1]
    assert key_text=='fexmgsgle'
    keys={'corrected_letters_A0':[ord(c)-97 for c in key_text],
          'corrected_letters_A1':[ord(c)-96 for c in key_text],
          'corrected_raw_sums':sums[4:]+[5]}
    manifest=dict(hypothesis='Reserve final e from the matrix sum, then append it to the remaining eight rendered letters or raw sums',
                  justification='Correct the actual double-counting premise in historical hill_faed_exact.cjs; reserving the cell is still an unproven operation',
                  corrected_key=key_text,key_vectors=keys,
                  scope='3x3 invertible Hill matrices; mod9 and mod10; transpose; encrypt/decrypt; a=0/a=1 input; adjacent/three-rail blocks; complete decimal/base9 integer outputs',
                  criterion='Full reversible transform; retain every output; no substring success, passwords, or AES',
                  limitation='A negative result covers these corrected constructions only; an output format alone is not authentication')
    results=[]; singular=[]; reviews=[]
    for modulus in (9,10):
        for key_name,key in keys.items():
            for transposed in (False,True):
                matrix=[key[c*3+r]%modulus for r in range(3) for c in range(3)] if transposed else [v%modulus for v in key]
                inv=inverse(matrix,modulus)
                if inv is None:
                    singular.append(dict(modulus=modulus,key=key_name,transposed=transposed,determinant=determinant(matrix)%modulus))
                    continue
                for direction,m in [('decrypt',inv),('encrypt',matrix)]:
                    undo=matrix if direction=='decrypt' else inv
                    for input_base in (0,1):
                        source=[(ord(c)-97+input_base)%modulus for c in faed]
                        for layout in ('adjacent','three_rails'):
                            out=transform(source,m,modulus,layout)
                            assert transform(out,undo,modulus,layout)==source
                            rec=dict(modulus=modulus,key=key_name,transposed=transposed,direction=direction,input_base=input_base,layout=layout,
                                     residues=out,roundtrip=True,integer_views=[])
                            forms=[('decimal_residues',out,10)]
                            if modulus==9:
                                forms += [('decimal_one_based',[(v-input_base)%9+1 for v in out],10),
                                          ('base9_zero_based',[(v-input_base)%9 for v in out],9)]
                            for name,digits,radix in forms:
                                n=0
                                for digit in digits:n=radix*n+digit
                                raw=n.to_bytes((n.bit_length()+7)//8,'big')
                                printable=sum(32<=v<=126 or v in (9,10,13) for v in raw)/len(raw)
                                view=dict(name=name,radix=radix,bytes=len(raw),hex=raw.hex(),printable_ascii_fraction=printable)
                                try:view['utf8']=raw.decode('utf-8')
                                except UnicodeError:pass
                                rec['integer_views'].append(view)
                                if printable==1 or 'utf8' in view:
                                    reviews.append(dict(model=len(results),view=view))
                            results.append(rec)
    # A planted decimal-text -> Hill -> inverse -> decimal-text control.
    known=b'A complete reversible control message.'
    digit_values=[int(c) for c in str(int.from_bytes(known,'big'))]
    padded=[0]*(-len(digit_values)%3)+digit_values
    matrix=[1,2,3,0,1,4,0,0,1]
    for layout in ('adjacent','three_rails'):
        enc=transform(padded,matrix,10,layout)
        dec=transform(enc,inverse(matrix,10),10,layout)
        n=int(''.join(map(str,dec)))
        assert n.to_bytes((n.bit_length()+7)//8,'big')==known
    summary=dict(corrected_key=key_text,complete_models=len(results),integer_views=sum(len(r['integer_views']) for r in results),
                 singular_matrices=singular,format_reviews=reviews,
                 highest_ascii_fraction=max(v['printable_ascii_fraction'] for r in results for v in r['integer_views']),
                 controls_passed=True,status='No authenticated result; all intermediate outputs retained')
    for name,data in [('reserved_e_manifest.json',manifest),('reserved_e_results.json',results),('reserved_e_summary.json',summary)]:
        (OUT/name).write_text(json.dumps(data,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
