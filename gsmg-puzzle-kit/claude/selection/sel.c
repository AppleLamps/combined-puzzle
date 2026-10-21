/* ordered selections without repetition, k = 1..KMAX, of the atoms in a file, plain concatenation.
   usage: sel ATOMS KMIN KMAX SHARD NSHARDS   (shard = first-atom index mod NSHARDS) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static char at[64][256]; static int n, used[64], idx[16], kmax, kmin, shard, ns;
static char buf[4096];
static void rec(int d, int len) {
  if (d >= kmin) { buf[len] = '\n'; fwrite(buf, 1, len + 1, stdout); }
  if (d == kmax) return;
  for (int i = 0; i < n; i++) {
    if (used[i]) continue;
    if (d == 0 && i % ns != shard) continue;
    int l = strlen(at[i]); used[i] = 1; memcpy(buf + len, at[i], l);
    rec(d + 1, len + l); used[i] = 0;
  }
}
int main(int c, char **v) {
  FILE *f = fopen(v[1], "r"); kmin = atoi(v[2]); kmax = atoi(v[3]); shard = atoi(v[4]); ns = atoi(v[5]);
  while (n < 64 && fgets(at[n], 256, f)) { at[n][strcspn(at[n], "\n")] = 0; if (at[n][0]) n++; }
  static char ob[1 << 20]; setvbuf(stdout, ob, _IOFBF, sizeof ob);
  rec(0, 0); return 0;
}
