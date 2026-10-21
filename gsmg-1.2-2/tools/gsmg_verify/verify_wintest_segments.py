import sys
import hashlib, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib
import coincurve, base58

PASS=[]; FAIL=[]
def check(name, cond, detail=''):
    (PASS if cond else FAIL).append(name)
    print(('PASS ' if cond else 'FAIL '), name, ' ', detail)

# ---- win test / target self-consistency ----
# Extracted programmatically from the dossier (never hand-retyped) to avoid transcription error.
_dlines = lib.dossier_lines()
_uncomp_hex = _dlines[76].split(None,1)[1].strip() + _dlines[77].strip()
_comp_hex = _dlines[78].split(None,1)[1].strip()
UNCOMP = bytes.fromhex(_uncomp_hex)
COMP   = bytes.fromhex(_comp_hex)
check('uncompressed pubkey length 65', len(UNCOMP)==65, len(UNCOMP))
check('compressed pubkey length 33', len(COMP)==33, len(COMP))
check('hash160(uncompressed) == prize target', lib.h160(UNCOMP)==lib.PRIZE_H160, lib.h160(UNCOMP))
check('hash160(compressed)   == compressed-twin target', lib.h160(COMP)==lib.COMPRESSED_TWIN_H160, lib.h160(COMP))

def b58_encode_addr(h160hex, version=0x00):
    payload = bytes([version]) + bytes.fromhex(h160hex)
    chk = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return base58.b58encode(payload+chk).decode()

addr_uncomp = b58_encode_addr(lib.PRIZE_H160)
check('base58 address from prize h160 == 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe',
      addr_uncomp=='1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe', addr_uncomp)

addr_comptwin = b58_encode_addr(lib.COMPRESSED_TWIN_H160)
check('base58 address from compressed-twin h160 == 1cc6xayvqpeetixmuXDRsGug7GKyoRdxP',
      addr_comptwin=='1cc6xayvqpeetixmuXDRsGug7GKyoRdxP', addr_comptwin)

addr_sentinel = b58_encode_addr(lib.SENTINEL_H160)
check('base58 address from sentinel h160 == 17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa',
      addr_sentinel=='17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa', addr_sentinel)

# ---- public scalar-1 control ----
pk1 = coincurve.PrivateKey(bytes.fromhex('00'*31 + '01'))
comp1 = pk1.public_key.format(True)
uncomp1 = pk1.public_key.format(False)
check('scalar=1 compressed hash160 == pinned control',
      lib.h160(comp1)=='751e76e8199196d454941c45d1b3a323f1433bd6', lib.h160(comp1))
addr1 = b58_encode_addr(lib.h160(uncomp1))
check('scalar=1 uncompressed address == 1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm', addr1=='1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm', addr1)

# negative control: random key must not match
import os
rand_priv = os.urandom(32)
check('random 32B key does not match prize (negative control)', not lib.win_raw(rand_priv), lib.h160(coincurve.PrivateKey(rand_priv).public_key.format(True)))

# ---- SalPhaseIon textarea decode rules (section 6.1/6.2), applied to REAL textarea ----
textarea = open(str(Path(__file__).resolve().parent / 'out' / 'textarea.txt')).read()
check('textarea length 1075', len(textarea)==1075, len(textarea))

def rule1(block):
    bits = ''.join('0' if ch=='a' else '1' for ch in block)
    out = bytearray()
    for i in range(0, len(bits), 8):
        out.append(int(bits[i:i+8], 2))
    return bytes(out)

def rule2(block):
    d = ''.join('0' if c=='o' else str(ord(c)-96) for c in block)
    n = int(d)
    h = hex(n)[2:]
    if len(h) % 2:
        h = '0'+h
    return bytes.fromhex(h)

seg_dbbi   = textarea[0:91]
seg_ab1    = textarea[91:195]
seg_faed   = textarea[195:765]
seg_z1     = textarea[765:766]
seg_lastwords = textarea[766:829]
seg_z2     = textarea[829:830]
seg_thispw = textarea[830:859]
seg_z3     = textarea[859:860]
seg_lit1   = textarea[860:895]
seg_b64a   = textarea[895:959]
seg_ab2    = textarea[959:999]
seg_b64b   = textarea[999:1063]
seg_lit2   = textarea[1063:1075]

check('z separators are literal z', (seg_z1,seg_z2,seg_z3)==('z','z','z'), (seg_z1,seg_z2,seg_z3))

msl = rule1(seg_ab1)
check('matrixsumlist decode', msl==b'matrixsumlist', msl)

lwb = rule2(seg_lastwords)
check('lastwordsbeforearchichoice decode', lwb==b'lastwordsbeforearchichoice', lwb)

tpw = rule2(seg_thispw)
check('thispassword decode', tpw==b'thispassword', tpw)

enter = rule1(seg_ab2)
check('enter decode', enter==b'enter', enter)

check('literal1 == shabefourfirsthintisyourlastcommand', seg_lit1=='shabefourfirsthintisyourlastcommand', seg_lit1)
check('literal2 == shabefanstoo', seg_lit2=='shabefanstoo', seg_lit2)

full_short_b64 = seg_b64a + seg_b64b
dossier_sps_b64 = lib.block_joined(17, sep='')
check('reconstructed SalPhaseIon-short b64 (from textarea segments) == dossier block 17',
      full_short_b64 == dossier_sps_b64, '')

print('\ndbbi   [0:91]  :', seg_dbbi)
print('faed   [195:765] len', len(seg_faed))
print('faed head:', seg_faed[:80])

# faed symbol counts
from collections import Counter
faedcnt = Counter(seg_faed)
print('faed symbol counts:', dict(sorted(faedcnt.items())))
check('faed length 570', len(seg_faed)==570, len(seg_faed))
EXPECTED_FAED = {'a':54,'b':49,'c':52,'d':49,'e':69,'f':57,'g':107,'h':58,'i':75}
check('faed symbol counts match dossier', dict(faedcnt)==EXPECTED_FAED, dict(faedcnt))

print('\nSUMMARY:', len(PASS), 'passed,', len(FAIL), 'failed')
if FAIL: print('FAILURES', FAIL)
sys.exit(1 if FAIL else 0)
