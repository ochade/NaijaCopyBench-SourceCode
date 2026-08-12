import json
from pathlib import Path
m = json.loads(Path("data/derived/section_map.json").read_text(encoding="utf-8"))
for s in ["10","11","12","13","14","31","32","33","34"]:
    print("="*72)
    print(f"s.{s}: {m[s]['title']}  (page {m[s].get('page')})")
    print("-"*72)
    print(m[s]["text"][:900])
    print()
