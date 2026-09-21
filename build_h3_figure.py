import json, re
from pathlib import Path
import matplotlib.pyplot as plt

def gold_secs(s):
    if not s: return set()
    if re.search(r"\bno\s+(such\s+)?section\b|does\s+not\s+exist", str(s), re.I): return set()
    s = re.sub(r"c\.?\s?a\.?\s?2022|copyright act|of this act"," ",str(s),flags=re.I)
    return {m for m in re.findall(r"(?:s|sec|section)?\.?\s*(\d{1,3})",s) if 1<=int(m)<=109}

gold = {g["item_id"]:g.get("gold_provision","") for g in
        (json.loads(l) for l in Path("data/eval/gold_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}
m2v = {r["item_id"]:r["m2_verdict"] for r in
       (json.loads(l) for l in Path("results/A5_m2_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}
resp = [json.loads(l) for l in Path("runs/A5_responses_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]

pres_ok=pres_n=abs_ok=abs_n=0
for r in resp:
    if r["category"]=="fabrication" or "retrieved" not in r: continue
    gs = gold_secs(gold.get(r["item_id"],""))
    got = {c.lstrip("s").split("(")[0] for c in r["retrieved"]}
    ok = m2v.get(r["item_id"]) in ("correct","correct_section_coarse")
    if gs & got: pres_n+=1; pres_ok+=ok
    else: abs_n+=1; abs_ok+=ok

vals = [100*pres_ok/pres_n, 100*abs_ok/abs_n]
ns   = [pres_n, abs_n]

fig, ax = plt.subplots(figsize=(6,5))
bars = ax.bar(["gold provision\nretrieved","gold provision\nNOT retrieved"],
              vals, color=["#16a085","#c0392b"], edgecolor="white", width=0.55)
for b,v,n in zip(bars,vals,ns):
    ax.text(b.get_x()+b.get_width()/2, v+2.5, f"{v:.0f}%",
            ha="center", fontsize=13, fontweight="bold")
    ax.text(b.get_x()+b.get_width()/2, v-6, f"n={n}",
            ha="center", fontsize=10, color="white")

ax.set_ylabel("A5 citation accuracy (%)")
ax.set_ylim(0, 110)
ax.set_title("A5 accuracy depends on retrieval, not hop depth",
             loc="left", fontsize=12, pad=14)
ax.spines[["top","right"]].set_visible(False)
plt.tight_layout()
plt.savefig("figures/fig_h3_retrieval.png", dpi=300, bbox_inches="tight")
print("wrote figures/fig_h3_retrieval.png")
