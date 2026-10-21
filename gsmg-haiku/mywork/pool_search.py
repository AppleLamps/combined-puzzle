"""Historical password search. Importing this module does not run it."""
import time
try:
    from .candidate_pool import build_pool, trans
    from .lib import load, evp, printable
except ImportError:  # direct script execution
    from candidate_pool import build_pool, trans
    from lib import load, evp, printable
from Crypto.Cipher import AES

def try_pw(raw, pw):
    k, iv = evp(pw, raw[8:16])
    ct = raw[16:]
    if len(ct) > 32:  # decrypt last two blocks only
        prev = ct[-32:-16]
        p = AES.new(k, AES.MODE_CBC, prev).decrypt(ct[-16:])
    else:
        p = AES.new(k, AES.MODE_CBC, iv).decrypt(ct)[-16:] if len(ct) == 16 else None
        if p is None:
            prev = ct[-32:-16]; p = AES.new(k, AES.MODE_CBC, prev).decrypt(ct[-16:])
    n = p[-1]
    if 1 <= n <= 16 and p[-n:] == bytes([n]) * n:
        full = AES.new(k, AES.MODE_CBC, iv).decrypt(ct)[:-n]
        return full
    return None

def main():
    pool = build_pool()
    print("pool", len(pool))
    conts = {n: load(n + '.b64') for n in ('terminal', 'salphaseion-short', 'cosmic-duality')}
    conts['phase3.2'] = load('phase3.2.b64')  # control

    hits = []
    t0 = time.time()
    pl = sorted(pool)
    for idx, s in enumerate(pl):
        for tn, pw in trans(s):
            for cn, raw in conts.items():
                f = try_pw(raw, pw)
                if f is not None:
                    pr = printable(f)
                    if (cn == 'phase3.2' and pr > 0.55) or (cn != 'phase3.2' and pr > 0.85):
                        hits.append((cn, tn, s[:60], round(pr, 2), f[:80]))
                        print('HIT', hits[-1], flush=True)
    print('done', time.time() - t0)

if __name__ == '__main__':
    main()
