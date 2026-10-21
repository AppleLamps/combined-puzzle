#!/usr/bin/env python3
"""
Look at:
1. Full section 0-446 of Phase 3.2 (lastwordsbeforearchichoice)
2. The 149 digits for repeated patterns
3. What's "18CchrjA3Uzfrzy4DFqao9ric6YfK4hjdc" mentioned in STEPS.md?
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'derived', 'phase3.2-plaintext.bin'), 'rb') as f:
    phase32 = f.read()

# Full section 0-446 as ASCII
full_before_archi = phase32[0:447].decode('latin-1')
print("="*70)
print("Full 'last words before archi choice' (bytes 0-446)")
print("="*70)
print(full_before_archi)

print("\n" + "="*70)
print("Length:", len(full_before_archi), "chars")
print("Last 100 chars:", repr(full_before_archi[-100:]))

# Check for the "One for one, four for one"
idx = full_before_archi.lower().find('four for one')
if idx > 0:
    print(f"\n'four for one' at position {idx}")
    print(f"  Context: {full_before_archi[max(0,idx-50):idx+50]}")

print("\n" + "="*70)
print("149 checkerboard digits - analyze patterns")
print("="*70)

cb_digits = "15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112"
print(f"Digits: {cb_digits}")
print(f"Length: {len(cb_digits)}")

# Look for repeated sequences
print("\nLooking for repeated sequences (length 6+):")
seen = {}
for l in range(6, 30):
    for i in range(len(cb_digits) - l + 1):
        seq = cb_digits[i:i+l]
        if seq in seen:
            if seq not in [e[0] for e in seen.values()]:
                print(f"  '{seq}' appears at pos {seen[seq]} and {i}")
                # Also show first
                del seen[seq]
        else:
            seen[seq] = i

# Try reading STEPS.md for that weird string
print("\n" + "="*70)
print("Searching STEPS.md for '18CchrjA3Uzfrzy4DFqao9ric6YfK4hjdc'")
print("="*70)

with open(os.path.join(BASE_DIR, 'STEPS.md'), 'r') as f:
    steps = f.read()

pattern = r'18CchrjA3Uzfrzy4DFqao9ric6YfK4hjdc'
for m in re.finditer('.{0,150}' + pattern + '.{0,150}', steps):
    print(f"\nContext:")
    print(m.group(0))

# Also search for "four for one"
print("\n" + "="*70)
print("Searching for 'four for one' in STEPS.md")
print("="*70)

for m in re.finditer('.{0,150}four for one.{0,150}', steps, re.IGNORECASE):
    print(f"\nContext:")
    print(m.group(0))

# What about the plaintext?
print("\n" + "="*70)
print("Checkerboard plaintext (91 chars)")
print("="*70)

with open(os.path.join(BASE_DIR, 'derived', 'checkerboard-plaintext.txt'), 'r') as f:
    cb_plain = f.read().strip()
print(f"Content: {cb_plain}")
print(f"Length: {len(cb_plain)}")

# Words
print("\n" + "="*70)
print("Looking for substrings: HALF, BETTERHALF, KEY, KEYS")
print("="*70)

# Check lowercase
cb_lower = cb_plain.lower()
for word in ['half', 'better', 'key', 'private']:
    if word in cb_lower:
        print(f"  '{word}' found at position {cb_lower.find(word)}")

# Actually split it differently
print("\n" + "="*70)
print("Splitting the checkerboard plaintext:")
print("="*70)
# INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE

# Split manually based on capitalization
text = cb_plain

# Capital letter positions
caps = [i for i, c in enumerate(text) if c.isupper()]
print(f"Capital letters at positions: {caps}")

# Try to find word boundaries
print(f"\nText: {text}")

# Capital letters: every position that is capital, possibly start of new word
# Words are probably: IN, CASE, YOU, MANAGE, TO, CRACK, THIS, THE, PRIVATE, KEYS, BELONG, TO, HALF, AND, BETTER, HALF, AND, THEY, ALSO, NEED, FUNDS, TO, LIVE
# Let's check
expected = ['IN','CASE','YOU','MANAGE','TO','CRACK','THIS','THE','PRIVATE','KEYS','BELONG','TO','HALF','AND','BETTER','HALF','AND','THEY','ALSO','NEED','FUNDS','TO','LIVE']
print(f"\nExpected words (lowercase): {[w.lower() for w in expected]}")

# Try to see if these words can be matched
t = text.lower()
pos = 0
matched_words = []
for w in expected:
    wl = w.lower()
    if t.startswith(wl, pos):
        matched_words.append(w)
        pos += len(wl)
print(f"\nMatched sequence: {matched_words}")
print(f"  At position: {pos}, remaining text: {text[pos:] if pos < len(text) else '(end)'}")

print(f"\nFull text matched this far: {text[:pos]}")

# What's at the end?
print(f"\nFull text length: {len(text)}")

# Let's just display the whole thing with spacing for visualization
spaced = ''
for i, c in enumerate(text):
    spaced += c
    if i > 0 and i % 10 == 0:
        spaced += ' '
print(f"\nSpaced (every 10): {spaced}")

print("\nDone.")
