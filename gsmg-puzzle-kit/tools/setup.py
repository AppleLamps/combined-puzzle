#!/usr/bin/env python3
"""Rebuild the working files the other tools expect, from the Project's own files.

Usage:   python3 setup.py [SRC] [DEST]
  SRC   folder holding the Project files (default '.'). It needs
        phase2.b64 phase3.b64 terminal.b64 salphaseion-short.b64 cosmic-duality.b64
        salphaseion-textarea.txt architect_letters_1539.txt puzzle.png
        and the dossier (GSMG-PUZZLE-DOSSIER.md, here or under claude/).
  DEST  folder to build in (default '.'). Put the tools/ scripts there too.

Creates in DEST:
  b64/phase2.b64 b64/terminal.b64 b64/short.b64 b64/cosmic.b64
  ta.txt          the 1,075-character SalPhaseIon textarea
  pt2.bin         phase-2 plaintext (648 bytes), opened with the answer 'causality'
  pt3.bin         phase-3 plaintext (4,090 bytes), opened with the seven-part answer of dossier 3.3
  pt32.bin        phase-3.2 plaintext (2,422 bytes), opened with the phase-3.2 answer
  architect.txt   the 1,539-letter Architect text (cp273, reciprocal Beaufort, key THEMATRIXHASYOU)
  puzzle.png      copy of the poster
  words.txt       234k-word list from the english-words package (pip install english-words),
                  used only by n1.py, n2.py and seg.py
Every step checks its result against the hash or length the dossier records (section 13).
"""
import base64, hashlib, os, re, shutil, sys
from Crypto.Cipher import AES

SRC = sys.argv[1] if len(sys.argv) > 1 else '.'
DEST = sys.argv[2] if len(sys.argv) > 2 else '.'
os.makedirs(os.path.join(DEST, 'b64'), exist_ok=True)


def find(*names):
    for n in names:
        for base in (SRC, os.path.join(SRC, 'claude')):
            p = os.path.join(base, n)
            if os.path.exists(p):
                return p
    sys.exit('missing file: ' + ' or '.join(names))


def evp(pw, salt):
    d = b''
    prev = b''
    while len(d) < 48:
        prev = hashlib.sha256(prev + pw + salt).digest()
        d += prev
    return d[:32], d[32:48]


def decrypt(raw, answer):
    pw = hashlib.sha256(answer.encode()).hexdigest().encode()
    k, iv = evp(pw, raw[8:16])
    pt = AES.new(k, AES.MODE_CBC, iv).decrypt(raw[16:])
    p = pt[-1]
    return pt[:-p] if 1 <= p <= 16 and pt[-p:] == bytes([p]) * p else None


def sha(b):
    return hashlib.sha256(b).hexdigest()


def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        sys.exit(1)


def w(name, data):
    with open(os.path.join(DEST, name), 'wb' if isinstance(data, bytes) else 'w') as f:
        f.write(data)


# textarea and container files
ta = open(find('salphaseion-textarea.txt')).read().strip()
ok('textarea is 1,075 characters', len(ta) == 1075)
w('ta.txt', ta + '\n')
for src, dst in (('phase2.b64', 'phase2'), ('terminal.b64', 'terminal'),
                 ('salphaseion-short.b64', 'short'), ('cosmic-duality.b64', 'cosmic')):
    w('b64/%s.b64' % dst, open(find(src)).read().replace('\n', '').strip() + '\n')
sizes = {n: len(base64.b64decode(open(os.path.join(DEST, 'b64', n + '.b64')).read())) for n in ('terminal', 'short', 'cosmic')}
ok('container sizes 96, 96, 1344', sizes == {'terminal': 96, 'short': 96, 'cosmic': 1344})
expect = {'terminal': '291dfd6f3e759ec2e272b35a00c24907da70c3e7a9291b4c13605c7b0b4f3de9',
          'short': '9e2831e1b34b5f34796df47ccaf6530d48d371c61a6bff84d60db1064fa7a258',
          'cosmic': 'b18950551a4dd0cb8a9378f0906ba18c03a15f0ee83eb98c6bc90165c5f79805'}
for n, h in expect.items():
    ok('container %s sha256 matches dossier 6.5' % n, sha(base64.b64decode(open(os.path.join(DEST, 'b64', n + '.b64')).read())) == h)

# phase 2
raw2 = base64.b64decode(open(os.path.join(DEST, 'b64', 'phase2.b64')).read())
pt2 = decrypt(raw2, 'causality')
ok('phase-2 plaintext, 648 bytes, sha e2f9dd65', pt2 is not None and len(pt2) == 648 and sha(pt2).startswith('e2f9dd65'))
w('pt2.bin', pt2)

# phase 3 and 3.2 (the seven-part answer is read from dossier section 3.3)
doss = open(find('GSMG-PUZZLE-DOSSIER.md')).read()
m = re.search(r'The answer is the plain concatenation of seven parts:\n\n(.*?)\nPart 6 is', doss, re.S)
parts = [re.match(r'\d\. `(.*)`$', l).group(1) for l in m.group(1).split('\n') if re.match(r'\d\. `', l)]
ok('seven answer parts found', len(parts) == 7)
ans3 = ''.join(parts)
raw3 = base64.b64decode(open(find('phase3.b64')).read().strip())
pt3 = decrypt(raw3, ans3)
ok('phase-3 plaintext, 4,090 bytes, sha c4ad9455', pt3 is not None and len(pt3) == 4090 and sha(pt3).startswith('c4ad9455'))
w('pt3.bin', pt3)
i = pt3.find(b'U2FsdGVkX1')
raw32 = base64.b64decode(pt3[i:].decode().strip())
ans32 = 'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple'
ok('phase-3.2 answer appears in the dossier', ans32 in doss)
pt32 = decrypt(raw32, ans32)
ok('phase-3.2 plaintext, 2,422 bytes, sha b82afeb8', pt32 is not None and len(pt32) == 2422 and sha(pt32).startswith('b82afeb8'))
w('pt32.bin', pt32)

# the Architect text
c = pt32[447:1986].decode('latin-1').encode('cp273')
key = 'THEMATRIXHASYOU'
cs = [b - 97 for b in c]
ok('cp273 bytes are lowercase letters', all(0 <= x < 26 for x in cs))
arch = ''.join(chr(97 + ((ord(key[i % len(key)]) - 65) - cs[i]) % 26) for i in range(len(cs)))
ok('Architect text: 1,539 letters, PRIVATEKEY at 479', len(arch) == 1539 and arch[479:489] == 'privatekey')
ok('matches architect_letters_1539.txt', arch.upper() == open(find('architect_letters_1539.txt')).read().strip().upper())
w('architect.txt', arch)

src_png, dst_png = find('puzzle.png'), os.path.join(DEST, 'puzzle.png')
if not (os.path.exists(dst_png) and os.path.samefile(src_png, dst_png)):
    shutil.copy(src_png, dst_png)

# word list (only for the English-fit tools)
try:
    from english_words import get_english_words_set
    words = sorted(w for w in get_english_words_set(['web2'], lower=True) if w.isalpha())
    w('words.txt', '\n'.join(words) + '\n')
    print('words.txt written,', len(words), 'words')
except Exception as e:
    print('words.txt not written (pip install english-words):', e)
print('setup done')
