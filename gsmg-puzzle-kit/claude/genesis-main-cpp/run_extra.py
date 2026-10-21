"""Planted control for this candidate file, plus the newline-bearing dump forms.
A container is made with the openssl CLI from a candidate read out of cands.txt;
it must be recovered by rt.dec/judge before any null below counts."""
import hashlib, subprocess, sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'riddle-method')); import rt
sys.argv = ['gen.py', 'main_v0.3.10.cpp', 'main_v0.1.0.cpp']
cands = [l.rstrip('\n') for l in open('cands.txt') if l.strip() and not l.startswith('#')]
pick = random.Random(35).choice(cands)
pw = hashlib.sha256(pick.encode()).hexdigest()
msg = os.urandom(300)  # not printable: recogniser must work on pad alone
ct = subprocess.run(['openssl', 'enc', '-aes-256-cbc', '-md', 'sha256', '-salt', '-pass', 'pass:' + pw],
                    input=msg, capture_output=True, check=True).stdout
hit = False
for x in cands:
    p, body = rt.dec(ct, hashlib.sha256(x.encode()).hexdigest().encode())
    if p and body == msg and rt.judge(body, p): hit = x
assert hit == pick, 'planted control did not fire'
print('planted control fired: openssl container keyed by candidate %r recovered from cands.txt' % pick[:40])
ns = {}; exec(open('gen.py').read().split("print('\\n'.join")[0], ns)
t, p, fl = rt.run(ns['MULTI'])
print('multiline forms %d, decrypts %d, valid pads %d, flags %d' % (len(ns['MULTI']), t, p, len(fl)))
for f in fl: print('FLAG', *f, sep='\t')
