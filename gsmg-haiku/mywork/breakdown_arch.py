arch = open(r'c:\gsmg-puzzle-clean\derived\architect-text.txt').read().strip()

print("ARCHITECT-TEXT.TXT FULL BREAKDOWN:")
print("=" * 75)

# 0 to 344:
print("[0:344] (matches Line 4, Architect):")
print(arch[0:344])

print("\n[344:373] (matches Line 5, Neo):")
print(arch[344:373])

print("\n[373:421] (matches Line 6, Architect):")
print(arch[373:421])

print("\n[421:836] (PUZZLE AUTHOR CUSTOM TEXT!):")
print(arch[421:836])

print("\n[836:980] (matches start of Line 18, Architect):")
print(arch[836:980])

print("\n[980:1539] (PUZZLE AUTHOR CUSTOM TEXT AT END!):")
print(arch[980:1539])
