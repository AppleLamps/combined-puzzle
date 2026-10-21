import sys, re, hashlib, itertools
from lib import *

# Let's inspect line 49 and the entire transcript
lines = [l.strip() for l in open(r'c:\gsmg-puzzle-clean\matrix-reloaded.txt', encoding='utf-8') if l.strip()]

# Load containers
conts = {
    'terminal': load('terminal.b64'),
    'salphaseion-short': load('salphaseion-short.b64'),
    'cosmic-duality': load('cosmic-duality.b64')
}

print("Container lengths (bytes):", {k: len(v) for k, v in conts.items()})

# Let's see what line 49 has:
for idx, l in enumerate(lines):
    if 'moment of truth' in l or 'quintessential' in l or 'choice' in l:
        print(f"Line {idx}: {l}\n")
