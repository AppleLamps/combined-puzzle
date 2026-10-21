# Check everything related to 14 or board as wide as the first one seen
from lib import *

D = r'c:\gsmg-puzzle-clean\derived'
cb_digits = open(D + r'\checkerboard-digits.txt').read().strip()
cb_text = open(D + r'\checkerboard-plaintext.txt').read().strip()
arch_text = open(D + r'\architect-text.txt').read().strip()
sp_text = re.sub(r'\s', '', open(r'c:\gsmg-puzzle-clean\files\salphaseion-textarea.txt').read())

print("Lengths:")
print("cb_digits:", len(cb_digits))
print("cb_text:", len(cb_text))
print("arch_text:", len(arch_text))
print("sp r1 (91):", len(sp_text[0:91]))
print("sp r3 (570):", len(sp_text[195:765]))

# What about 14?
# 14 * 14 = 196 (poster)
# Does anything divide by 14?
for name, val in [('cb_digits', len(cb_digits)), ('cb_text', len(cb_text)), ('arch_text', len(arch_text)), ('r1', 91), ('r3', 570)]:
    print(f"{name} ({val}): div 14? {val % 14 == 0}, div 7? {val % 7 == 0}")
