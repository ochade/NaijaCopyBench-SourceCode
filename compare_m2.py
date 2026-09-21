import json, sys
from pathlib import Path
sys.path.insert(0, "src/score")
from metrics_citation import m2_citation_accuracy, m1_citation_validity
from parse_gold import parse_gold

gold = {g["item_id"]: g.get("gold_provision","") for g in
        (json.loads(l) for l in Path("data/eval/gold_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}
resp = [json.loads(l) for l in Path("runs/A3_responses_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]

print("items where OLD said correct and NEW says wrong, or vice versa\n")
n = 0
for r in resp:
    if r["category"] == "fabrication": continue
    gp = gold.get(r["item_id"], "")
    old = m2_citation_accuracy(r["response"], [gp] if gp else [])["verdict"]
    cited = {(str(d.get("section","")), str(d.get("subsection") or ""))
             for d in m1_citation_validity(r["response"])["detail"]
             if str(d.get("section","")).isdigit()}
    gset = parse_gold(gp)
    new = ("correct" if cited & gset else
           "correct_section_coarse" if {s for s,_ in cited} & {s for s,_ in gset} else
           "wrong_but_real" if cited else "no_citation")
    old_ok = old in ("correct","correct_section_coarse")
    new_ok = new in ("correct","correct_section_coarse")
    if old_ok != new_ok:
        n += 1
        if n <= 8:
            print(f"{r['item_id']}  gold={gp[:26]!r}")
            print(f"   cited {sorted(cited)}   gold_parsed {sorted(gset)}")
            print(f"   old={old}  new={new}\n")
print(f"total disagreements: {n}")
