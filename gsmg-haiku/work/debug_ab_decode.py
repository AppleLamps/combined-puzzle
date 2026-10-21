#!/usr/bin/env python3
"""
Debug the a/b binary decoding method
"""

def ab_binary_to_text_v1(chars: str) -> str:
    """a=0, b=1, 8 bits per ASCII character. MSB first."""
    bits = []
    for c in chars:
        if c == 'a':
            bits.append('0')
        elif c == 'b':
            bits.append('1')
    
    bits_str = ''.join(bits)
    result = []
    for i in range(0, len(bits_str), 8):
        byte = bits_str[i:i+8]
        if len(byte) == 8:
            result.append(chr(int(byte, 2)))
    return ''.join(result)

def ab_binary_to_text_v2(chars: str) -> str:
    """Reverse bit order in each byte (LSB first within byte)"""
    bits = []
    for c in chars:
        if c == 'a':
            bits.append('0')
        elif c == 'b':
            bits.append('1')
    
    bits_str = ''.join(bits)
    result = []
    for i in range(0, len(bits_str), 8):
        byte = bits_str[i:i+8]
        if len(byte) == 8:
            # Reverse the bits within the byte
            reversed_byte = byte[::-1]
            result.append(chr(int(reversed_byte, 2)))
    return ''.join(result)

def ab_binary_to_text_v3(chars: str) -> str:
    """Reverse the entire bit stream before byte-splitting"""
    bits = []
    for c in chars:
        if c == 'a':
            bits.append('0')
        elif c == 'b':
            bits.append('1')
    
    bits_str = ''.join(reversed(bits))
    result = []
    for i in range(0, len(bits_str), 8):
        byte = bits_str[i:i+8]
        if len(byte) == 8:
            result.append(chr(int(byte, 2)))
    return ''.join(result)

# "matrixsumlist" = 13 chars = 104 bits
# So we need 104 a/b characters
# Read the actual content
with open(r'c:\gsmg-puzzle-clean\files\salphaseion-textarea.txt', 'r') as f:
    content = f.read().strip()

# offset 91-194 is 104 chars: a,b 
ab_run = content[91:195]
print(f"Input: [{91}:{195}] = {len(ab_run)} chars")
print(f"Content sample: {ab_run}")
print()
print(f"Expected: 'matrixsumlist' ({len('matrixsumlist')} chars)")
print(f"ASCII hex of expected: {' '.join(f'{ord(c):02x}' for c in 'matrixsumlist')}")
print(f"Binary of expected:")
for c in 'matrixsumlist':
    print(f"  '{c}' = {ord(c):08b}")
print()

print("-"*60)
print("Testing decoding variants")
print("-"*60)

v1 = ab_binary_to_text_v1(ab_run)
v2 = ab_binary_to_text_v2(ab_run)
v3 = ab_binary_to_text_v3(ab_run)

print(f"\nv1 (straight):  {repr(v1)}")
print(f"  matches expected: {v1 == 'matrixsumlist'}")
if v1 and all(32 <= ord(c) < 127 for c in v1):
    print(f"  printable: {v1}")

print(f"\nv2 (reverse bits in byte):  {repr(v2)}")
print(f"  matches expected: {v2 == 'matrixsumlist'}")
if v2 and all(32 <= ord(c) < 127 for c in v2):
    print(f"  printable: {v2}")

print(f"\nv3 (reverse entire stream):  {repr(v3)}")
print(f"  matches expected: {v3 == 'matrixsumlist'}")
if v3 and all(32 <= ord(c) < 127 for c in v3):
    print(f"  printable: {v3}")

# Try combinations
print("\n" + "-"*60)
print("More variants (byte order reversal)")
print("-"*60)

def ab_binary_to_text_v4(chars: str) -> str:
    """LSB of entire stream first. Reverse stream AND reverse bits in each byte."""
    bits = []
    for c in chars:
        if c == 'a':
            bits.append('0')
        elif c == 'b':
            bits.append('1')
    
    bits_str = ''.join(reversed(bits))
    result = []
    for i in range(0, len(bits_str), 8):
        byte = bits_str[i:i+8]
        if len(byte) == 8:
            reversed_byte = byte[::-1]
            result.append(chr(int(reversed_byte, 2)))
    return ''.join(result)

v4 = ab_binary_to_text_v4(ab_run)
print(f"\nv4 (rev stream + rev bits in byte):  {repr(v4)}")
print(f"  matches expected: {v4 == 'matrixsumlist'}")

# What if "a" = 1 and "b" = 0?
print("\n" + "-"*60)
print("Swapping: a=1, b=0")
print("-"*60)

def ab_binary_to_text_swap_v1(chars: str) -> str:
    """a=1, b=0, straightforward"""
    bits = []
    for c in chars:
        if c == 'a':
            bits.append('1')
        elif c == 'b':
            bits.append('0')
    bits_str = ''.join(bits)
    result = []
    for i in range(0, len(bits_str), 8):
        byte = bits_str[i:i+8]
        if len(byte) == 8:
            result.append(chr(int(byte, 2)))
    return ''.join(result)

swap1 = ab_binary_to_text_swap_v1(ab_run)
print(f"\nswap1 (a=1, b=0, straight):  {repr(swap1)}")
print(f"  matches expected: {swap1 == 'matrixsumlist'}")

def ab_binary_to_text_swap_v2(chars: str) -> str:
    """a=1, b=0, reverse bits in each byte"""
    bits = []
    for c in chars:
        if c == 'a':
            bits.append('1')
        elif c == 'b':
            bits.append('0')
    bits_str = ''.join(bits)
    result = []
    for i in range(0, len(bits_str), 8):
        byte = bits_str[i:i+8]
        if len(byte) == 8:
            result.append(chr(int(byte[::-1], 2)))
    return ''.join(result)

swap2 = ab_binary_to_text_swap_v2(ab_run)
print(f"\nswap2 (a=1, b=0, reverse bits in byte):  {repr(swap2)}")
print(f"  matches expected: {swap2 == 'matrixsumlist'}")

if swap2 == 'matrixsumlist':
    print(f"  => SUCCESS!")
    print(f"  Decoded: {swap2}")

def ab_binary_to_text_swap_v3(chars: str) -> str:
    """a=1, b=0, reverse entire stream first"""
    bits = []
    for c in chars:
        if c == 'a':
            bits.append('1')
        elif c == 'b':
            bits.append('0')
    bits_str = ''.join(reversed(bits))
    result = []
    for i in range(0, len(bits_str), 8):
        byte = bits_str[i:i+8]
        if len(byte) == 8:
            result.append(chr(int(byte, 2)))
    return ''.join(result)

swap3 = ab_binary_to_text_swap_v3(ab_run)
print(f"\nswap3 (a=1, b=0, rev stream):  {repr(swap3)}")

print("\nDone debugging.")
