import json
from pathlib import Path
rows = [json.loads(l) for l in Path("data/eval/benchmark_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
div = [r for r in rows if r["category"] == "divergence"]
print(f"{len(div)} divergence items\n")
for r in div[:6]:
    fd = r.get("foreign_default") or {}
    print("="*74)
    print(r["item_id"], "|", r["question"][:70])
    for j, v in fd.items():
        print(f"  {j}: {str(v)[:230]}")
    print()
