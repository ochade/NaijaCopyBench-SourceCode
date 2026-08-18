"""Diagnostic: does deeper retrieval fix the gold-recall problem? A5b = top-15."""
import json, sys, time, faiss
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[2]
MODEL = "gpt-4o-mini-2024-07-18"
ARM, TOPK = "A5b", 15

items = [json.loads(l) for l in (ROOT/"data/eval/vertical_slice_12.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
chunks = [json.loads(l) for l in (ROOT/"data/derived/chunks.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
index = faiss.read_index(str(ROOT/"data/derived/chunks.faiss"))
embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")

load_dotenv(ROOT/".env")
client = OpenAI()

SYSTEM = ("You are a legal information assistant answering questions about Nigerian "
          "copyright law. Base your answer on the Nigerian Copyright Act 2022. "
          "Cite the specific section of the Act that supports your answer.")

# --- first: retrieval-only check, no API calls ---
print("=== RETRIEVAL RECALL: top-5 vs top-15 (no API cost) ===")
hits5 = hits15 = n_gold = 0
for item in items:
    gold = {g.split("(")[0] for g in item.get("gold_sections", [])}
    if not gold: continue
    n_gold += 1
    qv = embedder.encode([item["question"]], normalize_embeddings=True).astype("float32")
    _, I = index.search(qv, TOPK)
    got = [chunks[i]["chunk_id"] for i in I[0]]
    strip = lambda cs: {c.split("(")[0].lstrip("s") for c in cs}
    h5, h15 = bool(gold & strip(got[:5])), bool(gold & strip(got))
    hits5 += h5; hits15 += h15
    rank = next((r for r, c in enumerate(got, 1)
                 if c.split("(")[0].lstrip("s") in gold), None)
    print(f"  {item['id']:14} gold={sorted(gold)}  top5={h5}  top15={h15}  rank={rank}")
print(f"\ngold recall @5 : {hits5}/{n_gold}")
print(f"gold recall @15: {hits15}/{n_gold}")

if hits15 == hits5:
    print("\nNo gain from depth -> the problem is the embedding, not k.")
    print("Skipping API calls.")
    sys.exit(0)

# --- only if depth helped, run the arm ---
print(f"\n=== running {ARM} (top-{TOPK}) ===")
responses = []
for n, item in enumerate(items, 1):
    qv = embedder.encode([item["question"]], normalize_embeddings=True).astype("float32")
    D, I = index.search(qv, TOPK)
    retrieved = [chunks[i] for i in I[0]]
    ctx = "\n\n".join(c["text"] for c in retrieved)
    user = f"Relevant extracts from the Nigerian Copyright Act 2022:\n\n{ctx}\n\nQuestion: {item['question']}"
    r = client.chat.completions.create(model=MODEL, temperature=0,
        messages=[{"role":"system","content":SYSTEM},{"role":"user","content":user}])
    responses.append({"arm":ARM,"model":r.model,"item_id":item["id"],
        "category":item["category"],"response":r.choices[0].message.content,
        "retrieved":[c["chunk_id"] for c in retrieved],
        "retrieval_scores":[float(x) for x in D[0]],"tokens":r.usage.total_tokens})
    print(f"[{n:2}/{len(items)}] {item['id']:14} ok")
    time.sleep(0.3)

(ROOT/f"runs/{ARM}_responses.jsonl").write_text(
    "\n".join(json.dumps(r, ensure_ascii=False) for r in responses)+"\n", encoding="utf-8")
print(f"\nwrote runs/{ARM}_responses.jsonl")
