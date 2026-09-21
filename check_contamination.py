import json, re
from pathlib import Path
from difflib import SequenceMatcher

ft = [json.loads(l) for l in Path("data/ft/ft_pairs.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
bench = [json.loads(l) for l in Path("data/eval/benchmark_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]

def norm(s): return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()

ftq = {norm(p["question"]) for p in ft}
exact = [b["item_id"] for b in bench if norm(b["question"]) in ftq]
print(f"FT pairs: {len(ft)} | benchmark items: {len(bench)}")
print(f"exact duplicate questions: {len(exact)}", exact[:5])

# near duplicates — report the full distribution, not just the count over threshold
ftl = [norm(p["question"]) for p in ft]
ratios = []
for b in bench:
    nb = norm(b["question"])
    best = max(((SequenceMatcher(None, nb, q).ratio(), q) for q in ftl), default=(0, ""))
    ratios.append((b["item_id"], round(best[0], 3), best[1][:70]))

ratios.sort(key=lambda x: -x[1])
print(f"\nnear duplicates (ratio > 0.80): {len([r for r in ratios if r[1] > 0.80])}")
print(f"max similarity observed: {ratios[0][1]}")
for r in ratios[:5]: print("  ", r)

ho = set(json.loads(Path("data/ft/held_out_sections.json").read_text(encoding="utf-8")))
used = {p["source_section"] for p in ft}
print(f"\nheld-out sections appearing in FT set: {sorted(ho & used) or 'none'}")
print(f"sections covered by FT set: {len(used)}")
