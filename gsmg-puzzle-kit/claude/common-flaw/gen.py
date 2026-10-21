# Cross-camp pairing: matrixsumlist computed on the poster matrix (data camp's most literal reading)
# x lastwordsbeforearchichoice as the film's Architect line (riddle camp's survivor, S1 wording).
import json, os
from assembly import assemble
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'matrix.json'), encoding='utf-8') as f:
    m = json.load(f)
g=[[int(c) for c in r] for r in m['bit_grid']]
assert m['cell_grid'][7][4]=='F'
lists={}
for fv in (0,1):
    G=[r[:] for r in g]; G[7][4]=fv
    lists[f'rows_F{fv}']=[sum(r) for r in G]
    lists[f'cols_F{fv}']=[sum(G[i][j] for i in range(14)) for j in range(14)]
def forms(L):
    return {'digits':''.join(map(str,L)),'comma':','.join(map(str,L)),'commaspace':', '.join(map(str,L)),
            'space':' '.join(map(str,L)),'pyrepr':str(L),'json':json.dumps(L,separators=(',',':'))}
M=[]
for k,L in lists.items():
    for f,s in forms(L).items(): M.append(s)
M=list(dict.fromkeys(M))
LW=['sheisgoingtodieandthereisnothingthatyoucandotostopit','sheisgoingtodieandthereisnothingyoucandotostopit',
    'nothingthatyoucandotostopit','stopit','wewont','theproblemis']
out = assemble(M, LW)
# Compare membership, not merely a count: all four pair forms and M alone.
expected = set(M) | {s for a in M for b in LW
                     for s in (a+b, b+a, a+b+'thispassword', b+a+'thispassword')}
assert out == expected
assert len(M) == 24 and len(LW) == 6 and len(out) == 600
if __name__ == '__main__':
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cross.txt')
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# M alone (python list / json forms are new; digit/comma/space forms were in doc 114/115 pools)\n')
        f.write('\n'.join(M) + '\n')
        f.write('# Historical M+L, L+M, M+L+thispassword subset\n')
        historical = [s for a in M for b in LW for s in (a+b, b+a, a+b+'thispassword')]
        f.write('\n'.join(historical) + '\n')
        f.write('# Corrected missing L+M+thispassword assemblies; NOT SEARCHED\n')
        f.write('\n'.join(b+a+'thispassword' for a in M for b in LW) + '\n')
    print(len(M), 'M strings;', len(out), 'unique assembly candidates (not searched)')
