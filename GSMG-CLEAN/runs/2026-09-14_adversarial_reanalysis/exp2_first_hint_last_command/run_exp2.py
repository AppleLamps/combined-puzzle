"""Experiment 2: 'sha256: our first hint is your last command' — bounded, source-based candidate set over the
three locked envelopes, with harness validation on Phases 2/3/3.2 and full raw-output retention.
See SPEC.md (written before this script was run)."""
import hashlib, json, os, re, sys, time, base64
from itertools import product

ROOT = 'E:/rabbit-combined/GSMG-CLEAN/'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'outputs')
os.makedirs(OUT, exist_ok=True)
LOG = open(os.path.join(HERE, 'run.log'), 'w', encoding='utf-8')


def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s)
    LOG.write(s + '\n')
    LOG.flush()


try:
    from Crypto.Cipher import AES
    def aes_cbc_dec(key, iv, ct):
        return AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    log('AES backend: pycryptodome')
except ImportError:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    def aes_cbc_dec(key, iv, ct):
        d = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
        return d.update(ct) + d.finalize()
    log('AES backend: cryptography')

import coincurve


def evp_bytes_to_key(password: bytes, salt: bytes, md: str, key_len=32, iv_len=16):
    out = b''
    prev = b''
    while len(out) < key_len + iv_len:
        prev = hashlib.new(md, prev + password + salt).digest()
        out += prev
    return out[:key_len], out[key_len:key_len + iv_len]


def openssl_decrypt(blob: bytes, password: bytes, md: str):
    assert blob[:8] == b'Salted__', 'not a Salted__ blob'
    salt = blob[8:16]
    key, iv = evp_bytes_to_key(password, salt, md)
    return aes_cbc_dec(key, iv, blob[16:])


def unpad(raw: bytes):
    if not raw:
        return None, 0
    n = raw[-1]
    if 1 <= n <= 16 and raw[-n:] == bytes([n]) * n:
        return raw[:-n], n
    return None, 0


def sha256hex(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


# ---------------------------------------------------------------- key recogniser (same logic as Experiment 1)
def b58dec_h160(addr):
    A = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    n = 0
    for ch in addr:
        n = n * 58 + A.index(ch)
    raw = n.to_bytes(25, 'big')
    assert hashlib.sha256(hashlib.sha256(raw[:-4]).digest()).digest()[:4] == raw[-4:]
    return raw[1:-4].hex()


MARKERS = {'18CchrjA3Uzfrzy4DFqao9ric6YfK4hjdc': 'marker_checkerboard',
           '1AD2wfwXukZ1kUAy848hTQQ72aSBZPB75r': 'marker_phase1',
           '13HGhjkmKUkP8sk9k63BLmhkxRjy7uK4Rp': 'marker_posterbits',
           '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe': 'prize_half',
           '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa': 'prize_betterhalf'}
TARGET_H160 = {b58dec_h160(a): lab for a, lab in MARKERS.items()}   # elements are hash160 hex, never addresses
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


def h160(pub: bytes) -> str:
    return hashlib.new('ripemd160', hashlib.sha256(pub).digest()).hexdigest()


def b58enc(b: bytes) -> str:
    A = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    n = int.from_bytes(b, 'big')
    s = ''
    while n:
        n, r = divmod(n, 58)
        s = A[r] + s
    return '1' * (len(b) - len(b.lstrip(b'\0'))) + s


def addr_from_h160(h: str) -> str:
    raw = b'\0' + bytes.fromhex(h)
    return b58enc(raw + hashlib.sha256(hashlib.sha256(raw).digest()).digest()[:4])


def oracle(k: int):
    if not (1 <= k < N):
        return None
    pk = coincurve.PrivateKey.from_int(k)
    hits = []
    for form, pub in (('compressed', pk.public_key.format(True)), ('uncompressed', pk.public_key.format(False))):
        h = h160(pub)
        if h in TARGET_H160:
            hits.append((form, TARGET_H160[h]))
        elif form == 'compressed' and addr_from_h160(h).startswith('1GyT5W'):
            hits.append((form, 'partial_1GyT5W'))
    return hits or None


def scalars_from_bytes(b: bytes):
    yield 'sha256', int.from_bytes(hashlib.sha256(b).digest(), 'big')
    yield 'sha256d', int.from_bytes(hashlib.sha256(hashlib.sha256(b).digest()).digest(), 'big')
    for i in range(0, max(0, len(b) - 31)):
        w = b[i:i + 32]
        yield f'raw32be@{i}', int.from_bytes(w, 'big')
        yield f'raw32le@{i}', int.from_bytes(w, 'little')
    txt = b.decode('latin1')
    for m in re.finditer(r'[0-9a-fA-F]{64}', txt):
        yield f'hex64@{m.start()}', int(m.group(), 16)
    for m in re.finditer(r'[0-9]{60,78}', txt):
        yield f'dec@{m.start()}', int(m.group())
    stripped = txt.strip()
    if stripped and stripped.isprintable():
        yield 'sha256_stripped', int.from_bytes(hashlib.sha256(stripped.encode()).digest(), 'big')


def recognise(b: bytes):
    seen = set()
    out = []
    for lab, k in scalars_from_bytes(b):
        if k in seen:
            continue
        seen.add(k)
        r = oracle(k)
        if r:
            out.append((lab, r))
    return out


# ---------------------------------------------------------------- harness validation
def extract_page_blobs():
    h = open(ROOT + 'originals/pages/phase2_choice.html', encoding='utf-8', errors='replace').read()
    blobs = [re.sub(r'\s', '', m.group()) for m in re.finditer(r'U2FsdGVk[A-Za-z0-9+/=\s]{40,}', h)]
    return [base64.b64decode(b) for b in blobs]


def validate():
    p2ct, p3ct = extract_page_blobs()
    p3pt = open(ROOT + 'data/phase3_plaintext.bin', 'rb').read()
    i = p3pt.find(b'U2FsdGVk')
    p32ct = base64.b64decode(re.sub(rb'\s', b'', p3pt[i:]))
    cases = [('phase2', p2ct, sha256hex('causality'), ROOT + 'data/phase2_plaintext.bin'),
             ('phase3', p3ct, '1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5', ROOT + 'data/phase3_plaintext.bin'),
             ('phase3_2', p32ct, sha256hex('jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple'), ROOT + 'data/phase3_2_plaintext.bin')]
    ok = True
    for name, ct, pw, ref in cases:
        want = open(ref, 'rb').read()
        raw = openssl_decrypt(ct, pw.encode(), 'sha256')
        pt, n = unpad(raw)
        good = pt == want
        # negative: one hex digit changed
        bad = list(pw)
        bad[10] = '0' if bad[10] != '0' else '1'
        rawn = openssl_decrypt(ct, ''.join(bad).encode(), 'sha256')
        ptn, nn = unpad(rawn)
        neg_ok = (ptn is None) or (ptn != want)
        # md5 profile must NOT open it (documents that the profile is distinguishable)
        rawm = openssl_decrypt(ct, pw.encode(), 'md5')
        ptm, _ = unpad(rawm)
        md5_opens = ptm == want
        log(f'VALIDATE {name}: ct={len(ct)}B salt={ct[8:16].hex()} sha256-profile match={good} pad={n} | negative control ok={neg_ok} | md5 profile opens={md5_opens}')
        ok &= good and neg_ok and not md5_opens
    # recogniser positive: Phase 1 answer must map to marker_phase1 through the production recogniser
    r = recognise(b'theflowerblossomsthroughwhatseemstobeaconcretesurface')
    log('VALIDATE recogniser on Phase-1 answer bytes:', r)
    ok &= any(lab == 'sha256' and ('compressed', 'marker_phase1') in hits for lab, hits in r)
    # recogniser positive: raw 32-byte key embedded in noise
    k = hashlib.sha256(b'theflowerblossomsthroughwhatseemstobeaconcretesurface').digest()
    r2 = recognise(b'xx' + k + b'yy')
    log('VALIDATE recogniser on embedded raw32 key:', r2)
    ok &= any(lab == 'raw32be@2' for lab, _ in r2)
    r3 = recognise(b'garbage bytes with no key in them at all 0123456789')
    log('VALIDATE recogniser negative:', r3)
    ok &= not r3
    return ok


# ---------------------------------------------------------------- candidates
def candidates():
    C = []
    def add(fid, label, s):
        C.append((fid, label, s))
    poem = ('Roses are White but often Red.\nYellow has a number and so does Blue.\n'
            'Go back to the first puzzle piece without further ado.\n\n'
            'It might have shown you only one door, beware that the rabbits nest may contain a whole lot more.\n\nHush hush.')
    F1 = ['Follow the white rabbit', 'follow the white rabbit', 'followthewhiterabbit', 'FOLLOWTHEWHITERABBIT',
          'Followthewhiterabbit', 'follow_the_white_rabbit', 'Follow the White Rabbit', 'follow the white rabbit.',
          'Follow the white rabbit.', 'white rabbit', 'whiterabbit', 'thewhiterabbit', 'rabbit']
    for s in F1: add('F1', 'follow_white_rabbit', s)
    add('F2', 'msg225_digest', '5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75')
    add('F2', 'msg225_digest_upper', '5AC407837447FBA24BA2802E4D1E9AECB4580AA29FEF1088CC387C180B746F75')
    add('F3', 'phase1_answer', 'theflowerblossomsthroughwhatseemstobeaconcretesurface')
    add('F3', 'phase1_answer_spaced', 'the flower blossoms through what seems to be a concrete surface')
    for s in ['giveit = givetit', 'giveit=givetit', 'givetit', 'giveit', 'give it', 'givetit = giveit']:
        add('F4', 'givetit', s)
    add('F5', 'poem_full', poem)
    add('F5', 'poem_full_crlf', poem.replace('\n', '\r\n'))
    add('F5', 'poem_line1', 'Roses are White but often Red.')
    add('F5', 'poem_line1_nopunct', 'rosesarewhitebutoftenred')
    add('F5', 'poem_hushhush', 'Hush hush.')
    add('F5', 'poem_hushhush2', 'hushhush')
    for s in ['gsmg.io/theseedisplanted', 'theseedisplanted', 'the seed is planted', 'https://gsmg.io/theseedisplanted']:
        add('F6', 'seed_planted', s)
    for s in ['HASHTHETEXT', 'hashthetext', 'hash the text']:
        add('F7', 'hashthetext', s)
    # 'last command' readings of the SalPhaseIon line itself (source-contained; also small)
    for s in ['enter', 'ENTER', 'thispassword', 'lastwordsbeforearchichoice', 'matrixsumlist', 'yellowblueprimes',
              'ourfirsthintisyourlastcommand', 'our first hint is your last command', 'firsthint', 'lastcommand',
              'shabefourfirsthintisyourlastcommand', 'shabefanstoo', 'sha256 ans too', 'shabef']:
        add('F8', 'salphaseion_literals', s)
    return C


def reps(s: str):
    h = sha256hex(s)
    yield 'raw', s.encode('utf-8')
    yield 'sha256hex', h.encode()
    yield 'sha256hex_twice', sha256hex(h).encode()


def main():
    t0 = time.time()
    log('== Experiment 2 run', time.strftime('%Y-%m-%d %H:%M:%S'))
    ok = validate()
    log('HARNESS VALID:', ok)
    if not ok:
        log('ABORT: harness validation failed; no envelope touched')
        sys.exit(1)
    envs = {}
    for name in ['locked_salphaseion_short', 'locked_terminal_phase3_2_end', 'locked_cosmic_duality']:
        b = open(ROOT + f'data/{name}.bin', 'rb').read()
        envs[name] = b
        log(f'ENVELOPE {name}: {len(b)}B salt={b[8:16].hex()} sha256={hashlib.sha256(b).hexdigest()}')
    C = candidates()
    rows = []
    n_valid_pad = 0
    n_total = 0
    hits = []
    idx = 0
    for fid, label, s in C:
        for rname, pw in reps(s):
            for md in ['sha256', 'md5']:
                for ename, blob in envs.items():
                    raw = openssl_decrypt(blob, pw, md)
                    pt, n = unpad(raw)
                    idx += 1
                    n_total += 1
                    fn = f'{idx:05d}_{fid}_{rname}_{md}_{ename}.bin'
                    open(os.path.join(OUT, fn), 'wb').write(raw)
                    printable = sum(32 <= c < 127 or c in (9, 10, 13) for c in raw) / len(raw)
                    rec = recognise(raw)
                    row = dict(idx=idx, file=fn, fid=fid, label=label, string=s, rep=rname, passphrase=pw.decode(), kdf=md,
                               envelope=ename, pad_valid=pt is not None, pad_len=n, printable=round(printable, 3),
                               raw_sha256=hashlib.sha256(raw).hexdigest(), recogniser=rec)
                    rows.append(row)
                    if pt is not None:
                        n_valid_pad += 1
                        log(f'PAD-VALID idx={idx} {fid} {label!r} rep={rname} kdf={md} env={ename} pad={n} printable={printable:.2f} head={raw[:40]!r}')
                    if rec:
                        hits.append(row)
                        log(f'*** KEY HIT idx={idx} {rec}')
    json.dump(rows, open(os.path.join(HERE, 'results.jsonl.json'), 'w'), indent=1)
    # chance rate of a valid PKCS#7 pad for random last block: sum_{n=1..16} 256^-n ~ 1/255
    expected = n_total / 255.0
    summary = dict(candidates=len(C), decrypts=n_total, pad_valid=n_valid_pad, expected_pad_valid_by_chance=round(expected, 2),
                   key_hits=len(hits), seconds=round(time.time() - t0, 1),
                   inputs={k: hashlib.sha256(v).hexdigest() for k, v in envs.items()},
                   code_sha256=hashlib.sha256(open(__file__, 'rb').read()).hexdigest())
    json.dump(summary, open(os.path.join(HERE, 'summary.json'), 'w'), indent=1)
    log('SUMMARY', json.dumps(summary))


if __name__ == '__main__':
    main()
