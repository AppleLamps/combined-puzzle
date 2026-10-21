"""L5 back-check: every string still on disk that earlier rounds tried or discussed -> DBBI hash pattern (2026-09-13).

  python run_l5_backcheck.py prepare   # walks the sources read-only, hashes files, picks planted controls, writes manifest.json
  python run_l5_backcheck.py run       # refuses if this script changed since prepare; writes results.json

L5 (03 §2): tokenise DBBI with b and g starting 2-letter tokens -> 64 tokens / 16 codes. Its first-seen equality
pattern has exactly the shape of a hex digest. If DBBI is a letter-substituted sha256 of the answer, the answer's
digest has the same equality pattern. Chance for a random 64-hex string: 16!/16^64 ~ 2^-212. Decisive gate:
a hit is proof (for that string/form/view), a null covers exactly the strings listed in the manifest.

Strings harvested from each file (deduplicated within a file):
  JSON / JSONL / ipynb  every string value and key, numbers as text, Telegram text entity lists joined,
                        and for multi-line strings every line
  .py                   every str/bytes literal (ast); lines if it does not parse
  other text files      every line, markdown/tab/csv cells, "quoted" 'quoted' `quoted` substrings
  every string          even-length hex of 16..8192 chars is also decoded to bytes (password_hex / preimage_hex)
  reference texts       word n-grams 1..12 and sentences (GSMG-CLEAN reference_texts, readable plaintexts)
  letter streams        substrings of length 1..64 (Architect letters, checkerboard, DBBI, FAED, derived streams)
Forms per string: raw, strip, lower, upper, no-whitespace lower/upper, alnum lower, letters lower/upper, +LF, +CRLF.
Views per form: sha256, sha256(sha256), sha256(lower hexdigest), sha3_256; plus identity if the form is 64 hex.
Each digest is checked as hex, char-reversed hex and byte-reversed hex.
Offline. Reads the other workspaces; writes only inside this folder.
"""
import ast, hashlib, json, os, random, re, sys, time
from multiprocessing import Pool
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CLEAN = HERE.parents[1]
DATA = CLEAN / 'data'
SESSION_ID = 'c4866a28-ecc4-48bf-b933-1ec9dc42137f'   # this conversation's own log (still being written) is excluded

ROOTS = [
    ('rabbit-combined', r'E:\rabbit-combined', None),
    ('fresh-start', r'E:\testing-btc-p\fresh-start', None),
    ('astra', r'D:\astra', None),
    ('puzle', r'D:\puzle', None),
    ('idk-btc', r'C:\Users\lucas\Desktop\idk-btc', None),
    ('claude-logs', r'C:\Users\lucas\.claude\projects', 'claude'),
    ('codex-sessions', r'C:\Users\lucas\.codex\sessions', 'codex'),
    ('codex-archived', r'C:\Users\lucas\.codex\archived_sessions', 'codex'),
]
CLAUDE_PROJECTS = {'C--Users-lucas-Desktop-idk-btc', 'C--Users-lucas-Desktop-idk-btc-telegram-export-9-8-26',
                   'C--Users-lucas-Desktop-rabbit', 'D--5btc', 'D--rabbitv2', 'E--rabbit-combined', 'E--rabbitv4'}
CODEX_KEYWORDS = [b'gsmg', b'salphaseion', b'dbbi', b'cosmic duality', b'theseedisplanted']
SKIP_DIRS = {'photos', 'video_files', 'stickers', 'voice_messages', 'round_video_messages', 'node_modules', '.git',
             '__pycache__', 'venv', '.venv', 'site-packages', 'env', '.mypy_cache', '.pytest_cache'}
TEXT_EXT = {'.txt', '.md', '.log', '.csv', '.tsv', '.html', '.htm', '.yml', '.yaml', '.js', '.mjs', '.ts', '.sh',
            '.ps1', '.toml', '.ini', '.cfg', '.rst', '.xml'}
JSON_EXT = {'.json', '.ipynb'}
JSONL_EXT = {'.jsonl', '.ndjson'}
PY_EXT = {'.py'}
ALL_EXT = TEXT_EXT | JSON_EXT | JSONL_EXT | PY_EXT
CAP = 2048                 # max chars of a non-hex text string
HEX_CAP = 8192             # max chars of a hex string decoded to bytes
BIG_JSON = 150 * 1024 * 1024
REFERENCE_NGRAM = [CLEAN / 'reference_texts' / n for n in (
    'matrix_reloaded_architect_scene_transcript.txt', 'looking_forward_fresco_keyes_1969.txt',
    'executive_order_11110.txt', 'community_github_readme_snapshot.md', 'prize_address_dossier.txt',
    'GSMG_COMPLETE_PUZZLE_REFERENCE_2026-09-10.txt')] + [DATA / 'architect_plaintext_readable.txt']
LETTER_STREAMS = [DATA / n for n in ('architect_letters_1539.txt', 'checkerboard_vic_91.txt', 'DBBI_91.txt',
                  'FAED_570.txt', 'dbbi_minus_vic_91.txt', 'faed_bifid_570.txt', 'hill_ifindo_282.txt',
                  'salphaseion_compact_1075.txt')]
HEXD = set('0123456789abcdefABCDEF')


# ---------------------------------------------------------------- gate
def eq_pattern(h):
    first = {}
    return ''.join('0123456789abcdef'[first.setdefault(c, len(first))] if len(first) < 16 or c in first else '?'
                   for c in h)


def dbbi_pattern():
    s = (DATA / 'DBBI_91.txt').read_text().split('\n')[0]
    t, i = [], 0
    while i < len(s):
        n = 2 if s[i] in 'bg' else 1
        t.append(s[i:i + n]); i += n
    assert len(t) == 64 and len(set(t)) == 16, (len(t), len(set(t)))
    first = {}
    return ''.join('0123456789abcdef'[first.setdefault(x, len(first))] for x in t), t


def prefilter_pairs(pat):
    """First two positions j whose symbol already appeared at i < j: a digest must repeat there too."""
    seen, pairs = {}, []
    for j, c in enumerate(pat):
        if c in seen and len(pairs) < 2:
            pairs.append((seen[c], j))
        seen.setdefault(c, j)
    return pairs[0] + pairs[1]


# ---------------------------------------------------------------- harvest
QUOTED = re.compile(r'"([^"\n]{1,512})"|\'([^\'\n]{1,512})\'|`([^`\n]{1,512})`')
JSON_STR = re.compile(r'"((?:[^"\\\n]|\\.)*)"')


def emit_text(s, add):
    if len(s) <= CAP:
        add(s)
    hexcand(s, add)
    lines = s.splitlines() if ('\n' in s or '\r' in s) else [s]
    for ln in lines:
        if ln is not s and len(ln) <= CAP:
            add(ln)
            hexcand(ln, add)
        if len(ln) > 20000:
            continue
        for m in QUOTED.finditer(ln):
            q = m.group(1) or m.group(2) or m.group(3)
            if q:
                add(q); hexcand(q, add)
        if '|' in ln or '\t' in ln:
            for cell in re.split(r'\||\t', ln):
                c = cell.strip().strip('`').strip()
                if c and len(c) <= CAP:
                    add(c)


def hexcand(s, add):
    t = s.strip()
    if 16 <= len(t) <= HEX_CAP and len(t) % 2 == 0 and all(c in HEXD for c in t):
        add(bytes.fromhex(t))


def walk_json(o, add):
    stack = [o]
    while stack:
        x = stack.pop()
        if isinstance(x, str):
            emit_text(x, add)
        elif isinstance(x, bool) or x is None:
            continue
        elif isinstance(x, (int, float)):
            add(str(x))
        elif isinstance(x, list):
            stack.extend(x)
        elif isinstance(x, dict):
            for k, v in x.items():
                if len(k) <= CAP:
                    add(k)
                stack.append(v)
            t = x.get('text')
            if isinstance(t, list):   # Telegram: text as a list of plain strings and entity dicts
                emit_text(''.join(p if isinstance(p, str) else str(p.get('text', '')) for p in t), add)


def json_regex_lines(text, add):
    for ln in text.splitlines():
        for m in JSON_STR.finditer(ln):
            raw = m.group(1)
            try:
                s = json.loads('"' + raw + '"')
            except Exception:
                s = raw
            emit_text(s, add)


def harvest_file(path, add):
    ext = path.suffix.lower()
    data = path.read_bytes()
    text = data.decode('utf-8', errors='replace')
    if ext in JSON_EXT:
        if len(data) <= BIG_JSON:
            try:
                walk_json(json.loads(text), add); return 'json'
            except Exception:
                pass
        json_regex_lines(text, add); return 'json-regex'
    if ext in JSONL_EXT:
        mode = 'jsonl'
        for ln in text.splitlines():
            if not ln.strip():
                continue
            try:
                walk_json(json.loads(ln), add)
            except Exception:
                json_regex_lines(ln, add); mode = 'jsonl+regex'
        return mode
    if ext in PY_EXT:
        try:
            tree = ast.parse(text)
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant):
                    if isinstance(node.value, str):
                        emit_text(node.value, add)
                    elif isinstance(node.value, bytes):
                        if len(node.value) <= CAP:
                            add(node.value)
                    elif isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                        add(str(node.value))
            return 'py-ast'
        except Exception:
            for ln in text.splitlines():
                emit_text(ln, add)
            return 'py-lines'
    for ln in text.splitlines():
        emit_text(ln, add)
    return 'text'


def harvest_special(kind, path, add):
    text = path.read_text(encoding='utf-8', errors='replace')
    if kind == 'ngram':
        words = text.split()
        for n in range(1, 13):
            for i in range(len(words) - n + 1):
                add(' '.join(words[i:i + n]))
        for sent in re.split(r'(?<=[.!?])\s+|\n+', text):
            if sent.strip() and len(sent) <= CAP:
                add(sent)
        return 'ngram'
    s = text.split('\n')[0].strip()
    for n in range(1, 65):
        for i in range(len(s) - n + 1):
            add(s[i:i + n])
    return 'letters'


# ---------------------------------------------------------------- check
WS = re.compile(r'\s+')
NONALNUM = re.compile(r'[^0-9A-Za-z]')
NONALPHA = re.compile(r'[^A-Za-z]')


def forms(item):
    if isinstance(item, bytes):
        return [('bytes', item)]
    st = item.strip()
    nows = WS.sub('', st)
    cand = [('raw', item), ('strip', st), ('lower', st.lower()), ('upper', st.upper()),
            ('nows_lower', nows.lower()), ('nows_upper', nows.upper()), ('alnum_lower', NONALNUM.sub('', st).lower()),
            ('letters_lower', NONALPHA.sub('', st).lower()), ('letters_upper', NONALPHA.sub('', st).upper()),
            ('lf', st + '\n'), ('crlf', st + '\r\n')]
    out, seen = [], set()
    for lab, v in cand:
        if v and v not in seen:
            seen.add(v)
            out.append((lab, v.encode('utf-8', errors='surrogatepass')))
    return out


def views(b):
    d = hashlib.sha256(b).digest()
    h = d.hex()
    yield 'sha256', d
    yield 'sha256d', hashlib.sha256(d).digest()
    yield 'sha256_of_hex', hashlib.sha256(h.encode()).digest()
    yield 'sha3_256', hashlib.sha3_256(b).digest()


class Checker:
    def __init__(self, targets):
        self.targets = [(name, pat, prefilter_pairs(pat)) for name, pat in targets]
        self.hexchecks = 0
        self.dbbi_pref = 0
        self.hits = []
        self.seen_forms = set()     # identical digest inputs within one file are hashed once
        self.cur = ''               # sha256 of the current digest input (recorded with hits)

    def check_hex(self, h, meta):
        self.hexchecks += 1
        for name, pat, (a, b, c, d) in self.targets:
            if h[a] == h[b] and h[c] == h[d]:
                if name == 'DBBI':
                    self.dbbi_pref += 1
                if eq_pattern(h) == pat:
                    self.hits.append((name,) + meta + (self.cur,))

    def check_item(self, item):
        for flab, fb in forms(item):
            fk = hashlib.blake2b(fb, digest_size=8).digest()
            if fk in self.seen_forms:
                continue
            self.seen_forms.add(fk)
            self.cur = hashlib.sha256(fb).hexdigest()
            if len(fb) == 64:
                try:
                    s = fb.decode('ascii')
                except UnicodeDecodeError:
                    s = ''
                if s and all(c in HEXD for c in s):
                    s = s.lower()
                    self.check_hex(s, (flab, 'identity', 'fwd'))
                    self.check_hex(s[::-1], (flab, 'identity', 'charrev'))
                    self.check_hex(bytes.fromhex(s)[::-1].hex(), (flab, 'identity', 'byterev'))
            for vlab, d in views(fb):
                h = d.hex()
                self.check_hex(h, (flab, vlab, 'fwd'))
                self.check_hex(h[::-1], (flab, vlab, 'charrev'))
                self.check_hex(d[::-1].hex(), (flab, vlab, 'byterev'))


def item_key(item):
    return hashlib.blake2b((b'B' + item) if isinstance(item, bytes) else
                           (b'S' + item.encode('utf-8', errors='surrogatepass')), digest_size=8).digest()


def item_repr(item, n=300):
    if isinstance(item, bytes):
        return 'hex:' + item.hex()[:n]
    return item if len(item) <= n else item[:n] + f'...(+{len(item) - n})'


def process(job):
    """job = (kind, path, expected_sha256, targets). Returns counts, hits and any integrity problem."""
    kind, path, want, targets = job
    t0 = time.time()
    p = Path(path)
    res = {'kind': kind, 'path': path, 'error': None}
    try:
        if want:
            h = hashlib.sha256()
            with open(p, 'rb') as f:
                for chunk in iter(lambda: f.read(1 << 22), b''):
                    h.update(chunk)
            res['sha_ok'] = h.hexdigest() == want
        items = {}

        def add(x):
            k = item_key(x)
            if k not in items:
                items[k] = x
        res['mode'] = harvest_special(kind, p, add) if kind in ('ngram', 'letters') else harvest_file(p, add)
        ck = Checker(targets)
        hits = []
        for x in items.values():
            before = len(ck.hits)
            ck.check_item(x)
            for hit in ck.hits[before:]:
                hits.append({'target': hit[0], 'form': hit[1], 'view': hit[2], 'orient': hit[3], 'form_sha256': hit[4],
                             'item': item_repr(x), 'item_sha256': hashlib.sha256(
                                 x if isinstance(x, bytes) else x.encode('utf-8', 'surrogatepass')).hexdigest()})
        res.update(items=len(items), hexchecks=ck.hexchecks, dbbi_prefilter=ck.dbbi_pref, hits=hits)
    except Exception as e:
        res['error'] = f'{type(e).__name__}: {e}'
        res.update(items=0, hexchecks=0, dbbi_prefilter=0, hits=[])
    res['elapsed_s'] = round(time.time() - t0, 2)
    return res


# ---------------------------------------------------------------- source listing
def list_sources():
    files, skipped = [], {'ext': 0, 'dir': 0, 'claude_project': 0, 'codex_nokeyword': 0, 'own_session': 0}
    excl = str(HERE).lower()
    for root_name, root, filt in ROOTS:
        if not os.path.isdir(root):
            continue
        for dp, dns, fns in os.walk(root):
            keep = []
            for d in dns:
                full = os.path.join(dp, d)
                if d.lower() in SKIP_DIRS or full.lower() == excl:
                    skipped['dir'] += 1
                elif filt == 'claude' and os.path.normcase(dp) == os.path.normcase(root) and d not in CLAUDE_PROJECTS:
                    skipped['claude_project'] += 1
                else:
                    keep.append(d)
            dns[:] = keep
            for fn in fns:
                full = os.path.join(dp, fn)
                if os.path.splitext(fn)[1].lower() not in ALL_EXT:
                    skipped['ext'] += 1; continue
                if SESSION_ID in full:
                    skipped['own_session'] += 1; continue
                files.append((root_name, full, filt))
    return files, skipped


def sha_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 22), b''):
            h.update(chunk)
    return h.hexdigest()


def codex_relevant(path):
    with open(path, 'rb') as f:
        data = f.read().lower()
    return any(k in data for k in CODEX_KEYWORDS)


def _prep_one(entry):
    root_name, full, filt = entry
    try:
        if filt == 'codex' and not codex_relevant(full):
            return None
        return {'root': root_name, 'path': full, 'size': os.path.getsize(full), 'sha256': sha_file(full)}
    except Exception as e:
        return {'root': root_name, 'path': full, 'error': str(e)}


def self_test_gate(pat, tokens):
    codes = {}
    for t in tokens:
        if t not in codes:
            codes[t] = '0123456789abcdef'[len(codes)]
    rng = random.Random(1)
    perm = list('0123456789abcdef'); rng.shuffle(perm)
    synth = ''.join(perm[int(codes[t], 16)] for t in tokens)
    ck = Checker([('DBBI', pat)])
    ck.check_hex(synth, ('synthetic', '-', '-'))
    assert len(ck.hits) == 1, 'gate misses a synthetic substituted digest'
    bad = synth[:-1] + next(c for c in '0123456789abcdef' if c != synth[-1])
    ck.check_hex(bad, ('synthetic-1', '-', '-'))
    assert len(ck.hits) == 1, 'gate accepts a digest with one changed nibble'
    return synth


def prepare():
    t0 = time.time()
    pat, tokens = dbbi_pattern()
    assert pat == '01234556728966286abc61c88b48de3086dd501d5557d6bab5605233df7bbb96'
    synth = self_test_gate(pat, tokens)
    entries, skipped = list_sources()
    with Pool(12) as pool:
        rows = [r for r in pool.imap_unordered(_prep_one, entries, chunksize=8) if r]
    errors = [r for r in rows if 'error' in r]
    rows = [r for r in rows if 'error' not in r]
    skipped['codex_nokeyword'] = sum(1 for e in entries if e[2] == 'codex') - sum(1 for r in rows if r['root'].startswith('codex'))
    by_sha = {}
    for r in sorted(rows, key=lambda r: (0 if r['path'].lower().startswith(str(CLEAN).lower()) else 1, r['path'])):
        by_sha.setdefault(r['sha256'], {'path': r['path'], 'root': r['root'], 'size': r['size'], 'sha256': r['sha256'],
                                        'copies': []})['copies'].append(r['path'])
    unique = sorted(by_sha.values(), key=lambda u: u['path'])
    special = [('ngram', str(p)) for p in REFERENCE_NGRAM if p.exists()] + \
              [('letters', str(p)) for p in LETTER_STREAMS if p.exists()]

    # planted controls: a harvested string from seeded-random real files, one form/view/orientation each.
    rng = random.Random(20260913)
    pools = {}
    for u in unique:
        if 2_000 <= u['size'] <= 3_000_000:
            pools.setdefault(Path(u['path']).suffix.lower(), []).append(u)
    controls = []
    for ext in ['.json', '.py', '.md', '.txt', '.jsonl', '.csv', '.log', '.html']:
        if ext not in pools:
            continue
        u = rng.choice(pools[ext])
        items = {}
        harvest_file(Path(u['path']), lambda x: items.setdefault(item_key(x), x))
        its = sorted(items.values(), key=lambda x: item_key(x))
        its = [x for x in its if isinstance(x, bytes) or len(x.strip()) >= 3]
        if not its:
            continue
        x = rng.choice(its)
        flab, fb = rng.choice(forms(x))
        vlab, d = rng.choice(list(views(fb)))
        orient = rng.choice(['fwd', 'charrev', 'byterev'])
        h = {'fwd': d.hex(), 'charrev': d.hex()[::-1], 'byterev': d[::-1].hex()}[orient]
        controls.append({'name': f'CONTROL_{len(controls) + 1}', 'pattern': eq_pattern(h), 'file': u['path'],
                         'form_sha256': hashlib.sha256(fb).hexdigest(),
                         'item': item_repr(x), 'item_sha256': hashlib.sha256(
                             x if isinstance(x, bytes) else x.encode('utf-8', 'surrogatepass')).hexdigest(),
                         'form': flab, 'view': vlab, 'orient': orient})
    per_root = {}
    for u in unique:
        pr = per_root.setdefault(u['root'], {'files': 0, 'bytes': 0})
        pr['files'] += 1; pr['bytes'] += u['size']
    manifest = {
        'created': time.strftime('%Y-%m-%d %H:%M:%S'),
        'script_sha256': sha_file(__file__),
        'dbbi_pattern': pat,
        'chance_per_random_hex': '16!/16^64 = 2^-212.1',
        'gate_self_test_synthetic_digest': synth,
        'forms': ['raw', 'strip', 'lower', 'upper', 'nows_lower', 'nows_upper', 'alnum_lower', 'letters_lower',
                  'letters_upper', 'lf', 'crlf', 'bytes (hex-decoded)'],
        'views': ['sha256', 'sha256d', 'sha256_of_hex', 'sha3_256', 'identity (form is 64 hex)'],
        'orientations': ['fwd', 'charrev', 'byterev'],
        'roots': ROOTS, 'claude_projects_included': sorted(CLAUDE_PROJECTS),
        'codex_keywords': [k.decode() for k in CODEX_KEYWORDS], 'skip_dirs': sorted(SKIP_DIRS),
        'extensions': sorted(ALL_EXT), 'cap_chars': CAP, 'hex_cap_chars': HEX_CAP,
        'acceptance': {
            'proof': 'any DBBI target hit (exact 64-symbol equality pattern) -> stop and report first',
            'controls': 'every planted control must be recovered in its planted file with the same digest-input bytes, view and orientation',
            'health': 'DBBI prefilter pass rate ~ 1/256 of hex checks',
            'integrity': 'script sha256 must match; files whose sha256 changed since prepare are listed'},
        'skipped_counts': skipped, 'listing_errors': errors[:50], 'per_root_unique': per_root,
        'files_listed': len(rows), 'unique_files': len(unique),
        'unique_bytes': sum(u['size'] for u in unique),
        'special_jobs': special, 'controls': controls, 'files': unique,
    }
    (HERE / 'manifest.json').write_text(json.dumps(manifest, indent=1))
    print(json.dumps({'files_listed': len(rows), 'unique_files': len(unique), 'unique_MB': round(manifest['unique_bytes'] / 1e6, 1),
                      'per_root': per_root, 'controls': len(controls), 'skipped': skipped,
                      'listing_errors': len(errors), 'elapsed_s': round(time.time() - t0, 1)}, indent=1))


def run():
    t0 = time.time()
    man = json.loads((HERE / 'manifest.json').read_text())
    if sha_file(__file__) != man['script_sha256']:
        sys.exit('script changed since prepare: refusing (re-run prepare)')
    pat, tokens = dbbi_pattern()
    assert pat == man['dbbi_pattern']
    self_test_gate(pat, tokens)
    targets = [('DBBI', pat)] + [(c['name'], c['pattern']) for c in man['controls']]
    jobs = [(k, p, None, targets) for k, p in man['special_jobs']] + \
           [('file', u['path'], u['sha256'], targets) for u in sorted(man['files'], key=lambda u: -u['size'])]
    tot = {'jobs': len(jobs), 'items': 0, 'hexchecks': 0, 'dbbi_prefilter': 0}
    dbbi_hits, control_hits, errors, changed, per_root, modes = [], {}, [], [], {}, {}
    root_of = {u['path']: u['root'] for u in man['files']}
    log = open(HERE / 'run_log.txt', 'w', encoding='utf-8')
    done = 0
    with Pool(12) as pool:
        for r in pool.imap_unordered(process, jobs, chunksize=1):
            done += 1
            tot['items'] += r['items']; tot['hexchecks'] += r['hexchecks']; tot['dbbi_prefilter'] += r['dbbi_prefilter']
            root = root_of.get(r['path'], 'special:' + r['kind'])
            pr = per_root.setdefault(root, {'jobs': 0, 'items': 0, 'hexchecks': 0})
            pr['jobs'] += 1; pr['items'] += r['items']; pr['hexchecks'] += r['hexchecks']
            modes[r.get('mode', 'error')] = modes.get(r.get('mode', 'error'), 0) + 1
            if r['error']:
                errors.append({'path': r['path'], 'error': r['error']})
            if r.get('sha_ok') is False:
                changed.append(r['path'])
            for hit in r['hits']:
                hit = dict(hit, file=r['path'])
                if hit['target'] == 'DBBI':
                    dbbi_hits.append(hit)
                    print('[DBBI-PATTERN MATCH]', json.dumps(hit), file=log, flush=True)
                    print('[DBBI-PATTERN MATCH]', json.dumps(hit), flush=True)
                else:
                    control_hits.setdefault(hit['target'], []).append(hit)
            if done % 200 == 0 or r['elapsed_s'] > 30:
                msg = f"{done}/{len(jobs)} items={tot['items']:,} hex={tot['hexchecks']:,} dbbi_hits={len(dbbi_hits)} " \
                      f"last={r['path']} ({r['elapsed_s']}s) t={time.time() - t0:.0f}s"
                print(msg, file=log, flush=True); print(msg, flush=True)
    recovered = {}
    for c in man['controls']:
        hs = control_hits.get(c['name'], [])
        recovered[c['name']] = {
            'planted_found': any(h['file'] == c['file'] and h['form_sha256'] == c['form_sha256']
                                 and h['view'] == c['view'] and h['orient'] == c['orient'] for h in hs),
            'total_hits': len(hs),
            'hits_with_other_bytes': sum(1 for h in hs if h['form_sha256'] != c['form_sha256'])}
    expected_pref = tot['hexchecks'] / 256
    results = {
        'dbbi_hits': dbbi_hits, 'totals': tot,
        'dbbi_prefilter_expected': round(expected_pref, 1),
        'dbbi_prefilter_ratio': round(tot['dbbi_prefilter'] / expected_pref, 4) if expected_pref else None,
        'controls': recovered, 'control_hit_samples': {k: v[:20] for k, v in control_hits.items()},
        'changed_since_prepare': changed, 'errors': errors, 'per_root': per_root, 'harvest_modes': modes,
        'elapsed_s': round(time.time() - t0, 1)}
    (HERE / 'results.json').write_text(json.dumps(results, indent=1))
    summary = {'dbbi_hits': len(dbbi_hits), 'items': tot['items'], 'hexchecks': tot['hexchecks'],
               'prefilter_ratio': results['dbbi_prefilter_ratio'],
               'controls_recovered': sum(v['planted_found'] for v in recovered.values()), 'controls': len(recovered),
               'changed': len(changed), 'errors': len(errors), 'elapsed_s': results['elapsed_s']}
    print(json.dumps(summary), file=log); log.close()
    print(json.dumps(summary))


if __name__ == '__main__':
    {'prepare': prepare, 'run': run}[sys.argv[1]]()
