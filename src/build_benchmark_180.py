import json
from pathlib import Path
from collections import Counter

ROOT = Path(".")
OUT = ROOT / "data/eval/benchmark_180.jsonl"

items = []
for cat in ["A","B","C","D","E","F"]:
    p = ROOT / f"data/eval/cat{cat}_internal.jsonl"
    if not p.exists():
        print(f"MISSING: {p}")
        continue
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        r = json.loads(line)
        items.append({
            "item_id": r["item_id"],
            "question": r["question"],
            "category": r.get("category", cat),
            "expected_provision": r.get("expected_provision") or r.get("expected_chain") or "",
            "jurisdiction_cue": r.get("jurisdiction_cue", ""),
            "foreign_default": r.get("foreign_default"),
            "fabrication_tier": r.get("fabrication_tier"),
            "double_annotated": r.get("double_annotated", False),
        })

OUT.write_text("\n".join(json.dumps(i, ensure_ascii=False) for i in items) + "\n",
               encoding="utf-8")
print(f"wrote {OUT}  ({len(items)} items)")
print("by category:", dict(Counter(i["category"] for i in items)))
