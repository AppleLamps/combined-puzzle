"""Parallel screen runner: feed (label, bytes) items; aggregate stats and flags.

Uses the spawn start method on every platform, so a run behaves the same on Linux,
macOS and Windows. Per-run harness state (planted control containers and targets)
is passed to each worker through the pool initializer, never through forked globals.
"""
import multiprocessing as mp, time
import harness as H

def _init(extra_containers, extra_targets):
    H.CONTAINERS.update(extra_containers or {})
    H.TARGETS.update(extra_targets or ())

def _work(chunk):
    st = H.Stats()
    for label, c in chunk:
        H.screen(c, st, label)
    return st.cands, st.dec, st.valid, st.flags

def run(items, procs=4, chunk=500, tag='', extra_containers=None, extra_targets=None):
    t0 = time.time()
    chunks = [items[i:i + chunk] for i in range(0, len(items), chunk)]
    C = D = V = 0; F = []
    ctx = mp.get_context('spawn')
    with ctx.Pool(procs, initializer=_init, initargs=(extra_containers, extra_targets)) as pool:
        for c, d, v, f in pool.imap_unordered(_work, chunks):
            C += c; D += d; V += v; F += f
    print(f'[{tag}] candidates {C}  decrypts {D}  valid pads {V} (expected {D/256:.0f})  flags {len(F)}  {time.time()-t0:.0f}s')
    return C, D, V, F
