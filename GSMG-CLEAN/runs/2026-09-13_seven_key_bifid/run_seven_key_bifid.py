"""Seven-key Bifid (BAR/CAN/FEE) -> all three locked envelopes, with matched shuffle controls (2026-09-13).

  python run_seven_key_bifid.py prepare   # builds candidates for the real DBBI and 200 shuffled controls; writes manifest.json
  python run_seven_key_bifid.py run       # refuses if candidates changed; writes results.json

Construction (astra `tools/audit_mnemonic_models.py`, community #45661): the seven contiguous 13-letter DBBI rows
are Bifid keys (I/J-merged 25-letter keyed square, whole-period decryption of all 570 FAED letters).
'successive' feeds each output into the next key; rounds 2/4/5 of the real DBBI begin BAR / CAN / FEE.

Controls: astra's conditional randomisation (seed 20260905): shuffle the 53 DBBI letters outside the first 13
and outside every prime B/BE span of the 83-token parse. Its 2,000-trial histogram is reproduced first as a
fidelity check; the first 200 shuffles are used as controls and go through the identical generator.

Already tested elsewhere (not a reason to skip, included and flagged): astra's 8 complete final outputs
(successive listed/reverse x raw/400-474-zeroed FAED x upper/lower) with sha256-hex + EVP SHA-256/MD5: 0 pad.
"""
import hashlib, json, random, sys, time
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / '2026-09-13_zero_envelopes'))
import run_zero_envelopes as Z   # shared: ENVELOPES, open_cbc, find_keys, text_score, positive controls

DATA = Z.DATA
ASTRA = Path('D:/astra/gsmg-io-5btc-puzzle')
WORDLIST = Path('D:/astra/.firecrawl/bip39-english-words-20260905.md')
DBBI = (DATA / 'DBBI_91.txt').read_text().strip().upper()
FAED = (DATA / 'FAED_570.txt').read_text().strip().upper()
FAED_Z = ''.join('A' if i in (400, 474) else c for i, c in enumerate(FAED))
ALPHA25 = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
REVERSE_RAW_SHA = '9aa4d617642f9d6ad4336dcf5f4bfafecff77933a341429330df769535abd007'
N_CONTROLS = 200


def sha(b): return hashlib.sha256(b).hexdigest()

def square(key): return ''.join(dict.fromkeys(key + ALPHA25))

def decode(text, key):
    sq = square(key)
    table = {c: divmod(i, 5) for i, c in enumerate(sq)}
    co = [v for c in text for v in table[c]]
    return ''.join(sq[5 * r + c] for r, c in zip(co[:len(text)], co[len(text):]))

def encode(text, key):
    sq = square(key)
    co = [divmod(sq.index(c), 5) for c in text]
    flat = [x[0] for x in co] + [x[1] for x in co]
    return ''.join(sq[5 * flat[i] + flat[i + 1]] for i in range(0, len(flat), 2))

def rounds(dbbi, faed, order):
    keys = [dbbi[13 * r:13 * (r + 1)] for r in range(7)]
    if order == 'reverse': keys = keys[::-1]
    out, cur = {'independent': [], 'successive': []}, faed
    for k in keys:
        out['independent'].append(decode(faed, k))
        cur = decode(cur, k); out['successive'].append(cur)
    return keys, out


# ---------------------------------------------------------------- generator (identical for real and controls) --
def materials(dbbi):
    m = {}
    def add(label, text):
        m[f'{label}/upper'] = text.upper(); m[f'{label}/lower'] = text.lower()
    keys, _ = rounds(dbbi, FAED, 'listed')
    for fname, faed in (('raw', FAED), ('z400_474', FAED_Z)):
        for order in ('listed', 'reverse'):
            _, out = rounds(dbbi, faed, order)
            for mode, outs in out.items():
                if order == 'reverse' and mode == 'independent':
                    continue  # identical set to listed independent
                for r, o in enumerate(outs, 1):
                    add(f'{fname}/{order}/{mode}/r{r}/full', o)
                    if o.startswith('BTCSEED'):
                        add(f'{fname}/{order}/{mode}/r{r}/after-BTCSEED', o[7:])
                add(f'{fname}/{order}/{mode}/concat7', ''.join(outs))
                for n in range(3, 13):
                    add(f'{fname}/{order}/{mode}/prefix{n}-concat', ''.join(o[:n] for o in outs))
                    add(f'{fname}/{order}/{mode}/prefix{n}-spaced', ' '.join(o[:n] for o in outs))
    # word forms from the successive listed raw outputs: every 3..8-letter prefix that is a BIP39 word
    _, out = rounds(dbbi, FAED, 'listed')
    words = [next((o[:n] for n in range(8, 2, -1) if o[:n] in VOCAB), None) for o in out['successive']]
    found = [w for w in words if w]
    if found:
        for sep in ('', ' ', ',', '-', '_'):
            add(f'words/found/sep{sep!r}', sep.join(found))
            add(f'words/btcseed+found/sep{sep!r}', sep.join(['BTCSEED'] + found))
            add(f'words/btc+seed+found/sep{sep!r}', sep.join(['BTC', 'SEED'] + found))
            add(f'words/seed+found/sep{sep!r}', sep.join(['SEED'] + found))
            add(f'words/found+seed/sep{sep!r}', sep.join(found + ['SEED']))
        for w in found:
            add(f'words/single/{w}', w)
    # the seven keys themselves ("seven intertwined passwords")
    for kname, ks in (('listed', keys), ('reverse', keys[::-1])):
        for sep in ('', ' ', ',', '\n'):
            add(f'keys/{kname}/join{sep!r}', sep.join(ks))
        add(f'keys/{kname}/intertwined', ''.join(k[i] for i in range(13) for k in ks))
        dig = [hashlib.sha256(k.encode()).digest() for k in ks]
        dig_l = [hashlib.sha256(k.lower().encode()).digest() for k in ks]
        for dn, dd in (('upper', dig), ('lower', dig_l)):
            m[f'keys/{kname}/sha-{dn}/concat-hex'] = ''.join(d.hex() for d in dd)
            m[f'keys/{kname}/sha-{dn}/intertwined-hex'] = ''.join(d.hex()[i] for i in range(64) for d in dd)
            x = bytes(32)
            for d in dd: x = bytes(a ^ b for a, b in zip(x, d))
            m[f'keys/{kname}/sha-{dn}/xor-hex'] = x.hex()
    return m


def eligible_positions():
    audit = json.loads((ASTRA / 'analysis/mnemonic-model-audit.json').read_text(encoding='utf-8'))
    ctl = audit['seven_key_conditional_randomization']
    return ctl['eligible_raw_positions_zero_based'], ctl['histogram_scores_0_to_6']

def shuffles(eligible, n):
    rng = random.Random(20260905)
    for _ in range(n):
        s = [DBBI[i] for i in eligible]; rng.shuffle(s)
        ch = list(DBBI)
        for i, c in zip(eligible, s): ch[i] = c
        yield ''.join(ch)

def score(dbbi):
    _, out = rounds(dbbi, FAED, 'listed')
    return sum(any(o[:n] in VOCAB for n in range(3, 9)) for o in out['successive'][1:])


VOCAB = set(w.upper() for w in WORDLIST.read_text(encoding='utf-8').split())


# ---------------------------------------------------------------- prepare -------------------------------
def prepare():
    t = time.time()
    assert len(VOCAB) == 2048 and len(DBBI) == 91 and len(FAED) == 570
    keys, out = rounds(DBBI, FAED, 'listed')
    assert keys[0] == 'DBBIBFBHCCBEG' and square(keys[0]) == 'DBIFHCEGAKLMNOPQRSTUVWXYZ'
    assert [o[:12] for o in out['successive']] == ['BTCSEEDDEOEM', 'BARSKCRNEYIW', 'EOHWRIRMDVFE', 'CANQFIVISCKT',
                                                   'FEEFPMQBGGAQ', 'IKDGCBFHNWNA', 'GTHWKMGLAKIG']
    for o, k, prev in zip(out['successive'], keys, [FAED] + out['successive'][:-1]):
        assert encode(o, k) == prev
    _, rev = rounds(DBBI, FAED, 'reverse')
    assert sha(rev['successive'][-1].encode()) == REVERSE_RAW_SHA
    assert score(DBBI) == 3
    eligible, astra_hist = eligible_positions()
    assert len(eligible) == 53
    hist = Counter(score(s) for s in shuffles(eligible, 2000))
    mine = [hist.get(i, 0) for i in range(7)]
    assert mine == astra_hist, (mine, astra_hist)
    controls = list(shuffles(eligible, N_CONTROLS))
    table = {}
    for label, text in materials(DBBI).items():
        table.setdefault(text, {'real': [], 'controls': set()})['real'].append(label)
    for ci, d in enumerate(controls):
        for label, text in materials(d).items():
            table.setdefault(text, {'real': [], 'controls': set()})['controls'].add(ci)
    rows = [{'text': k, 'real_labels': v['real'], 'controls': len(v['controls'])} for k, v in table.items()]
    (HERE / 'candidates.json').write_text(json.dumps({'controls_dbbi': controls, 'materials': rows}), encoding='utf-8')
    man = {
        'created': time.strftime('%Y-%m-%d %H:%M:%S'), 'status': 'PRE-REGISTERED, NOT YET RUN',
        'script_sha256': sha(Path(__file__).read_bytes()),
        'shared_helpers_sha256': sha((HERE.parent / '2026-09-13_zero_envelopes/run_zero_envelopes.py').read_bytes()),
        'candidates_sha256': sha((HERE / 'candidates.json').read_bytes()),
        'envelopes_sha256': {n: sha(r) for n, r in Z.ENVELOPES.items()},
        'fidelity_checks': ['7 successive prefixes BTCSEED/BAR/EOHW/CAN/FEE/IKDG/GTHW reproduced', 'Bifid round-trips',
                            'reverse-order raw sha256 9aa4d617… reproduced', f'2,000-shuffle histogram reproduced: {mine}'],
        'counts': {'controls': N_CONTROLS, 'unique_texts': len(rows),
                   'real_texts': sum(bool(r['real_labels']) for r in rows),
                   'real_only_texts': sum(bool(r['real_labels']) and r['controls'] == 0 for r in rows),
                   'control_scores_first_200': dict(Counter(score(c) for c in controls))},
        'derivations': ['sha256hex/EVP-SHA256 (proven)', 'sha256hex/EVP-MD5', 'raw/EVP-SHA256', 'raw/EVP-MD5',
                        'sha256raw/EVP-SHA256', 'sha256raw/EVP-MD5'],
        'acceptance': ['KEY MATCH (Half/Better Half) -> result; stop and report',
                       'pad>=2 or printable>=0.95 & letters>=0.65 -> inspect by hand',
                       'real-only vs control pad rates at chance -> null'],
    }
    (HERE / 'manifest.json').write_text(json.dumps(man, indent=2), encoding='utf-8')
    print(json.dumps(man, indent=2), '\nelapsed', round(time.time() - t, 1))


# ---------------------------------------------------------------- run -----------------------------------
def run():
    t0 = time.time()
    man = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))
    assert sha((HERE / 'candidates.json').read_bytes()) == man['candidates_sha256'], 'candidates changed'
    assert sha((HERE.parent / '2026-09-13_zero_envelopes/run_zero_envelopes.py').read_bytes()) == man['shared_helpers_sha256']
    # positive + detector controls (same as the ZERO run)
    import base64, re
    p3 = (DATA / 'phase3_plaintext.bin').read_bytes()
    env = base64.b64decode(re.sub(rb'\s+', b'', p3[p3.index(b'U2FsdGVk'):]))
    pw = hashlib.sha256(b'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple').hexdigest().encode()
    n, pt = Z.open_cbc(env, pw, hashlib.sha256)
    assert n == 10 and len(pt) == 2422
    Z.TARGETS['91b24bf9f5288532960ac687abb035127b1d28a5'] = 'TEST'
    hits, _ = Z.find_keys(b'xx' + (1).to_bytes(32, 'big'))
    del Z.TARGETS['91b24bf9f5288532960ac687abb035127b1d28a5']
    assert hits

    rows = json.loads((HERE / 'candidates.json').read_text(encoding='utf-8'))['materials']
    res = {'manifest_sha256': sha((HERE / 'manifest.json').read_bytes()), 'key_matches': [], 'inspect': [], 'pad_hits': []}
    tally = Counter()
    for r in rows:
        group = 'real_only' if r['real_labels'] and not r['controls'] else 'shared' if r['real_labels'] else 'control_only'
        b = r['text'].encode()
        hx, rw = hashlib.sha256(b).hexdigest().encode(), hashlib.sha256(b).digest()
        for env_name, raw in Z.ENVELOPES.items():
            for deriv, pw, md in (('sha256hex/SHA256', hx, hashlib.sha256), ('sha256hex/MD5', hx, hashlib.md5),
                                  ('raw/SHA256', b, hashlib.sha256), ('raw/MD5', b, hashlib.md5),
                                  ('sha256raw/SHA256', rw, hashlib.sha256), ('sha256raw/MD5', rw, hashlib.md5)):
                tally[(group, env_name, deriv, 'trials')] += 1
                n, pt = Z.open_cbc(raw, pw, md)
                if not n: continue
                tally[(group, env_name, deriv, 'pad')] += 1
                keyhits, shapes = Z.find_keys(pt)
                pr, lr = Z.text_score(pt)
                row = {'group': group, 'labels': r['real_labels'][:4], 'text': r['text'][:100], 'envelope': env_name,
                       'derivation': deriv, 'pad': n, 'len': len(pt), 'printable': round(pr, 3), 'letters': round(lr, 3),
                       'key_shapes': shapes, 'plaintext_hex': pt[:128].hex()}
                res['pad_hits'].append(row)
                if keyhits:
                    row['KEY'] = keyhits; res['key_matches'].append(row)
                    (HERE / 'KEY_MATCH.bin').write_bytes(pt); print('!!! KEY MATCH', row, flush=True)
                if n >= 2 or (pr >= .95 and lr >= .65):
                    res['inspect'].append(row)
    res['tallies'] = ['|'.join(k) + f'={v}' for k, v in sorted(tally.items())]
    res['elapsed_s'] = round(time.time() - t0, 1)
    (HERE / 'results.json').write_text(json.dumps(res, indent=1), encoding='utf-8')
    print(json.dumps({'key_matches': len(res['key_matches']), 'inspect': len(res['inspect']),
                      'pad_hits': len(res['pad_hits']), 'elapsed_s': res['elapsed_s']}))


if __name__ == '__main__':
    {'prepare': prepare, 'run': run}[sys.argv[1]]()
