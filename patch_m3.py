from pathlib import Path
p = Path("src/score/metrics_jurisdiction.py")
t = p.read_text(encoding="utf-8")
old = '''    ng_hit = bool(r & ng)'''
new = '''    # if neither gold nor foreign carries extractable quantities, M3 cannot judge
    if not ng and not any(foreign.values()):
        return {"verdict": "n/a_no_quantities",
                "reason": "no comparable numeric values; needs prose-level review"}

    ng_hit = bool(r & ng)'''
t = t.replace(old, new)
p.write_text(t, encoding="utf-8")
print("patched:", new.split(chr(10))[1] in t)
