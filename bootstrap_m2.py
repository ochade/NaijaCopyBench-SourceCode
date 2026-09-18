"""Bootstrap confidence intervals for M2 citation accuracy.
Resampling unit is the item. Category E excluded: those items have no
governing provision against which accuracy can be assessed.
"""
import json, random
from pathlib import Path

random.seed(42)
B = 10000
CATS = ["single_hop","multi_hop","divergence","control","summarization"]

def load(arm):
    rows = [json.loads(l) for l in
            Path(f"results/{arm}_m2_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    return [r for r in rows if r["category"] != "fabrication"]

def acc(items):
    if not items: return None
    ok = sum(1 for i in items if i["m2_verdict"] in ("correct","correct_section_coarse"))
    return 100 * ok / len(items)

def ci(items, b=B):
    obs = acc(items)
    if obs is None: return None, None, None
    n = len(items)
    reps = sorted(acc([items[random.randrange(n)] for _ in range(n)]) for _ in range(b))
    return obs, reps[int(0.025*b)], reps[int(0.975*b)]

arms = {a: load(a) for a in ["A1","A2","A3","A5"] if Path(f"results/{a}_m2_180.jsonl").exists()}

print(f"M2 citation accuracy, percentile bootstrap over items, B={B}")
print("Category E excluded (no governing provision); n = 145 per arm\n")
print(f"{'arm':6}{'accuracy':>11}{'95% CI':>20}")
print("-"*38)
for a, items in arms.items():
    o, lo, hi = ci(items)
    print(f"{a:6}{o:>10.1f}%   [{lo:5.1f}, {hi:5.1f}]")

print("\npairwise differences (percentage points)")
print(f"{'comparison':16}{'diff':>9}{'95% CI':>20}{'':>6}")
print("-"*52)
for x, y in [("A1","A2"), ("A1","A3"), ("A1","A5"), ("A2","A5"), ("A3","A5")]:
    if x not in arms or y not in arms: continue
    ix, iy = arms[x], arms[y]
    d = acc(ix) - acc(iy)
    reps = sorted(acc([ix[random.randrange(len(ix))] for _ in range(len(ix))]) -
                  acc([iy[random.randrange(len(iy))] for _ in range(len(iy))])
                  for _ in range(B))
    lo, hi = reps[int(0.025*B)], reps[int(0.975*B)]
    sig = "excludes 0" if (lo > 0 or hi < 0) else "includes 0"
    print(f"{x} - {y:<11}{d:>8.1f}   [{lo:6.1f}, {hi:6.1f}]  {sig}")

print("\nby category, with 95% CI")
for cat in CATS:
    print(f"\n  {cat}")
    for a, items in arms.items():
        sub = [i for i in items if i["category"] == cat]
        o, lo, hi = ci(sub, b=2000)
        print(f"    {a}  {o:5.1f}%   [{lo:5.1f}, {hi:5.1f}]   n={len(sub)}")

out = {"B": B, "n_per_arm": {a: len(v) for a, v in arms.items()},
       "overall": {a: dict(zip(("acc","lo","hi"), ci(v))) for a, v in arms.items()}}
Path("results/m2_bootstrap.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print("\nwrote results/m2_bootstrap.json")
