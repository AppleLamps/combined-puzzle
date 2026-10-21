from reconstruct import *
import random, shutil
rng=random.Random(20261015)
assert (R/'quadgrams.bin').exists(), 'Use the bundled scoring table'
control='readthecompleteinstructionbeforechangingtheorderofthesenumberskeepbothhalvesofeachpairandplaceeachpairinthepositionmarkedontheboardthecoloursindicatethedirectioninwhichyoushouldreadthefinishedrowcomparethefinalresultwiththechecksumanddonotacceptapartialmatchasthesolution'
control=(control+'everycharacterhasitsplaceinthemessage')[:282];assert len(control)==282
encrypted=hill(control,(1,19,6,3))
encoded='btcseed'+encrypted[0]
for c in encrypted[1:]:
    x,y=divmod(square.index(c),5)
    rx=rng.randrange(2) if x<4 else 0;ry=rng.randrange(2) if y<4 else 0
    encoded+=square[5*rx+ry]+c
synthetic=bifid(encoded,square,inverse=True)
assert len(synthetic)==570 and set(synthetic)<=set('abcdefghi')
assert bifid(synthetic,square)==encoded
assert hill(bifid(synthetic,square)[7::2],hkey)==control
models={'carrier':carrier,'tail_carrier':carrier,'full_bifid':bif,'full_bifid_shift1':bif[1:-1],'invented_forward_control':encrypted}
blocks=[carrier[i:i+2] for i in range(0,len(carrier),2)]
for i in range(12):
    # Preserve the exact IFINDO prefix, digraph counts, and Hill block alignment.
    tail=blocks[3:].copy();rng.shuffle(tail)
    models['tail_shuffle'+str(i)]=''.join(blocks[:3]+tail)
(R/'hill_models.txt').write_text('\n'.join(k+' '+v for k,v in models.items())+'\n')
(R/'hill_control.json').write_text(json.dumps(dict(plaintext=control,ciphertext=encrypted,source=synthetic,bifid=encoded,seed=20261015),indent=2))
print('models',len(models),'forward control source alphabet',''.join(sorted(set(synthetic))))
