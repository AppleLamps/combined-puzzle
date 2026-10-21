"""Solved-gate regression/retrodiction check. Independence depends on the supplied
generator: gen_riddle.py hardcodes known answers and is only a regression fixture.
Would a candidate-generating METHOD have opened the solved gates
from only what a solver could see at the time?

Usage: python3 retro.py 'COMMAND'
COMMAND reads a stage's visible text on stdin and prints candidates, one per line.
It is run once per solved stage (phase 2, phase 3, phase 3.2). A method passes a stage
only if one of its candidates opens that stage's container under the proven convention
(hex sha256, EVP sha256). A method that passes none should not get CPU time on the locks.
"""
import hashlib, html, os, re, subprocess, sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from rt import SOLVED, dec

K = __import__('os').environ.get('GSMG_KIT', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
page = open(K + 'phase2_choice.html', encoding='utf-8', errors='replace').read()
page = re.sub(r'<textarea.*?</textarea>', ' ', page, flags=re.S)
page = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', page)))
pt2 = dec(SOLVED['phase2'], hashlib.sha256(b'causality').hexdigest().encode())[1].decode('latin-1')
pt3 = dec(SOLVED['phase3'], b'1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5')[1][:726].decode('latin-1')
URL = 'choiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecialdessertiwroteitmyself'
STAGES = [('phase2', URL + ' ' + page),
          ('phase3', URL + ' ' + page + ' ' + pt2),
          ('phase3.2', URL + ' ' + page + ' ' + pt2 + ' ' + pt3)]

PT = {'phase2': 'e2f9dd65604a3231f8b3301724e8d713a88fffc4b6c7c4aeeb20f58a582b593a',
      'phase3': 'c4ad94559a44a927c1032cc0e024515f9510a0806a2d14458dbf4a360af9865f',
      'phase3.2': 'b82afeb86f9e50848220f9b64b744b821400308aea273a1c949b9d2d0e408a34'}
def opens(name, c):
    # the real plaintext, not a random valid pad (about 1 wrong key in 255 gives pad 1)
    p, body = dec(SOLVED[name], hashlib.sha256(c.encode('latin-1')).hexdigest().encode())
    return bool(p) and hashlib.sha256(body).hexdigest() == PT[name]

def check(cmd):
    res = {}
    for name, text in STAGES:
        out = subprocess.run(cmd, shell=True, input=text.encode('utf-8'), capture_output=True).stdout
        cands = list(dict.fromkeys(out.decode('latin-1').splitlines()))
        hit = next((c for c in cands if opens(name, c)), None)
        res[name] = (len(cands), hit)
        print('%-9s %8d candidates  %s' % (name, len(cands), 'OPENED by %r' % hit if hit else 'not opened'))
    return res

if __name__ == '__main__':
    r = check(sys.argv[1])
    passed = sum(1 for v in r.values() if v[1])
    print('PASS %d/3' % passed)
    sys.exit(0 if passed == 3 else 1)
