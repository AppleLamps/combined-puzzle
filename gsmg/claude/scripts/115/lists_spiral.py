def spiral(n):
    """Inward counter-clockwise spiral from the top-left, going down first (dossier s3.0)."""
    top, left, bot, right = 0, 0, n - 1, n - 1; out = []
    while top <= bot and left <= right:
        for r in range(top, bot + 1): out.append((r, left))
        left += 1
        for c in range(left, right + 1): out.append((bot, c))
        bot -= 1
        if left <= right:
            for r in range(bot, top - 1, -1): out.append((r, right))
            right -= 1
        if top <= bot:
            for c in range(right, left - 1, -1): out.append((top, c))
            top += 1
    return out
