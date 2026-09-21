from pathlib import Path
p = Path("make_adjudication_sheet.py")
t = p.read_text(encoding="utf-8")

t = t.replace(
'A_NAME, B_NAME = "Euchay", "Eloho"',
'''import sys
CAT = sys.argv[1] if len(sys.argv) > 1 else "A"
A_NAME, B_NAME = "Euchay", "Eloho"''')

t = t.replace('A = load(f"catA_annotation_sheet_{A_NAME}.xlsx")',
              'A = load(f"cat{CAT}_annotation_sheet_{A_NAME}.xlsx")')
t = t.replace('B = load(f"catA_annotation_sheet_{B_NAME}.xlsx")',
              'B = load(f"cat{CAT}_annotation_sheet_{B_NAME}.xlsx")')
t = t.replace('ws.title = "catA_adjudication"', 'ws.title = f"cat{CAT}_adjudication"')
t = t.replace('OUT = DL / "catA_adjudication_sheet.xlsx"',
              'OUT = DL / f"cat{CAT}_adjudication_sheet.xlsx"')

p.write_text(t, encoding="utf-8")
print("patched: takes category argument")
