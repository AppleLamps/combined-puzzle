"""Candidates for 'return to the source codes' read as Satoshi's genesis comment block.
Values are pulled by script from main.cpp (original Bitcoin v0.1.0, trottier/original-bitcoin),
lines 1439-1448, never retyped."""
import re, sys
src = open(sys.argv[1], encoding='latin-1').read().splitlines()
blk = src[1438:1448]
vals = {}
for l in blk:
    m = re.match(r'\s*//\s*(\S+)\s*=\s*(.+?)\s*$', l)
    if m: vals[m.group(1)] = m.group(2)
for k, v in vals.items(): print('#', k, '=', v, file=sys.stderr)
out = []
def forms(v):
    f = [v, v.lower()]
    if v.lower().startswith('0x'): f += [v[2:], v[2:].lower()]
    return f
note = {
 'GetHash()': "G2: the block's first source code, the genesis hash, sits one line above the line the solver already used",
 'hashMerkleRoot': "G3: the second code in the same block, the merkle root",
 'txNew.vout[0].scriptPubKey': "G1: the only other code in the block in the same reversed-hex 0x form as the code you carry; strip OP_CHECKSIG",
 'txNew.vin[0].scriptSig': "G5: the whole raw scriptSig line, including what precedes 'after 4'",
 'block.nNonce': "G6: block header constants", 'block.nTime': "G6", 'block.nBits': "G6",
 'txNew.vout[0].nValue': "G6", 'block.nVersion': None,
}
for k, v in vals.items():
    if note.get(k) is None: continue
    v = v.replace(' OP_CHECKSIG', '')
    out.append('# ' + note[k])
    out += forms(v)
# G4: the code you carry, disseminated (decoded) back to text
p6 = vals['txNew.vin[0].scriptSig'].split()[-1]
txt = bytes.fromhex(p6[2:])[::-1].decode()
out.append("# G4: the code you hopefully carry, temporarily disseminated: part 6 decoded to the headline")
out += [txt, txt.replace(' ', ''), txt.lower(), txt.lower().replace(' ', ''),
        re.sub(r'[^a-z0-9]', '', txt.lower())]
# G7: the block as one object, the values concatenated in source order
cat = ''.join(v.replace(' OP_CHECKSIG', '') for k, v in vals.items())
out.append('# G7: the whole comment block values, concatenated in source order')
out += [cat]
print('\n'.join(dict.fromkeys(out)))
