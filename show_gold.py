import json
from pathlib import Path
rows = [json.loads(l) for l in Path("data/eval/gold_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
print(f"{len(rows)} records\n")
seen = set()
for r in rows:
    if r["category"] in seen: continue
    seen.add(r["category"])
    print("="*72)
    print(r["category"].upper())
    for k, v in r.items():
        print(f"  {k:24} {str(v)[:120]}")
    print()
