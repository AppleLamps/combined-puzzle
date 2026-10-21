import sys, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import (test_candidate, run_positive_control, run_negative_control,
                      run_recognizer_controls, run_chaining_control, print_chain_summary, report,
                      PHASE32_PLAINTEXT, SPS_TEXTAREA)

run_positive_control(); run_negative_control(); run_recognizer_controls(); run_chaining_control()

textarea = SPS_TEXTAREA
faed = textarea[195:765]
assert len(faed) == 570 and set(faed) <= set('abcdefghi')

def divisors(n):
    return [d for d in range(2, n) if n % d == 0]

def rule2_from_digits(digitstr):
    n = int(digitstr)
    h = hex(n)[2:]
    if len(h) % 2:
        h = '0' + h
    try:
        return bytes.fromhex(h)
    except ValueError:
        return None

all_hits = []
tested = 0
for w in divisors(570):
    h = 570 // w
    matrix = [faed[r*w:(r+1)*w] for r in range(h)]
    row_sums = [sum(ord(c)-96 for c in row) for row in matrix]   # a=1..i=9
    col_sums = [sum(ord(matrix[r][c])-96 for r in range(h)) for c in range(w)]

    candidates = []
    # (a) sums mod 256 as raw bytes directly (mirrors "as ASCII" reading)
    try:
        candidates.append((f'w={w} row-sums-as-bytes', bytes(v % 256 for v in row_sums)))
        candidates.append((f'w={w} col-sums-as-bytes', bytes(v % 256 for v in col_sums)))
    except ValueError:
        pass
    # (b) rule2-consistent: concatenated decimal digit string -> hex -> ascii
    row_digits = ''.join(str(v) for v in row_sums)
    col_digits = ''.join(str(v) for v in col_sums)
    rb = rule2_from_digits(row_digits)
    cb = rule2_from_digits(col_digits)
    if rb: candidates.append((f'w={w} row-rule2', rb))
    if cb: candidates.append((f'w={w} col-rule2', cb))
    # (c) row/col sums mod 26 as letters (in case the intended alphabet is still a-z)
    row_letters = ''.join(chr(97 + (v % 26)) for v in row_sums)
    col_letters = ''.join(chr(97 + (v % 26)) for v in col_sums)
    candidates.append((f'w={w} row-letters-mod26', row_letters))
    candidates.append((f'w={w} col-letters-mod26', col_letters))

    for note, cand in candidates:
        tested += 1
        hits = test_candidate(cand, note=note)
        if hits:
            all_hits.append((note, cand, hits))

print(f'Total candidates tested: {tested}')
report(all_hits)

print_chain_summary()
