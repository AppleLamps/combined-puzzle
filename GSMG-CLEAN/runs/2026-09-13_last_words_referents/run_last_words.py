"""Pinned referents for 'lastwordsbeforearchichoice' and the 'unforeseen hint' sum lists -> L5 gate + envelopes.

    python run_last_words.py build   # writes candidates.jsonl + manifest.json (pre-registration)
    python run_last_words.py run     # refuses if candidates/script changed; writes results.json

Not a sweep: every candidate is a suffix ("last N words"), sentence or clause of one of the pinned passages
P1..P5 (see REPORT.md), in exact source wording, or a list built from the L1/L2 prime sums.
"""
import hashlib, json, re, sys, unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import check_candidate as cc  # noqa: E402  (envelopes, try_envelope, find_keys, eq_pattern)

# The pure-python EC in check_candidate costs ~12 ms per 32-byte window (~15 s per pad-valid 1,328-byte Cosmic
# plaintext). Swap in coincurve for scalar_hits; run() checks it gives identical results to the original first.
import coincurve  # noqa: E402
_pure_scalar_hits = cc.scalar_hits


def fast_scalar_hits(k):
    if not 1 <= k < cc.N:
        return []
    pk = coincurve.PrivateKey(k.to_bytes(32, 'big')).public_key
    forms = {'uncompressed': pk.format(compressed=False), 'compressed': pk.format(compressed=True)}
    return [f'{cc.TARGETS[cc.h160(pub)]} ({form})' for form, pub in forms.items() if cc.h160(pub) in cc.TARGETS]

SM = Path(r'E:\rabbit-combined\rabbit\tools\arch_src2.md')                      # Scott Manning transcript
KD = ROOT / 'reference_texts' / 'matrix_reloaded_architect_scene_transcript.txt'  # kedri transcript
PT = ROOT / 'data' / 'architect_plaintext_readable.txt'                           # puzzle Architect text


def line(path, n):
    return path.read_text(encoding='utf-8').split('\n')[n - 1]


def body(s):
    return re.sub(r'^\*\*[^*]+:\*\*\s*|^[A-Za-z]+:\s*', '', s).strip()


def passages():
    sm105, kd52 = body(line(SM, 105)), body(line(KD, 52))
    pt = ' '.join(l.strip() for l in PT.read_text(encoding='utf-8').split('\n') if l.strip())
    cut = sm105.index('As you adequately put')
    kcut = kd52.index('As you adequately put')
    sel = pt.index(' SELECT FROM')
    P = {
        # P1: last words before Neo's door choice (_Neo walks to the door on his left_)
        'P1_sm_line105': sm105,
        'P1_kd_line52_to_stop_it': kd52[:kd52.index('stop it.') + len('stop it.')],
        'P1_kd_line52_full': kd52,
        'P1_neo_last_words': 'No!',
        # P2: words before the Architect states the choice ("As you adequately put, the problem is choice.")
        'P2_sm_before_problem_is_choice': sm105[:cut].strip(),
        'P2_kd_before_problem_is_choice': kd52[:kcut].strip(),
        'P2_sm_through_problem_is_choice': sm105[:sm105.index('choice.') + 7],
        # P3: before Neo's "Choice. The problem is choice."
        'P3_sm_architect_line61': body(line(SM, 61)),
        'P3_kd_architect_line24': body(line(KD, 24)),
        'P3_sm_neo_line59': body(line(SM, 59)),
        'P3_kd_neo_line22': body(line(KD, 22)),
        # P4: puzzle text before its choice verb SELECT
        'P4_puzzle_before_SELECT': pt[:sel].strip(),
        # P5: puzzle text end
        'P5_puzzle_full': pt.strip(),
        # after the choice (control group of already-tested ideas, kept for completeness)
        'X_sm_after_choice_109_113': ' '.join(body(line(SM, n)) for n in (109, 111, 113)),
    }
    return P


def pieces(text):
    words = text.split()
    out = [(f'suffix{n}', ' '.join(words[-n:])) for n in range(1, len(words) + 1)]
    out += [(f'sent{i}', s.strip()) for i, s in enumerate(re.split(r'(?<=[.!?:])\s+', text)) if s.strip()]
    out += [(f'clause{i}', s.strip()) for i, s in enumerate(re.split(r'[,;:.!?]\s*', text)) if s.strip()]
    return out


def sum_lists():
    d = json.loads((ROOT / 'data' / 'leads_reproduced.json').read_text())
    L1 = d['L1_color_primes']
    pairs = L1['pairs'].split()
    yl = [p[:-1] for p in pairs if p.endswith('Y')]
    bl = [p[:-1] for p in pairs if p.endswith('B')]
    vals = d['L2_prime_matrix']['values_84']
    lists = {
        'L1_yb': ['479', '484'], 'L1_by': ['484', '479'], 'L1_total': ['963'],
        'L1_yellow_primes': yl, 'L1_blue_primes': bl,
        'L1_yellow_then_blue_primes': yl + bl,
        'L2_colsums_7x12': [str(v) for v in d['L2_prime_matrix']['column_sums_7x12']],
    }
    for r, c in ((7, 12), (12, 7)):
        rows = [sum(vals[i * c + j] for j in range(c)) for i in range(r)]
        cols = [sum(vals[i * c + j] for i in range(r)) for j in range(c)]
        lists[f'L2_rowsums_{r}x{c}'] = [str(v) for v in rows]
        lists[f'L2_colsums_{r}x{c}'] = [str(v) for v in cols]
        lists[f'L2_abs_colsums_{r}x{c}'] = [str(abs(v)) for v in cols]
    out = []
    for name, L in lists.items():
        for sep_name, sep in (('none', ''), ('space', ' '), ('comma', ','), ('comma_space', ', ')):
            out.append((f'{name}/{sep_name}', sep.join(L)))
        out.append((f'{name}/pylist', '[' + ', '.join(L) + ']'))
    out += [('L1_words', 'yellow479blue484'), ('L1_words2', 'yellow 479 blue 484'), ('L1_words3', 'yellowblueprimes'),
            ('L1_privatekey', 'PRIVATEKEY'), ('L1_privatekey_l', 'privatekey'), ('L1_arch479', '479')]
    return out


def forms(s):
    variants = {s, s.replace('\u2019', "'"), s.replace("'", '\u2019')}
    out = set()
    for v in variants:
        v = unicodedata.normalize('NFC', v)
        nows = re.sub(r'\s+', '', v)
        for f in (v, v.lower(), v.upper(), nows, nows.lower(), nows.upper(),
                  re.sub(r'[^A-Za-z0-9]', '', v).lower(), re.sub(r'[^A-Za-z]', '', v).lower(),
                  re.sub(r'[^A-Za-z]', '', v).upper(), v + '\n', v.lower() + '\n'):
            if f:
                out.add(f)
    return sorted(out)


def build():
    cands = {}
    for pname, text in passages().items():
        for lab, piece in pieces(text):
            for f in forms(piece):
                cands.setdefault(f, f'{pname}/{lab}')
    for lab, piece in sum_lists():
        for f in forms(piece):
            cands.setdefault(f, f'SUM/{lab}')
    rows = [{'src': src, 'cand': c} for c, src in cands.items()]
    p = HERE / 'candidates.jsonl'
    p.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), encoding='utf-8')
    man = {'candidates_sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'n_candidates': len(rows),
           'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'sources': {str(SM): hashlib.sha256(SM.read_bytes()).hexdigest(), str(KD): hashlib.sha256(KD.read_bytes()).hexdigest(),
                       str(PT): hashlib.sha256(PT.read_bytes()).hexdigest()},
           'gate': 'L5 DBBI bg-token equality pattern on sha256/sha256d/sha256_of_hex/sha3_256 x fwd/charrev/byterev',
           'envelopes': 'terminal, salphaseion_short, cosmic_duality x profiles gsmg/raw/gsmg-md5/raw-md5; pad>=3 or key = notable'}
    (HERE / 'manifest.json').write_text(json.dumps(man, indent=1), encoding='utf-8')
    print(json.dumps(man, indent=1))


def views(b):
    d = hashlib.sha256(b).digest()
    yield 'sha256', d
    yield 'sha256d', hashlib.sha256(d).digest()
    yield 'sha256_of_hex', hashlib.sha256(d.hex().encode()).digest()
    yield 'sha3_256', hashlib.sha3_256(b).digest()


def gate_hits(b):
    hits = []
    for vname, d in views(b):
        for oname, h in (('fwd', d.hex()), ('charrev', d.hex()[::-1]), ('byterev', d[::-1].hex())):
            if cc.eq_pattern(h) == cc.DBBI_PATTERN:
                hits.append(f'{vname}/{oname}')
    return hits


def run():
    man = json.loads((HERE / 'manifest.json').read_text())
    p = HERE / 'candidates.jsonl'
    assert hashlib.sha256(p.read_bytes()).hexdigest() == man['candidates_sha256'], 'candidates changed'
    assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest() == man['script_sha256'], 'script changed'
    # self-tests: envelope code opens Phase 3.2, and gate accepts a DBBI-shaped hex / rejects a 1-nibble change
    cc.selftest()   # uses the pure-python EC
    import random
    rnd = random.Random(13)
    cc.TARGETS['91b24bf9f5288532960ac687abb035127b1d28a5'] = 'TEST k=1'
    for k in [1, 2, 3, cc.N - 1] + [rnd.randrange(1, cc.N) for _ in range(20)]:
        assert fast_scalar_hits(k) == _pure_scalar_hits(k), k
    assert fast_scalar_hits(1) == ['TEST k=1 (uncompressed)']
    del cc.TARGETS['91b24bf9f5288532960ac687abb035127b1d28a5']
    cc.scalar_hits = fast_scalar_hits
    print('coincurve scalar_hits == pure-python scalar_hits on 24 scalars (incl. planted k=1 target)', flush=True)
    sym = rnd.sample('0123456789abcdef', 16)
    good = ''.join(sym[int(c, 16)] for c in cc.DBBI_PATTERN)
    bad = good[:-1] + ('0' if good[-1] != '0' else '1')
    assert cc.eq_pattern(good) == cc.DBBI_PATTERN and cc.eq_pattern(bad) != cc.DBBI_PATTERN
    rows = [json.loads(l) for l in p.read_text(encoding='utf-8').splitlines()]
    res = {'n_candidates': len(rows), 'gate_checks': 0, 'gate_hits': [], 'envelope_trials': 0,
           'pad_hist': {}, 'notable': [], 'by_group': {}}
    for r in rows:
        c, b = r['cand'], r['cand'].encode('utf-8')
        g = r['src'].split('/')[0]
        res['by_group'][g] = res['by_group'].get(g, 0) + 1
        res['gate_checks'] += 12
        for h in gate_hits(b):
            res['gate_hits'].append({'src': r['src'], 'cand': c, 'view': h})
        for prof in cc.PROFILES:
            for ename, raw in cc.ENVELOPES.items():
                res['envelope_trials'] += 1
                pad, pt = cc.try_envelope(raw, c, prof)
                res['pad_hist'][str(pad)] = res['pad_hist'].get(str(pad), 0) + 1
                if pad:
                    keys = [(dsc, hh) for dsc, hh in cc.find_keys(pt) if hh]
                    if pad >= 3 or keys:
                        res['notable'].append({'src': r['src'], 'cand': c, 'profile': prof, 'envelope': ename,
                                               'pad': pad, 'keys': keys, 'pt80': pt[:80].hex()})
    exp1 = res['envelope_trials'] * 255 / 256 / 256
    res['pad1_expected'] = round(exp1, 1)
    (HERE / 'results.json').write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({k: v for k, v in res.items() if k != 'notable'} | {'n_notable': len(res['notable'])}, indent=1))
    for n in res['notable']:
        print('NOTABLE', n)


if __name__ == '__main__':
    {'build': build, 'run': run}[sys.argv[1]]()
