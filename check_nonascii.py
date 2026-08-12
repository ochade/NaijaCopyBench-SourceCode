import json, collections
from pathlib import Path
m = json.loads(Path("data/derived/section_map.json").read_text(encoding="utf-8"))
txt = "".join(v["text"] for k,v in m.items() if k!="SCHEDULE")
c = collections.Counter(ch for ch in txt if ord(ch) > 127)
print("non-ASCII in section_map:")
for ch, n in c.most_common():
    print(f"  U+{ord(ch):04X} {ch!r}: {n}")
