// GSMG container harness. stdin mode: one candidate answer per line. dbbi mode: enumerate zeroings.
#pragma GCC optimize("O3")
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <openssl/sha.h>
#include <openssl/md5.h>
#include <openssl/aes.h>
#include "audit_output.h"

typedef struct { char name[32]; uint8_t *ct; size_t clen; uint8_t salt[8]; } Con;
static Con cons[8]; static int ncons = 0;
static unsigned long long tests = 0, validpads = 0, flags = 0;
static unsigned long long hist[8][17];
static int formmask = 3;
static unsigned long long retained = 0;
static const unsigned long long audit_limit = 1000;

static void load_con(const char *name, const char *path) {
    FILE *f = fopen(path, "rb"); if (!f) { perror(path); exit(1); }
    fseek(f, 0, SEEK_END); long n = ftell(f); fseek(f, 0, SEEK_SET);
    uint8_t *b = malloc(n); if (fread(b, 1, n, f) != (size_t)n) exit(1); fclose(f);
    if (memcmp(b, "Salted__", 8)) { fprintf(stderr, "%s: no Salted__\n", path); exit(1); }
    Con *c = &cons[ncons++]; strncpy(c->name, name, 31);
    memcpy(c->salt, b + 8, 8); c->clen = n - 16; c->ct = malloc(c->clen); memcpy(c->ct, b + 16, c->clen); free(b);
}
static inline void hexof(const uint8_t *d, size_t n, char *out) {
    static const char *H = "0123456789abcdef";
    for (size_t i = 0; i < n; i++) { out[2*i] = H[d[i] >> 4]; out[2*i+1] = H[d[i] & 15]; }
    out[2*n] = 0;
}
static inline void sha256(const uint8_t *a, size_t n, uint8_t o[32]) {
    SHA256_CTX c; SHA256_Init(&c); SHA256_Update(&c, a, n); SHA256_Final(o, &c);
}
static inline void evp_sha256(const uint8_t *pw, size_t pl, const uint8_t *salt, uint8_t key[32], uint8_t iv[16]) {
    SHA256_CTX c; uint8_t d2[32];
    SHA256_Init(&c); SHA256_Update(&c, pw, pl); SHA256_Update(&c, salt, 8); SHA256_Final(key, &c);
    SHA256_Init(&c); SHA256_Update(&c, key, 32); SHA256_Update(&c, pw, pl); SHA256_Update(&c, salt, 8); SHA256_Final(d2, &c);
    memcpy(iv, d2, 16);
}
static inline void evp_md5(const uint8_t *pw, size_t pl, const uint8_t *salt, uint8_t key[32], uint8_t iv[16]) {
    MD5_CTX c; uint8_t d[48];
    MD5_Init(&c); MD5_Update(&c, pw, pl); MD5_Update(&c, salt, 8); MD5_Final(d, &c);
    MD5_Init(&c); MD5_Update(&c, d, 16); MD5_Update(&c, pw, pl); MD5_Update(&c, salt, 8); MD5_Final(d + 16, &c);
    MD5_Init(&c); MD5_Update(&c, d + 16, 16); MD5_Update(&c, pw, pl); MD5_Update(&c, salt, 8); MD5_Final(d + 32, &c);
    memcpy(key, d, 32); memcpy(iv, d + 32, 16);
}
// recogniser: returns reason string or NULL
static const char *recognise(const uint8_t *p, size_t n) {
    if (n < 8) return NULL;
    size_t pr = 0, z = 0, alt = 0; int distinct[256] = {0}; size_t nd = 0; size_t bits[8] = {0};
    for (size_t i = 0; i < n; i++) {
        uint8_t c = p[i];
        if ((c >= 32 && c < 127) || c == 9 || c == 10 || c == 13) pr++;
        if (!distinct[c]) { distinct[c] = 1; nd++; }
        for (int b = 0; b < 8; b++) if (c >> b & 1) bits[b]++;
        if (i % 2 == 1 && c == 0) alt++;
    }
    if ((double)pr / n >= 0.80) return "printable";
    double sd = sqrt(n / 4.0);
    for (int b = 0; b < 8; b++) { double zz = ((double)bits[b] - n / 2.0) / sd; if (zz >= 6 || zz <= -6) return "bitbias"; }
    { double q = 1.0 - 1.0 / 256, E = 256 * (1 - pow(q, n));
      double V = 256 * 255 * pow(1 - 2.0 / 256, n) + 256 * pow(q, n) - 65536 * pow(q, 2.0 * n);
      if (V > 0 && ((double)nd - E) / sqrt(V) <= -6) return "distinct"; }
    if (n >= 16 && (double)alt / (n / 2) >= 0.6) return "utf16";
    for (size_t i = 0; i + 8 <= n; i++) if (!memcmp(p + i, "Salted__", 8)) return "nestedsalt";
    if (n > 10 && ((p[0] == 0x1f && p[1] == 0x8b && p[2] == 8) || (p[0] == 'P' && p[1] == 'K' && p[2] == 3 && p[3] == 4) || (!memcmp(p, "BZh", 3) && p[3] >= '1' && p[3] <= '9' && !memcmp(p + 4, "\x31\x41\x59\x26\x53\x59", 6)) || !memcmp(p, "\x89PNG", 4) || !memcmp(p, "%PDF", 4) || !memcmp(p, "\xfd" "7zXZ", 5) || !memcmp(p, "7z\xbc\xaf", 4))) return "magic";
    return NULL;
}
static void print_cand(const uint8_t *a, size_t n) {
    audit_print_hex(stdout, a, n);
}
static void try_pw(const uint8_t *pw, size_t pl, const uint8_t *cand, size_t cl, int form) {
    uint8_t key[32], iv[16], last[16], out[16];
    for (int ci = 0; ci < ncons; ci++) {
        Con *c = &cons[ci];
        for (int md = 0; md < 2; md++) {
            if (md == 0) evp_sha256(pw, pl, c->salt, key, iv); else evp_md5(pw, pl, c->salt, key, iv);
            AES_KEY ks; AES_set_decrypt_key(key, 256, &ks);
            AES_decrypt(c->ct + c->clen - 16, last, &ks);
            const uint8_t *prev = c->clen >= 32 ? c->ct + c->clen - 32 : iv;
            for (int i = 0; i < 16; i++) out[i] = last[i] ^ prev[i];
            tests++;
            int p = audit_padding(out, sizeof out, 16);
            if (!p) continue;
            validpads++; hist[ci][p]++;
            uint8_t *full = malloc(c->clen); uint8_t iv2[16]; memcpy(iv2, iv, 16);
            AES_cbc_encrypt(c->ct, full, c->clen, &ks, iv2, AES_DECRYPT);
            size_t bl = c->clen - p; const char *why = NULL;
            why = recognise(full, bl);
            if (why) flags++;
            if (audit_retain(&retained, audit_limit)) {
                printf("FLAG\t%s\tform%d\tmd%d\tpad%d\t%s\tbodylen=%zu\tcandhex=", c->name, form, md, p, why ? why : "unranked", bl);
                print_cand(cand, cl);
                printf("\tbody="); for (size_t i = 0; i < bl; i++) printf("%02x", full[i]); printf("\n"); fflush(stdout);
            }
            free(full);
        }
    }
}
static void try_answer(const uint8_t *a, size_t al) {
    uint8_t d[32], d2[32]; char hx[65], hx2[65];
    sha256(a, al, d); hexof(d, 32, hx);
    if (formmask & 1) try_pw((uint8_t *)hx, 64, a, al, 0);
    if (formmask & 2) try_pw(d, 32, a, al, 1);
    if (formmask & 12) {
        sha256(d, 32, d2); hexof(d2, 32, hx2);
        if (formmask & 4) try_pw((uint8_t *)hx2, 64, a, al, 2);
        if (formmask & 8) { uint8_t d3[32]; char hx3[65]; sha256((uint8_t *)hx, 64, d3); hexof(d3, 32, hx3); try_pw((uint8_t *)hx3, 64, a, al, 3); }
    }
}
// ---- dbbi enumeration ----
typedef struct { uint64_t w[5]; } Big;
static Big big_from_u(uint64_t x) { Big b = {{x,0,0,0,0}}; return b; }
static Big big_mul10(Big a) { Big r; unsigned __int128 c = 0; for (int i = 0; i < 5; i++) { unsigned __int128 t = (unsigned __int128)a.w[i] * 10 + c; r.w[i] = (uint64_t)t; c = t >> 64; } return r; }
static Big big_add(Big a, Big b) { Big r; unsigned __int128 c = 0; for (int i = 0; i < 5; i++) { unsigned __int128 t = (unsigned __int128)a.w[i] + b.w[i] + c; r.w[i] = (uint64_t)t; c = t >> 64; } return r; }
static Big big_sub(Big a, Big b) { Big r; uint64_t br = 0; for (int i = 0; i < 5; i++) { unsigned __int128 t = (unsigned __int128)a.w[i] - b.w[i] - br; r.w[i] = (uint64_t)t; br = (t >> 64) ? 1 : 0; } return r; }
static size_t big_bytes(Big a, uint8_t *out) { // minimal big-endian
    uint8_t buf[40]; for (int i = 0; i < 5; i++) for (int j = 0; j < 8; j++) buf[39 - (i * 8 + j)] = (a.w[i] >> (8 * j)) & 255;
    size_t s = 0; while (s < 39 && buf[s] == 0) s++; size_t n = 40 - s; memcpy(out, buf + s, n); return n;
}
static int strmode = 0, nonum = 0;
static void dbbi_mode(const char *digits, int zeroDigitVal, int rev, int part, int nparts, int textonly) {
    // digits: string of a..i letters; zero the positions where letter == zl
    char s[128]; size_t L = strlen(digits);
    for (size_t i = 0; i < L; i++) s[i] = rev ? digits[L - 1 - i] : digits[i];
    Big pw10[100]; pw10[0] = big_from_u(1); for (int i = 1; i < 100; i++) pw10[i] = big_mul10(pw10[i - 1]);
    Big base = big_from_u(0);
    int pos[40], npos = 0; Big wt[40];
    for (size_t i = 0; i < L; i++) {
        int d = s[i] - 'a' + 1; Big t = pw10[L - 1 - i];
        for (int k = 0; k < d; k++) base = big_add(base, t);
        if (d == zeroDigitVal) { pos[npos] = i; Big w = big_from_u(0); for (int k = 0; k < d; k++) w = big_add(w, t); wt[npos++] = w; }
    }
    fprintf(stderr, "dbbi mode: L=%zu zero-letter positions=%d rev=%d part %d/%d\n", L, npos, rev, part, nparts);
    uint64_t total = 1ULL << npos, lo = total / nparts * part, hi = part == nparts - 1 ? total : total / nparts * (part + 1);
    uint64_t g = lo ^ (lo >> 1); Big v = base;
    for (int j = 0; j < npos; j++) if (g >> j & 1) v = big_sub(v, wt[j]);
    char dstr[128], lstr[128]; for (size_t i = 0; i < L; i++) { dstr[i] = '0' + (s[i] - 'a' + 1); lstr[i] = s[i]; } dstr[L] = lstr[L] = 0;
    for (int j = 0; j < npos; j++) if (g >> j & 1) { dstr[pos[j]] = '0'; lstr[pos[j]] = 'o'; }
    uint8_t B[48], R[48], H[100];
    for (uint64_t i = lo; i < hi; i++) {
        if (i > lo) { int j = __builtin_ctzll(i); uint64_t bit = (g >> j) & 1; if (bit) v = big_add(v, wt[j]); else v = big_sub(v, wt[j]); g ^= 1ULL << j; if (bit) { dstr[pos[j]] = '0' + (s[pos[j]] - 'a' + 1); lstr[pos[j]] = s[pos[j]]; } else { dstr[pos[j]] = '0'; lstr[pos[j]] = 'o'; } }
        if (strmode) { try_answer((uint8_t *)dstr, L); try_answer((uint8_t *)lstr, L); }
        if (nonum) { if ((i - lo) % 4000000 == 0 && i > lo) fprintf(stderr, "  ... %llu of %llu\n", (unsigned long long)(i - lo), (unsigned long long)(hi - lo)); continue; }
        size_t n = big_bytes(v, B);
        // text filter
        size_t pr = 0; for (size_t k = 0; k < n; k++) if (B[k] >= 32 && B[k] < 127) pr++;
        if (n >= 10 && pr * 100 >= n * 85) { printf("TEXT\tmask=%llx\trev=%d\t", (unsigned long long)g, rev); fwrite(B, 1, n, stdout); printf("\n"); fflush(stdout); }
        if (textonly) continue;
        try_answer(B, n);
        hexof(B, n, (char *)H); try_answer(H, 2 * n);
        for (size_t k = 0; k < n; k++) R[k] = B[n - 1 - k]; try_answer(R, n);
        if ((i - lo) % 4000000 == 0 && i > lo) fprintf(stderr, "  ... %llu of %llu\n", (unsigned long long)(i - lo), (unsigned long long)(hi - lo));
    }
}

static char **readlines(const char *path, size_t *cnt) {
    FILE *f = fopen(path, "r"); if (!f) { perror(path); exit(1); }
    size_t cap = 1024, n = 0; char **v = malloc(cap * sizeof(char *)); char *line = NULL; size_t lc = 0; ssize_t k;
    while ((k = getline(&line, &lc, f)) > 0) { if (line[k-1] == '\n') k--; if (k == 0) continue; if (n == cap) { cap *= 2; v = realloc(v, cap * sizeof(char *)); } v[n] = malloc(k + 1); memcpy(v[n], line, k); v[n][k] = 0; n++; }
    fclose(f); *cnt = n; return v;
}
// orders: 1 = A+B only, 2 = B+A only, 3 = both
static void cross_mode(const char *fa, const char *fb, const char *mid, int part, int nparts, int orders) {
    size_t na, nb; char **A = readlines(fa, &na), **B = readlines(fb, &nb);
    fprintf(stderr, "cross: %zu x %zu, mid=%s part %d/%d orders=%d\n", na, nb, mid ? mid : "(none)", part, nparts, orders);
    char buf[4096];
    for (size_t i = part; i < na; i += nparts) {
        size_t la = strlen(A[i]);
        for (size_t j = 0; j < nb; j++) {
            size_t lb = strlen(B[j]);
            for (int ord = 0; ord < 2; ord++) {
                if (!(orders >> ord & 1)) continue;
                size_t n = 0;
                if (ord == 0) { memcpy(buf, A[i], la); memcpy(buf + la, B[j], lb); n = la + lb; }
                else { memcpy(buf, B[j], lb); memcpy(buf + lb, A[i], la); n = la + lb; }
                try_answer((uint8_t *)buf, n);
                if (mid) { size_t lm = strlen(mid); memcpy(buf + n, mid, lm); try_answer((uint8_t *)buf, n + lm); }
            }
        }
        if (i % 500 == (size_t)part) fprintf(stderr, "  ... row %zu of %zu\n", i, na);
    }
}
int main(int argc, char **argv) {
    const char *mode = "stdin"; const char *dig = NULL; int zv = 2, rev = 0, part = 0, nparts = 1, textonly = 0, orders = 1; const char *fa = NULL, *fb = NULL, *mid = NULL;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-c") && i + 2 < argc) { load_con(argv[i + 1], argv[i + 2]); i += 2; }
        else if (!strcmp(argv[i], "-f") && i + 1 < argc) formmask = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--dbbi") && i + 1 < argc) { mode = "dbbi"; dig = argv[++i]; }
        else if (!strcmp(argv[i], "--zero") && i + 1 < argc) zv = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--rev")) rev = 1;
        else if (!strcmp(argv[i], "--part") && i + 2 < argc) { part = atoi(argv[i + 1]); nparts = atoi(argv[i + 2]); i += 2; }
        else if (!strcmp(argv[i], "--textonly")) textonly = 1;
        else if (!strcmp(argv[i], "--strforms")) strmode = 1;
        else if (!strcmp(argv[i], "--nonum")) nonum = 1;
        else if (!strcmp(argv[i], "--cross") && i + 2 < argc) { mode = "cross"; fa = argv[i+1]; fb = argv[i+2]; i += 2; }
        else if (!strcmp(argv[i], "--mid") && i + 1 < argc) mid = argv[++i];
        else if (!strcmp(argv[i], "--both")) orders = 3;
        else if (!strcmp(argv[i], "--order") && i + 1 < argc) orders = atoi(argv[++i]);
    }
    if (!strcmp(mode, "dbbi")) dbbi_mode(dig, zv, rev, part, nparts, textonly);
    else if (!strcmp(mode, "cross")) cross_mode(fa, fb, mid, part, nparts, orders);
    else {
        char *line = NULL; size_t cap = 0; ssize_t n; unsigned long long cands = 0;
        while ((n = getline(&line, &cap, stdin)) > 0) {
            if (line[n - 1] == '\n') n--;
            if (n == 0) continue;
            cands++; try_answer((uint8_t *)line, n);
        }
        fprintf(stderr, "candidates %llu\n", cands);
    }
    double exp = 0; for (int p = 1; p <= 16; p++) exp += pow(256, -p) * 256.0 / 255.0 * (p == 1 ? 1 : 1) * 0; // placeholder
    exp = tests * (1.0 / 256 + 1.0 / 65536 + 1.0 / 16777216);
    fprintf(stderr, "SUMMARY tests=%llu validpads=%llu expected~%.0f flags=%llu\n", tests, validpads, exp, flags);
    for (int c = 0; c < ncons; c++) { fprintf(stderr, "  %s pads:", cons[c].name); for (int p = 1; p <= 16; p++) if (hist[c][p]) fprintf(stderr, " %d:%llu", p, hist[c][p]); fprintf(stderr, "\n"); }
    fprintf(stderr, "AUDIT retained=%llu omitted=%llu; padding is not proof; heuristics rank only; overflow means incomplete review\n", retained, validpads - retained);
    return validpads > retained ? 2 : 0;
}
