"""ZERO construction -> all three locked envelopes, with matched controls (2026-09-13).

  python run_zero_envelopes.py prepare   # builds candidates + controls, writes manifest.json (pre-registration)
  python run_zero_envelopes.py run       # refuses if the candidate files differ from manifest.json; writes results.json

Arms
  A  ZERO family: materials built from DBBI 7x13 prime-row x prime-column cells coloured by a 24-label
     schedule. Observed schedule = the poster's; controls = the other 149 nine-yellow schedules that also
     spell ZERO. The same generator is applied to every schedule.
  B  fresh-start `prime_matrix_cross_stage.py` materials (5,076 byte strings), previously tried only on the
     SalPhaseIon envelope. Re-run on all three (SalPhaseIon repeat = loader control: expect 45 pad hits).
  C  astra zero-mask checkerboard strings (decode-only before): every zeroed digit input and decoded output.
  D  fresh-start `openssl_cipher_family_audit.py` 1,514 passwords x 46 cipher configs x md5/sha256 on the FULL
     96-byte Terminal envelope (its earlier run loaded 48 B).

Derivations for text materials (arms A, C): sha256-hex (proven convention), raw text, sha256-raw bytes,
each with EVP SHA-256 and MD5 -> AES-256-CBC. Arm B materials are already byte passwords: EVP SHA-256 / MD5.
Detection on every output that survives: PKCS#7 pad length, Half / Better Half key in raw32 / hex64 / WIF /
base64 windows, printable+letter ratio. pad=1 is chance (1/256). Stop rule: any key match is reported first.
Offline. Reads the other workspaces; writes only inside this folder.
"""
import base64, hashlib, itertools, json, re, sys, time
from collections import Counter
from math import comb
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CLEAN = HERE.parents[1]
DATA = CLEAN / 'data'
FRESH_TOOLS = Path('E:/testing-btc-p/fresh-start/tools')
ASTRA_ZERO = Path('D:/astra/gsmg-io-5btc-puzzle/analysis/zero-checkerboard')

from Crypto.Cipher import AES
import coincurve

ENVELOPES = {n: (DATA / f'locked_{n}.bin').read_bytes()
             for n in ('terminal_phase3_2_end', 'salphaseion_short', 'cosmic_duality')}
SALTS = {'terminal_phase3_2_end': 'b45a', 'salphaseion_short': '3ab5', 'cosmic_duality': '2d3f'}
TARGETS = {'a9553269572a317e39f0f518cb87c1a0ee1dbae4': 'HALF', '4bc468447fe1b048ad030a2f9a125478eabc4ed6': 'BETTER HALF'}
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
POSTER_LABELS = 'BBBBYBBBYYBBBBYBBYYBYYBY'


# ---------------------------------------------------------------- key detection (coincurve) ------------
def h160(b):
    return hashlib.new('ripemd160', hashlib.sha256(b).digest()).hexdigest()

def scalar_hits(k):
    if not 1 <= k < N:
        return []
    pub = coincurve.PrivateKey(k.to_bytes(32, 'big')).public_key
    return [f'{TARGETS[h]} ({form})' for form, h in
            (('compressed', h160(pub.format(True))), ('uncompressed', h160(pub.format(False)))) if h in TARGETS]

def wif_scalar(s):
    n = 0
    for ch in s:
        n = n * 58 + B58.index(ch)
    raw = n.to_bytes(len(s) * 6 // 8 + 2, 'big').lstrip(b'\0')
    body, chk = raw[:-4], raw[-4:]
    if hashlib.sha256(hashlib.sha256(body).digest()).digest()[:4] != chk or body[:1] != b'\x80':
        return None
    if len(body) == 33 or (len(body) == 34 and body[-1] == 1):
        return int.from_bytes(body[1:33], 'big')
    return None

def find_keys(pt):
    found = []
    for i in range(max(0, len(pt) - 31)):
        h = scalar_hits(int.from_bytes(pt[i:i + 32], 'big'))
        if h: found.append((f'raw32@{i}', h))
    text = pt.decode('latin1')
    for m in re.finditer(r'(?<![0-9a-fA-F])[0-9a-fA-F]{64}(?![0-9a-fA-F])', text):
        found.append((f'hex64@{m.start()}', scalar_hits(int(m.group(), 16))))
    for m in re.finditer(r'[5KL][1-9A-HJ-NP-Za-km-z]{50,51}', text):
        k = wif_scalar(m.group())
        if k is not None: found.append((f'WIF@{m.start()}', scalar_hits(k)))
    for m in re.finditer(r'[A-Za-z0-9+/]{43,}={0,2}', text):
        try: raw = base64.b64decode(m.group() + '=' * (-len(m.group()) % 4))
        except Exception: continue
        if len(raw) == 32: found.append((f'base64@{m.start()}', scalar_hits(int.from_bytes(raw, 'big'))))
    return [(d, h) for d, h in found if h], [d for d, h in found]

def text_score(pt):
    if not pt: return 0.0, 0.0
    s = pt.decode('latin1')
    return (sum(c in '\t\r\n' or ' ' <= c <= '~' for c in s) / len(s), sum(c.isalpha() for c in s) / len(s))


# ---------------------------------------------------------------- envelope ----------------------------
def evp(pw, salt, md):
    d = prev = b''
    while len(d) < 48:
        prev = md(prev + pw + salt).digest(); d += prev
    return d[:32], d[32:48]

def open_cbc(raw, pw, md):
    """Pad check from the last two blocks only; full decrypt only when padding is valid."""
    key, iv = evp(pw, raw[8:16], md)
    ct = raw[16:]
    prev = ct[-32:-16] if len(ct) > 16 else iv
    last = bytes(a ^ b for a, b in zip(AES.new(key, AES.MODE_ECB).decrypt(ct[-16:]), prev))
    n = last[-1]
    if not (1 <= n <= 16 and last[-n:] == bytes([n]) * n):
        return 0, None
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    return n, pt[:-n]


# ---------------------------------------------------------------- arm A generator ---------------------
def prime(n):
    return n >= 2 and all(n % d for d in range(2, int(n ** .5) + 1))

DBBI = (DATA / 'DBBI_91.txt').read_text().strip()
ROWS1, COLS1 = [r for r in range(1, 8) if prime(r)], [c for c in range(1, 14) if prime(c)]
SEL = [(r - 1) * 13 + (c - 1) for r in ROWS1 for c in COLS1]
A1 = lambda ch: ord(ch) - 96
A1L = lambda v: chr(65 + (v - 1) % 26)
A0L = lambda v: chr(65 + v % 26)

def zero_schedules():
    vals = [A1(DBBI[i]) for i in SEL]
    rows = [vals[i:i + 6] for i in range(0, 24, 6)]
    per_row = []
    for vs, letter in zip(rows, 'ZERO'):
        per_row.append([m for m in range(64)
                        if A1L(sum(v if m >> j & 1 else -v for j, v in enumerate(vs))) == letter])
    out = []
    for combo in itertools.product(*per_row):
        if sum(bin(m).count('1') for m in combo) == 9:
            out.append(''.join(''.join('Y' if m >> j & 1 else 'B' for j in range(6)) for m in combo))
    return sorted(out)

def list_forms(tag, values):
    f = {f'{tag}/dec': ''.join(map(str, values)), f'{tag}/csv': ','.join(map(str, values)),
         f'{tag}/space': ' '.join(map(str, values)), f'{tag}/a1': ''.join(A1L(v) for v in values),
         f'{tag}/a0': ''.join(A0L(v) for v in values)}
    f[f'{tag}/a1-lower'] = f[f'{tag}/a1'].lower(); f[f'{tag}/a0-lower'] = f[f'{tag}/a0'].lower()
    return f

def arm_a_materials(labels):
    vals = [A1(DBBI[i]) for i in SEL]
    Y = [i for i, l in zip(SEL, labels) if l == 'Y']; B = [i for i, l in zip(SEL, labels) if l == 'B']
    blue = [v for v, l in zip(vals, labels) if l == 'B']; yellow = [v for v, l in zip(vals, labels) if l == 'Y']
    rows = [(vals[i:i + 6], labels[i:i + 6]) for i in range(0, 24, 6)]
    rb = [sum(v for v, l in zip(vs, ls) if l == 'B') for vs, ls in rows]
    ry = [sum(v for v, l in zip(vs, ls) if l == 'Y') for vs, ls in rows]
    d = [y - b for y, b in zip(ry, rb)]
    m = {}
    lists = {'sel': vals, 'sel-yzero': [0 if l == 'Y' else v for v, l in zip(vals, labels)],
             'sel-bzero': [0 if l == 'B' else v for v, l in zip(vals, labels)],
             'blue': blue, 'yellow': yellow, 'blue+yellow': blue + yellow, 'yellow+blue': yellow + blue,
             'rowdiff': d, 'rowdiff-abs': [abs(x) for x in d], 'rowdiff-neg': [-x for x in d],
             'rowblue': rb, 'rowyellow': ry, 'rowblue+rowyellow': rb + ry,
             'rowpairs': [x for p in zip(rb, ry) for x in p],
             'colour-sums': [sum(blue), sum(yellow)], 'sums4': [sum(blue), sum(yellow), sum(blue) - sum(yellow), sum(vals)]}
    for name, zero in (('none', []), ('yellow', Y), ('blue', B), ('all24', SEL)):
        full = [0 if i in zero else A1(ch) for i, ch in enumerate(DBBI)]
        grid = [full[i:i + 13] for i in range(0, 91, 13)]
        lists[f'dbbi-{name}0/rowsums'] = [sum(r) for r in grid]
        lists[f'dbbi-{name}0/colsums'] = [sum(grid[r][c] for r in range(7)) for c in range(13)]
        lists[f'dbbi-{name}0/rowcolsums'] = lists[f'dbbi-{name}0/rowsums'] + lists[f'dbbi-{name}0/colsums']
        if zero:
            m[f'dbbi-{name}0/digits'] = ''.join(map(str, full))
            m[f'dbbi-{name}0/letters0'] = ''.join('0' if i in zero else ch for i, ch in enumerate(DBBI))
            m[f'dbbi-{name}0/deleted'] = ''.join(ch for i, ch in enumerate(DBBI) if i not in zero)
            m[f'dbbi-{name}0/deleted-upper'] = m[f'dbbi-{name}0/deleted'].upper()
    for name, values in lists.items():
        m.update(list_forms(name, values))
    for w in ('ZERO', 'zero', 'zeroed', 'zeroedout', 'ZEROEDOUT', 'zeroout'):
        m[f'word/{w}'] = w
    m['zero+dbbi-yellow0-deleted'] = 'zero' + m['dbbi-yellow0/deleted']
    m['dbbi-yellow0-deleted+zero'] = m['dbbi-yellow0/deleted'] + 'zero'
    return m


# ---------------------------------------------------------------- arms B, C, D sources ----------------
def arm_b_materials():
    sys.path.insert(0, str(FRESH_TOOLS))
    import prime_matrix_cross_stage as pm
    seen = []
    pm.decrypt = lambda blob, password, digest: (seen.append(password), None)[1]
    class _Sink:
        def write_text(self, *_a, **_k): pass
    pm.derived = lambda name: _Sink()
    report = pm.run()
    uniq = list(dict.fromkeys(seen))
    assert report['coverage']['unique_password_materials'] == len(uniq) == 5076, len(uniq)
    return uniq

def arm_c_materials():
    m = {}
    for p in sorted(ASTRA_ZERO.glob('*.json')):
        d = json.loads(p.read_text(encoding='utf-8'))
        for ci, comp in enumerate(d['computations']):
            m[f'{p.stem}/{ci}/zeroed_digits'] = comp['zeroed_digits']
            for out in comp['outputs']:
                m[f'{p.stem}/{ci}/{"+".join(out["boards"])}/text'] = out['text']
                m[f'{p.stem}/{ci}/{"+".join(out["boards"])}/text-upper'] = out['text'].upper()
    return m

def arm_d_setup():
    sys.path.insert(0, str(FRESH_TOOLS))
    import openssl_cipher_family_audit as oc
    from evidence_first_solver import coherent, nested
    return oc, coherent, nested


# ---------------------------------------------------------------- prepare ------------------------------
def sha(b): return hashlib.sha256(b).hexdigest()

def prepare():
    t = time.time()
    for n, raw in ENVELOPES.items():
        assert raw[:8] == b'Salted__' and raw[8:10].hex() == SALTS[n], n
    scheds = zero_schedules()
    assert len(scheds) == 150 == 150 and POSTER_LABELS in scheds and comb(24, 9) == 1307504
    obs = arm_a_materials(POSTER_LABELS)
    assert obs['rowdiff/csv'] == '-26,-21,-8,15' and obs['rowdiff/a1'] == 'ZERO' and obs['sums4/csv'] == '72,32,40,104'
    arm_a = {}  # text -> {'obs': [labels], 'ctl': {schedule: [labels]}}
    for s in scheds:
        for label, text in arm_a_materials(s).items():
            e = arm_a.setdefault(text, {'obs': [], 'ctl_schedules': set(), 'labels': set()})
            e['labels'].add(label)
            if s == POSTER_LABELS: e['obs'].append(label)
            else: e['ctl_schedules'].add(s)
    a_rows = [{'text': k, 'observed': bool(v['obs']), 'control_schedules': len(v['ctl_schedules']),
               'labels': sorted(v['labels'])[:6]} for k, v in arm_a.items()]
    arm_b = arm_b_materials()
    arm_c = arm_c_materials()
    oc, _, _ = arm_d_setup()
    arm_d = oc.password_family()
    files = {
        'arm_A_candidates.json': json.dumps({'schedules': scheds, 'materials': a_rows}, indent=0),
        'arm_B_passwords.hex': '\n'.join(p.hex() for p in arm_b) + '\n',
        'arm_C_candidates.json': json.dumps(arm_c, indent=0),
        'arm_D_passwords.hex': '\n'.join(p.hex() for p in arm_d) + '\n',
    }
    for name, content in files.items():
        (HERE / name).write_text(content, encoding='utf-8')
    manifest = {
        'created': time.strftime('%Y-%m-%d %H:%M:%S'), 'status': 'PRE-REGISTERED, NOT YET RUN',
        'script_sha256': sha(Path(__file__).read_bytes()),
        'candidate_files_sha256': {n: sha((HERE / n).read_bytes()) for n in files},
        'envelopes_sha256': {n: sha(r) for n, r in ENVELOPES.items()},
        'counts': {'zero_schedules': len(scheds), 'arm_A_unique_texts': len(a_rows),
                   'arm_A_observed_texts': sum(r['observed'] for r in a_rows),
                   'arm_A_observed_only_texts': sum(r['observed'] and r['control_schedules'] == 0 for r in a_rows),
                   'arm_B_passwords': len(arm_b), 'arm_C_texts': len(set(arm_c.values())), 'arm_D_passwords': len(arm_d)},
        'derivations_text': ['sha256hex/EVP-SHA256 (proven)', 'sha256hex/EVP-MD5', 'raw/EVP-SHA256', 'raw/EVP-MD5',
                             'sha256raw/EVP-SHA256', 'sha256raw/EVP-MD5'],
        'derivations_arm_B': ['bytes/EVP-SHA256', 'bytes/EVP-MD5'],
        'arm_D': '46 OpenSSL cipher configs x EVP md5/sha256 on the full 96-byte Terminal envelope',
        'expected_by_chance': 'CBC pad-valid ~1/256 per decrypt (mostly pad=1); pad>=3 ~1/16.7M; key match ~0',
        'acceptance': ['KEY MATCH (Half or Better Half) in any window -> result; stop and report',
                       'pad>=3 on an 80-byte envelope or pad>=2 anywhere -> inspect by hand',
                       'printable>=0.95 and letters>=0.65 on a CBC pad-valid output, or fresh-start coherent()/nested() on arm D -> inspect',
                       'Arm A: compare observed vs control pad-hit rate per derivation (binomial); an observed-only readable/key hit is the only thing that would count as signal',
                       'Arm B SalPhaseIon repeat must reproduce 45 pad hits (loader control)'],
        'elapsed_s': round(time.time() - t, 1),
    }
    (HERE / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(manifest, indent=2))


# ---------------------------------------------------------------- run ----------------------------------
def run():
    t0 = time.time()
    man = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))
    for n, h in man['candidate_files_sha256'].items():
        assert sha((HERE / n).read_bytes()) == h, f'{n} changed after pre-registration'
    for n, h in man['envelopes_sha256'].items():
        assert sha(ENVELOPES[n]) == h
    # positive control: the envelope code opens the real Phase 3.2 envelope
    p3 = (DATA / 'phase3_plaintext.bin').read_bytes()
    env = base64.b64decode(re.sub(rb'\s+', b'', p3[p3.index(b'U2FsdGVk'):]))
    pw = hashlib.sha256(b'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple').hexdigest().encode()
    pc = open_cbc(env, pw, hashlib.sha256)
    assert pc[0] == 10 and len(pc[1]) == 2422, 'positive control failed'
    # detector control with a temporary k=1 target
    TARGETS['91b24bf9f5288532960ac687abb035127b1d28a5'] = 'TEST'
    hits, _ = find_keys(b'xx' + (1).to_bytes(32, 'big') + b' 5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf')
    del TARGETS['91b24bf9f5288532960ac687abb035127b1d28a5']
    assert {d.split('@')[0] for d, _ in hits} == {'raw32', 'WIF'}, hits

    results = {'manifest_sha256': sha((HERE / 'manifest.json').read_bytes()), 'controls_passed': True,
               'key_matches': [], 'inspect': [], 'pad_hits': [], 'tallies': {}}
    tally = Counter()

    def record(arm, group, label, env, deriv, n, pt):
        tally[(arm, group, env, deriv, 'pad')] += 1
        keyhits, shapes = find_keys(pt)
        pr, lr = text_score(pt)
        row = {'arm': arm, 'group': group, 'label': label, 'envelope': env, 'derivation': deriv,
               'pad': n, 'len': len(pt), 'printable': round(pr, 3), 'letters': round(lr, 3),
               'key_shapes': shapes, 'plaintext_hex': pt.hex() if len(pt) <= 128 else pt[:128].hex() + '...'}
        results['pad_hits'].append(row)
        if keyhits:
            row['KEY'] = keyhits; results['key_matches'].append(row)
            (HERE / 'KEY_MATCH.bin').write_bytes(pt)
            print('!!! KEY MATCH', row)
        if n >= 2 or (pr >= .95 and lr >= .65):
            results['inspect'].append(row)

    def text_derivs(text):
        b = text.encode()
        hx, rw = hashlib.sha256(b).hexdigest().encode(), hashlib.sha256(b).digest()
        return (('sha256hex/SHA256', hx, hashlib.sha256), ('sha256hex/MD5', hx, hashlib.md5),
                ('raw/SHA256', b, hashlib.sha256), ('raw/MD5', b, hashlib.md5),
                ('sha256raw/SHA256', rw, hashlib.sha256), ('sha256raw/MD5', rw, hashlib.md5))

    # arm A
    a = json.loads((HERE / 'arm_A_candidates.json').read_text(encoding='utf-8'))
    for r in a['materials']:
        group = 'observed_only' if r['observed'] and not r['control_schedules'] else \
                'shared' if r['observed'] else 'control_only'
        for env, raw in ENVELOPES.items():
            for deriv, pw, md in text_derivs(r['text']):
                tally[('A', group, env, deriv, 'trials')] += 1
                n, pt = open_cbc(raw, pw, md)
                if n: record('A', group, r['text'][:120], env, deriv, n, pt)
    print('arm A done', round(time.time() - t0), 's', flush=True)
    # arm B
    for line in (HERE / 'arm_B_passwords.hex').read_text().split():
        pw = bytes.fromhex(line)
        for env, raw in ENVELOPES.items():
            for deriv, md in (('bytes/SHA256', hashlib.sha256), ('bytes/MD5', hashlib.md5)):
                tally[('B', 'all', env, deriv, 'trials')] += 1
                n, pt = open_cbc(raw, pw, md)
                if n: record('B', 'all', line[:120], env, deriv, n, pt)
    print('arm B done', round(time.time() - t0), 's', flush=True)
    # arm C
    c = json.loads((HERE / 'arm_C_candidates.json').read_text(encoding='utf-8'))
    for text in dict.fromkeys(c.values()):
        for env, raw in ENVELOPES.items():
            for deriv, pw, md in text_derivs(text):
                tally[('C', 'all', env, deriv, 'trials')] += 1
                n, pt = open_cbc(raw, pw, md)
                if n: record('C', 'all', text[:120], env, deriv, n, pt)
    print('arm C done', round(time.time() - t0), 's', flush=True)
    # arm D
    oc, coherent, nested = arm_d_setup()
    configs = [(al, mo, kl) for al, kls in (('aes', (16, 24, 32)), ('des', (8,)), ('3des', (16, 24)),
               ('blowfish', (16, 32)), ('cast', (16,)), ('rc2', (16, 32))) for kl in kls
               for mo in ('cbc', 'ecb', 'cfb', 'ofb')] + [('rc4', 'stream', kl) for kl in (16, 32)]
    assert len(configs) == 46
    raw = ENVELOPES['terminal_phase3_2_end']
    salt, ct = raw[8:16], raw[16:]
    for line in (HERE / 'arm_D_passwords.hex').read_text().split():
        pw = bytes.fromhex(line)
        for md in ('md5', 'sha256'):
            for al, mo, kl in configs:
                deriv = f'{al}-{mo}-{kl * 8}/{md}'
                tally[('D', 'all', 'terminal_phase3_2_end', f'{mo}', 'trials')] += 1
                pt = oc.decrypt_variant(ct, pw, salt, md, al, mo, kl)
                if pt is None: continue
                keyhits, shapes = find_keys(pt)
                coh = bool(coherent(pt)) or bool(nested(pt))
                if mo in ('cbc', 'ecb'):
                    tally[('D', 'all', 'terminal_phase3_2_end', mo, 'pad')] += 1
                if keyhits or coh or mo in ('cbc', 'ecb'):
                    pr, lr = text_score(pt)
                    row = {'arm': 'D', 'label': line[:120], 'envelope': 'terminal_phase3_2_end', 'derivation': deriv,
                           'len': len(pt), 'printable': round(pr, 3), 'letters': round(lr, 3), 'coherent_or_nested': coh,
                           'key_shapes': shapes, 'plaintext_hex': pt.hex()}
                    if keyhits:
                        row['KEY'] = keyhits; results['key_matches'].append(row)
                        (HERE / 'KEY_MATCH.bin').write_bytes(pt); print('!!! KEY MATCH', row)
                    if coh: results['inspect'].append(row)
                    if mo in ('cbc', 'ecb'): results['pad_hits'].append(row)
    print('arm D done', round(time.time() - t0), 's', flush=True)
    results['tallies'] = ['|'.join(map(str, k)) + f'={v}' for k, v in sorted(tally.items())]
    results['elapsed_s'] = round(time.time() - t0, 1)
    (HERE / 'results.json').write_text(json.dumps(results, indent=1), encoding='utf-8')
    print(json.dumps({'key_matches': len(results['key_matches']), 'inspect': len(results['inspect']),
                      'pad_hits': len(results['pad_hits']), 'elapsed_s': results['elapsed_s']}))


if __name__ == '__main__':
    {'prepare': prepare, 'run': run}[sys.argv[1]]()
