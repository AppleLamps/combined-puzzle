"""Test candidate ANSWERS against the three locked envelopes and check any valid-padding output for the
prize keys. Offline, no brute-force generation: you supply the candidates.

  python tools/check_candidate.py --selftest
  python tools/check_candidate.py "some answer" "another answer"
  python tools/check_candidate.py --file candidates.txt          (one candidate per line, taken verbatim)
  python tools/check_candidate.py --profile raw "passphrase"     (use the text itself as the OpenSSL passphrase)

Default profile = the proven GSMG convention: passphrase = sha256(answer UTF-8) as 64 lowercase hex,
EVP_BytesToKey(SHA-256, 1 iter), AES-256-CBC, PKCS#7. Other profiles are explicit opt-ins, never fallbacks.

Reading the output: pad=1 happens ~1/256 by chance and is NOT a result. pad>=3 is ~1/16.7M (worth a look).
On the 80-byte envelopes a 64-byte plaintext gives pad=16 (chance 2^-128). Key detection runs on every
valid-padding output: raw 32-byte windows, 64-hex runs, WIF (5/K/L), and base64 runs, each derived to
compressed+uncompressed hash160 and compared with Half and Better Half.
Each candidate is also checked against the DBBI equality pattern (lead 2 in 03_OPEN_LEADS.md): if sha256(answer)
has the same repeat structure as DBBI's 64 tokens, it prints DBBI-PATTERN MATCH (chance ~2^-100; not yet seen).
"""
import argparse, base64, hashlib, re, sys
from pathlib import Path
from Crypto.Cipher import AES

DATA = Path(__file__).resolve().parents[1] / 'data'
ENVELOPES = {n: (DATA / f'locked_{n}.bin').read_bytes() for n in ('terminal_phase3_2_end', 'salphaseion_short', 'cosmic_duality')}
TARGETS = {'a9553269572a317e39f0f518cb87c1a0ee1dbae4': 'HALF 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe',
           '4bc468447fe1b048ad030a2f9a125478eabc4ed6': 'BETTER HALF 17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa'}

# --- secp256k1 (pure python, fine for checking a handful of scalars) ---------------------------------
P = 2**256 - 2**32 - 977
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
def _add(a, b):
    if a is None: return b
    if b is None: return a
    if a[0] == b[0] and (a[1] + b[1]) % P == 0: return None
    s = (3 * a[0] * a[0] * pow(2 * a[1], -1, P) if a == b else (b[1] - a[1]) * pow(b[0] - a[0], -1, P)) % P
    x = (s * s - a[0] - b[0]) % P
    return x, (s * (a[0] - x) - a[1]) % P
def _mul(k):
    r, c = None, G
    while k:
        if k & 1: r = _add(r, c)
        c = _add(c, c); k >>= 1
    return r
h160 = lambda b: hashlib.new('ripemd160', hashlib.sha256(b).digest()).hexdigest()
B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def scalar_hits(k):
    if not 1 <= k < N: return []
    x, y = _mul(k)
    forms = {'uncompressed': b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big'),
             'compressed': bytes([2 + (y & 1)]) + x.to_bytes(32, 'big')}
    return [f'{TARGETS[h160(pub)]} ({form})' for form, pub in forms.items() if h160(pub) in TARGETS]

def wif_scalar(s):
    n = 0
    for ch in s: n = n * 58 + B58.index(ch)
    raw = n.to_bytes(len(s) * 6 // 8 + 2, 'big').lstrip(b'\0')
    body, chk = raw[:-4], raw[-4:]
    if hashlib.sha256(hashlib.sha256(body).digest()).digest()[:4] != chk or body[:1] != b'\x80': return None
    if len(body) == 33 or (len(body) == 34 and body[-1] == 1): return int.from_bytes(body[1:33], 'big')
    return None

def find_keys(pt):
    """Every key-shaped reading of a plaintext -> list of (description, hits)."""
    found = []
    for i in range(0, max(0, len(pt) - 31)):
        k = int.from_bytes(pt[i:i + 32], 'big')
        hits = scalar_hits(k)
        if hits: found.append((f'raw32@{i}', hits))
    text = pt.decode('latin1')
    for m in re.finditer(r'(?<![0-9a-fA-F])[0-9a-fA-F]{64}(?![0-9a-fA-F])', text):
        hits = scalar_hits(int(m.group(), 16)); found.append((f'hex64@{m.start()}', hits))
    for m in re.finditer(r'[5KL][1-9A-HJ-NP-Za-km-z]{50,51}', text):
        k = wif_scalar(m.group())
        if k is not None: found.append((f'WIF@{m.start()}', scalar_hits(k)))
    for m in re.finditer(r'[A-Za-z0-9+/]{43,}={0,2}', text):
        try: raw = base64.b64decode(m.group() + '=' * (-len(m.group()) % 4))
        except Exception: continue
        if len(raw) == 32: found.append((f'base64@{m.start()}', scalar_hits(int.from_bytes(raw, 'big'))))
    return found

# --- envelopes -----------------------------------------------------------------------------------------
def evp(pw, salt, md):
    d = prev = b''
    while len(d) < 48:
        prev = md(prev + pw + salt).digest(); d += prev
    return d[:32], d[32:48]

PROFILES = {
    'gsmg': lambda a: (hashlib.sha256(a.encode()).hexdigest().encode(), hashlib.sha256),
    'raw': lambda a: (a.encode(), hashlib.sha256),
    'gsmg-md5': lambda a: (hashlib.sha256(a.encode()).hexdigest().encode(), hashlib.md5),
    'raw-md5': lambda a: (a.encode(), hashlib.md5),
}

def try_envelope(raw, answer, profile):
    pw, md = PROFILES[profile](answer)
    key, iv = evp(pw, raw[8:16], md)
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(raw[16:])
    n = pt[-1]
    return (n, pt[:-n]) if 1 <= n <= 16 and pt[-n:] == bytes([n]) * n else (0, None)

DBBI_PATTERN = '01234556728966286abc61c88b48de3086dd501d5557d6bab5605233df7bbb96'
def eq_pattern(h):
    first = {}
    return ''.join('0123456789abcdef'[first.setdefault(c, len(first))] if len(first) < 16 or c in first else '?' for c in h)

def check(answer, profile, quiet=False):
    notable = False
    if eq_pattern(hashlib.sha256(answer.encode()).hexdigest()) == DBBI_PATTERN:
        print(f'[DBBI-PATTERN MATCH] sha256({answer!r}) has the DBBI token repeat structure'); notable = True
    for name, raw in ENVELOPES.items():
        pad, pt = try_envelope(raw, answer, profile)
        if not pad: continue
        keys = find_keys(pt)
        hits = [(d, h) for d, h in keys if h]
        level = 'KEY MATCH' if hits else ('STRONG pad' if pad >= 3 else 'chance-level pad')
        notable |= bool(hits) or pad >= 3
        if pad >= 3 or hits or not quiet:
            print(f'[{level}] {name} pad={pad} len={len(pt)} answer={answer!r} profile={profile}')
            print('   plaintext[:80] =', pt[:80])
            for d, h in hits: print('   ', d, '->', h)
            if hits or pad >= 3: (DATA.parent / 'CANDIDATE_HIT.bin').write_bytes(pt)
    return notable

def selftest():
    # 1. envelope code opens the real Phase 3.2 envelope (from data/phase3_plaintext.bin)
    p3 = (DATA / 'phase3_plaintext.bin').read_bytes()
    env = base64.b64decode(re.sub(rb'\s+', b'', p3[p3.index(b'U2FsdGVk'):]))
    pad, pt = try_envelope(env, 'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple', 'gsmg')
    assert pad == 10 and len(pt) == 2422, 'envelope self-test failed'
    # 2. hash160 code reproduces Half's hash160 from its published public key
    pub = bytes.fromhex('04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a4649c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559')
    assert h160(pub) == 'a9553269572a317e39f0f518cb87c1a0ee1dbae4'
    # 3. EC + WIF + detectors on a known key (k=1) with temporary targets
    x, y = _mul(1)
    assert h160(b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')) == '91b24bf9f5288532960ac687abb035127b1d28a5'  # 1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm
    assert wif_scalar('5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf') == 1
    TARGETS['91b24bf9f5288532960ac687abb035127b1d28a5'] = 'TEST k=1'
    sample = b'x' * 5 + (1).to_bytes(32, 'big') + b' 5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf ' + b'0' * 63 + b'1'
    kinds = {d.split('@')[0] for d, h in find_keys(sample) if h}
    del TARGETS['91b24bf9f5288532960ac687abb035127b1d28a5']
    assert kinds == {'raw32', 'WIF', 'hex64'}, kinds
    # 4. equality-pattern helper
    assert eq_pattern('0123456789abcdef' * 4) == '0123456789abcdef' * 4 and eq_pattern('ba' * 32) == '01' * 32
    print('SELFTEST PASSED (envelope open, hash160 of Half pubkey, EC k=1, WIF, raw/hex detectors, pattern helper)')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('answers', nargs='*')
    ap.add_argument('--file')
    ap.add_argument('--profile', choices=PROFILES, default='gsmg')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--quiet', action='store_true', help='only print pad>=3 or key matches')
    a = ap.parse_args()
    if a.selftest: selftest(); sys.exit(0)
    cands = list(a.answers) + (Path(a.file).read_text(encoding='utf-8').splitlines() if a.file else [])
    if not cands: ap.error('no candidates')
    n = sum(check(c, a.profile, a.quiet) for c in cands)
    print(f'{len(cands)} candidates x {len(ENVELOPES)} envelopes, profile={a.profile}: {n} notable')
