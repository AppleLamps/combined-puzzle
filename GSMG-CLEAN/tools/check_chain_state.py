"""Refresh the on-chain facts of 01 section 9 from a public block explorer and re-derive every
address the ledger relies on.  Read-only: it sends nothing but GET requests for public addresses.

  python tools/check_chain_state.py [run_dir]        default run_dir: runs/2026-11-10_state_refresh

Writes <run_dir>/chain_state.json (the summary) and <run_dir>/chain_raw/<address>.json (the raw
transaction lists as returned).  Checks made:

  - balance, transaction count and every spend of Half and Better Half;
  - the eight checkpoint addresses are sha256(answer) or the URL integer, compressed key;
  - the four "neighbors" addresses are P+G, P-G, 2P and P/2 of Half's public key, uncompressed;
  - every payment and OP_RETURN message sent by 3GSMG24TujqfMJG1kQoBX18DzJHQLeJYMK.
"""
import datetime
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import prize_gate as pg  # noqa: E402

API = 'https://blockstream.info/api'
HALF = '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
BETTER_HALF = '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa'
MESSENGER = '3GSMG24TujqfMJG1kQoBX18DzJHQLeJYMK'
TIP_ADDRESS = '1NULY7DhzuNvSDtPkFzNo6oRTZQWBqXNE9'
HALF_PUBKEY = ('04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a4649c73d25fc5ed8fd7227cab0be4e576'
               'c0c6404db5aa546286563e4be12bf33559')
VIC_DIGITS = ('15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631'
              '213131281491109166131412199114371612126021664313711154112')
P_FIELD = 2 ** 256 - 2 ** 32 - 977
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)


def get(url):
    err = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'curl'})
            return json.loads(urllib.request.urlopen(req, timeout=40).read())
        except Exception as exc:                            # noqa: BLE001  (network: retry, then raise)
            err = exc
            time.sleep(2 * (attempt + 1))
    raise err


def all_txs(address):
    out, last = [], None
    while True:
        page = get(f'{API}/address/{address}/txs/chain' + (f'/{last}' if last else ''))
        if not page:
            break
        out += page
        last = page[-1]['txid']
        if len(page) < 25:
            break
        time.sleep(0.4)
    return out


def add(a, b):
    if a is None:
        return b
    if b is None:
        return a
    if a[0] == b[0] and (a[1] + b[1]) % P_FIELD == 0:
        return None
    if a == b:
        lam = 3 * a[0] * a[0] * pow(2 * a[1], -1, P_FIELD) % P_FIELD
    else:
        lam = (b[1] - a[1]) * pow(b[0] - a[0], -1, P_FIELD) % P_FIELD
    x = (lam * lam - a[0] - b[0]) % P_FIELD
    return x, (lam * (a[0] - x) - a[1]) % P_FIELD


def mul(k, pt):
    acc = None
    while k:
        if k & 1:
            acc = add(acc, pt)
        pt = add(pt, pt)
        k >>= 1
    return acc


def address(pt, compressed):
    x = pt[0].to_bytes(32, 'big')
    pub = bytes([2 + (pt[1] & 1)]) + x if compressed else b'\x04' + x + pt[1].to_bytes(32, 'big')
    return pg.address_from_public(pub)


def derived_addresses():
    seven = ''.join(json.loads((ROOT / 'data' / 'seven_part_phase3_answer.json').read_text()))
    answers = {
        'the prize address as text': HALF,
        'Phase 2 answer "causality"': 'causality',
        'the 149 checkerboard digits': VIC_DIGITS,
        'Phase 1 answer': 'theflowerblossomsthroughwhatseemstobeaconcretesurface',
        'Phase 3.2 answer (62 characters)': 'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple',
        'Phase 3 seven-part answer (227 characters)': seven,
    }
    assert len(seven) == 227
    out = {}
    for label, text in answers.items():
        k = int.from_bytes(hashlib.sha256(text.encode()).digest(), 'big')
        out[address(mul(k % pg.N, G), True)] = f'sha256 of {label}'
    bits = ''.join(f'{b:08b}' for b in b'gsmg.io/theseedisplanted')
    out[address(mul(int(bits, 2), G), True)] = 'the URL gsmg.io/theseedisplanted as a 192-bit integer'
    out[address(mul(int(bits[::-1], 2), G), True)] = 'the same 192 bits in reverse order'
    half = bytes.fromhex(HALF_PUBKEY)
    p = (int.from_bytes(half[1:33], 'big'), int.from_bytes(half[33:], 'big'))
    assert address(p, False) == HALF
    neighbours = {
        'P+G': add(p, G), 'P-G': add(p, (G[0], P_FIELD - G[1])),
        '2P': add(p, p), 'P/2': mul(pow(2, -1, pg.N), p),
    }
    return out, {address(pt, False): name for name, pt in neighbours.items()}


def when(tx):
    s = tx['status']
    day = datetime.datetime.fromtimestamp(s['block_time'], datetime.timezone.utc).strftime('%Y-%m-%d')
    return day, s['block_height']


def messages(tx):
    out = []
    for v in tx['vout']:
        if v.get('scriptpubkey_type') == 'op_return':
            raw = bytes.fromhex(v['scriptpubkey'])[1:]
            if raw and raw[0] <= 75:
                raw = raw[1:1 + raw[0]]
            elif raw and raw[0] == 76:
                raw = raw[2:2 + raw[1]]
            out.append(raw.decode('latin-1'))
    return out


def summary(addr, txs):
    received = sum(v['value'] for t in txs for v in t['vout'] if v.get('scriptpubkey_address') == addr)
    spent = sum(i['prevout']['value'] for t in txs for i in t['vin'] if i['prevout'].get('scriptpubkey_address') == addr)
    spends = [t for t in txs if any(i['prevout'].get('scriptpubkey_address') == addr for i in t['vin'])]
    latest = max(txs, key=lambda t: t['status']['block_height'])
    return {
        'transactions': len(txs), 'received_sat': received, 'spent_sat': spent, 'balance_sat': received - spent,
        'spending_transactions': len(spends),
        'inputs_signed': sum(1 for t in spends for i in t['vin'] if i['prevout'].get('scriptpubkey_address') == addr),
        'latest_transaction': dict(zip(('date', 'block'), when(latest))),
    }, spends


def main(run_dir):
    run = Path(run_dir)
    raw = run / 'chain_raw'
    raw.mkdir(parents=True, exist_ok=True)
    txs = {}
    for addr in (HALF, BETTER_HALF, MESSENGER, TIP_ADDRESS):
        txs[addr] = all_txs(addr)
        (raw / f'{addr}.json').write_text(json.dumps(txs[addr]), encoding='utf-8')
    checkpoints, neighbours = derived_addresses()
    state = {'checked_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
             'source': API}
    for name, addr in (('half', HALF), ('better_half', BETTER_HALF)):
        info, spends = summary(addr, txs[addr])
        info['spends'] = []
        for t in sorted(spends, key=lambda t: t['status']['block_height']):
            day, height = when(t)
            info['spends'].append({
                'date': day, 'block': height, 'txid': t['txid'], 'locktime': t['locktime'],
                'inputs': [{'from_tx': i['txid'], 'value': i['prevout']['value']} for i in t['vin']],
                'outputs': [{'to': v.get('scriptpubkey_address'), 'value': v['value']} for v in t['vout']],
                'messages': messages(t),
            })
        state[name] = info
    carrying = [t for t in txs[HALF] if messages(t)]
    state['half']['transactions_with_op_return'] = len(carrying)
    state['half']['of_which_spend_from_half'] = sum(
        any(i['prevout'].get('scriptpubkey_address') == HALF for i in t['vin']) for t in carrying)
    # the 2020 sweep: which outputs existed at the time and which were taken
    spent_refs = {(i['txid'], i['vout']) for t in txs[HALF] for i in t['vin']
                  if i['prevout'].get('scriptpubkey_address') == HALF}
    first_spend = state['half']['spends'][0]['block']
    early = [(t['txid'], n) for t in txs[HALF] if t['status']['block_height'] <= first_spend
             for n, v in enumerate(t['vout']) if v.get('scriptpubkey_address') == HALF]
    state['half']['outputs_held_at_first_spend'] = len(early)
    state['half']['of_which_swept'] = sum(ref in spent_refs for ref in early)

    info, spends = summary(MESSENGER, txs[MESSENGER])
    sent = []
    for t in sorted(spends, key=lambda t: (t['status']['block_height'], t['txid'])):
        day, height = when(t)
        for v in t['vout']:
            to = v.get('scriptpubkey_address')
            if to and to != MESSENGER:
                meaning = checkpoints.get(to) or (neighbours.get(to) and f'{neighbours[to]} of the prize public key, uncompressed')
                if to == HALF:
                    meaning = 'the prize address'
                if to == TIP_ADDRESS:
                    meaning = 'tip address hard-coded in a public Pollard-kangaroo tool; not derived from a puzzle answer'
                sent.append({'date': day, 'block': height, 'txid': t['txid'], 'to': to, 'value': v['value'],
                             'messages': messages(t), 'address_is': meaning})
    info['payments'] = sent
    state['messenger_3GSMG24'] = info
    halving = next(p for p in sent if p['to'] == HALF)
    sweep = state['half']['spends'][0]
    state['halving_link'] = {
        'message_tx': halving['txid'], 'message_block': halving['block'],
        'swept_by_prize_key_in_tx': sweep['txid'], 'sweep_block': sweep['block'],
        'same_block': halving['block'] == sweep['block'],
        'sweep_spends_message_output': any(i['from_tx'] == halving['txid'] for i in sweep['inputs']),
    }
    tip, _ = summary(TIP_ADDRESS, txs[TIP_ADDRESS])
    tip['only_sender'] = sorted({i['prevout'].get('scriptpubkey_address') for t in txs[TIP_ADDRESS] for i in t['vin']})
    state['tip_address_1NULY7'] = tip
    paid = {p['to'] for p in sent}
    state['checks'] = {
        'checkpoint_addresses_derived': len(checkpoints),
        'checkpoint_addresses_paid_by_messenger': sorted(a for a in checkpoints if a in paid),
        'all_eight_checkpoints_paid': all(a in paid for a in checkpoints),
        'neighbour_addresses_paid': {name: addr in paid for addr, name in neighbours.items()},
        'payments_to_addresses_with_no_derivation': sorted(p['to'] for p in sent if p['address_is'] is None),
    }
    state['derived'] = {'checkpoints': checkpoints, 'neighbours': neighbours}
    (run / 'chain_state.json').write_text(json.dumps(state, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({k: state[k] for k in ('checked_utc', 'halving_link', 'tip_address_1NULY7', 'checks')}, indent=1))
    for name in ('half', 'better_half'):
        s = state[name]
        print(name, s['balance_sat'], 'sat,', s['transactions'], 'txs,', s['spending_transactions'], 'spends, latest',
              s['latest_transaction'])
    for p in sent:
        print(p['date'], p['block'], p['to'], p['value'], p['messages'], '|', p['address_is'])


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else ROOT / 'runs' / '2026-11-10_state_refresh')
