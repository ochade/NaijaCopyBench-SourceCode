import json
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse

x = json.loads(Path("data/derived/xrefs.json").read_text(encoding="utf-8"))
m = json.loads(Path("data/derived/section_map.json").read_text(encoding="utf-8"))

G = nx.DiGraph()
G.add_edges_from((int(a), int(b)) for a, b in x["edges"])
deg = dict(G.degree())

# --- cluster membership by Part, for colouring ---
def cluster(n):
    if 63 <= n <= 76:  return "performers"       # Part VIII
    if 31 <= n <= 34:  return "licences"         # compulsory licences
    if 54 <= n <= 62:  return "takedown"         # Part VII
    if 9  <= n <= 13:  return "nature"           # nature of copyright
    return "other"

PALETTE = {"performers":"#8e44ad", "licences":"#16a085", "takedown":"#d35400",
           "nature":"#2980b9", "other":"#95a5a6"}

sizes  = [200 + 150 * deg[n] for n in G.nodes()]
colors = [PALETTE[cluster(n)] for n in G.nodes()]
# hubs get a heavier ring rather than a different fill
edgecols = ["#c0392b" if deg[n] >= 5 else "white" for n in G.nodes()]
edgewid  = [2.2 if deg[n] >= 5 else 0.7 for n in G.nodes()]

pos = nx.spring_layout(G, seed=11, k=1.9, iterations=800)

fig, ax = plt.subplots(figsize=(13, 9.5))

nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.22, arrows=True, arrowsize=9,
                       width=0.8, edge_color="#7f8c8d",
                       connectionstyle="arc3,rad=0.08")
nx.draw_networkx_nodes(G, pos, ax=ax, node_size=sizes, node_color=colors,
                       linewidths=edgewid, edgecolors=edgecols)
nx.draw_networkx_labels(G, pos, {n: str(n) for n in G.nodes()},
                        ax=ax, font_size=7.5, font_color="white",
                        font_weight="bold")

ax.set_title("Cross-reference structure of the Copyright Act 2022",
             fontsize=14, pad=34, loc="left")
ax.text(0.0, 1.005,
        "60 directed edges connecting 63 sections; 46 sections with no citational link are omitted. "
        "Node size is proportional to degree.",
        transform=ax.transAxes, fontsize=9, color="#555555", va="bottom")

legend = [
    Line2D([0],[0], marker="o", color="none", label="Nature of copyright (ss.9-13)",
           markerfacecolor=PALETTE["nature"], markersize=11),
    Line2D([0],[0], marker="o", color="none", label="Compulsory licences (ss.31-34)",
           markerfacecolor=PALETTE["licences"], markersize=11),
    Line2D([0],[0], marker="o", color="none", label="Online takedown (ss.54-62)",
           markerfacecolor=PALETTE["takedown"], markersize=11),
    Line2D([0],[0], marker="o", color="none", label="Performers' rights (ss.63-76)",
           markerfacecolor=PALETTE["performers"], markersize=11),
    Line2D([0],[0], marker="o", color="none", label="Other provisions",
           markerfacecolor=PALETTE["other"], markersize=11),
    Line2D([0],[0], marker="o", color="none", label="Degree >= 5 (hub)",
           markerfacecolor="white", markeredgecolor="#c0392b",
           markeredgewidth=2.2, markersize=11),
]
ax.legend(handles=legend, loc="lower left", frameon=False,
          fontsize=9, bbox_to_anchor=(0.0, -0.10), ncol=3)

ax.set_axis_off()
plt.tight_layout()
plt.savefig("figures/xref_graph.png", dpi=300, bbox_inches="tight")
print("wrote figures/xref_graph.png")
print(f"{G.number_of_nodes()} connected sections, {G.number_of_edges()} edges")
