from reconstruct import *
from coincurve import PrivateKey
import sys as _sys
_sys.path.insert(0, str(R.parents[1] / 'tools'))
import prize_gate  # shared gate: Half and Better Half, both serializations
import random
Qtarget=bytes.fromhex('04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a4649c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559')
target=hashlib.new('ripemd160',hashlib.sha256(Qtarget).digest()).digest()
assert target.hex()=='a9553269572a317e39f0f518cb87c1a0ee1dbae4'
seen=set();hits=[]
def scalar(k,where):
    if len(k)!=32 or k in seen:return
    seen.add(k)
    # Was Half's public key only; a correct Better Half key could never match.
    if prize_gate.gate_bytes(k):hits.append(dict(source=where,key=k.hex()))
containers={n:base64.b64decode((R/'inputs'/f'{n}.b64').read_bytes()) for n in ['terminal','salphaseion-short','cosmic-duality']}
binary=json.loads((R/'companion_tests.json').read_text())['binary'];objects={bytes.fromhex(x['hex']):x for x in binary}
trials=0;padding=[];structured=[]
for raw,source in objects.items():
    # Direct contiguous raw keys, including little-endian representation.
    for i in range(len(raw)-31):
        scalar(raw[i:i+32],dict(kind='companion raw window',offset=i,source=source))
        scalar(raw[i:i+32][::-1],dict(kind='companion reversed window',offset=i,source=source))
    scalar(hashlib.sha256(raw).digest(),dict(kind='SHA256 complete companion bytes',source=source))
    for form,pw in [('raw',raw),('sha256hex',hashlib.sha256(raw).hexdigest().encode())]:
        for name,ct in containers.items():
            body=decrypt(ct,pw);trials+=1
            if body is None:continue
            rec=dict(source=source,form=form,container=name,plaintext_hex=body.hex());padding.append(rec)
            for i in range(len(body)-31):scalar(body[i:i+32],dict(kind='decrypted raw window',offset=i,parent=rec))
            if all(x in (9,10,13) or 32<=x<=126 for x in body) or body.startswith(b'Salted__'):structured.append(rec)
            if len(body)==64 and all(chr(x) in '0123456789abcdefABCDEF' for x in body):scalar(bytes.fromhex(body.decode()),dict(kind='decrypted hex scalar',parent=rec))
# Independent generator for a planted AES control using a decoded 2-bit message.
answer=b'read the entire message and preserve every bit'
bits=''.join(f'{x:08b}' for x in answer);symbols=''.join('bcde'[int(bits[i:i+2],2)] for i in range(0,len(bits),2))
recovered=''.join(f'{"bcde".index(c):02b}' for c in symbols);candidate=bytes(int(recovered[i:i+8],2) for i in range(0,len(recovered),8))
pw=hashlib.sha256(candidate).hexdigest().encode();salt=bytes.fromhex('1928374655aabbcc');key=b'';prev=b''
while len(key)<48:prev=hashlib.sha256(prev+pw+salt).digest();key+=prev
plain=b'Positive control: the complete message is recovered.';pad=16-len(plain)%16
ct=b'Salted__'+salt+AES.new(key[:32],AES.MODE_CBC,key[32:48]).encrypt(plain+bytes([pad])*pad)
assert decrypt(ct,hashlib.sha256(answer).hexdigest().encode())==plain
# Scalar checking control does not depend on the unknown prize scalar.
one=PrivateKey(bytes.fromhex('00'*31+'01')).public_key.format(compressed=False)
assert one.hex().startswith('0479be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798')
result=dict(binary_models=len(binary),distinct_byte_objects=len(objects),aes_trials=trials,padding_only=len(padding),structured_outputs=structured,distinct_scalars=len(seen),prize_hits=hits,controls=['known phase32 through reconstruct.py','2-bit decode -> sha256 -> planted AES exact recovery','secp256k1 generator from scalar 1'],scope='All 24 bijections of b/c/d/e to two-bit values, both bit directions, 7/8-bit grouping at every alignment; raw and SHA256-hex passwords, SHA256 EVP, all three real containers. Scalar tests: all contiguous raw 32-byte windows and their reversals, complete-object SHA256, plus raw windows in padding-valid decrypts.')
(R/'oracle_checks.json').write_text(json.dumps(result,indent=2));(R/'oracle_padding.json').write_text(json.dumps(padding,indent=2));print(json.dumps(result,indent=2))
