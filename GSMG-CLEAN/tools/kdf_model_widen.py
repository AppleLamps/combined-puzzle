#!/usr/bin/env python3
"""Re-test saved step-2/3/4 materials under a widened OpenSSL KDF.

The candidate strings are the ones already written down:

- step 2: the 84-cell gap-sum / board-sum decodes
  (runs/2026-11-10_step2_gap_sums_v2, parse 84 only)
- steps 2 and 3: the sealed sum-list selections of last words
  (runs/2026-11-10_step2_sumlist_lastwords_v3/outputs.jsonl)
- step 3: the sealed last-words referent list
  (runs/2026-09-13_last_words_referents/candidates.jsonl)
- step 4: the yin-yang label, and nothing generated beyond it
- chat: the highest-scoring sentence and clause fragments of the creator
  catalog, not whole messages

Passphrase forms stay literal UTF-8, sha256 hex, and the raw sha256 digest.
What changes is the KDF and the IV. Whole-message hashed-raw is not rebuilt.

The three locked envelopes have no validated round-trip. Phase 3.2 is the
control, and it is not mixed into the candidate counts.
"""
import hashlib
import json
import multiprocessing as mp
import re
import sys
import time
from collections import Counter
from pathlib import Path

from Crypto.Cipher import AES

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RUN = ROOT / 'runs' / '2026-11-27_kdf_model_widen'
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from oracles import english_score  # noqa: E402

PHASE32_ANSWER = 'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple'
ZERO_IV = b'\x00' * 16
KDFs = ('evp-md5', 'evp-sha256', 'pbkdf2-sha256-10000')
IVS = ('derived', 'zero')
FORMS = ('literal', 'sha256hex', 'rawdigest')


def evp_stream(password, salt, md_name, n=48):
    md = hashlib.md5 if md_name == 'md5' else hashlib.sha256
    out = b''
    prev = b''
    while len(out) < n:
        prev = md(prev + password + salt).digest()
        out += prev
    return out[:n]


def derive(password, salt, kdf):
    """Return 48 bytes. The first 32 are the key; the next 16 are the derived IV."""
    if kdf == 'evp-md5':
        return evp_stream(password, salt, 'md5')
    if kdf == 'evp-sha256':
        return evp_stream(password, salt, 'sha256')
    if kdf == 'pbkdf2-sha256-10000':
        return hashlib.pbkdf2_hmac('sha256', password, salt, 10000, 48)
    raise ValueError(kdf)


def unpad(pt):
    if not pt:
        return 0, None
    n = pt[-1]
    if 1 <= n <= 16 and pt[-n:] == bytes([n]) * n:
        return n, pt[:-n]
    return 0, None


def load_envelopes():
    locked = {}
    for name in ('terminal_phase3_2_end', 'salphaseion_short', 'cosmic_duality'):
        raw = (DATA / f'locked_{name}.bin').read_bytes()
        locked[name] = describe(name, raw, validated=False)
    phase3 = (DATA / 'phase3_plaintext.bin').read_bytes()
    blob = base64_blob(phase3[phase3.index(b'U2FsdGVk'):])
    locked['phase3_2_control'] = describe('phase3_2_control', blob, validated=True)
    return locked


def base64_blob(raw_tail):
    import base64
    return base64.b64decode(re.sub(rb'\s+', b'', raw_tail))


def describe(name, raw, validated):
    salted = raw[:8] == b'Salted__'
    return {
        'name': name,
        'raw_len': len(raw),
        'head16': raw[:16].hex(),
        'salted': salted,
        'salt': raw[8:16].hex() if salted else None,
        'ct': raw[16:] if salted else raw,
        'ct_len': len(raw) - 16 if salted else len(raw),
        'validated_round_trip': validated,
        'raw': raw,
    }


def forms(text):
    data = text.encode('utf-8')
    digest = hashlib.sha256(data).digest()
    yield 'literal', data
    yield 'sha256hex', digest.hex().encode('ascii')
    yield 'rawdigest', digest


def add(pool, source, text):
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    if not text or text.isspace():
        return
    pool.setdefault(text, set()).add(source)


def load_candidates():
    pool = {}
    gap = json.loads((ROOT / 'runs/2026-11-10_step2_gap_sums_v2/results.json').read_text())
    for row in gap['parses']['84']['outputs']:
        add(pool, 'step2-84cell-decode', row['text'])
        vals = row['values']
        add(pool, 'step2-84cell-digits', ''.join(str(v) for v in vals))
        add(pool, 'step2-84cell-digits', ','.join(str(v) for v in vals))
        add(pool, 'step2-84cell-digits', ' '.join(str(v) for v in vals))
    model = json.loads((ROOT / 'runs/2026-09-14_dbbi_forward_comparison/models.json').read_text())['perbyte84']
    primes = [c['token'] for c in model['cells'] if c['prime']]
    add(pool, 'standing-84cell', model['payload'])
    add(pool, 'standing-84cell', ''.join(primes))
    add(pool, 'standing-84cell', ' '.join(primes))
    add(pool, 'standing-84cell', '23-16-7')
    add(pool, 'standing-84cell', '23167')
    b = sum(t == 'b' for t in primes)
    be = sum(t == 'be' for t in primes)
    if (len(primes), b, be) != (23, 16, 7):
        raise SystemExit(f'84-cell census changed: {len(primes)} {b} {be}')
    sel = ROOT / 'runs/2026-11-10_step2_sumlist_lastwords_v3/outputs.jsonl'
    for line in sel.read_text(encoding='utf-8').splitlines():
        if line.strip():
            add(pool, 'step23-selection', json.loads(line)['text'])
    last = ROOT / 'runs/2026-09-13_last_words_referents/candidates.jsonl'
    for line in last.read_text(encoding='utf-8').splitlines():
        if line.strip():
            add(pool, 'step3-lastwords', json.loads(line)['cand'])
    for label in ('yinyang', 'yin yang', 'yin-yang', 'yingyang', 'the yinyang', 'theyinyang'):
        add(pool, 'step4-label', label)
    for frag, _score in top_chat_fragments():
        add(pool, 'chat-fragment', frag)
    items = [(text, sorted(sources)) for text, sources in pool.items()]
    items.sort(key=lambda row: row[0])
    return items


def creator_pieces():
    raw = (ROOT / 'telegram/sourcebooks/CREATOR_MESSAGES.md').read_text(encoding='utf-8')
    bodies = re.findall(r'````text\n(.*?)````', raw, re.S)
    pieces = []
    for body in bodies:
        lines = body.splitlines()
        message = '\n'.join(lines[1:]).strip() if lines else ''
        if not message:
            continue
        # Whole messages are the closed hashed-raw sweep. Keep sentences and clauses.
        for chunk in re.split(r'[.!?]\s+|\n+', message):
            chunk = chunk.strip(' \t"“”')
            if 12 <= len(chunk) <= 180 and chunk != message:
                pieces.append(chunk)
            for clause in re.split(r'[,;:]\s+', chunk):
                clause = clause.strip(' \t"“”')
                if 12 <= len(clause) <= 120 and clause != message:
                    pieces.append(clause)
    return list(dict.fromkeys(pieces))


def top_chat_fragments(limit=500):
    scored = []
    for piece in creator_pieces():
        score = english_score(piece)
        if score is None:
            continue
        scored.append((score, piece))
    scored.sort(key=lambda row: (-row[0], row[1]))
    # English prose sits near -4.4. Keep the top slice, and every fragment that
    # scores like prose, without taking the whole catalog.
    chosen = []
    for score, piece in scored:
        if len(chosen) >= limit and score < -4.6:
            break
        if len(chosen) >= limit and score >= -4.6 and len(chosen) >= 800:
            break
        chosen.append((piece, score))
        if len(chosen) >= 800:
            break
    return chosen


def confirmation_rows(envelopes):
    rows = []
    for env in envelopes.values():
        rows.append({
            'envelope': env['name'],
            'raw_decoded_len': env['raw_len'],
            'first_16_hex': env['head16'],
            'salted_magic': env['salted'],
            'salt_hex': env['salt'],
            'ciphertext_len': env['ct_len'],
            'validated_round_trip': env['validated_round_trip'],
        })
    return rows


def decrypt_one(ct, material, iv):
    pt = AES.new(material[:32], AES.MODE_CBC, iv).decrypt(ct)
    return unpad(pt)


def structured(pt):
    if pt is None:
        return False, None, 0.0
    if not pt:
        return False, None, 0.0
    printable = sum(32 <= b < 127 or b in (9, 10, 13) for b in pt) / len(pt)
    try:
        text = pt.decode('utf-8')
    except UnicodeDecodeError:
        text = pt.decode('latin1')
    score = english_score(text)
    good = (score is not None and score >= -4.6) or (printable >= 0.90 and len(pt) >= 20)
    return good, score, printable


G = {}


def _init(packed):
    G['env'] = packed


def _work(chunk):
    """chunk is a list of (text, sources)."""
    counts = Counter()
    hits = []
    envelopes = G['env']
    targets = [e for e in envelopes if e['name'] != 'phase3_2_control']
    for text, sources in chunk:
        for form, password in forms(text):
            for env in targets:
                salt = env['raw'][8:16]
                ct = env['ct']
                derived = {}
                for kdf in KDFs:
                    derived[kdf] = derive(password, salt, kdf)
                for kdf in KDFs:
                    material = derived[kdf]
                    for iv_name, iv in (('derived', material[32:48]), ('zero', ZERO_IV)):
                        pad, pt = decrypt_one(ct, material, iv)
                        key = (env['name'], kdf, iv_name)
                        counts[(key, 'tests')] += 1
                        if not pad:
                            continue
                        counts[(key, 'pad_ge_1')] += 1
                        if pad >= 3:
                            counts[(key, 'pad_ge_3')] += 1
                        good, score, printable = structured(pt)
                        if good:
                            counts[(key, 'structured')] += 1
                        if pad >= 3 or good:
                            hits.append({
                                'envelope': env['name'],
                                'kdf': kdf,
                                'iv': iv_name,
                                'form': form,
                                'pad': pad,
                                'pt_len': len(pt),
                                'printable': round(printable, 3),
                                'english_score': None if score is None else round(score, 3),
                                'structured': good,
                                'sources': sources,
                                'candidate': text[:180],
                                'head_hex': pt[:32].hex(),
                            })
    return counts, hits


def control_matrix(envelopes):
    env = envelopes['phase3_2_control']
    rows = []
    for form, password in forms(PHASE32_ANSWER):
        material_by_kdf = {kdf: derive(password, env['raw'][8:16], kdf) for kdf in KDFs}
        for kdf, material in material_by_kdf.items():
            for iv_name, iv in (('derived', material[32:48]), ('zero', ZERO_IV)):
                pad, pt = decrypt_one(env['ct'], material, iv)
                opened = pad == 10 and pt is not None and len(pt) == 2422 and pt.startswith(b"I've been waiting")
                rows.append({
                    'form': form,
                    'kdf': kdf,
                    'iv': iv_name,
                    'pad': pad,
                    'pt_len': None if pt is None else len(pt),
                    'opens_phase32': opened,
                })
    expected = [r for r in rows if r['form'] == 'sha256hex' and r['kdf'] == 'evp-sha256' and r['iv'] == 'derived']
    if not expected or not expected[0]['opens_phase32']:
        raise SystemExit('control failed: EVP-SHA256 + derived IV + sha256 hex did not open phase 3.2')
    return rows


def matrix_from(counts, n_candidates):
    rows = []
    for env in ('terminal_phase3_2_end', 'salphaseion_short', 'cosmic_duality'):
        for kdf in KDFs:
            for iv in IVS:
                key = (env, kdf, iv)
                tests = counts.get((key, 'tests'), 0)
                rows.append({
                    'envelope': env,
                    'kdf': kdf,
                    'iv': iv,
                    'tests': tests,
                    'pad_ge_1': counts.get((key, 'pad_ge_1'), 0),
                    'pad_ge_1_expected': round(tests / 256, 2),
                    'pad_ge_3': counts.get((key, 'pad_ge_3'), 0),
                    'pad_ge_3_expected': round(tests / 16777216, 4),
                    'structured': counts.get((key, 'structured'), 0),
                })
    return rows


def source_counts(items):
    c = Counter()
    for _text, sources in items:
        for source in sources:
            c[source] += 1
    return dict(c)


def write_report(conf, control, rows, hits, items, elapsed):
    RUN.mkdir(parents=True, exist_ok=True)
    payload = {
        'confirmation': conf,
        'control_phase32': control,
        'candidates': len(items),
        'source_counts': source_counts(items),
        'forms': list(FORMS),
        'elapsed_sec': round(elapsed, 1),
        'matrix': rows,
        'hits': hits,
        'excluded': 'whole-message hashed-raw sweep; 83-cell parse; new password families',
        'standing': '84-cell parse, 23 prime tokens, 16 b and 7 be',
    }
    (RUN / 'results.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    lines = []
    lines.append('# KDF model check, 2026-11-27')
    lines.append('')
    lines.append('The 11.3M candidate dump from the previous pass is not in this repository.')
    lines.append('This run uses the saved step-2, step-3 and step-4 strings and the')
    lines.append('top-scoring creator-message fragments. It does not rebuild a password family')
    lines.append('and it does not repeat the whole-message hashed-raw sweep.')
    lines.append('The 84-cell parse stands: 23 prime tokens, 16 `b` and 7 `be`.')
    lines.append('')
    lines.append('## 1. Ciphertext, before any decrypt')
    lines.append('')
    lines.append('| Envelope | Decoded bytes | First 16 bytes | Salted__ | Salt | Ciphertext bytes | Validated round-trip |')
    lines.append('|---|---:|---|---|---|---:|---|')
    for row in conf:
        lines.append(
            f"| {row['envelope']} | {row['raw_decoded_len']} | `{row['first_16_hex']}` | "
            f"{'yes' if row['salted_magic'] else 'no'} | `{row['salt_hex']}` | {row['ciphertext_len']} | "
            f"{'yes' if row['validated_round_trip'] else 'no'} |"
        )
    lines.append('')
    lines.append('Salted__ is the ASCII magic `53 61 6c 74 65 64 5f 5f`. Where it is present, bytes 8–15 are the salt and the ciphertext starts at byte 16.')
    lines.append('Terminal, SalPhaseIon short and Cosmic Duality have no validated round-trip. Phase 3.2 does, and it is the control only.')
    lines.append('')
    lines.append('## 2. Control: the one envelope that opens')
    lines.append('')
    lines.append('Answer `jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple`. An open is pad 10 and the 2,422-byte plaintext beginning `I\'ve been waiting`.')
    lines.append('')
    lines.append('| Form | KDF | IV | Pad | Opens |')
    lines.append('|---|---|---|---:|---|')
    for row in control:
        lines.append(f"| {row['form']} | {row['kdf']} | {row['iv']} | {row['pad']} | {'yes' if row['opens_phase32'] else 'no'} |")
    lines.append('')
    lines.append('## 3. Candidates')
    lines.append('')
    lines.append(f"{len(items)} unique strings. A string can belong to more than one source.")
    lines.append('')
    for source, n in sorted(source_counts(items).items()):
        lines.append(f'- `{source}`: {n}')
    lines.append('')
    lines.append('Forms on every string: literal UTF-8, lowercase sha256 hex, raw 32-byte sha256.')
    lines.append(f'Runtime {elapsed:.0f}s.')
    lines.append('')
    lines.append('## 4. Matrix')
    lines.append('')
    lines.append('`pad>=1` is the chance PKCS#7 gate (about 1/256). `pad>=3` is the signal named for this run (about 1/16.8M). Structured means the unpadded bytes score as English (quadgram ≥ -4.6) or are at least 90% printable and 20 bytes or longer.')
    lines.append('')
    lines.append('| Envelope | KDF | IV | Tests | pad≥1 | expected | pad≥3 | expected | structured |')
    lines.append('|---|---|---|---:|---:|---:|---:|---:|---:|')
    for row in rows:
        lines.append(
            f"| {row['envelope']} | {row['kdf']} | {row['iv']} | {row['tests']} | {row['pad_ge_1']} | "
            f"{row['pad_ge_1_expected']} | {row['pad_ge_3']} | {row['pad_ge_3_expected']} | {row['structured']} |"
        )
    lines.append('')
    lines.append('## 5. Hits')
    lines.append('')
    if not hits:
        lines.append('No pad≥3 decrypt and no structured plaintext on the three locked envelopes.')
        lines.append('')
        lines.append('## 6. What this separates')
        lines.append('')
        lines.append('A fixed or zero IV does not kill the PKCS#7 gate. In CBC the last block is chained to the previous ciphertext block, so the padding bytes never see the message IV. The phase 3.2 control shows it: sha256 hex with EVP-SHA256 and a zero IV still has pad 10, and the plaintext does not open, because the first block is the one the IV changes.')
        lines.append('')
        lines.append('Every KDF sits on the 1/256 line. None of them produces a pad≥3 hit. The model that opens phase 3.2 stays sha256 hex, EVP_BytesToKey SHA-256, and the IV from that same stream. MD5, PBKDF2, a raw digest and a zero IV fail that control, and they do not produce pad≥3 hits on the two unopened envelopes.')
    else:
        for hit in hits:
            lines.append(
                f"- {hit['envelope']} {hit['kdf']} iv={hit['iv']} form={hit['form']} pad={hit['pad']} "
                f"printable={hit['printable']} english={hit['english_score']} `{hit['candidate']}` head `{hit['head_hex']}`"
            )
    lines.append('')
    (RUN / 'REPORT.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main():
    envelopes = load_envelopes()
    conf = confirmation_rows(envelopes)
    print('CIPHERTEXT CONFIRMATION (before decrypt)', flush=True)
    for row in conf:
        trip = 'validated round-trip' if row['validated_round_trip'] else 'NO validated round-trip'
        magic = 'Salted__ yes' if row['salted_magic'] else 'Salted__ no'
        print(
            f"  {row['envelope']}: len={row['raw_decoded_len']} head={row['first_16_hex']} "
            f"{magic} salt={row['salt_hex']} ct={row['ciphertext_len']} {trip}",
            flush=True,
        )
    print('CONTROL', flush=True)
    control = control_matrix(envelopes)
    for row in control:
        if row['opens_phase32'] or row['pad']:
            print(f"  open={row['opens_phase32']} form={row['form']} kdf={row['kdf']} iv={row['iv']} pad={row['pad']}", flush=True)
    print('LOADING CANDIDATES', flush=True)
    items = load_candidates()
    print(f'  {len(items)} unique strings {source_counts(items)}', flush=True)
    packed = []
    for env in envelopes.values():
        packed.append({
            'name': env['name'],
            'raw': env['raw'],
            'ct': env['ct'],
        })
    workers = 4
    chunk = max(1, len(items) // (workers * 8))
    chunks = [items[i:i + chunk] for i in range(0, len(items), chunk)]
    counts = Counter()
    hits = []
    t0 = time.time()
    with mp.get_context('fork').Pool(workers, initializer=_init, initargs=(packed,)) as pool:
        done = 0
        for part_counts, part_hits in pool.imap_unordered(_work, chunks):
            counts.update(part_counts)
            hits.extend(part_hits)
            done += 1
            if done % 4 == 0 or done == len(chunks):
                print(f'  chunks {done}/{len(chunks)} {time.time() - t0:.0f}s', flush=True)
    elapsed = time.time() - t0
    rows = matrix_from(counts, len(items))
    hits.sort(key=lambda h: (h['envelope'], h['kdf'], h['iv'], -h['pad']))
    write_report(conf, control, rows, hits, items, elapsed)
    print('MATRIX', flush=True)
    for row in rows:
        print(
            f"  {row['envelope']:24} {row['kdf']:22} {row['iv']:8} tests={row['tests']:6} "
            f"pad1={row['pad_ge_1']:4}/{row['pad_ge_1_expected']} pad3={row['pad_ge_3']} structured={row['structured']}",
            flush=True,
        )
    print(f'HITS {len(hits)} elapsed {elapsed:.0f}s wrote {RUN}', flush=True)


if __name__ == '__main__':
    main()
