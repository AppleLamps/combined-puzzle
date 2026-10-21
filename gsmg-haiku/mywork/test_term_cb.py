from lib import *

term = load('terminal.b64')
cb_plain = open(r'c:\gsmg-puzzle-clean\derived\checkerboard-plaintext.txt').read().strip()
cb_digits = open(r'c:\gsmg-puzzle-clean\derived\checkerboard-digits.txt').read().strip()

print("Testing checkerboard plaintext on terminal.b64:")
for text in [
    cb_plain,
    cb_plain.lower(),
    cb_digits,
    "HALFANDBETTERHALF",
    "halfandbetterhalf",
    "HALF",
    "half",
    "BETTERHALF",
    "betterhalf",
    "Raising the stakes without extra chances of winning",
    "raising the stakes without extra chances of winning",
    "raisingthestakeswithoutextrachancesofwinning",
    "A fubcd-king & oracle-queen, thingky mvps, on a sad board but as wide as the first one seen.",
    "Afubcd-king&oracle-queen,thingkymvps,onasadboardbutaswideasthefirstoneseen.",
    "fubcd-king",
    "oracle-queen",
    "thingky mvps",
    "fubcd",
    "oracle",
    "thingky",
    "mvps"
]:
    # sha256 hex
    pw_hex = hashlib.sha256(text.encode('utf-8')).hexdigest()
    p = dec(term, pw_hex, hashed=False)
    if p is not None:
        print(f"MATCH (sha_hex)! {text[:40]!r} -> pr={printable(p):.2f}")
    
    # raw
    p = dec(term, text, hashed=False)
    if p is not None:
        print(f"MATCH (raw)! {text[:40]!r} -> pr={printable(p):.2f}")
