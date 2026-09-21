import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

Path("figures").mkdir(exist_ok=True)
NAMES = {"A1":"Qwen-3B","A2":"Qwen-3B\ntuned","A3":"gpt-4o-mini","A5":"gpt-4o-mini\n+RAG"}
COL = {"A1":"#95a5a6","A2":"#8e44ad","A3":"#2980b9","A5":"#16a085"}

m1 = json.loads(Path("results/m1_bootstrap.json").read_text())["overall"]
m2 = json.loads(Path("results/m2_bootstrap.json").read_text())["overall"]

def barci(data, key, lo, hi, title, ylab, fname):
    arms = list(data.keys())
    vals = [data[a][key] for a in arms]
    err  = [[data[a][key]-data[a][lo] for a in arms],
            [data[a][hi]-data[a][key] for a in arms]]
    fig, ax = plt.subplots(figsize=(7,4.5))
    ax.bar([NAMES[a] for a in arms], vals, yerr=err, capsize=6,
           color=[COL[a] for a in arms], edgecolor="white", linewidth=1)
    for a,v in zip(arms,vals):
        ax.text(NAMES[a], v+2, f"{v:.1f}%", ha="center", fontsize=10)
    ax.set_ylabel(ylab); ax.set_title(title, loc="left", fontsize=12)
    ax.set_ylim(0, max(vals)+15); ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout(); plt.savefig(f"figures/{fname}", dpi=300, bbox_inches="tight")
    print("wrote figures/"+fname)

barci(m1,"rate","lo","hi","Fabrication rate by arm (M1)","Fabricated citations (%)","fig_m1.png")
barci(m2,"acc","lo","hi","Citation accuracy by arm (M2)","Correct citations (%)","fig_m2.png")

# difference-interval (forest) plot for M2 - the figure that shows which arms differ
diffs = [("A1 - A2",-23.4,-31.7,-15.2),("A1 - A3",1.4,-2.8,6.2),
         ("A1 - A5",-44.8,-53.8,-35.9),("A2 - A5",-21.4,-32.4,-10.3),
         ("A3 - A5",-46.2,-55.2,-37.2)]
fig, ax = plt.subplots(figsize=(7,4))
for i,(lab,d,lo,hi) in enumerate(diffs):
    col = "#c0392b" if lo>0 or hi<0 else "#95a5a6"
    ax.plot([lo,hi],[i,i],color=col,lw=2)
    ax.plot(d,i,"o",color=col,ms=7)
    ax.text(hi+1,i,lab,va="center",fontsize=9)
ax.axvline(0,color="#333",lw=1,ls="--")
ax.set_yticks([]); ax.set_xlabel("Difference in citation accuracy (percentage points)")
ax.set_title("M2 pairwise differences (red = interval excludes zero)",loc="left",fontsize=11)
ax.spines[["top","right","left"]].set_visible(False)
plt.tight_layout(); plt.savefig("figures/fig_m2_diff.png",dpi=300,bbox_inches="tight")
print("wrote figures/fig_m2_diff.png")
