import matplotlib.pyplot as plt
from pathlib import Path
Path("figures").mkdir(exist_ok=True)

# M1 fabrication-rate pairwise differences (percentage points), from bootstrap
diffs = [("A1 - A2",  -2.5, -13.2,  8.2),
         ("A1 - A3",   8.7,  -1.6, 18.6),
         ("A1 - A5",  22.1,  13.3, 30.9),
         ("A2 - A5",  24.6,  16.0, 33.3),
         ("A3 - A5",  13.4,   5.8, 21.0)]

fig, ax = plt.subplots(figsize=(7,4))
for i,(lab,d,lo,hi) in enumerate(diffs):
    col = "#c0392b" if (lo>0 or hi<0) else "#95a5a6"
    ax.plot([lo,hi],[i,i],color=col,lw=2)
    ax.plot(d,i,"o",color=col,ms=7)
    ax.text(hi+1.2,i,lab,va="center",fontsize=9)
ax.axvline(0,color="#333",lw=1,ls="--")
ax.set_yticks([])
ax.set_xlabel("Difference in fabrication rate (percentage points)")
ax.set_title("M1 pairwise differences (red = interval excludes zero)",
             loc="left", fontsize=11)
ax.spines[["top","right","left"]].set_visible(False)
plt.tight_layout()
plt.savefig("figures/fig_m1_diff.png", dpi=300, bbox_inches="tight")
print("wrote figures/fig_m1_diff.png")
