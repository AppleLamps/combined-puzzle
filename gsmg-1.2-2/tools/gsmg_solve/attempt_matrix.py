import sys, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import (test_candidate, run_positive_control, run_negative_control,
                      run_recognizer_controls, run_chaining_control, print_chain_summary, report,
                      PHASE32_PLAINTEXT, SPS_TEXTAREA)

run_positive_control(); run_negative_control(); run_recognizer_controls(); run_chaining_control()

pt32 = PHASE32_PLAINTEXT
raw = pt32[447:1986]
s = raw.decode('latin-1')
ciph_letters = s.encode('cp273').decode('ascii')
KEY = "THEMATRIXHASYOU"
def reciprocal_beaufort_decrypt(ciph, key):
    out = []
    for i, c in enumerate(ciph):
        k = ord(key[i % len(key)].upper()) - 65
        cc = ord(c.upper()) - 65
        p = (k - cc) % 26
        out.append(chr(p + 65))
    return ''.join(out)
architect = reciprocal_beaufort_decrypt(ciph_letters, KEY)
assert len(architect) == 1539

def divisors(n):
    """Every valid rectangular width, including the two degenerate endpoints
    (1 row of n, or n rows of 1) -- both are still well-defined "matrices"."""
    return [d for d in range(1, n+1) if n % d == 0]

widths = divisors(1539)
print('1539 =', 1539, 'all divisors (including endpoints 1 and 1539):', widths)

all_hits = []
tested = 0

for w in widths:
    h = 1539 // w
    matrix = [architect[r*w:(r+1)*w] for r in range(h)]
    assert len(matrix) == h and all(len(row) == w for row in matrix)
    for offset in (0, 1):  # A=0..Z=25, or A=1..Z=26
        row_sums = [sum(ord(c)-65+offset for c in row) for row in matrix]
        col_sums = [sum(ord(matrix[r][c])-65+offset for r in range(h)) for c in range(w)]
        row_letters = ''.join(chr(65 + (v % 26)) for v in row_sums)
        col_letters = ''.join(chr(65 + (v % 26)) for v in col_sums)
        row_digits2 = ''.join(f'{v%100:02d}' for v in row_sums)
        col_digits2 = ''.join(f'{v%100:02d}' for v in col_sums)
        row_list_text = ','.join(str(v) for v in row_sums)
        col_list_text = ','.join(str(v) for v in col_sums)
        candidates = [
            (f'w={w} row-letters offset={offset} upper', row_letters),
            (f'w={w} row-letters offset={offset} lower', row_letters.lower()),
            (f'w={w} col-letters offset={offset} upper', col_letters),
            (f'w={w} col-letters offset={offset} lower', col_letters.lower()),
            (f'w={w} rowcol-letters offset={offset}', (row_letters+col_letters).lower()),
            (f'w={w} row-digits2 offset={offset}', row_digits2),
            (f'w={w} col-digits2 offset={offset}', col_digits2),
            (f'w={w} row-list-text offset={offset}', row_list_text),
            (f'w={w} col-list-text offset={offset}', col_list_text),
        ]
        for note, cand in candidates:
            tested += 1
            hits = test_candidate(cand, note=note)
            if hits:
                all_hits.append((note, cand, hits))

print(f'Total distinct candidate strings tested: {tested}')
report(all_hits, null_message='NULL. No meaningful hit above the expected chance rate for this candidate family.')

print_chain_summary()
