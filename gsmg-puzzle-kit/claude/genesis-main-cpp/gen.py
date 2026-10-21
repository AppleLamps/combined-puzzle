"""Genesis construction in Satoshi's main.cpp, second pass (ledger row R35).

Source: bitcoin/bitcoin tag v0.3.10, main.cpp (copy here: main_v0.3.10.cpp), the only
release tag whose scriptSig comment sits on row 1616. Everything is pulled by script,
never retyped. Prints candidates on stdout; the retrodiction check runs first.

Usage: python3 gen.py main_v0.3.10.cpp main_v0.1.0.cpp > cands.txt
"""
import hashlib, re, sys
import base58  # pip install base58

src = open(sys.argv[1], encoding='latin-1').read().splitlines()
old = open(sys.argv[2], encoding='latin-1').read().splitlines()
row = lambda n: src[n - 1]

# --- retrodiction: phase 3 part 6 = "raw data after 4 on row 1616" -------------------
r1616 = row(1616)
assert 'scriptSig' in r1616, r1616
part6 = r1616.split(' 4 ', 1)[1].strip()
p3 = ('causality' 'Safenet' 'Luna' 'HSM' '11110' + part6 +
      'B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1')
assert hashlib.sha256(p3.encode()).hexdigest() == \
    '1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5'
print('# retrodiction: row 1616 of v0.3.10, text after " 4 ", rebuilds the phase-3 password (verified sha)',
      file=sys.stderr)

# --- pull the values ---------------------------------------------------------------
cb_row = next(i for i in range(1613, 1630) if 'coinbase' in row(i))
coinbase = re.search(r'coinbase ([0-9a-f]+)\)', row(cb_row)).group(1)
pk_rev = re.search(r'0x([0-9A-F]{130})', row(1618)).group(1)
pk = bytes.fromhex(pk_rev)[::-1].hex()              # the key in serialised order, 04...
assert pk.startswith('04') and len(pk) == 130
h160 = hashlib.new('ripemd160', hashlib.sha256(bytes.fromhex(pk)).digest()).hexdigest()
addr = base58.b58encode_check(b'\x00' + bytes.fromhex(h160)).decode()
cb = bytes.fromhex(coinbase)
# coinbase = 04 ffff001d | 01 04 | 45 <69 bytes headline>
assert cb[:1] == b'\x04' and cb[5:7] == b'\x01\x04' and cb[7] == len(cb) - 8
after4 = cb[7:].hex()                              # push length byte + headline
headline_hex = cb[8:].hex()
assert bytes.fromhex(headline_hex)[::-1].hex().upper() == part6[2:]
cblock = row(1623).split('// ', 1)[1].strip()
dump = '\n'.join(row(i).split('//', 1)[1][1:] for i in range(1623, 1628))
dbg_old = next(l for l in old if 'delete this later' in l).split('////', 1)[1].strip()

out = []
def add(note, *c): out.append('# ' + note); out.extend(c)
add('N1 "raw data": the scriptSig as raw serialised bytes, the coinbase hex the dump prints on row %d' % cb_row,
    coinbase, coinbase.upper(), '0x' + coinbase)
add('N2 "raw data after 4" read on the raw bytes: what follows the push of 4 (0104), with and without the length byte',
    after4, after4.upper(), headline_hex, headline_hex.upper(), '0x' + headline_hex.upper())
add('N3 the sibling code un-reversed: the genesis public key in serialised order, its hash160 and address',
    pk, pk.upper(), '0x' + pk.upper(), h160, addr)
add('N4 the source the row number names: the release whose row 1616 is the scriptSig line',
    'v0.3.10', '0.3.10', 'bitcoinv0.3.10', 'bitcoin0.3.10', 'Bitcoin v0.3.10')
add('N5 "a temporary dissemination": Satoshi\'s temporary debug print that disseminated these codes',
    'debugprint', 'debug print', dbg_old.replace(' ', '').replace(',', ''), dbg_old)
add('N6 the debug print\'s own output as the source keeps it: the CBlock line, and the five dump rows',
    cblock, dump.replace('\n', ''))
MULTI = [dump, dump + '\n']  # newline-bearing forms, tested by run_multi.py
add('N7 "row 1616" as a whole row, as written and stripped of indentation and comment marks',
    r1616, r1616.strip(), r1616.split('// ', 1)[1].strip())
print('\n'.join(dict.fromkeys(out)))
print('# address %s' % addr, file=sys.stderr)
