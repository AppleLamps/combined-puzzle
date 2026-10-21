import time, hashlib, sys
import harness as H
from lists import all_lists

LISTS = all_lists()

def encodings(L):
    out = {}
    out['cat'] = ''.join(map(str, L))
    out['comma'] = ','.join(map(str, L))
    out['space'] = ' '.join(map(str, L))
    if all(1 <= v <= 26 for v in L): out['a1z26'] = ''.join(chr(96 + v) for v in L)
    if all(0 <= v <= 9 for v in L):
        out['a1z26o'] = ''.join('o' if v == 0 else chr(96 + v) for v in L)
        for base in (5, 10):
            if all(v < base for v in L):
                n = 0
                for v in L: n = n * base + v
                out[f'b{base}dec'] = str(n); out[f'b{base}hex'] = format(n, 'x')
    out['sum'] = str(sum(L))
    try:
        n = int(out['cat']); h = format(n, 'x'); h = '0' * (len(h) % 2) + h
        out['rule2'] = bytes.fromhex(h)
    except Exception: pass
    if all(0 <= v < 256 for v in L): out['bytes'] = bytes(L)
    return out

LAST = ['', 'thispassword', 'hope', 'wewont', 'causality', 'choice', 'stopit', 'nothingthatyoucandotostopit',
        'hopeitisthequintessentialhumandelusion',
        'hopeitisthequintessentialhumandelusionsimultaneouslythesourceofyourgreateststrengthandyourgreatestweakness',
        'humphhopeitisthequintessentialhumandelusionsimultaneouslythesourceofyourgreateststrengthandyourgreatestweakness',
        'ifiwereyouiwouldhopethatwedontmeetagain', 'theproblemischoice', 'therearetwodoors',
        'takethisprivatekey', 'taketheprivatekey', 'takethe', 'privatekey', 'ciaobella', 'ciaobellao',
        'goodlucknevertheless', 'ireallyhopeyouretheone', 'theone', 'bccahhbiibibbibdcbahaidhfahiihic',
        'lastwordsbeforearchichoice', 'matrixsumlist', 'yellowblueprimes', 'yinyang']

def main():
    st = H.Stats(); t0 = time.time(); scal = 0
    for ln, L in LISTS.items():
        for en, v in encodings(L).items():
            vb = v if isinstance(v, bytes) else v.encode()
            # raw scalar test on integer readings
            if en in ('cat', 'b5dec', 'b10dec'):
                n = int(v) % H.N
                if n: scal += 1;
                if n and H.key_hits(n.to_bytes(32, 'big')): st.flags.append(('SCALAR', ln, en))
            for lw in LAST:
                lb = lw.encode()
                cands = [vb] if not lw else [vb + lb, lb + vb]
                for c in cands:
                    H.screen(c, st, f'{ln}|{en}|{lw}')
    dt = time.time() - t0
    print(f'candidates {st.cands}  decrypts {st.dec}  valid pads {st.valid} (expected {st.dec/256:.0f})  scalars {scal}  {dt:.0f}s')
    for f in st.flags: print('FLAG', f)

if __name__ == '__main__':
    main()
