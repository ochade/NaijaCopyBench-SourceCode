"""Full run: arm A3 (gpt-4o-mini, no retrieval) over the 180-item benchmark."""
import json, sys, time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "data/eval/benchmark_180.jsonl"
MODEL, ARM = "gpt-4o-mini-2024-07-18", "A3"

SYSTEM = ("You are a legal information assistant answering questions about Nigerian "
          "copyright law. Base your answer on the Nigerian Copyright Act 2022. "
          "Cite the specific section of the Act that supports your answer.")

load_dotenv(ROOT / ".env")
client = OpenAI()
items = [json.loads(l) for l in ITEMS.read_text(encoding="utf-8").splitlines() if l.strip()]

(ROOT / "runs").mkdir(exist_ok=True)
out_path = ROOT / f"runs/{ARM}_responses_180.jsonl"
done = set()
if out_path.exists():
    done = {json.loads(l)["item_id"] for l in out_path.read_text(encoding="utf-8").splitlines() if l.strip()}
    print(f"resuming: {len(done)} already done")

with open(out_path, "a", encoding="utf-8") as f:
    for n, item in enumerate(items, 1):
        if item["item_id"] in done:
            continue
        try:
            r = client.chat.completions.create(
                model=MODEL, temperature=0,
                messages=[{"role":"system","content":SYSTEM},
                          {"role":"user","content":item["question"]}])
            rec = {"arm":ARM,"model":r.model,"item_id":item["item_id"],
                   "category":item["category"],"response":r.choices[0].message.content,
                   "tokens":r.usage.total_tokens}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
            print(f"[{n:3}/{len(items)}] {item['item_id']:14} ok")
        except Exception as e:
            print(f"[{n:3}/{len(items)}] {item['item_id']:14} FAILED: {e}")
        time.sleep(0.25)

print("\nwrote", out_path)
