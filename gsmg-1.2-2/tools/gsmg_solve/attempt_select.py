import sys, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import (test_candidate, run_positive_control, run_negative_control,
                      run_recognizer_controls, run_chaining_control, print_chain_summary,
                      report, PHASE32_PLAINTEXT, SPS_TEXTAREA)

run_positive_control(); run_negative_control(); run_recognizer_controls(); run_chaining_control()

# Re-derive the Architect text exactly as in verify_architect_checkerboard.py (never retyped).
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
assert architect.startswith('YOURLIFEISTHESUMOFAREMAINDER')
assert 'SELECT' in architect

idx = architect.index('SELECT')
print(f'Found SELECT at index {idx} in the 1539-letter Architect text.')
print('Context:', architect[max(0,idx-60):idx], '|SELECT|', architect[idx+6:idx+40])

# Any other decision-shaped words worth checking?
for word in ['CHOOSE', 'CHOICE', 'DECIDE', 'DECISION', 'OPTION', 'PICK']:
    if word in architect:
        print(f'ALSO FOUND: {word} at {architect.index(word)}')
    else:
        print(f'not present: {word}')

print()
all_hits = []

# Character-window candidates ending right before "SELECT" (mirrors the dossier's own
# "3 to 200 characters before each choice point" methodology, applied to this NEW anchor).
for n in list(range(1, 61)):
    window = architect[idx-n:idx]
    for form, cand in [('upper', window), ('lower', window.lower())]:
        note = f'chars-before-SELECT n={n} form={form}'
        hits = test_candidate(cand, note=note)
        if hits:
            all_hits.append((note, cand, hits))

# word-segmented candidates (hand-segmented from the visible plaintext, English is unambiguous here)
segment = 'AFTERWHICHYOUWILLBEREQUIREDTOSELECT'
assert architect[idx-len('AFTERWHICHYOUWILLBEREQUIREDTO'):idx] == 'AFTERWHICHYOUWILLBEREQUIREDTO'
words = ['AFTER','WHICH','YOU','WILL','BE','REQUIRED','TO']
for n in range(1, len(words)+1):
    chosen = words[-n:]
    concat = ''.join(chosen)
    spaced = ' '.join(chosen)
    for form_name, cand in [
        ('concat-upper', concat), ('concat-lower', concat.lower()),
        ('spaced-upper', spaced), ('spaced-lower', spaced.lower()),
    ]:
        note = f'words-before-SELECT n={n} form={form_name}'
        hits = test_candidate(cand, note=note)
        if hits:
            all_hits.append((note, cand, hits))

print(f'Total candidates tested: character-windows 60*2 + word-windows 7*4 = {60*2 + 7*4}')
report(all_hits, null_message='NULL. No meaningful hit for any SELECT-anchored candidate on any container.')

print_chain_summary()
