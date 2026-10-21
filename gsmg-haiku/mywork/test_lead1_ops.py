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
clean_words = [re.sub(r'[^a-zA-Z0-9]', '', w) for w in words_space]
clean_words = [w for w in clean_words if w]

# 3. Get Checkerboard
cb_plain = "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE"

# 4. Containers
import base64
def load_b64(path):
    with open(path) as f:
        return base64.b64decode(f.read().replace('\n',''))

term = load_b64(r'C:\gsmg-puzzle-clean\files\terminal.b64')
salp = load_b64(r'C:\gsmg-puzzle-clean\files\salphaseion-short.b64')
cosm = load_b64(r'C:\gsmg-puzzle-clean\files\cosmic-duality.b64')
conts = [("term", term), ("salp", salp), ("cosm", cosm)]

def test_pw(pw_text):
    h = hashlib.sha256(pw_text.encode('utf-8')).hexdigest().lower()
    for name, ct in conts:
        try:
            res = openssl_aes_decrypt(ct, h)
            if res is not None:
                pr = sum(1 for b in res if 32<=b<127) / len(res)
                if pr > 0.3:
                    print(f"SUCCESS '{pw_text}' -> pr={pr:.2f}")
        except ValueError:
            pass

cands = set()

# Ops between Run 1 and Line 20
idx_0based = ""
idx_1based = ""
idx_mod = ""
word_lens = ""
sum_lens = ""
for i in range(91):
    w = clean_words[i]
    d = run1_digits[i]
    if d < len(w): idx_0based += w[d]
    if d-1 < len(w): idx_1based += w[d-1]
    idx_mod += w[d % len(w)]
    word_lens += str(len(w))
    sum_lens += str((len(w) + d) % 10)

cands.update([idx_0based, idx_1based, idx_mod, word_lens, sum_lens])

# Ops between Run 1 and Checkerboard
shift_plus = ""
shift_minus = ""
xor_val = ""
for i in range(91):
    c = cb_plain[i]
    d = run1_digits[i]
    shift_plus += chr((ord(c) - 65 + d) % 26 + 65)
    shift_minus += chr((ord(c) - 65 - d) % 26 + 65)
    xor_val += chr(ord(c) ^ d)

cands.update([shift_plus, shift_minus, xor_val])

# Test all + "matrixsumlist"
final_cands = set()
for c in cands:
    final_cands.add(c)
    final_cands.add(c.lower())
    final_cands.add(c + "matrixsumlist")
    final_cands.add(c.lower() + "matrixsumlist")

print(f"Testing {len(final_cands)} candidates...")
for c in final_cands:
    test_pw(c)
print("Done")
