import json
from pathlib import Path

bench = {b["item_id"]: b for b in (json.loads(l) for l in
         Path("data/eval/benchmark_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}
gold  = {g["item_id"]: g for g in (json.loads(l) for l in
         Path("data/eval/gold_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}

div = sorted(i for i, b in bench.items() if b["category"] == "divergence")
out = []
for i in div:
    b, g = bench[i], gold.get(i, {})
    fd = b.get("foreign_default") or {}
    out.append(f"{'='*78}\n{i}\nQ: {b['question']}\n"
               f"GOLD (Nigerian): {g.get('gold_answer','')[:400]}\n"
               f"US: {str(fd.get('US',''))[:300]}\n"
               f"UK: {str(fd.get('UK',''))[:300]}\n")
Path("divergence_dump.txt").write_text("\n".join(out), encoding="utf-8")
print(f"wrote divergence_dump.txt  ({len(div)} items)")
