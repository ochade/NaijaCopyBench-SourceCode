import json, sys
sys.path.insert(0, "src/rag")
from hybrid import hybrid_search, chunks
from pathlib import Path

items = [json.loads(l) for l in Path("data/eval/vertical_slice_12.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
print("Is gold in the POOL of 50 (even if not in top-5)?\n")
in5 = in50 = n = 0
for item in items:
    gold = {g.split("(")[0] for g in item.get("gold_sections", [])}
    if not gold: continue
    n += 1
    res = hybrid_search(item["question"], k=50)
    ids = [c["chunk_id"].split("(")[0].lstrip("s") for c,*_ in res]
    rank = next((r for r,i in enumerate(ids,1) if i in gold), None)
    in5 += bool(rank and rank <= 5); in50 += bool(rank)
    print(f"  {item['id']:14} gold={sorted(gold)!s:12} rank in pool = {rank}")
print(f"\ngold in top-5 : {in5}/{n}")
print(f"gold in top-50: {in50}/{n}   <- reranker's ceiling")
