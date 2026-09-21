import json, sys
from pathlib import Path
from collections import Counter
sys.path.insert(0, "src/score")
from metrics_citation import m1_citation_validity

CATS = ["single_hop","multi_hop","divergence","control","fabrication","summarization"]
Path("results").mkdir(exist_ok=True)
summary = {}

for arm in ["A1", "A2", "A3", "A5"]:
    p = Path(f"runs/{arm}_responses_180.jsonl")
    if not p.exists():
        print(f"{arm}: missing"); continue
    resp = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    scored = [{**r, "m1": m1_citation_validity(r["response"])} for r in resp]
    Path(f"results/{arm}_m1_180.jsonl").write_text(
        "\n".join(json.dumps(s, ensure_ascii=False) for s in scored) + "\n", encoding="utf-8")

    tc = sum(s["m1"]["n_citations"] for s in scored)
    tf = sum(s["m1"]["n_fabricated"] for s in scored)
    nocite = sum(1 for s in scored if s["m1"]["n_citations"] == 0)
    summary[arm] = (tc, tf, nocite, scored)

print(f"{'arm':6}{'citations':>11}{'fabricated':>12}{'rate':>9}{'no-cite items':>15}")
print("-"*54)
for arm,(tc,tf,nc,_) in summary.items():
    print(f"{arm:6}{tc:>11}{tf:>12}{100*tf/tc:>8.1f}%{nc:>15}")

print("\nfabrication rate by category")
print(f"{'category':16}" + "".join(f"{a:>12}" for a in summary))
print("-"*52)
for cat in CATS:
    row = f"{cat:16}"
    for arm,(_,_,_,scored) in summary.items():
        sub = [s for s in scored if s["category"] == cat]
        c = sum(s["m1"]["n_citations"] for s in sub)
        f_ = sum(s["m1"]["n_fabricated"] for s in sub)
        row += f"{(100*f_/c if c else 0):>11.1f}%"
    print(row)

print("\nfabrication tiers (all arms)")
tiers = Counter(d["verdict"] for _,(_,_,_,sc) in summary.items()
                for s in sc for d in s["m1"]["detail"] if d["verdict"] != "valid")
for k,v in tiers.most_common():
    print(f"  {k:26} {v}")
