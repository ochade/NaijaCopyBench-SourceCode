import re, random
from pathlib import Path
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from collections import Counter

DL = Path.home() / "Downloads"
import sys
CAT = sys.argv[1] if len(sys.argv) > 1 else "A"
A_NAME, B_NAME = "Euchay", "Eloho"

def load(fn):
    ws = load_workbook(DL / fn, data_only=True).active
    hdr = [c.value for c in ws[1]]
    out = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        rec = dict(zip(hdr, row))
        iid = (rec.get("item_id") or "").strip() if rec.get("item_id") else ""
        if iid:
            out[iid] = {k: (str(v).strip() if v is not None else "") for k, v in rec.items()}
    return out

A = load(f"cat{CAT}_annotation_sheet_{A_NAME}.xlsx")
B = load(f"cat{CAT}_annotation_sheet_{B_NAME}.xlsx")
ids = sorted(set(A) | set(B))

def sections(s):
    """Extract the set of SECTION numbers from a citation string.
    'S.7 , S.19(1)(b)' -> {7,19};  'sec 19(1b)' -> {19}"""
    if not s: return set()
    s = re.sub(r"c\.?\s?a\.?\s?2022|copyright act|of this act", "", s.lower())
    return {int(m) for m in re.findall(r"(?:s|sec|section)?\.?\s*(\d{1,3})", s) if int(m) <= 109}

def primary(s):
    """First section cited - treated as the primary provision."""
    ss = re.sub(r"c\.?\s?a\.?\s?2022|copyright act|of this act", "", (s or "").lower())
    m = re.search(r"(?:s|sec|section)?\.?\s*(\d{1,3})", ss)
    return int(m.group(1)) if m and int(m.group(1)) <= 109 else None

def compare(pa, pb):
    """Returns one of: SAME, SUBSET (one recorded the chain, one the destination),
    PARTIAL (overlap but each has provisions the other lacks), DIFFERENT."""
    A_, B_ = sections(pa), sections(pb)
    if not A_ or not B_: return "MISSING"
    if A_ == B_: return "SAME"
    if A_ <= B_ or B_ <= A_: return "SUBSET"
    if A_ & B_: return "PARTIAL"
    return "DIFFERENT"

random.seed(42)
rows = []
for iid in ids:
    a, b = A.get(iid, {}), B.get(iid, {})
    pa, pb = a.get("governing_provision",""), b.get("governing_provision","")
    ca, cb = a.get("confidence",""), b.get("confidence","")
    cmp = compare(pa, pb)
    same_primary = primary(pa) is not None and primary(pa) == primary(pb)
    low = "low" in (ca + cb).lower()
    notes = bool(a.get("notes","").strip() or b.get("notes","").strip())

    if cmp == "DIFFERENT":
        reason = "PROVISION DISAGREEMENT"
    elif cmp == "PARTIAL":
        reason = "PARTIAL OVERLAP"
    elif cmp == "SUBSET":
        reason = "CHAIN vs DESTINATION" if same_primary else "PARTIAL OVERLAP"
    elif low:
        reason = "LOW CONFIDENCE"
    elif notes:
        reason = "NOTES FLAGGED"
    else:
        reason = "AGREED"
    rows.append([iid, reason, a.get("question") or b.get("question",""),
                 pa, a.get("answer",""), ca, a.get("notes",""),
                 pb, b.get("answer",""), cb, b.get("notes",""),
                 "", "", "", "", ""])

order = {"PROVISION DISAGREEMENT":0,"PARTIAL OVERLAP":1,"CHAIN vs DESTINATION":2,
         "LOW CONFIDENCE":3,"NOTES FLAGGED":4,"AGREED":5}
rows.sort(key=lambda r: (order[r[1]], r[0]))

HDR = ["item_id","review_reason","question",
       f"{A_NAME}_provision",f"{A_NAME}_answer",f"{A_NAME}_confidence",f"{A_NAME}_notes",
       f"{B_NAME}_provision",f"{B_NAME}_answer",f"{B_NAME}_confidence",f"{B_NAME}_notes",
       "FINAL_provision","FINAL_answer","basis_of_resolution","reasoning","question_verdict"]

wb = Workbook(); ws = wb.active; ws.title = f"cat{CAT}_adjudication"
ws.append(HDR)
for r in rows: ws.append(r)

hdr_fill = PatternFill("solid", fgColor="1F3864")
for c in ws[1]:
    c.font = Font(bold=True, color="FFFFFF"); c.fill = hdr_fill
    c.alignment = Alignment(wrap_text=True, vertical="center")

fills = {"PROVISION DISAGREEMENT":"FFC7CE","PARTIAL OVERLAP":"FCE4D6",
         "CHAIN vs DESTINATION":"FFF2CC","LOW CONFIDENCE":"FFEB9C",
         "NOTES FLAGGED":"DDEBF7"}
for i, r in enumerate(rows, start=2):
    if r[1] in fills:
        ws.cell(row=i, column=2).fill = PatternFill("solid", fgColor=fills[r[1]])
    for col in (3,5,7,9,11,13,15):
        ws.cell(row=i, column=col).alignment = Alignment(wrap_text=True, vertical="top")

widths = {"A":13,"B":24,"C":46,"D":18,"E":46,"F":11,"G":32,
          "H":18,"I":46,"J":11,"K":32,"L":18,"M":46,"N":22,"O":40,"P":18}
for col, w in widths.items(): ws.column_dimensions[col].width = w
ws.freeze_panes = "C2"

OUT = DL / f"cat{CAT}_adjudication_sheet.xlsx"
wb.save(OUT)

c = Counter(r[1] for r in rows)
print("wrote", OUT)
print(f"{len(rows)} items")
for k in order:
    if c.get(k): print(f"  {k}: {c[k]}")
print(f"\nALL {len(rows)} items sent for review; disagreements sorted to the top.")
