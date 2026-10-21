import json

with open('C:/Users/lucas/.gemini/antigravity/brain/8ffe66a9-72e3-491d-b823-00ac4a9c8edb/.system_generated/logs/transcript.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for l in lines:
    d = json.loads(l)
    src = d.get('source')
    t = d.get('type')
    idx = d.get('step_index')
    content = str(d.get('content', ''))
    if t in ('USER_INPUT', 'PLANNER_RESPONSE') and content:
        print(f"=== Step {idx} ({src}, {t}) ===")
        print(content[:600])
        print()
