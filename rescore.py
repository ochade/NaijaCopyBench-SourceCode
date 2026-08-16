import json, sys
from pathlib import Path
from collections import Counter
sys.path.insert(0, "src/score")
from metrics_citation import m1_citation_validity, m2_citation_accuracy

items = {i["id"]: i for i in (json.loads(l) for l in
         Path("data/eval/vertical_slice_12.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}

for arm in ["A1", "A3"]:
    raw = Path(f"runs/{arm}_responses.jsonl")
    if not raw.exists():
        print(f"{arm}: no raw file, skipping"); continue
    resp = [json.loads(l) for l in raw.read_text(encoding="utf-8").splitlines() if l.strip()]
    scored = []
    for r in resp:
        if not r.get("response"): continue
        it = items[r["item_id"]]
        scored.append({**r,
            "m1": m1_citation_validity(r["response"]),
            "m2": m2_citation_accuracy(r["response"], it.get("gold_sections", []))})
    Path("results").mkdir(exist_ok=True)
    Path(f"results/{arm}_scored.jsonl").write_text(
        "\n".join(json.dumps(s, ensure_ascii=False) for s in scored) + "\n", encoding="utf-8")

    tc = sum(s["m1"]["n_citations"] for s in scored)
    tf = sum(s["m1"]["n_fabricated"] for s in scored)
    v = Counter(s["m2"]["verdict"] for s in scored)
    gold = sum(n for k, n in v.items() if k != "n/a_no_gold")
    print(f"\n=== {arm}  ({scored[0]['model']}) ===")
    print(f"  citations emitted : {tc}")
    print(f"  fabricated        : {tf}  ({100*tf/tc:.1f}%)" if tc else "  no citations")
    print(f"  correct citations : {v.get('correct',0)}/{gold}")
    print(f"  M2 verdicts       : {dict(v)}")
