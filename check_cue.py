import json
from pathlib import Path
from collections import Counter
rows = [json.loads(l) for l in Path("data/eval/benchmark_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
print("jurisdiction_cue across the benchmark:")
print(" ", dict(Counter(r.get("jurisdiction_cue","(missing)") for r in rows)))
print("\nby category:")
for cat in ["single_hop","multi_hop","divergence","control","fabrication","summarization"]:
    sub = [r for r in rows if r["category"] == cat]
    print(f"  {cat:16} {dict(Counter(r.get('jurisdiction_cue','(missing)') for r in sub))}")
