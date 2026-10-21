import hashlib
import sys

sys.path.append(r"C:\gsmg-puzzle-clean\work")
from openssl_decrypt import decrypt_openssl_aes256cbc as openssl_aes_decrypt

cb_plain = "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE"

import base64
def load_b64(path):
    with open(path) as f:
        return base64.b64decode(f.read().replace('\n',''))

conts = [
    ("term", load_b64(r'C:\gsmg-puzzle-clean\files\terminal.b64')),
    ("salp", load_b64(r'C:\gsmg-puzzle-clean\files\salphaseion-short.b64')),
    ("cosm", load_b64(r'C:\gsmg-puzzle-clean\files\cosmic-duality.b64'))
]

def test_pw(pw_text, desc):
    h = hashlib.sha256(pw_text.encode('utf-8')).hexdigest().lower()
    for name, ct in conts:
        try:
            res = openssl_aes_decrypt(ct, h)
            if res is not None:
                pr = sum(1 for b in res if 32<=b<127) / len(res)
                if pr > 0.3:
                    print(f"[{name}] SUCCESS '{pw_text}' ({desc}) -> pr={pr:.2f} text: {res[:50]}")
        except ValueError:
            pass

def transpose(text, key):
    cols = sorted(list(enumerate(key)), key=lambda x: x[1])
    grid = [''] * len(key)
    for i, c in enumerate(text):
        grid[i % len(key)] += c
    out = ''
    for idx, _ in cols:
        out += grid[idx]
    return out

keys = [
    "FUBCDORACLESAD",
    "THINGKYMVPSSAD",
    "FUBCDORACLE",
    "THINGKYMVPS",
    "SADBOARD"
]

cands = set()
for k in keys:
    res = transpose(cb_plain, k)
    cands.add(res)
    cands.add(res.lower())
    cands.add(res + "matrixsumlist")
    cands.add(res.lower() + "matrixsumlist")
    
print(f"Testing {len(cands)} candidates...")
for c in cands:
    test_pw(c, "transposition")
print("Done")
