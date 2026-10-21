"""Summarise results.json: key matches, inspect rows, pad-hit rates vs chance, observed vs control."""
import json
from collections import defaultdict
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
r = json.loads((HERE / 'results.json').read_text(encoding='utf-8'))

def binom_sf(k, n, p):
    """P(X >= k)."""
    if k <= 0: return 1.0
    mean = n * p
    if n > 5000:  # normal approximation with continuity correction
        from math import erf, sqrt
        z = (k - 0.5 - mean) / sqrt(n * p * (1 - p))
        return 0.5 * (1 - erf(z / sqrt(2)))
    return 1 - sum(comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k))

t = defaultdict(int)
for line in r['tallies']:
    key, v = line.rsplit('=', 1)
    t[tuple(key.split('|'))] = int(v)

print('key matches:', len(r['key_matches']))
for row in r['key_matches']: print('  ', row)
print('rows to inspect:', len(r['inspect']))
for row in r['inspect']:
    print('  ', {k: row[k] for k in row if k != 'plaintext_hex'}, row['plaintext_hex'][:80])

print('\npad-hit rates (CBC; chance ~ 1/256 = 0.00391 per trial, slightly more counting pad>=2)')
groups = defaultdict(lambda: [0, 0])
for (arm, group, env, deriv, kind), v in t.items():
    if arm == 'D': continue
    groups[(arm, group, env)][0 if kind == 'trials' else 1] += v
p = sum(1 / 256**i for i in range(1, 17)) / 1  # P(valid PKCS#7) ~ 1/255
for k, (n, hits) in sorted(groups.items()):
    print(f'  {"/".join(k):55s} trials={n:7d} pad={hits:5d} expected={n*p:8.1f} P(>=)={binom_sf(hits, n, p):.3f}')
print('\narm D (full Terminal)')
for (arm, group, env, mode, kind), v in sorted(t.items()):
    if arm == 'D': print(f'  {mode:7s} {kind:6s} {v}')

# loader control: arm B SalPhaseIon
sal = sum(v for (arm, g, env, d, kind), v in t.items() if arm == 'B' and env == 'salphaseion_short' and kind == 'pad')
print('\narm B SalPhaseIon pad hits (fresh-start saw 45):', sal)
