from lib import *
arch = open(r'c:\gsmg-puzzle-clean\derived\architect-text.txt').read().strip()
print("Length of arch:", len(arch))
print("Does arch have CHOICE?", 'CHOICE' in arch)
for word in ['CHOICE', 'DOOR', 'SELECT', 'CHOOSE', 'TRUTH', 'MOMENT', 'HOPE', 'STRENGTH', 'WEAKNESS', 'DELUSION', 'END']:
    print(word, arch.find(word))

# Let's print the entire arch text with word breaks or look at sections
print("\nArch text:")
print(arch)
