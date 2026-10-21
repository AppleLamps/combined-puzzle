import numpy as np
n = 33

def function_mask():
    F = np.zeros((n, n), bool)
    for r0, c0 in ((0, 0), (0, n - 7), (n - 7, 0)):
        F[max(r0 - 1, 0):r0 + 8, max(c0 - 1, 0):c0 + 8] = True
    F[6, :] = True; F[:, 6] = True
    F[24:29, 24:29] = True          # alignment centred at (26,26)
    F[8, 0:9] = True; F[0:9, 8] = True
    F[8, n - 8:] = True; F[n - 8:, 8] = True
    F[n - 8, 8] = True              # dark module
    return F

def mask_fn(m):
    return {0: lambda i, j: (i + j) % 2 == 0, 1: lambda i, j: i % 2 == 0, 2: lambda i, j: j % 3 == 0,
            3: lambda i, j: (i + j) % 3 == 0, 4: lambda i, j: (i // 2 + j // 3) % 2 == 0,
            5: lambda i, j: (i * j) % 2 + (i * j) % 3 == 0, 6: lambda i, j: ((i * j) % 2 + (i * j) % 3) % 2 == 0,
            7: lambda i, j: ((i + j) % 2 + (i * j) % 3) % 2 == 0}[m]

def read_order():
    F = function_mask(); order = []
    c = n - 1; up = True
    while c > 0:
        if c == 6: c -= 1
        rows = range(n - 1, -1, -1) if up else range(n)
        for r in rows:
            for cc in (c, c - 1):
                if not F[r, cc]: order.append((r, cc))
        up = not up; c -= 2
    return order

def codewords(Q, mask):
    mf = mask_fn(mask); bits = []
    for r, c in read_order():
        bits.append(Q[r, c] ^ (1 if mf(r, c) else 0))
    return bits

# GF(256) RS for EC check
EXP = [0] * 512; LOG = [0] * 256; x = 1
for i in range(255):
    EXP[i] = x; LOG[x] = i; x <<= 1
    if x & 0x100: x ^= 0x11d
for i in range(255, 512): EXP[i] = EXP[i - 255]
def gmul(a, b): return 0 if a == 0 or b == 0 else EXP[LOG[a] + LOG[b]]
def rs_gen(k):
    g = [1]
    for i in range(k):
        ng = [0] * (len(g) + 1)
        for j, gv in enumerate(g):
            ng[j] ^= gv; ng[j + 1] ^= gmul(gv, EXP[i])
        g = ng
    return g
def rs_ec(data, k):
    g = rs_gen(k); msg = list(data) + [0] * k
    for i in range(len(data)):
        coef = msg[i]
        if coef:
            for j in range(1, len(g)): msg[i + j] ^= gmul(g[j], coef)
    return msg[len(data):]
