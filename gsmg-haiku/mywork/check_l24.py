txt = open(r'c:\gsmg-puzzle-clean\matrix-reloaded.txt', encoding='utf-8').read()
lines = [l.strip() for l in txt.split('\n') if l.strip()]

l24 = lines[24]
# Remove "Architect: "
speech = l24.split(":", 1)[1].strip()

# Find "choice"
idx = speech.find("the problem is choice")
before_choice = speech[:idx + len("the problem is ")]
print("Before choice:")
print(repr(before_choice))
print("Raw len:", len(before_choice))
clean = "".join(c for c in before_choice.upper() if 'A' <= c <= 'Z')
print("Alpha len:", len(clean))

# What about up to the end of species (before the choice)?
idx2 = speech.find("As you adequately put")
before_choice2 = speech[:idx2].strip()
print("\nBefore 'As you adequately put':")
print(repr(before_choice2))
print("Raw len:", len(before_choice2))
clean2 = "".join(c for c in before_choice2.upper() if 'A' <= c <= 'Z')
print("Alpha len:", len(clean2))
