import json
from pathlib import Path
cs = [json.loads(l) for l in Path("data/derived/chunks.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
big = sorted([c for c in cs if c["n_words"] > 400], key=lambda x: -x["n_words"])
print(f"{len(big)} chunks over 400 words:\n")
for c in big:
    print(f"  {c['chunk_id']:10} sub={str(c['subsection']):5} {c['n_words']:4}w  {c['title'][:45]}")
