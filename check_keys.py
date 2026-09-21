import json
from pathlib import Path

for name in ["runs/A1_responses_180.jsonl", "runs/A2_responses_180.jsonl"]:
    p = Path(name)
    if not p.exists():
        print(f"{name}: NOT FOUND"); continue
    rows = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"\n{name}: {len(rows)} rows")
    print("  keys:", list(rows[0].keys()))
    print("  sample response field:", repr(next((rows[0][k] for k in ("response","output","text","answer") if k in rows[0]), "??"))[:120])
