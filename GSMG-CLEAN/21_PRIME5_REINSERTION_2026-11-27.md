# 21 - Prime 5 reinserted into the source record

**Status (2026-11-27): NO MATCH.** This closes one reading. It does not show that no continuation exists.

The reading: the blue prime 5 was the quantity removed to make the poster sums balance at 479, and putting that prime back into the raw pre-Beaufort source record produces the prize scalar. The source record is phase 3.2 bytes `[447:1986]`, SHA-256 `bd7a29432546c67c4170e0c523ddbf43ae82d20ee187d1b4dbf7907a0faf4c7b`.

The sealed family is 116 scalars: XOR, add and insert of `0x05`, the 24 primes, the 24 primes mod 256, and the big-endian pair `(484, 479)`, at zero-based and one-based prime indices, on the full record and on the 32-byte window at 479; append of each operand after that window; XOR of `0x05` across the window. Each result is taken as the 32-byte window and as SHA-256 of the whole result. No AES.

Every scalar was inside the curve order. None matched Half's pubkey or either prize hash160.

116 9bb5f43408d7fa67d0893bc64f0274328a41af5308565e46aa4250d23605e732 NO MATCH

Detail: [runs/2026-11-27_prime5_reinsertion/REPORT.md](runs/2026-11-27_prime5_reinsertion/REPORT.md).
