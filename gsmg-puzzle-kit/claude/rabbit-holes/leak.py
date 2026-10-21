"""What do the locked ciphertexts give away without a password? (3 Oct 2026)
Controls: the three solved containers (real AES) must pass as random; planted fakes
(text XOR a short repeating key, text under a Vigenere-style byte shift, AES-ECB of
repetitive text) must be caught."""
import sys, os, zlib, math, hashlib, collections, random, base64, argparse, platform
from Crypto.Cipher import AES
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
def load(name):
    with open(os.path.join(D, name)) as f:
        return base64.b64decode(''.join(f.read().split()))


def stats(b):
    ct = b[16:] if b[:8] == b'Salted__' else b
    n = len(ct); c = collections.Counter(ct)
    chi = sum((c.get(i, 0) - n / 256) ** 2 / (n / 256) for i in range(256))
    ones = sum(bin(x).count('1') for x in ct); zb = (ones - 4 * n) / math.sqrt(2 * n)
    comp = len(zlib.compress(ct, 9)) / n
    blocks = [ct[i:i+16] for i in range(0, n, 16)]; rep = n // 16 - len(set(blocks))
    m = sum(ct) / n; v = sum((x - m) ** 2 for x in ct) / n
    ser = sum((ct[i] - m) * (ct[i+1] - m) for i in range(n - 1)) / ((n - 1) * v)
    # periodicity: index of coincidence at shifts 1..64 (repeating-key XOR shows a spike)
    ic = max(sum(ct[i] == ct[i+k] for i in range(n - k)) / (n - k) for k in range(1, min(65, n // 2 + 1))) * 256
    # chi-square p-value for 255 dof via Wilson-Hilferty
    z = ((chi / 255) ** (1/3) - (1 - 2 / (9 * 255))) / math.sqrt(2 / (9 * 255))
    return dict(n=n, chi_z=z, bit_z=zb, zlib=comp, dup_blocks=rep,
                serial=ser, max_ic_x256=ic)

def verdict(s):
    bad = []
    if abs(s['chi_z']) > 4: bad.append('byte histogram')
    if abs(s['bit_z']) > 4: bad.append('bit bias')
    if s['zlib'] < 1.0: bad.append('compressible')
    if s['dup_blocks']: bad.append('repeated blocks (ECB)')
    if abs(s['serial']) > 4 / math.sqrt(s['n']): bad.append('serial corr')
    if s['max_ic_x256'] > 1 + 6 * math.sqrt(256 / s['n']) * 1.2: bad.append('periodic')
    return ', '.join(bad) or 'looks random'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=7)
    parser.add_argument('--samples', type=int, default=4000)
    args = parser.parse_args()
    if args.samples <= 0: parser.error('--samples must be positive')
    rnd = random.Random(args.seed)
    L = {'short': load('salphaseion-short.b64'), 'terminal': load('terminal.b64'),
         'cosmic': load('cosmic-duality.b64')}
    S = {n: load(n + '.b64') for n in ('phase2', 'phase3', 'phase3.2')}
    print('PROVENANCE seed=%d samples=%d PRNG=Python random.Random Python=%s zlib=%s' %
          (args.seed, args.samples, platform.python_version(), zlib.ZLIB_VERSION))
    print('Uniform byte controls, not AES controls; randomness cannot identify a cipher.')
    text = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'architect_letters_1539.txt'), 'rb').read()[:1328]
    key = b'THEMATRIX'
    fakes = {
      'FAKE xor repeating key': bytes(t ^ key[i % len(key)] for i, t in enumerate(text)),
      'FAKE byte shift (Vigenere)': bytes((t + key[i % len(key)]) % 256 for i, t in enumerate(text)),
      'FAKE AES-ECB of repetitive text': AES.new(b'k' * 32, AES.MODE_ECB).encrypt((b'ABCDEFGHIJKLMNOP' * 83)),
      'FAKE xor 32-byte key (one block of key)': bytes(t ^ hashlib.sha256(b'x').digest()[i % 32] for i, t in enumerate(text)),
    }
    print('%-40s %s' % ('object', 'stats -> verdict'))
    for name, b in list(S.items()) + list(L.items()) + list(fakes.items()):
        s = stats(b); print('%-40s %s -> %s' % (name, s, verdict(s)))

    # Same ciphertext length, header handling and statistics as each measured object.
    for nm, blob in L.items():
        observed = stats(blob)
        null = [stats(rnd.randbytes(observed['n'])) for _ in range(args.samples)]
        trip = collections.Counter(flag for row in null for flag in verdict(row).split(', '))
        print(nm, 'matched uniform controls n=', observed['n'], 'flag counts:', dict(trip))
        for metric in ('chi_z', 'bit_z', 'zlib', 'dup_blocks', 'serial', 'max_ic_x256'):
            value = observed[metric]
            # Signed deviations use a two-sided absolute statistic; IC is upper-tail.
            transform = abs if metric in ('chi_z', 'bit_z', 'serial') else (lambda x: x)
            tail = sum(transform(row[metric]) <= transform(value) if metric == 'zlib'
                       else transform(row[metric]) >= transform(value) for row in null)
            print(nm, metric, 'observed=', value, 'empirical anomaly tail=',
                  (tail + 1) / (args.samples + 1))

    # Lengths and what fits (OpenSSL: CT = 16*(floor(P/16)+1))
    def rng(ct): return (ct - 16, ct - 1)
    print('Assuming 16-byte PKCS#7 CBC/ECB, plaintext range: short/terminal', rng(80), ' cosmic', rng(1328))
    # Could Cosmic's plaintext be another OpenSSL envelope? base64 with LF every 64 chars, with or without trailing LF;
    # or hex, or raw.  Inner envelope = 16 header + 16*k bytes.
    fits = []
    for k in range(1, 200):
        B = 16 + 16 * k; b64 = 4 * math.ceil(B / 3); lines = math.ceil(b64 / 64)
        for nl, tag in ((lines - 1, 'b64 LF'), (lines, 'b64 LF+trail'), (2 * (lines - 1), 'b64 CRLF'), (2 * lines, 'b64 CRLF+trail'), (0, 'b64 one line')):
            if 1312 <= b64 + nl <= 1327: fits.append((tag, B, B - 16 - 1, 'inner plaintext %d..%d' % (B - 32, B - 17)))
        if 1312 <= 2 * B <= 1327: fits.append(('hex', B))
        if 1312 <= B <= 1327: fits.append(('raw', B))
    print('cosmic as nested envelope:', fits)
    fits = []
    for k in range(1, 6):
        B = 16 + 16 * k; b64 = 4 * math.ceil(B / 3); lines = math.ceil(b64 / 64)
        for nl, tag in ((lines - 1, 'b64 LF'), (lines, 'b64 LF+trail'), (2*(lines-1), 'b64 CRLF'), (2*lines, 'b64 CRLF+trail')):
            if 64 <= b64 + nl <= 79: fits.append((tag, 'inner envelope %d B, inner plaintext %d..%d B' % (B, B - 32, B - 17)))
    print('short as nested envelope:', fits)

if __name__ == "__main__":
    main()
