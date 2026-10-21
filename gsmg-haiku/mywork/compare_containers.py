from lib import *

t_raw = load('terminal.b64')
s_raw = load('salphaseion-short.b64')
c_raw = load('cosmic-duality.b64')

print("Terminal:")
print("  Total len:", len(t_raw))
print("  Salt:", t_raw[8:16].hex())
print("  Ciphertext len:", len(t_raw[16:]))
print("  Ciphertext hex:", t_raw[16:].hex())

print("\nSalPhaseIon short:")
print("  Total len:", len(s_raw))
print("  Salt:", s_raw[8:16].hex())
print("  Ciphertext len:", len(s_raw[16:]))
print("  Ciphertext hex:", s_raw[16:].hex())

print("\nCosmic Duality:")
print("  Total len:", len(c_raw))
print("  Salt:", c_raw[8:16].hex())
print("  Ciphertext len:", len(c_raw[16:]))
