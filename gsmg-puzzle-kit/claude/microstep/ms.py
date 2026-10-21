"""Microstep form tester: the ledger's answers hashed the way a terminal hashes them.

Usage: python3 ms.py FILE [FILE...]   one candidate per line; '#' lines are notes
Reading: the password was made with `echo ANSWER | sha256sum` (or the Windows cmd
equivalent), so the hashed input carries the line ending that Enter adds.
Suffixes: '\\n' (Unix echo), '\\r\\n' (Windows), ' \\r\\n' (cmd `echo x | ...`).
Forms per suffix: hex(sha256(x+s)) [as -pass pass:HEX], raw sha256(x+s), and
hex(sha256(hex(sha256(x+s))+s)) (the hex piped back through echo); EVP sha256 and md5.
Every locked container plus the three solved ones; rt.judge on every valid pad; the win
test on sha256(x+s) and its double hash.
Controls: rt.controls(), plus planted containers made by the openssl CLI with
`printf 'plantedmicrostep\\n' | sha256sum`-style passwords, one per suffix.
"""
import base64, hashlib, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'riddle-method'))
import rt

SUFFIXES = {'lf': '\n', 'crlf': '\r\n', 'spcrlf': ' \r\n'}

def forms(x):
    for sn, s in SUFFIXES.items():
        b = (x + s).encode()
        h = hashlib.sha256(b)
        yield sn + ':hex', h.hexdigest().encode()
        yield sn + ':raw', h.digest()
        yield sn + ':hexecho', hashlib.sha256((h.hexdigest() + s).encode()).hexdigest().encode()

def planted():
    out = {}
    for sn, s in SUFFIXES.items():
        pw = hashlib.sha256(('plantedmicrostep' + s).encode()).hexdigest()
        with tempfile.NamedTemporaryFile('wb', delete=False) as f:
            f.write(hashlib.sha256(b'plantedmicrostepplaintext').hexdigest().encode()); fn = f.name
        r = subprocess.run(['openssl', 'enc', '-aes-256-cbc', '-md', 'sha256', '-salt', '-in', fn,
                            '-pass', 'pass:' + pw], capture_output=True, check=True)
        out['plant-' + sn] = r.stdout
        os.unlink(fn)
    return out

def run(cands, extra):
    flags = rt.AuditResults(); tests = pads = 0
    conts = {**rt.LOCKED, **rt.SOLVED, **extra}
    for x in cands:
        for sn, s in SUFFIXES.items():
            if rt.win(x + s): flags.append(('WIN', 'scalar', sn, '', x))
        for fname, pw in forms(x):
            for md in ('sha256', 'md5'):
                for cn, raw in conts.items():
                    p, body = rt.dec(raw, pw, md); tests += 1
                    if p:
                        pads += 1
                        r = rt.judge(body, p) if not cn.startswith('plant') else ('opened' if body == hashlib.sha256(b'plantedmicrostepplaintext').hexdigest().encode() else '')
                        flags.append((cn, fname, md, r or 'unranked', x, p, body.hex()))
    return tests, pads, flags

if __name__ == '__main__':
    rt.controls()
    pl = planted()
    t, p, fl = run(['plantedmicrostep'], pl)
    opened = sorted({f[0] for f in fl if f[0].startswith('plant')
                     and f[1] == f[0][len('plant-'):] + ':hex'
                     and f[2] == 'sha256' and f[3] == 'opened'})
    assert opened == sorted(pl), opened
    print('controls fired: key1, phase2/3/3.2 open; planted openssl containers opened for', ', '.join(opened))
    cands = []
    for f in sys.argv[1:]:
        for l in open(f, encoding='utf-8'):
            l = l.rstrip('\n')
            if l and not l.startswith('#'): cands.append(l)
    cands = list(dict.fromkeys(cands))
    t, p, fl = run(cands, {})
    print('candidates %d, decrypts %d, valid pads %d (expected ~%.1f)' % (len(cands), t, p, t / 255.))
    fl.report()
    fl.emit()

    sys.exit(2 if fl.omitted else 0)
