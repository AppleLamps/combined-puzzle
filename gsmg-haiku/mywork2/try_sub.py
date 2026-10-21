import sys, re, hashlib, base64
sys.path.insert(0, 'mywork'); import lib
from Crypto.Cipher import AES
cands = set()
for f in sys.argv[1:]:
    for line in open(f):
        for w in re.findall(r'\b[a-z]{63}\b', line): cands.add(w)
raw = {n: base64.b64decode(open(f'files/{n}.b64').read()) for n in ('salphaseion-short', 'terminal', 'cosmic-duality')}
def evp(pw, salt, md):
    d = b''; out = b''
    while len(out) < 48: d = hashlib.new(md, d + pw + salt).digest(); out += d
    return out[:32], out[32:48]
hits = 0; trials = 0
for c in sorted(cands):
    for pw in (hashlib.sha256(c.encode()).hexdigest().encode(), c.encode(), hashlib.sha256(c.upper().encode()).hexdigest().encode()):
        for n, r in raw.items():
            for md in ('sha256', 'md5'):
                k, iv = evp(pw, r[8:16], md); pt = AES.new(k, AES.MODE_CBC, iv).decrypt(r[16:]); trials += 1
                pad = pt[-1]
                if 1 <= pad <= 16 and pt.endswith(bytes([pad])*pad):
                    body = pt[:-pad]; pr = sum(32 <= b < 127 or b in (9, 10, 13) for b in body)/max(1, len(body))
                    if pr > 0.85: hits += 1; print('HIT', n, md, c, body[:80])
print(len(cands), 'candidates', trials, 'trials', hits, 'hits')
