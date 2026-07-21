"""
Step 4 (Path B): furniture removal + 0x02 control-byte repair.
  R1  running headers (68)
  R3  s.109 prefix
  R4  0x02 repair: soft-hyphen line-splits joined; compound hyphens restored (E-002/E-003)
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

before109 = text_out.count("Citation. 109. This Act may be cited")
text_out = text_out.replace("Citation. 109. This Act may be cited",
                            "109. This Act may be cited")

# R4a: soft-hyphen line-splits -> join (single words wrongly broken)
n_ctrl_before = text_out.count("\x02")
for split, joined in [("Commence\x02ments", "Commencements"),
                      ("Commence\x02ment", "Commencement"),
                      ("Misrepresenta\x02tion", "Misrepresentation")]:
    text_out = text_out.replace(split, joined)

# R4b: remaining 0x02 are genuine compound hyphens -> "-"
n_ctrl_hyphen = text_out.count("\x02")
text_out = text_out.replace("\x02", "-")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(text_out, encoding="utf-8")

print(f"R1 removed {n_removed} header lines")
print(f"R3 s.109 fixed: {before109}")
print(f"R4 total 0x02: {n_ctrl_before} | joined-splits: {n_ctrl_before - n_ctrl_hyphen} | hyphens: {n_ctrl_hyphen}")
assert text_out.count("\x02") == 0, "0x02 still present!"
for needle in ["Commencement", "Misrepresentation", "co-owners", "counter-notice", "Director-General", "70 years", "50 years"]:
    print(f"'{needle}': {text_out.count(needle)}")
print("OK -- wrote", OUT)
