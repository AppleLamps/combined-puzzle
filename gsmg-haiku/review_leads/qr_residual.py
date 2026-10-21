"""Test QR redundancy, not the already-known URL decode.
Dependency: python -m pip install --target review_leads/vendor qrcodegen
"""
from pathlib import Path
import sys,json
from PIL import Image
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'vendor'))
from qrcodegen import QrCode,QrSegment
im=Image.open(HERE.parent/'files/puzzle.png').convert('RGB')
# QR finder extent x=1..49 is seven 7-pixel modules; entire QR is 33 modules.
observed=[[max(im.getpixel((1+7*x+3,1290+7*y+3)))<128 for x in range(33)] for y in range(33)]
url='https://www.blockchain.com/btc/address/1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
results=[]
for en,ecc in [('L',QrCode.Ecc.LOW),('M',QrCode.Ecc.MEDIUM),('Q',QrCode.Ecc.QUARTILE),('H',QrCode.Ecc.HIGH)]:
    for mask in range(8):
        for eci in (None,26):
            segments=([QrSegment.make_eci(eci)] if eci is not None else [])+[QrSegment.make_bytes(url.encode())]
            try:q=QrCode.encode_segments(segments,ecc,4,4,mask,False)
            except ValueError:continue
            delta=[(x,y) for y in range(33) for x in range(33) if q.get_module(x,y)!=observed[y][x]]
            results.append(dict(ecc=en,mask=mask,eci=eci,different_modules=len(delta),delta=delta))
results.sort(key=lambda x:x['different_modules'])
(HERE/'qr-results.json').write_text(json.dumps(results,indent=2))
print(json.dumps([{k:v for k,v in x.items() if k!='delta'} for x in results],indent=2))
