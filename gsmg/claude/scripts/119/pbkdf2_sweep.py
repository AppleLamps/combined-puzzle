#!/usr/bin/env python3
"""Doc 119: the three locks under PBKDF2 (openssl enc -pbkdf2), a KDF no session tried.

Profile: key||iv = PBKDF2-HMAC-<md>(password, salt, iter, 48), AES-256-CBC, PKCS7,
then the doc 110 recogniser. Passwords: the candidate as typed and its sha256 hex.
Iterations: 10000 (openssl default) and 600000 (Trust Wallet's export), md sha256;
plus sha1 at 10000. A planted container per (iter, md) is opened by a known candidate.

    python3 pbkdf2_sweep.py A            # tier A: grounded strings, all profiles
    python3 pbkdf2_sweep.py B            # tier B: every chat token and creator n-gram, 10000 only
"""
import hashlib, multiprocessing as mp, os, random, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '115')); sys.path.insert(0, os.path.join(HERE, '..', 'telegram'))
import harness as H
from Crypto.Cipher import AES

PROFILES_A = [('sha256', 10000), ('sha256', 600000), ('sha1', 10000), ('sha256', 1000), ('sha256', 2048), ('sha256', 100000)]
PROFILES_B = [('sha256', 10000)]

def planted(answer, md, it, seed):
    r = random.Random(seed); salt = r.randbytes(8); pt = r.randbytes(64)
    dk = hashlib.pbkdf2_hmac(md, answer, salt, it, 48)
    return b'Salted__' + salt + AES.new(dk[:32], AES.MODE_CBC, dk[32:48]).encrypt(pt + bytes([16]) * 16)

def open_one(raw, pw, md, it):
    dk = hashlib.pbkdf2_hmac(md, pw, raw[8:16], it, 48)
    ct = raw[16:]
    last = AES.new(dk[:32], AES.MODE_CBC, ct[-32:-16]).decrypt(ct[-16:]) if len(ct) > 32 else None
    if last is not None:
        p = last[-1]
        if not (1 <= p <= 16 and last[-p:] == bytes([p]) * p): return None
    pt = AES.new(dk[:32], AES.MODE_CBC, dk[32:48]).decrypt(ct); p = pt[-1]
    return (p, pt[:-p]) if 1 <= p <= 16 and pt[-p:] == bytes([p]) * p else None

G = {}
def _init(containers, profiles):
    G['c'] = containers; G['p'] = profiles

def _work(chunk):
    dec = valid = 0; flags = []
    for lab, cand in chunk:
        b = cand.encode() if isinstance(cand, str) else cand
        for prof, pw in (('raw', b), ('sha', hashlib.sha256(b).hexdigest().encode())):
            for md, it in G['p']:
                for name, raw in G['c'].items():
                    dec += 1; r = open_one(raw, pw, md, it)
                    if r:
                        valid += 1; pad, pt = r; why = H.recognise(pt, pad)
                        if why: flags.append((name, prof, md, it, pad, why, lab, cand))
    return len(chunk), dec, valid, flags

def run(items, profiles, tag, procs=None, chunk=None):
    procs = procs or os.cpu_count()
    containers = dict(H.CONTAINERS)
    ctl = items[len(items) // 2][1]; ctl_b = ctl.encode() if isinstance(ctl, str) else ctl
    for md, it in profiles:
        containers[f'CONTROL-{md}-{it}'] = planted(ctl_b, md, it, seed=119 + it)
    chunk = chunk or max(1, len(items) // (procs * 8))
    chunks = [items[i:i + chunk] for i in range(0, len(items), chunk)]
    t0 = time.time(); C = D = V = 0; F = []
    with mp.get_context('spawn').Pool(procs, initializer=_init, initargs=(containers, profiles)) as pool:
        for c, d, v, f in pool.imap_unordered(_work, chunks):
            C += c; D += d; V += v; F += f
    ctl_fired = sorted({f[0] for f in F if f[0].startswith('CONTROL') and f[7] == ctl})
    real = [f for f in F if not f[0].startswith('CONTROL')]
    print(f'[{tag}] candidates {C} decrypts {D} valid {V} (expected {D/256:.0f}) controls fired {len(ctl_fired)}/{len(profiles)} real flags {len(real)} {time.time()-t0:.0f}s', flush=True)
    with open(os.path.join(HERE, f'pbkdf2-{tag}.flags'), 'w') as fh:
        fh.write(f'# {tag}: candidates {C} decrypts {D} valid {V} expected {D/256:.0f}; controls {len(ctl_fired)}/{len(profiles)}\n')
        for f in real: fh.write(repr(f) + '\n')
    for f in real: print('FLAG', repr(f)[:300], flush=True)
    return real

def tier_a():
    d = os.path.join(HERE, '..', '115', 'data')
    rd = lambda n: open(os.path.join(d, n), encoding='utf-8').read()
    soup = rd('soup.txt'); arch = rd('architect.txt'); chk = rd('checker.txt')
    labels = ['yellowblueprimes', 'matrixsumlist', 'lastwordsbeforearchichoice', 'yinyang', 'yingyang', 'thispassword', 'enter',
              'ourfirsthintisyourlastcommand', 'theanswerstoo', 'anstoo', 'fanstoo', 'shabefanstoo', 'shabefourfirsthintisyourlastcommand',
              'salphaseion', 'SalPhaseIon', 'salvation', 'salphation', 'cosmicduality', 'CosmicDuality', 'Cosmic Duality', 'hashthetext', 'HASHTHETEXT']
    answers = ['theflowerblossomsthroughwhatseemstobeaconcretesurface', 'causality', 'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple',
               'causalitySafenetLunaHSM111100x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1',
               'Safenet', 'Luna', 'HSM', '11110', 'jacquefresco', 'giveit', 'givetit', 'justonesecond', 'heisenbergsuncertaintyprinciple',
               '5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75', 'eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf',
               '1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5', '250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c',
               '89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32', 'GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe',
               '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe', 'gsmg.io/theseedisplanted', 'theseedisplanted', 'gsmg.io', 'gsmg', 'GSMG', 'gsmg.io/puzzle',
               'choiceisanillusioncreatedbetweenthosewithpowerandthosewithout', 'averyspecialdessertiwroteitmyself', 'choiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecialdessertiwroteitmyself',
               'thematrixhasyou', 'THEMATRIXHASYOU', 'followthewhiterabbit', 'wakeupneo', 'knockknockneo', 'neo', 'Neo', 'trinity', 'morpheus', 'architect', 'oracle', 'merovingian', 'keymaker', 'zion', 'source', 'thesource',
               'halfandbetterhalf', 'betterhalf', 'half', 'oneforonefourforone', 'FUBCDORA.LETHINGKYMVPS/JQZXW', 'fubcdoraletehingkymvpsjqzxw',
               'password', 'Password', 'PASSWORD', 'password1', 'Password1', 'Password1$', 'gsmgpuzzle', 'puzzle', 'bitcoin', 'satoshi', 'sowut', 'SoWut', 'jrk', 'jrkbgrt', 'Jrk Bgrt',
               'hopeitisthequintessentialhumandelusion', 'hope', 'choice', 'thechoiceisours', 'jacquefrescothechoiceisours', 'lookingforward', 'Looking Forward',
               'primes', 'prime', '257', '101', '127', '42', '0', '1', 'one', 'zero', 'yellow', 'blue', 'red', 'black', 'white', 'purple', 'infrared',
               soup, soup[:91], soup[195:765], soup[766:829], soup[830:859], arch, arch.upper(), chk, chk.upper(),
               'difhccgihaeeihggegebgehhehhfafdhffcdbfcccgfeggecdcifffgigeea',
               'yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyang',
               'yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyangwewontgiveawaythepassworditsinfrontofyoureyesbutyourenotseeingitverylaststepisatruegiveawaypromised',
               'wewontgiveawaythepassworditsinfrontofyoureyesbutyourenotseeingitverylaststepisatruegiveawaypromised',
               'itsinfrontofyoureyesbutyourenotseeingit', 'verylaststepisatruegiveawaypromised',
               'Roses are White but often Red.', 'rosesarewhitebutoftenred', 'yellowhasanumberandsodoesblue', 'gobacktothefirstpuzzlepiecewithoutfurtherado', 'hushhush', 'Hush hush',
               'giveyourselfyourselfandyourselfwillbegivenyourself', 'yourself', 'inamatrixcypherkindaway', 'cypher', 'hadmyeyesclosedbutstillsawdouble',
               'Happy new year! Make the best of everything. Oh, and here\'s a "tiny hint" <3.', 'tinyhint', 'tiny hint', 'happynewyear',
               'U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9zQvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ',
               'U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46zgKlIi8aaqY5gpJPPEzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4']
    items = [(f'A{i}', s) for i, s in enumerate(labels + answers)]
    # case and spacing variants of the short ones
    extra = []
    for lab, s in items:
        if len(s) <= 60:
            for v in (s.lower(), s.upper(), s.title(), s.replace(' ', ''), s.capitalize()):
                if v != s: extra.append((lab + 'v', v))
    seen = set(); out = []
    for lab, s in items + extra:
        if s not in seen: seen.add(s); out.append((lab, s))
    return out

def tier_b():
    from tg import load, text, CREATOR_ID
    b = load(); out = []; seen = set()
    for m in b.values():
        if m['type'] != 'message': continue
        t = text(m)
        if not t: continue
        toks = [x.strip('.,;:!?"\'()[]{}') for x in t.split()]
        toks = [x for x in toks if x]
        cre = m.get('from_id') == CREATOR_ID
        for x in toks:
            for v in (x, x.lower()):
                if v not in seen: seen.add(v); out.append(('tok', v))
        if cre:
            for n in (2, 3, 4, 5, 6):
                for i in range(len(toks) - n + 1):
                    for v in (' '.join(toks[i:i + n]), ''.join(toks[i:i + n]).lower()):
                        if v not in seen: seen.add(v); out.append(('cre', v))
            for v in (t, t.strip(), t.lower()):
                if v not in seen: seen.add(v); out.append(('cmsg', v))
    return out

if __name__ == '__main__':
    tier = sys.argv[1] if len(sys.argv) > 1 else 'A'
    if tier == 'A':
        items = tier_a(); print(f'tier A: {len(items)} candidates x {len(PROFILES_A)} profiles', flush=True)
        run(items, PROFILES_A, 'A', chunk=8)
    else:
        items = tier_b(); print(f'tier B: {len(items)} candidates', flush=True)
        run(items, PROFILES_B, 'B')
