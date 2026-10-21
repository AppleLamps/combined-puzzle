"""Generic data-derived method, the shape of lw_words / subs / book sweeps:
every contiguous run of 1-12 words (lowercase, letters and digits only, joined with no
spaces), plus every letter substring of length 4-40."""
import re, sys
t = sys.stdin.buffer.read().decode('utf-8','replace')
w = [re.sub(r'[^a-z0-9]', '', x.lower()) for x in t.split()]
w = [x for x in w if x]
out = set()
for i in range(len(w)):
    for k in range(1, 13):
        if i + k <= len(w): out.add(''.join(w[i:i + k]))
L = re.sub(r'[^a-z]', '', t.lower())
for i in range(len(L)):
    for k in range(4, 41):
        if i + k <= len(L): out.add(L[i:i + k])
sys.stdout.write('\n'.join(out))
