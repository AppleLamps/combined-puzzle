from lib import *

D = r'c:\gsmg-puzzle-clean\derived'
cb = open(D + r'\checkerboard-plaintext.txt').read().strip()
sp_text = re.sub(r'\s', '', open(r'c:\gsmg-puzzle-clean\files\salphaseion-textarea.txt').read())
r1 = sp_text[0:91]

print("Length of checkerboard-plaintext:", len(cb))
print("Length of SalPhaseIon Run 1:", len(r1))
print("cb:", cb)
print("r1:", r1)
