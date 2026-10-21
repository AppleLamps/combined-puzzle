import hashlib
import sys

sys.path.append(r"C:\gsmg-puzzle-clean\work")
from openssl_decrypt import decrypt_openssl_aes256cbc as openssl_aes_decrypt

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

run1 = 'dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe'
digits = [ord(c)-ord('a')+1 for c in run1]
pairs = []
i = 0
while i < len(digits):
    d = digits[i]
    if d in [2, 5]:
        if i + 1 < len(digits):
            pairs.append(str(d) + str(digits[i+1]))
            i += 2
        else:
            pairs.append(str(d))
            i += 1
    else:
        pairs.append(str(d))
        i += 1

slots = ['1', '3', '4', '6', '7', '8', '9',
         '21', '22', '23', '24', '25', '26', '27', '28', '29',
         '51', '52', '53', '54', '55', '56', '57', '58', '59']

alpha_str = "FUBCDORACLESADTHINGKYMVPSJQWXZ"
alpha = []
for c in alpha_str:
    if c not in alpha:
        alpha.append(c)

cands = set()

for drop in ['Z', 'J', 'X', 'Q', 'W', '']:
    curr_alpha = [c for c in alpha if c != drop]
    if len(curr_alpha) > 25:
        curr_alpha = curr_alpha[:25]
    
    mapping = dict(zip(slots, curr_alpha))
    
    try:
        dec = "".join(mapping[p] for p in pairs)
        cands.add(dec)
        cands.add(dec.lower())
        cands.add(dec + "matrixsumlist")
        cands.add(dec.lower() + "matrixsumlist")
    except KeyError:
        pass

print(f"Testing {len(cands)} candidates...")
for c in cands:
    test_pw(c, "checkerboard")
print("Done")
