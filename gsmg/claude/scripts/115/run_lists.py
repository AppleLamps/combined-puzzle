"""Doc 115 s4: the sum-list family as passwords (alone and crossed with last-words
strings) and as raw private scalars, with seeded planted controls."""
import hashlib
import harness as H, prun
from controls import planted_container, planted_target
from screen_lists import LISTS, encodings, LAST

def build():
    items = []; scalars = []
    for ln, L in LISTS.items():
        for en, v in encodings(L).items():
            vb = v if isinstance(v, bytes) else v.encode()
            if en in ('cat', 'b5dec', 'b10dec'):
                n = int(v) % H.N
                if n: scalars.append((f'{ln}|{en}', n.to_bytes(32, 'big')))
            for lw in LAST:
                lb = lw.encode()
                for c in ([vb] if not lw else [vb + lb, lb + vb]):
                    items.append((f'{ln}|{en}|{lw}', c))
    return items, scalars

def main():
    items, scalars = build()
    # controls: a container opened by one candidate, a win-test target for another's
    # sha256, and a target for one raw scalar
    ctl_pw, ctl_key = items[4321][1], items[9876][1]
    ctl_scalar = scalars[200][1]
    extra_c = {'CONTROL': planted_container(ctl_pw, seed=115)}
    extra_t = {planted_target(hashlib.sha256(ctl_key).digest()), planted_target(ctl_scalar)}
    H.TARGETS.update(extra_t)
    sflags = [lab for lab, s in scalars if H.key_hits(s)]
    print('scalar tests', len(scalars), 'scalar hits', sflags,
          '(control', 'FIRED)' if scalars[200][0] in sflags else 'MISSED)')
    C, D, V, F = prun.run(items, tag='poster sum lists', extra_containers=extra_c, extra_targets=extra_t)
    fired_c = sum(f[0] == 'CONTROL' and f[6] == ctl_pw for f in F)
    fired_k = sum(f[0] == 'WIN' and f[2] == ctl_key for f in F)
    print(f'container control fired {fired_c}x (identical encodings repeat across lists); key control fired {fired_k}x')
    for f in F:
        if f[0] == 'CONTROL' and f[6] != ctl_pw:
            print('chance flag on control container', f[:6])   # random-content container; ~0.06 expected
        elif not (f[0] == 'CONTROL' or (f[0] == 'WIN' and f[2] == ctl_key)):
            print('FLAG', f[:6])

if __name__ == '__main__':
    main()
