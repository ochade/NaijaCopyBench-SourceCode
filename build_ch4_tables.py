import json
from pathlib import Path

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8")) if Path(p).exists() else None

print("="*70)
print("TABLE 4.x  M1 FABRICATION RATE BY ARM (180 items, 95% CI)")
print("="*70)
m1 = load("results/m1_bootstrap.json")
if m1:
    print(f"{'Arm':6}{'Rate':>10}{'95% CI':>18}")
    names = {"A1":"Qwen-3B","A2":"Qwen-3B tuned","A3":"gpt-4o-mini","A5":"gpt-4o-mini+RAG"}
    for a, v in m1["overall"].items():
        print(f"{a:6}{v['rate']:>9.1f}%   [{v['lo']:.1f}, {v['hi']:.1f}]")

print("\n"+"="*70)
print("TABLE 4.x  M2 CITATION ACCURACY BY ARM (145 items, Cat E excluded)")
print("="*70)
m2 = load("results/m2_bootstrap.json")
if m2:
    for a, v in m2["overall"].items():
        print(f"{a:6}{v['acc']:>9.1f}%   [{v['lo']:.1f}, {v['hi']:.1f}]")

print("\n"+"="*70)
print("TABLE 4.x  M4 CLAIM-LEVEL FACTUALITY (sampled, 611 claims)")
print("="*70)
m4 = load("results/m4_scored.json")
if m4:
    print(f"{'Arm':6}{'Claims':>8}{'Supported':>11}{'Contra':>9}{'Precision':>11}{'Contra rate':>13}")
    for a, d in m4["by_arm"].items():
        tot = d["S"]+d["N"]+d["C"]
        print(f"{a:6}{tot:>8}{d['S']:>11}{d['C']:>9}{100*d['S']/tot:>10.1f}%{100*d['C']/tot:>12.1f}%")
