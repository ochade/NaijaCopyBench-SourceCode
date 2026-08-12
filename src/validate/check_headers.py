import json, re
from pathlib import Path
m = json.loads(Path("data/derived/section_map.json").read_text(encoding="utf-8"))
mismatches = []
for k, v in m.items():
    if k == "SCHEDULE" or "text" not in v:
        continue
    first = v["text"].lstrip()
    mm = re.match(r"(\d{1,3})[.\u2014\s]", first)
    text_num = mm.group(1) if mm else "NONE"
    if text_num != str(v["number"]):
        mismatches.append((v["number"], text_num, first[:40]))
print(f"header-number mismatches: {len(mismatches)}")
for real, got, preview in mismatches:
    print(f"  s.{real}: text starts with {got!r} -> {preview!r}")
