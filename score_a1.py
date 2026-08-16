import json, sys
from pathlib import Path
sys.path.insert(0, "src/score")
from metrics_citation import m1_citation_validity, m2_citation_accuracy

items = {i["id"]: i for i in (json.loads(l) for l in
         Path("data/eval/vertical_slice_12.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}
resp = [json.loads(l) for l in Path("runs/A1_responses.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]

scored = []
for r in resp:
    it = items[r["item_id"]]
    m1 = m1_citation_validity(r["response"])
    m2 = m2_citation_accuracy(r["response"], it.get("gold_sections", []))
    scored.append({**r, "m1": m1, "m2": m2})

Path("results").mkdir(exist_ok=True)
Path("results/A1_scored.jsonl").write_text(
    "\n".join(json.dumps(s, ensure_ascii=False) for s in scored) + "\n", encoding="utf-8")

print(f"{'item':15}{'cat':15}{'cites':6}{'fab':5}{'M2'}")
print("-"*66)
for s in scored:
    print(f"{s['item_id']:15}{s['category']:15}{s['m1']['n_citations']:<6}"
          f"{s['m1']['n_fabricated']:<5}{s['m2']['verdict']}")

from collections import Counter
print("\nM2:", dict(Counter(s["m2"]["verdict"] for s in scored)))
tc = sum(s["m1"]["n_citations"] for s in scored)
tf = sum(s["m1"]["n_fabricated"] for s in scored)
print(f"M1: {tf}/{tc} fabricated ({100*tf/tc:.1f}%)" if tc else "M1: no citations")
