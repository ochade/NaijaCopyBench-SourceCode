import json
from pathlib import Path

m = json.loads(Path("data/derived/section_map.json").read_text(encoding="utf-8"))
secs = [k for k in m if k != "SCHEDULE"]

print("total sections:", len(secs))
nums = sorted(int(k) for k in secs)
print("range:", nums[0], "-", nums[-1])
print("missing 1..109:", sorted(set(range(1,110)) - set(nums)))

print("\n--- s.19 record ---")
s = m["19"]
for f in ["number","title","subsections","paragraph_letters","page","n_chars"]:
    print(f"  {f}: {s.get(f)}")
print("  has text:", bool(s.get("text")))

print("\n--- FIELD COMPLETENESS across 109 ---")
for f in ["title","subsections","paragraph_letters","page","n_chars","text"]:
    filled = sum(1 for k in secs if m[k].get(f) not in (None, "", []))
    print(f"  {f}: {filled}/109")

print("\n--- sections with NO subsections (bare provisions) ---")
bare = [k for k in secs if not m[k].get("subsections")]
print(f"  count: {len(bare)}  e.g. {bare[:8]}")
