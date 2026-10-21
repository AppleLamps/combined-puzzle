import re,sys
from collections import Counter
cell=['WWKKWBWWKWKKWY', 'KKBKWWKKKWBWKK', 'KKWKKKWBWWKWWK', 'WKKWBWWWWKKKWK', 'WBKWWWKKWYWKKW', 'KWWKKWYWKWYWKK', 'KWWBKKWWWKWYWW', 'BKKWFWWWWWKWYW', 'WWWKKBWKKKKKWB', 'KKBKKKYWKKWWWK', 'KKWKWWWYWKKWKK', 'KKKKWWKWBWKKWW', 'WBWKKKWKWYWKKW', 'WKBWKKWKKWBWKK']
bit=['00110100101100', '11110011101011', '11011101001001', '01101000011101', '01100011000110', '10011000100011', '10011100010000', '11100000001000', '00011101111101', '11111100110001', '11010000011011', '11110010101100', '01011101000110', '01101101101011']
failures = []
def chk(n,c,e=''):
    if not c: failures.append(n)
    print(('PASS ' if c else 'FAIL ')+n,'' if c else e)
n=14
# spiral: start top-left, down first, counterclockwise inward
def spiral(n):
    seen=set();r=c=0;dr,dc=1,0;out=[]
    for _ in range(n*n):
        out.append((r,c));seen.add((r,c))
        nr,nc=r+dr,c+dc
        if not(0<=nr<n and 0<=nc<n) or (nr,nc) in seen:
            dr,dc=(dc,-dr) if False else {(1,0):(0,1),(0,1):(-1,0),(-1,0):(0,-1),(0,-1):(1,0)}[(dr,dc)]
            nr,nc=r+dr,c+dc
        r,c=nr,nc
    return out
sp=spiral(n)
bits=''.join(bit[r][c] for r,c in sp)
doc=open(sys.argv[1]).read()
blocks=re.findall(r'```[a-z]*\n(.*?)```',doc,re.S)
sb=''.join([b for b in blocks if b.startswith('0110011101110011')][0].split('\n'))
chk('spiral of bit grid == dossier bit string',bits==sb)
cnt=Counter(''.join(cell))
chk('cell counts K86 W85 B15 Y9 F1',(cnt['K'],cnt['W'],cnt['B'],cnt['Y'],cnt['F'])==(86,85,15,9,1),cnt)
chk('101 set cells',cnt['K']+cnt['B']==101)
cols=[cell[r][c] for r,c in sp]
seq=' '.join(x for x in cols if x in 'BY')
chk('colour sequence',seq=='B B B B Y B B B Y Y B B B B Y B B Y Y B Y Y B Y',seq)
chk('coloured spiral positions = 7 mod 8',all(i%8==7 for i,x in enumerate(cols) if x in 'BY'))
fi=cols.index('F')
chk('F at spiral 163, grid (7,4)',fi==163 and sp[163]==(7,4),(fi,sp[fi]))
chk('F row-major 1-based 103',7*14+4+1==103)
nb=[(7+dr,4+dc) for dr in(-1,0,1) for dc in(-1,0,1) if (dr,dc)!=(0,0)]
dark=sum(cell[r][c] in 'KB' for r,c in nb)
chk('6 of 8 neighbours dark',dark==6,dark)
# spliced program
prog=''.join(x for x in cols if x in 'BYF')
chk('spliced program',prog=='BBBBYBBBYYBBBBYBBYYBFYYBY',prog)
chk('F is 21st symbol',prog.index('F')==20)
# 14 spiral positions giving the same program (152..158,160..166): shifting F position keeps program
ok=[]
for p in range(len(sp)):
    if cols[p]=='F' or cols[p] in 'BY': continue
    # place F at p, others as-is: program with F inserted at p among coloured
    cc=[x if x in 'BY' else '.' for x in cols]; cc[p]='F'
    pr=''.join(x for x in cc if x!='.')
    if pr==prog: ok.append(p)
print('positions giving same program:',ok+[163], len(ok)+1)
def isprime(k): return k>1 and all(k%p for p in range(2,int(k**.5)+1))
fp=[p for p in ok+[163] if isprime(p)]
print('prime (0-based spiral) among them:',fp)
# rabbit centre 2x2 rows 6-7 cols 6-7 are spiral 192..195
cen=[sp.index((r,c)) for r in(6,7) for c in(6,7)]
chk('centre 2x2 = spiral 192..195',sorted(cen)==[192,193,194,195],sorted(cen))
chk('centre four bits 0000',bits[192:]=='0000')
print('--- diffs')
diff=[i for i in range(196) if bits[i]!=sb[i]]
print('bit diffs at spiral idx',diff,[sp[i] for i in diff],[cell[sp[i][0]][sp[i][1]] for i in diff])
eq=[]
for p in range(196):
    if cols[p] in 'BYF': continue
    cc=[x if x in 'BY' else '.' for x in cols]; cc[p]='B'
    pr=''.join(x for x in cc if x!='.')
    if pr==prog.replace('F','B'): eq.append(p)
print('positions equivalent with F as blue:',eq,len(eq)+1)

sys.exit(1 if failures else 0)
