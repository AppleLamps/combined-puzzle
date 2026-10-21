/* Plain bytes only. No encryption, key search, puzzle data or wallet operations. */
#include <assert.h>
#include <string.h>
#include "../tools/audit_output.h"
int main(void) {
    uint8_t raw[16];
    for (size_t block = 8; block <= 16; block += 8) {
        for (int pad = 1; pad <= (int)block; pad++) {
            memset(raw, 'Z', block);
            memset(raw + block - pad, pad, pad);
            assert(audit_padding(raw, block, block) == pad);
        }
    }
    assert(audit_padding(raw, 0, 16) == 0);
    assert(audit_padding(raw, 16, 0) == 0);
    memset(raw, 'Z', 16); raw[15] = 2;
    assert(audit_padding(raw, 16, 16) == 0);
    raw[14] = 2;
    assert(audit_padding(raw, 16, 16) == 2);
    raw[15] = 1;
    assert(audit_padding(raw, 16, 16) == 1);
    unsigned long long retained = 0;
    for (int i = 0; i < 5; i++) assert(audit_retain(&retained, 2) == (i < 2));
    assert(retained == 2);
    FILE *out = tmpfile(); assert(out);
    audit_print_hex(out, (const uint8_t *)"0x4142", 6);
    rewind(out); char encoded[13] = {0};
    assert(fread(encoded, 1, 12, out) == 12);
    assert(strcmp(encoded, "307834313432") == 0);
    fclose(out);
    puts("PASS C plain-byte padding, bounded retention, literal 0x encoding");
    return 0;
}
