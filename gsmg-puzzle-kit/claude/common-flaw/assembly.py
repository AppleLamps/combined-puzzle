"""Explicit assembly hypotheses; generation does not test any password."""
def assemble(matrix_strings, last_words):
    out = set(matrix_strings)
    for m in matrix_strings:
        for l in last_words:
            for ordered in (m + l, l + m):
                out.add(ordered)
                out.add(ordered + 'thispassword')
    return out
