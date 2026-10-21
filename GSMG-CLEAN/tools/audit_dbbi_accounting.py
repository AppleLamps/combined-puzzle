"""Audit source consumption and complete Hill/Bifid compositions; no passwords."""
import hashlib
import itertools
import json
from collections import Counter
from math import gcd
from pathlib import Path

from audit_dbbi_prime_grammar import parse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'runs/2026-09-13_dbbi_accounting'
A = 'abcdefghiklmnopqrstuvwxyz'


def signed(p):
    return [(-slot if token == 'b' else slot) if prime else ord(token)-96
            for slot, offset, token, prime in p]


def summed(values):
    sums = [sum(values[c::12]) for c in range(12)]
    return sums, ''.join(chr(97+n%26) for n in sums)


def bifid(s, square, decrypt=True):
    coordinates = [divmod(square.index(c), 5) for c in s]
    if decrypt:
        stream = list(itertools.chain.from_iterable(coordinates))
        return ''.join(square[5*stream[i]+stream[i+len(s)]] for i in range(len(s)))
    stream = [r for r,c in coordinates]+[c for r,c in coordinates]
    return ''.join(square[5*stream[i]+stream[i+1]] for i in range(0,len(stream),2))


def inverse(m, n):
    a,b,c,d = m
    det = (a*d-b*c)%n
    if gcd(det,n) != 1:
        return None
    q = pow(det,-1,n)
    return tuple(q*x%n for x in (d,-b,-c,a))


def hill(s, alphabet, base, matrix):
    assert len(s)%2 == 0
    n = len(alphabet)
    v = [(alphabet.index(c)+base)%n for c in s]
    a,b,c,d = matrix
    out = []
    for x,y in zip(v[::2],v[1::2]):
        out.extend((alphabet[(a*x+b*y-base)%n], alphabet[(c*x+d*y-base)%n]))
    return ''.join(out)


def example_keys(plain, cipher, alphabet, base):
    n = len(alphabet)
    p = [(alphabet.index(c)+base)%n for c in plain]
    q = [(alphabet.index(c)+base)%n for c in cipher]
    rows = []
    for side in (0,1):
        rows.append([(a,b) for a in range(n) for b in range(n)
                     if (a*p[0]+b*p[1])%n == q[side]
                     and (a*p[2]+b*p[3])%n == q[side+2]])
    keys = [tuple(r1+r2) for r1,r2 in itertools.product(*rows)]
    return [k for k in keys if inverse(k,n) is not None]


def ic(s):
    return sum(v*(v-1) for v in Counter(s).values())/(len(s)*(len(s)-1))


def main():
    OUT.mkdir(exist_ok=True)
    dbbi = (ROOT/'data/DBBI_91.txt').read_text().strip()
    faed = (ROOT/'data/FAED_570.txt').read_text().strip()
    p84 = next(p for p in parse(dbbi,'e') if len(p)==84)
    p83 = next(p for p in parse(dbbi,'e') if len(p)==83)
    assert ''.join(t for _,_,t,_ in p84) == dbbi
    ownership = []
    for slot, offset, token, prime in p84:
        ownership.append(dict(slot=slot, source_span=[offset,offset+len(token)], token=token,
                              prime=prime, row=(slot-1)//12+1, column=(slot-1)%12+1,
                              value=signed([(slot,offset,token,prime)])[0]))
    covered = [i for r in ownership for i in range(*r['source_span'])]
    assert covered == list(range(91))
    vals = signed(p84)
    sums, instruction = summed(vals)
    assert instruction == 'hillfexmgsgq'
    final_column = [r for r in ownership if r['column']==12]
    assert final_column[-1]['source_span']==[90,91]
    assert [r['value'] for r in final_column] == [7,7,5,6,6,6,5]
    assert sum(r['value'] for r in final_column)==42
    shortened = summed(vals[:-1])
    alternate = summed(signed(p83))
    assert shortened[1]=='hillfexmgsgl'
    assert alternate[1]=='hillfexmgsql'
    colors = (ROOT/'data/poster_spiral_bits.txt').read_text().splitlines()[1]
    color_values = vals.copy()
    prime_rows = [r for r in ownership if r['prime']]
    for i,r in enumerate(prime_rows):
        color_values[r['slot']-1] = r['slot']*(1 if colors[i]=='Y' else -1)
    color_sums, color_instruction = summed(color_values)
    assert color_instruction=='xillfexmgsgq'
    square = ''.join(dict.fromkeys(dbbi+A))
    prefix_square = ''.join(dict.fromkeys(dbbi[:13]+A))
    assert square == prefix_square
    decoded = bifid(faed,square)
    assert decoded.startswith('btcseed')
    assert bifid(decoded,square,False)==faed
    assert decoded==(ROOT/'data/faed_bifid_570.txt').read_text().strip()
    arch = (ROOT/'data/architect_letters_1539.txt').read_text().strip().lower().replace('j','i')
    planted = arch[:570]
    assert bifid(bifid(planted,square,False),square)==planted
    constructions = []
    blocked = []
    conventions = []
    # Keep all 570 characters. The explicit example interpretation and alphabets
    # were already used in the prior carrier-only audit; no new keys are guessed.
    for alphabet_name,alphabet in [('natural25',A),('dbbi25',square),('natural26','abcdefghijklmnopqrstuvwxyz')]:
        for base in (0,1):
            for plain,cipher in [('fexm','gsgq'),('gsgq','fexm')]:
                keys = example_keys(plain,cipher,alphabet,base)
                conventions.append(dict(alphabet=alphabet_name,base=base,plain=plain,cipher=cipher,keys=keys))
                for key in keys:
                    inv = inverse(key,len(alphabet))
                    assert hill(plain,alphabet,base,key)==cipher
                    assert hill(hill(planted,alphabet,base,key),alphabet,base,inv)==planted
                    context = dict(alphabet=alphabet_name,base=base,plain=plain,cipher=cipher,key=key)
                    for order in ('bifid_then_hill','hill_then_bifid'):
                        if order=='bifid_then_hill':
                            value = hill(decoded,alphabet,base,inv)
                            back = bifid(hill(value,alphabet,base,key),square,False)
                            # Independent planted composition: encrypt in inverse order.
                            planted_cipher = bifid(hill(planted,alphabet,base,key),square,False) if set(hill(planted,alphabet,base,key))<=set(square) else None
                            if planted_cipher is not None:
                                assert hill(bifid(planted_cipher,square),alphabet,base,inv)==planted
                        else:
                            intermediate = hill(faed,alphabet,base,inv)
                            if not set(intermediate)<=set(square):
                                blocked.append(dict(**context,order=order,reason='Hill output contains J absent from the specified Bifid square',intermediate=intermediate))
                                continue
                            value = bifid(intermediate,square)
                            back = hill(bifid(value,square,False),alphabet,base,key)
                            planted_cipher = hill(bifid(planted,square,False),alphabet,base,key)
                            assert bifid(hill(planted_cipher,alphabet,base,inv),square)==planted
                        assert back==faed and len(value)==570
                        constructions.append(dict(**context,order=order,value=value,ic=ic(value),
                                                  full_architect_window_match=value in arch,roundtrip=True))
    source_claims = []
    for name in ('hill_faed_exact.cjs','hill_bifid_count_matrix.cjs'):
        p = ROOT.parent/'read/SOLVE'/name
        source_claims.append(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                                 opening=p.read_text(encoding='utf-8').splitlines()[:5]))
    result = dict(status='Accounting corrections verified; no recovered complete instruction',
                  hashes={name:hashlib.sha256((ROOT/'data'/name).read_bytes()).hexdigest() for name in ('DBBI_91.txt','FAED_570.txt')},
                  source_consumption=dict(raw_characters=91,logical_cells=84,unconsumed_characters=0,final_e_cell=ownership[-1]),
                  original_sums=sums,instruction=instruction,final_column=final_column,
                  remove_final_e=dict(sums=shortened[0],instruction=shortened[1]),
                  alternate83=dict(sums=alternate[0],instruction=alternate[1]),
                  poster_colors=dict(sums=color_sums,instruction=color_instruction,changed_prime=73,
                                     interpretation='Comparison under existing signed model, not a proposed correction'),
                  full_dbbi_square=square,prefix13_square_identical=True,bifid_prefix=decoded[:40],
                  conventions=conventions,complete_compositions=len(constructions),alphabet_incompatible_compositions=len(blocked),
                  exact_architect_matches=sum(r['full_architect_window_match'] for r in constructions),
                  controls_passed=True,historical_claims=source_claims)
    for name,data in [('summary.json',result),('ownership.json',ownership),('complete_compositions.json',constructions),('blocked_compositions.json',blocked)]:
        (OUT/name).write_text(json.dumps(data,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('conventions','historical_claims','final_column')},indent=2))
    print(json.dumps([dict(alphabet=r['alphabet'],base=r['base'],example=r['plain']+'->'+r['cipher'],order=r['order'],prefix=r['value'][:80],ic=r['ic']) for r in constructions],indent=2))


if __name__=='__main__':
    main()
