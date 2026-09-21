from pathlib import Path
import re

p = Path("make_adjudication_sheet.py")
t = p.read_text(encoding="utf-8")

OLD = t[t.index("def prov_key"):t.index("random.seed(42)")]

NEW = '''def sections(s):
    """Extract the set of SECTION numbers from a citation string.
    'S.7 , S.19(1)(b)' -> {7,19};  'sec 19(1b)' -> {19}"""
    if not s: return set()
    s = re.sub(r"c\\.?\\s?a\\.?\\s?2022|copyright act|of this act", "", s.lower())
    return {int(m) for m in re.findall(r"(?:s|sec|section)?\\.?\\s*(\\d{1,3})", s) if int(m) <= 109}

def primary(s):
    """First section cited - treated as the primary provision."""
    ss = re.sub(r"c\\.?\\s?a\\.?\\s?2022|copyright act|of this act", "", (s or "").lower())
    m = re.search(r"(?:s|sec|section)?\\.?\\s*(\\d{1,3})", ss)
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

'''
t = t.replace(OLD, NEW)

# replace the classification block
old_cls = '''    match = prov_key(pa) == prov_key(pb) and pa != ""
    low = "low" in (ca + cb).lower()
    notes = bool(a.get("notes","").strip() or b.get("notes","").strip())

    reason = ("PROVISION DISAGREEMENT" if not match
              else "LOW CONFIDENCE" if low
              else "NOTES FLAGGED" if notes
              else "AGREED")'''
new_cls = '''    cmp = compare(pa, pb)
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
        reason = "AGREED"'''
t = t.replace(old_cls, new_cls)

t = t.replace(
'''order = {"PROVISION DISAGREEMENT":0,"LOW CONFIDENCE":1,"NOTES FLAGGED":2,
         "AGREED - SAMPLED CHECK":3,"AGREED":4}''',
'''order = {"PROVISION DISAGREEMENT":0,"PARTIAL OVERLAP":1,"CHAIN vs DESTINATION":2,
         "LOW CONFIDENCE":3,"NOTES FLAGGED":4,"AGREED":5}''')

t = t.replace(
'''fills = {"PROVISION DISAGREEMENT":"FFC7CE","LOW CONFIDENCE":"FFEB9C",
         "NOTES FLAGGED":"DDEBF7","AGREED - SAMPLED CHECK":"E2EFDA"}''',
'''fills = {"PROVISION DISAGREEMENT":"FFC7CE","PARTIAL OVERLAP":"FCE4D6",
         "CHAIN vs DESTINATION":"FFF2CC","LOW CONFIDENCE":"FFEB9C",
         "NOTES FLAGGED":"DDEBF7"}''')

p.write_text(t, encoding="utf-8")
print("patched: set-based comparison")
