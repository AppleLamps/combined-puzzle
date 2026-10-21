"""Full prime-derived sum-key models; ten-digit page alphabet plus mod-9 control."""
import hashlib
import json
import unicodedata
from pathlib import Path
from audit_dbbi_prime_grammar import parse

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-13_prime_control_faed'
DIGITS='oabcdefghi'

def text_reviews(raw):
    hits=[]
    for codec in ('utf-8','utf-16-le','utf-16-be','utf-32-le','utf-32-be','cp037','cp273'):
        try:t=raw.decode(codec)
        except UnicodeError:continue
        # Broad review gate, not authentication or a negative verdict for unknown bytes.
        score=sum(c in '\t\r\n' or not unicodedata.category(c).startswith('C') for c in t)/max(1,len(t))
        if score>=.95:
            hits.append(dict(codec=codec,noncontrol_fraction=score,text=t))
    return hits

def main():
    OUT.mkdir(exist_ok=True)
    dbbi=(ROOT/'data/DBBI_91.txt').read_text().strip()
    faed=(ROOT/'data/FAED_570.txt').read_text().strip()
    c=[DIGITS.index(ch) for ch in faed]
    manifest=dict(primary='Beaufort over decimal residues 0..9, as demonstrated by page a..i/o digits',
                  control='Previous closed a..i alphabet (mod 9, a=1)',
                  source_key_models='Both complete DBBI prime parses; restore prime index, zero prime cells, or preserve nonprime payload; all exact rectangles and both sum axes',
                  key_representations='Numeric list entries, or concatenated decimal digits of those entries',
                  scope='Full FAED transformed; one whole decimal integer decoded to bytes; no password guessing or AES',
                  warning='These operators and use of sums as repeating keys remain hypotheses. Round trips and format flags do not authenticate them.',
                  source_hashes={n:hashlib.sha256((ROOT/'data'/n).read_bytes()).hexdigest() for n in ('DBBI_91.txt','FAED_570.txt')})
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
    arrays={'raw91':[DIGITS.index(ch) for ch in dbbi]}
    for p in parse(dbbi,'e'):
        size=len(p)
        arrays[f'parse{size}_prime_restored']=[slot if pr else DIGITS.index(t) for slot,off,t,pr in p]
        arrays[f'parse{size}_prime_zero']=[0 if pr else DIGITS.index(t) for slot,off,t,pr in p]
        arrays[f'parse{size}_payload']=[DIGITS.index(t) for slot,off,t,pr in p if not pr]
        for color,token in [('blue','b'),('yellow','be')]:
            arrays[f'parse{size}_{color}_prime_restored']=[slot if pr and t==token else 0 if pr else DIGITS.index(t) for slot,off,t,pr in p]
    keys={}
    for name,values in arrays.items():
        for width in range(1,len(values)+1):
            if len(values)%width:continue
            sums=[('rows',[sum(values[i:i+width]) for i in range(0,len(values),width)]),
                  ('cols',[sum(values[i::width]) for i in range(width)])]
            for axis,seq in sums:
                for form,k in [('entries',seq),('decimal_digits',[int(ch) for ch in ''.join(map(str,seq))])]:
                    keys.setdefault(tuple(k),[]).append(dict(source=name,width=width,axis=axis,form=form))
    targets={n:(ROOT/'data'/n).read_bytes().strip() for n in ('architect_letters_1539.txt','DBBI_91.txt','FAED_570.txt')}
    records=[]; reviews=[]; seen={}; exact=[]
    for modulus in (10,9):
        for key,provenance in keys.items():
            residues=tuple((key[i%len(key)]-v)%modulus for i,v in enumerate(c))
            dedup=(modulus,residues)
            if dedup in seen:
                records[seen[dedup]]['key_sources'].append(dict(key=key,provenance=provenance))
                continue
            assert [(key[i%len(key)]-v)%modulus for i,v in enumerate(residues)]==[v%modulus for v in c]
            nums=residues if modulus==10 else tuple(v if v else 9 for v in residues)
            digits=''.join(map(str,nums)); n=int(digits)
            raw=n.to_bytes((n.bit_length()+7)//8,'big')
            assert str(int.from_bytes(raw,'big'))==digits.lstrip('0') or n==0
            row=dict(id=len(records),modulus=modulus,key_sources=[dict(key=key,provenance=provenance)],
                     digits=digits,zero_digits=digits.count('0'),leading_zero_digits=len(digits)-len(digits.lstrip('0')),
                     source_alphabet=''.join(DIGITS[v] for v in nums),bytes_hex=raw.hex(),
                     reversible_beaufort=True,review_status='UNRESOLVED_RETAINED')
            seen[dedup]=len(records); records.append(row)
            hits=text_reviews(raw)
            if hits:reviews.append(dict(id=row['id'],views=hits))
            for target,value in targets.items():
                if raw==value:exact.append(dict(id=row['id'],target=target))
    # A control containing zero digits must survive encode -> Beaufort -> inverse
    # -> integer bytes. Mod-9's 1..9 serialization cannot represent it literally.
    plain=b'thispassword'; ds=[int(ch) for ch in str(int.from_bytes(plain,'big'))]
    key=[17,23,41]; ct=[(key[i%3]-v)%10 for i,v in enumerate(ds)]
    back=[(key[i%3]-v)%10 for i,v in enumerate(ct)]
    assert ds==back and 0 in ds
    n=int(''.join(map(str,back))); assert n.to_bytes((n.bit_length()+7)//8,'big')==plain
    summary=dict(distinct_key_lists=len(keys),unique_full_outputs=len(records),
                 outputs_by_modulus={str(m):sum(r['modulus']==m for r in records) for m in (10,9)},
                 all_roundtrips=True,exact_matches=exact,format_review_outputs=len(reviews),
                 ascii_printable_outputs=sum(all(32<=v<=126 or v in (9,10,13) for v in bytes.fromhex(r['bytes_hex'])) for r in records),
                 zero_digit_positive_control=dict(plaintext=plain.decode(),decimal_digits=''.join(map(str,ds)),passed=True),
                 conclusion='No result authenticated by round-trip or format recognition alone; inspect reviews and retain unknown outputs')
    for filename,data in [('outputs.json',records),('format_reviews.json',reviews),('summary.json',summary)]:
        (OUT/filename).write_text(json.dumps(data,indent=2))
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
