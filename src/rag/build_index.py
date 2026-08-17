"""Step 6b: Embed chunks with bge-small-en-v1.5, index in FAISS."""
import json, numpy as np, faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[2]
chunks = [json.loads(l) for l in (ROOT/"data/derived/chunks.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
print(f"loaded {len(chunks)} chunks")

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
texts = [c["text"] for c in chunks]
emb = model.encode(texts, normalize_embeddings=True, show_progress_bar=True,
                   batch_size=32).astype("float32")

index = faiss.IndexFlatIP(emb.shape[1])
index.add(emb)

faiss.write_index(index, str(ROOT/"data/derived/chunks.faiss"))
np.save(ROOT/"data/derived/chunk_emb.npy", emb)
print(f"indexed {index.ntotal} chunks, dim {emb.shape[1]}")

# sanity retrieval on the item both models got wrong
for q in ["How long does copyright last in a sound recording?",
          "Do I need to register my book to have copyright?"]:
    qv = model.encode([q], normalize_embeddings=True).astype("float32")
    D, I = index.search(qv, 5)
    print(f"\nquery: {q}")
    for rank, (score, idx) in enumerate(zip(D[0], I[0]), 1):
        c = chunks[idx]
        print(f"  {rank}. {c['chunk_id']:10} {score:.3f}  {c['title'][:45]}")
