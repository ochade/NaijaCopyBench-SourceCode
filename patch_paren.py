from pathlib import Path
p = Path("src/extract/build_section_map.py")
t = p.read_text(encoding="utf-8")
before = t
t = t.replace(
    'para_letters = sorted(set(re.findall(r"(?m)^\\s*\\(([a-z])\\)", body)))',
    'para_letters = sorted(set(re.findall(r"(?m)^\\s*\\(\\s*([a-z])\\s*\\)", body)))'
)
p.write_text(t, encoding="utf-8")
print("changed:", t != before)
