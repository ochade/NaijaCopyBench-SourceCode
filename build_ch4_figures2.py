import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

Path("figures").mkdir(exist_ok=True)
ARMS = ["A1","A2","A3","A5"]
LABEL = {"A1":"Qwen-3B","A2":"Qwen-3B tuned","A3":"gpt-4o-mini","A5":"gpt-4o-mini+RAG"}
COL = {"A1":"#95a5a6","A2":"#8e44ad","A3":"#2980b9","A5":"#16a085"}
CATS = ["single_hop","multi_hop","divergence","control","summarization"]
CATLAB = ["single-hop","multi-hop","divergence","control","summ."]

def load_m2(arm):
    p = Path(f"results/{arm}_m2_180.jsonl")
    if not p.exists(): return {}
    d = {}
    for l in p.read_text(encoding="utf-8").splitlines():
        if not l.strip(): continue
        r = json.loads(l)
        d.setdefault(r["category"], []).append(r["m2_verdict"])
    return d

def load_m1(arm):
    p = Path(f"results/{arm}_m1_180.jsonl")
    if not p.exists(): return {}
    d = {}
    for l in p.read_text(encoding="utf-8").splitlines():
        if not l.strip(): continue
        r = json.loads(l)
        c = r["m1"]["n_citations"]; f = r["m1"]["n_fabricated"]
        d.setdefault(r["category"], [0,0])
        d[r["category"]][0]+=c; d[r["category"]][1]+=f
    return d

def grouped(get_rate, cats, catlab, title, ylab, fname):
    x = np.arange(len(cats)); w = 0.2
    fig, ax = plt.subplots(figsize=(10,5))
    for k, arm in enumerate(ARMS):
        vals = [get_rate(arm, c) for c in cats]
        ax.bar(x + (k-1.5)*w, vals, w, label=LABEL[arm],
               color=COL[arm], edgecolor="white", linewidth=0.5)
    ax.set_xticks(x); ax.set_xticklabels(catlab)
    ax.set_ylabel(ylab); ax.set_title(title, loc="left", fontsize=12)
    ax.set_ylim(0,100); ax.legend(frameon=False, fontsize=9, ncol=4, loc="upper center",
                                  bbox_to_anchor=(0.5,1.13))
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout(); plt.savefig(f"figures/{fname}", dpi=300, bbox_inches="tight")
    print("wrote figures/"+fname)

# M2 accuracy by category (excludes fabrication)
m2 = {a: load_m2(a) for a in ARMS}
def m2rate(arm, cat):
    v = m2[arm].get(cat, [])
    if not v: return 0
    return 100*sum(1 for x in v if x in ("correct","correct_section_coarse"))/len(v)
grouped(m2rate, CATS, CATLAB,
        "Citation accuracy by category and arm (M2)",
        "Correct citations (%)", "fig_m2_bycat.png")

# M1 fabrication by category (includes fabrication category)
m1 = {a: load_m1(a) for a in ARMS}
CATS1 = CATS[:3] + ["control","fabrication","summarization"]
CATLAB1 = ["single-hop","multi-hop","divergence","control","fab. probe","summ."]
def m1rate(arm, cat):
    c,f = m1[arm].get(cat, [0,0])
    return 100*f/c if c else 0
grouped(m1rate, CATS1, CATLAB1,
        "Fabrication rate by category and arm (M1)",
        "Fabricated citations (%)", "fig_m1_bycat.png")

# H3 figure: A5 accuracy when gold retrieved vs not
import re
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
fig, ax = plt.subplots(figsize=(6,4.5))
bars = ax.bar(["gold provision\nretrieved","gold provision\nNOT retrieved"],
              [100*pres_ok/pres_n, 100*abs_ok/abs_n],
              color=["#16a085","#c0392b"], edgecolor="white")
for b,v,n in zip(bars,[100*pres_ok/pres_n,100*abs_ok/abs_n],[pres_n,abs_n]):
    ax.text(b.get_x()+b.get_width()/2, v+2, f"{v:.0f}%\n(n={n})", ha="center", fontsize=10)
ax.set_ylabel("A5 citation accuracy (%)"); ax.set_ylim(0,100)
ax.set_title("A5 accuracy depends on retrieval, not hop depth (H3)", loc="left", fontsize=11)
ax.spines[["top","right"]].set_visible(False)
plt.tight_layout(); plt.savefig("figures/fig_h3_retrieval.png", dpi=300, bbox_inches="tight")
print("wrote figures/fig_h3_retrieval.png")
