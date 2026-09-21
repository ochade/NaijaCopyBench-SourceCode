from pathlib import Path
for fn in ["score_m1_all.py", "score_m2_180.py"]:
    p = Path(fn)
    if not p.exists():
        print(f"missing: {fn}"); continue
    t = p.read_text(encoding="utf-8")
    before = t
    t = t.replace('for arm in ["A1", "A3", "A5"]:', 'for arm in ["A1", "A2", "A3", "A5"]:')
    t = t.replace('for arm in ["A1","A3","A5"]:',   'for arm in ["A1","A2","A3","A5"]:')
    p.write_text(t, encoding="utf-8")
    print(f"{fn}: {'patched' if t != before else 'NO CHANGE - check the arm list by hand'}")
