import re
import hashlib
import sys

sys.path.append(r"C:\gsmg-puzzle-clean\work")
from openssl_decrypt import decrypt_openssl_aes256cbc as openssl_aes_decrypt

# 1. Get Run 1 digits
with open(r'C:\gsmg-puzzle-clean\files\salphaseion-textarea.txt') as f:
    text = f.read()
run1_chars = text.split('z')[0][:91]
run1_digits = [ord(c) - ord('a') + 1 for c in run1_chars]

# 2. Get Line 20 words
with open(r'C:\gsmg-puzzle-clean\matrix-reloaded.txt') as f:
    lines = [l.strip() for l in f if l.strip()]
line20_text = lines[20].split('Architect: ')[1]
words_space = line20_text.split()
clean_words = [re.sub(r'[^a-zA-Z]', '', w) for w in words_space]
clean_words = [w for w in clean_words if w]
word_lens = [len(w) for w in clean_words]

# 3. Get Checkerboard
cb_plain = "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE"
cb_vals = [ord(c) - 64 for c in cb_plain]

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

cands = set()

# element-wise sums
sum_1 = [run1_digits[i] + word_lens[i] for i in range(91)]
sum_2 = [run1_digits[i] + cb_vals[i] for i in range(91)]
sum_3 = [word_lens[i] + cb_vals[i] for i in range(91)]
sum_4 = [run1_digits[i] + word_lens[i] + cb_vals[i] for i in range(91)]

for s in [sum_1, sum_2, sum_3, sum_4]:
    cands.add("".join(map(str, s)))
    cands.add(",".join(map(str, s)))
    cands.add("".join(chr(x % 26 + 65) for x in s))
    cands.add("".join(chr((x-1) % 26 + 65) for x in s))

final_cands = set()
for c in cands:
    final_cands.add(c)
    final_cands.add(c.lower())
    final_cands.add(c + "matrixsumlist")
    final_cands.add(c.lower() + "matrixsumlist")

print(f"Testing {len(final_cands)} matrix sum candidates...")
for c in final_cands:
    test_pw(c, "matrix sum")
print("Done")
