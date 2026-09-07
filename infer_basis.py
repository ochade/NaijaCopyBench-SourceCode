import re
from pathlib import Path
from openpyxl import load_workbook
from collections import Counter

p = Path.home() / "Downloads" / "catA_adjudication_sheet.xlsx"
ws = load_workbook(p, data_only=True).active
hdr = [c.value for c in ws[1]]
i = {h: n for n, h in enumerate(hdr) if h}

def secs(s):
    if not s: return frozenset()
    s = re.sub(r"c\.?\s?a\.?\s?2022|copyright act|of this act", "", str(s).lower())
    return frozenset(int(m) for m in re.findall(r"(?:s|sec|section)?\.?\s*(\d{1,3})", s)
                     if 1 <= int(m) <= 109)

rows = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[0]]
out = []
for r in rows:
    e = secs(r[i["Euchay_provision"]])
    l = secs(r[i["Eloho_provision"]])
    f = secs(r[i["FINAL_provision_ Sammy"]])
    if f == e == l:      basis = "BOTH CORRECT"
    elif f == e:         basis = "EUCHAY CORRECT"
    elif f == l:         basis = "ELOHO CORRECT"
    elif f & (e | l):    basis = "PARTIAL - drew on both"
    else:                basis = "NEITHER - own answer"
    out.append((r[0], basis, sorted(e), sorted(l), sorted(f)))

print("gold-answer provenance, Category A\n")
for k, v in Counter(b for _, b, *_ in out).most_common():
    print(f"  {k:26} {v}")

print("\nitems where the adjudicator departed from both annotators:")
n = 0
for iid, b, e, l, f in out:
    if b == "NEITHER - own answer":
        n += 1
        print(f"  {iid}  Euchay {e}  Eloho {l}  ->  FINAL {f}")
if n == 0:
    print("  none")
