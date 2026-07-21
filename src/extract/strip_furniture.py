"""
Step 4 (Path B): Remove page furniture that is unambiguous and global.
  R1  running headers (68 lines, one per page)
  R3  s.109 furniture-prefixed header
Marginal-note removal deferred to Step 5 (per-section, whitelist-gated).
Reads:  data/act/raw/CopyrightAct2022.txt  (frozen)
Writes: data/act/clean/act_clean.txt
"""
import re, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW  = ROOT / "data/act/raw/CopyrightAct2022.txt"
OUT  = ROOT / "data/act/clean/act_clean.txt"
EXPECTED_SHA = "11a195164e989fe6a3ea745dd4ba5b7615aee4050213257768432d4c2f39d52e"

raw = RAW.read_text(encoding="utf-8")
sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
assert sha == EXPECTED_SHA, f"FREEZE VIOLATION: {sha} != {EXPECTED_SHA}"

lines = raw.split("\n")
n0 = len(lines)

HEADER = re.compile(r"(Copyright Act, 2022\s+2023 No\. 8\s+A ?\d{2,3}"
                    r"|A ?\d{2,3}\s+2023 No\. 8\s+Copyright Act, 2022)")
kept = [l for l in lines if not HEADER.search(l)]
n_removed = n0 - len(kept)
text_out = "\n".join(kept)

before = text_out.count("Citation. 109. This Act may be cited")
text_out = text_out.replace("Citation. 109. This Act may be cited",
                            "109. This Act may be cited")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(text_out, encoding="utf-8")

print(f"R1 removed {n_removed} header lines (expect ~68)")
print(f"R3 s.109 prefix fixed: {before} occurrence(s)")
d = len(raw) - len(text_out)
print(f"chars {len(raw):,} -> {len(text_out):,}  (removed {d:,}, {100*d/len(raw):.2f}%)")
for needle in ["70 years", "50 years"]:
    assert text_out.count(needle) > 0, f"LOST {needle}"
    print(f"'{needle}': {text_out.count(needle)} survive")
assert 0 < d < 6000, f"char delta {d} outside expected range"
print("OK -- wrote", OUT)
