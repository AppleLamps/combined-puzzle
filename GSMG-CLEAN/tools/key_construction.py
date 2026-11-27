#!/usr/bin/env python3
"""Test saved step-2/3/4 strings as private keys against the two prize addresses.

No envelope is opened. The candidate strings are:

- step 2: the seven yellow (`be`) groups of the standing 84-cell parse,
  intertwined by concatenation, braid, zip and reversed-braid, from every
  cyclic start, in both directions. The combination list was not saved by an
  earlier run, so it is rebuilt here from those seven groups and nothing else.
- step 3: the saved colour-selector renderings, and the standing yin-yang
  operators (identity, reverse, atbash, both half-interleaves, xor-mod-26)
  applied to the saved last-words selections. Upper and lower renderings of
  each operator result are included. The operator file itself was not on disk.
- step 4: the saved 479/484 extraction strings (M4 candidates, and pointer
  windows whose note names 479 or 484).

The Phase 3.2 answer is a control only. It is not counted with the candidates.
"""
import hashlib
import hmac
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dbbi_step2  # noqa: E402
import prize_gate as pg  # noqa: E402

RUN = ROOT / 'runs' / '2026-11-27_key_construction'
WORDLIST = ROOT / 'data' / 'bip39_english.txt'
WORDLIST_SHA256 = '2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda'
PHASE32 = 'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple'
N = pg.N
INTERPS = ('wif', 'hex64', 'sha256', 'bip39')

# BIP173 vector and the BIP39/BIP44 abandon/TREZOR vector.
BECH32_VECTOR = ('751e76e8199196d454941c45d1b3a323f1433bd6',
                 'bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4')
ABANDON = ' '.join(['abandon'] * 11 + ['about'])
ABANDON_SEED = ('c55257c360c07c72029aebc1b53c05ed0362ada38ead3e3e9efa3708e5349553'
                '1f09a6987599d18264c1e1c92f2cf141630c7a3c4ab7c81b2f001698e7463b04')
ABANDON_P2PKH = '1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA'
KEY1_P2PKH = '1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH'

CHARSET = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'
_GEN = (0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3)


def bech32_polymod(values):
    chk = 1
    for value in values:
        top = chk >> 25
        chk = ((chk & 0x1ffffff) << 5) ^ value
        for i in range(5):
            if (top >> i) & 1:
                chk ^= _GEN[i]
    return chk


def bech32_hrp_expand(hrp):
    return [ord(c) >> 5 for c in hrp] + [0] + [ord(c) & 31 for c in hrp]


def bech32_encode(hrp, data):
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
    checksum = [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]
    return hrp + '1' + ''.join(CHARSET[d] for d in data + checksum)


def convertbits(data, frombits, tobits, pad=True):
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            return None
        acc = ((acc << frombits) | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret


def p2wpkh(h160):
    program = convertbits(h160, 8, 5)
    if program is None:
        raise ValueError('witness program')
    return bech32_encode('bc', [0] + program)


def load_words():
    raw = WORDLIST.read_bytes()
    if hashlib.sha256(raw).hexdigest() != WORDLIST_SHA256:
        raise SystemExit('BIP39 wordlist hash mismatch')
    words = raw.decode('ascii').splitlines()
    if len(words) != 2048 or len(set(words)) != 2048:
        raise SystemExit('BIP39 wordlist is not 2048 distinct words')
    return {word: i for i, word in enumerate(words)}


def mnemonic_ok(text, index):
    parts = text.split()
    if len(parts) not in (12, 15, 18, 21, 24):
        return False
    try:
        indices = [index[part] for part in parts]
    except KeyError:
        return False
    packed = 0
    for value in indices:
        packed = (packed << 11) | value
    total = len(parts) * 11
    cs_len = total // 33
    ent_len = total - cs_len
    entropy = packed >> cs_len
    checksum = packed & ((1 << cs_len) - 1)
    raw = entropy.to_bytes(ent_len // 8, 'big')
    expect = int.from_bytes(hashlib.sha256(raw).digest(), 'big') >> (256 - cs_len)
    return checksum == expect


def mnemonic_seed(mnemonic, passphrase):
    return hashlib.pbkdf2_hmac(
        'sha512', mnemonic.encode('utf-8'), b'mnemonic' + passphrase.encode('utf-8'), 2048, 64)


def compressed_pubkey(scalar):
    _unc, comp = pg.public_keys(scalar)
    return comp


def ck_priv(key, chain, index):
    if index >= 0x80000000:
        data = b'\x00' + key + index.to_bytes(4, 'big')
    else:
        data = compressed_pubkey(int.from_bytes(key, 'big')) + index.to_bytes(4, 'big')
    digest = hmac.new(chain, data, hashlib.sha512).digest()
    left, right = digest[:32], digest[32:]
    left_i = int.from_bytes(left, 'big')
    if left_i >= N:
        return None
    child = (left_i + int.from_bytes(key, 'big')) % N
    if child == 0:
        return None
    return child.to_bytes(32, 'big'), right


def bip44_scalar(seed):
    digest = hmac.new(b'Bitcoin seed', seed, hashlib.sha512).digest()
    key, chain = digest[:32], digest[32:]
    if int.from_bytes(key, 'big') == 0 or int.from_bytes(key, 'big') >= N:
        return None
    for index in (44 + 0x80000000, 0x80000000, 0x80000000, 0, 0):
        got = ck_priv(key, chain, index)
        if got is None:
            return None
        key, chain = got
    return int.from_bytes(key, 'big')


def accept(scalar):
    if not isinstance(scalar, int) or scalar <= 0 or scalar >= N:
        return None
    return scalar


def wif_scalar(text):
    got = pg._wif_scalar(text)
    if got is None:
        return None
    return accept(got[0])


def hex_scalar(text):
    if len(text) != 64:
        return None
    try:
        return accept(int(text, 16))
    except ValueError:
        return None


def sha_scalar(text):
    return accept(int.from_bytes(hashlib.sha256(text.encode('utf-8')).digest(), 'big'))


def bip39_scalars(text, index):
    out = []
    if mnemonic_ok(text, index):
        scalar = bip44_scalar(mnemonic_seed(text, ''))
        if scalar is not None:
            out.append(('mnemonic', scalar))
    scalar = bip44_scalar(mnemonic_seed('', text))
    if scalar is not None:
        out.append(('empty-mnemonic-passphrase', scalar))
    return out


def addresses(scalar):
    unc, comp = pg.public_keys(scalar)
    h_comp = pg.hash160(comp)
    return {
        'p2pkh_uncompressed': pg.address_from_public(unc),
        'p2pkh_compressed': pg.address_from_public(comp),
        'p2wpkh': p2wpkh(h_comp),
        'hash160_uncompressed': pg.hash160(unc).hex(),
        'hash160_compressed': h_comp.hex(),
    }


def seven_groups():
    ops = dbbi_step2.operands()
    cells = ops[84]['cells']
    groups = ops[84]['groups']
    primes = [(i, token) for i, token in enumerate(cells, 1) if dbbi_step2.is_prime(i)]
    if len(primes) != 23:
        raise SystemExit(f'prime census changed: {len(primes)}')
    be = [(slot, groups[n]) for n, (slot, token) in enumerate(primes, 1) if token == 'be']
    b = [token for _slot, token in primes if token == 'b']
    if (len(be), len(b)) != (7, 16):
        raise SystemExit(f'84-cell census changed: be={len(be)} b={len(b)}')
    if any(not group for _slot, group in be):
        raise SystemExit('a yellow group is empty')
    return tuple(group for _slot, group in be)


def cycle(parts, start, reverse):
    seq = list(reversed(parts) if reverse else parts)
    return tuple(seq[start:] + seq[:start])


def braid(parts):
    out = []
    for index in range(max(len(part) for part in parts)):
        for part in parts:
            if index < len(part):
                out.append(part[index])
    return ''.join(out)


def zip_shortest(parts):
    width = min(len(part) for part in parts)
    return ''.join(part[index] for index in range(width) for part in parts)


def reversed_braid(parts):
    return braid(tuple(part[::-1] for part in parts))


def select_strings(parts):
    forms = (
        ('concat', ''.join),
        ('braid', braid),
        ('zip', zip_shortest),
        ('reversed-braid', reversed_braid),
    )
    rows = []
    for start in range(len(parts)):
        for reverse in (False, True):
            ordered = cycle(parts, start, reverse)
            direction = 'reverse' if reverse else 'forward'
            for name, function in forms:
                rows.append({
                    'text': function(ordered),
                    'form': name,
                    'start': start,
                    'direction': direction,
                })
    return rows


def atbash(text):
    out = []
    for char in text:
        if 'a' <= char <= 'z':
            out.append(chr(ord('z') - (ord(char) - 97)))
        elif 'A' <= char <= 'Z':
            out.append(chr(ord('Z') - (ord(char) - 65)))
        else:
            out.append(char)
    return ''.join(out)


def interleave(left, right):
    out = []
    for index in range(max(len(left), len(right))):
        if index < len(left):
            out.append(left[index])
        if index < len(right):
            out.append(right[index])
    return ''.join(out)


def xor_mod26(text):
    half = len(text) // 2
    left, right = text[:half], text[half:]
    width = min(len(left), len(right))
    out = []
    for index in range(width):
        a, b = left[index], right[index]
        if a.isalpha() and b.isalpha():
            out.append(chr(97 + ((ord(a.lower()) - 97) ^ (ord(b.lower()) - 97)) % 26))
        else:
            out.append(chr(97 + ((ord(a) ^ ord(b)) % 26)))
    longer = left if len(left) > len(right) else right
    out.append(longer[width:])
    return ''.join(out)


def yinyang_renderings(text):
    half = len(text) // 2
    left, right = text[:half], text[half:]
    produced = {
        'identity': text,
        'reverse': text[::-1],
        'atbash': atbash(text),
        'interleave': interleave(left, right),
        'interleave-swapped': interleave(right, left),
        'xor-mod26': xor_mod26(text),
    }
    rows = []
    for operator, value in produced.items():
        for rendering, rendered in (
            ('as-written', value),
            ('lower', value.lower()),
            ('upper', value.upper()),
        ):
            if rendered:
                rows.append((operator, rendering, rendered))
    return rows


def add(pool, family, text, detail):
    if text is None:
        return
    pool.setdefault(family, {})
    pool[family].setdefault(text, []).append(detail)


def load_pool(parts):
    pool = {}
    for row in select_strings(parts):
        add(pool, 'step2-select', row['text'],
            f"{row['form']}/start{row['start']}/{row['direction']}")
    for index, part in enumerate(parts):
        add(pool, 'step2-source', part, f'be-group/{index}')
    colour = ROOT / 'runs/2026-09-14_colour_selectors/all_outputs.jsonl'
    for line in colour.read_text(encoding='utf-8').splitlines():
        if line.strip():
            row = json.loads(line)
            add(pool, 'step3-colour-rendering', row['output'],
                f"{row['selector']}/{row['list']}/{row['decode']}")
    last = ROOT / 'runs/2026-11-10_step2_sumlist_lastwords_v3/outputs.jsonl'
    for line in last.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        text = json.loads(line)['text']
        for operator, rendering, rendered in yinyang_renderings(text):
            add(pool, 'step3-yinyang', rendered, f'{operator}/{rendering}')
    m4 = ROOT / 'runs/2026-09-14_m4_zeroing_oracles/candidates.jsonl'
    for line in m4.read_text(encoding='utf-8').splitlines():
        if line.strip():
            row = json.loads(line)
            add(pool, 'step4-m4', row['candidate'], f"{row['family']}/{row['note']}")
    pointer = ROOT / 'runs/2026-09-14_pointer_selectors/candidates.jsonl'
    for line in pointer.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        note = row.get('note', '')
        if '479' in note or '484' in note:
            add(pool, 'step4-479-484', row['candidate'], f"{row['family']}/{note}")
    return pool


def interpret(text, index):
    found = {'wif': [], 'hex64': [], 'sha256': [], 'bip39': []}
    wif = wif_scalar(text)
    if wif is not None:
        found['wif'].append(('wif', wif))
    hex64 = hex_scalar(text)
    if hex64 is not None:
        found['hex64'].append(('hex64', hex64))
    digest = sha_scalar(text)
    if digest is not None:
        found['sha256'].append(('sha256', digest))
    found['bip39'].extend(bip39_scalars(text, index))
    return found


def prize_targets():
    half_h160 = pg.HALF_H160
    better_h160 = pg.BETTER_H160
    return {
        'p2pkh': {
            pg.HALF_ADDRESS: 'half',
            pg.BETTER_ADDRESS: 'better-half',
        },
        'hash160': {
            half_h160.hex(): 'half',
            better_h160.hex(): 'better-half',
        },
        'p2wpkh_of_prize_hash160': {
            p2wpkh(half_h160): 'half-hash160-as-witness-program',
            p2wpkh(better_h160): 'better-half-hash160-as-witness-program',
        },
    }


def selftest(index):
    checks = []

    def check(name, ok):
        checks.append((name, bool(ok)))
        print(('PASS ' if ok else 'FAIL ') + name)
        if not ok:
            raise SystemExit('address path failed its own control')

    program, expect = BECH32_VECTOR
    check('BIP173 P2WPKH vector', p2wpkh(bytes.fromhex(program)) == expect)
    check('BIP39 abandon checksum', mnemonic_ok(ABANDON, index))
    check('BIP39 abandon seed, passphrase TREZOR',
          mnemonic_seed(ABANDON, 'TREZOR').hex() == ABANDON_SEED)
    abandon = bip44_scalar(mnemonic_seed(ABANDON, ''))
    got = addresses(abandon)
    check('BIP44 m/44\'/0\'/0\'/0/0 abandon, empty passphrase',
          got['p2pkh_compressed'] == ABANDON_P2PKH)
    check('P2WPKH of that compressed key', got['p2wpkh'] == p2wpkh(bytes.fromhex(got['hash160_compressed'])))
    check('key 1 compressed P2PKH', addresses(1)['p2pkh_compressed'] == KEY1_P2PKH)
    wif_c = pg.b58check_encode(b'\x80' + (1).to_bytes(32, 'big') + b'\x01')
    wif_u = pg.b58check_encode(b'\x80' + (1).to_bytes(32, 'big'))
    check('compressed WIF of key 1', wif_scalar(wif_c) == 1)
    check('uncompressed WIF of key 1', wif_scalar(wif_u) == 1)
    check('bad WIF checksum rejected', wif_scalar(wif_c[:-1] + ('X' if wif_c[-1] != 'X' else 'Y')) is None)
    check('order rejected', accept(N) is None and accept(0) is None)
    check('short hex rejected', hex_scalar('11' * 32) == int('11' * 32, 16) and hex_scalar('11' * 31) is None)
    parts = seven_groups()
    check('seven yellow groups', parts == ('g', 'ggege', 'b', 'ffcdb', 'eggec', 'dci', 'eea'))
    rows = select_strings(parts)
    check('56 select rows', len(rows) == 56)
    check('braid of two', braid(('abc', 'de')) == 'adbec')
    check('zip stops at shortest', zip_shortest(('abc', 'de')) == 'adbe')
    control = sha_scalar(PHASE32)
    check('phase 3.2 brainwallet in range', control is not None)
    check('phase 3.2 brainwallet address decodes',
          pg.b58check_decode(addresses(control)['p2pkh_compressed']) is not None)
    return checks, parts, addresses(control)


def blank():
    return {
        'strings': 0,
        'valid_keys': 0,
        'addresses': 0,
        'matches': [],
    }


def main():
    index = load_words()
    _checks, parts, control_addresses = selftest(index)
    targets = prize_targets()
    pool = load_pool(parts)
    families = {}
    matches = []
    for family in (
        'step2-select', 'step2-source', 'step3-colour-rendering',
        'step3-yinyang', 'step4-m4', 'step4-479-484',
    ):
        texts = pool.get(family, {})
        cell = {name: blank() for name in INTERPS}
        cell['strings'] = len(texts)
        for text, details in texts.items():
            found = interpret(text, index)
            for name in INTERPS:
                scalars = found[name]
                if not scalars:
                    continue
                cell[name]['valid_keys'] += len(scalars)
                cell[name]['addresses'] += 3 * len(scalars)
                for kind, scalar in scalars:
                    got = addresses(scalar)
                    hit = {}
                    for form in ('p2pkh_uncompressed', 'p2pkh_compressed'):
                        label = targets['p2pkh'].get(got[form])
                        if label:
                            hit[form] = label
                    for form in ('hash160_uncompressed', 'hash160_compressed'):
                        label = targets['hash160'].get(got[form])
                        if label:
                            hit[form] = label
                    label = targets['p2wpkh_of_prize_hash160'].get(got['p2wpkh'])
                    if label:
                        hit['p2wpkh'] = label
                    if hit:
                        record = {
                            'family': family,
                            'interpretation': name,
                            'kind': kind,
                            'matches': hit,
                            'addresses': {k: got[k] for k in (
                                'p2pkh_uncompressed', 'p2pkh_compressed', 'p2wpkh')},
                            'scalar': f'{scalar:064x}',
                            'text': text,
                            'details': details[:8],
                        }
                        cell[name]['matches'].append(record)
                        matches.append(record)
        for name in INTERPS:
            cell[name]['strings'] = cell['strings']
        families[family] = cell
        print(family, cell['strings'],
              {name: cell[name]['valid_keys'] for name in INTERPS}, flush=True)

    control_found = interpret(PHASE32, index)
    control = {
        'text': PHASE32,
        'brainwallet_addresses': control_addresses,
        'valid_keys': {name: len(control_found[name]) for name in INTERPS},
        'wif': bool(control_found['wif']),
        'hex64': bool(control_found['hex64']),
        'sha256_in_range': bool(control_found['sha256']),
        'bip39_kinds': [kind for kind, _scalar in control_found['bip39']],
        'prize_match': False,
    }
    for name in INTERPS:
        for _kind, scalar in control_found[name]:
            got = addresses(scalar)
            if (got['p2pkh_compressed'] in targets['p2pkh']
                    or got['p2pkh_uncompressed'] in targets['p2pkh']
                    or got['p2wpkh'] in targets['p2wpkh_of_prize_hash160']):
                control['prize_match'] = True

    payload = {
        'backend': pg.BACKEND,
        'prize_addresses': {
            'half': pg.HALF_ADDRESS,
            'better_half': pg.BETTER_ADDRESS,
            'half_hash160': pg.HALF_H160.hex(),
            'better_half_hash160': pg.BETTER_H160.hex(),
            'half_hash160_as_p2wpkh': p2wpkh(pg.HALF_H160),
            'better_half_hash160_as_p2wpkh': p2wpkh(pg.BETTER_H160),
        },
        'seven_groups': list(parts),
        'census': {'primes': 23, 'b': 16, 'be': 7},
        'families': {
            family: {
                'strings': families[family]['strings'],
                **{name: {
                    'valid_keys': families[family][name]['valid_keys'],
                    'addresses': families[family][name]['addresses'],
                    'matches': len(families[family][name]['matches']),
                } for name in INTERPS},
            }
            for family in families
        },
        'matches': matches,
        'control': control,
        'notes': {
            'envelopes': 'not opened',
            'chat_sweep': 'not run',
            'step2_combinations': 'rebuilt from the seven standing yellow groups; no earlier dump was on disk',
            'step3_operators': 'applied here to the saved last-words selections; no earlier operator dump was on disk',
        },
    }
    RUN.mkdir(parents=True, exist_ok=True)
    (RUN / 'results.json').write_text(json.dumps(payload, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'matches': len(matches), 'control_sha256': control['sha256_in_range']}, indent=1))


if __name__ == '__main__':
    main()
