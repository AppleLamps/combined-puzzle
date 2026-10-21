by_seq = "BBBBYBBBYYBBBBYBBYBYYBY"
# Wait, let's get the exact sequence of 24 special cells from the script
# Indices 7, 15, 23, 31, 39, 47, 55, 63, 71, 79, 87, 95, 103, 111, 119, 127, 135, 143, 151, 159, 167, 175, 183, 191
# (24 bytes)

# Let's verify each byte's colored cell:
colors = ['B', 'B', 'B', 'B', 'Y', 'B', 'B', 'B', 'Y', 'Y', 'B', 'B', 'B', 'B', 'Y', 'B', 'B', 'Y', 'Y', 'B', 'Y', 'Y', 'B', 'Y']
print("Length of colors:", len(colors))
print("B count:", colors.count('B'))
print("Y count:", colors.count('Y'))

# If B=1, Y=0:
b1 = "".join('1' if c == 'B' else '0' for c in colors)
# If B=0, Y=1:
b0 = "".join('0' if c == 'B' else '1' for c in colors)

print("B=1, Y=0 bits:", b1)
print("B=0, Y=1 bits:", b0)

# Convert 24 bits into 3 ASCII characters:
chars1 = "".join(chr(int(b1[i:i+8], 2)) for i in range(0, 24, 8))
chars0 = "".join(chr(int(b0[i:i+8], 2)) for i in range(0, 24, 8))
print("B=1, Y=0 as ASCII (3 chars):", repr(chars1), [ord(c) for c in chars1])
print("B=0, Y=1 as ASCII (3 chars):", repr(chars0), [ord(c) for c in chars0])

# As hex:
print("B=1, Y=0 hex:", hex(int(b1, 2)))
print("B=0, Y=1 hex:", hex(int(b0, 2)))
