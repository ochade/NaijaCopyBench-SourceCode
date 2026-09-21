from pathlib import Path
for fn in ["bootstrap_m1.py", "bootstrap_m2.py"]:
    p = Path(fn)
    t = p.read_text(encoding="utf-8")
    t = t.replace('for arm in ["A1", "A3", "A5"]', 'for arm in ["A1", "A2", "A3", "A5"]')
    t = t.replace('["A1","A3","A5"]', '["A1","A2","A3","A5"]')
    t = t.replace('[("A1","A3"), ("A1","A5"), ("A3","A5")]',
                  '[("A1","A2"), ("A1","A3"), ("A1","A5"), ("A2","A5"), ("A3","A5")]')
    t = t.replace('[("A1","A3"), ("A1","A5"), ("A3","A5")]',
                  '[("A1","A2"), ("A1","A3"), ("A1","A5"), ("A2","A5"), ("A3","A5")]')
    p.write_text(t, encoding="utf-8")
    print(f"{fn} patched")
