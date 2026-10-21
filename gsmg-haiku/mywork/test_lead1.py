import re
import hashlib
import sys
import os

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
print(f"Number of clean words in Line 20: {len(clean_words)}")

if len(clean_words) != 91:
    print(f"Warning: expected 91 words, got {len(clean_words)}")

# 3. Get Checkerboard plaintext
cb_plain = "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE"
print(f"Checkerboard length: {len(cb_plain)}")

# 4. Containers to test
import base64
def load_b64(path):
    with open(path) as f:
        return base64.b64decode(f.read().replace('\n',''))

term = load_b64(r'C:\gsmg-puzzle-clean\files\terminal.b64')
salp = load_b64(r'C:\gsmg-puzzle-clean\files\salphaseion-short.b64')
cosm = load_b64(r'C:\gsmg-puzzle-clean\files\cosmic-duality.b64')

conts = [("term", term), ("salp", salp), ("cosm", cosm)]

def test_pw(pw_text, desc):
    h = hashlib.sha256(pw_text.encode('utf-8')).hexdigest().lower()
    for name, ct in conts:
        try:
            res = openssl_aes_decrypt(ct, h)
            if res is not None:
                pr = sum(1 for b in res if 32<=b<127) / len(res)
                if pr > 0.5:
                    print(f"[{name}] SUCCESS '{pw_text}' ({desc}) -> pr={pr:.2f} text: {res[:50]}")
        except ValueError:
            pass

# Idea A: $i$-th digit selects the $d$-th letter of the $i$-th word
cands_A = []
idx1 = ""; idx2 = ""; idx3 = ""; idx4 = ""
for i in range(min(91, len(clean_words))):
    w = clean_words[i]
    d = run1_digits[i]
    # 1-based indexing
    idx1 += w[d-1] if d <= len(w) else w[-1]
    idx2 += w[(d-1) % len(w)]
    # from end
    idx3 += w[-d] if d <= len(w) else w[0]
    idx4 += w[-((d-1)%len(w)) - 1]

cands_A.extend([idx1, idx2, idx3, idx4])

# Idea B: checkerboard + digit
cands_B = []
sh1 = ""; sh2 = ""
for i in range(91):
    c = cb_plain[i]
    d = run1_digits[i]
    sh1 += chr((ord(c) - 65 + d) % 26 + 65)
    sh2 += chr((ord(c) - 65 - d) % 26 + 65)

cands_B.extend([sh1, sh2])

all_cands = []
for c in cands_A + cands_B:
    all_cands.append((c, "direct"))
    all_cands.append((c.lower(), "lower"))
    all_cands.append((c + "matrixsumlist", "direct+msl"))
    all_cands.append((c.lower() + "matrixsumlist", "lower+msl"))

print(f"Testing {len(all_cands)} derived candidates...")
for c, d in all_cands:
    test_pw(c, d)

print("Done lead 1")
