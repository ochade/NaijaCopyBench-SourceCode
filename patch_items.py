from pathlib import Path

p = Path("src/build_eval_items.py")
t = p.read_text(encoding="utf-8")

before = t

# fix 1: s.30(4) also allows "inferred from conduct"
t = t.replace(
    '"non-exclusive licence may be oral or written"',
    '"non-exclusive licence may be written, oral, or inferred from conduct"'
)

# fix 2: s.103 is on page 59, not 62
t = t.replace('"source_page": 62,', '"source_page": 59,')

p.write_text(t, encoding="utf-8")
print("changed:", t != before)
print("has inferred-from-conduct:", "inferred from conduct" in t)
print("still has page 62:", '"source_page": 62,' in t)
