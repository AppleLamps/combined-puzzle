#!/usr/bin/env python3
"""Everything about the genesis block, derived and self-verified.

Nothing here is recalled: the block is rebuilt from protocol constants and the
reconstruction is proved correct by its own double-SHA256 matching the known
genesis hash. If any byte were wrong the hash would not match.
"""
import hashlib, struct

MSG = b'The Times 03/Jan/2009 Chancellor on brink of second bailout for banks'
PUSH4 = bytes.fromhex('04ffff001d')      # push 4 bytes: the bits/nBits value 0x1d00ffff LE
PUSH1 = bytes.fromhex('0104')            # push 1 byte: 0x04
SS    = PUSH4 + PUSH1 + bytes([len(MSG)]) + MSG
tx  = struct.pack('<I',1) + b'\x01' + b'\x00'*32 + b'\xff'*4
tx += bytes([len(SS)]) + SS + b'\xff'*4
PK  = bytes.fromhex('4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb6'
                    '49f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac')
tx += b'\x01' + struct.pack('<Q', 5_000_000_000) + bytes([len(PK)]) + PK + struct.pack('<I',0)
MERKLE = hashlib.sha256(hashlib.sha256(tx).digest()).digest()
HDR = (struct.pack('<I',1) + b'\x00'*32 + MERKLE +
       struct.pack('<III', 1231006505, 0x1d00ffff, 2083236893))
GH  = hashlib.sha256(hashlib.sha256(HDR).digest()).digest()[::-1].hex()
RAW = HDR + b'\x01' + tx
assert GH == '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f'

def b58c(payload):
    A='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    chk=hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    n=int.from_bytes(payload+chk,'big'); s=''
    while n: n,r=divmod(n,58); s=A[r]+s
    return '1'*(len(payload+chk)-len((payload+chk).lstrip(b'\0')))+s
h160=lambda b: hashlib.new('ripemd160',hashlib.sha256(b).digest()).digest()

from datetime import datetime, timezone
print('='*74)
print('GENESIS BLOCK — reconstructed and VERIFIED by its own hash')
print('='*74)
print(f'block hash        {GH}')
print(f'                  matches the known genesis hash -> reconstruction is correct\n')
print('--- header, 80 bytes ---')
print(f'  version         1                    {HDR[0:4].hex()}')
print(f'  prev block      all zero             {HDR[4:36].hex()[:32]}…')
print(f'  merkle root     {MERKLE[::-1].hex()}')
print(f'  nTime           1231006505           {datetime.fromtimestamp(1231006505,timezone.utc):%Y-%m-%d %H:%M:%S} UTC')
print(f'  nBits           0x1d00ffff           difficulty 1')
print(f'  nonce           2083236893')
print(f'  raw header      {HDR.hex()}\n')
print('--- coinbase transaction ---')
print(f'  txid            {MERKLE[::-1].hex()}   (== merkle root: a single tx)')
print(f'  output          50.00000000 BTC to an uncompressed P2PK script')
# PK is the scriptPubKey: 0x41 push, 65-byte pubkey, 0xac OP_CHECKSIG.
# Strip BOTH ends -- keeping the trailing 0xac yields a bogus address.
PUB = PK[1:-1]
_addr = b58c(bytes([0]) + h160(PUB))
assert _addr == '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', 'address derivation wrong'
print(f'  pubkey          {PUB.hex()}')
print(f'  hash160         {h160(PUB).hex()}')
print(f'  P2PKH address   {_addr}   (verified against the known genesis address)')
print(f'  spendable?      NO — the genesis coinbase is not in the UTXO set, by consensus\n')
print('--- the scriptSig: what "row 1616" holds ---')
print(f'  {SS.hex()}')
print(f'  breakdown:')
print(f'    04            push 4 bytes')
print(f'    ffff001d        -> 0x1d00ffff little-endian, the nBits value')
print(f'    01            push 1 byte')
print(f'    04              -> the number 4          <<-- "raw data AFTER 4"')
print(f'    45            push 0x45 = 69 bytes')
print(f'    {MSG.hex()[:56]}…')
print(f'      = {MSG.decode()!r}\n')
print('--- line 1616 of Satoshi\'s main.cpp, as the comment renders it ---')
rev = MSG[::-1].hex().upper()
line = f'// txNew.vin[0].scriptSig     = 486604799 4 0x{rev}'
print(f'  486604799 = 0x{486604799:08x} = the nBits push')
print(f'  4         = the second push          <<-- the "4" in "after 4"')
print(f'  0x{rev[:60]}…')
print(f'  that hex is the message BYTE-REVERSED: 73="s" 6b="k" 6e="n" 61="a" 62="b" -> "sknab" = "banks" backwards')
print(f'  length of "0x" + hex = 2 + {len(rev)} = {2+len(rev)}   <<-- HUNDRED FOURTY\n')
print('--- sizes ---')
print(f'  full raw block  {len(RAW)} bytes')
print(f'  coinbase tx     {len(tx)} bytes')
print(f'  scriptSig       {len(SS)} bytes')
print(f'  message         {len(MSG)} bytes = {len(MSG)*2} hex chars\n')
print('--- full raw block hex ---')
for i in range(0, len(RAW), 32):
    print(f'  {i:04d}  {RAW[i:i+32].hex()}')
