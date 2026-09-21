from pathlib import Path
p = Path("make_adjudication_sheet.py")
t = p.read_text(encoding="utf-8")

# remove the 20% sampling block - all agreed rows go for review
old_sample = '''# 20% of AGREED rows sampled in as a validity check on the agreed set
agreed_idx = [i for i, r in enumerate(rows) if r[1] == "AGREED"]
for i in random.sample(agreed_idx, max(1, round(0.2 * len(agreed_idx)))):
    rows[i][1] = "AGREED - SAMPLED CHECK"

'''
t = t.replace(old_sample, "")

# keep priority ordering but everything is in scope
t = t.replace('print(f"\\nFOR REVIEW: {sum(v for k,v in c.items() if k!=\'AGREED\')} of {len(rows)}")',
              'print(f"\\nALL {len(rows)} items sent for review; disagreements sorted to the top.")')
p.write_text(t, encoding="utf-8")
print("patched: full-set review")
