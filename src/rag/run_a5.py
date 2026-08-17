"""Step 6c: Arm A5 = gpt-4o-mini + RAG (top-5 retrieved chunks)."""
import json, sys, time, faiss
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/"src/score"))
from metrics_citation import m1_citation_validity, m2_citation_accuracy

MODEL = "gpt-4o-mini-2024-07-18"
ARM, TOPK = "A5", 5

items = [json.loads(l) for l in (ROOT/"data/eval/vertical_slice_12.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
chunks = [json.loads(l) for l in (ROOT/"data/derived/chunks.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
index = faiss.read_index(str(ROOT/"data/derived/chunks.faiss"))
embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")

load_dotenv(ROOT/".env")
client = OpenAI()

SYSTEM = ("You are a legal information assistant answering questions about Nigerian "
          "copyright law. Base your answer on the Nigerian Copyright Act 2022. "
          "Cite the specific section of the Act that supports your answer.")

responses = []
for n, item in enumerate(items, 1):
    qv = embedder.encode([item["question"]], normalize_embeddings=True).astype("float32")
    D, I = index.search(qv, TOPK)
    retrieved = [chunks[i] for i in I[0]]
    ctx = "\n\n".join(c["text"] for c in retrieved)
    user = f"Relevant extracts from the Nigerian Copyright Act 2022:\n\n{ctx}\n\nQuestion: {item['question']}"
    try:
        r = client.chat.completions.create(model=MODEL, temperature=0,
            messages=[{"role":"system","content":SYSTEM},{"role":"user","content":user}])
        ans = r.choices[0].message.content
        responses.append({"arm":ARM,"model":r.model,"item_id":item["id"],
            "category":item["category"],"response":ans,
            "retrieved":[c["chunk_id"] for c in retrieved],
            "retrieval_scores":[float(x) for x in D[0]],
            "tokens":r.usage.total_tokens})
        print(f"[{n:2}/{len(items)}] {item['id']:14} ok  retrieved: {[c['chunk_id'] for c in retrieved]}")
    except Exception as e:
        print(f"[{n:2}/{len(items)}] {item['id']:14} FAILED: {e}")
    time.sleep(0.3)

(ROOT/"runs").mkdir(exist_ok=True)
(ROOT/f"runs/{ARM}_responses.jsonl").write_text(
    "\n".join(json.dumps(r, ensure_ascii=False) for r in responses)+"\n", encoding="utf-8")
print(f"\nwrote runs/{ARM}_responses.jsonl")
