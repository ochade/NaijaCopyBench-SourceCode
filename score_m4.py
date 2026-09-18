import json
from pathlib import Path
from openpyxl import load_workbook
from collections import defaultdict

p = Path.home()/"Downloads"/"m4_verification.xlsx"
ws = load_workbook(p, data_only=True).active
hdr = [c.value for c in ws[1]]
i = {h: n for n, h in enumerate(hdr) if h}
vcol = [h for h in hdr if h and "verdict" in str(h).lower()][0]

# carry arm/item down the merged-looking rows (only first claim row is labelled fully)
rows = []
cur_arm = cur_item = cur_cat = None
for r in ws.iter_rows(min_row=2, values_only=True):
    if r[i["row_id"]] is None: continue
    if r[i["arm"]]:  cur_arm  = r[i["arm"]]
    if r[i["item_id"]]: cur_item = r[i["item_id"]]
    if r[i["category"]]: cur_cat = r[i["category"]]
    v = str(r[i[vcol]] or "").strip().upper()
    rows.append({"arm": cur_arm, "item": cur_item, "cat": cur_cat, "verdict": v})

# validate
bad = [x for x in rows if x["verdict"] not in ("S","N","C")]
print(f"{len(rows)} claims total")
if bad:
    print(f"WARNING: {len(bad)} claims have no S/N/C verdict:")
    seen=set()
    for x in bad[:10]:
        if x["item"] not in seen: print("  ", x["arm"], x["item"]); seen.add(x["item"])

# precision per arm: supported / (supported + not-supported + contradicted)
print(f"\n{'arm':6}{'claims':>8}{'supported':>11}{'not-supp':>10}{'contra':>8}{'precision':>11}")
print("-"*54)
for arm in ["A1","A3","A5"]:
    a = [x for x in rows if x["arm"]==arm]
    s = sum(1 for x in a if x["verdict"]=="S")
    n = sum(1 for x in a if x["verdict"]=="N")
    c = sum(1 for x in a if x["verdict"]=="C")
    tot = s+n+c
    print(f"{arm:6}{tot:>8}{s:>11}{n:>10}{c:>8}{100*s/tot:>10.1f}%" if tot else f"{arm}: no verdicts")

# contradiction rate = how often the model asserts something the Act rules out
print(f"\ncontradiction rate (claims that CONTRADICT the Act, per arm)")
for arm in ["A1","A3","A5"]:
    a = [x for x in rows if x["arm"]==arm]
    c = sum(1 for x in a if x["verdict"]=="C")
    print(f"  {arm}: {c}/{len(a)}  ({100*c/len(a):.1f}%)")

# by category, precision
print(f"\nprecision by category")
print(f"{'category':16}" + "".join(f"{a:>10}" for a in ['A1','A3','A5']))
print("-"*46)
for cat in ["single_hop","divergence","summarization"]:
    row=f"{cat:16}"
    for arm in ["A1","A3","A5"]:
        a=[x for x in rows if x["arm"]==arm and x["cat"]==cat]
        s=sum(1 for x in a if x["verdict"]=="S")
        row += f"{(100*s/len(a) if a else 0):>9.1f}%"
    print(row)

Path("results/m4_scored.json").write_text(json.dumps({
    "n_claims": len(rows),
    "by_arm": {arm: {v: sum(1 for x in rows if x["arm"]==arm and x["verdict"]==v)
                     for v in ("S","N","C")} for arm in ["A1","A3","A5"]}}, indent=2))
print("\nwrote results/m4_scored.json")
