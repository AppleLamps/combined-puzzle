import hashlib, json, time, urllib.request, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from ecdsa import SigningKey, SECP256k1

N = SECP256k1.order
TARGET = bytes.fromhex('a9553269572a317e39f0f518cb87c1a0ee1dbae4')
A58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
OUT = 'ltc_scan2_results.jsonl'


def b58check(payload):
    c = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    b = payload + c
    n = int.from_bytes(b, 'big')
    s = ''
    while n:
        n, r = divmod(n, 58)
        s = A58[r] + s
    pad = len(b) - len(b.lstrip(b'\x00'))
    return '1' * pad + s


def pubkey(d, comp):
    sk = SigningKey.from_secret_exponent(d, curve=SECP256k1)
    p = sk.verifying_key.pubkey.point
    x, y = p.x(), p.y()
    if comp:
        return bytes([2 + (y & 1)]) + x.to_bytes(32, 'big')
    return b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')


def h160(b):
    return hashlib.new('ripemd160', hashlib.sha256(b).digest()).digest()


toks = ['matrixsumlist', 'enter', 'lastwordsbeforearchichoice', 'thispassword', 'yourlastcommand',
        'secondanswer', 'yinyang', 'theproblemischoice', 'oneforonefourforone', 'causality',
        'fourfirsthintisyourlastcommand', 'yellow', 'blue', 'primes', 'yellowblueprimes',
        'ourfirsthintisyourlastcommand', 'yellowblueprimesmatrixsumlistlastwordsbeforearchichoiceyinyang',
        'ltc', 'btc', 'litecoin', 'bitcoin', 'archichoice', 'lastwords', 'password', 'giveaway',
        'givetit', 'surebutwewontgiveitaway', 'thepassworditsinfrontofyoureyes',
        'removethecorrecthinttoproceedtothenextstage',
        'adu', 'bev', 'ltcbtc', 'btcltc', 'btc not ltc', '100% btc not ltc', 'jrk not use this 100% btc not ltc',
        'happy new year', 'tiny hint', 'the number c is the 2nd hint', 'whatif13',
        'youtubecomwatchvdQw4w9WgXcQ']
variants = set()
for t in toks:
    for v in {t, t.upper(), t.lower(), t.capitalize(), t.title(), t.replace(' ', '')}:
        variants.add(v)
        variants.add(v + '1')
        variants.add(v + '!')
        variants.add(v + '\n')
phrases = sorted(variants)
print('phrases:', len(phrases), flush=True)

rows = []
for ph in phrases:
    d = int.from_bytes(hashlib.sha256(ph.encode()).digest(), 'big') % N
    if not d:
        continue
    for comp in (True, False):
        hh = h160(pubkey(d, comp))
        rows.append((ph, 'comp' if comp else 'uncomp', hh.hex(), b58check(b'\x00' + hh), b58check(b'\x30' + hh), hh == TARGET))
print('keys:', len(rows), 'target matches:', sum(r[5] for r in rows), flush=True)

addrs = {}
for r in rows:
    addrs.setdefault(r[3], 'BTC')
    addrs.setdefault(r[4], 'LTC')
print('unique addresses:', len(addrs), flush=True)


def get(a, chain):
    url = (f'https://mempool.space/api/address/{a}' if chain == 'BTC'
           else f'https://litecoinspace.org/api/address/{a}')
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'chk'}), timeout=20) as r:
                d = json.loads(r.read())
            cs = d.get('chain_stats', {})
            ms = d.get('mempool_stats', {})
            return (chain, cs.get('tx_count', 0), ms.get('tx_count', 0), cs.get('funded_txo_sum', 0))
        except Exception as e:
            err = str(e)[:60]
            time.sleep(1.5 * (attempt + 1))
    return ('ERR', err)


done = 0
t0 = time.time()
active = []
errors = 0
with open(OUT, 'w') as f, ThreadPoolExecutor(max_workers=8) as ex:
    futs = {ex.submit(get, a, c): (a, c) for a, c in addrs.items()}
    for fut in as_completed(futs):
        a, c = futs[fut]
        res = fut.result()
        done += 1
        if res[0] == 'ERR':
            errors += 1
        elif res[1] or res[2]:
            active.append((a, res))
            print('HISTORY', a, res, flush=True)
        f.write(json.dumps({'addr': a, 'chain': c, 'res': res}) + '\n')
        f.flush()
        if done % 100 == 0 or done == len(addrs):
            rate = done / (time.time() - t0)
            print(f'progress {done}/{len(addrs)} errors={errors} active={len(active)} rate={rate:.1f}/s', flush=True)

print('DONE. queried', done, 'errors', errors, 'addresses with history', len(active), flush=True)
