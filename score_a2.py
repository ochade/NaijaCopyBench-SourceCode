import json, importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("mc", "src/score/metrics_citation.py")
mc = importlib.util.module_from_spec(spec); spec.loader.exec_module(mc)

resp = {json.loads(l)["item_id"]: json.loads(l)
        for l in Path("runs/A2_responses_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
gold = {json.loads(l)["item_id"]: json.loads(l)
        for l in Path("data/eval/gold_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
print(f"responses: {len(resp)} | gold: {len(gold)}")

m1_rows, m2_rows = [], []
for iid, r in resp.items():
    text, cat = r["response"], r["category"]
    m1 = mc.m1_citation_validity(text)
    m1_rows.append({"item_id": iid, "category": cat, **({"m1": m1} if not isinstance(m1, dict) else m1)})

    # M2 only where a governing provision exists — exclude fabrication probes (Category E)
    if cat != "fabrication" and iid in gold:
        gs = mc.parse_gold(gold[iid])
        m2 = mc.m2_citation_accuracy(text, gs)
        m2_rows.append({"item_id": iid, "category": cat, **({"m2": m2} if not isinstance(m2, dict) else m2)})

Path("results/A2_m1_180.jsonl").write_text(
    "\n".join(json.dumps(x, ensure_ascii=False) for x in m1_rows) + "\n", encoding="utf-8")
Path("results/A2_m2_180.jsonl").write_text(
    "\n".join(json.dumps(x, ensure_ascii=False) for x in m2_rows) + "\n", encoding="utf-8")

def rate(rows, key):
    vals = [x[key] for x in rows if isinstance(x.get(key), (int, float, bool))]
    return (sum(vals) / len(vals) * 100, len(vals)) if vals else (None, 0)

# M1 fabrication = share of responses whose citations are NOT all valid.
# Adjust the sense once we see the field: if m1=1 means "valid", fabrication = 100 - rate.
m1r, m1n = rate(m1_rows, "m1")
m2r, m2n = rate(m2_rows, "m2")
print(f"\nA2 M1 field mean: {m1r if m1r is None else round(m1r,1)}%  (n={m1n})")
print(f"A2 M2 accuracy:   {m2r if m2r is None else round(m2r,1)}%  (n={m2n})")
print("\nM1 sample rows:", *m1_rows[:2], sep="\n  ")
print("M2 sample rows:", *m2_rows[:2], sep="\n  ")
