"""Held-out probe: did A2 generalise from the fine-tuning set, or memorise it?

Ten sections were withheld entirely from training. If A2's citation accuracy on
items whose gold provision falls in a held-out section is comparable to its
accuracy on trained sections, the adapter generalised. A large gap indicates
memorisation of the training pairs rather than acquisition of the statute.
"""
import json, re, random
from pathlib import Path

random.seed(42)
HELD = set(json.loads(Path("data/ft/held_out_sections.json").read_text(encoding="utf-8")))
print("held-out sections:", sorted(HELD, key=int), "\n")

def gold_secs(s):
    """Section numbers in a gold provision string."""
    if not s: return set()
    if re.search(r"\bno\s+(such\s+)?section\b|does\s+not\s+exist", str(s), re.I):
        return set()
    s = re.sub(r"c\.?\s?a\.?\s?2022|copyright act|of this act", " ", str(s), flags=re.I)
    return {m for m in re.findall(r"(?:s|sec|section)?\.?\s*(\d{1,3})", s)
            if 1 <= int(m) <= 109}

gold = {g["item_id"]: g.get("gold_provision","") for g in
        (json.loads(l) for l in Path("data/eval/gold_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}

def load_m2(arm):
    return [json.loads(l) for l in
            Path(f"results/{arm}_m2_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]

def acc(items):
    if not items: return None
    ok = sum(1 for i in items if i["m2_verdict"] in ("correct","correct_section_coarse"))
    return 100*ok/len(items)

def ci(items, b=5000):
    o = acc(items)
    if o is None: return None, None, None
    n = len(items)
    reps = sorted(acc([items[random.randrange(n)] for _ in range(n)]) for _ in range(b))
    return o, reps[int(0.025*b)], reps[int(0.975*b)]

print(f"{'arm':6}{'split':14}{'n':>5}{'accuracy':>11}{'95% CI':>18}")
print("-"*56)
for arm in ["A1","A2","A3","A5"]:
    p = Path(f"results/{arm}_m2_180.jsonl")
    if not p.exists(): continue
    rows = [r for r in load_m2(arm) if r["category"] != "fabrication"]
    ho  = [r for r in rows if gold_secs(gold.get(r["item_id"],"")) & HELD]
    tr  = [r for r in rows if gold_secs(gold.get(r["item_id"],"")) and
           not (gold_secs(gold.get(r["item_id"],"")) & HELD)]
    for label, sub in [("trained", tr), ("held out", ho)]:
        o, lo, hi = ci(sub)
        if o is None:
            print(f"{arm:6}{label:14}{len(sub):>5}      no items")
        else:
            print(f"{arm:6}{label:14}{len(sub):>5}{o:>10.1f}%   [{lo:5.1f}, {hi:5.1f}]")
    print()

# the comparison that matters: A2 trained vs held out
rows = [r for r in load_m2("A2") if r["category"] != "fabrication"]
ho = [r for r in rows if gold_secs(gold.get(r["item_id"],"")) & HELD]
tr = [r for r in rows if gold_secs(gold.get(r["item_id"],"")) and
      not (gold_secs(gold.get(r["item_id"],"")) & HELD)]
if ho and tr:
    d = acc(tr) - acc(ho)
    reps = sorted(acc([tr[random.randrange(len(tr))] for _ in range(len(tr))]) -
                  acc([ho[random.randrange(len(ho))] for _ in range(len(ho))])
                  for _ in range(5000))
    lo, hi = reps[125], reps[4874]
    print(f"A2 trained minus held out: {d:+.1f} points  [{lo:+.1f}, {hi:+.1f}]")
    print("  " + ("excludes zero - evidence of memorisation"
                  if (lo > 0 or hi < 0) else
                  "includes zero - no detectable memorisation effect"))
    print(f"\nheld-out items in the evaluation set: {len(ho)}")
    for r in ho[:12]:
        print(f"  {r['item_id']:12} gold={gold.get(r['item_id'],'')[:26]:28} {r['m2_verdict']}")
