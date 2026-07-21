import re, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLEAN = ROOT / "data/act/clean/act_clean.txt"
MAP   = ROOT / "data/derived/section_map.json"

text = CLEAN.read_text(encoding="utf-8")
m = json.loads(MAP.read_text(encoding="utf-8"))
lines = text.split("\n")

PAGE = re.compile(r"=+ ?\[PAGE (\d+) of source scan\] ?=+")
HDR  = re.compile(r"^(\d{1,3})\.(?:\u2014|\s)")

# find BODY start — skip the Arrangement entirely
body_start = next(i for i, l in enumerate(lines)
                  if re.match(r"^1\.\s+The objectives of this Act", l))

# track page only from body_start onward; take FIRST body occurrence of each section
cur_page = None
section_page = {}
for i in range(len(lines)):
    pm = PAGE.match(lines[i].strip())
    if pm:
        cur_page = int(pm.group(1))
    if i < body_start:
        continue
    hm = HDR.match(lines[i])
    if hm:
        n = int(hm.group(1))
        if 1 <= n <= 109 and str(n) not in section_page:
            section_page[str(n)] = cur_page

def strip_pages(t):
    return "\n".join(x for x in t.split("\n") if not PAGE.match(x.strip())).strip()

tagged = 0
for k, v in m.items():
    if k == "SCHEDULE" or "text" not in v:
        continue
    if k in section_page:
        v["page"] = section_page[k]; tagged += 1
    v["text"] = strip_pages(v["text"])
    v["n_chars"] = len(v["text"])

MAP.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"sections tagged: {tagged} (expect 109)")
print(f"s.19 page: {m['19'].get('page')} (should be 13)")
print(f"s.1 page: {m['1'].get('page')}  s.109 page: {m['109'].get('page')}")
# sanity: page numbers should be non-decreasing across sections 1..109
pages = [m[str(n)].get('page') for n in range(1,110) if m[str(n)].get('page')]
monotonic = all(pages[i] <= pages[i+1] for i in range(len(pages)-1))
print(f"pages non-decreasing 1->109: {monotonic}")
print("VERSION: page-tagger-v2")
