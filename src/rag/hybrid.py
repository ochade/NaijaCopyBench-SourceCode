"""Hybrid retrieval: BM25 (sparse) + bge-small (dense), fused with RRF.
Following HyPA-RAG (Kalra et al. 2024) and T2-RAGBench. One configuration, no tuning.
"""
import json, re, numpy as np, faiss
from pathlib import Path
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[2]
chunks = [json.loads(l) for l in (ROOT/"data/derived/chunks.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
index = faiss.read_index(str(ROOT/"data/derived/chunks.faiss"))
embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")

def tok(s):
    return re.findall(r"[a-z0-9]+", s.lower())

bm25 = BM25Okapi([tok(c["text"]) for c in chunks])

def hybrid_search(query, k=5, k_rrf=60, pool=50):
    """Reciprocal Rank Fusion over BM25 and dense rankings."""
    # dense
    qv = embedder.encode([query], normalize_embeddings=True).astype("float32")
    _, dense_I = index.search(qv, pool)
    dense_rank = {int(i): r for r, i in enumerate(dense_I[0], 1)}
    # sparse
    scores = bm25.get_scores(tok(query))
    sparse_I = np.argsort(scores)[::-1][:pool]
    sparse_rank = {int(i): r for r, i in enumerate(sparse_I, 1)}
    # RRF
    fused = {}
    for i in set(dense_rank) | set(sparse_rank):
        fused[i] = (1/(k_rrf + dense_rank.get(i, 10**6)) +
                    1/(k_rrf + sparse_rank.get(i, 10**6)))
    top = sorted(fused, key=fused.get, reverse=True)[:k]
    return [(chunks[i], fused[i], dense_rank.get(i), sparse_rank.get(i)) for i in top]

if __name__ == "__main__":
    items = [json.loads(l) for l in (ROOT/"data/eval/vertical_slice_12.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    print("=== GOLD RECALL: dense-only vs hybrid (no API calls) ===\n")
    hd = hh = n = 0
    for item in items:
        gold = {g.split("(")[0] for g in item.get("gold_sections", [])}
        if not gold: continue
        n += 1
        q = item["question"]
        # dense-only top5
        qv = embedder.encode([q], normalize_embeddings=True).astype("float32")
        _, I = index.search(qv, 5)
        d_ids = {chunks[i]["chunk_id"].split("(")[0].lstrip("s") for i in I[0]}
        # hybrid top5
        h = hybrid_search(q, k=5)
        h_ids = {c["chunk_id"].split("(")[0].lstrip("s") for c,*_ in h}
        dh, hh_ = bool(gold & d_ids), bool(gold & h_ids)
        hd += dh; hh += hh_
        flag = "  <-- FIXED" if hh_ and not dh else ""
        print(f"{item['id']:14} gold={sorted(gold)!s:14} dense={dh!s:5} hybrid={hh_}{flag}")
    print(f"\ndense-only recall@5 : {hd}/{n}")
    print(f"hybrid    recall@5 : {hh}/{n}")

    print("\n--- worked example: s.103 (dense missed it entirely) ---")
    for c, f, dr, sr in hybrid_search("Which court do I file a copyright case in Nigeria?", k=5):
        print(f"  {c['chunk_id']:8} rrf={f:.4f}  dense_rank={dr}  bm25_rank={sr}")
