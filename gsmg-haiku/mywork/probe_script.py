import re
p = r'C:\Users\lucas\.gemini\antigravity\brain\8ffe66a9-72e3-491d-b823-00ac4a9c8edb\.system_generated\steps\77\content.md'
s = open(p, encoding='utf-8', errors='replace').read()
for kw in ['quintessential', 'ARCHITECT', 'Architect', 'twenty', 'Source']:
    print(kw, [m.start() for m in re.finditer(kw, s)][:10])
i = s.find('ARCHITECT')
print(s[i - 300:i + 200] if i >= 0 else s[3000:3600])
