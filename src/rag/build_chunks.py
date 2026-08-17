"""
Step 6a: Chunk section_map.json for retrieval.
EDA-B decision: median section = 149 words; 15 sections > 400 words.
  -> section-level chunks for the 94 short/medium sections
  -> subsection-level splits for the 15 long ones
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
m = json.loads((ROOT/"data/derived/section_map.json").read_text(encoding="utf-8"))
secs = {int(k): v for k, v in m.items() if k != "SCHEDULE"}

LONG = 400   # words

def split_subsections(text):
    """Split on lines beginning (1) (2) (3)... keeping the header with sub (1)."""
    parts, cur, label = [], [], None
    for line in text.split("\n"):
        mm = re.match(r"^\s*\((\d{1,2})\)", line)
        if mm:
            if cur:
                parts.append((label, "\n".join(cur).strip()))
            label, cur = mm.group(1), [line]
        else:
            cur.append(line)
    if cur:
        parts.append((label, "\n".join(cur).strip()))
    return [(l, t) for l, t in parts if t]

def split_paragraphs(text):
    """Fallback: split on lines beginning (a) (b) (c)... for sections with no
    numbered subsections (e.g. s.20 exceptions, s.108 definitions)."""
    parts, cur, label = [], [], None
    for line in text.split("\n"):
        mm = re.match(r"^\s*\(\s*([a-z])\s*\)", line)
        if mm:
            if cur:
                parts.append((label, "\n".join(cur).strip()))
            label, cur = mm.group(1), [line]
        else:
            cur.append(line)
    if cur:
        parts.append((label, "\n".join(cur).strip()))
    return [(l, t_) for l, t_ in parts if t_]

def word_cap(label, text, cap=350):
    """Last resort: cut into <=cap-word pieces on line boundaries."""
    out, cur, count, i = [], [], 0, 1
    for line in text.split("\n"):
        w = len(line.split())
        if count + w > cap and cur:
            out.append((f"{label}p{i}" if label else f"p{i}", "\n".join(cur).strip()))
            cur, count, i = [], 0, i + 1
        cur.append(line); count += w
    if cur:
        out.append((f"{label}p{i}" if label else f"p{i}", "\n".join(cur).strip()))
    return [(l, t_) for l, t_ in out if t_]

chunks = []
for n, s in sorted(secs.items()):
    text, title, page = s["text"], s["title"], s.get("page")
    words = len(text.split())
    if words <= LONG:
        chunks.append({"chunk_id": f"s{n}", "section": n, "subsection": None,
                       "title": title, "page": page, "n_words": words,
                       "text": f"Section {n}. {title}.\n{text}"})
    else:
        parts = split_subsections(text)
        # any part still too long: try paragraph markers, then hard word cap
        expanded = []
        for label, part in parts:
            if len(part.split()) <= LONG:
                expanded.append((label, part)); continue
            sub = split_paragraphs(part)
            if len(sub) > 1:
                for plabel, ppart in sub:
                    if len(ppart.split()) <= LONG:
                        expanded.append((f"{label}{plabel}" if label else plabel, ppart))
                    else:
                        expanded.extend(word_cap(label, ppart))
            else:
                expanded.extend(word_cap(label, part))
        parts = expanded
        for label, part in parts:
            tag = f"s{n}" if label is None else f"s{n}({label})"
            chunks.append({"chunk_id": tag, "section": n, "subsection": label,
                           "title": title, "page": page,
                           "n_words": len(part.split()),
                           "text": f"Section {n}. {title}.\n{part}"})

out = ROOT/"data/derived/chunks.jsonl"
out.write_text("\n".join(json.dumps(c, ensure_ascii=False) for c in chunks) + "\n",
               encoding="utf-8")

ws = [c["n_words"] for c in chunks]
print(f"chunks: {len(chunks)}")
print(f"words/chunk - min {min(ws)}, median {sorted(ws)[len(ws)//2]}, max {max(ws)}")
print(f"sections split: {len({c['section'] for c in chunks if c['subsection']})}")
print(f"still over {LONG} words: {sum(1 for w in ws if w > LONG)}")
print("wrote", out)
