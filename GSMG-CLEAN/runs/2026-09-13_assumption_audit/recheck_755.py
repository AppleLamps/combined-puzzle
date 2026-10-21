"""Independent AES replay, trigger accounting, and fragment review. No dismissal gate."""
import hashlib
import json
import math
import random
import re
import sys
from collections import Counter
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import inspect_decrypts as inspector

SOURCE = ROOT / 'runs/2026-09-13_assumption_audit/all_padding_valid.jsonl'
OUT = ROOT / 'runs/2026-09-13_recheck_755'
PRINT = re.compile(rb'[\x20-\x7e]{6,}')

def independent_decrypt(row):
    raw = (ROOT / 'data' / ('locked_' + row['envelope'] + '.bin')).read_bytes()
    assert raw[:8] == b'Salted__' and (len(raw)-16) % 16 == 0
    password = row['candidate'].encode('utf-8')
    if row['profile'] in ('gsmg', 'gsmg-md5'):
        password = hashlib.sha256(password).hexdigest().encode('ascii')
    digest = hashlib.md5 if row['profile'].endswith('md5') else hashlib.sha256
    material, previous = b'', b''
    while len(material) < 48:
        previous = digest(previous + password + raw[8:16]).digest()
        material += previous
    cipher = Cipher(algorithms.AES(material[:32]), modes.CBC(material[32:48]))
    decryptor = cipher.decryptor()
    padded = decryptor.update(raw[16:]) + decryptor.finalize()
    n = padded[-1]
    assert 1 <= n <= 16 and padded[-n:] == bytes([n])*n
    assert n == row['pad'] and padded[:-n].hex() == row['plaintext_hex']
    return padded, raw

def fragments(raw):
    found = []
    for name in ('ascii', 'cp037', 'cp273'):
        view = raw if name == 'ascii' else raw.decode(name).encode('ascii', 'replace')
        # Replace non-ASCII with a nonprintable byte so '?' doesn't manufacture runs.
        if name != 'ascii':
            view = bytes(ord(c) if ord(c) < 128 else 0 for c in raw.decode(name))
        for m in PRINT.finditer(view):
            found.append(dict(encoding=name, offset=m.start(), text=m.group().decode()))
    # Both byte alignments, retaining actual source byte offsets.
    for endian in ('little', 'big'):
        for align in (0, 1):
            view = bytes(v if 32 <= v <= 126 else 0 for i in range(align, len(raw)-1, 2)
                         for v in [int.from_bytes(raw[i:i+2], endian)])
            for m in PRINT.finditer(view):
                found.append(dict(encoding='utf16-' + endian, offset=align+2*m.start(), text=m.group().decode()))
    return found

def embedded(raw):
    events = []
    magics = [(b'Salted__', 'openssl'), (b'\x1f\x8b', 'gzip'), (b'BZh', 'bzip2'),
              (b'\xfd7zXZ\x00', 'xz'), (b'%PDF-', 'pdf'), (b'PK\x03\x04', 'zip'),
              (b'\x89PNG\r\n\x1a\n', 'png')]
    for sig, name in magics:
        for m in re.finditer(re.escape(sig), raw):
            event = dict(kind=name, offset=m.start(), status='signature-only')
            if name in ('gzip', 'bzip2', 'xz'):
                decoded = inspector.decompress(raw[m.start():])
                if decoded:
                    _, data, status = decoded
                    event.update(status=status, decoded_hex=None if data is None else data.hex())
            events.append(event)
    # Validate possible zlib streams at EVERY offset; preserve failures too.
    for i in range(len(raw)-1):
        a, b = raw[i:i+2]
        if a & 15 == 8 and a >> 4 <= 7 and (a*256+b) % 31 == 0:
            decoded = inspector.decompress(raw[i:])
            if decoded:
                name, data, status = decoded
                events.append(dict(kind=name, offset=i, status=status,
                                   decoded_hex=None if data is None else data.hex()))
    for f in fragments(raw):
        if len(f['text']) < 16:
            continue
        for kind, value in inspector.encoded_views(f['text']):
            events.append(dict(kind='embedded-' + kind, offset=f['offset'], encoding=f['encoding'],
                               decoded_hex=value.hex(), status='decoded-not-authenticated'))
    return events

def metrics(raw):
    runs = re.findall(rb'[\x20-\x7e]+', raw)
    return (sum(32 <= b <= 126 or b in (9, 10, 13) for b in raw)/len(raw),
            max(map(len, runs), default=0))

def main():
    OUT.mkdir(exist_ok=True)
    rows = [json.loads(line) for line in SOURCE.read_text().splitlines()]
    assert len(rows) == 755
    # Positive controls: mixed binary/text, UTF16 at odd offset, and embedded compression.
    import zlib
    assert any(f['text'] == 'Follow the white rabbit' for f in fragments(b'\xff\x00Follow the white rabbit\x00\xff'))
    assert any(f['encoding'] == 'utf16-little' and f['offset'] == 1 for f in fragments(b'\xff' + 'Read the next instruction'.encode('utf-16-le')))
    assert any(e['status'] == 'complete' for e in embedded(b'\xff' + zlib.compress(b'next instruction')))
    # A real mixed-encoding solved stage is intentionally NOT required to pass a global text gate.
    solved = (ROOT / 'data/phase3_2_plaintext.bin').read_bytes()
    assert any("I've been waiting for you" in f['text'] for f in fragments(solved))
    counts = Counter()
    actual_metrics = []
    pad2, event_rows = [], []
    with (OUT / 'reviewed_outputs.jsonl').open('w', encoding='utf-8') as out:
        for index, row in enumerate(rows, 1):
            padded, envelope = independent_decrypt(row)
            raw = bytes.fromhex(row['plaintext_hex'])
            fs, events = fragments(raw), embedded(raw)
            mt = metrics(raw)
            actual_metrics.append(mt)
            counts['independently_reproduced'] += 1
            counts['pad_' + str(row['pad'])] += 1
            counts['outputs_with_fragments'] += bool(fs)
            counts['outputs_with_embedded_events'] += bool(events)
            for e in events:
                counts[e['kind'] + ':' + e['status']] += 1
            record = dict(id=index, source=row, status='UNRESOLVED_RETAINED',
                          trigger='PKCS7_PADDING_VALID_ONLY', pad_bytes_hex=padded[-row['pad']:].hex(),
                          final_decrypted_block_hex=padded[-16:].hex(),
                          envelope_sha256=hashlib.sha256(envelope).hexdigest(),
                          independent_plaintext_verified=True,
                          ascii_ratio=mt[0], longest_ascii_run=mt[1], fragments=fs, embedded_events=events,
                          interpretation='No authenticity conclusion follows from padding or unrecognized formatting.')
            out.write(json.dumps(record, ensure_ascii=True)+'\n')
            if row['pad'] == 2:
                pad2.append(record)
            if events:
                event_rows.append(record)
    # A deterministic, length-matched wrong-key baseline for aggregate ASCII statistics.
    # Bodies after removing a valid random padding tail are modeled as uniform bytes.
    rng = random.Random(75520260913)
    controls = []
    for _ in range(100):
        ms = [metrics(rng.randbytes(len(bytes.fromhex(r['plaintext_hex'])))) for r in rows]
        controls.append(dict(max_ascii_ratio=max(m[0] for m in ms), max_ascii_run=max(m[1] for m in ms)))
    observed = dict(max_ascii_ratio=max(m[0] for m in actual_metrics), max_ascii_run=max(m[1] for m in actual_metrics))
    N = 188112
    lam2 = N / 256**2
    summary = dict(counts=dict(counts), all_status='UNRESOLVED_RETAINED',
                   source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                   unique_plaintexts=len(set(r['plaintext_hex'] for r in rows)),
                   trials_in_source_run=N, expected_pad1=N/256, expected_pad2=lam2,
                   expected_any_valid_padding=N*sum(256**(-k) for k in range(1,17)),
                   poisson_approx_probability_at_least_5_pad2=1-math.exp(-lam2)*sum(lam2**k/math.factorial(k) for k in range(5)),
                   observed_metrics=observed,
                   controls_count=100,
                   control_batches_at_least_observed={k:sum(c[k]>=v for c in controls) for k,v in observed.items()},
                   positive_controls='mixed ASCII, odd-offset UTF16, embedded zlib, actual solved Phase3.2: passed',
                   caution='Random-like aggregate results do not prove any particular output is incorrect. '
                           'Statistical baseline assumes wrong-key pseudorandom outputs; correlated trials can depart from it.')
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2))
    (OUT/'controls.json').write_text(json.dumps(controls,indent=2))
    (OUT/'pad2_review.json').write_text(json.dumps(pad2,indent=2))
    (OUT/'embedded_review.json').write_text(json.dumps(event_rows,indent=2))
    print(json.dumps(summary,indent=2))

if __name__ == '__main__':
    main()
