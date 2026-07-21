import re, json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]
MAP = ROOT / "data/derived/section_map.json"
OUT = ROOT / "logs/numerals_checklist.md"

m = json.loads(MAP.read_text(encoding="utf-8"))
secs = {int(k): v for k, v in m.items() if k != "SCHEDULE"}

DUR  = re.compile(r"\b(\d+)\s+years?\b")
FINE = re.compile(r"N([\d,]{3,})")
TERM = re.compile(r"term of (?:at least|not less than)\s+(\w+)\s+(year|month|day)")

rows = []
for n, s in sorted(secs.items()):
    t, pg = s["text"], s.get("page", "?")
    for label, rx in [("DURATION", DUR), ("FINE", FINE), ("TERM", TERM)]:
        for mm in rx.finditer(t):
            val = mm.group(0)
            a = max(0, mm.start() - 30)
            b = min(len(t), mm.end() + 30)
            ctx = t[a:b].replace("\n", " ").strip()
            rows.append((label, n, pg, val, ctx))

lines = ["# Numerals gate checklist", "",
         "Verify each against the scan page in data/act/pages/Copyright-Act-2022.pdf.",
         "Tick [x] when confirmed; flag [!] + note if OCR differs from scan.", "",
         "| ok | type | s. | page | value | context |",
         "|----|------|----|------|-------|---------|"]
for label, n, pg, val, ctx in rows:
    lines.append(f"| [ ] | {label} | {n} | {pg} | {val} | ...{ctx}... |")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines), encoding="utf-8")

print("wrote", OUT)
print("total numerals:", len(rows))
print("by type:", dict(Counter(r[0] for r in rows)))
print("distinct fines:", sorted(set(r[3] for r in rows if r[0] == "FINE")))
print("distinct durations:", sorted(set(r[3] for r in rows if r[0] == "DURATION")))
