import json, numpy as np, faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer

chunks = [json.loads(l) for l in Path("data/derived/chunks.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
index = faiss.read_index("data/derived/chunks.faiss")
m = SentenceTransformer("BAAI/bge-small-en-v1.5")

s19 = next(c for c in chunks if c["chunk_id"] == "s19")

print("TEST 1: query with s.19's OWN text - does it rank first?")
qv = m.encode([s19["text"]], normalize_embeddings=True).astype("float32")
D, I = index.search(qv, 3)
for r,(s,i) in enumerate(zip(D[0],I[0]),1):
    print(f"  {r}. {chunks[i]['chunk_id']:8} {s:.3f}")

print("\nTEST 2: score spread over ALL chunks for the failing query")
q = "Under the Nigerian Copyright Act 2022, what is the term of copyright in a literary work?"
qv = m.encode([q], normalize_embeddings=True).astype("float32")
D, I = index.search(qv, len(chunks))
sc = D[0]
print(f"  max {sc.max():.3f} | min {sc.min():.3f} | mean {sc.mean():.3f} | std {sc.std():.3f}")
rank = [chunks[i]["chunk_id"] for i in I[0]].index("s19") + 1
print(f"  s19 rank: {rank}/{len(chunks)}  score {sc[rank-1]:.3f}  (top score {sc.max():.3f})")
print(f"  gap between top and s19: {sc.max()-sc[rank-1]:.3f}")
