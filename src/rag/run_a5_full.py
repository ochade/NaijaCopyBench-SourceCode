"""Full run: arm A5 (gpt-4o-mini + RAG, top-5) over the 180-item benchmark."""
import json, time, faiss
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[2]
MODEL, ARM, TOPK = "gpt-4o-mini-2024-07-18", "A5", 5

items  = [json.loads(l) for l in (ROOT/"data/eval/benchmark_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
chunks = [json.loads(l) for l in (ROOT/"data/derived/chunks.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
index  = faiss.read_index(str(ROOT/"data/derived/chunks.faiss"))
embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")

load_dotenv(ROOT/".env")
client = OpenAI()
SYSTEM = ("You are a legal information assistant answering questions about Nigerian "
          "copyright law. Base your answer on the Nigerian Copyright Act 2022. "
          "Cite the specific section of the Act that supports your answer.")

out_path = ROOT / f"runs/{ARM}_responses_180.jsonl"
done = set()
if out_path.exists():
    done = {json.loads(l)["item_id"] for l in out_path.read_text(encoding="utf-8").splitlines() if l.strip()}
    print(f"resuming: {len(done)} done")

with open(out_path, "a", encoding="utf-8") as f:
    for n, item in enumerate(items, 1):
        if item["item_id"] in done: continue
        qv = embedder.encode([item["question"]], normalize_embeddings=True).astype("float32")
        D, I = index.search(qv, TOPK)
        retrieved = [chunks[i] for i in I[0]]
        ctx = "\n\n".join(c["text"] for c in retrieved)
        user = (f"Relevant extracts from the Nigerian Copyright Act 2022:\n\n{ctx}\n\n"
                f"Question: {item['question']}")
        try:
            r = client.chat.completions.create(model=MODEL, temperature=0,
                messages=[{"role":"system","content":SYSTEM},{"role":"user","content":user}])
            f.write(json.dumps({"arm":ARM,"model":r.model,"item_id":item["item_id"],
                "category":item["category"],"response":r.choices[0].message.content,
                "retrieved":[c["chunk_id"] for c in retrieved],
                "retrieval_scores":[float(x) for x in D[0]],
                "tokens":r.usage.total_tokens}, ensure_ascii=False) + "\n")
            f.flush()
            print(f"[{n:3}/{len(items)}] {item['item_id']:14} ok")
        except Exception as e:
            print(f"[{n:3}/{len(items)}] {item['item_id']:14} FAILED: {e}")
        time.sleep(0.25)

print("\nwrote", out_path)
