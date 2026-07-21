import re, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAP = ROOT / "data/derived/section_map.json"
WL  = ROOT / "data/derived/arrangement_titles.json"

m = json.loads(MAP.read_text(encoding="utf-8"))
titles = json.loads(WL.read_text(encoding="utf-8"))

def norm(s):
    return re.sub(r"[^a-z]", "", s.lower())   # keep only letters -> maximal tolerance

title_norms = {norm(v) for v in titles.values()}

def strip_marginalia(text):
    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        s = lines[i].strip()
        if 0 < len(s) <= 30 and not re.match(r"^\(?[a-z0-9ivx]+\)|^\d{1,3}\.", s):
            j, buf, done = i, "", False
            while j < len(lines) and (j - i) < 14:
                buf += lines[j]
                nb = norm(buf)
                if nb in title_norms:            # full title matched -> drop run
                    i = j + 1; done = True; break
                if nb and not any(t.startswith(nb) for t in title_norms):
                    out.append(lines[i]); i += 1; done = True; break   # not furniture
                j += 1
            if not done:
                out.append(lines[i]); i += 1
        else:
            out.append(lines[i]); i += 1
    return "\n".join(out).strip()

changed = 0
for k, v in m.items():
    if k == "SCHEDULE" or "text" not in v:
        continue
    new = strip_marginalia(v["text"])
    if new != v["text"]:
        changed += 1
        v["text"] = new
        v["n_chars"] = len(new)

MAP.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"sections cleaned: {changed}")
print("VERSION: marginalia-cleaner-standalone")
