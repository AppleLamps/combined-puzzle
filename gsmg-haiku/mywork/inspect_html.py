import glob, re

for fn in glob.glob('files/*.html'):
    print('=== ' + fn + ' ===')
    content = open(fn, encoding='utf-8', errors='ignore').read()
    # find HTML comments
    comments = re.findall(r'<!--(.*?)-->', content, re.DOTALL)
    for c in comments:
        print('  COMMENT:', c.strip()[:100])
    # find script tags
    scripts = re.findall(r'<script.*?>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
    for s in scripts:
        print('  SCRIPT:', s.strip()[:100])
    # find hidden inputs
    hidden = re.findall(r'<input[^>]*type=["\']hidden["\'][^>]*>', content, re.IGNORECASE)
    for h in hidden:
        print('  HIDDEN:', h)
