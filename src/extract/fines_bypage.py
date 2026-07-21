import re, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
m = json.loads((ROOT/"data/derived/section_map.json").read_text(encoding="utf-8"))
secs = {int(k): v for k, v in m.items() if k != "SCHEDULE"}

DUR  = re.compile(r"\b(\d+)\s+years?\b")
FINE = re.compile(r"N[\d,]{3,}")

# first occurrence of each distinct fine value, with section + page
seen = {}
for n, s in sorted(secs.items()):
    for val in FINE.findall(s["text"]):
        if val not in seen:
            seen[val] = (n, s.get("page"))

print("=== DISTINCT FINES — verify each ONCE on the listed page ===")
for val, (n, pg) in sorted(seen.items(), key=lambda x: len(x[0])):
    # pull context
    t = secs[n]["text"]
    mm = re.search(re.escape(val), t)
    ctx = t[max(0,mm.start()-40):mm.end()+15].replace("\n"," ")
    print(f"  {val:12} -> s.{n}, PDF page {pg}   ...{ctx.strip()}")

print("\n=== group by page (open each page once) ===")
from collections import defaultdict
bypage = defaultdict(list)
for val,(n,pg) in seen.items():
    bypage[pg].append(f"{val}(s.{n})")
for pg in sorted(bypage):
    print(f"  page {pg}: {', '.join(bypage[pg])}")
