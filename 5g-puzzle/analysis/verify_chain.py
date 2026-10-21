#!/usr/bin/env python3
"""Independently verify the on-chain report from the raw transaction hex.

Nothing here trusts the reporting agent's parse: txids are recomputed from the
hex, r/s are re-extracted from the DER in each scriptSig, the legacy sighash z is
rebuilt from scratch, and every signature is verified against the public key. If
the z construction were wrong the verifications would fail -- that is the check
that makes the nonce-reuse null trustworthy rather than merely asserted."""
import hashlib, json
from ecdsa import VerifyingKey, SECP256k1, util as eutil
from ecdsa.util import sigdecode_der

RAW = {}
for line in open('/root/.claude/uploads/3ce5fd60-660e-5825-8dbb-c2131e61358a/4be8dd79-rawhex.txt'):
    line = line.strip()
    if line.startswith('=='):
        txid, src = line.split()[1], line.split()[2]
    elif line:
        RAW.setdefault(txid, {})[src] = line

H160_HALF   = 'a9553269572a317e39f0f518cb87c1a0ee1dbae4'
H160_BETTER = '4bc468447fe1b048ad030a2f9a125478eabc4ed6'
SPK_HALF    = bytes.fromhex('76a914' + H160_HALF + '88ac')
PUB = bytes.fromhex('04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464'
                    '9c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559')

def d256(b): return hashlib.sha256(hashlib.sha256(b).digest()).digest()
def h160(b): return hashlib.new('ripemd160', hashlib.sha256(b).digest()).digest()

class R:
    def __init__(s, b): s.b, s.i = b, 0
    def take(s, n):
        v = s.b[s.i:s.i+n]; s.i += n; return v
    def u32(s): return int.from_bytes(s.take(4), 'little')
    def u64(s): return int.from_bytes(s.take(8), 'little')
    def varint(s):
        v = s.take(1)[0]
        if v < 0xfd: return v
        return int.from_bytes(s.take({0xfd:2, 0xfe:4, 0xff:8}[v]), 'little')

def parse(raw):
    r = R(raw); tx = {'version': r.u32(), 'vin': [], 'vout': []}
    for _ in range(r.varint()):
        prev = r.take(32)[::-1].hex(); idx = r.u32()
        script = r.take(r.varint()); seq = r.u32()
        tx['vin'].append({'prev': prev, 'idx': idx, 'script': script, 'seq': seq})
    for _ in range(r.varint()):
        val = r.u64(); spk = r.take(r.varint())
        tx['vout'].append({'value': val, 'spk': spk})
    tx['locktime'] = r.u32()
    return tx

def ser(tx, scripts):
    o = tx['version'].to_bytes(4,'little') + bytes([len(tx['vin'])])
    for v, sc in zip(tx['vin'], scripts):
        o += bytes.fromhex(v['prev'])[::-1] + v['idx'].to_bytes(4,'little')
        o += bytes([len(sc)]) + sc + v['seq'].to_bytes(4,'little')
    o += bytes([len(tx['vout'])])
    for v in tx['vout']:
        o += v['value'].to_bytes(8,'little') + bytes([len(v['spk'])]) + v['spk']
    return o + tx['locktime'].to_bytes(4,'little')

vk = VerifyingKey.from_string(PUB[1:], curve=SECP256k1)
print(f"pubkey hash160 = {h160(PUB).hex()}  ({'MATCHES Half' if h160(PUB).hex()==H160_HALF else 'MISMATCH'})\n")

sigs = []
for txid, srcs in RAW.items():
    assert len(set(srcs.values())) == 1, f'{txid}: sources disagree'
    raw = bytes.fromhex(next(iter(srcs.values())))
    calc = d256(raw)[::-1].hex()
    print(f'== {txid}')
    print(f'   txid recomputed from hex: {calc}  {"OK" if calc==txid else "MISMATCH"}'
          f'   (both sources byte-identical: yes)')
    tx = parse(raw)
    for i, v in enumerate(tx['vin']):
        sc = v['script']
        n = sc[0]; der = sc[1:1+n]; ht = der[-1]; der = der[:-1]
        pk = sc[1+n+1:]
        assert pk == PUB, f'input {i} signed by a different key'
        scripts = [SPK_HALF if j == i else b'' for j in range(len(tx['vin']))]
        z = d256(ser(tx, scripts) + ht.to_bytes(4, 'little'))
        r_, s_ = sigdecode_der(der, SECP256k1.order)
        ok = vk.verify_digest(eutil.sigencode_string(r_, s_, SECP256k1.order), z,
                              sigdecode=eutil.sigdecode_string)
        sigs.append({'txid': txid, 'vin': i, 'r': r_, 's': s_, 'z': int.from_bytes(z,'big'), 'ok': ok})
        print(f'   vin[{i}] ht=0x{ht:02x} verified={ok}')
        print(f'      r = {r_:064x}')
        print(f'      z = {int.from_bytes(z,"big"):064x}')
    for j, o in enumerate(tx['vout']):
        who = 'Half' if o['spk'].hex()[6:6+40]==H160_HALF else \
              'BetterHalf' if o['spk'].hex()[6:6+40]==H160_BETTER else 'THIRD PARTY'
        print(f'   out[{j}] {o["value"]:>12,} sat -> {who}')
    print(f'   locktime {tx["locktime"]}')
print()
print(f'signatures: {len(sigs)}   all verified: {all(s["ok"] for s in sigs)}')
rs = [s['r'] for s in sigs]
print(f'distinct r: {len(set(rs))} of {len(rs)}   REUSED NONCE: {"YES" if len(set(rs))<len(rs) else "NONE"}')
json.dump([{k:(hex(v) if isinstance(v,int) else v) for k,v in s.items()} for s in sigs],
          open('/tmp/claude-0/my_sigs.json','w'), indent=1)
