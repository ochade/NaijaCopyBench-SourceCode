import json, sys
from pathlib import Path
from collections import Counter
sys.path.insert(0, "src/score")
from foreign_markers import MARKERS

def hits(text, iid):
    t = (text or "").lower()
    return [m for m in MARKERS.get(iid, []) if m.lower() in t]

def load(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]

orig = {r["item_id"]: r for r in load("runs/A3_responses_180.jsonl")
        if r["category"] == "divergence"}
neut = {r["item_id"]: r for r in load("runs/A3_neutral_divergence.jsonl")}

ids = sorted(set(orig) & set(neut))
print(f"comparing {len(ids)} divergence items, same model, same decoding\n")

o_hits = {i: hits(orig[i]["response"], i) for i in ids}
n_hits = {i: hits(neut[i]["response"], i) for i in ids}

o_d = sum(1 for i in ids if o_hits[i])
n_d = sum(1 for i in ids if n_hits[i])

print(f"{'prompt':34}{'displaced':>11}{'rate':>9}")
print("-"*54)
print(f"{'names the Act (original)':34}{o_d:>11}{100*o_d/len(ids):>8.1f}%")
print(f"{'no jurisdiction named (neutral)':34}{n_d:>11}{100*n_d/len(ids):>8.1f}%")

print("\nitems displaced only under the neutral prompt")
for i in ids:
    if n_hits[i] and not o_hits[i]:
        print(f"  {i}  {n_hits[i]}")
        print(f"     {neut[i]['response'][:200]}")
print("\nitems displaced only under the original prompt")
for i in ids:
    if o_hits[i] and not n_hits[i]:
        print(f"  {i}  {o_hits[i]}")

print("\nmarkers triggered, neutral prompt")
c = Counter(m for v in n_hits.values() for m in v)
for m, k in c.most_common(10):
    print(f"  {m:36} {k}")
