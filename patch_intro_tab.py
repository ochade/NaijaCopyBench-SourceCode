from pathlib import Path
p = Path("make_adjudication_B.py")
t = p.read_text(encoding="utf-8")

old = '''wb = Workbook(); ws = wb.active; ws.title = f"cat{CAT}_adjudication"

# --- intro block: merged across all columns, rows 1-2 ---
ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(HDR))
c = ws.cell(row=1, column=1, value=INTRO)
c.alignment = Alignment(wrap_text=True, vertical="top")
c.font = Font(size=11)
c.fill = PatternFill("solid", fgColor="FFF2CC")
ws.row_dimensions[1].height = 330
ws.row_dimensions[2].height = 8

# --- header row 3 ---
ws.append([]) if False else None
for col, h in enumerate(HDR, start=1):
    cell = ws.cell(row=3, column=col, value=h)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor="1F3864")
    cell.alignment = Alignment(wrap_text=True, vertical="center")

for r in rows:
    ws.append(r)'''

new = '''wb = Workbook()

# --- sheet 1: instructions, one paragraph per row ---
intro_ws = wb.active
intro_ws.title = "READ FIRST"
intro_ws.column_dimensions["A"].width = 110
for n, para in enumerate(INTRO.split("\\n\\n"), start=1):
    cell = intro_ws.cell(row=n*2-1, column=1, value=para)
    cell.alignment = Alignment(wrap_text=True, vertical="top")
    lines = max(1, len(para) // 100 + para.count("\\n") + 1)
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
    ws.append(r)'''

t = t.replace(old, new)
t = t.replace('for i, r in enumerate(rows, start=4):', 'for i, r in enumerate(rows, start=2):')
t = t.replace('ws.freeze_panes = "C4"', 'ws.freeze_panes = "C2"')
p.write_text(t, encoding="utf-8")
print("patched:", "READ FIRST" in t)
