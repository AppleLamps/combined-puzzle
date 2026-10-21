from lib import *

sp_text = re.sub(r'\s', '', open(r'c:\gsmg-puzzle-clean\files\salphaseion-textarea.txt').read())
r1 = [ord(c) - ord('a') + 1 for c in sp_text[0:91]]
cb = open(r'c:\gsmg-puzzle-clean\derived\checkerboard-plaintext.txt').read().strip()

# Add elementwise
add1 = "".join(chr(ord(c) + d) for c, d in zip(cb, r1))
sub1 = "".join(chr(ord(c) - d) for c, d in zip(cb, r1))
print("cb + r1:", add1)
print("cb - r1:", sub1)

# Add mod 26
add26 = "".join(chr(ord('A') + (ord(c) - ord('A') + d) % 26) for c, d in zip(cb, r1))
sub26 = "".join(chr(ord('A') + (ord(c) - ord('A') - d) % 26) for c, d in zip(cb, r1))
print("cb + r1 (mod 26):", add26)
print("cb - r1 (mod 26):", sub26)

# What if a=0..i=8?
r1_0 = [ord(c) - ord('a') for c in sp_text[0:91]]
add26_0 = "".join(chr(ord('A') + (ord(c) - ord('A') + d) % 26) for c, d in zip(cb, r1_0))
sub26_0 = "".join(chr(ord('A') + (ord(c) - ord('A') - d) % 26) for c, d in zip(cb, r1_0))
print("cb + r1_0 (mod 26):", add26_0)
print("cb - r1_0 (mod 26):", sub26_0)
