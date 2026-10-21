#!/usr/bin/env python3
"""
GSMG Puzzle - Decode the real chess content

The "chess board" is not actually chess! The "values" are ASCII characters
packed as 4-byte little-endian integers.

Each square:
- byte 0: piece char (1 ASCII char)
- bytes 1-4: value (4 ASCII chars, little-endian = read bytes backwards)

So each square gives 5 characters total.
64 squares * 5 = 320 characters.

Also decode section 3a fully.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Read phase 3.2 binary
with open(os.path.join(BASE_DIR, 'derived', 'phase3.2-plaintext.bin'), 'rb') as f:
    phase32_bin = f.read()

print("="*70)
print("SECTION 3a: Matrix Text (bytes 0-126)")
print("="*70)
section_3a = phase32_bin[0:127]
print("\nFull section 3a decoded as ASCII:")
print("-"*70)
print(section_3a.decode('latin-1'))
print("-"*70)
print(f"Length: {len(section_3a)} chars")

print("\n" + "="*70)
print("SECTION 3b: 'Chess' Decoded as ASCII (bytes 127-446)")
print("="*70)
chess_bytes = phase32_bin[127:447]
print(f"Total: {len(chess_bytes)} bytes")

# Decode each square
full_message = []
for i in range(0, 320, 5):
    # byte 0: piece char
    piece_char = chr(chess_bytes[i])
    
    # bytes 1-4: 4 chars, little-endian means we read from HIGH to LOW
    # In little-endian, the least significant byte is stored first.
    # So bytes [1, 2, 3, 4] represent: value = byte1 + byte2*256 + byte3*65536 + byte4*16777216
    # But as ASCII characters, the FIRST byte stored is the LOW-order byte.
    # So when displayed as text, the order would be: byte4, byte3, byte2, byte1
    # because that's highest to lowest significance.
    
    # Actually wait - let me check both ways. Let me interpret bytes as chars directly
    # AND also reversed.
    
    raw_4chars = chess_bytes[i+1:i+5]
    
    # Try both interpretations
    as_stored = ''.join(chr(b) for b in raw_4chars)
    reversed_4 = ''.join(chr(b) for b in reversed(raw_4chars))
    
    # Store both
    full_message.append((piece_char, as_stored, reversed_4, raw_4chars))

# First let me see what the actual character values are by looking at raw bytes
print("\n\nFirst 10 squares raw:")
all_piece_chars = []
all_bytes_1_to_4 = []
for idx in range(min(64, len(full_message))):
    pc, stored, rev, raw = full_message[idx]
    all_piece_chars.append(pc)
    all_bytes_1_to_4.extend(raw)
    
    # Print hex
    hex_vals = ' '.join(f'{b:02x}' for b in raw)
    # Try to see if ASCII
    ascii_stored = ''.join(chr(b) if 32 <= b < 127 else '.' for b in raw)
    print(f"  Square {idx:2d}: piece='{pc}' ({ord(pc):02x}), bytes={hex_vals} = '{ascii_stored}'")

print(f"\n\nAll piece chars concatenated ({len(all_piece_chars)} chars):")
print(''.join(all_piece_chars))

# What if bytes 1-4 are actually consecutive text? Let's treat them as a stream
print(f"\n\nAll bytes 1-4 concatenated as ASCII ({len(all_bytes_1_to_4)} chars):")
ascii_text = ''.join(chr(b) if 32 <= b < 127 else f'\\x{b:02x}' for b in all_bytes_1_to_4)
print(ascii_text[:300])

# But also - what if the LITTLE ENDIAN was about the ORDER of extraction?
# Let me think differently. In STEPS.md it says:
# "64 squares. Each square is 5 bytes: byte 0 is the piece (KQRBNPkqrbnp or '.'), 
# and bytes 1-4 are the value in cents as a 4-byte little-endian signed integer."
#
# But the values we saw were things like:
#   Rank 8 piece='a' value=544828514
#   
# Let's decode 544828514 as hex and see what characters it gives:
#   544828514 in hex = 0x20796162
#   In little-endian, this was stored as bytes: 62 61 79 20
#   Which is: 'b' 'a' 'y' ' '
# 
# So: byte0=62='b', byte1=61='a', byte2=79='y', byte3=20=' '
# But as a VALUE 0x20796162, reading highest to lowest: 0x20=' ', 0x79='y', 0x61='a', 0x62='b'
# = " yab"
# 
# So we need to take the 4-byte integer value, convert to 8 hex chars,
# then take bytes high-to-low (or equivalently reverse the stored bytes).

print("\n" + "="*70)
print("Proper Decoding: Interpret 'value' as 4 chars via LE int -> hex")
print("="*70)

def decode_4byte_val_le(val: int) -> str:
    """Take a 4-byte little-endian signed integer and decode to 4 ASCII chars.
    
    The integer is stored little-endian (lowest byte first in memory).
    When interpreting the 32 bits as 4 characters, we take them from 
    most significant byte to least significant.
    
    Example: val = 544828514 = 0x20796162
      Stored in memory as bytes: 62 61 79 20 (little-endian: LSByte first)
      As 32-bit value: 0x20 0x79 0x61 0x62
                    or: ' '  'y'  'a'  'b'
    """
    # Convert to unsigned 32-bit
    if val < 0:
        val = val + 2**32
    
    # Get 4 bytes from MSB to LSB
    byte3 = (val >> 24) & 0xFF  # most significant
    byte2 = (val >> 16) & 0xFF
    byte1 = (val >> 8) & 0xFF
    byte0 = val & 0xFF             # least significant
    
    return chr(byte3) + chr(byte2) + chr(byte1) + chr(byte0)

decoded_pieces = []
decoded_values = []

for i in range(0, 320, 5):
    piece = chr(chess_bytes[i])
    value_int = int.from_bytes(chess_bytes[i+1:i+5], 'little', signed=True)
    
    decoded_val = decode_4byte_val_le(value_int)
    
    decoded_pieces.append(piece)
    decoded_values.append(decoded_val)
    
    # Debug first few
    if i < 10*5:
        print(f"  {piece} + {repr(decoded_val)}  (from int={value_int}, hex={value_int & 0xFFFFFFFF:08x})")

print("\n" + "="*70)
print("FULL MESSAGE: pieces interleaved with value chars")
print("="*70)

# The piece chars and value chars together make the message.
# But how are they interleaved?
# Is it: piece1, val1_char1, val1_char2, val1_char3, val1_char4, piece2, val2_char1, ... ?
# That would be the natural byte order.

# Let's try that first
full_by_order = []
for p, v in zip(decoded_pieces, decoded_values):
    full_by_order.append(p)
    full_by_order.extend(v)

full_text_ordered = ''.join(full_by_order)
print(f"\nOrder: piece + 4-val-chars, then next... ({len(full_text_ordered)} chars):")
print("-"*70)
print(full_text_ordered)
print("-"*70)

# Maybe ALL pieces first, then ALL values?
all_pieces_together = ''.join(decoded_pieces)
all_values_together = ''.join(decoded_values)

print(f"\n\nAll pieces first ({len(all_pieces_together)} chars):")
print("-"*70)
print(all_pieces_together)

print(f"\n\nAll values second ({len(all_values_together)} chars):")
print("-"*70)
print(all_values_together)

print("\n" + "="*70)
print("SECTION 4a: Architect text (bytes 447-1985)")
print("="*70)
arch_bytes = phase32_bin[447:1986]
print(f"Length: {len(arch_bytes)} bytes")
# First 100 and last 100 chars
print(f"\nFirst 200 chars:")
print(arch_bytes[:200].decode('latin-1'))
print(f"\nLast 100 chars:")
print(arch_bytes[-100:].decode('latin-1'))

# What's in bytes 1986+?
print(f"\n\nBytes 1986+ ({len(phase32_bin)-1986} bytes remaining):")
remaining = phase32_bin[1986:]
print(f"Hex first 100: {remaining[:100].hex()}")
print(f"As ASCII (printable):")
print(''.join(chr(b) if 32 <= b < 127 else '.' for b in remaining))

print("\n" + "="*70)
print("SUMMARY OF KEY FINDS")
print("="*70)
print("""
Phase 3.2 decrypted binary has the following structure (now decoded):

1. Section 3a (bytes 0-126, 127 chars):
   MORPHEUS QUOTE from Matrix: 
   "I've been waiting for you. You have many questions, and although 
    the process has altered your consciousness, you remain irrevoc..."

2. Section 3b (bytes 127-446, 320 chars) - "Chess board":
   NOT ACTUALLY CHESS! This is a packed message where:
   - byte 0 of each square = 1 ASCII char (the "piece")
   - bytes 1-4 = 4 more ASCII chars packed as little-endian 32-bit int
   
   Try decoding as:
   a) Full ordered interleaving: piece, then its 4 value chars...
   b) All pieces first, then all values

3. Section 4a (bytes 447-1985, 1539 chars):
   Architect monologue (already decoded to architect-text.txt)

POTENTIAL PASSWORD CANDIDATES from this:
- Maybe the Section 3a text itself (or part of it)
- Maybe the decoded Section 3b message
- Maybe "last words before archi choice" means Section 3a + 3b combined?
""")
