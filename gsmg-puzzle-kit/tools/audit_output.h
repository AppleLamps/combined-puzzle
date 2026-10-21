/* Plain-byte validation and bounded retention; no cipher operations. */
#ifndef GSMG_AUDIT_OUTPUT_H
#define GSMG_AUDIT_OUTPUT_H
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
static void audit_print_hex(FILE *out, const uint8_t *data, size_t n) {
    for (size_t i = 0; i < n; i++) fprintf(out, "%02x", data[i]);
}
static int audit_padding(const uint8_t *data, size_t n, size_t block) {
    if (!block || !n || n % block) return 0;
    int pad = data[n - 1];
    if (pad < 1 || (size_t)pad > block) return 0;
    for (size_t i = n - pad; i < n; i++) if (data[i] != pad) return 0;
    return pad;
}
static int audit_retain(unsigned long long *retained, unsigned long long limit) {
    if (*retained >= limit) return 0;
    ++*retained;
    return 1;
}
#endif
