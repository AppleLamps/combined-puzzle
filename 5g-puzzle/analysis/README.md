# Analysis scripts

Reproduce the figures in `../GROUP_COMMS_ANALYSIS.md`:

```bash
python3 analysis/parse_chats.py
python3 analysis/analyze.py
python3 analysis/extract_threads.py
python3 analysis/extract_quotes.py
```

`parse_chats.py` writes `/tmp/gsmg/messages.jsonl` (not committed).  
`analyze.py` writes `analysis/stats.json`.
