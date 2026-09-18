"""M3 with foreign-phrase markers in addition to quantity matching."""
import json, sys, re
from pathlib import Path
from collections import Counter
sys.path.insert(0, "src/score")
from metrics_jurisdiction import m3_jurisdictional
from foreign_markers import MARKERS

bench = {b["item_id"]: b for b in (json.loads(l) for l in
         Path("data/eval/benchmark_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}
gold  = {g["item_id"]: g for g in (json.loads(l) for l in
         Path("data/eval/gold_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}

def hits(text, item_id):
    t = (text or "").lower()
    return [m for m in MARKERS.get(item_id, []) if m.lower() in t]

summary = {}
for arm in ["A1", "A3", "A5"]:
    resp = [json.loads(l) for l in
            Path(f"runs/{arm}_responses_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    scored = []
    for r in resp:
        if r["category"] != "divergence": continue
        fd = bench.get(r["item_id"], {}).get("foreign_default")
        ga = gold.get(r["item_id"], {}).get("gold_answer", "")
        quant = m3_jurisdictional(r["response"], ga, fd)
        mk = hits(r["response"], r["item_id"])
        if quant["verdict"] == "foreign_substituted":
            verdict, basis = "foreign_substituted", "quantity"
        elif mk:
            verdict, basis = "foreign_substituted", "phrase"
        elif quant["verdict"] == "NG_correct":
            verdict, basis = "NG_correct", "quantity"
        else:
            verdict, basis = "not_displaced", "no marker"
        scored.append({**r, "m3_verdict": verdict, "basis": basis,
                       "markers_hit": mk, "quantity_verdict": quant["verdict"]})
    Path(f"results/{arm}_m3_180.jsonl").write_text(
        "\n".join(json.dumps(s, ensure_ascii=False) for s in scored) + "\n", encoding="utf-8")
    summary[arm] = scored

n = len(summary["A1"])
print(f"M3 with phrase markers, Category C, n = {n} per arm\n")
print(f"{'verdict':22}" + "".join(f"{a:>8}" for a in summary))
print("-" * (22 + 8*len(summary)))
for v in ["foreign_substituted", "NG_correct", "not_displaced"]:
    row = f"{v:22}"
    for a, sc in summary.items():
        row += f"{sum(1 for s in sc if s['m3_verdict'] == v):>8}"
    print(row)

print("\ndisplacement rate")
for a, sc in summary.items():
    d = sum(1 for s in sc if s["m3_verdict"] == "foreign_substituted")
    print(f"  {a}: {d}/{n}  ({100*d/n:.1f}%)")

print("\ndetected by")
for a, sc in summary.items():
    b = Counter(s["basis"] for s in sc if s["m3_verdict"] == "foreign_substituted")
    print(f"  {a}: {dict(b)}")

print("\nmost frequently triggered markers")
allhits = Counter(m for sc in summary.values() for s in sc for m in s["markers_hit"])
for m, c in allhits.most_common(12):
    print(f"  {m:38} {c}")
