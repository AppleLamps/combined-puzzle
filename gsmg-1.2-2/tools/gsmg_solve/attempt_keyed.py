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
KEYSTR = "THEMATRIXHASYOU"
def reciprocal_beaufort_decrypt(ciph, key):
    out = []
    for i, c in enumerate(ciph):
        k = ord(key[i % len(key)].upper()) - 65
        cc = ord(c.upper()) - 65
        p = (k - cc) % 26
        out.append(chr(p + 65))
    return ''.join(out)
architect = reciprocal_beaufort_decrypt(ciph_letters, KEYSTR)
idx = architect.index('SELECT')

def vig_encrypt(text, key_vals):
    return ''.join(chr(65 + (ord(c)-65 + key_vals[i % len(key_vals)]) % 26) for i, c in enumerate(text))
def vig_decrypt(text, key_vals):
    return ''.join(chr(65 + (ord(c)-65 - key_vals[i % len(key_vals)]) % 26) for i, c in enumerate(text))
def beaufort(text, key_vals):
    return ''.join(chr(65 + (key_vals[i % len(key_vals)] - (ord(c)-65)) % 26) for i, c in enumerate(text))

KEYS = {
    '574061-digits': [5,7,4,0,6,1],
    'BUT-vigkey0': [ord(c)-65 for c in 'BUT'],   # A=0..Z=25, the standard Vigenere key convention
    'HYE-vigkey0': [ord(c)-65 for c in 'HYE'],
    'BUT-a1z26': [ord(c)-64 for c in 'BUT'],     # A=1..Z=26, actual A1Z26 (matches "shabef via a1z26")
    'HYE-a1z26': [ord(c)-64 for c in 'HYE'],
    '231607-digits': [2,3,1,6,0,7],  # the raw census order [23,16,7] digit-joined alt reading
}

all_hits = []
tested = 0
for n in range(2, 41):
    window = architect[idx-n:idx]
    for kname, kvals in KEYS.items():
        for opname, op in [('vig-enc', vig_encrypt), ('vig-dec', vig_decrypt), ('beaufort', beaufort)]:
            out = op(window, kvals)
            for form_name, cand in [('upper', out), ('lower', out.lower())]:
                tested += 1
                hits = test_candidate(cand, note=f'n={n} key={kname} op={opname} {form_name}')
                if hits:
                    all_hits.append((f'n={n} key={kname} op={opname} {form_name}', cand, hits))

print(f'Total candidates tested: {tested}')
report(all_hits)

print_chain_summary()
