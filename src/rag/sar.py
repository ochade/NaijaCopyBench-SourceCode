"""Structure-Aware Reranking (SAR), after Beyond Case Law (arXiv 2604.06173).

Dense retrieval gives seeds; seeds propagate relevance along EXPLICIT statutory
cross-references to recover provisions that are structurally linked but
lexically/semantically disjoint from the query.

    B(n) = (1/L(n)) * sum_{s in S} I(s->n) * S_dense(s) / L(s)

  L(s) = out-degree of seed s   (a seed citing many sections dilutes its vote)
  L(n) = in-degree of candidate (a heavily-cited section is damped)
Final score: S_dense(n) + alpha * B(n)
"""
import json, numpy as np, faiss
from pathlib import Path
from collections import defaultdict
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[2]
chunks = [json.loads(l) for l in (ROOT/"data/derived/chunks.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
xr = json.loads((ROOT/"data/derived/xrefs.json").read_text(encoding="utf-8"))
index = faiss.read_index(str(ROOT/"data/derived/chunks.faiss"))
embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")

# section -> chunk indices  (a section may span several chunks)
sec2idx = defaultdict(list)
for i, c in enumerate(chunks):
    sec2idx[c["section"]].append(i)

# citation graph
edges = [(int(a), int(b)) for a, b in xr["edges"]]
out_edges = defaultdict(set)
for a, b in edges:
    out_edges[a].add(b)
out_deg = {s: max(1, len(t)) for s, t in out_edges.items()}
in_deg = defaultdict(int)
for a, b in edges:
    in_deg[b] += 1

def sar_search(query, k=5, seed_k=10, alpha=0.5):
    qv = embedder.encode([query], normalize_embeddings=True).astype("float32")
    D, I = index.search(qv, max(seed_k, k * 4))
    dense = {int(i): float(s) for s, i in zip(D[0], I[0])}
    seeds = list(I[0][:seed_k])

    # robust voting: seeds propagate to explicitly linked sections
    bonus = defaultdict(float)
    for si in seeds:
        s_sec = chunks[si]["section"]
        Ls = out_deg.get(s_sec, 1)
        for tgt in out_edges.get(s_sec, ()):
            Ln = max(1, in_deg.get(tgt, 1))
            contrib = dense[int(si)] / Ls / Ln
            for ti in sec2idx[tgt]:
                bonus[ti] += contrib

    final = {i: dense.get(i, 0.0) + alpha * bonus.get(i, 0.0)
             for i in set(dense) | set(bonus)}
    top = sorted(final, key=final.get, reverse=True)[:k]
    return [(chunks[i], final[i], dense.get(i, 0.0), bonus.get(i, 0.0)) for i in top]

if __name__ == "__main__":
    items = [json.loads(l) for l in (ROOT/"data/eval/vertical_slice_12.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"graph: {len(edges)} edges, {len(out_edges)} sections with outgoing refs\n")
    print("=== GOLD RECALL@5: dense-only vs SAR ===\n")
    nd = ns = n = 0
    for item in items:
        gold = {g.split("(")[0] for g in item.get("gold_sections", [])}
        if not gold: continue
        n += 1
        q = item["question"]
        qv = embedder.encode([q], normalize_embeddings=True).astype("float32")
        _, I = index.search(qv, 5)
        d_ids = {str(chunks[i]["section"]) for i in I[0]}
        s_ids = {str(c["section"]) for c, *_ in sar_search(q, k=5)}
        dh, sh = bool(gold & d_ids), bool(gold & s_ids)
        nd += dh; ns += sh
        flag = "  <-- SAR FIXED" if sh and not dh else ("  <-- SAR LOST" if dh and not sh else "")
        print(f"{item['id']:14} gold={sorted(gold)!s:12} dense={dh!s:5} SAR={sh}{flag}")
    print(f"\ndense-only recall@5 : {nd}/{n}")
    print(f"SAR        recall@5 : {ns}/{n}")

    print("\n--- MH-001 (gold s.19+s.7; xrefs has 19->7) ---")
    for c, f, d, b in sar_search("A Nigerian federal government ministry produced a training manual in-house in 2018. How long does copyright in it last?", k=8):
        mark = " *" if b > 0 else ""
        print(f"  {c['chunk_id']:9} final={f:.4f} dense={d:.4f} graph_bonus={b:.4f}{mark}")
