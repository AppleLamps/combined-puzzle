#!/usr/bin/env python3
"""Doc 120 s1: "select from over twenty three ciphers ... brute forcing might be required".
Every cipher this OpenSSL can run (130 names, 115 after aliases), EVP_BytesToKey with
md5 and sha256, the grounded candidate set (doc 119 tier A) as typed and as sha256 hex,
all three locks. Block modes: OpenSSL's own padding check, then the recogniser with
the true pad length (ciphertext size minus header minus plaintext size), so a pad
flag means a pad of 3 or more, as in every other harness path. Stream modes (cfb,
ofb, ctr, rc4, chacha20): the recogniser on the 80 or 1328 bytes, pad sentinel 0.
Planted controls: a block-mode and a stream-mode container encrypted under a known
candidate with two of the ciphers, restored by the sweep.

    python3 cipher_sweep.py            # writes cipher-sweep.flags
"""
import os, random, subprocess, sys, multiprocessing as mp, time, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '115')); sys.path.insert(0, os.path.join(HERE, '..', '119'))
import harness as H
from pbkdf2_sweep import tier_a

ALIAS = {'aes128': 'aes-128-cbc', 'aes192': 'aes-192-cbc', 'aes256': 'aes-256-cbc', 'aria128': 'aria-128-cbc', 'aria192': 'aria-192-cbc', 'aria256': 'aria-256-cbc',
         'bf': 'bf-cbc', 'blowfish': 'bf-cbc', 'camellia128': 'camellia-128-cbc', 'camellia192': 'camellia-192-cbc', 'camellia256': 'camellia-256-cbc',
         'cast': 'cast5-cbc', 'cast-cbc': 'cast5-cbc', 'des': 'des-cbc', 'des-ede': 'des-ede-ecb', 'des-ede3': 'des-ede3-ecb', 'des3': 'des-ede3-cbc', 'desx': 'desx-cbc',
         'rc2': 'rc2-cbc', 'rc2-128': 'rc2-cbc', 'rc2-64': 'rc2-64-cbc', 'rc2-40': 'rc2-40-cbc', 'seed': 'seed-cbc', 'sm4': 'sm4-cbc'}
def ciphers():
    out = subprocess.run(['openssl', 'enc', '-ciphers'], capture_output=True, text=True).stdout
    names = sorted({t.lstrip('-') for t in out.split() if t.startswith('-')})
    names = [n for n in names if 'wrap' not in n and 'smime' not in n and n not in ALIAS]
    return names
STREAM = ('cfb', 'ofb', 'ctr', 'rc4', 'chacha20')
def is_stream(c): return any(s in c for s in STREAM)

def dec(cipher, md, pw, path):
    r = subprocess.run(['openssl', 'enc', '-d', '-' + cipher, '-provider', 'legacy', '-provider', 'default', '-md', md, '-pass', 'pass:' + pw, '-in', path],
                       capture_output=True)
    return r.returncode, r.stdout

def work(args):
    cipher, items, files = args
    n = 0; flags = []
    sizes = {name: os.path.getsize(path) for name, path in files.items()}
    stream = is_stream(cipher)
    for lab, cand in items:
        s = cand if isinstance(cand, str) else cand.decode('latin-1')
        if '\n' in s or '\r' in s or not s or len(s) > 2000: continue
        for prof, pw in (('raw', s), ('sha', hashlib.sha256(s.encode()).hexdigest())):
            for md in ('sha256', 'md5'):
                for name, path in files.items():
                    n += 1; rc, pt = dec(cipher, md, pw, path)
                    if rc != 0 or not pt: continue
                    # block modes: OpenSSL stripped the padding; recover its length from the sizes
                    # (16-byte Salted__ header). Stream modes have no padding: sentinel 0.
                    pad = 0 if stream else sizes[name] - 16 - len(pt)
                    why = H.recognise(pt, pad)
                    if why: flags.append((cipher, prof, md, name, why, lab, s[:60], pt[:40]))
    return cipher, n, flags

if __name__ == '__main__':
    items = tier_a(); files = {n: os.path.join(HERE, f'{n}.bin') for n in ('salshort', 'terminal', 'cosmic')}
    ctl = items[7][1]; r = random.Random(120)
    open(os.path.join(HERE, 'ctl_pt.bin'), 'wb').write(r.randbytes(64))
    for c, tag in (('camellia-256-cbc', 'CONTROLblock'), ('rc4', 'CONTROLstream')):
        pt = os.path.join(HERE, 'ctl_pt.bin') if tag.endswith('block') else None
        if tag.endswith('stream'): open(os.path.join(HERE, 'ctl_txt.bin'), 'w').write('the quick brown fox jumps over the lazy dog; ' * 2); pt = os.path.join(HERE, 'ctl_txt.bin')
        subprocess.run(['openssl', 'enc', '-e', '-' + c, '-provider', 'legacy', '-provider', 'default', '-md', 'md5', '-pass', 'pass:' + ctl, '-in', pt, '-out', os.path.join(HERE, tag + '.bin')], check=True)
        files[tag] = os.path.join(HERE, tag + '.bin')
    cs = ciphers(); print(f'{len(items)} candidates x {len(cs)} ciphers x 2 forms x 2 digests x {len(files)} files', flush=True)
    t0 = time.time(); total = 0; F = []
    with mp.get_context('spawn').Pool(os.cpu_count()) as pool:
        for cipher, n, flags in pool.imap_unordered(work, [(c, items, files) for c in cs]):
            total += n; F += flags
            if flags: print(f'  {cipher}: {len(flags)} flags', flush=True)
    ctlb = [f for f in F if f[3] == 'CONTROLblock' and f[6] == ctl[:60] and f[0] == 'camellia-256-cbc']
    ctls = [f for f in F if f[3] == 'CONTROLstream' and f[6] == ctl[:60] and f[0] == 'rc4']
    real = [f for f in F if not f[3].startswith('CONTROL')]
    print(f'decrypts {total}  controls block {len(ctlb)} stream {len(ctls)}  real flags {len(real)}  {time.time()-t0:.0f}s', flush=True)
    with open(os.path.join(HERE, 'cipher-sweep.flags'), 'w') as fh:
        fh.write(f'# decrypts {total}; controls block {len(ctlb)} stream {len(ctls)}; real flags {len(real)}\n')
        for f in real: fh.write(repr(f) + '\n')
    for f in real: print('FLAG', repr(f)[:300], flush=True)
