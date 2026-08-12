from pathlib import Path
p = Path("src/build_catE.py")
t = p.read_text(encoding="utf-8")
before = t

old = '''# lawyer sheet: ENTITY probes only - the rest are decidable from section_map
lawyer_items = [(i,q) for i,q,t,w,nl in ITEMS if nl]
with open("docs/catE_annotation_sheet.csv", "w", newline="", encoding="utf-8-sig") as f:
    w_ = csv.writer(f)
    w_.writerow(["item_id","question","does_this_body_or_instrument_exist","if_not_what_is_correct","confidence","notes"])
    for i,q in lawyer_items:
        w_.writerow([i,q,"","","",""])'''

new = '''# lawyer sheet: ALL 35 items
with open("docs/catE_annotation_sheet.csv", "w", newline="", encoding="utf-8-sig") as f:
    w_ = csv.writer(f)
    w_.writerow(["item_id","question","does_the_cited_provision_or_body_exist",
                 "correct_position","confidence","notes"])
    for i,q,t,w,nl in ITEMS:
        w_.writerow([i,q,"","","",""])'''

t = t.replace(old, new)
t = t.replace('print(f"decidable from section_map (no lawyer): {sum(1 for *_,nl in ITEMS if not nl)}")',
              'print(f"structural (also decidable from section_map): {sum(1 for *_,nl in ITEMS if not nl)}")')
t = t.replace('print(f"need lawyer (entity/instrument):        {sum(1 for *_,nl in ITEMS if nl)}")',
              'print(f"entity/instrument (lawyer knowledge essential): {sum(1 for *_,nl in ITEMS if nl)}")')
t = t.replace('print("to lawyers -> docs/catE_annotation_sheet.csv  (entity probes only)")',
              'print("to lawyers -> docs/catE_annotation_sheet.csv  (ALL 35)")')

p.write_text(t, encoding="utf-8")
print("changed:", t != before)
