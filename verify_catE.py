import json
from pathlib import Path
m = json.loads(Path("data/derived/section_map.json").read_text(encoding="utf-8"))
for s in ["19","4","103","88","74","61","36","9","2","3","54"]:
    r = m[s]
    print(f"s.{s:4} subs={r['subsections']}  paras={r['paragraph_letters']}")
