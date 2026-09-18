"""Bootstrap confidence intervals for M1 fabrication rate.
Resampling unit is the ITEM, not the citation: citations cluster within
responses, so item-level resampling is required for a valid interval.
"""
import json, random
from pathlib import Path
from collections import Counter

random.seed(42)
B = 10000          # bootstrap replicates
CATS = ["single_hop","multi_hop","divergence","control","fabrication","summarization"]

def load(arm):
    p = Path(f"results/{arm}_m1_180.jsonl")
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]

def rate(items):
    c = sum(i["m1"]["n_citations"] for i in items)
    f = sum(i["m1"]["n_fabricated"] for i in items)
    return 100 * f / c if c else None

def ci(items, b=B):
    """Percentile bootstrap over items."""
    n = len(items)
    obs = rate(items)
    if obs is None: return None, None, None
    reps = []
    for _ in range(b):
        s = [items[random.randrange(n)] for _ in range(n)]
        r = rate(s)
        if r is not None: reps.append(r)
    reps.sort()
    return obs, reps[int(0.025 * len(reps))], reps[int(0.975 * len(reps))]

arms = {}
for arm in ["A1", "A2", "A3", "A5"]:
    if Path(f"results/{arm}_m1_180.jsonl").exists():
        arms[arm] = load(arm)

print(f"M1 fabrication rate, percentile bootstrap over items, B={B}\n")
print(f"{'arm':6}{'n':>5}{'rate':>9}{'95% CI':>20}")
print("-" * 42)
overall = {}
for arm, items in arms.items():
    obs, lo, hi = ci(items)
    overall[arm] = (obs, lo, hi)
    print(f"{arm:6}{len(items):>5}{obs:>8.1f}%   [{lo:5.1f}, {hi:5.1f}]")

# pairwise difference intervals - do the arms actually differ?
print("\npairwise differences in fabrication rate (percentage points)")
print(f"{'comparison':16}{'diff':>9}{'95% CI':>20}{'':>6}")
print("-" * 52)
pairs = [("A1","A2"), ("A1","A3"), ("A1","A5"), ("A2","A5"), ("A3","A5")]
for a, b_ in pairs:
    if a not in arms or b_ not in arms: continue
    ia, ib = arms[a], arms[b_]
    d_obs = rate(ia) - rate(ib)
    reps = []
    for _ in range(B):
        sa = [ia[random.randrange(len(ia))] for _ in range(len(ia))]
        sb = [ib[random.randrange(len(ib))] for _ in range(len(ib))]
        ra, rb = rate(sa), rate(sb)
        if ra is not None and rb is not None: reps.append(ra - rb)
    reps.sort()
    lo, hi = reps[int(0.025*len(reps))], reps[int(0.975*len(reps))]
    sig = "excludes 0" if (lo > 0 or hi < 0) else "includes 0"
    print(f"{a} - {b_:<11}{d_obs:>8.1f}   [{lo:6.1f}, {hi:6.1f}]  {sig}")

# per category
print("\nfabrication rate by category, with 95% CI")
for cat in CATS:
    print(f"\n  {cat}")
    for arm, items in arms.items():
        sub = [i for i in items if i["category"] == cat]
        obs, lo, hi = ci(sub, b=2000)
        if obs is None:
            print(f"    {arm}: no citations")
        else:
            print(f"    {arm}  {obs:5.1f}%   [{lo:5.1f}, {hi:5.1f}]   n={len(sub)}")

# save
out = {"B": B, "overall": {k: {"rate": v[0], "lo": v[1], "hi": v[2]}
                           for k, v in overall.items()}}
Path("results/m1_bootstrap.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print("\nwrote results/m1_bootstrap.json")
