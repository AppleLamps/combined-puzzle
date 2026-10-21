"""Locate historical full-field/tail copies and explicitly named digest hints."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'runs/2026-09-13_faed_tail'


def flat(value):
    return value if isinstance(value, str) else ''.join(v if isinstance(v, str) else v.get('text', '') for v in value)


def main():
    s = (ROOT/'data/FAED_570.txt').read_text().strip()
    copies = []
    nearby = []
    sources = []
    for chat, name in [('PUZ', 'ChatExport_2026-09-13_result.json'), ('COMM', 'CommunityGroup_2026-09-10_result.json')]:
        path = ROOT/'telegram'/name
        raw = path.read_bytes()
        messages = json.loads(raw)['messages']
        sources.append(dict(chat=chat, file=name, sha256=hashlib.sha256(raw).hexdigest(), messages=len(messages)))
        for m in messages:
            text = flat(m.get('text', ''))
            compact = re.sub(r'\s+', '', text).lower()
            if s in compact or s[523:] in compact:
                copies.append(dict(chat=chat, id=m['id'], date=m.get('date'), edited=m.get('edited'),
                                   author=m.get('from'), original_creator=m.get('from_id') == 'user9815232' and not m.get('forwarded_from'),
                                   entire_faed=s in compact, exact_tail=s[523:] in compact,
                                   text=text))
            if s[:20] in compact and s not in compact:
                a = compact.index(s[:20])
                piece = re.match('[a-i]+', compact[a:]).group()
                nearby.append(dict(chat=chat, id=m['id'], date=m.get('date'), prefix_match_length=len(piece),
                                   candidate=piece, text=text))
    inventory = json.loads((ROOT/'runs/2026-09-13_operation_instructions/creator_inventory.json').read_text())
    hash_names = {}
    for name, expression in [('sha1', r'\bsha[ -]?1\b'), ('ripemd160', r'\bripemd[ -]?160\b'),
                             ('md5', r'\bmd5\b'), ('sha256', r'\bsha[ -]?256\b')]:
        hash_names[name] = [m for m in inventory if re.search(expression, m['text'], re.I)]
    result = dict(sources=sources, exact_copies=sorted(copies, key=lambda m:m['date']),
                  prefix_only_or_different=nearby, explicitly_named_digest_messages=hash_names,
                  limitations=['Whitespace-normalized, case-insensitive text only; attachments and images are not searched.',
                               'Posted dates do not establish original text when an edit timestamp is present.',
                               'Repeated solver copies are not independent creator confirmations.',
                               'No literal hash name does not exclude an indirect clue.'])
    (OUT/'source_trace.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(dict(exact_copy_count=len(copies), earliest_exact_copies=[{k:v for k,v in m.items() if k!='text'} for m in result['exact_copies'][:5]],
                          prefix_only_or_different=len(nearby), digest_name_counts={k:len(v) for k,v in hash_names.items()}), indent=2))


if __name__ == '__main__':
    main()
