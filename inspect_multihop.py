import json, sys
from pathlib import Path
sys.path.insert(0, "src/score")
from metrics_citation import m1_citation_validity
from parse_gold import parse_gold

def cited(text):
    return sorted({(str(d.get("section","")), str(d.get("subsection") or ""))
                   for d in m1_citation_validity(text or "")["detail"]
                   if str(d.get("section","")).isdigit()})

gold = {g["item_id"]: g.get("gold_provision","") for g in
        (json.loads(l) for l in Path("data/eval/gold_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}

arms = {}
for a in ["A1","A3","A5"]:
    arms[a] = {r["item_id"]: r for r in
               (json.loads(l) for l in Path(f"runs/{a}_responses_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}

mh = sorted(i for i in gold if i.startswith("NCB-B-"))
print(f"{'item':12} {'gold':<20} {'A1 cited':<22} {'A3 cited':<22} A5 cited")
print("-"*100)
for i in mh:
    g = sorted(parse_gold(gold[i]))
    gs = ",".join(f"{s}({b})" if b else s for s,b in g)[:19]
    row = f"{i:12} {gs:<20}"
    for a in ["A1","A3","A5"]:
        c = cited(arms[a][i]["response"])
        cs = ",".join(f"{s}({b})" if b else s for s,b in c)[:21]
        row += f" {cs:<22}"
    print(row)

print("\n--- A3 on the three items A1 got right ---")
for i in mh:
    g = set(parse_gold(gold[i]))
    a1 = set(cited(arms["A1"][i]["response"]))
    a3 = set(cited(arms["A3"][i]["response"]))
    a1_ok = bool({s for s,_ in a1} & {s for s,_ in g})
    a3_ok = bool({s for s,_ in a3} & {s for s,_ in g})
    if a1_ok and not a3_ok:
        print(f"\n{i}  gold={gold[i]!r}")
        print(f"  A3 response: {arms['A3'][i]['response'][:320]}")
