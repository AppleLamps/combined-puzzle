from lib import *
t = re.sub(r'\s', '', open(F + r'\salphaseion-textarea.txt').read())
runs = {'r91': t[0:91], 'r570': t[195:765]}
for nm, r in runs.items():
    d = [ord(c) - 96 for c in r]
    print(nm, len(d), 'digitsum', sum(d))
    for rows in range(2, len(d)):
        if len(d) % rows: continue
        cols = len(d) // rows
        M = [d[i * cols:(i + 1) * cols] for i in range(rows)]
        rs = [sum(x) for x in M]
        cs = [sum(M[i][j] for i in range(rows)) for j in range(cols)]
        for lab, L in (('rows', rs), ('cols', cs)):
            asc = bytes(v for v in L if 0 <= v < 256)
            al = ''.join(chr(65 + v % 26) for v in L)
            pr = printable(bytes(v % 256 for v in L))
            print(f'  {rows}x{cols} {lab} n={len(L)} min={min(L)} max={max(L)} printable={pr:.2f} {al[:60]}')
