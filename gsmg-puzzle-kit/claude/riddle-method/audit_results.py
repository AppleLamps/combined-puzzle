"""Bounded records of padding-valid outputs, independent of heuristic ranking.

Padding validity is not proof of a correct password. Overflow makes review
incomplete; it must never be reported as absence of a solution.
"""
import json


def valid_padding(data, block_size=16):
    if block_size <= 0 or not data or len(data) % block_size:
        return 0
    pad = data[-1]
    return pad if 1 <= pad <= block_size and data[-pad:] == bytes([pad]) * pad else 0


class AuditResults(list):
    def __init__(self, limit=1000):
        super().__init__()
        if limit < 0:
            raise ValueError('negative audit limit')
        self.limit = limit
        self.total = 0

    def append(self, record):
        self.total += 1
        if len(self) < self.limit:
            super().append(record)

    @property
    def omitted(self):
        return self.total - len(self)

    def report(self):
        print('AUDIT retained=%d total=%d omitted=%d; padding is not proof; '
              'heuristics rank only; overflow means incomplete review' %
              (len(self), self.total, self.omitted))

    def emit(self):
        # JSON escapes candidate tabs/newlines; bytes are explicitly typed as hex.
        for record in self:
            print('VALID\t' + json.dumps(record, default=lambda b: {'hex': b.hex()}))
