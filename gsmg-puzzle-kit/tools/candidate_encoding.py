"""Unambiguous h3 candidate format; safe to copy with the other tools."""
def decode_candidate(field):
    if not field.startswith('candhex='):
        raise ValueError('ambiguous legacy candidate encoding; require candhex= records')
    return bytes.fromhex(field[len('candhex='):])
