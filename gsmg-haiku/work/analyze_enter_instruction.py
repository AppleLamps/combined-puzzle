#!/usr/bin/env python3
"""Verify the exact structure: how the container is formed."""

import base64

with open('files/salphaseion-textarea.txt', 'r') as f:
    content = f.read()

# Container from file
with open('files/salphaseion-short.b64', 'r') as f:
    container_b64 = f.read().strip()

# Extract parts
base64_part1 = content[895:959]   # 895-958 inclusive (64 chars)
ab_enter = content[959:999]        # 959-998 inclusive (40 chars)
base64_part2 = content[999:1063]   # 999-1062 inclusive (64 chars)

print("="*70)
print("CRITICAL STRUCTURE DISCOVERY")
print("="*70)

print(f"\nPart 1 (895-958, 64 chars base64):")
print(f"  Matches first 64 of container? {base64_part1 == container_b64[:64]}")

print(f"\nMiddle (959-998, 40 chars a,b):")
print(f"  Content: {ab_enter}")
print(f"  Decodes to: 'enter' (we verified)")

print(f"\nPart 2 (999-1062, 64 chars base64):")
print(f"  Matches last 64 of container? {base64_part2 == container_b64[64:]}")

joined = base64_part1 + base64_part2
print(f"\nJoined (part1 + part2) matches container? {joined == container_b64}")

print("\n" + "="*70)
print("MEANING: The 'enter' instruction is BETWEEN the two base64 halves")
print("="*70)
print("""
  The SalPhaseIon short container is:
    base64_part1 (895-958) + IGNORE 'enter' (959-998) + base64_part2 (999-1062)

  But logically, the structure is:
    [first base64 block]
    [INSTRUCTION: 'enter']   <-- this tells us what to do!
    [second base64 block]

  The instruction 'enter' is literally INSERTED between the two halves
  of the container. This is NOT an accident.

  What could 'enter' mean in this context?
  1. Press Enter = add newline character (\n)
  2. The two base64 halves need to be joined with a newline between them?
  3. Or: when we derive the password, we need to add 'enter' (or '\n')?

  Actually let's think about the solved phases:
  - password = sha256(answer_text).hexdigest().lower()

  Maybe 'enter' means the answer should have '\n' at the end?
  Or: there's a section of text somewhere, and we need to 'enter' (read) it?

  Actually let's look more carefully at Phase 3.2's structure.

  The other three decoded instructions:
    - 'lastwordsbeforearchichoice' -> POINTS TO Phase 3.2 bytes 0-446
    - 'thispassword'              -> POINTS TO ... what?
    - 'matrixsumlist'             -> POINTS TO ... what?
    - 'enter'                     -> Maybe an ACTION modifier?

  If 'lastwordsbeforearchichoice' is a literal pointer...
  Then maybe 'thispassword' also points to something literal.

  What comes AFTER the 'thispassword' instruction (z at 829, then a-i,o at 830-858)?
    - z separator at 859
    - text 'shabefourfirsthintisyourlastcommand'
    - then first base64 block
    - then 'enter'
    - then second base64 block

  Hmm... 'shabefourfirsthintisyourlastcommand'
  - 'shabe' might be a prefix/padding
  - 'fourfirsthint' = the FOUR hints are the FIRST thing?
  - Or: take the FOUR FIRST characters of something?

  FOUR hints/instructions:
  1. matrixsumlist
  2. lastwordsbeforearchichoice (pointed to Phase 3.2 bytes 0-446)
  3. thispassword
  4. enter (action modifier)
""")

# Now let's verify: base64_part2 decoded is 48 bytes
# Let's see what container_decoded looks like
container_decoded = base64.b64decode(container_b64)
print("\n" + "="*70)
print("SalPhaseIon short container decoded:")
print("="*70)
print(f"  Total: {len(container_decoded)} bytes")
print(f"  First 16: {container_decoded[:16].hex()} (Salted__ + salt)")
print(f"  Salt: {container_decoded[8:16].hex()}")
print(f"  Ciphertext (80 bytes): {container_decoded[16:].hex()}")

# base64_part2 decoded = last 48 bytes
part2_decoded = base64.b64decode(base64_part2)
print(f"\n  base64_part2 decoded (48 bytes): {part2_decoded.hex()}")
print(f"  Matches container[48:96]? {part2_decoded == container_decoded[48:]}")

# This confirms: container = Salted__(8) + salt(8) + ciphertext(80)
# But the split is:
#   base64_part1 decodes to 48 bytes = Salted__(8) + salt(8) + ciphertext[0:32]
#   base64_part2 decodes to 48 bytes = ciphertext[32:80]
#
# And right in the middle of the ciphertext (between byte 32 and 33 of it),
# there's an instruction: 'enter'

print("\n" + "="*70)
print("ENCRYPTED DATA SPLIT:")
print("="*70)
print("""
  Container layout:
    bytes 0-7:    Salted__
    bytes 8-15:   salt
    bytes 16-95:  ciphertext (80 bytes)

  The base64 split happens INSIDE the ciphertext:
    base64_part1 encodes: bytes 0-47 = Salted__ + salt + ciphertext[0:32]
    base64_part2 encodes: bytes 48-95 = ciphertext[32:80]

  And right AT THIS SPLIT POINT (between ciphertext byte 32 and 33),
  the author INSERTED the 'enter' instruction!

  This is a deliberate clue. The instruction is being placed literally at
  the point where we have to perform a JOIN operation.

  Could 'enter' mean: insert a newline character '\n' at the join point?
  But we're joining base64... unless the join isn't of base64, but of something else.

  Actually let's think differently. What if there's another base64 somewhere
  that also needs to be joined? Let's check Terminal and Cosmic Duality.
""")

# Check Terminal
with open('files/terminal.b64', 'r') as f:
    term_b64 = f.read().strip()
print(f"\nTerminal.b64 length: {len(term_b64)}")

# Check Cosmic Duality
with open('files/cosmic-duality.b64', 'r') as f:
    cosmic_b64 = f.read().strip()
print(f"Cosmic-duality.b64 length: {len(cosmic_b64)}")

print("\n" + "="*70)
print("INSIGHT: The 'enter' instruction is about ACTION, not location")
print("="*70)
print("""
  Three instructions are LOCATION pointers:
  - 'lastwordsbeforearchichoice' -> points to Phase 3.2 bytes 0-446
  - 'thispassword' -> probably points to something
  - 'matrixsumlist' -> probably points to something (matrix data)

  One instruction is an ACTION modifier:
  - 'enter' -> means we need to DO something to whatever we get from the pointers

  In the puzzle author's style (from solved phases), 'enter' could mean:
    - Add a newline character at the end: answer + '\n'
    - Or: the answer needs to be 'entered' (as in typed and Enter pressed)

  When we tried 'matrixsumlist\n' etc. they all failed.
  But maybe we need to get the ACTUAL TEXT from the other pointers first?

  We have:
  - 'lastwordsbeforearchichoice' -> text = Phase 3.2 bytes 0-446
  - 'thispassword' -> ? what text?
  - 'matrixsumlist' -> ? what text/numbers?

  Let's re-read 'thispassword'. If it's a location pointer like 'lastwordsbeforearchichoice',
  then 'thispassword' might mean: the password is in THIS (SalPhaseIon) section.

  Or: 'thispassword' could be a LITERAL, but we need to combine it with others.

  Actually let's think about 'fourfirsthintisyourlastcommand' again:
  - There are exactly FOUR decoded hints:
      1. matrixsumlist
      2. lastwordsbeforearchichoice
      3. thispassword
      4. enter
  - 'lastcommand' could mean the ENTER key (return) is the 'last command'

  Let me try a simple hypothesis: the answer is formed by:
    1. Getting the text from 'lastwordsbeforearchichoice' (Phase 3.2 bytes 0-446)
    2. Getting something from 'thispassword'
    3. Getting something from 'matrixsumlist'
    4. Apply 'enter' (add newline, or use as separator?)

  But wait: 'lastwordsbeforearchichoice' gave us a pointer that WORKED.
  So we should trust this pattern: the decoded a-i,o strings ARE location pointers.

  So:
  - 'lastwordsbeforearchichoice' -> literal English describing what to read
  - 'thispassword' -> literal English: THIS (section) is the password
  - 'matrixsumlist' -> literal English: sum the matrix, make a list

  And 'enter' is the action: press Enter (add newline).
""")
print("\nDone.")
