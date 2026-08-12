"""
Step 4: Run ALL items through ONE arm, save raw responses, score with M1/M2.
Usage: python src/run/run_arm.py A3
Saves: runs/A3_responses.jsonl  (raw, never overwritten by scoring)
       results/A3_scored.jsonl
"""
import json, sys, time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "score"))
from metrics_citation import m1_citation_validity, m2_citation_accuracy

ITEMS = ROOT / "data/eval/vertical_slice_12.jsonl"
MODEL = "gpt-4o-mini-2024-07-18"
ARM = sys.argv[1] if len(sys.argv) > 1 else "A3"

SYSTEM_PROMPT = (
    "You are a legal information assistant answering questions about Nigerian "
    "copyright law. Base your answer on the Nigerian Copyright Act 2022. "
    "Cite the specific section of the Act that supports your answer."
)

load_dotenv(ROOT / ".env")
client = OpenAI()

items = [json.loads(l) for l in ITEMS.read_text(encoding="utf-8").splitlines() if l.strip()]
print(f"arm={ARM} model={MODEL} items={len(items)}\n")

responses, total_tokens = [], 0
for n, item in enumerate(items, 1):
    try:
        r = client.chat.completions.create(
            model=MODEL, temperature=0,
            messages=[{"role": "system", "content": SYSTEM_PROMPT},
                      {"role": "user", "content": item["question"]}],
        )
        ans = r.choices[0].message.content
        total_tokens += r.usage.total_tokens
        responses.append({"arm": ARM, "model": r.model, "item_id": item["id"],
                          "category": item["category"], "response": ans,
                          "tokens": r.usage.total_tokens})
        print(f"[{n:2}/{len(items)}] {item['id']:14} ok  ({r.usage.total_tokens} tok)")
    except Exception as e:
        print(f"[{n:2}/{len(items)}] {item['id']:14} FAILED: {e}")
        responses.append({"arm": ARM, "item_id": item["id"],
                          "category": item["category"], "response": None, "error": str(e)})
    time.sleep(0.3)

# --- save RAW first, before any scoring ---
(ROOT / "runs").mkdir(exist_ok=True)
raw = ROOT / f"runs/{ARM}_responses.jsonl"
raw.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in responses) + "\n",
               encoding="utf-8")
print(f"\nraw responses -> {raw}   (total tokens: {total_tokens})")

# --- score ---
by_id = {i["id"]: i for i in items}
scored = []
for r in responses:
    if not r.get("response"):
        continue
    item = by_id[r["item_id"]]
    m1 = m1_citation_validity(r["response"])
    m2 = m2_citation_accuracy(r["response"], item.get("gold_sections", []))
    scored.append({**r, "m1": m1, "m2": m2})

(ROOT / "results").mkdir(exist_ok=True)
out = ROOT / f"results/{ARM}_scored.jsonl"
out.write_text("\n".join(json.dumps(s, ensure_ascii=False) for s in scored) + "\n",
               encoding="utf-8")

# --- summary ---
print(f"scored -> {out}\n")
print(f"{'item':15}{'cat':15}{'cites':6}{'fabricated':12}{'M2 verdict'}")
print("-" * 70)
for s in scored:
    print(f"{s['item_id']:15}{s['category']:15}{s['m1']['n_citations']:<6}"
          f"{s['m1']['n_fabricated']:<12}{s['m2']['verdict']}")

from collections import Counter
print("\nM2 verdicts:", dict(Counter(s["m2"]["verdict"] for s in scored)))
tot_c = sum(s["m1"]["n_citations"] for s in scored)
tot_f = sum(s["m1"]["n_fabricated"] for s in scored)
print(f"M1: {tot_f}/{tot_c} citations fabricated"
      f" ({100*tot_f/tot_c:.1f}%)" if tot_c else "M1: no citations")
