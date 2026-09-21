from pathlib import Path
p = Path("src/score/parse_gold.py")
t = p.read_text(encoding="utf-8")

t = t.replace('''    if not s: return set()
    txt = re.sub(''',
'''    if not s: return set()
    # a gold answer stating that a provision does NOT exist is not a citation
    if re.search(r"\\bno\\s+(such\\s+)?section\\b|does\\s+not\\s+exist|non-?existent|"
                 r"\\bnot\\s+in\\s+the\\s+act\\b|\\bincorrect\\b", str(s), re.I):
        return set()
    txt = re.sub(''')
p.write_text(t, encoding="utf-8")
print("patched: negation detection added")
