digits = '15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112'

# Checkerboard map:
# Row 0 (no prefix): 0:F, 2:U, 3:B, 5:C, 6:D, 7:O, 8:R, 9:A
# Row 1 (prefix 1): 0:., 1:L, 2:E, 3:T, 4:H, 5:I, 6:N, 7:G, 8:K, 9:Y
# Row 4 (prefix 4): 0:M, 1:V, 2:P, 3:S, 4:/, 5:J, 6:Q, 7:Z, 8:X, 9:W

board = {
    '0': 'F', '2': 'U', '3': 'B', '5': 'C', '6': 'D', '7': 'O', '8': 'R', '9': 'A',
    '10': '.', '11': 'L', '12': 'E', '13': 'T', '14': 'H', '15': 'I', '16': 'N', '17': 'G', '18': 'K', '19': 'Y',
    '40': 'M', '41': 'V', '42': 'P', '43': 'S', '44': '/', '45': 'J', '46': 'Q', '47': 'Z', '48': 'X', '49': 'W'
}

decoded = []
i = 0
mapping = []
while i < len(digits):
    d = digits[i]
    if d in ('1', '4'):
        code = digits[i:i+2]
        char = board[code]
        mapping.append((i, code, char))
        decoded.append(char)
        i += 2
    else:
        char = board[d]
        mapping.append((i, d, char))
        decoded.append(char)
        i += 1

full_text = "".join(decoded)
print("Decoded full text:", full_text)

# Let's inspect each letter and its digit offset
for pos, (d_idx, code, char) in enumerate(mapping):
    print(f"Letter {pos:2d} (digit {d_idx:3d}): code={code:2s} -> '{char}'")
