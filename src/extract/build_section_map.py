import re, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLEAN = ROOT / "data/act/clean/act_clean.txt"
WHITELIST = ROOT / "data/derived/arrangement_titles.json"
OUT = ROOT / "data/derived/section_map.json"

text = CLEAN.read_text(encoding="utf-8")
lines = text.split("\n")
titles = json.loads(WHITELIST.read_text(encoding="utf-8"))
titles = {int(k): v.strip().rstrip(".") for k, v in titles.items()}

body_start = next(i for i, l in enumerate(lines)
                  if re.match(r"^1\.\s+The objectives of this Act", l))
sched_start = next(i for i, l in enumerate(lines)
                   if re.match(r"^SCHEDULE\s+Section", l))
print(f"body: L{body_start}..L{sched_start-1}, schedule at L{sched_start}")

HDR = re.compile(r"^(\d{1,3})\.(?:\u2014|\s)")
heads = []
for i in range(body_start, sched_start):
    m = HDR.match(lines[i])
    if m:
        n = int(m.group(1))
        if 1 <= n <= 109:
            heads.append((i, n))

seen, ordered = set(), []
for i, n in heads:
    if n not in seen and (not ordered or n == ordered[-1][1] + 1):
        ordered.append((i, n)); seen.add(n)
print(f"section headers located: {len(ordered)} (expect 109)")

def norm(s):
    # lowercase, drop hyphens and all whitespace -> tolerant matching
    return re.sub(r"[-\s]+", "", s.lower())

title_norms = {norm(t) for t in titles.values()}

def strip_marginalia(block_lines):
    out, i = [], 0
    while i < len(block_lines):
        s = block_lines[i].strip()
        if 0 < len(s) <= 30 and not re.match(r"^\(?[a-z0-9ivx]+\)|^\d{1,3}\.", s):
            j, buf, matched = i, "", False
            while j < len(block_lines) and (j - i) < 12:
                buf += block_lines[j]
                nb = norm(buf)
                if nb in title_norms:
                    i = j + 1; matched = True; break
                if not any(t.startswith(nb) for t in title_norms):
                    out.append(block_lines[i]); i += 1; matched = True; break
                j += 1
            if not matched:
                out.append(block_lines[i]); i += 1
        else:
            out.append(block_lines[i]); i += 1
    return out

section_map = {}
bounds = [idx for idx, _ in ordered] + [sched_start]
for k, (idx, n) in enumerate(ordered):
    seg = lines[idx:bounds[k+1]]
    seg = strip_marginalia(seg)
    body = "\n".join(seg).strip()
    subs = set(re.findall(r"(?m)^\((\d{1,2})\)", body))
    if re.match(r"^\d{1,3}\.\u2014\(1\)", body):
        subs.add("1")
    subs = sorted(subs, key=int)
    para_letters = sorted(set(re.findall(r"(?m)^\(([a-z])\)", body)))
    section_map[str(n)] = {
        "number": n, "title": titles.get(n, "?"),
        "subsections": subs, "paragraph_letters": para_letters,
        "n_chars": len(body), "text": body,
    }

nums = sorted(int(k) for k in section_map)
print("\n=== VALIDATION ===")
print("sections:", len(nums), "missing:", sorted(set(range(1,110)) - set(nums)))
print("title mismatches:", [n for n in nums if section_map[str(n)]["title"] != titles.get(n)])
print("s.19 subs:", section_map["19"]["subsections"], "paras:", section_map["19"]["paragraph_letters"])
print("VERSION: fixed-v3-marginalia")

section_map["SCHEDULE"] = {"number": None, "title": "Schedule (re s.79(3))",
    "text": "\n".join(lines[sched_start:]).strip(), "flagged": True}

OUT.write_text(json.dumps(section_map, indent=2, ensure_ascii=False), encoding="utf-8")
print("wrote", OUT)
