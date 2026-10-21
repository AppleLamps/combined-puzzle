import re

raw = open(r'c:\gsmg-puzzle-clean\files\salphaseion-textarea.txt').read()
t = re.sub(r'\s', '', raw)

print("Total length:", len(t))

# Let's inspect all parts and their exact boundaries
# 1. 0 to 91
p1 = t[0:91]
# 2. 91 to 195
p2 = t[91:195]
# 3. 195 to 765
p3 = t[195:765]
# 4. 765
p4 = t[765]
# 5. 766 to 829
p5 = t[766:829]
# 6. 829
p6 = t[829]
# 7. 830 to 859
p7 = t[830:859]
# 8. 859
p8 = t[859]
# 9. 860 to 895
p9 = t[860:895]
# 10. 895 to 959
p10 = t[895:959]
# 11. 959 to 999
p11 = t[959:999]
# 12. 999 to 1063
p12 = t[999:1063]
# 13. 1063 to 1075
p13 = t[1063:1075]

print("p1 (a-i len):", len(p1))
print("p2 (ab len):", len(p2))
print("p3 (a-i len):", len(p3))
print("p4:", p4)
print("p5 (len):", len(p5), p5)
print("p6:", p6)
print("p7 (len):", len(p7), p7)
print("p8:", p8)
print("p9 (len):", len(p9), p9)
print("p10 (b64 len):", len(p10), p10)
print("p11 (ab len):", len(p11))
print("p12 (b64 len):", len(p12), p12)
print("p13 (len):", len(p13), p13)
