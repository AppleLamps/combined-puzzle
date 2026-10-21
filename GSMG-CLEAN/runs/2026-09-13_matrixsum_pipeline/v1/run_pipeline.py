"""#8446 read as a pipeline: yellow/blue primes -> matrix sum list -> last words before archi choice.

    python run_pipeline.py build   # writes manifest.json (pre-registration: inputs, families, counts, script hash)
    python run_pipeline.py run     # real pipeline + 400 shuffled-input controls + planted controls + L5/envelopes

Readability is judged ONLY against shuffled-input controls run through the identical pipeline (per decode family,
max score of the real run vs the max score of each control run). Every real output also goes through the L5 DBBI
gate and the 3 envelopes x 4 profiles. See REPORT.md.
"""
import hashlib, json, math, random, re, sys
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA, REF, ORIG = ROOT / 'data', ROOT / 'reference_texts', ROOT / 'originals'
sys.path.insert(0, str(ROOT / 'tools'))
import check_candidate as cc  # noqa: E402

N_CONTROLS = 400
INPUTS = {
    'poster': ORIG / 'poster' / 'puzzle.png',
    'dbbi': DATA / 'DBBI_91.txt', 'faed': DATA / 'FAED_570.txt',
    'arch_letters': DATA / 'architect_letters_1539.txt', 'arch_readable': DATA / 'architect_plaintext_readable.txt',
    'leads': DATA / 'leads_reproduced.json',
    'sm_transcript': REF / 'matrix_reloaded_architect_scene_scott_manning.md',
    'looking_forward': REF / 'looking_forward_fresco_keyes_1969.txt',
}

PRIMES = [p for p in range(2, 600) if all(p % d for d in range(2, int(p ** .5) + 1))]
P24 = PRIMES[:24]
ISPRIME = set(PRIMES)


# ---------------------------------------------------------------------------------------------- inputs
def poster_grid():
    from PIL import Image
    im = Image.open(INPUTS['poster']).convert('RGB')
    px = lambda crop: crop.get_flattened_data() if hasattr(crop, 'get_flattened_data') else crop.getdata()
    cls = {(0, 0, 0): 'K', (255, 255, 255): 'W', (63, 72, 204): 'B', (255, 242, 0): 'Y', (254, 254, 254): 'F'}
    grid = [[cls[Counter(px(im.crop((75 * c, 75 * r, min(75 * (c + 1), 1047), min(75 * (r + 1), 1047))))).most_common(1)[0][0]]
             for c in range(14)] for r in range(14)]
    return grid


def spiral14():
    order, seen, r, c, d = [], set(), 0, 0, 0
    dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))
    for _ in range(196):
        order.append((r, c)); seen.add((r, c))
        nr, nc = r + dirs[d][0], c + dirs[d][1]
        if not (0 <= nr < 14 and 0 <= nc < 14) or (nr, nc) in seen:
            d = (d + 1) % 4; nr, nc = r + dirs[d][0], c + dirs[d][1]
        r, c = nr, nc
    return order


SPIRAL = spiral14()
GRID = poster_grid()
DBBI = INPUTS['dbbi'].read_text().split('\n')[0]
FAED = INPUTS['faed'].read_text().split('\n')[0]
ARCH = INPUTS['arch_letters'].read_text().split('\n')[0]
PWORDS = re.findall(r"[A-Z']+", INPUTS['arch_readable'].read_text())
VALS84 = json.loads(INPUTS['leads'].read_text())['L2_prime_matrix']['values_84']
_sm = [re.sub(r'^\*\*[^*]+:\*\*\s*', '', l) for l in INPUTS['sm_transcript'].read_text(encoding='utf-8').split('\n') if l.startswith('**')]
SM_TEXT = ' '.join(_sm)
SM_LETTERS = re.sub(r'[^a-z]', '', SM_TEXT.lower())
SM_WORDS = re.findall(r"[a-z’']+", SM_TEXT.lower())
_lf = INPUTS['looking_forward'].read_text(encoding='utf-8', errors='replace').lower()
_lfw = re.findall(r'[a-z]+', _lf)
_wc = Counter(_lfw)
VOCAB = {w for w, n in _wc.items() if len(w) >= 3 and n >= 2} | {w for w in re.findall(r'[a-z]+', SM_TEXT.lower()) if len(w) >= 3} \
    | {w.lower() for w in PWORDS if len(w) >= 3 and w.isalpha()}
MAXW = max(len(w) for w in VOCAB)
BIGRAMS = set(zip(_lfw, _lfw[1:]))


# ---------------------------------------------------------------------------------------------- scoring
def score_letters(s):
    """max over segmentations of sum (len-2)^2 for vocabulary words (len>=3); unmatched letters score 0."""
    s = re.sub(r'[^a-z]', '', s.lower())
    n = len(s)
    best = [0] * (n + 1)
    for i in range(1, n + 1):
        b = best[i - 1]
        for L in range(3, min(MAXW, i) + 1):
            if s[i - L:i] in VOCAB:
                v = best[i - L] + (L - 2) ** 2
                if v > b:
                    b = v
        best[i] = b
    return best[n]


def score_words(ws):
    ws = [re.sub(r'[^a-z]', '', w.lower()) for w in ws]
    return sum(1 for a, b in zip(ws, ws[1:]) if (a, b) in BIGRAMS)


# ---------------------------------------------------------------------------------------------- decodes
def printable_letters(bs):
    if not bs:
        return None
    ok = sum(32 <= x < 127 for x in bs)
    return bs.decode('latin1') if ok / len(bs) >= 0.8 else None


def d_a1z26(L):
    v = [x for x in L if x != 0]
    return ''.join(chr(96 + x) for x in v) if len(v) >= 4 and all(1 <= x <= 26 for x in v) else None


def d_mod26a0(L): return ''.join(chr(97 + x % 26) for x in L)
def d_mod26a1(L): return ''.join(chr(97 + (x - 1) % 26) for x in L)
def d_ascii(L): return ''.join(map(chr, L)) if len(L) >= 4 and all(32 <= x < 127 for x in L) else None


def d_parity(L):
    if len(L) < 8:
        return None
    bits = ''.join(str(abs(x) & 1) for x in L)
    return printable_letters(bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits) - 7, 8)))


def d_decimal(L):
    digits = ''.join(str(abs(x)) for x in L).lstrip('0')
    if len(digits) < 6:
        return None
    n = int(digits)
    return printable_letters(n.to_bytes((n.bit_length() + 7) // 8, 'big'))


def d_arch0(L): return ''.join(ARCH[abs(x) % len(ARCH)] for x in L)
def d_arch1(L): return ''.join(ARCH[(abs(x) - 1) % len(ARCH)] for x in L)
def d_sm0(L): return ''.join(SM_LETTERS[abs(x) % len(SM_LETTERS)] for x in L)
def d_sm1(L): return ''.join(SM_LETTERS[(abs(x) - 1) % len(SM_LETTERS)] for x in L)
def d_pwords1(L): return [PWORDS[(abs(x) - 1) % len(PWORDS)] for x in L if x != 0]
def d_smwords1(L): return [SM_WORDS[(abs(x) - 1) % len(SM_WORDS)] for x in L if x != 0]


LETTER_DECODES = {'a1z26': d_a1z26, 'mod26a0': d_mod26a0, 'mod26a1': d_mod26a1, 'ascii': d_ascii, 'parity8': d_parity,
                  'decimal_bytes': d_decimal, 'arch_idx0': d_arch0, 'arch_idx1': d_arch1, 'sm_idx0': d_sm0, 'sm_idx1': d_sm1}
WORD_DECODES = {'puzzle_word_idx1': d_pwords1, 'sm_word_idx1': d_smwords1}


# ---------------------------------------------------------------------------------------------- matrices
def reshape(vals, r, c):
    return [vals[i * c:(i + 1) * c] for i in range(r)]


def matrices(grid, dbbi, faed, vals84):
    """-> list of (name, 2D int matrix). Colour order = coloured poster cells in spiral order (real: BBBBYBBBYYBBBBYBBYYBYYBY)."""
    M = []
    coloured = [(r, c) for r, c in SPIRAL if grid[r][c] in 'BY']
    colours = ''.join(grid[r][c] for r, c in coloured)
    pv = {rc: (P24[i], grid[rc[0]][rc[1]], i + 1) for i, rc in enumerate(coloured)}

    def pm(f):
        return [[f(pv[(r, c)]) if (r, c) in pv else 0 for c in range(14)] for r in range(14)]
    M += [('poster/Y_primes', pm(lambda t: t[0] if t[1] == 'Y' else 0)),
          ('poster/B_primes', pm(lambda t: t[0] if t[1] == 'B' else 0)),
          ('poster/all_primes', pm(lambda t: t[0])),
          ('poster/signed_B+Y-', pm(lambda t: t[0] if t[1] == 'B' else -t[0])),
          ('poster/signed_Y+B-', pm(lambda t: t[0] if t[1] == 'Y' else -t[0])),
          ('poster/Y_ordinals', pm(lambda t: t[2] if t[1] == 'Y' else 0)),
          ('poster/B_ordinals', pm(lambda t: t[2] if t[1] == 'B' else 0)),
          ('poster/all_ordinals', pm(lambda t: t[2])),
          ('poster/bits', [[1 if grid[r][c] in 'KB' else 0 for c in range(14)] for r in range(14)])]

    prime_colour = {p: colours[i] for i, p in enumerate(P24)}   # 1-based position -> 'Y'/'B' for the first 24 primes
    colour_of_prime_pos = prime_colour.get
    for tag, s, shapes in (('dbbi', dbbi, ((7, 13), (13, 7))),
                           ('faed', faed, ((19, 30), (30, 19), (15, 38), (38, 15), (10, 57), (57, 10)))):
        v = [ord(ch) - 96 for ch in s]
        pos = list(range(1, len(v) + 1))
        col = [colour_of_prime_pos(n) for n in pos]
        variants = {
            'full': v,
            'prime_pos_zeroed': [0 if n in ISPRIME else x for n, x in zip(pos, v)],
            'prime_pos_only': [x if n in ISPRIME else 0 for n, x in zip(pos, v)],
            'Y_prime_pos_only': [x if k == 'Y' else 0 for k, x in zip(col, v)],
            'B_prime_pos_only': [x if k == 'B' else 0 for k, x in zip(col, v)],
        }
        if tag == 'dbbi':
            variants.update({
                'Y_prime_pos_zeroed': [0 if k == 'Y' else x for k, x in zip(col, v)],
                'B_prime_pos_zeroed': [0 if k == 'B' else x for k, x in zip(col, v)],
                'signed_Y-B+': [-x if k == 'Y' else x for k, x in zip(col, v)],
                'signed_Y+B-': [-x if k == 'B' else x for k, x in zip(col, v)],
                'Y_prime_values': [n if k == 'Y' else 0 for k, n in zip(col, pos)],
                'B_prime_values': [n if k == 'B' else 0 for k, n in zip(col, pos)],
                'coloured_prime_values': [n if k else 0 for k, n in zip(col, pos)],
            })
        for vn, vv in variants.items():
            for r, c in shapes:
                M.append((f'{tag}/{vn}/{r}x{c}', reshape(vv, r, c)))
    for r, c in ((7, 12), (12, 7)):
        M += [(f'L2/values/{r}x{c}', reshape(vals84, r, c)),
              (f'L2/negatives_zeroed/{r}x{c}', reshape([x if x > 0 else 0 for x in vals84], r, c)),
              (f'L2/abs_negatives_only/{r}x{c}', reshape([-x if x < 0 else 0 for x in vals84], r, c))]
    return M


def sum_lists(M):
    out = []
    for name, m in M:
        rows = [sum(row) for row in m]
        cols = [sum(m[i][j] for i in range(len(m))) for j in range(len(m[0]))]
        for axis, L in (('rows', rows), ('cols', cols)):
            nz = [x for x in L if x != 0]
            cum, t = [], 0
            for x in L:
                t += x; cum.append(t)
            for vname, vv in (('fwd', L), ('rev', L[::-1]), ('nonzero', nz), ('cumsum', cum)):
                if vv:
                    out.append((f'{name}/{axis}/{vname}', vv))
    return out


def pipeline(grid, dbbi, faed, vals84, keep=False):
    lists = sum_lists(matrices(grid, dbbi, faed, vals84))
    fam_max = {k: 0 for k in list(LETTER_DECODES) + list(WORD_DECODES)}
    outs = []
    for lname, L in lists:
        for dn, f in LETTER_DECODES.items():
            t = f(L)
            if t:
                s = score_letters(t)
                fam_max[dn] = max(fam_max[dn], s)
                if keep:
                    outs.append((dn, lname, t, s))
        for dn, f in WORD_DECODES.items():
            ws = f(L)
            if ws:
                s = score_words(ws)
                fam_max[dn] = max(fam_max[dn], s)
                if keep:
                    outs.append((dn, lname, ' '.join(ws), s))
    return fam_max, outs, lists


def control(i):
    rnd = random.Random(1_000_003 + i)
    cells = [x for row in GRID for x in row]
    rnd.shuffle(cells)
    g = reshape(cells, 14, 14)
    d = list(DBBI); rnd.shuffle(d)
    f = list(FAED); rnd.shuffle(f)
    v = list(VALS84); rnd.shuffle(v)
    fm, _, _ = pipeline(g, ''.join(d), ''.join(f), v)
    return fm


# ---------------------------------------------------------------------------------------------- L5 + envelopes
import coincurve  # noqa: E402
_pure = cc.scalar_hits


def fast_scalar_hits(k):
    if not 1 <= k < cc.N:
        return []
    pk = coincurve.PrivateKey(k.to_bytes(32, 'big')).public_key
    forms = {'uncompressed': pk.format(compressed=False), 'compressed': pk.format(compressed=True)}
    return [f'{cc.TARGETS[cc.h160(pub)]} ({form})' for form, pub in forms.items() if cc.h160(pub) in cc.TARGETS]


def gate_hits(b):
    hits = []
    d = hashlib.sha256(b).digest()
    for vname, dd in (('sha256', d), ('sha256d', hashlib.sha256(d).digest()),
                      ('sha256_of_hex', hashlib.sha256(d.hex().encode()).digest()), ('sha3_256', hashlib.sha3_256(b).digest())):
        for oname, h in (('fwd', dd.hex()), ('charrev', dd.hex()[::-1]), ('byterev', dd[::-1].hex())):
            if cc.eq_pattern(h) == cc.DBBI_PATTERN:
                hits.append(f'{vname}/{oname}')
    return hits


def text_forms(t):
    nows = re.sub(r'\s+', '', t)
    letters = re.sub(r'[^A-Za-z]', '', t)
    return sorted({x for x in (t, t.lower(), t.upper(), nows, nows.lower(), nows.upper(), letters.lower(), letters.upper()) if x})


# ---------------------------------------------------------------------------------------------- build / run
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def build():
    fm, outs, lists = pipeline(GRID, DBBI, FAED, VALS84, keep=True)
    coloured = ''.join(GRID[r][c] for r, c in SPIRAL if GRID[r][c] in 'BY')
    assert coloured == 'BBBBYBBBYYBBBBYBBYYBYYBY', coloured
    assert sum(p for p, k in zip(P24, coloured) if k == 'Y') == 479
    man = {
        'script_sha256': sha(__file__), 'inputs': {k: sha(p) for k, p in INPUTS.items()},
        'n_matrices': len(matrices(GRID, DBBI, FAED, VALS84)), 'n_sum_lists': len(lists), 'n_real_outputs': len(outs),
        'decode_families': list(LETTER_DECODES) + list(WORD_DECODES),
        'n_controls': N_CONTROLS, 'control_seed': '1_000_003 + i',
        'control_model': 'poster 196 cell classes permuted (census kept; colour order and positions follow), DBBI letters permuted, FAED letters permuted, L2 values permuted; target texts fixed',
        'statistic': 'per decode family: max score over all outputs; letter families score = max segmentation sum (len-2)^2 over vocab words; word families = adjacent pairs in Looking Forward bigrams',
        'decision_rule': 'a family is SIGNAL only if its real max exceeds the max of ALL 400 controls (p <= 1/401 < 0.05/12 Bonferroni) AND its planted control also passes; otherwise null',
        'vocab_size': len(VOCAB), 'bigram_count': len(BIGRAMS),
        'also': 'every real output (8 text forms) -> L5 gate (4 views x 3 orientations) and 3 envelopes x 4 profiles',
    }
    (HERE / 'manifest.json').write_text(json.dumps(man, indent=1), encoding='utf-8')
    print(json.dumps(man, indent=1))


def planted():
    """Detection-power controls: synthetic lists that DO encode text, scored against the same control maxima."""
    phrase = 'thelastwordsbeforethechoice'
    a1 = [ord(ch) - 96 for ch in phrase]
    target = 'TAKETHEPRIVATEKEYYOUVEEARNEDIT'
    ai = ARCH.index(target)
    arch_idx = list(range(ai, ai + len(target)))
    want = 'THE FUNCTION OF THE YOU IS NOW TO RETURN TO THE SOURCE'.split()
    j = next(k for k in range(len(PWORDS)) if PWORDS[k:k + len(want)] == want)
    pw_idx = [k + 1 for k in range(j, j + len(want))]
    return {'a1z26': score_letters(d_a1z26(a1)), 'arch_idx0': score_letters(d_arch0(arch_idx)),
            'puzzle_word_idx1': score_words(d_pwords1(pw_idx)), 'mod26a1': score_letters(d_mod26a1(a1))}


def run():
    man = json.loads((HERE / 'manifest.json').read_text())
    assert sha(__file__) == man['script_sha256'], 'script changed since build'
    assert all(sha(p) == man['inputs'][k] for k, p in INPUTS.items()), 'inputs changed'
    cc.selftest()
    rnd = random.Random(13)
    cc.TARGETS['91b24bf9f5288532960ac687abb035127b1d28a5'] = 'TEST k=1'
    for k in [1, 2, 3, cc.N - 1] + [rnd.randrange(1, cc.N) for _ in range(20)]:
        assert fast_scalar_hits(k) == _pure(k), k
    del cc.TARGETS['91b24bf9f5288532960ac687abb035127b1d28a5']
    cc.scalar_hits = fast_scalar_hits
    sym = rnd.sample('0123456789abcdef', 16)
    good = ''.join(sym[int(c, 16)] for c in cc.DBBI_PATTERN)
    assert cc.eq_pattern(good) == cc.DBBI_PATTERN and cc.eq_pattern(good[:-1] + ('0' if good[-1] != '0' else '1')) != cc.DBBI_PATTERN
    print('self-tests passed (envelope open, coincurve==pure on 24 scalars, L5 gate accept/reject)', flush=True)

    fm, outs, lists = pipeline(GRID, DBBI, FAED, VALS84, keep=True)
    assert len(outs) == man['n_real_outputs'] and len(lists) == man['n_sum_lists']
    with Pool(11) as pool:
        ctrl = pool.map(control, range(N_CONTROLS), chunksize=8)
    fams = man['decode_families']
    summary = {}
    for k in fams:
        cm = sorted(c[k] for c in ctrl)
        ge = sum(1 for x in cm if x >= fm[k])
        summary[k] = {'real_max': fm[k], 'control_max': cm[-1], 'control_p50': cm[len(cm) // 2], 'control_p99': cm[int(len(cm) * .99) - 1],
                      'controls_ge_real': ge, 'p_value': round((ge + 1) / (N_CONTROLS + 1), 4)}
    pl = planted()
    for k, s in pl.items():
        summary[k]['planted_score'] = s
        summary[k]['planted_beats_all_controls'] = s > summary[k]['control_max']
    for k in fams:
        summary[k]['SIGNAL'] = fm[k] > summary[k]['control_max'] and summary[k].get('planted_beats_all_controls', None) is not False
    print(json.dumps(summary, indent=1), flush=True)

    top = {k: sorted([o for o in outs if o[0] == k], key=lambda o: -o[3])[:12] for k in fams}

    # L5 + envelopes on every real output
    seen, gate, notable, trials, pads = set(), [], [], 0, Counter()
    for dn, lname, t, s in outs:
        for f in text_forms(t):
            if f in seen:
                continue
            seen.add(f)
            for h in gate_hits(f.encode('utf-8', 'surrogatepass')):
                gate.append({'decode': dn, 'list': lname, 'form': f, 'view': h})
            for prof in cc.PROFILES:
                for ename, raw in cc.ENVELOPES.items():
                    trials += 1
                    pad, pt = cc.try_envelope(raw, f, prof)
                    pads[pad] += 1
                    if pad:
                        keys = [(d, h) for d, h in cc.find_keys(pt) if h]
                        if pad >= 3 or keys:
                            notable.append({'decode': dn, 'list': lname, 'form': f, 'profile': prof, 'envelope': ename, 'pad': pad, 'keys': keys})
    res = {'summary': summary, 'planted': pl, 'n_sum_lists': len(lists), 'n_real_outputs': len(outs),
           'l5_env': {'unique_forms': len(seen), 'gate_checks': 12 * len(seen), 'gate_hits': gate, 'envelope_trials': trials,
                      'pad_hist': dict(sorted(pads.items())), 'pad1_expected': round(trials / 256 * 255 / 256, 1), 'notable': notable},
           'top_outputs': {k: [{'list': o[1], 'text': o[2], 'score': o[3]} for o in v] for k, v in top.items()},
           'control_family_max': ctrl}
    (HERE / 'results.json').write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding='utf-8')
    (HERE / 'sum_lists.json').write_text(json.dumps(dict(lists)), encoding='utf-8')
    print(json.dumps(res['l5_env'] | {'notable': len(notable)}, indent=1))
    for k in fams:
        print('TOP', k, [(o[2][:60], o[3], o[1]) for o in top[k][:3]])


if __name__ == '__main__':
    {'build': build, 'run': run}[sys.argv[1]]()
