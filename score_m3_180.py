"""M3: jurisdictional specificity across all arms, Category C only.

Compares salient legal quantities in a response against three sets: the Nigerian
value from the gold answer, and the US and UK values from the foreign_default
field. Semi-automatic triage - items with no comparable quantity return n/a and
require prose-level review.
"""
import json, sys
from pathlib import Path
from collections import Counter
sys.path.insert(0, "src/score")
from metrics_jurisdiction import m3_jurisdictional

gold = {g["item_id"]: g for g in
        (json.loads(l) for l in Path("data/eval/gold_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}
bench = {b["item_id"]: b for b in
         (json.loads(l) for l in Path("data/eval/benchmark_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}

summary = {}
for arm in ["A1", "A3", "A5"]:
    resp = [json.loads(l) for l in
            Path(f"runs/{arm}_responses_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    scored = []
    for r in resp:
        if r["category"] != "divergence":
            continue
        fd = bench.get(r["item_id"], {}).get("foreign_default")
        ga = gold.get(r["item_id"], {}).get("gold_answer", "")
        v = m3_jurisdictional(r["response"], ga, fd)
        scored.append({**r, "gold_answer": ga, "m3": v})
    Path(f"results/{arm}_m3_180.jsonl").write_text(
        "\n".join(json.dumps(s, ensure_ascii=False) for s in scored) + "\n", encoding="utf-8")
    summary[arm] = scored

print(f"M3 on Category C (divergence), n = {len(summary['A1'])} per arm\n")
VERDICTS = ["NG_correct", "foreign_substituted", "both_present",
            "other_wrong", "n/a_no_quantities", "n/a"]
print(f"{'verdict':22}" + "".join(f"{a:>8}" for a in summary))
print("-" * (22 + 8*len(summary)))
for v in VERDICTS:
    row = f"{v:22}"
    for a, sc in summary.items():
        row += f"{sum(1 for s in sc if s['m3']['verdict'] == v):>8}"
    print(row)

print("\ndecidable items only (NG_correct + foreign_substituted)")
for a, sc in summary.items():
    dec = [s for s in sc if s["m3"]["verdict"] in ("NG_correct", "foreign_substituted")]
    ng = sum(1 for s in dec if s["m3"]["verdict"] == "NG_correct")
    print(f"  {a}: {ng}/{len(dec)} Nigerian" + (f"  ({100*ng/len(dec):.1f}%)" if dec else ""))

print("\nsubstitutions by jurisdiction")
for a, sc in summary.items():
    js = Counter()
    for s in sc:
        if s["m3"]["verdict"] == "foreign_substituted":
            for j in s["m3"].get("jurisdictions", {}):
                js[j] += 1
    print(f"  {a}: {dict(js) if js else 'none detected'}")

print("\nitems flagged foreign_substituted")
for a, sc in summary.items():
    hits = [s for s in sc if s["m3"]["verdict"] == "foreign_substituted"]
    if hits:
        print(f"\n  {a}")
        for s in hits[:6]:
            print(f"    {s['item_id']}  {s['m3'].get('jurisdictions')}")
