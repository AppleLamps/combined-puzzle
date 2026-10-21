import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import (test_candidate, run_positive_control, run_negative_control,
                      run_recognizer_controls, run_chaining_control, print_chain_summary, report,
                      PHASE32_PLAINTEXT, SPS_TEXTAREA)

run_positive_control(); run_negative_control(); run_recognizer_controls(); run_chaining_control()

# From scottmanning.com's Architect transcript (fetched live, not retyped from memory):
# the monitor-voice lines immediately preceding Neo's one-word line "Choice."
line = "You can't control me! Fuck you! I'm going to kill you! You can't make me do anything!"
words = [w.strip(".,!?'") for w in line.replace("can't", "cant").replace("I'm","im").split()]
print('word sequence before the literal word CHOICE:', words)

all_hits = []
tested = 0
for n in range(1, len(words)+1):
    chosen = words[-n:]
    concat = ''.join(chosen).lower()
    spaced = ' '.join(chosen).lower()
    for form_name, cand in [('concat', concat), ('spaced', spaced), ('concat-upper', concat.upper())]:
        tested += 1
        hits = test_candidate(cand, note=f'film-choice n={n} {form_name}')
        if hits: all_hits.append((f'film-choice n={n} {form_name}', cand, hits))

# character-window variant too (mirrors the dossier's own methodology, different anchor text)
fulltext_nospace = ''.join(words).upper()
for n in range(1, len(fulltext_nospace)+1):
    window = fulltext_nospace[-n:]
    for form_name, cand in [('chars-upper', window), ('chars-lower', window.lower())]:
        tested += 1
        hits = test_candidate(cand, note=f'film-choice-chars n={n} {form_name}')
        if hits: all_hits.append((f'film-choice-chars n={n} {form_name}', cand, hits))

print(f'Total candidates tested: {tested}')
report(all_hits)

print_chain_summary()
