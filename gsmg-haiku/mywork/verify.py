from lib import *
print('key1 compressed h160', hashes(1)[0], hashes(1)[0] == '751e76e8199196d454941c45d1b3a323f1433bd6')
# target pubkey sanity: hash of README pubkeys
pk = bytes.fromhex('04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a4649c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559')
print('target unc', h160(pk) == 'a9553269572a317e39f0f518cb87c1a0ee1dbae4')
print('target comp', h160(pk[:33].replace(b'\x04', b'\x03', 1)) == '06bbdc66fda09110435c79a86656a604c2d5c69b')
for name, pw in [('phase2.b64', 'causality'), ('phase3.b64', None), ('phase3.2.b64', 'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple')]:
    if pw is None:
        pw = 'causality' + 'Safenet' + 'Luna' + 'HSM' + '11110' + '0x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854' + 'B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1'
    p = dec(load(name), pw)
    print(name, None if p is None else (len(p), round(printable(p), 2)))
