"""Check pinned Esplora transaction snapshots; --live verifies against API.

Offline checks compare a manifest with saved explorer JSON and check accounting.
Use --live for independent comparison against a Bitcoin explorer's current
transaction data. Failure to reach the API is never silently skipped.
"""
import argparse
import datetime as dt
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib

MANIFEST = Path(lib.REPO) / 'source' / 'onchain' / 'manifest.json'


def require(condition, message):
    if not condition:
        raise AssertionError(message)
    print('PASS ' + message)


def load_url(url):
    with urllib.request.urlopen(url, timeout=20) as response:
        return json.load(response)


def output_matches(tx, item, vout=None):
    outputs = tx['vout']
    if vout is not None:
        outputs = [outputs[vout]]
    return any(out['value'] == item['value'] and
               out.get('scriptpubkey_address') == item['address'] for out in outputs)


def op_return_matches(tx, message):
    encoded = message.encode('utf-8')
    return any(encoded in bytes.fromhex(out['scriptpubkey']) for out in tx['vout']
               if out.get('scriptpubkey_type') == 'op_return' or
               out['scriptpubkey'].startswith('6a'))


def verify_transactions(manifest, txs, live=False):
    records = manifest['transactions']
    for name, item in records.items():
        tx = txs[name]
        require(tx['txid'] == item['txid'], name + ' txid')
        require(tx['status']['confirmed'], name + ' confirmed')
        if 'height' in item:
            require(tx['status']['block_height'] == item['height'], name + ' height')
        if 'date_utc' in item:
            date = dt.datetime.fromtimestamp(
                tx['status']['block_time'], dt.timezone.utc).date().isoformat()
            require(date == item['date_utc'], name + ' UTC date')
        if 'locktime' in item:
            require(tx['locktime'] == item['locktime'], name + ' locktime')
        if 'fee' in item:
            require(tx['fee'] == item['fee'], name + ' fee')
        if 'op_return_utf8' in item:
            require(op_return_matches(tx, item['op_return_utf8']), name + ' OP_RETURN')

    half = records['halving_message']
    require(output_matches(txs['halving_message'], {
        'address': manifest['prize'], 'value': half['prize_output']['value']
    }, half['prize_output']['vout']), 'Halving output to prize')
    for name in ('first_split', 'second_split'):
        item = records[name]
        tx = txs[name]
        require(len(tx['vin']) == len(item['inputs']), name + ' input count')
        require(len(tx['vout']) == len(item['outputs']), name + ' output count')
        for index, inp in enumerate(item['inputs']):
            vin = tx['vin'][index]
            require((vin['txid'], vin['vout'], vin['prevout']['value']) ==
                    (inp['txid'], inp['vout'], inp['value']),
                    name + ' vin ' + str(index))
            require(vin['prevout']['scriptpubkey_address'] == manifest['prize'],
                    name + ' input belongs to prize')
            script_sig = bytes.fromhex(vin['scriptsig'])
            require(lib.uncompressed_point(lib.PRIZE_POINT) in script_sig,
                    name + ' scriptSig exposes prize public key')
        for index, out in enumerate(item['outputs']):
            require(output_matches(tx, out, index), name + ' vout ' + str(index))
    for out in records['dual_funding']['outputs']:
        require(output_matches(txs['dual_funding'], out, out['vout']),
                'dual funding vout ' + str(out['vout']))
    neighbor = records['neighbor_message']
    for relation, address in neighbor['outputs'].items():
        require(output_matches(txs['neighbor_message'], {
            'address': address, 'value': neighbor['output_value_each']
        }), 'neighbor ' + relation)
    require(any(vin['prevout'].get('scriptpubkey_address') ==
                manifest['funding_vanity_address_unattributed'] for vin in txs['neighbor_message']['vin']),
            'neighbor transaction funded by unattributed vanity address')
    require(any(vin['prevout'].get('scriptpubkey_address') ==
                manifest['funding_vanity_address_unattributed'] for vin in txs['halving_message']['vin']),
            'Halving transaction funded by unattributed vanity address')
    if live:
        for name in ('halving_message', 'first_split'):
            item = records[name]
            tx = txs[name]
            # Esplora's /txid/:index returns the bare txid, not a JSON array.
            url = f"https://blockstream.info/api/block/{tx['status']['block_hash']}/txid/{item['block_position']}"
            with urllib.request.urlopen(url, timeout=20) as response:
                observed = response.read().decode().strip()
            require(observed == item['txid'], name + ' block position')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true', help='verify pinned data against Blockstream API')
    args = parser.parse_args()
    m = json.loads(MANIFEST.read_text(encoding='utf-8'))
    t = m['transactions']
    require(t['first_split']['inputs'][2]['txid'] == t['halving_message']['txid'] and
            t['first_split']['inputs'][2]['vout'] == t['halving_message']['prize_output']['vout'],
            'Halving 700-sat outpoint spent by first split')
    require(t['second_split']['inputs'][0]['txid'] == t['first_split']['txid'] and
            t['second_split']['inputs'][0]['value'] == t['first_split']['outputs'][0]['value'],
            'first split change spent by second split')
    dual_prize = t['dual_funding']['outputs'][0]
    dual_spend = t['second_split']['inputs'][2]
    require((dual_spend['txid'], dual_spend['vout'], dual_spend['value']) ==
            (t['dual_funding']['txid'], dual_prize['vout'], dual_prize['value']) and
            dual_prize['address'] == m['prize'],
            '2023 dual funding prize output spent by second split')
    require(t['halving_message']['height'] == t['first_split']['height'] and
            t['first_split']['block_position'] == t['halving_message']['block_position'] + 1,
            'Halving transaction directly precedes spend in same block')
    for name in ('first_split', 'second_split'):
        tx = t[name]
        require(sum(i['value'] for i in tx['inputs']) ==
                sum(o['value'] for o in tx['outputs']) + tx['fee'], name + ' accounting')
        require(tx['locktime'] != (630000 if name == 'first_split' else 840000),
                name + ' locktime is not halving height')
    require(t['neighbor_message']['outputs'] == lib.RELATED_ADDRESSES,
            'manifest neighbor addresses match verifier targets')
    snapshots = {name: json.loads(
        (MANIFEST.parent / (item['txid'] + '.json')).read_text(encoding='utf-8'))
        for name, item in t.items()}
    verify_transactions(m, snapshots)
    if args.live:
        live_txs = {name: load_url(m['source'].format(txid=item['txid']))
                    for name, item in t.items()}
        verify_transactions(m, live_txs, live=True)
        print('SUMMARY: saved snapshots and live transaction fields verified')
    else:
        print('SUMMARY: saved explorer snapshots verified; pass --live for independent chain checks')


if __name__ == '__main__':
    main()
