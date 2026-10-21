import re

# Load architect-text.txt
arch = open(r'c:\gsmg-puzzle-clean\derived\architect-text.txt').read().strip()
print(f"Total length of architect-text.txt: {len(arch)} chars")

# Load matrix-reloaded.txt
txt = open(r'c:\gsmg-puzzle-clean\matrix-reloaded.txt', encoding='utf-8').read()
lines = [l.strip() for l in txt.split('\n') if l.strip()]

# Let's align sentences/sections of architect-text with lines of matrix-reloaded
print("\nComparing lines of matrix-reloaded against architect-text:")
for i, l in enumerate(lines):
    speaker, dialogue = l.split(":", 1)
    dialogue = dialogue.strip()
    # clean alpha
    alpha = "".join(c for c in dialogue.upper() if 'A' <= c <= 'Z')
    
    # check if dialogue appears in arch
    pos = arch.find(alpha[:30])
    print(f"Line {i:2d} ({speaker:9s}, alpha={len(alpha):3d}): in arch? pos={pos} | {dialogue[:50]}")
