import re, sys
from pathlib import Path
from openpyxl import load_workbook
from collections import Counter

DL = Path.home() / "Downloads"
A_NAME, B_NAME = "Euchay", "Eloho"

def load(fn):
    ws = load_workbook(DL / fn, data_only=True).active
    hdr = [c.value for c in ws[1]]
    if hdr and hdr[0] in (None, ""): hdr[0] = "item_id"
    out = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        rec = dict(zip(hdr, row))
        iid = str(rec.get("item_id") or "").strip()
        if iid: out[iid] = {k: (str(v).strip() if v is not None else "") for k, v in rec.items()}
    return out

def sections(s):
    """Set of section numbers cited. 'S.7 , S.19(1)(b)' -> {7,19}"""
    if not s: return frozenset()
    s = re.sub(r"c\.?\s?a\.?\s?2022|copyright act|of this act", "", s.lower())
    return frozenset(int(m) for m in re.findall(r"(?:s|sec|section)?\.?\s*(\d{1,3})", s)
                     if 1 <= int(m) <= 109)

def full(s):
    """Normalised full citation: section + subsection + paragraph, order-insensitive.
    'sec 19(1c)' and 'S.19(1)(c)' both -> ('19','1','c')"""
    if not s: return frozenset()
    s = re.sub(r"c\.?\s?a\.?\s?2022|copyright act|of this act", "", s.lower())
    out = set()
    for m in re.finditer(r"(\d{1,3})\s*\(?\s*(\d{0,2})\s*([a-z]?)\s*\)?(?:\s*\(\s*([a-z])\s*\))?", s):
        sec, sub, p1, p2 = m.group(1), m.group(2), m.group(3), m.group(4)
        if not sec or int(sec) > 109: continue
        out.add((sec, sub or "", (p2 or p1 or "")))
    return frozenset(out)

def kappa(pairs):
    """Cohen's kappa on binary agree/disagree is degenerate; compute on the
    categorical label = the normalised citation itself."""
    n = len(pairs)
    if n == 0: return None
    po = sum(1 for a, b in pairs if a == b) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum((ca[k]/n) * (cb.get(k, 0)/n) for k in ca)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0, po

for CAT in ["A", "B"]:
    try:
        A = load(f"cat{CAT}_annotation_sheet_{A_NAME}.xlsx")
        B = load(f"cat{CAT}_annotation_sheet_{B_NAME}.xlsx")
    except FileNotFoundError as e:
        print(f"cat{CAT}: {e}"); continue
    ids = sorted(set(A) & set(B))

    raw   = [(A[i]["governing_provision"], B[i]["governing_provision"]) for i in ids]
    norm  = [(full(a), full(b)) for a, b in raw]
    setwise = [(sections(a), sections(b)) for a, b in raw]

    print(f"\n=== Category {CAT}  (n={len(ids)}) ===")
    for label, pairs in [("raw string", raw), ("normalised citation", norm),
                         ("section set", setwise)]:
        k, po = kappa(pairs)
        print(f"  {label:22} agreement {po:.3f}   kappa {k:.3f}")

    # containment: one recorded the chain, the other the destination
    contained = sum(1 for a, b in setwise if a != b and (a <= b or b <= a))
    disjoint  = sum(1 for a, b in setwise if a and b and not (a & b))
    print(f"  chain-vs-destination (one set contains the other): {contained}")
    print(f"  no shared section at all:                          {disjoint}")
