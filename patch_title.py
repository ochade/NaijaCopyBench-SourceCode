from pathlib import Path
p = Path("make_xref_figure.py")
t = p.read_text(encoding="utf-8")

t = t.replace(
'''ax.set_title("Cross-reference structure of the Copyright Act 2022",
             fontsize=14, pad=16, loc="left")''',
'''ax.set_title("Cross-reference structure of the Copyright Act 2022",
             fontsize=14, pad=34, loc="left")''')

t = t.replace('ax.text(0.0, 1.015,', 'ax.text(0.0, 1.005,')

p.write_text(t, encoding="utf-8")
print("patched: title pad 16 -> 34, subtitle y 1.015 -> 1.005")
