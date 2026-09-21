from pathlib import Path
p = Path("make_review_sheet.py")
t = p.read_text(encoding="utf-8")

old = '''rows = []
for r in ws_in.iter_rows(min_row=2, values_only=True):
    rec = {k: (str(v).strip() if v is not None else "") for k, v in zip(hdr, r)}
    if not rec.get("item_id"): continue
    conf = rec.get("confidence","")
    flag = ("LOW CONFIDENCE" if "low" in conf.lower()
            else "NOTES FLAGGED" if rec.get("notes","").strip()
            else "")
    rows.append([rec["item_id"], NOTES.get(CAT,""), flag, rec.get("question",""),
                 rec.get("governing_provision",""), rec.get("answer",""),
                 conf, rec.get("notes",""),
                 "", "", "", "", ""])'''

new = '''# per-category column mapping: (label_for_col5, source_key, label_for_col6, source_key)
COLMAP = {
 "C": ("provision","governing_provision","answer","answer"),
 "D": ("provision","governing_provision","answer","answer"),
 "E": ("exists?","does_the_cited_provision_or_body_exist","correct_position","correct_position"),
 "F": ("provisions","governing_provisions","required_elements","required_elements_any_correct_summary_must_contain"),
}
L5, K5, L6, K6 = COLMAP.get(CAT, ("provision","governing_provision","answer","answer"))

rows = []
for r in ws_in.iter_rows(min_row=2, values_only=True):
    rec = {k: (str(v).strip() if v is not None else "") for k, v in zip(hdr, r)}
    if not rec.get("item_id"): continue
    conf = rec.get("confidence","")
    extra = rec.get("common_errors_that_would_be_wrong","") if CAT == "F" else ""
    flag = ("LOW CONFIDENCE" if "low" in conf.lower()
            else "NOTES FLAGGED" if rec.get("notes","").strip()
            else "")
    rows.append([rec["item_id"], NOTES.get(CAT,""), flag, rec.get("question",""),
                 rec.get(K5,""), rec.get(K6,""), extra,
                 conf, rec.get("notes",""),
                 "", "", "", "", ""])'''
t = t.replace(old, new)

t = t.replace(
'''HDR = ["item_id","category_note","flag","question",
       f"{ANNOT}_provision", f"{ANNOT}_answer", f"{ANNOT}_confidence", f"{ANNOT}_notes",
       "AGREE?","FINAL_provision","FINAL_answer","reasoning","question_verdict"]''',
'''HDR = ["item_id","category_note","flag","question",
       f"{ANNOT}_{L5}", f"{ANNOT}_{L6}",
       (f"{ANNOT}_common_errors" if CAT == "F" else ""),
       f"{ANNOT}_confidence", f"{ANNOT}_notes",
       "AGREE?","FINAL_provision","FINAL_answer","reasoning","question_verdict"]''')

t = t.replace('for col in (2,4,6,8,11,12):', 'for col in (2,4,6,7,9,12,13):')
t = t.replace(
'''for col, w in {"A":13,"B":38,"C":16,"D":48,"E":18,"F":50,"G":11,"H":34,
               "I":10,"J":18,"K":50,"L":40,"M":18}.items():''',
'''for col, w in {"A":13,"B":38,"C":16,"D":46,"E":20,"F":48,"G":40,"H":11,
               "I":32,"J":10,"K":18,"L":48,"M":38,"N":18}.items():''')

p.write_text(t, encoding="utf-8")
print("patched: per-category column map")
