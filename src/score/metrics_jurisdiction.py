"""M3: jurisdictional specificity.

On items carrying a foreign_default, classify whether the answer states the
Nigerian value, a foreign value, or neither. Semi-automatic triage: it matches
salient legal quantities (terms of years, fine amounts). Prose-level displacement
- e.g. stating the US registration-before-suit rule with no number - is NOT
caught here and needs human review.
"""
import json, re
from pathlib import Path

def _numbers(s):
    """Salient legal quantities: '70 years', 'N100,000', '10 business days'."""
    out = set()
    s = s.lower()
    for m in re.finditer(r"(\d{1,3})\s*(?:business\s+)?(years?|months?|days?)", s):
        unit = m.group(2).rstrip("s")
        out.add(f"{m.group(1)} {unit}")
    for m in re.finditer(r"n\s?([\d,]{3,})", s):
        out.add("N" + m.group(1).replace(",", ""))
    for m in re.finditer(r"(\d{1,3})\s*per\s*cent|(\d{1,3})\s*%", s):
        out.add((m.group(1) or m.group(2)) + " percent")
    return out

def m3_jurisdictional(response, gold_answer, foreign_default):
    if not foreign_default:
        return {"verdict": "n/a", "reason": "no foreign_default"}

    r  = _numbers(response)
    ng = _numbers(gold_answer or "")
    foreign = {j: _numbers(v) for j, v in foreign_default.items()
               if j in ("US", "UK") and isinstance(v, str)}

    # if neither gold nor foreign carries extractable quantities, M3 cannot judge
    if not ng and not any(foreign.values()):
        return {"verdict": "n/a_no_quantities",
                "reason": "no comparable numeric values; needs prose-level review"}

    ng_hit = bool(r & ng)
    fhits = {j: sorted(r & v) for j, v in foreign.items() if r & v}

    if ng_hit and not fhits:
        return {"verdict": "NG_correct", "matched": sorted(r & ng)}
    if fhits and not ng_hit:
        return {"verdict": "foreign_substituted", "jurisdictions": fhits}
    if ng_hit and fhits:
        return {"verdict": "both_present", "ng": sorted(r & ng),
                "foreign": fhits, "note": "HUMAN REVIEW"}
    return {"verdict": "other_wrong", "in_response": sorted(r),
            "expected_ng": sorted(ng)}

if __name__ == "__main__":
    ROOT = Path(__file__).resolve().parents[2]
    items = {i["id"]: i for i in (json.loads(l) for l in
             (ROOT/"data/eval/vertical_slice_12.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}
    any_run = False
    for arm in ["A1", "A3", "A5"]:
        p = ROOT/f"results/{arm}_scored.jsonl"
        if not p.exists():
            print(f"{arm}: no scored file"); continue
        print(f"\n=== {arm} ===")
        for r in (json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()):
            it = items.get(r["item_id"], {})
            if not it.get("foreign_default"): continue
            any_run = True
            v = m3_jurisdictional(r["response"], it.get("gold_answer"), it["foreign_default"])
            detail = {k: x for k, x in v.items() if k != "verdict"}
            print(f"  {r['item_id']:14} {v['verdict']:22} {detail}")
    if not any_run:
        print("\nNo vertical-slice item carries a foreign_default. Check the items file.")
