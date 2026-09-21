"""Assemble the gold set for all 180 items from six source files.

Provenance differs by category:
  A, B  adjudicated (two annotators, resolved by a third practitioner)
  C, E  reviewed (one annotator, confirmed or corrected by a second practitioner)
  D, F  single annotator, no review
"""
import json, re
from pathlib import Path
from openpyxl import load_workbook
from collections import Counter

DL = Path.home() / "Downloads"

def rows_of(fn):
    ws = load_workbook(DL / fn, data_only=True).active
    hdr = [c.value for c in ws[1]]
    if hdr and hdr[0] in (None, ""): hdr[0] = "item_id"
    out = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        rec = {h: v for h, v in zip(hdr, r) if h}
        if rec.get("item_id"): out.append(rec)
    return out

def s(v):
    return str(v).strip() if v is not None else ""

gold = []

# ---- A: adjudicated, columns suffixed _Sammy ----
for r in rows_of("catA_adjudication_sheet.xlsx"):
    gold.append({"item_id": s(r["item_id"]), "category": "single_hop",
                 "gold_provision": s(r.get("FINAL_provision_ Sammy")),
                 "gold_answer": s(r.get("Euchay_answer")),
                 "provenance": "adjudicated",
                 "adjudicator_verdict": s(r.get("FINAL_answer_Sammy")),
                 "adjudicator_reasoning": s(r.get("reasoning_Sammy"))})

# ---- B: adjudicated, plain column names ----
for r in rows_of("catB_adjudication_sheet (1).xlsx"):
    gold.append({"item_id": s(r["item_id"]), "category": "multi_hop",
                 "gold_provision": s(r.get("FINAL_provision")),
                 "gold_answer": s(r.get("FINAL_answer")) or s(r.get("Euchay_answer")),
                 "provenance": "adjudicated",
                 "adjudicator_reasoning": s(r.get("basis_of_resolution"))})

# ---- C and E: reviewed. FINAL_provision wins if filled; else AGREE -> annotator ----
def reviewed(fn, cat, ann_prov, ann_ans):
    out = []
    for r in rows_of(fn):
        fin_p, fin_a = s(r.get("FINAL_provision")), s(r.get("FINAL_answer"))
        agree = s(r.get("AGREE?")).upper()
        if fin_p:
            prov, src = fin_p, "reviewer_corrected"
        elif "AGREE" in agree:
            prov, src = s(r.get(ann_prov)), "reviewer_confirmed"
        else:
            prov, src = s(r.get(ann_prov)), "annotator_unreviewed"
        out.append({"item_id": s(r["item_id"]), "category": cat,
                    "gold_provision": prov,
                    "gold_answer": fin_a or s(r.get(ann_ans)),
                    "provenance": src,
                    "agree_marker": agree,
                    "adjudicator_reasoning": s(r.get("reasoning"))})
    return out

gold += reviewed("catC_review_sheet.xlsx", "divergence",
                 "Euchay_provision", "Euchay_answer")
gold += reviewed("catE_review_sheet.xlsx", "fabrication",
                 "Euchay_correct_position", "Euchay_correct_position")

# ---- D and F: single annotator ----
for r in rows_of("catD_annotation_sheet_Euchay.xlsx"):
    gold.append({"item_id": s(r["item_id"]), "category": "control",
                 "gold_provision": s(r.get("governing_provision")),
                 "gold_answer": s(r.get("answer")),
                 "provenance": "single_annotator"})

for r in rows_of("catF_annotation_sheet_Euchay.xlsx"):
    gold.append({"item_id": s(r["item_id"]), "category": "summarization",
                 "gold_provision": s(r.get("governing_provisions")),
                 "gold_answer": s(r.get("required_elements_any_correct_summary_must_contain")),
                 "prohibited_claims": s(r.get("common_errors_that_would_be_wrong")),
                 "provenance": "single_annotator"})

Path("data/eval").mkdir(parents=True, exist_ok=True)
Path("data/eval/gold_180.jsonl").write_text(
    "\n".join(json.dumps(g, ensure_ascii=False) for g in gold) + "\n", encoding="utf-8")

print(f"assembled {len(gold)} gold records")
print("by category :", dict(Counter(g["category"] for g in gold)))
print("by provenance:", dict(Counter(g["provenance"] for g in gold)))
missing = [g["item_id"] for g in gold if not g["gold_provision"]]
print(f"missing provision: {len(missing)}", missing[:10] if missing else "")

bench = {json.loads(l)["item_id"] for l in Path("data/eval/benchmark_180.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
got = {g["item_id"] for g in gold}
print("in benchmark but no gold:", sorted(bench - got)[:10] or "none")
print("gold but not in benchmark:", sorted(got - bench)[:10] or "none")
