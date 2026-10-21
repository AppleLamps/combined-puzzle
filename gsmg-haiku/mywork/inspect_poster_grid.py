grid = [
    "WWKKWBWWKWKKWY",
    "KKBKWWKKKWBWKK",
    "KKWKKKWBWWKWWK",
    "WKKWBWWWWKKKWK",
    "WBKWWWKKWYWKKW",
    "KWWKKWYWKWYWKK",
    "KWWBKKWWWKWYWW",
    "BKKWFWWWWWKWYW",
    "WWWKKBWKKKKKWB",
    "KKBKKKYWKKWWWK",
    "KKWKWWWYWKKWKK",
    "KKKKWWKWBWKKWW",
    "WBWKKKWKWYWKKW",
    "WKBWKKWKKWBWKK"
]

print("Grid dimensions:", len(grid), "x", len(grid[0]))

cells = {'B': [], 'Y': [], 'F': []}
for r in range(14):
    for c in range(14):
        ch = grid[r][c]
        if ch in cells:
            cells[ch].append((r, c))

print(f"B cells ({len(cells['B'])}):", cells['B'])
print(f"Y cells ({len(cells['Y'])}):", cells['Y'])
print(f"F cell ({len(cells['F'])}):", cells['F'])

# What about spiral order?
# In Step 0, spiral starts at (0,0), goes DOWN first, counter-clockwise inward:
def get_spiral():
    visited = [[False]*14 for _ in range(14)]
    r, c = 0, 0
    dr, dc = 1, 0 # down first
    path = []
    for _ in range(196):
        path.append((r, c, grid[r][c]))
        visited[r][c] = True
        nr, nc = r + dr, c + dc
        if not (0 <= nr < 14 and 0 <= nc < 14 and not visited[nr][nc]):
            # turn counter-clockwise: down -> right -> up -> left
            # (dr, dc) = (1,0) -> (0,1) -> (-1,0) -> (0,-1)
            dr, dc = dc, -dr # wait: (1,0) -> (0, -1)? Let's check turn
    return path

# Let's verify Step 0 spiral direction:
# Step 0: "starts at top-left, going down first, counter-clockwise inward"
# (0,0) down to (13,0), then right to (13,13), then up to (0,13), then left to (0,1)
path = []
visited = [[False]*14 for _ in range(14)]
r, c = 0, 0
# directions: down (1,0), right (0,1), up (-1,0), left (0,-1)
dirs = [(1,0), (0,1), (-1,0), (0,-1)]
d_idx = 0
for i in range(196):
    path.append((r, c, grid[r][c]))
    visited[r][c] = True
    dr, dc = dirs[d_idx]
    nr, nc = r + dr, c + dc
    if not (0 <= nr < 14 and 0 <= nc < 14 and not visited[nr][nc]):
        d_idx = (d_idx + 1) % 4
        dr, dc = dirs[d_idx]
        nr, nc = r + dr, c + dc
    r, c = nr, nc

# Where do B, Y, F appear along the spiral path?
special_indices = [(idx, r, c, val) for idx, (r, c, val) in enumerate(path) if val in ('B', 'Y', 'F')]
print("\nSpecial cells along the spiral path:")
for s in special_indices:
    print(f"  spiral index {s[0]:3d}: ({s[1]:2d}, {s[2]:2d}) = {s[3]}")
