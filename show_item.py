import json, sys
from pathlib import Path

iid = sys.argv[1] if len(sys.argv) > 1 else "NCB-C-006"

items = {json.loads(l)["item_id"]: json.loads(l)
         for l in Path("data/eval/benchmark_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
it = items.get(iid)
if not it:
    print("unknown item:", iid); raise SystemExit

print("="*78)
print(iid, "|", it["category"], "| expected:", it.get("expected_provision"))
print("-"*78)
print("Q:", it["question"])
if it.get("foreign_default"):
    for j, v in it["foreign_default"].items():
        if j in ("US","UK"):
            print(f"\n{j} position: {str(v)[:180]}")

for arm in ["A1", "A3", "A5"]:
    p = Path(f"runs/{arm}_responses_180.jsonl")
    if not p.exists(): continue
    for l in p.read_text(encoding="utf-8").splitlines():
        if not l.strip(): continue
        r = json.loads(l)
        if r["item_id"] == iid:
            print("\n" + "="*78)
            print(f"{arm}  ({r['model']})")
            if r.get("retrieved"):
                print("retrieved:", r["retrieved"])
            print("-"*78)
            print(r["response"])
            break
