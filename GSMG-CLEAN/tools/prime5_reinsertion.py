#!/usr/bin/env python3
"""Reinsert the removed prime 5 into the pre-Beaufort source record, then gate.

No AES. The family is the one sealed in
runs/2026-11-27_prime5_reinsertion/PREREG.json. Scalars are enumerated and
hashed before any prize comparison.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import prize_gate as pg  # noqa: E402
import prereg  # noqa: E402

RUN = ROOT / 'runs' / '2026-11-27_prime5_reinsertion'
DATA = ROOT / 'data'
N = pg.N
PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89)
RAW_SHA256 = 'bd7a29432546c67c4170e0c523ddbf43ae82d20ee187d1b4dbf7907a0faf4c7b'
WINDOW_HEX = 'c35b3af65fc7f8c7c13af65f60c02cc9c8c9cad1cc2560c7c03f25c7cd3f5bf8'
ANCHORS = {
    479: 'PRIVATEKEY',
    1021: 'SOURCECODES',
    1103: 'PRIMEBASICS',
    1198: 'SEVENINTERTWINEDPASSWORDS',
}


def raw_record():
    plaintext = (DATA / 'phase3_2_plaintext.bin').read_bytes()
    marker = b'One for one, four for one.\r\n\r\n'
    start = plaintext.index(marker) + len(marker)
    end = plaintext.index(b'\r\n\r\n151659', start)
    raw = plaintext[start:end]
    if hashlib.sha256(raw).hexdigest() != RAW_SHA256 or raw[479:511].hex() != WINDOW_HEX:
        raise SystemExit('raw source record does not match the authenticated constants')
    if start != 447 or raw != plaintext[447:1986]:
        raise SystemExit('raw source record is not phase3.2 bytes [447:1986]')
    return raw


def verify_background(raw):
    letters = (DATA / 'architect_letters_1539.txt').read_text().strip()
    if len(letters) != 1539:
        raise SystemExit('Architect letter record is not 1539 symbols')
    for offset, word in ANCHORS.items():
        if letters[offset:offset + len(word)] != word:
            raise SystemExit(f'Architect offset {offset} is not {word}')
    colors = (DATA / 'poster_spiral_bits.txt').read_text().splitlines()[1]
    if len(colors) != 24 or set(colors) != set('BY'):
        raise SystemExit('poster marker colours are not 24 B/Y markers')
    yellow = sum(prime for prime, color in zip(PRIMES, colors) if color == 'Y')
    blue = sum(prime for prime, color in zip(PRIMES, colors) if color == 'B')
    if (yellow, blue) != (479, 484):
        raise SystemExit(f'colour sums are {yellow}/{blue}, not 479/484')
    if colors[PRIMES.index(5)] != 'B' or blue - 5 != 479:
        raise SystemExit('the blue imbalance is not the prime 5')
    return colors


def operands():
    primes = bytes(PRIMES)
    return (
        ('prime5', b'\x05'),
        ('primes24', primes),
        ('primes24-mod256', bytes(prime % 256 for prime in PRIMES)),
        ('pair-484-479', (484).to_bytes(2, 'big') + (479).to_bytes(2, 'big')),
    )


def positions(length, base):
    found = []
    for prime in PRIMES:
        index = prime - 1 if base == 1 else prime
        if 0 <= index < length:
            found.append(index)
    return found


def apply_at_positions(buffer, spots, operand, mode):
    out = bytearray(buffer)
    if mode == 'insert':
        ranked = sorted(enumerate(spots), key=lambda item: item[1], reverse=True)
        for rank, index in ranked:
            out.insert(index, operand[rank % len(operand)])
        return bytes(out)
    for rank, index in enumerate(spots):
        byte = operand[rank % len(operand)]
        if mode == 'xor':
            out[index] ^= byte
        elif mode == 'add':
            out[index] = (out[index] + byte) & 0xFF
        else:
            raise ValueError(mode)
    return bytes(out)


def append_after_window(buffer, operand, window_is_buffer):
    if window_is_buffer:
        return buffer + operand
    return buffer[:511] + operand + buffer[511:]


def xor_window(buffer, window_is_buffer):
    out = bytearray(buffer)
    start, end = (0, len(out)) if window_is_buffer else (479, 511)
    for index in range(start, end):
        out[index] ^= 0x05
    return bytes(out)


def window_bytes(result, window_is_buffer):
    if window_is_buffer:
        return result[:32] if len(result) >= 32 else None
    return result[479:511] if len(result) >= 511 else None


def enumerate_records(raw):
    window = raw[479:511]
    if len(window) != 32:
        raise SystemExit('479 window is not 32 bytes')
    records = []
    ops = operands()
    for target_name, buffer, window_is_buffer in (
        ('record', raw, False),
        ('window', window, True),
    ):
        for base in (0, 1):
            spots = positions(len(buffer), base)
            for op_name, operand in ops:
                for mode in ('xor', 'add', 'insert'):
                    result = apply_at_positions(buffer, spots, operand, mode)
                    records.append((f'{target_name}/{mode}/{op_name}/base{base}', result, window_is_buffer))
        for op_name, operand in ops:
            result = append_after_window(buffer, operand, window_is_buffer)
            records.append((f'{target_name}/append/{op_name}', result, window_is_buffer))
        result = xor_window(buffer, window_is_buffer)
        records.append((f'{target_name}/xor05-window', result, window_is_buffer))
    scalars = []
    for label, result, window_is_buffer in records:
        direct = window_bytes(result, window_is_buffer)
        if direct is None or len(direct) != 32:
            raise SystemExit(f'{label} has no 32-byte window')
        scalars.append((f'{label}/direct', direct))
        scalars.append((f'{label}/sha256', hashlib.sha256(result).digest()))
    return scalars


def stream_hash(scalars):
    return hashlib.sha256(b''.join(sorted(scalar for _label, scalar in scalars))).hexdigest()


def in_range(scalar):
    value = int.from_bytes(scalar, 'big')
    return 1 <= value < N


def gate(scalar):
    value = int.from_bytes(scalar, 'big')
    unc, comp = pg.public_keys(value)
    hits = []
    if unc == pg.HALF_PUBLIC_UNCOMPRESSED:
        hits.append('half-uncompressed-pubkey')
    hashes = {'uncompressed': pg.hash160(unc), 'compressed': pg.hash160(comp)}
    for form, digest in hashes.items():
        if digest == pg.HALF_H160:
            hits.append(f'half-hash160-{form}')
        if digest == pg.BETTER_H160:
            hits.append(f'better-half-hash160-{form}')
    return hits


def selftest():
    if pg.hash160(pg.HALF_PUBLIC_UNCOMPRESSED) != pg.HALF_H160:
        raise SystemExit('Half pubkey does not hash to the Half address')
    if pg.address_from_public(pg.HALF_PUBLIC_UNCOMPRESSED) != pg.HALF_ADDRESS:
        raise SystemExit('Half pubkey does not encode the Half address')
    _unc, comp = pg.public_keys(1)
    planted = pg.gate_scalar(1, {'planted': pg.hash160(comp)})
    if planted is None or pg.gate_scalar(1) is not None:
        raise SystemExit('the gate failed its planted control')
    if pg.address_from_public(comp) != '1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH':
        raise SystemExit('key 1 did not derive its compressed address')


def main():
    bound = prereg.verify(RUN)
    statement = prereg.load(RUN)
    if statement['candidate_bound'] != 116 or statement['aes_use'] != 'none':
        raise SystemExit('sealed statement is not this 116-scalar, no-AES family')
    selftest()
    raw = raw_record()
    verify_background(raw)
    scalars = enumerate_records(raw)
    if len(scalars) != statement['candidate_bound']:
        raise SystemExit(f'enumerated {len(scalars)} scalars, sealed bound is {statement["candidate_bound"]}')
    digest = stream_hash(scalars)
    print(f'CANDIDATES {len(scalars)}')
    print(f'STREAM_SHA256 {digest}')
    matches = []
    gated = 0
    for label, scalar in scalars:
        if not in_range(scalar):
            continue
        gated += 1
        hits = gate(scalar)
        if hits:
            matches.append({'label': label, 'scalar': scalar.hex(), 'hits': hits})
    verdict = 'PRIZE MATCH' if matches else 'NO MATCH'
    print(f'{len(scalars)} {digest} {verdict}')
    payload = {
        'prereg_sha256': bound,
        'candidates': len(scalars),
        'gated': gated,
        'rejected_out_of_range': len(scalars) - gated,
        'stream_sha256': digest,
        'stream_rule': 'sha256 of the sorted raw 32-byte scalars concatenated, duplicates retained',
        'verdict': verdict,
        'matches': matches,
        'identical_operands': {
            'primes24': bytes(PRIMES).hex(),
            'primes24-mod256': bytes(prime % 256 for prime in PRIMES).hex(),
            'byte_identical': bytes(PRIMES) == bytes(prime % 256 for prime in PRIMES),
        },
    }
    (RUN / 'results.json').write_text(json.dumps(payload, indent=1) + '\n', encoding='utf-8')
    labels = '\n'.join(f'{scalar.hex()} {label}' for label, scalar in scalars) + '\n'
    (RUN / 'scalars.txt').write_text(labels, encoding='utf-8')


if __name__ == '__main__':
    main()
