txt = open(r'c:\gsmg-puzzle-clean\matrix-reloaded.txt', encoding='utf-8').read()
lines = [l.strip() for l in txt.split('\n') if l.strip()]

for i, l in enumerate(lines):
    clean = "".join(c for c in l.upper() if 'A' <= c <= 'Z')
    print(f"Line {i:2d}: raw_len={len(l):4d}, alpha_len={len(clean):4d} | {l[:60]}")
