import json, re
from pathlib import Path
from collections import defaultdict

def gold_secs(s):
    if not s: return set()
    if re.search(r"\bno\s+(such\s+)?section\b|does\s+not\s+exist", str(s), re.I): return set()
    s = re.sub(r"c\.?\s?a\.?\s?2022|copyright act|of this act", " ", str(s), flags=re.I)
    return {m for m in re.findall(r"(?:s|sec|section)?\.?\s*(\d{1,3})", s) if 1<=int(m)<=109}

gold = {g["item_id"]: g.get("gold_provision","") for g in
        (json.loads(l) for l in Path("data/eval/gold_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}
m2 = {r["item_id"]: r["m2_verdict"] for r in
      (json.loads(l) for l in Path("results/A5_m2_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}
resp = [json.loads(l) for l in Path("runs/A5_responses_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]

CATS = ["single_hop","multi_hop","divergence","control","summarization"]
print(f"{'category':16}{'gold retrieved':>16}{'accuracy':>11}{'acc | gold present':>22}{'acc | gold absent':>20}")
print("-"*85)
for cat in CATS:
    items = [r for r in resp if r["category"]==cat and "retrieved" in r]
    if not items: continue
    got_gold, acc_present, n_present, acc_absent, n_absent, ok = 0,0,0,0,0,0
    for r in items:
        gs = gold_secs(gold.get(r["item_id"],""))
        retr = {c.lstrip("s").split("(")[0] for c in r["retrieved"]}
        present = bool(gs & retr)
        correct = m2.get(r["item_id"]) in ("correct","correct_section_coarse")
        got_gold += present
        ok += correct
        if present: n_present+=1; acc_present+=correct
        else: n_absent+=1; acc_absent+=correct
    n=len(items)
    ap = f"{100*acc_present/n_present:.0f}% (n={n_present})" if n_present else "-"
    aa = f"{100*acc_absent/n_absent:.0f}% (n={n_absent})" if n_absent else "-"
    print(f"{cat:16}{f'{got_gold}/{n} ({100*got_gold/n:.0f}%)':>16}{f'{100*ok/n:.0f}%':>11}{ap:>22}{aa:>20}")
