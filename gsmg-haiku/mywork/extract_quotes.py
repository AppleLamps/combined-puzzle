import re, html
s = open(r'C:\Users\lucas\.gemini\antigravity\brain\8ffe66a9-72e3-491d-b823-00ac4a9c8edb\.system_generated\steps\64\content.md', encoding='utf-8').read()
s = re.sub(r'(?s)<style.*?</style>|<script.*?</script>', '', s)
s = re.sub(r'<(br|/p|/dd|/li|/dl)[^>]*>', '\n', s)
t = html.unescape(re.sub(r'<[^>]+>', '', s))
lines = [l.strip() for l in t.split('\n') if l.strip()]
open('wikiquote_reloaded.txt', 'w', encoding='utf-8').write('\n'.join(lines))
for i, l in enumerate(lines):
    if 'Architect' in l:
        print(i, l[:200])
