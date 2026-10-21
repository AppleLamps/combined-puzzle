#!/usr/bin/env python3
"""
Verify: How do the two base64 runs form SalPhaseIon short container?

From STEPS.md:
| 895-958  | 64  | base64 | U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z | -> SalPhaseIon short container part 1
| 959-998  | 40  | a,b    | abbaabababbabbbaabbbabaaabbaabababbbaaba -> 'enter'
| 999-1062 | 64  | base64 | QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ | -> part 2

BUT there's:
- Position 958: 'z' separator
- Positions 959-998: 40 chars a,b -> 'enter'

So between the two base64 runs (895-958 and 999-1062), there are:
- 'z' at 958
- 40 chars of a,b at 959-998

The STEPS.md note says:
"The two base64 runs joined are the SalPhaseIon short container (files/salphaseion-short.b64)."

So they IGNORE the 'z' and the a,b run between them?
Let's verify.
"""

import os
import base64

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'files', 'salphaseion-textarea.txt'), 'r') as f:
    content = f.read()

# Read the container
with open(os.path.join(BASE_DIR, 'files', 'salphaseion-short.b64'), 'r') as f:
    container_b64 = f.read().strip()

container_decoded = base64.b64decode(container_b64)

print("="*70)
print("Analyzing: How do the two base64 runs join to form the container?")
print("="*70)

print(f"\nContainer from file ({len(container_b64)} chars b64, {len(container_decoded)} bytes):")
print(f"  b64: {container_b64}")
print(f"  decoded hex: {container_decoded.hex()}")
print(f"  starts with Salted__: {container_decoded.startswith(b'Salted__')}")
if container_decoded.startswith(b'Salted__'):
    salt = container_decoded[8:16]
    ciphertext = container_decoded[16:]
    print(f"  salt: {salt.hex()}")
    print(f"  ciphertext portion: {len(ciphertext)} bytes, hex: {ciphertext.hex()}")

# Now let's get first base64 run from STEPS.md: 895-958 (64 chars)
first_b64_run = content[895:959]  # inclusive 895 to 958 = 64 chars
print(f"\nFirst base64 run (895-958, 64 chars):")
print(f"  content: {first_b64_run}")
print(f"  ends with 'z': {first_b64_run[-1] == 'z'}")

# Try decoding with and without the trailing 'z'
try:
    first_with_z = base64.b64decode(first_b64_run)
    print(f"  with trailing 'z': ERROR - but decoded anyway to {len(first_with_z)} bytes?")
except Exception as e:
    print(f"  with trailing 'z': decode error (expected) - {e}")

# Without trailing z: 63 chars
first_no_z = first_b64_run[:-1]
print(f"\nFirst without 'z' (895-957, 63 chars): {first_no_z}")

# Base64: 63 chars needs padding
# 63 chars = 63 * 6 = 378 bits = 47 bytes + 2 bits
# So we need two padding '=' chars to make it 64 chars (384 bits)

try:
    first_padded = first_no_z + '=='
    first_decoded = base64.b64decode(first_padded)
    print(f"\n  After padding with '==': {len(first_decoded)} bytes")
    print(f"  hex: {first_decoded.hex()}")
    print(f"  starts with Salted__: {first_decoded.startswith(b'Salted__')}")
except Exception as e:
    print(f"  Error: {e}")

# Second base64 run from STEPS.md: 999-1062 (64 chars)
second_b64_run = content[999:1063]  # 999 to 1062 inclusive = 64 chars
print(f"\nSecond base64 run (999-1062, 64 chars):")
print(f"  content: {second_b64_run}")

second_decoded = base64.b64decode(second_b64_run)
print(f"  decoded: {len(second_decoded)} bytes")
print(f"  hex: {second_decoded.hex()}")

# Now: what's the relationship?
# - Container decoded = 96 bytes
# - First decoded (padded 63 chars) = 47 bytes
# - Second decoded = 48 bytes
# That's 47 + 48 = 95 bytes. Close but not 96.

# Actually wait: Base64 padding rules:
# - 63 chars base64 = 378 bits
# - To make it byte-aligned: 384 bits = 48 bytes, so add 2 padding chars
# - But 378 bits in 48 bytes means 6 padding bits

# Let's try the ACTUAL container bytes:
# Container hex: 53616c7465645f5f 3ab585348552415d 75270543bb0b4f97e0a5169d6902be...

# First 16: 53616c7465645f5f = 'Salted__'
# Next 8: 3ab585348552415d = salt
# Then ciphertext starts: 75270543bb0b4f97...

# Our first decoded was 47 bytes. Let's compare:
print(f"\n" + "="*70)
print("Key insight: Compare first decoded + second decoded vs container")
print("="*70)

# We had:
# first_decoded = base64.b64decode(first_no_z + '==') = 47 bytes
# second_decoded = 48 bytes
#
# But container = 96 bytes
#
# Actually wait - what if first base64 run is NOT 63 chars, but the container uses
# the ACTUAL base64 without splitting around z?

# Let me check: container_b64 = 128 chars
# The textarea has:
# - first 64 chars ending in 'z'
# - then 'z' separator (already counted at pos 958)
# - then 40 chars a,b (959-998)
# - then second 64 chars (999-1062)

# Actually STEPS.md table row for 895-958 says 64 chars and content includes the trailing 'z'
# But the table says this is "base64", not "base64 with extra char"

# Let's look at this differently:
# In the container, ciphertext after Salted__+salt = 96 - 16 = 80 bytes
# 80 bytes in base64 = 80 * 4/3 = 107 chars, rounded up to 108 chars
# But container b64 is 128 chars total...

# Actually let me just check: is the SECOND decoded portion (48 bytes) 
# the SAME as the LAST 48 bytes of the container?

print(f"\nContainer full decoded: {len(container_decoded)} bytes")
print(f"  hex: {container_decoded.hex()}")
print(f"\nSecond base64 decoded: {len(second_decoded)} bytes")
print(f"  hex: {second_decoded.hex()}")
print(f"\nContainer LAST 48 bytes: {container_decoded[-48:].hex()}")
print(f"Match? {second_decoded == container_decoded[-48:]}")

# If second decoded is the LAST 48 of container...
# Then what is the FIRST part of container?
if second_decoded == container_decoded[-48:]:
    container_first_part = container_decoded[:-48]
    print(f"\nContainer FIRST 48 bytes (96-48=48): {container_first_part.hex()}")

# Let me try decoding first base64 differently.
# 63 chars is valid base64 with implicit padding for many decoders.
# Actually let's just try: 895-958 is 64 chars but last is 'z' which is NOT base64
# So actual base64 is 895-957 (63 chars).

# 63 chars base64:
# With '=' padding to 64 chars: maybe '=' or '==' depending on alignment
# 63 % 4 = 3, so we need 1 padding char to make it 64

print(f"\n" + "="*70)
print("Trying different padding options for first 63 chars")
print("="*70)

first_63 = first_b64_run[:-1]  # remove the trailing 'z'
print(f"First 63 chars: {first_63}")
print(f"Length mod 4: {len(first_63) % 4}")  # 63 % 4 = 3, need 1 padding

for padding in ['', '=', '==', '===']:
    try:
        dec = base64.b64decode(first_63 + padding)
        print(f"\n  With '{padding}' padding: {len(dec)} bytes")
        print(f"    hex: {dec.hex()}")
        print(f"    Starts with Salted__: {dec[:8] == b'Salted__'}")
        # Compare to container start
        if len(dec) <= len(container_decoded):
            print(f"    Match container first {len(dec)} bytes: {dec == container_decoded[:len(dec)]}")
    except Exception as e:
        print(f"\n  With '{padding}' padding: Error - {e}")

print("\nDone.")
