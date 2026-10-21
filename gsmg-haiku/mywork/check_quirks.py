from lib import *

# Let's inspect the diffs and quirks in matrix-reloaded.txt
txt = open(r'c:\gsmg-puzzle-clean\matrix-reloaded.txt', encoding='utf-8').read()

# Look at specific spellings/words in matrix-reloaded.txt:
# "quicker then the others" (notice "then" instead of "than"!)
# "burden deciduously avoided" (in movie/wikiquote it was "sedulously avoided"!)
# "While this answered function" (in movie it was "While this answer functioned"!)
# "Hope: it is the quintessential human delusion, simultaneously the source of your greatest strength and your greatest weakness."

print("Quirks found in matrix-reloaded.txt:")
for word in ['then', 'deciduously', 'answered function', 'grotesqueries', 'predication']:
    if word in txt:
        print(f"Found: {word}")

# Compare with architect-text.txt:
arch = open(r'c:\gsmg-puzzle-clean\derived\architect-text.txt').read()
print("\nIn architect-text.txt:")
print("SEDULOUSLY in arch?", 'SEDULOUSLY' in arch)
print("DECIDUOUSLY in arch?", 'DECIDUOUSLY' in arch)
print("THAN in arch?", 'THAN' in arch)
print("THEN in arch?", 'THEN' in arch)
