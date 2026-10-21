# Verify decoding of p5 and p7
p5 = "agdafaoaheiecggchgicbbhcgbehcfcoabicfdhhcdbbcagbdaiobbgbeadedde"
p7 = "cfobfdhgdobdgooiigdocdaoofidh"

def decode_dec_hex(s):
    # map a-i -> 1-9, o -> 0
    mapping = {chr(ord('a') + i): str(i + 1) for i in range(9)}
    mapping['o'] = '0'
    digits = "".join(mapping[c] for c in s)
    num = int(digits)
    hex_str = hex(num)[2:]
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str
    try:
        raw = bytes.fromhex(hex_str)
        return raw.decode('latin-1')
    except Exception as e:
        return f"Error: {e}"

print("p5 decoded:", decode_dec_hex(p5))
print("p7 decoded:", decode_dec_hex(p7))
