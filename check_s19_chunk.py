import json
from pathlib import Path
cs = [json.loads(l) for l in Path("data/derived/chunks.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
for c in cs:
    if c["section"] in (19, 103, 4):
        print(f"--- {c['chunk_id']}  ({c['n_words']}w) ---")
        print(c["text"][:350])
        print()
