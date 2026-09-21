import json, sys
from pathlib import Path
from collections import Counter
sys.path.insert(0, "src/score")
from metrics_citation import m1_citation_validity
from parse_gold import parse_gold

def cited_pairs(text):
    out = set()
    for d in m1_citation_validity(text or "")["detail"]:
        sec = str(d.get("section",""))
        if sec.isdigit() and int(sec) <= 109:
            out.add((sec, str(d.get("subsection") or "")))
    return out

def score(response, gold_str):
    g = parse_gold(gold_str)
    if not g: return "n/a_no_gold"
    c = cited_pairs(response)
    if not c: return "no_citation"
    if c & g: return "correct"
    if {s for s,_ in c} & {s for s,_ in g}: return "correct_section_coarse"
    return "wrong_but_real"

gold = {g["item_id"]: g.get("gold_provision","") for g in
        (json.loads(l) for l in Path("data/eval/gold_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}
CATS = ["single_hop","multi_hop","divergence","control","summarization"]   # fabrication excluded

summary = {}
for arm in ["A1","A2","A3","A5"]:
    resp = [json.loads(l) for l in Path(f"runs/{arm}_responses_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    scored = [{**r, "gold_provision": gold.get(r["item_id"],""),
               "m2_verdict": score(r["response"], gold.get(r["item_id"],""))} for r in resp]
    Path(f"results/{arm}_m2_180.jsonl").write_text(
        "\n".join(json.dumps(s, ensure_ascii=False) for s in scored)+"\n", encoding="utf-8")
    summary[arm] = scored

print("Category E (fabrication) excluded: those items have no governing provision.\n")
print(f"{'arm':6}{'n':>5}{'correct':>10}{'coarse':>9}{'wrong':>8}{'no_cite':>9}{'accuracy':>10}")
print("-"*57)
for arm, sc in summary.items():
    sub = [s for s in sc if s["category"] != "fabrication"]
    v = Counter(s["m2_verdict"] for s in sub)
    ok = v.get("correct",0)+v.get("correct_section_coarse",0)
    print(f"{arm:6}{len(sub):>5}{v.get('correct',0):>10}{v.get('correct_section_coarse',0):>9}"
          f"{v.get('wrong_but_real',0):>8}{v.get('no_citation',0):>9}{100*ok/len(sub):>9.1f}%")

print("\nby category")
print(f"{'category':16}" + "".join(f"{a:>10}" for a in summary))
print("-"*46)
for cat in CATS:
    row = f"{cat:16}"
    for arm, sc in summary.items():
        sub = [s for s in sc if s["category"] == cat]
        ok = sum(1 for s in sub if s["m2_verdict"] in ("correct","correct_section_coarse"))
        row += f"{(100*ok/len(sub) if sub else 0):>9.1f}%"
    print(row)
