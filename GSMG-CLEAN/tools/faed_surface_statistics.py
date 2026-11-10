"""Surface statistics of FAED (the 570 unread letters of the SalPhaseIon page).

A measurement, not a candidate generator: it produces no passwords and reads no envelope.
It settles which model classes FAED's own letters allow, so that whole families can be
retired by argument instead of variant by variant.

  python tools/faed_surface_statistics.py        writes runs/2026-11-10_faed_surface/results.json
"""
import json
import random
import string
from collections import Counter
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAED = (ROOT / 'data' / 'FAED_570.txt').read_text().strip()
OUT = ROOT / 'runs' / '2026-11-10_faed_surface'
L = 'abcdefghi'
SEED = 20261110


def chi_blocks(s, cuts):
    parts = [s[a:b] for a, b in zip([0] + cuts, cuts + [len(s)])]
    total, n, x = Counter(s), len(s), 0.0
    for p in parts:
        c = Counter(p)
        for letter in L:
            e = total[letter] * len(p) / n
            if e:
                x += (c.get(letter, 0) - e) ** 2 / e
    return x


def chi_digram(s):
    n = len(s) - 1
    dg, c1, c2 = Counter(zip(s, s[1:])), Counter(s[:-1]), Counter(s[1:])
    return sum((dg.get((a, b), 0) - c1[a] * c2[b] / n) ** 2 / (c1[a] * c2[b] / n) for a in L for b in L if c1[a] and c2[b])


def perm_p(stat_fn, s, rnd, runs):
    observed, r, k = stat_fn(s), list(s), 0
    for _ in range(runs):
        rnd.shuffle(r)
        if stat_fn(''.join(r)) >= observed:
            k += 1
    return observed, (k + 1) / (runs + 1)


def ic(t):
    c, n = Counter(t), len(t)
    return sum(v * (v - 1) for v in c.values()) / (n * (n - 1))


def tokens(s, prefixes):
    out, i = [], 0
    while i < len(s):
        if s[i] in prefixes:
            if i + 1 >= len(s):
                return None
            out.append(s[i:i + 2])
            i += 2
        else:
            out.append(s[i])
            i += 1
    return out


def best_token_ic(s):
    best = (0.0, '')
    for k in (1, 2):
        for pre in combinations(L, k):
            t = tokens(s, pre)
            if t:
                best = max(best, (ic(t), ''.join(pre)))
    return best


def tail_first(s, ambiguous, allowed, alt=0, cap=400000):
    """Page codec read from the low end: the low k bytes of the integer depend only on its
    low 8k digits, so the choice 'this letter is really zero' can be searched exactly.
    Returns (bytes matched before the branch died, survivors, complete texts)."""
    digs = [ord(c) - 96 for c in s][::-1]
    amb = [c == ambiguous for c in s][::-1]
    front, k, pos = [0], 0, 0
    while pos < len(digs):
        end, new = min(len(digs), pos + 8), []
        for v in front:
            cand = [v]
            for p in range(pos, end):
                w = 10 ** p
                cand = [x + d * w for x in cand for d in ((digs[p], alt) if amb[p] else (digs[p],))]
            new += [x for x in cand if end == len(digs) or ((x >> (8 * k)) & 0xFF) in allowed]
        if not new:
            return k, 0, []
        front, pos, k = new[:cap], end, k + 1
    texts = []
    for v in front:
        raw = v.to_bytes((v.bit_length() + 7) // 8, 'big')
        if all(b in allowed for b in raw):
            texts.append(raw.decode('latin-1'))
    return k, len(front), texts


def main():
    rnd = random.Random(SEED)
    res = {'length': len(FAED), 'counts': dict(sorted(Counter(FAED).items()))}
    others = [v for k, v in res['counts'].items() if k != 'g']
    res['g_over_mean_of_others'] = round(res['counts']['g'] / (sum(others) / len(others)), 3)

    stat, p = perm_p(chi_digram, FAED, rnd, 4000)
    res['adjacent_letters_independent'] = {'chi2': round(stat, 1), 'permutation_p': round(p, 4)}

    res['period_ic'] = {str(k): round(sum(ic(FAED[i::k]) for i in range(k)) / k, 4) for k in range(1, 41)}
    shuffled, r = [], list(FAED)
    for _ in range(200):
        rnd.shuffle(r)
        s = ''.join(r)
        shuffled.append(max(sum(ic(s[i::k]) for i in range(k)) / k for k in range(2, 41)))
    res['period_ic_max_2_40'] = {'real': max(v for k, v in res['period_ic'].items() if k != '1'),
                                 'shuffle_max_median': round(sorted(shuffled)[100], 4),
                                 'shuffle_max_p95': round(sorted(shuffled)[190], 4)}

    real_ic, real_pre = best_token_ic(FAED)
    ctl = []
    for _ in range(200):
        rnd.shuffle(r)
        ctl.append(best_token_ic(''.join(r))[0])
    res['checkerboard_tokens'] = {'best_real_ic': round(real_ic, 4), 'prefixes': real_pre,
                                  'shuffle_median': round(sorted(ctl)[100], 4), 'shuffle_max': round(max(ctl), 4)}

    homog = {}
    for name, s, cuts in (('full_quarters', FAED, [142, 285, 427]), ('full_halves', FAED, [285]),
                          ('full_thirds', FAED, [190, 380]), ('head538_quarters', FAED[:538], [134, 269, 403]),
                          ('full_19_blocks_of_30', FAED, list(range(30, 570, 30)))):
        stat, p = perm_p(lambda t, c=cuts: chi_blocks(t, c), s, rnd, 4000)
        homog[name] = {'chi2': round(stat, 1), 'permutation_p': round(p, 5)}
    grid = [[a, b, c] for a in range(60, 400, 40) for b in range(a + 60, 480, 40) for c in range(b + 40, 550, 40)]
    stat, p = perm_p(lambda t: max(chi_blocks(t, c) for c in grid), FAED, rnd, 400)
    homog['best_of_three_free_cuts'] = {'chi2': round(stat, 1), 'permutation_p_corrected_for_cut_choice': round(p, 4),
                                        'cut_sets_searched': len(grid)}
    res['homogeneity'] = homog

    tail = FAED[-32:]
    low4 = (int(''.join(str(ord(c) - 96) for c in tail)) % 2 ** 32).to_bytes(4, 'big')
    res['tail'] = {'last_32': tail, 'letters_absent': ''.join(c for c in L if c not in tail),
                   'low_4_bytes_fixed_by_last_32_digits': low4.hex(),
                   'printable': all(32 <= b < 127 for b in low4),
                   'why': '10^32 is a multiple of 2^32, so the low four bytes of the integer depend only on the '
                          'last 32 digits; no g occurs there, so no choice of g-as-zero can change them.'}

    printable = set(range(32, 127)) | {10, 13}
    lower = set(map(ord, string.ascii_lowercase))
    control_text = b'restorethezerosbeforedecidingthatthisisnotamessage'
    planted = ''.join('g' if c == '0' else chr(96 + int(c)) for c in str(int.from_bytes(control_text, 'big')))
    k, n, texts = tail_first(planted, 'g', lower)
    merged = {'planted_control_recovered': control_text.decode() in texts, 'by_letter': {}}
    for direction, s in (('forward', FAED), ('reversed', FAED[::-1])):
        for letter in L:
            k, n, texts = tail_first(s, letter, printable)
            merged['by_letter'][f'{direction}:{letter}'] = {'bytes_before_branch_died': k if not n else None,
                                                            'survivors': n, 'complete_printable_texts': len(texts)}
    merged['complete_printable_texts_total'] = sum(v['complete_printable_texts'] for v in merged['by_letter'].values())
    res['merged_zero_as_text'] = merged

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'results.json').write_text(json.dumps(res, indent=1) + '\n', encoding='utf-8')
    show = {k: v for k, v in res.items() if k not in ('period_ic',)}
    show['merged_zero_as_text'] = {k: v for k, v in merged.items() if k != 'by_letter'}
    print(json.dumps(show, indent=1))


if __name__ == '__main__':
    main()
