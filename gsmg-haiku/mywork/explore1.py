from lib import *
t = re.sub(r'\s', '', open(F + r'\salphaseion-textarea.txt').read())
r1 = t[0:91]; r3 = t[195:765]
d1 = ''.join(str(ord(c) - 96) for c in r1)
d3 = ''.join(str(ord(c) - 96) for c in r3)
print(d1); print(d3)
for d in (d1, d3):
    n = int(d)
    h = '%x' % n
    if len(h) % 2: h = '0' + h
    b = bytes.fromhex(h)
    print(len(b), b[:80], printable(b))
    # digit stats
    from collections import Counter
    print(sorted(Counter(d).items()))
