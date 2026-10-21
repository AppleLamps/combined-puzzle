import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from PIL import Image
from collections import Counter
import lib

PASS=[]; FAIL=[]
def check(name, cond, detail=''):
    (PASS if cond else FAIL).append(name)
    print(('PASS ' if cond else 'FAIL '), name, ' ', detail)

im = Image.open(str(Path(lib.REPO) / 'source' / 'poster' / 'puzzle.png')).convert('RGB')
W,H = im.size
CELL=75; GRID=14
Wg = W/GRID
def cell_color(r,c):
    x0=round(c*Wg); x1=round((c+1)*Wg); y0=r*CELL; y1=(r+1)*CELL
    region = im.crop((x0,y0,x1,y1))
    return Counter(region.get_flattened_data() if hasattr(region,'get_flattened_data') else region.getdata()).most_common(1)[0][0]

colors = {(r,c): cell_color(r,c) for r in range(GRID) for c in range(GRID)}

def spiral_coords(n):
    coords=[]; top,bottom,left,right=0,n-1,0,n-1
    while top<=bottom and left<=right:
        for rr in range(top,bottom+1): coords.append((rr,left))
        for cc in range(left+1,right+1): coords.append((bottom,cc))
        for rr in range(bottom-1,top-1,-1): coords.append((rr,right))
        for cc in range(right-1,left,-1): coords.append((top,cc))
        top+=1; bottom-=1; left+=1; right-=1
    return coords

coords = spiral_coords(14)

BLUE=(63,72,204); YELLOW=(255,242,0); OFFWHITE=(254,254,254)
colored_positions_0idx = [i for i,rc in enumerate(coords) if colors[rc] in (BLUE,YELLOW)]
check('colored spiral positions all == 7 mod 8 (0-indexed)',
      all(p%8==7 for p in colored_positions_0idx), colored_positions_0idx)
check('24 colored cells', len(colored_positions_0idx)==24, len(colored_positions_0idx))

byseq = ''.join('B' if colors[coords[p]]==BLUE else 'Y' for p in colored_positions_0idx)
print('derived colour sequence (spiral order):', byseq)
check("colour sequence == BBBBYBBBYYBBBBYBBYYBYYBY", byseq=='BBBBYBBBYYBBBBYBBYYBYYBY', byseq)

offwhite_pos = [i for i,rc in enumerate(coords) if colors[rc]==OFFWHITE]
check('off-white spiral position(s)', len(offwhite_pos)==1, offwhite_pos)
check('off-white spiral index (0-based) == 163', offwhite_pos[0]==163, offwhite_pos[0])
check('off-white is inside byte 21 (21st ASCII byte, 0-based char 20, bits 160-167)',
      160 <= offwhite_pos[0] < 168, offwhite_pos[0])

# ---- dbbi walk, both models, against the REAL dbbi string ----
dbbi = open(str(Path(__file__).resolve().parent / 'out' / 'textarea.txt')).read()[0:91]
check('dbbi length 91', len(dbbi)==91, len(dbbi))

def sieve_primes(n):
    isprime=[True]*(n+1); isprime[0]=isprime[1]=False
    for i in range(2,int(n**0.5)+1):
        if isprime[i]:
            for j in range(i*i,n+1,i): isprime[j]=False
    return [i for i in range(2,n+1) if isprime[i]]

def walk(dbbi, hostseq, maxpos):
    """hostseq: list of 'B'/'Y' consumed at successive prime positions (in order).
    Returns (residue, hosts_used, chars_consumed) or None if it runs out of dbbi chars."""
    primes = sieve_primes(maxpos)
    residue = []
    hi = 0
    idx = 0  # pointer into dbbi
    for p in range(1, maxpos+1):
        if p in primes:
            if hi >= len(hostseq):
                return None
            h = hostseq[hi]; hi += 1
            need = 1 if h=='B' else 2
            chunk = dbbi[idx:idx+need]
            if len(chunk) != need or (h=='Y' and chunk!=dbbi[idx:idx+2]):
                pass
            idx += need
        else:
            if idx >= len(dbbi):
                return None
            residue.append(dbbi[idx]); idx += 1
    return ''.join(residue), hi, idx

# INSERTION model L=83: splice F as blue at position 21 of the 24-seq (0-indexed 20)
ins_seq = list(byseq)
ins_seq.insert(20, 'B')  # F treated as blue, inserted at position 21 (1-based)
ins_seq_str = ''.join(ins_seq)
check('insertion 25-symbol sequence == BBBBYBBBYYBBBBYBBYYBFYYBY (F->B)',
      ins_seq_str == 'BBBBYBBBYYBBBBYBBYYBBYYBY', ins_seq_str)
res = walk(dbbi, ins_seq_str[:23], 83)
check('insertion model L=83 consumes all 91 chars', res is not None and res[2]==91, res)
if res:
    residue83, hosts_used, consumed = res
    b_ct = ins_seq_str[:23].count('B'); y_ct = ins_seq_str[:23].count('Y')
    check('insertion model host split 15 B / 8 Y', (b_ct,y_ct)==(15,8), (b_ct,y_ct))
    check('insertion residue length 60', len(residue83)==60, len(residue83))
    dossier_ins_residue = lib.block_joined(14, sep='')
    check('insertion residue == dossier block 14', residue83==dossier_ins_residue, residue83)
    print('insertion residue:', residue83)

# REPLACEMENT model L=84: flip position 21 (1-based) of the 24-seq from Y to B
rep_seq = list(byseq)
check('position 21 (1-based) of 24-seq is Y (to be replaced)', rep_seq[20]=='Y', rep_seq[20])
rep_seq[20] = 'B'
rep_seq_str = ''.join(rep_seq)
check('replacement 24-symbol sequence == BBBBYBBBYYBBBBYBBYYBBYBY', rep_seq_str=='BBBBYBBBYYBBBBYBBYYBBYBY', rep_seq_str)
res2 = walk(dbbi, rep_seq_str[:23], 84)
check('replacement model L=84 consumes all 91 chars', res2 is not None and res2[2]==91, res2)
if res2:
    residue84, hosts_used2, consumed2 = res2
    b_ct2 = rep_seq_str[:23].count('B'); y_ct2 = rep_seq_str[:23].count('Y')
    check('replacement model host split 16 B / 7 Y', (b_ct2,y_ct2)==(16,7), (b_ct2,y_ct2))
    check('replacement residue length 61', len(residue84)==61, len(residue84))
    check('replacement residue == insertion residue + trailing e', residue84==residue83+'e' if res else False, residue84)
    print('replacement residue:', residue84)

print('\nSUMMARY:', len(PASS),'passed,', len(FAIL),'failed')
if FAIL: print('FAILURES', FAIL)
sys.exit(1 if FAIL else 0)
