import json
from pathlib import Path
m = json.loads(Path("data/derived/section_map.json").read_text(encoding="utf-8"))
for s in ["21","22","23","24","25","26"]:
    print("="*72)
    print(f"s.{s}: {m[s]['title']}  (page {m[s].get('page')})")
    print("-"*72)
    print(m[s]["text"])
    print()
