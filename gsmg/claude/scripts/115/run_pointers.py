"""Doc 115 s5: poster-family numbers as pointers into decoded texts; the letters just
before each pointer as 'last words', alone and with the label/number, screened with a
seeded planted control."""
import os, re
import harness as H, prun
from controls import planted_container
from lists import all_lists, matrices, SP

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def letters(s): return re.sub('[^a-z]', '', s.lower())

def texts():
    rd = lambda n: open(os.path.join(DATA, n), encoding='utf-8').read()
    return {'arch': rd('architect.txt'), 'checker': rd('checker.txt'), 'phase2': letters(rd('phase2.txt')),
            'intro': letters(rd('intro.txt')), 'riddle': letters(rd('riddle.txt'))}

def pointer_numbers():
    nums = set()
    for mn, M in matrices().items():
        nums.add(int(M.sum()))
        # counts and sums of spiral / row-major positions of each value class, 0- and 1-based
        for v in set(M.flatten().tolist()):
            for base in (0, 1):
                sp = [i + base for i, (r, c) in enumerate(SP) if M[r, c] == v]
                rm = [r * 14 + c + base for r in range(14) for c in range(14) if M[r, c] == v]
                nums.update([sum(sp), sum(rm), len(sp)])
    for ln, Lst in all_lists().items():
        nums.add(sum(Lst))
        if len(Lst) <= 14: nums.update(Lst)
    return sorted(n for n in nums if 3 <= n <= 1539)

def build():
    nums = pointer_numbers(); print('pointer numbers', len(nums))
    items = []; seen = set()
    for tn, T in texts().items():
        for n in nums:
            if n > len(T): continue
            for L in range(3, 41):
                if n - L < 0: break
                w = T[n - L:n]
                for c in (w, w + 'thispassword', str(n) + w, w + str(n)):
                    if c in seen: continue
                    seen.add(c); items.append((f'{tn}@{n}-{L}', c.encode()))
    return items

def main():
    items = build()
    ctl = items[len(items) // 2][1]
    extra_c = {'CONTROL': planted_container(ctl, seed=116, pt_len=70)}
    C, D, V, F = prun.run(items, tag='pointer last-words', extra_containers=extra_c)
    for f in F:
        if f[0] == 'CONTROL':
            # the planted container holds random bytes, so a wrong password can still give
            # pad >= 3 by chance (about 0.03 expected per run); only the planted answer counts
            print(('CONTROL FIRED ' if f[6] == ctl else 'chance flag on control container ') + str(f[:6]))
        else:
            print('FLAG ' + str(f[:6]))

if __name__ == '__main__':
    main()
