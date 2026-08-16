"""
M1: citation validity  - does every cited provision EXIST in the Act?
M2: citation accuracy  - does the citation match the gold provision?

Both decided against data/derived/section_map.json (the verified oracle).
Fabrication is DECIDABLE here, not estimated: the Act has exactly 109 sections
with known subsection/paragraph bounds.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAP = json.loads((ROOT / "data/derived/section_map.json").read_text(encoding="utf-8"))
SECS = {k: v for k, v in MAP.items() if k != "SCHEDULE"}

# ---------- citation extraction ----------
# Formats observed from gpt-4o-mini: "Section 114", "Section 27(1)", "Section 10"
# Also handle: s.19, S. 19, section 19(1)(d), sections 9-13
CITE = re.compile(
    r"(?:\b[Ss]ections?\s+|(?<![A-Za-z])[Ss]\.\s?|(?<![A-Za-z])[Ss]ec\.\s?)"
    r"(\d{1,3})"                      # section number
    r"(?:\s?\((\d{1,2})\))?"          # optional subsection (1)
    r"(?:\s?\(([a-z])\))?"            # optional paragraph (a)
)

def extract_citations(text):
    """Return list of dicts: {raw, section, subsection, paragraph}."""
    out = []
    for m in CITE.finditer(text):
        out.append({
            "raw": m.group(0).strip(),
            "section": m.group(1),
            "subsection": m.group(2),
            "paragraph": m.group(3),
        })
    return out

# ---------- M1: validity ----------
def check_validity(c):
    """Return 'valid' | 'fabricated_section' | 'fabricated_subsection' | 'fabricated_paragraph'."""
    s = c["section"]
    if s not in SECS:
        return "fabricated_section"
    rec = SECS[s]
    if c["subsection"]:
        if c["subsection"] not in (rec.get("subsections") or []):
            return "fabricated_subsection"
    if c["paragraph"]:
        if c["paragraph"] not in (rec.get("paragraph_letters") or []):
            return "fabricated_paragraph"
    return "valid"

def m1_citation_validity(response_text):
    cites = extract_citations(response_text)
    results = [{**c, "verdict": check_validity(c)} for c in cites]
    n = len(results)
    n_valid = sum(1 for r in results if r["verdict"] == "valid")
    return {
        "n_citations": n,
        "n_valid": n_valid,
        "n_fabricated": n - n_valid,
        "fabrication_rate": (n - n_valid) / n if n else None,
        "detail": results,
    }

# ---------- M2: accuracy ----------
def parse_gold(g):
    """'19(1)(d)' -> ('19','1','d');  '4' -> ('4',None,None)"""
    m = re.match(r"(\d{1,3})(?:\((\d{1,2})\))?(?:\(([a-z])\))?", g)
    return (m.group(1), m.group(2), m.group(3)) if m else (g, None, None)

def m2_citation_accuracy(response_text, gold_sections):
    cites = extract_citations(response_text)
    if not gold_sections:                      # fabrication items: no gold citation
        return {"verdict": "n/a_no_gold", "n_citations": len(cites)}
    golds = [parse_gold(g) for g in gold_sections]
    gold_secs = {g[0] for g in golds}
    cited_secs = {c["section"] for c in cites}

    if not cites:
        return {"verdict": "no_citation", "n_citations": 0}

    # exact: gold section AND subsection matched
    for c in cites:
        for gs, gsub, gpar in golds:
            if c["section"] == gs and (gsub is None or c["subsection"] == gsub):
                return {"verdict": "correct", "matched": c["raw"],
                        "n_citations": len(cites),
                        "over_cited": len(cited_secs - gold_secs)}
    # right section, missing/wrong subsection
    if cited_secs & gold_secs:
        return {"verdict": "correct_section_coarse", "n_citations": len(cites),
                "cited": sorted(cited_secs), "gold": sorted(gold_secs)}
    # all cited sections exist but none is the gold one
    if all(c["section"] in SECS for c in cites):
        return {"verdict": "wrong_but_real", "n_citations": len(cites),
                "cited": sorted(cited_secs), "gold": sorted(gold_secs)}
    return {"verdict": "fabricated", "n_citations": len(cites),
            "cited": sorted(cited_secs), "gold": sorted(gold_secs)}

# ---------- self-test on the three responses we actually observed ----------
if __name__ == "__main__":
    tests = [
        ("FAB-001 s.114 fabrication",
         "Section 114 of the Nigerian Copyright Act 2022 addresses digital rights management (DRM).",
         []),
        ("DIV-001 wrong-but-real",
         "According to Section 27(1) of the Act, copyright in a sound recording lasts 50 years.",
         ["19(1)(d)"]),
        ("FAB-003 wrong section for registration",
         "According to Section 10 of the Act, the application must be made in writing.",
         []),
        ("synthetic: correct citation",
         "Under Section 19(1)(d), sound recordings are protected for 50 years.",
         ["19(1)(d)"]),
        ("synthetic: coarse citation",
         "Section 19 governs the duration of copyright.",
         ["19(1)(d)"]),
        ("synthetic: fabricated subsection",
         "See Section 19(4) for database duration.",
         []),
    ]
    for name, text, gold in tests:
        m1 = m1_citation_validity(text)
        m2 = m2_citation_accuracy(text, gold)
        print(f"\n--- {name}")
        print(f"  text: {text[:60]}...")
        print(f"  M1: {m1['n_citations']} cites, {m1['n_fabricated']} fabricated "
              f"-> {[d['verdict'] for d in m1['detail']]}")
        print(f"  M2: {m2['verdict']}")
