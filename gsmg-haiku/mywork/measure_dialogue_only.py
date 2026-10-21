txt = open(r'c:\gsmg-puzzle-clean\matrix-reloaded.txt', encoding='utf-8').read()
lines = [l.strip() for l in txt.split('\n') if l.strip()]

print("WITHOUT character name prefix (pure dialogue only):")
print("-" * 75)
for i, l in enumerate(lines):
    speaker, dialogue = l.split(":", 1)
    dialogue = dialogue.strip()
    alpha_only = "".join(c for c in dialogue.upper() if 'A' <= c <= 'Z')
    print(f"Line {i:2d} ({speaker:9s}): raw_len={len(dialogue):4d}, alpha_len={len(alpha_only):4d} | {dialogue[:65]}")
