p32 = open(r'c:\gsmg-puzzle-clean\derived\phase3.2-plaintext.bin', 'rb').read()
chunk = p32[2100:2300]
print(repr(chunk))
