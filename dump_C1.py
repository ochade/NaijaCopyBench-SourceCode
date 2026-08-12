import json
from pathlib import Path
m = json.loads(Path("data/derived/section_map.json").read_text(encoding="utf-8"))

# Batch C1: Part VII - online content / takedown (your best divergence material)
for s in ["54","55","56","57","58","59","60","61","62"]:
    print("="*72)
    print(f"s.{s}: {m[s]['title']}  (page {m[s].get('page')})")
    print("-"*72)
    print(m[s]["text"])
    print()
