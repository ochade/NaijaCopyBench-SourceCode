import json, sys
from pathlib import Path
from collections import Counter
sys.path.insert(0, "src/score")
from metrics_citation import m1_citation_validity, m2_citation_accuracy

items = {i["id"]: i for i in (json.loads(l) for l in
         Path("data/eval/vertical_slice_12.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}
resp = [json.loads(l) for l in Path("runs/A5_responses.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]

scored = []
for r in resp:
    it = items[r["item_id"]]
    gold = {g.split("(")[0] for g in it.get("gold_sections", [])}
    got  = {c.split("(")[0].lstrip("s") for c in r["retrieved"]}
    scored.append({**r,
        "m1": m1_citation_validity(r["response"]),
        "m2": m2_citation_accuracy(r["response"], it.get("gold_sections", [])),
        "gold_retrieved": bool(gold & got) if gold else None})

Path("results/A5_scored.jsonl").write_text(
    "\n".join(json.dumps(s, ensure_ascii=False) for s in scored)+"\n", encoding="utf-8")

print(f"{'item':15}{'gold_retr':11}{'cites':6}{'fab':5}{'M2'}")
print("-"*62)
for s in scored:
    print(f"{s['item_id']:15}{str(s['gold_retrieved']):11}{s['m1']['n_citations']:<6}"
          f"{s['m1']['n_fabricated']:<5}{s['m2']['verdict']}")
v = Counter(s["m2"]["verdict"] for s in scored)
tc = sum(s["m1"]["n_citations"] for s in scored); tf = sum(s["m1"]["n_fabricated"] for s in scored)
gr = sum(1 for s in scored if s["gold_retrieved"])
print(f"\nA5: correct {v.get('correct',0)}/9 | fabricated {tf}/{tc} ({100*tf/tc:.1f}%)")
print(f"gold chunk retrieved: {gr}/9")
