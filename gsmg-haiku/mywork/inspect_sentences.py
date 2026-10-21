import re

txt = open(r'c:\gsmg-puzzle-clean\matrix-reloaded.txt', encoding='utf-8').read()
lines = [l.strip() for l in txt.split('\n') if l.strip()]

# Let's inspect each line and its sentences
for i, l in enumerate(lines):
    speaker, dialogue = l.split(":", 1)
    dialogue = dialogue.strip()
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', dialogue) if s.strip()]
    for s_idx, s in enumerate(sentences):
        alpha = "".join(c for c in s.upper() if 'A' <= c <= 'Z')
        words = re.findall(r"[A-Za-z0-9']+", s)
        print(f"Line {i:2d} ({speaker:9s}) sent {s_idx}: len={len(s):3d}, alpha={len(alpha):3d}, words={len(words):2d} | {s[:60]}")
