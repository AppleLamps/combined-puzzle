import re

with open('derived/architect-text.txt', 'r') as f:
    arch = f.read().strip()

with open('matrix-reloaded.txt', 'r', encoding='utf-8') as f:
    mat = f.read()

# Clean mat to uppercase letters only per line
lines = []
for l in mat.splitlines():
    l = l.strip()
    if not l: continue
    spk, text = l.split(':', 1)
    spk_clean = re.sub(r'[^A-Z]', '', spk.upper())
    txt_clean = re.sub(r'[^A-Z]', '', text.upper())
    lines.append((spk, text, txt_clean))

print(f"Total lines in matrix-reloaded: {len(lines)}")

# Let's search where each line matches in arch
pos = 0
for i, (spk, orig, clean) in enumerate(lines):
    # find clean in arch
    idx = arch.find(clean)
    if idx != -1:
        print(f"Line {i:2d} ({spk:9s}): MATCH at arch[{idx}:{idx+len(clean)}] ({clean[:25]}...)")
    else:
        # Check partial match
        # find longest common substring
        longest = 0
        match_str = ""
        for length in range(len(clean), 10, -1):
            for s in range(len(clean) - length + 1):
                sub = clean[s:s+length]
                if sub in arch:
                    longest = length
                    match_str = sub
                    break
            if longest > 0: break
        if longest > 0:
            print(f"Line {i:2d} ({spk:9s}): PARTIAL match len {longest}/{len(clean)}: {match_str[:25]}...")
        else:
            print(f"Line {i:2d} ({spk:9s}): NO MATCH ({clean[:25]}...)")
