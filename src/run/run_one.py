"""
Step 2: Run ONE item through ONE model. Smallest possible pipeline test.
Usage:  python src/run/run_one.py            (defaults to NCB-DIV-001)
        python src/run/run_one.py NCB-FAB-001
"""
import json, sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "data/eval/vertical_slice_12.jsonl"
MODEL = "gpt-4o-mini-2024-07-18"

SYSTEM_PROMPT = (
    "You are a legal information assistant answering questions about Nigerian "
    "copyright law. Base your answer on the Nigerian Copyright Act 2022. "
    "Cite the specific section of the Act that supports your answer."
)

load_dotenv(ROOT / ".env")
client = OpenAI()

# --- load items ---
items = [json.loads(l) for l in ITEMS.read_text(encoding="utf-8").splitlines() if l.strip()]
by_id = {i["id"]: i for i in items}

item_id = sys.argv[1] if len(sys.argv) > 1 else "NCB-DIV-001"
if item_id not in by_id:
    print(f"unknown id {item_id}. available: {list(by_id)}")
    sys.exit(1)
item = by_id[item_id]

# --- call the model ---
resp = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": item["question"]},
    ],
    temperature=0,
)
answer = resp.choices[0].message.content

# --- show it ---
print("=" * 70)
print(f"ITEM      : {item['id']}  [{item['category']}]")
print(f"QUESTION  : {item['question']}")
print("-" * 70)
print("MODEL SAYS:")
print(answer)
print("-" * 70)
print(f"GOLD SECTIONS : {item.get('gold_sections')}")
if item.get("gold_answer"):
    print(f"GOLD ANSWER   : {item['gold_answer']}")
if item.get("gold_verdict"):
    print(f"GOLD VERDICT  : {item['gold_verdict']}  ({item.get('note','')})")
if item.get("foreign_default"):
    print(f"FOREIGN DEFAULT (displacement watch): {item['foreign_default']}")
print("=" * 70)
print(f"model={resp.model}  tokens={resp.usage.total_tokens}")
