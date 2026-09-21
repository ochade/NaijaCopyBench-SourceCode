import re, sys
from pathlib import Path
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from collections import Counter

DL = Path.home() / "Downloads"
CAT = "B"
A_NAME, B_NAME = "Euchay", "Eloho"

INTRO = (
 "CATEGORY B - MULTI-STEP (MULTI-HOP) QUESTIONS\n\n"
 "These questions cannot be answered from a single provision. They require a chain of "
 "reasoning: one provision identifies which rule applies, and a second supplies the rule "
 "itself. For example, a question about how long copyright lasts in a work produced by a "
 "government ministry requires first identifying the work as a government work under one "
 "section, then applying the duration rule for such works under another.\n\n"
 "WHY THE TWO ANNOTATORS OFTEN DIFFER HERE\n"
 "The two annotators adopted different recording conventions. One generally recorded the "
 "FULL CHAIN of provisions relied on; the other generally recorded only the DESTINATION "
 "provision that supplies the answer. Where this is the only difference, they agree on the "
 "law and differ only in what they wrote down. Those rows are marked PARTIAL OVERLAP.\n\n"
 "Rows marked NO OVERLAP are the ones where the annotators cited genuinely different "
 "provisions. These need your attention most.\n\n"
 "WHAT WE NEED FROM YOU\n"
 "For each row, complete the five columns on the right:\n"
 "  FINAL_provision      - the provision(s) you consider governing. For a multi-step "
 "question please list the full chain in the order used, and mark which is primary.\n"
 "  FINAL_answer         - a concise statement of the legal position, 2-4 sentences.\n"
 "  basis_of_resolution  - EUCHAY CORRECT / ELOHO CORRECT / BOTH PARTIALLY CORRECT / "
 "NEITHER CORRECT / BOTH CORRECT / GENUINELY UNSETTLED\n"
 "  reasoning            - why. One or two sentences. This is the most valuable field.\n"
 "  question_verdict     - SOUND / AMBIGUOUS / DEFECTIVE. Did the question itself cause "
 "the difficulty?\n\n"
 "Answer only from the Copyright Act 2022. Please do not use any AI assistant at any "
 "stage - this study measures AI accuracy against expert judgement.\n\n"
 "If the Act does not settle a point, mark GENUINELY UNSETTLED and record both readings. "
 "That is a permitted and useful outcome; please do not manufacture a resolution."
)

def load(fn):
    ws = load_workbook(DL / fn, data_only=True).active
    hdr = [c.value for c in ws[1]]
    out = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        rec = dict(zip(hdr, row))
        iid = str(rec.get("item_id") or "").strip()
        if iid:
            out[iid] = {k: (str(v).strip() if v is not None else "") for k, v in rec.items()}
    return out

A = load(f"cat{CAT}_annotation_sheet_{A_NAME}.xlsx")
B = load(f"cat{CAT}_annotation_sheet_{B_NAME}.xlsx")

def sections(s):
    """All section numbers cited, as a set. 'S.7 , S.19(1)(b)' -> {7,19}"""
    if not s: return set()
    s = re.sub(r"c\.?\s?a\.?\s?2022|copyright act|of this act", "", s.lower())
    return {int(n) for n in re.findall(r"(?:s(?:ec)?\.?\s*)?(\d{1,3})", s) if 1 <= int(n) <= 109}

rows = []
for iid in sorted(set(A) | set(B)):
    a, b = A.get(iid, {}), B.get(iid, {})
    pa, pb = a.get("governing_provision",""), b.get("governing_provision","")
    sa, sb = sections(pa), sections(pb)
    if sa and sa == sb:            reason = "SAME SECTIONS"
    elif sa & sb:                  reason = "PARTIAL OVERLAP"
    elif not sa or not sb:         reason = "MISSING ANSWER"
    else:                          reason = "NO OVERLAP"
    if reason in ("SAME SECTIONS","PARTIAL OVERLAP") and "low" in (a.get("confidence","")+b.get("confidence","")).lower():
        reason = "LOW CONFIDENCE"
    rows.append([iid, reason, a.get("question") or b.get("question",""),
                 pa, a.get("answer",""), a.get("confidence",""), a.get("notes",""),
                 pb, b.get("answer",""), b.get("confidence",""), b.get("notes",""),
                 "", "", "", "", ""])

order = {"NO OVERLAP":0,"MISSING ANSWER":1,"LOW CONFIDENCE":2,"PARTIAL OVERLAP":3,"SAME SECTIONS":4}
rows.sort(key=lambda r: (order[r[1]], r[0]))

HDR = ["item_id","review_reason","question",
       f"{A_NAME}_provision",f"{A_NAME}_answer",f"{A_NAME}_confidence",f"{A_NAME}_notes",
       f"{B_NAME}_provision",f"{B_NAME}_answer",f"{B_NAME}_confidence",f"{B_NAME}_notes",
       "FINAL_provision","FINAL_answer","basis_of_resolution","reasoning","question_verdict"]

wb = Workbook()

# --- sheet 1: instructions, one paragraph per row ---
intro_ws = wb.active
intro_ws.title = "READ FIRST"
intro_ws.column_dimensions["A"].width = 110
for n, para in enumerate(INTRO.split("\n\n"), start=1):
    cell = intro_ws.cell(row=n*2-1, column=1, value=para)
    cell.alignment = Alignment(wrap_text=True, vertical="top")
    lines = max(1, len(para) // 100 + para.count("\n") + 1)
    intro_ws.row_dimensions[n*2-1].height = 15 * lines + 6
    intro_ws.row_dimensions[n*2].height = 8
intro_ws.cell(row=1, column=1).font = Font(bold=True, size=13)

# --- sheet 2: the data ---
ws = wb.create_sheet(f"cat{CAT}_adjudication")
for col, h in enumerate(HDR, start=1):
    cell = ws.cell(row=1, column=col, value=h)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor="1F3864")
    cell.alignment = Alignment(wrap_text=True, vertical="center")

for r in rows:
    ws.append(r)

fills = {"NO OVERLAP":"FFC7CE","MISSING ANSWER":"F4B183",
         "LOW CONFIDENCE":"FFEB9C","PARTIAL OVERLAP":"DDEBF7"}
for i, r in enumerate(rows, start=2):
    if r[1] in fills:
        ws.cell(row=i, column=2).fill = PatternFill("solid", fgColor=fills[r[1]])
    for col in (3,5,7,9,11,13,15):
        ws.cell(row=i, column=col).alignment = Alignment(wrap_text=True, vertical="top")

widths = [13,20,46,20,46,11,30,20,46,11,30,20,46,24,40,18]
for n, w in enumerate(widths, start=1):
    ws.column_dimensions[get_column_letter(n)].width = w
ws.freeze_panes = "C2"

OUT = DL / f"cat{CAT}_adjudication_sheet.xlsx"
wb.save(OUT)

c2 = Counter(r[1] for r in rows)
print("wrote", OUT)
print(f"{len(rows)} items")
for k in order:
    if c2.get(k): print(f"  {k}: {c2[k]}")
