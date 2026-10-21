"""New hypothesis: prize scalar = +/- a known puzzle seed + a bounded offset.
Baby-step/giant-step tests a large interval in square-root work. Read-only.
Usage: python review_leads/vanity_offset.py --bits 32
Only needs coincurve, already present in this workspace's Python environment.
"""
from pathlib import Path
import argparse,hashlib,json,math,time
from coincurve import PublicKey,PrivateKey
ROOT=Path(__file__).resolve().parents[1]
N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Q=PublicKey(bytes.fromhex('03f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464'))
TARGET='a9553269572a317e39f0f518cb87c1a0ee1dbae4'
G=PrivateKey.from_int(1).public_key
OPS=0

def point(n):
    n%=N
    return PrivateKey.from_int(n).public_key if n else None

def enc(p):return p.format() if p is not None else b''

def add(a,b):
    global OPS
    OPS+=1
    if a is None:return b
    if b is None:return a
    try:return PublicKey.combine_keys([a,b])
    except ValueError:
        aa,bb=a.point(),b.point()
        if aa[0]==bb[0] and aa[1]!=bb[1]:return None
        raise

def make_table(width):
    m=math.isqrt(width-1)+1
    table={};p=None
    for j in range(m):table[enc(p)]=j;p=add(p,G)
    return m,table,point(-m)

def interval(target,seed,width,tabledata):
    m,table,step=tabledata
    lo=seed-width//2
    current=add(target,point(-lo))
    for i in range((width+m-1)//m):
        j=table.get(enc(current))
        if j is not None and i*m+j<width:return (lo+i*m+j)%N,i*m+j-width//2
        current=add(current,step)
    return None

def seeds():
    part6='0x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854'
    fen='B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1'
    texts={
       'phase1':'theflowerblossomsthroughwhatseemstobeaconcretesurface',
       'phase2':'causality',
       'phase3':'causalitySafenetLunaHSM11110'+part6+fen,
       'phase3.2':'jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple',
       'checkerboard-digits':(ROOT/'derived/checkerboard-digits.txt').read_text().strip(),
       'checkerboard-plain':(ROOT/'derived/checkerboard-plaintext.txt').read_text().strip(),
       'poster-title-address':'GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe',
       'target-address':'1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'}
    nums={name:int.from_bytes(hashlib.sha256(t.encode()).digest(),'big') for name,t in texts.items()}
    b=b'gsmg.io/theseedisplanted'
    nums['poster-raw']=int.from_bytes(b,'big')
    nums['poster-bit-reversed']=int(''.join(f'{c:08b}' for c in b)[::-1],2)
    return nums

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--bits',type=int,default=32);args=ap.parse_args()
    if not 8<=args.bits<=36:raise SystemExit('bounded to bits 8..36')
    # Boundary, negative-offset, and identity controls for this new algorithm only.
    tiny=make_table(256)
    for offset in (-128,-1,0,1,127):
        assert interval(point(1000+offset),1000,256,tiny)==(1000+offset,offset)
    assert interval(point(1128),1000,256,tiny) is None
    OPS=0;t=time.monotonic();width=1<<args.bits;table=make_table(width);hits=[]
    for name,seed in seeds().items():
        for sign in (1,-1):
            found=interval(Q,(sign*seed)%N,width,table)
            if found:
                d,delta=found;pub=point(d).format(compressed=False)
                h=hashlib.new('ripemd160',hashlib.sha256(pub).digest()).hexdigest()
                assert h==TARGET
                hits.append(dict(seed=name,sign=sign,offset=delta,private_key_hex=f'{d:064x}'))
        print('completed',name,flush=True)
    result=dict(bits=args.bits,offset_range=[-width//2,width//2-1],seed_count=len(seeds()),
                signs_per_seed=2,point_additions=OPS,seconds=round(time.monotonic()-t,2),hits=hits)
    (ROOT/'review_leads'/f'vanity-offset-{args.bits}.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result),flush=True)
