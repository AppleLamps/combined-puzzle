import sys, itertools
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import (test_candidate, run_positive_control, run_negative_control,
                      run_recognizer_controls, run_chaining_control, print_chain_summary, report,
                      PHASE32_PLAINTEXT, SPS_TEXTAREA)

run_positive_control(); run_negative_control(); run_recognizer_controls(); run_chaining_control()

LABELS = ['yellowblueprimes', 'matrixsumlist', 'lastwordsbeforearchichoice', 'thispassword', 'yinyang']

all_hits = []
tested = 0

# every individual label alone
for l in LABELS:
    tested += 1
    hits = test_candidate(l, note=f'label-alone:{l}')
    if hits: all_hits.append((f'label-alone:{l}', l, hits))

# every non-empty subset AND every ordering of it (dbbi/yellowblueprimes excluded since
# it's a structural relation not a decoded word -- keep to the 3 labels co-located with
# the unopened SalPhaseIon-short container)
ORDERED = ['matrixsumlist', 'lastwordsbeforearchichoice', 'thispassword']
for r in range(1, len(ORDERED)+1):
    for combo in itertools.combinations(ORDERED, r):
        for perm in itertools.permutations(combo):
            cand = ''.join(perm)
            tested += 1
            hits = test_candidate(cand, note=f'subset-perm:{perm}')
            if hits: all_hits.append((f'subset-perm:{perm}', cand, hits))

# all 5 labels, every permutation (small: 5! = 120)
for perm in itertools.permutations(LABELS):
    cand = ''.join(perm)
    tested += 1
    hits = test_candidate(cand, note=f'perm:{perm}')
    if hits: all_hits.append((f'perm:{perm}', cand, hits))

print(f'Total candidates tested: {tested}')
report(all_hits)

print_chain_summary()
