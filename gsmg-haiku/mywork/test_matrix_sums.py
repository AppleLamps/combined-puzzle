from lib import *

sp_text = re.sub(r'\s', '', open(r'c:\gsmg-puzzle-clean\files\salphaseion-textarea.txt').read())
r1 = [ord(c) - ord('a') + 1 for c in sp_text[0:91]] # 91 digits 1-9
r3 = [ord(c) - ord('a') + 1 for c in sp_text[195:765]] # 570 digits 1-9

cb = open(r'c:\gsmg-puzzle-clean\derived\checkerboard-plaintext.txt').read().strip()
cb_vals = [ord(c) - ord('A') for c in cb] # 0-25
cb_ascii = [ord(c) for c in cb]

print("r1 digits sum:", sum(r1))
print("cb ascii sum:", sum(cb_ascii))

# 7x13 matrix
m7x13 = [r1[i*13:(i+1)*13] for i in range(7)]
row_sums_7x13 = [sum(row) for row in m7x13]
col_sums_7x13 = [sum(m7x13[r][c] for r in range(7)) for c in range(13)]
print("7x13 row sums (len 7):", row_sums_7x13)
print("7x13 col sums (len 13):", col_sums_7x13)

# 13x7 matrix
m13x7 = [r1[i*7:(i+1)*7] for i in range(13)]
row_sums_13x7 = [sum(row) for row in m13x7]
col_sums_13x7 = [sum(m13x7[r][c] for r in range(13)) for c in range(7)]
print("13x7 row sums (len 13):", row_sums_13x7)
print("13x7 col sums (len 7):", col_sums_13x7)

# What if cb letters are in a 7x13 or 13x7 matrix?
m_cb_7x13 = [cb_ascii[i*13:(i+1)*13] for i in range(7)]
row_cb_7x13 = [sum(row) for row in m_cb_7x13]
col_cb_7x13 = [sum(m_cb_7x13[r][c] for r in range(7)) for c in range(13)]
print("\nCB 7x13 row sums (len 7):", row_cb_7x13)
print("CB 7x13 col sums (len 13):", col_cb_7x13)
