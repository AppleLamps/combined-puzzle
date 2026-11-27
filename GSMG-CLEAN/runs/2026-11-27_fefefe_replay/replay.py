"""Replay of the 5g-puzzle FEFEFE candidates against the three locked envelopes, pinned gsmg profile only.
Modelled on runs/2026-11-27_matrixsum_replay/replay.py.

Usage (from any directory):
    python replay.py build    # read both arms exactly, write candidates.txt + provenance.tsv
    python replay.py prereg   # write PREREG.json, then PREREG.sealed (its sha256), before any decrypt
    python replay.py run      # verify seal, controls, decrypt every candidate x envelope, find_keys, report
"""
import hashlib, json, math, string, sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
GSMG = HERE.parents[1]                      # GSMG-CLEAN/
REPO = HERE.parents[2]                      # combined-puzzle/
sys.path.insert(0, str(GSMG / 'tools'))

ARM_A_PATH = REPO / '5g-puzzle' / 'packet' / 'password_list_ybpos.json'
ARM_B_PATH = REPO / '5g-puzzle' / 'packet' / 'out' / 'results_fefefe_read.json'
ARM_A_N, ARM_B_N = 40, 72
PROFILE = 'gsmg'

PLANTED_PASSPHRASE = 'planted_control_fefefe_replay_2026_11_27'
PLANTED_PLAINTEXT = b'PLANTED CONTROL: fefefe replay 2026-11-27, gsmg profile.'   # 56 B -> pad 8
PLANTED_SALT = hashlib.sha256(b'fefefe replay planted salt').digest()[:8]
K1_HASH160 = '91b24bf9f5288532960ac687abb035127b1d28a5'    # k=1 uncompressed, 1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm
K1_WIF = '5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf'
PRINTABLE = set(bytes(string.printable, 'ascii')) - set(b'\x0b\x0c')


def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def esc(s):
    return s.replace('\\', '\\\\').replace('\t', '\\t').replace('\n', '\\n').replace('\r', '\\r')


# --- step: build -----------------------------------------------------------------------------------------
def load_arms():
    a = json.loads(ARM_A_PATH.read_text(encoding='utf-8'))['passwords']
    assert len(a) == ARM_A_N, f'arm A: expected {ARM_A_N} strings, got {len(a)}'
    assert len(set(a)) == ARM_A_N, f'arm A: expected {ARM_A_N} unique, got {len(set(a))}'
    takes = json.loads(ARM_B_PATH.read_text(encoding='utf-8'))['takes']
    assert len(takes) == ARM_B_N, f'arm B: expected {ARM_B_N} takes, got {len(takes)}'
    b = [(t['name'], t['printable']) for t in takes]
    assert all(isinstance(s, str) for _, s in b), 'arm B: non-string printable field'
    return a, b


def build():
    a, b = load_arms()
    candidates, seen, prov = [], set(), []
    for i, s in enumerate(a):
        prov.append((s, 'A', f'password_list_ybpos.json:passwords[{i}]'))
        if s not in seen:
            seen.add(s); candidates.append(s)
    b_unique = {s for _, s in b}
    b_in_a = sorted(b_unique & set(a))
    for name, s in b:
        prov.append((s, 'B', name))
        if s not in seen:
            seen.add(s); candidates.append(s)
    for s in candidates:
        assert s and '\n' not in s and '\r' not in s and s == s.strip('\n'), f'unsafe candidate {s!r}'
    (HERE / 'candidates.txt').write_bytes(''.join(c + '\n' for c in candidates).encode('utf-8'))
    with open(HERE / 'provenance.tsv', 'w', encoding='utf-8', newline='') as fh:
        fh.write('string\tarm\tsource_name\n')
        for s, arm, src in prov:
            fh.write(f'{esc(s)}\t{arm}\t{esc(src)}\n')
    counts = {
        'arm_a_strings': len(a), 'arm_a_unique': len(set(a)),
        'arm_b_takes': len(b), 'arm_b_unique_printable': len(b_unique),
        'arm_b_duplicates_within_b': len(b) - len(b_unique),
        'arm_b_unique_already_in_a': len(b_in_a), 'arm_b_new': len(b_unique - set(a)),
        'candidates_total': len(candidates),
    }
    assert counts['candidates_total'] == counts['arm_a_unique'] + counts['arm_b_new']
    print(json.dumps(counts, indent=1))
    print('arm B strings already in arm A:', b_in_a)
    return counts, b_in_a


# --- step: prereg ----------------------------------------------------------------------------------------
def prereg():
    import check_candidate as cc
    assert not (HERE / 'PREREG.json').exists(), 'PREREG.json already exists; a changed plan is a new run'
    assert not (HERE / 'outputs').exists() and not (HERE / 'results.json').exists(), 'decrypt output already present'
    counts, b_in_a = build_counts()
    statement = {
        'run': 'runs/2026-11-27_fefefe_replay',
        'hypothesis': 'One of the FEFEFE candidates (5g-puzzle arm A yb-position passwords, arm B fefefe-read '
                      'printable takes) is the answer to a locked envelope under the pinned gsmg profile.',
        'inputs': {
            'arm_a': {'file': '5g-puzzle/packet/password_list_ybpos.json', 'key': 'passwords',
                      'sha256': sha256_file(ARM_A_PATH)},
            'arm_b': {'file': '5g-puzzle/packet/out/results_fefefe_read.json', 'key': 'takes[].printable',
                      'sha256': sha256_file(ARM_B_PATH)},
            'rule': 'read exactly, no additions; arm A first in file order, then arm B in file order, '
                    'first occurrence kept',
        },
        'candidates_file': 'candidates.txt',
        'candidates_sha256': sha256_file(HERE / 'candidates.txt'),
        'provenance_sha256': sha256_file(HERE / 'provenance.tsv'),
        'counts': counts,
        'arm_b_unique_already_in_a': b_in_a,
        'profile': PROFILE,
        'profile_detail': 'passphrase = lowercase sha256 hex of the candidate (UTF-8); EVP_BytesToKey SHA-256, '
                          '1 iteration; AES-256-CBC; salt = envelope bytes 8..16; strict PKCS#7',
        'envelopes': list(cc.ENVELOPES),
        'envelope_sha256': {n: hashlib.sha256(r).hexdigest() for n, r in cc.ENVELOPES.items()},
        'decrypts_planned': counts['candidates_total'] * len(cc.ENVELOPES),
        'controls': {
            'harness': 'cc.selftest() must pass, which reopens the Phase 3.2 envelope (pad 10, 2,422 B).',
            'planted_envelope': f'a Salted__ envelope built here under the gsmg profile from passphrase '
                                f'{PLANTED_PASSPHRASE!r}, salt sha256("fefefe replay planted salt")[:8], '
                                f'plaintext {PLANTED_PLAINTEXT.decode()!r} ({len(PLANTED_PLAINTEXT)} B). '
                                f'The planted string is appended to the real candidates and the whole list goes '
                                f'through the same decrypt loop against that envelope only. It must be found with '
                                f'pad >= 3 and the exact plaintext.',
            'find_keys': 'k=1 is added to cc.TARGETS temporarily, a sample holding k=1 as raw32, hex64 and WIF is '
                         'passed through the same key scan used on retained outputs, and all three readings must '
                         'hit. k=1 is then removed and cc.TARGETS must be exactly Half and Better Half.',
        },
        'retention': 'every pad-valid plaintext (pad 1..16) of every candidate x envelope is written to '
                     'outputs/ENVELOPE/N.bin, whatever the pad',
        'key_scan': 'cc.find_keys on every retained plaintext, any pad, against Half '
                    'a9553269572a317e39f0f518cb87c1a0ee1dbae4 and Better Half '
                    '4bc468447fe1b048ad030a2f9a125478eabc4ed6',
        'pass_rules': {
            'valid_run': 'harness, planted_envelope and find_keys controls all pass; otherwise the run is invalid '
                         'and reports no result',
            'hit': 'any find_keys reading on a retained plaintext that derives Half or Better Half '
                   '(compressed or uncompressed)',
            'notable': 'any real decrypt with pad >= 3 (chance ~1/16.8M per decrypt); reported and inspected, '
                       'not a hit by itself',
            'null': 'valid run, no hit, no notable; pad 1 and 2 are the chance rate (expected per envelope: '
                    'pad>=1 = N/256, pad 1 = N*255/65536)',
        },
    }
    body = (json.dumps(statement, indent=2, ensure_ascii=False) + '\n').encode('utf-8')
    (HERE / 'PREREG.json').write_bytes(body)
    record = {'prereg_sha256': hashlib.sha256(body).hexdigest(),
              'hashed': 'raw bytes of PREREG.json',
              'sealed_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
    (HERE / 'PREREG.sealed').write_bytes((json.dumps(record, indent=2) + '\n').encode('utf-8'))
    print('sealed', record)


def build_counts():
    a, b = load_arms()
    b_unique = {s for _, s in b}
    cands = (HERE / 'candidates.txt').read_text(encoding='utf-8').split('\n')[:-1]
    counts = {
        'arm_a_strings': len(a), 'arm_a_unique': len(set(a)),
        'arm_b_takes': len(b), 'arm_b_unique_printable': len(b_unique),
        'arm_b_duplicates_within_b': len(b) - len(b_unique),
        'arm_b_unique_already_in_a': len(b_unique & set(a)), 'arm_b_new': len(b_unique - set(a)),
        'candidates_total': len(cands),
    }
    assert len(set(cands)) == len(cands) == counts['arm_a_unique'] + counts['arm_b_new']
    return counts, sorted(b_unique & set(a))


# --- step: run -------------------------------------------------------------------------------------------
def verify_seal():
    body = (HERE / 'PREREG.json').read_bytes()
    rec = json.loads((HERE / 'PREREG.sealed').read_text(encoding='utf-8'))
    assert hashlib.sha256(body).hexdigest() == rec['prereg_sha256'], 'PREREG.json changed after sealing'
    st = json.loads(body)
    assert sha256_file(HERE / 'candidates.txt') == st['candidates_sha256'], 'candidates.txt changed after sealing'
    return st, rec


def printable_fraction(pt):
    return round(sum(c in PRINTABLE for c in pt) / len(pt), 4) if pt else 0.0


def make_envelope(passphrase, plaintext, salt):
    import check_candidate as cc
    from Crypto.Cipher import AES
    pw, md = cc.PROFILES[PROFILE](passphrase)
    key, iv = cc.evp(pw, salt, md)
    n = 16 - len(plaintext) % 16
    return b'Salted__' + salt + AES.new(key, AES.MODE_CBC, iv).encrypt(plaintext + bytes([n]) * n)


def decrypt_loop(candidates, envelopes, out_dir):
    """The one loop used for the planted control and the real run. Retains every pad-valid plaintext."""
    import check_candidate as cc
    pads = {e: Counter() for e in envelopes}
    retained = []
    per_env = Counter()
    for s in candidates:
        for ename, raw in envelopes.items():
            pad, pt = cc.try_envelope(raw, s, PROFILE)
            pads[ename][pad] += 1
            if pad >= 1:
                path = out_dir / ename / f'{per_env[ename]}.bin'
                per_env[ename] += 1
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(pt)
                retained.append({'candidate': s, 'envelope': ename, 'pad': pad, 'plaintext_len': len(pt),
                                 'printable_fraction': printable_fraction(pt),
                                 'plaintext_sha256': hashlib.sha256(pt).hexdigest(),
                                 'hex_64': pt[:64].hex(), 'file': path.relative_to(HERE).as_posix()})
    return pads, retained


def key_scan(pt):
    """cc.find_keys on one plaintext. Returns readings that hit, plus how many readings of each kind were checked."""
    import check_candidate as cc
    found = cc.find_keys(pt)
    kinds = Counter(d.split('@')[0] for d, _ in found)
    return {'raw32_windows_checked': max(0, len(pt) - 31),
            'hex64_readings': kinds.get('hex64', 0), 'wif_readings': kinds.get('WIF', 0),
            'base64_32_readings': kinds.get('base64', 0),
            'hits': [[d, h] for d, h in found if h]}


def run():
    import check_candidate as cc
    st, rec = verify_seal()
    assert not (HERE / 'outputs').exists(), 'outputs/ already exists'
    assert list(cc.ENVELOPES) == st['envelopes']
    candidates = (HERE / 'candidates.txt').read_text(encoding='utf-8').split('\n')[:-1]
    assert len(candidates) == st['counts']['candidates_total']
    controls = {}

    # 1. harness
    cc.selftest()
    controls['harness'] = {'passed': True, 'detail': 'cc.selftest(): Phase 3.2 envelope opens, pad 10, 2,422 B'}

    # 2. planted envelope through the same loop
    env = make_envelope(PLANTED_PASSPHRASE, PLANTED_PLAINTEXT, PLANTED_SALT)
    c_pads, c_ret = decrypt_loop(candidates + [PLANTED_PASSPHRASE], {'planted_control': env},
                                 HERE / 'controls')
    hit = [r for r in c_ret if r['candidate'] == PLANTED_PASSPHRASE]
    ok = (len(hit) == 1 and hit[0]['pad'] >= 3
          and (HERE / hit[0]['file']).read_bytes() == PLANTED_PLAINTEXT)
    controls['planted_envelope'] = {
        'passed': ok, 'envelope_hex': env.hex(), 'envelope_len': len(env),
        'decrypts': len(candidates) + 1, 'found': bool(hit), 'pad': hit[0]['pad'] if hit else None,
        'plaintext_matches': ok,
        'other_pad_valid': [{k: r[k] for k in ('candidate', 'pad')} for r in c_ret
                            if r['candidate'] != PLANTED_PASSPHRASE],
        'pad_histogram': dict(sorted(c_pads['planted_control'].items())),
    }
    assert ok, f'planted envelope control FAILED: {controls["planted_envelope"]}'
    print(f'planted envelope control ok: pad={hit[0]["pad"]}')

    # 3. find_keys planted k=1 through the same key_scan
    real_targets = dict(cc.TARGETS)
    x, y = cc._mul(1)
    assert cc.h160(b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')) == K1_HASH160
    sample = b'xxxxx' + (1).to_bytes(32, 'big') + b' ' + K1_WIF.encode() + b' ' + b'0' * 63 + b'1'
    cc.TARGETS[K1_HASH160] = 'TEST k=1'
    try:
        ks = key_scan(sample)
    finally:
        del cc.TARGETS[K1_HASH160]
    kinds = sorted({d.split('@')[0] for d, _ in ks['hits']})
    targets_restored = cc.TARGETS == real_targets and sorted(cc.TARGETS) == sorted(
        ['a9553269572a317e39f0f518cb87c1a0ee1dbae4', '4bc468447fe1b048ad030a2f9a125478eabc4ed6'])
    controls['find_keys'] = {'passed': kinds == ['WIF', 'hex64', 'raw32'] and targets_restored,
                             'kinds_hit': kinds, 'hits': ks['hits'], 'targets_restored': targets_restored}
    assert controls['find_keys']['passed'], f'find_keys control FAILED: {controls["find_keys"]}'
    print('find_keys control ok:', kinds)

    # 4. the real run
    pads, retained = decrypt_loop(candidates, cc.ENVELOPES, HERE / 'outputs')
    for r in retained:
        r['key_scan'] = key_scan((HERE / r['file']).read_bytes())
    hits = [r for r in retained if r['key_scan']['hits']]
    notable = [r for r in retained if r['pad'] >= 3]
    n = len(candidates)
    hist = {}
    for e in cc.ENVELOPES:
        hist[e] = {'decrypts': n, 'counts': dict(sorted(pads[e].items())),
                   'expected_pad_valid': round(n / 256, 3),
                   'expected_pad1': round(n * 255 / 65536, 3),
                   'expected_pad2': round(n * 255 / 256 ** 3, 5)}
    total_valid = len(retained)
    lam = n * len(cc.ENVELOPES) / 256
    p_tail = 1 - sum(math.exp(-lam) * lam ** k / math.factorial(k) for k in range(total_valid))
    results = {
        'prereg_sha256': rec['prereg_sha256'], 'sealed_utc': rec['sealed_utc'],
        'run_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'profile': PROFILE, 'candidates': n, 'envelopes': list(cc.ENVELOPES),
        'total_decrypts': n * len(cc.ENVELOPES),
        'pad_histograms': hist,
        'pad_valid_total': total_valid, 'pad_valid_expected': round(lam, 3),
        'poisson_p_at_least_observed': round(p_tail, 4),
        'pad_ge_3': notable,
        'targets_checked': cc.TARGETS,
        'find_keys_hits': hits,
        'controls': controls,
        'retained': retained,
        'verdict': 'HIT' if hits else ('NOTABLE' if notable else 'NULL'),
    }
    (HERE / 'results.json').write_text(json.dumps(results, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({k: results[k] for k in ('total_decrypts', 'pad_valid_total', 'pad_valid_expected',
                                              'poisson_p_at_least_observed', 'verdict')}, indent=1))
    for e, h in hist.items():
        print(e, h['counts'])
    for r in retained:
        print(r['envelope'], r['pad'], r['printable_fraction'], r['candidate'][:40], r['key_scan'])


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    {'build': build, 'prereg': prereg, 'run': run}.get(cmd, lambda: sys.exit('usage: replay.py build|prereg|run'))()
