import sys, os, hashlib, itertools, multiprocessing as mp, time
import coincurve
def h160(b): return hashlib.new('ripemd160', hashlib.sha256(b).digest()).digest()
TARGETS={bytes.fromhex(x) for x in ('a9553269572a317e39f0f518cb87c1a0ee1dbae4','4bc468447fe1b048ad030a2f9a125478eabc4ed6','06bbdc66fda09110435c79a86656a604c2d5c69b',
 'a4ae210a25bb8e2c359a134fafc2e30c6709dbc0','f8fca692ffc90cba0c330dc56e02fa8da8d2d6e6','3de34fca1bd6b7607243b0316a8102b7598cc9dc','c889dfbf698413209b6131895250b869f68560e0')}
def win_priv(priv, targets=TARGETS):
    try: pk=coincurve.PrivateKey(priv).public_key
    except Exception: return False
    return h160(pk.format(True)) in targets or h160(pk.format(False)) in targets
def win(x, targets=TARGETS, dbl=False):
    b=x.encode() if isinstance(x,str) else x
    p=hashlib.sha256(b).digest()
    if win_priv(p,targets): return True
    if dbl and win_priv(hashlib.sha256(p).digest(),targets): return True
    return False
def worker(args):
    chunk,dbl=args
    return [x for x in chunk if win(x,dbl=dbl)]
def readl(p): return [l.rstrip('\n') for l in open(p) if l.strip()]
def gen(mode,files,mid,orders):
    if mode=='base':
        for f in files:
            for l in readl(f): yield l
    else:
        A=readl(files[0]); B=readl(files[1])
        for a in A:
            for b in B:
                if orders&1:
                    yield a+b
                    if mid: yield a+b+mid
                if orders&2:
                    yield b+a
                    if mid: yield b+a+mid
if __name__=='__main__':
    # controls
    assert win_priv((1).to_bytes(32,'big'),{bytes.fromhex('751e76e8199196d454941c45d1b3a323f1433bd6')}), 'key1 control failed'
    ctl='plantedwincontrol'
    pk=coincurve.PrivateKey(hashlib.sha256(ctl.encode()).digest()).public_key
    tset={h160(pk.format(False))}
    assert win(ctl,tset) and not win('other',tset), 'planted control failed'
    tset2={h160(coincurve.PrivateKey(hashlib.sha256(hashlib.sha256(ctl.encode()).digest()).digest()).public_key.format(True))}
    assert win(ctl,tset2,dbl=True), 'double-hash control failed'
    print('controls ok',flush=True)
    mode=sys.argv[1]; args=sys.argv[2:]
    mid=None; orders=1; dbl=False; files=[]; procs=2
    i=0
    while i<len(args):
        if args[i]=='--mid': mid=args[i+1]; i+=2
        elif args[i]=='--both': orders=3; i+=1
        elif args[i]=='--order': orders=int(args[i+1]); i+=2
        elif args[i]=='--procs': procs=int(args[i+1]); i+=2
        elif args[i]=='--dbl': dbl=True; i+=1
        else: files.append(args[i]); i+=1
    t0=time.time(); n=0; hits=[]
    it=gen(mode,files,mid,orders)
    with mp.Pool(procs) as pool:
        def chunks():
            while True:
                c=list(itertools.islice(it,20000))
                if not c: return
                yield (c,dbl)
        for res in pool.imap_unordered(worker,chunks()):
            hits+=res
    n=None
    print('hits',hits,'time',round(time.time()-t0,1),flush=True)
