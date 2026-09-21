import json
from pathlib import Path
x = json.loads(Path("data/derived/xrefs.json").read_text(encoding="utf-8"))
m = json.loads(Path("data/derived/section_map.json").read_text(encoding="utf-8"))
ind = {int(k): v for k, v in x["in_degree"].items()}
outd = {int(k): v for k, v in x["out_degree"].items()}
print("edges:", x["n_edges"], "| sections citing:", len(outd), "| sections cited:", len(ind))
print("\nTOP IN-DEGREE (most referenced)")
for s, d in sorted(ind.items(), key=lambda t: -t[1])[:6]:
    print(f"  s.{s:<4} {d}x  {m[str(s)]['title'][:45]}")
print("\nTOP OUT-DEGREE (most referencing)")
for s, d in sorted(outd.items(), key=lambda t: -t[1])[:6]:
    print(f"  s.{s:<4} {d}  {m[str(s)]['title'][:45]}")
