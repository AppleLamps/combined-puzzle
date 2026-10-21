# Closed packets

Requires `pycryptodome`, `ecdsa`, `pillow`.

## Packet 1 — Cosmic Duality / yinyang-as-password

```bash
python3 packet/build_hint_sheet.py
python3 packet/extra_door_pixels.py
python3 packet/run_packet.py
```

Frozen list: `password_list.json` (hashed at start to `out/password_list.sha256`).  
Outcome: `RESULTS.md`. **Yinyang-as-password did not decrypt Cosmic Duality.** The published 7-XOR decrypt was reproduced and is not the `1GSMG` key.

## Packet 2 — leftover 3.2 × yellow/blue pixel counts

Operands were the HSV pass (yellow **50400**, blue **96791**). Exact palette blue is **83700**; that password list stays frozen and is not retried.

```bash
python3 packet/run_packet.py \
  --spec password_list_leftover32.json \
  --results-name results_leftover32.json
```

Outcome: `RESULTS_LEFTOVER32.md`. **No leftover-3.2 decrypt** (40 attempts, list SHA-256 `c558330f…5e71`).

## Packet 3 — extra door as a hashed find (not AES)

```bash
python3 packet/extra_door_pixels.py
python3 packet/extra_door_find.py
```

Uses only `#1710` as quoted in 2020 `#3388`, unedited `#4590` / `#7914`. **Does not use `{1,4,21}`.** Does not retry leftover 3.2.  
Outcome: `RESULTS_EXTRA_DOOR.md`. **Main door reproduced. No second URL.** Extra channel `f73d92` hashed, not claimed as a find.

## Packet 4 — matrixsumlist as an operation, then enter

```bash
python3 packet/matrixsumlist.py
python3 packet/run_packet.py \
  --spec password_list_synthesis.json \
  --results-name results_synthesis.json
```

Row/col sums mod 9 on the frozen a–i stream, then leftover 3.2 only (plus Neo passport date forms and Architect two-door sentences). Not a 7-interleave retry.  
Outcome: `RESULTS_SYNTHESIS.md`. **No leftover-3.2 decrypt** (188 attempts, list SHA-256 `60f29326…2baf`). Sum letters are not English.

## Packet — Architect substitution delta

The Beaufort 3.2.1 speech is *The Matrix Reloaded* Architect text with a short list of replacements. Those replacements (not the copied film) are the frozen passwords. No 7-interleave. No brute force.

```bash
python3 packet/run_architect_delta.py
```

Frozen list: `password_list_architect_delta.json` (spec SHA-256 `7a752931…bc7f`).  
Outcome: `RESULTS_ARCHITECT_DELTA.md`. **No leftover-3.2 decrypt** (1008 attempts, 0 readable, 0 prize). The substitutions are instructions, not a password.

