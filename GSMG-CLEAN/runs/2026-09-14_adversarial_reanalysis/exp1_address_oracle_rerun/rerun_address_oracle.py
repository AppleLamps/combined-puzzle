"""Experiment 1 (v2: first run voided by its own controls because a deduplicated scalar was not re-reported; fixed): correct hash160 oracle over the seven retained candidate sets (see SPEC.md).

The membership test is against a SET OF HASH160 HEX STRINGS. Controls are planted into copies of the
real corpus files and scanned by the very same function as the real corpora.
No AES, no envelope bytes, no network.
"""
import base64, hashlib, json, re, shutil, sys, time
from pathlib import Path
from coincurve import PrivateKey

ROOT = Path('E:/rabbit-combined/GSMG-CLEAN')
HERE = Path(__file__).resolve().parent
RUNS = ROOT / 'runs'
SOURCES = [
    (RUNS / '2026-09-14_m4_zeroing_oracles/candidates.jsonl', 'candidate'),
    (RUNS / '2026-09-14_pointer_selectors/candidates.jsonl', 'candidate'),
    (RUNS / '2026-09-14_board_shape_sums/all_outputs.jsonl', 'output'),
    (RUNS / '2026-09-14_colour_selectors/all_outputs.jsonl', 'output'),
    (RUNS / '2026-09-14_keyed_faed/all_outputs.jsonl', 'output'),
    (RUNS / '2026-09-14_tail_cipher/all_outputs.jsonl', 'output'),
    (RUNS / '2026-09-14_matrixsum_lastwords/all_outputs.jsonl', 'output'),
]
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
sha = lambda b: hashlib.sha256(b).digest()


def b58dec_h160(a):
    n = 0
    for ch in a:
        n = n * 58 + B58.index(ch)
    raw = n.to_bytes(25, 'big')
    assert sha(sha(raw[:-4]))[:4] == raw[-4:], a
    return raw[1:21].hex()


def b58enc(raw):
    raw = raw + sha(sha(raw))[:4]
    n = int.from_bytes(raw, 'big')
    s = ''
    while n:
        s, n = B58[n % 58] + s, n // 58
    return '1' * (len(raw) - len(raw.lstrip(b'\0'))) + s


MARKERS = {'18CchrjA3Uzfrzy4DFqao9ric6YfK4hjdc': 'marker 18Cchrj (sha256 of 149 digits)',
           '1AD2wfwXukZ1kUAy848hTQQ72aSBZPB75r': 'marker 1AD2wf (sha256 of phase-1 answer)',
           '13HGhjkmKUkP8sk9k63BLmhkxRjy7uK4Rp': 'marker 13HGhjk (bit-reversed URL integer)',
           '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe': 'PRIZE Half',
           '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa': 'PRIZE Better Half'}
TARGET_H160 = {b58dec_h160(a): lab for a, lab in MARKERS.items()}   # keys ARE hash160 hex
assert all(len(k) == 40 for k in TARGET_H160)
MARKER_PREFIX = '1GyT5W'


def h160(pub):
    return hashlib.new('ripemd160', sha(pub)).hexdigest()


def oracle(k):
    """Return list of (label, pubkey_form, address) for scalar k, or []"""
    if not 1 <= k < N:
        return []
    pk = PrivateKey(k.to_bytes(32, 'big')).public_key
    out = []
    for comp in (True, False):
        hh = h160(pk.format(compressed=comp))
        form = 'compressed' if comp else 'uncompressed'
        if hh in TARGET_H160:
            out.append((TARGET_H160[hh], form, b58enc(b'\x00' + bytes.fromhex(hh))))
        else:
            a = b58enc(b'\x00' + bytes.fromhex(hh))
            if a.startswith(MARKER_PREFIX):
                out.append((f'PREFIX {MARKER_PREFIX} (partial marker)', form, a))
    return out


def derivations(s):
    b = s.encode('utf-8')
    d = {'sha256': int.from_bytes(sha(b), 'big'),
         'sha256d': int.from_bytes(sha(sha(b)), 'big'),
         'sha3_256': int.from_bytes(hashlib.sha3_256(b).digest(), 'big'),
         'sha256_of_hexdigest': int.from_bytes(sha(hashlib.sha256(b).hexdigest().encode()), 'big')}
    if s != s.lower():
        d['sha256_lower'] = int.from_bytes(sha(s.lower().encode()), 'big')
    if re.fullmatch(r'\d{1,80}', s):
        d['raw_decimal'] = int(s)
    if len(b) == 32:
        d['raw32_be'] = int.from_bytes(b, 'big')
        d['raw32_le'] = int.from_bytes(b, 'little')
    if re.fullmatch(r'[0-9a-fA-F]{64}', s):
        d['hex64_int'] = int(s, 16)
        d['sha256_of_hexbytes'] = int.from_bytes(sha(bytes.fromhex(s)), 'big')
    if len(b) > 32:
        for i in range(len(b) - 31):
            d[f'win_be@{i}'] = int.from_bytes(b[i:i + 32], 'big')
            d[f'win_le@{i}'] = int.from_bytes(b[i:i + 32], 'little')
    return d


def scan(path, field, log):
    hits, n_rows, n_scalars, seen, hit_cache = [], 0, 0, set(), {}
    with open(path, encoding='utf-8') as f:
        for ln, line in enumerate(f, 1):
            row = json.loads(line)
            s = row.get(field)
            if not isinstance(s, str):
                continue
            n_rows += 1
            for name, k in derivations(s).items():
                if not 1 <= k < N:
                    continue
                if k in seen:
                    found = hit_cache.get(k, [])      # a repeated scalar is still reported if it hits
                else:
                    seen.add(k)
                    n_scalars += 1
                    found = oracle(k)
                    if found:
                        hit_cache[k] = found
                for lab, form, addr in found:
                    hits.append({'file': str(path), 'line': ln, 'field': field, 'candidate': s[:200],
                                 'derivation': name, 'pubkey_form': form, 'address': addr, 'target': lab,
                                 'scalar_hex': f'{k:064x}', 'family': row.get('family'), 'note': row.get('note')})
            if ln % 5000 == 0:
                log(f'  {path.name}: {ln} rows, {n_scalars} unique scalars, {len(hits)} hits')
    return {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'rows': n_rows,
            'unique_scalars': n_scalars, 'hits': hits}


def plant(src, field, outdir):
    """Copy src and append the positive and negative control rows using the file's own field name."""
    PHASE1 = 'theflowerblossomsthroughwhatseemstobeaconcretesurface'
    digits149 = (ROOT / 'data/checkerboard_vic_91.txt').read_text().splitlines()[1].strip()
    assert len(digits149) == 149 and digits149.isdigit(), len(digits149)
    url_bits = (ROOT / 'data/poster_spiral_bits.txt').read_text().splitlines()[0][:192]
    hex1 = hashlib.sha256(PHASE1.encode()).hexdigest()
    pos = [('P1 phase1 answer -> sha256 -> 1AD2wf', PHASE1, '1AD2wf'),
           ('P2 149 digits -> sha256 -> 18Cchrj', digits149, '18Cchrj'),
           ('P3 bit-reversed URL integer -> raw_decimal -> 13HGhjk', str(int(url_bits[::-1], 2)), '13HGhjk'),
           ('P4 hex64 of sha256(phase1) -> hex64_int -> 1AD2wf', hex1, '1AD2wf'),
           ('P5 prize address -> sha256 -> prefix 1GyT5W', '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe', '1GyT5W'),
           ('P6 upper-case phase1 -> sha256_lower -> 1AD2wf', PHASE1.upper(), '1AD2wf')]
    neg = [('N1 phase1 last letter changed', PHASE1[:-1] + 'x'),
           ('N2 hex64 one nibble changed', hex1[:10] + ('0' if hex1[10] != '0' else '1') + hex1[11:]),
           ('N3 149 digits one digit changed', digits149[:50] + str((int(digits149[50]) + 1) % 10) + digits149[51:])]
    dst = outdir / (src.parent.name + '__' + src.name)
    shutil.copy(src, dst)
    expect = {}
    with open(dst, 'a', encoding='utf-8') as f:
        base = sum(1 for _ in open(src, encoding='utf-8'))
        for i, (lab, s, want) in enumerate(pos, 1):
            f.write(json.dumps({field: s, 'family': 'PLANTED_POSITIVE', 'note': lab}) + '\n')
            expect[base + i] = want
        for j, (lab, s) in enumerate(neg, len(pos) + 1):
            f.write(json.dumps({field: s, 'family': 'PLANTED_NEGATIVE', 'note': lab}) + '\n')
    return dst, expect


def main():
    t0 = time.time()
    logf = open(HERE / 'run.log', 'w', encoding='utf-8')

    def log(m):
        print(m, flush=True)
        logf.write(m + '\n')
        logf.flush()

    log(f'start {time.strftime("%Y-%m-%d %H:%M:%S")}; targets(hash160)={json.dumps(TARGET_H160)}')
    # ---- controls through the production loop ----
    planted_dir = HERE / 'planted'
    planted_dir.mkdir(exist_ok=True)
    control_ok = True
    control_report = []
    for src, field in SOURCES:
        dst, expect = plant(src, field, planted_dir)
        r = scan(dst, field, log)
        got = {}
        for h in r['hits']:
            got.setdefault(h['line'], set()).add(h['address'][:len(expect.get(h['line'], 'xxxxxx'))])
        ok = set(got) == set(expect) and all(expect[ln] in got[ln] for ln in expect)
        control_ok &= ok
        control_report.append({'planted_file': str(dst), 'expected_lines': expect,
                               'hit_lines': {ln: sorted(v) for ln, v in got.items()}, 'ok': ok,
                               'rows': r['rows'], 'unique_scalars': r['unique_scalars']})
        log(f'CONTROL {dst.name}: ok={ok} expected={expect} got={ {ln: sorted(v) for ln, v in got.items()} }')
    if not control_ok:
        log('CONTROLS FAILED — run voided'); json.dump(control_report, open(HERE / 'controls.json', 'w'), indent=1)
        sys.exit(2)
    json.dump(control_report, open(HERE / 'controls.json', 'w'), indent=1)
    # ---- real corpora ----
    results, all_hits, total_rows, total_scalars = [], [], 0, 0
    for src, field in SOURCES:
        r = scan(src, field, log)
        results.append({k: v for k, v in r.items() if k != 'hits'} | {'n_hits': len(r['hits'])})
        all_hits += r['hits']
        total_rows += r['rows']; total_scalars += r['unique_scalars']
        log(f'REAL {src.parent.name}/{src.name}: rows={r["rows"]} unique_scalars={r["unique_scalars"]} hits={len(r["hits"])}')
    with open(HERE / 'hits.jsonl', 'w', encoding='utf-8') as f:
        for h in all_hits:
            f.write(json.dumps(h) + '\n')
    summary = {'date': '2026-09-14', 'spec': 'SPEC.md', 'controls_passed': control_ok,
               'files_scanned': results, 'total_rows': total_rows, 'total_unique_scalars': total_scalars,
               'total_hits': len(all_hits), 'hits': all_hits,
               'targets_hash160': TARGET_H160, 'prefix_target': MARKER_PREFIX,
               'derivations': ['sha256', 'sha256d', 'sha3_256', 'sha256_of_hexdigest', 'sha256_lower',
                               'raw_decimal', 'raw32_be/le', 'hex64_int', 'sha256_of_hexbytes',
                               'overlapping 32-byte windows be/le'],
               'seconds': round(time.time() - t0, 1), 'aes_decryptions': 0, 'envelope_bytes_read': 0,
               'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    json.dump(summary, open(HERE / 'results.json', 'w'), indent=1)
    json.dump({'inputs': {str(s): hashlib.sha256(s.read_bytes()).hexdigest() for s, _ in SOURCES},
               'code_sha256': summary['code_sha256'], 'coincurve': True}, open(HERE / 'manifest.json', 'w'), indent=1)
    log(f'DONE rows={total_rows} scalars={total_scalars} hits={len(all_hits)} in {summary["seconds"]}s')


if __name__ == '__main__':
    main()
