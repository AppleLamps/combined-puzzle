# Inspect bytes 0 to 447 of phase3.2-plaintext.bin
p32 = open(r'c:\gsmg-puzzle-clean\derived\phase3.2-plaintext.bin', 'rb').read()
print("Total length of phase3.2-plaintext.bin:", len(p32))

b0_447 = p32[:447]
print("Length of b0_447:", len(b0_447))
print("Bytes 0 to 447 raw representation:")
print(repr(b0_447))

# Let's inspect where non-printable or special bytes are:
print("\nPrintable check:")
for i in range(0, 447, 50):
    chunk = b0_447[i:i+50]
    print(f"{i:3d}-{i+len(chunk)-1:3d}: {repr(chunk)}")
