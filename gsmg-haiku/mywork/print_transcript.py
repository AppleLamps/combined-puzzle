# Let's inspect every line of matrix-reloaded.txt with its line numbers
with open(r'c:\gsmg-puzzle-clean\matrix-reloaded.txt', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if line.strip():
            print(f"{i:2d}: {line.strip()}")
