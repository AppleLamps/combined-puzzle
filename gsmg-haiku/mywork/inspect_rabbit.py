from PIL import Image

im = Image.open(r'c:\gsmg-puzzle-clean\files\follow_the_white_rabbit.png')
print("Image format:", im.format, "size:", im.size, "mode:", im.mode)

# Let's inspect the palette or pixel colors
colors = im.getcolors(maxcolors=256)
print("Colors in follow_the_white_rabbit.png:", len(colors) if colors else "Many")
if colors:
    for count, col in sorted(colors, reverse=True)[:10]:
        print(f"  count={count}: {col}")
