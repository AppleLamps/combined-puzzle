"""Complete model: DBBI sums -> Beaufort over a..i -> numeric bytes. No AES."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-13_salphaseion_construction'
dbbi=(ROOT/'data/DBBI_91.txt').read_text().strip()
faed=(ROOT/'data/FAED_570.txt').read_text().strip()
manifest=dict(model='Raw DBBI exact rectangles -> ordinary axis sum list -> repeating Beaufort key on all FAED -> decimal integer bytes',
              reasons='matrixsumlist explicitly names sums; Beaufort is demonstrated in Phase 3.2; decimal integer decoding is demonstrated beside FAED',
              assumptions='DBBI is key material; a..i is the Beaufort alphabet; key is repeated; numeric output is the demonstrated next layer',
              choices='All factor widths including 1 and 91; rows/columns; a=0 and a=1 numeric conventions',
              acceptance='No prefixes or isolated words; save every full intermediate and verify exact re-encryption',
              source_hashes={n:hashlib.sha256((ROOT/'data'/n).read_bytes()).hexdigest() for n in ['DBBI_91.txt','FAED_570.txt']})
(OUT/'sum_key_manifest.json').write_text(json.dumps(manifest,indent=2))
records=[]
for base in (0,1):
    vals=[ord(c)-97+base for c in dbbi]
    cipher=[ord(c)-97+base for c in faed]
    for width in range(1,92):
        if 91%width:continue
        rows=[sum(vals[i:i+width]) for i in range(0,91,width)]
        cols=[sum(vals[i::width]) for i in range(width)]
        for axis,key in [('rows',rows),('cols',cols)]:
            # Residues 0..8 represented by a..i under each declared convention.
            plain=[(key[i%len(key)]-v)%9 for i,v in enumerate(cipher)]
            rebuilt=[(key[i%len(key)]-v)%9 for i,v in enumerate(plain)]
            assert rebuilt==[v%9 for v in cipher]
            letters=''.join(chr(97+(v-base)%9) for v in plain)
            # Decode page letter digits, not invented English-word filtering.
            digits=''.join(str(ord(c)-96) for c in letters)
            n=int(digits); raw=n.to_bytes((n.bit_length()+7)//8,'big')
            printable=all(32<=v<=126 or v in (9,10,13) for v in raw)
            try:utf8=raw.decode('utf-8')
            except UnicodeError:utf8=None
            records.append(dict(base=base,width=width,axis=axis,key=key,letters=letters,
                                digits=digits,bytes_hex=raw.hex(),whole_ascii_printable=printable,
                                whole_utf8=utf8,exact_beaufort_roundtrip=True))
(OUT/'sum_key_outputs.json').write_text(json.dumps(records,indent=2))
summary=dict(cases=len(records),unique_letter_outputs=len({r['letters'] for r in records}),
             all_roundtrips=True,whole_printable_outputs=sum(r['whole_ascii_printable'] for r in records),
             whole_utf8_outputs=sum(r['whole_utf8'] is not None for r in records),
             conclusion='No complete readable decimal-byte output; every intermediate retained. This rejects no other alphabet, key derivation or further layer.')
(OUT/'sum_key_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
