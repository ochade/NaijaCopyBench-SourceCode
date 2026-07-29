import json
from pathlib import Path
m = json.loads(Path("data/derived/section_map.json").read_text(encoding="utf-8"))
gaps, stems = [], []
for k, v in m.items():
    if k == "SCHEDULE" or not v.get("subsections"):
        continue
    subs = sorted(int(s) for s in v["subsections"])
    # true gaps: missing numbers BETWEEN the lowest and highest observed
    missing = [n for n in range(subs[0], subs[-1] + 1) if n not in subs]
    if missing:
        gaps.append((k, v["title"][:35], v["subsections"], missing))
    if subs[0] != 1:
        stems.append((k, v["title"][:35], v["subsections"]))

print(f"TRUE gaps (missing between observed): {len(gaps)}")
for k, t, s, ms in gaps:
    print(f"  s.{k:>4} {t:37} {s} missing {ms}")
print()
print(f"UNNUMBERED-STEM sections (start above 1 - drafting pattern, not a bug): {len(stems)}")
for k, t, s in stems:
    print(f"  s.{k:>4} {t:37} {s}")
