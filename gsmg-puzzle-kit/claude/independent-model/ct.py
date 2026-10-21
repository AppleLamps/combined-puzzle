"""Convention tester: few candidates, every locked container, a cipher x KDF matrix.

Questions the convention (AES-256-CBC, EVP_BytesToKey) for the three locked containers,
whose pages never name their cipher or KDF (phase 2, 3 and 3.2 did).

Usage: python3 ct.py FILE [FILE...]   one candidate per line; '#' lines are notes
       python3 ct.py --controls       openssl-made planted controls only
Forms: raw x, hex(sha256 x) [canonical], hex(sha256(sha256 x)), hex(sha256(hex sha256 x))
KDFs:  EVP md5 / sha1 / sha256 / sha512 (1 iter), PBKDF2-HMAC-SHA256 10000 (openssl -pbkdf2 default)
Ciphers: AES-128/192/256 CBC+ECB, Camellia-128/192/256 CBC, SEED, SM4, 3DES, Blowfish, CAST5 (CBC)
"""
import base64, hashlib, os, subprocess, sys, warnings, tempfile
warnings.filterwarnings('ignore')
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms as A, modes
from cryptography.hazmat.decrepit.ciphers import algorithms as DA
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'riddle-method'))
import rt  # win(), keyhit(), judge(), h160

D = os.environ.get('GSMG_KIT', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
def load(n): return base64.b64decode(''.join(open(D + n).read().split()))
LOCKED = {'terminal': load('terminal.b64'), 'short': load('salphaseion-short.b64'),
          'cosmic': load('cosmic-duality.b64')}

# name: (algorithm factory, key len, iv len (0 = ECB), block)
CIPHERS = {
    'aes-128-cbc': (A.AES, 16, 16, 16), 'aes-192-cbc': (A.AES, 24, 16, 16), 'aes-256-cbc': (A.AES, 32, 16, 16),
    'aes-128-ecb': (A.AES, 16, 0, 16), 'aes-192-ecb': (A.AES, 24, 0, 16), 'aes-256-ecb': (A.AES, 32, 0, 16),
    'camellia-128-cbc': (DA.Camellia, 16, 16, 16), 'camellia-192-cbc': (DA.Camellia, 24, 16, 16),
    'camellia-256-cbc': (DA.Camellia, 32, 16, 16), 'seed-cbc': (DA.SEED, 16, 16, 16), 'sm4-cbc': (A.SM4, 16, 16, 16),
    'des-ede3-cbc': (DA.TripleDES, 24, 8, 8), 'bf-cbc': (DA.Blowfish, 16, 8, 8), 'cast5-cbc': (DA.CAST5, 16, 8, 8),
}
KDFS = ['evp-md5', 'evp-sha1', 'evp-sha256', 'evp-sha512', 'pbkdf2-sha256-10000']

def derive(kdf, pw, salt, n=56):
    if kdf.startswith('evp-'):
        md = kdf[4:]; d = b''; prev = b''
        while len(d) < n:
            prev = hashlib.new(md, prev + pw + salt).digest(); d += prev
        return d[:n]
    return hashlib.pbkdf2_hmac('sha256', pw, salt, 10000, n)

def tail_pad(raw, cname, kiv):
    alg, kl, il, bs = CIPHERS[cname]
    key = kiv[:kl]; ct = raw[16:]
    if il:
        prev = kiv[kl:kl + il] if len(ct) == bs else ct[-2 * bs:-bs]
        last = Cipher(alg(key), modes.ECB()).decryptor().update(ct[-bs:])
        last = bytes(a ^ b for a, b in zip(last, prev))
    else:
        last = Cipher(alg(key), modes.ECB()).decryptor().update(ct[-bs:])
    p = last[-1]
    return p if 1 <= p <= bs and last[-p:] == bytes([p]) * p else 0

def full(raw, cname, kiv):
    alg, kl, il, bs = CIPHERS[cname]
    m = modes.CBC(kiv[kl:kl + il]) if il else modes.ECB()
    pt = Cipher(alg(kiv[:kl]), m).decryptor().update(raw[16:])
    return pt[:-pt[-1]]

def forms(x):
    b = x.encode(); h = hashlib.sha256(b)
    yield 'raw', b
    yield 'hex', h.hexdigest().encode()
    yield 'dblhex', hashlib.sha256(h.digest()).hexdigest().encode()
    yield 'hexofhex', hashlib.sha256(h.hexdigest().encode()).hexdigest().encode()

def run(cands, locked=LOCKED, quiet=False):
    tests = pads = 0; flags = rt.AuditResults()
    for x in cands:
        if rt.win(x): flags.append(('WIN', 'scalar', '', '', x))
        for fname, pw in forms(x):
            for kdf in KDFS:
                for cn, raw in locked.items():
                    kiv = derive(kdf, pw, raw[8:16])
                    for cname in CIPHERS:
                        if (len(raw) - 16) % CIPHERS[cname][3]: continue
                        tests += 1
                        p = tail_pad(raw, cname, kiv)
                        if p:
                            pads += 1
                            body = full(raw, cname, kiv)
                            r = rt.judge(body, p) if body else ''
                            flags.append((cn, cname, kdf, fname, r or 'unranked', x, body, p))
    return tests, pads, flags

def controls():
    """Encrypt planted plaintexts with the openssl CLI and require that run() flags each one."""
    rt.controls()
    secret = 'plantedcontrolanswer'
    pwhex = hashlib.sha256(secret.encode()).hexdigest()
    plain = hashlib.sha256(b'plantedplaintext').hexdigest().encode()  # 64 hex chars -> 80-byte container
    cases = [('aes-128-cbc', ['-md', 'md5']), ('camellia-256-cbc', ['-md', 'sha256']),
             ('des-ede3-cbc', ['-md', 'sha1']), ('aes-256-ecb', ['-md', 'sha512']),
             ('aes-256-cbc', ['-pbkdf2']), ('sm4-cbc', ['-pbkdf2']), ('aes-192-cbc', ['-md', 'sha256'])]
    ok = 0
    with tempfile.TemporaryDirectory() as td:
        pf = os.path.join(td, 'p'); open(pf, 'wb').write(plain)
        for cname, extra in cases:
            out = subprocess.run(['openssl', 'enc', '-' + cname, '-salt', '-in', pf, '-pass', 'pass:' + pwhex] + extra,
                                 capture_output=True).stdout
            assert out[:8] == b'Salted__', (cname, out[:40])
            t, p, fl = run([secret], {'ctl': out})
            expected_kdf = 'pbkdf2-sha256-10000' if '-pbkdf2' in extra else 'evp-' + extra[1]
            hit = [f for f in fl if f[1] == cname and f[2] == expected_kdf
                   and f[3] == 'hex' and f[6] == plain]
            assert hit and hit[0][6] == plain, (cname, extra, fl)
            ok += 1
    # the bf/cast5/seed paths, which openssl 3 keeps in the legacy provider, are checked by self-encryption
    for cname in ('bf-cbc', 'cast5-cbc', 'seed-cbc', 'camellia-128-cbc'):
        alg, kl, il, bs = CIPHERS[cname]
        salt = os.urandom(8); kiv = derive('evp-sha256', pwhex.encode(), salt)
        padn = bs - len(plain) % bs
        e = Cipher(alg(kiv[:kl]), modes.CBC(kiv[kl:kl + il])).encryptor().update(plain + bytes([padn]) * padn)
        t, p, fl = run([secret], {'ctl': b'Salted__' + salt + e})
        assert any(f[1] == cname and f[3] == 'hex' and f[6] == plain for f in fl), cname
        ok += 1
    return ok

if __name__ == '__main__':
    n = controls()
    print('controls fired: key1 + phase 2/3/3.2 (rt), %d planted containers (7 made by openssl CLI) recovered' % n)
    if sys.argv[1:] == ['--controls']: sys.exit()
    cands = []
    for f in sys.argv[1:]:
        for l in open(f, encoding='utf-8'):
            l = l.rstrip('\n')
            if l and not l.startswith('#'): cands.append(l)
    cands = list(dict.fromkeys(cands))
    t, p, fl = run(cands)
    exp = t * (15 / 16 / 255)  # approx share of valid pads over 16- and 8-byte blocks
    print('candidates %d, decrypts %d, valid pads %d (expected ~%.0f)' % (len(cands), t, p, t / 255.))
    fl.report()
    fl.emit()

    sys.exit(2 if fl.omitted else 0)
