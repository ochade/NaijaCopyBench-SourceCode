import re, json
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parents[2]
m = json.loads((ROOT/"data/derived/section_map.json").read_text(encoding="utf-8"))
secs = {int(k): v for k, v in m.items() if k != "SCHEDULE"}

def numbers_from_ref(ref):
    """Expand 'sections 9-13' -> [9..13]; 'sections 3, 4 and 8' -> [3,4,8]; 'section 7' -> [7]."""
    ref = re.sub(r"\s+", " ", ref)               # collapse newlines/spaces
    ref = ref.replace(" of this", "")
    out = set()
    # ranges: 9-13  or 9 to 13
    for a, b in re.findall(r"(\d+)\s*(?:-|to)\s*(\d+)", ref):
        out.update(range(int(a), int(b)+1))
    # remove ranges, then grab remaining individual numbers
    ref2 = re.sub(r"\d+\s*(?:-|to)\s*\d+", "", ref)
    out.update(int(x) for x in re.findall(r"\d+", ref2))
    return sorted(n for n in out if 1 <= n <= 109)

# reference patterns (order matters: match multi-number forms first)
REF = re.compile(r"sections?\s+[\d,\s\-]+(?:and\s*\d+)?(?:\s*of this)?"
                 r"|Part\s+[IVX]+", re.IGNORECASE)

edges = []          # (from_section, to_section)
part_refs = defaultdict(list)
for src, s in secs.items():
    txt = re.sub(r"\s+", " ", s["text"])         # normalise wraps
    for mm in REF.finditer(txt):
        ref = mm.group(0)
        if ref.lower().startswith("part"):
            part_refs[src].append(ref.strip())
            continue
        for tgt in numbers_from_ref(ref):
            if tgt != src:                       # ignore self-refs
                edges.append((src, tgt))

# build graph stats
out_deg = Counter(a for a, b in edges)
in_deg  = Counter(b for a, b in edges)

xrefs = {
    "edges": sorted(set(edges)),
    "n_edges": len(set(edges)),
    "out_degree": dict(out_deg),
    "in_degree": dict(in_deg),
    "part_refs": {str(k): v for k, v in part_refs.items()},
}
(ROOT/"data/derived/xrefs.json").write_text(json.dumps(xrefs, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"section-to-section edges: {len(set(edges))}")
print(f"\nMOST-REFERENCED sections (in-degree = multi-hop hubs):")
for sec, d in in_deg.most_common(8):
    print(f"  s.{sec} ({secs[sec]['title'][:30]}): referenced {d}x")
print(f"\nMOST-REFERENCING sections (out-degree):")
for sec, d in out_deg.most_common(8):
    print(f"  s.{sec} ({secs[sec]['title'][:30]}): makes {d} refs")
print(f"\nsample edges (multi-hop seeds):")
for a, b in sorted(set(edges))[:12]:
    print(f"  s.{a} -> s.{b}  ({secs[a]['title'][:22]} -> {secs[b]['title'][:22]})")
print("VERSION: xref-v1")
