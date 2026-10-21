"""Lossless padding-valid journal plus bounded, multi-format plaintext inspection.

python tools/inspect_decrypts.py --replay runs/.../all_padding_valid.jsonl --out runs/inspection
python tools/inspect_decrypts.py --file candidates.txt --profiles all --out runs/inspection
Format recognition is a lead, never authentication. Unknown bytes are retained.
"""
import argparse
import base64
import bz2
import hashlib
import json
import lzma
import re
import zlib
from collections import Counter, deque
from pathlib import Path
import check_candidate as cc

MAX_BYTES = 65536
MAX_NODES = 32
KEY_BYTES = 4096

def enable_fast_keys():
    try:
        from coincurve import PrivateKey
    except ImportError:
        return 'pure-python'
    original = cc.scalar_hits
    def fast(k):
        if not 1 <= k < cc.N:
            return []
        pub = PrivateKey(k.to_bytes(32, 'big')).public_key
        return [f'{cc.TARGETS[h]} ({label})'
                for compressed, label in ((True, 'compressed'), (False, 'uncompressed'))
                if (h := cc.h160(pub.format(compressed=compressed))) in cc.TARGETS]
    for k in (1, 2, 1234567, cc.N - 1):
        assert sorted(fast(k)) == sorted(original(k))
    cc.scalar_hits = fast
    return 'coincurve'

def text_views(raw):
    for enc in ('utf-8-sig', 'utf-16-le', 'utf-16-be', 'utf-32-le', 'utf-32-be',
                'cp037', 'cp273', 'latin1'):
        try:
            text = raw.decode(enc)
        except UnicodeError:
            continue
        # Decodability alone (especially UTF-16/Latin-1) carries little evidence.
        printable = sum(c.isprintable() or c in '\r\n\t' for c in text) / max(1, len(text))
        ascii_letters = sum(c.isascii() and c.isalpha() for c in text) / max(1, len(text))
        structured = bool(re.fullmatch(r'[0-9a-fA-F\s]{16,}', text))
        if printable >= .95 and (ascii_letters >= .35 or structured) and len(text.strip()) >= 8:
            yield enc, text

def decompress(raw):
    if raw.startswith(b'\x1f\x8b'):
        name, decoder = 'gzip', zlib.decompressobj(31)
    elif len(raw) >= 2 and raw[0] & 15 == 8 and int.from_bytes(raw[:2], 'big') % 31 == 0:
        name, decoder = 'zlib', zlib.decompressobj()
    elif raw.startswith(b'BZh'):
        name, decoder = 'bzip2', bz2.BZ2Decompressor()
    elif raw.startswith(b'\xfd7zXZ\x00'):
        name, decoder = 'xz', lzma.LZMADecompressor(memlimit=32 * 1024 * 1024)
    else:
        return None
    try:
        value = decoder.decompress(raw, MAX_BYTES + 1)
        if len(value) > MAX_BYTES:
            return name, value[:MAX_BYTES], 'output-limit'
        if not decoder.eof:
            return name, value, 'incomplete-or-limited'
        return name, value, 'complete-with-trailing-data' if decoder.unused_data else 'complete'
    except (ValueError, OSError, EOFError, zlib.error, lzma.LZMAError):
        return name, None, 'invalid'

def encoded_views(text):
    compact = re.sub(r'\s+', '', text)
    stripped = compact.removeprefix('0x')
    if len(stripped) >= 16 and len(stripped) % 2 == 0 and re.fullmatch('[0-9a-fA-F]+', stripped):
        yield 'hex', bytes.fromhex(stripped)
    if len(compact) >= 8 and len(compact) % 8 == 0 and re.fullmatch('[01]+|[ab]+', compact):
        bits = compact.translate(str.maketrans('ab', '01'))
        yield 'binary', bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    for name, token, alt in [('base64', compact, None), ('base64url', compact, b'-_')]:
        if len(token) < 16 or not re.fullmatch(r'[A-Za-z0-9+/_-]+={0,2}', token):
            continue
        try:
            value = base64.b64decode(token + '=' * (-len(token) % 4), altchars=alt, validate=True)
            canonical = base64.b64encode(value, altchars=alt).decode().rstrip('=')
            if canonical == token.rstrip('='):
                yield name, value
        except ValueError:
            pass
    if 8 <= len(compact) <= 4000 and re.fullmatch('[0-9]+|[a-io]+', compact):
        digits = compact.translate(str.maketrans('abcdefghio', '1234567890'))
        n = int(digits)
        yield 'decimal-integer', n.to_bytes(max(1, (n.bit_length()+7)//8), 'big')

def inspect(raw, depth=2, keys=True):
    queue = deque([('raw', raw, 0)])
    seen = set()
    nodes, limits = [], []
    while queue and len(nodes) < MAX_NODES:
        path, data, level = queue.popleft()
        if data in seen:
            continue
        seen.add(data)
        if len(data) > MAX_BYTES:
            limits.append(path + ': byte limit')
            continue
        node = dict(path=path, length=len(data), plaintext_hex=data.hex(), signals=[], key_matches=[])
        nodes.append(node)
        signals = node['signals']
        if data.startswith(b'Salted__') and len(data) >= 32 and (len(data)-16) % 16 == 0:
            signals.append('OpenSSL envelope shape; cipher/KDF unknown')
        for magic, name in ((b'%PDF-', 'PDF'), (b'PK\x03\x04', 'ZIP'), (b'\x89PNG\r\n\x1a\n', 'PNG')):
            if data.startswith(magic):
                signals.append(name + ' signature only')
        if keys:
            if len(data) > KEY_BYTES:
                limits.append(path + ': raw key scanning limited to first 4096 bytes')
            node['key_matches'] = [(d, h) for d, h in cc.find_keys(data[:KEY_BYTES]) if h]
            # Additional scalar layouts: little endian and decimal text.
            for i in range(max(0, min(len(data), KEY_BYTES)-31)):
                hits = cc.scalar_hits(int.from_bytes(data[i:i+32], 'little'))
                if hits:
                    node['key_matches'].append((f'raw32-little@{i}', hits))
        children = []
        packed = decompress(data)
        if packed:
            name, decoded, status = packed
            signals.append(name + ': ' + status)
            if decoded is not None:
                children.append((name, decoded))
            if status in ('output-limit', 'incomplete-or-limited'):
                limits.append(path + ': ' + name + ' ' + status)
        texts = list(text_views(data))
        for enc, text in texts:
            signals.append('text heuristic: ' + enc)
            node.setdefault('text_previews', []).append(dict(encoding=enc, preview=text[:500]))
            if enc != 'utf-8-sig':
                children.append((enc + '-to-utf8', text.encode()))
        # Structured encodings may be entirely numeric and fail prose heuristics.
        try:
            text = data.decode('utf-8-sig')
        except UnicodeError:
            text = None
        if text is not None:
            try:
                obj = json.loads(text)
                if isinstance(obj, (list, dict)):
                    signals.append('JSON container parsed')
            except (ValueError, RecursionError):
                pass
            children.extend(encoded_views(text))
            if keys:
                for m in re.finditer(r'(?<!\d)\d{1,78}(?!\d)', text):
                    hits = cc.scalar_hits(int(m.group()))
                    if hits:
                        node['key_matches'].append((f'decimal@{m.start()}', hits))
        for name, child in children:
            if child == data or child in seen:
                continue
            signals.append('decodable: ' + name)
            if level < depth:
                queue.append((path + '/' + name, child, level + 1))
            else:
                limits.append(path + '/' + name + ': depth limit')
    if queue:
        limits.append('node limit')
    assessment = 'FINAL_KEY_MATCH' if any(n['key_matches'] for n in nodes) else 'UNRESOLVED_RETAINED'
    return dict(nodes=nodes, limits=sorted(set(limits)), key_check_enabled=keys,
                assessment=assessment,
                interpretation='Unrecognized formatting is not evidence of unimportance or an incorrect password.')

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    source = ap.add_mutually_exclusive_group(required=True)
    source.add_argument('--replay', type=Path, help='JSONL with plaintext_hex; preserves input metadata')
    source.add_argument('--file', type=Path, help='UTF-8 candidate text, one exact answer per line')
    ap.add_argument('--profiles', choices=['all', *cc.PROFILES], default='gsmg')
    ap.add_argument('--out', required=True, type=Path, help='new output directory')
    ap.add_argument('--depth', type=int, choices=range(5), default=2)
    ap.add_argument('--no-key-check', action='store_true', help='format-only inspection, explicitly recorded')
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    backend = enable_fast_keys() if not args.no_key_check else 'disabled'
    profiles = list(cc.PROFILES) if args.profiles == 'all' else [args.profiles]
    counts = Counter()
    def records():
        source_path = args.replay or args.file
        with source_path.open(encoding='utf-8') as f:
            for line_number, line in enumerate(f, 1):
                if args.replay:
                    yield json.loads(line)
                    continue
                candidate = line.rstrip('\r\n')
                for profile in profiles:
                    for name, raw in cc.ENVELOPES.items():
                        counts['trials'] += 1
                        pad, pt = cc.try_envelope(raw, candidate, profile)
                        if pad:
                            yield dict(candidate=candidate, source_line=line_number, profile=profile,
                                       envelope=name, pad=pad, plaintext_hex=pt.hex())
    with (args.out / 'all_results.jsonl').open('w', encoding='utf-8') as out:
        for row in records():
            raw = bytes.fromhex(row['plaintext_hex'])
            result = inspect(raw, args.depth, not args.no_key_check)
            out.write(json.dumps(dict(source=row, inspection=result), ensure_ascii=True) + '\n')
            out.flush()
            counts['retained'] += 1
            counts['with_format_signals'] += any(n['signals'] for n in result['nodes'])
            counts['with_key_matches'] += any(n['key_matches'] for n in result['nodes'])
            counts['with_limits'] += bool(result['limits'])
            if counts['retained'] % 100 == 0:
                print(f"Retained and inspected {counts['retained']} outputs", flush=True)
    manifest = dict(source=str(args.replay or args.file),
                    source_sha256=hashlib.sha256((args.replay or args.file).read_bytes()).hexdigest(),
                    profiles=profiles if args.file else 'inherited from replay', depth=args.depth,
                    key_backend=backend, counts=dict(counts), max_nodes=MAX_NODES,
                    max_bytes=MAX_BYTES, key_scan_bytes=KEY_BYTES,
                    interpretation='Signals are leads, not authenticated decryptions. Unknown bytes retained. '
                                   'Live mode assumes PKCS#7; no unpadded or alternate cipher search.')
    (args.out / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(manifest, indent=2))

if __name__ == '__main__':
    main()
