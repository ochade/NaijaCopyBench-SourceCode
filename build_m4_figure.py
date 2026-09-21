import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

m4 = json.loads(Path("results/m4_scored.json").read_text())["by_arm"]
ARMS = ["A1","A3","A5"]
LABEL = {"A1":"Qwen-3B","A3":"gpt-4o-mini","A5":"gpt-4o-mini+RAG"}

prec, contra = [], []
for a in ARMS:
    d = m4[a]; tot = d["S"]+d["N"]+d["C"]
    prec.append(100*d["S"]/tot)
    contra.append(100*d["C"]/tot)

x = np.arange(len(ARMS)); w = 0.35
fig, ax = plt.subplots(figsize=(7.5,5))
b1 = ax.bar(x-w/2, prec,   w, label="Precision (supported by the Act)",
            color="#16a085", edgecolor="white")
b2 = ax.bar(x+w/2, contra, w, label="Contradiction rate (ruled out by the Act)",
            color="#c0392b", edgecolor="white")
for b,v in list(zip(b1,prec))+list(zip(b2,contra)):
    ax.text(b.get_x()+b.get_width()/2, v+1.5, f"{v:.1f}%", ha="center", fontsize=9)

ax.set_xticks(x); ax.set_xticklabels([LABEL[a] for a in ARMS])
ax.set_ylabel("Percentage of claims"); ax.set_ylim(0,100)
ax.set_title("Claim-level factuality (M4, sampled: 611 claims)", loc="left",
             fontsize=12, pad=12)
# legend BELOW the plot, clear of the title and bars
ax.legend(frameon=False, fontsize=9, loc="upper center",
          bbox_to_anchor=(0.5,-0.12), ncol=2)
ax.spines[["top","right"]].set_visible(False)
plt.tight_layout()
plt.savefig("figures/fig_m4.png", dpi=300, bbox_inches="tight")
print("wrote figures/fig_m4.png")
