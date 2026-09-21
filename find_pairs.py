for fn in ["bootstrap_m1.py", "bootstrap_m2.py"]:
    print("="*60)
    print(fn)
    for line in open(fn, encoding="utf-8"):
        s = line.strip()
        if '"A1"' in s and '"A3"' in s and "(" in s:
            print("  PAIR LINE:", s)
        if "for arm in" in s and "A1" in s:
            print("  ARM LOOP :", s)
