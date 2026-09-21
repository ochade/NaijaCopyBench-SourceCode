import re

def parse_gold(s):
    """Parse a gold provision string into a set of (section, subsection) pairs.
    Handles comma lists, subsection ranges, section ranges, fused notation such
    as 19(1a), and orphan subsections such as '87(3), (4)'."""
    if not s: return set()
    # a gold answer stating that a provision does NOT exist is not a citation
    if re.search(r"\bno\s+(such\s+)?section\b|does\s+not\s+exist|non-?existent|"
                 r"\bnot\s+in\s+the\s+act\b|\bincorrect\b", str(s), re.I):
        return set()
    txt = re.sub(r"c\.?\s?a\.?\s?2022|copyright act|of this act|sections?|secs?\.?|s\.",
                 " ", str(s), flags=re.I)

    # blank out everything inside brackets before looking for SECTION ranges,
    # so "2(1-2)" cannot be read as sections 1 to 2
    masked = re.sub(r"\([^)]*\)", lambda m: " " * len(m.group(0)), txt)

    out, last_sec = set(), None
    for m in re.finditer(r"(\d{1,3})\s*[-–]\s*(\d{1,3})", masked):
        a, b = int(m.group(1)), int(m.group(2))
        if a < b <= 109:
            for n in range(a, b + 1): out.add((str(n), ""))

    for m in re.finditer(r"(\d{1,3})\s*\(\s*(\d{1,2})\s*([a-z])?\s*(?:[-–]\s*(\d{1,2}))?\s*\)"
                         r"|\(\s*(\d{1,2})\s*([a-z])?\s*\)"
                         r"|(\d{1,3})", txt):
        sec, sub, _p, sub2, osub, _op, bare = m.groups()
        if sec:
            if int(sec) > 109: continue
            last_sec = sec
            if sub2:
                for n in range(int(sub), int(sub2) + 1): out.add((sec, str(n)))
            else:
                out.add((sec, sub))
        elif osub and last_sec:
            out.add((last_sec, osub))
        elif bare:
            if int(bare) > 109: continue
            last_sec = bare
            out.add((bare, ""))
    return out

if __name__ == "__main__":
    tests = ["sections 2(1-2), 2(6), 3", "Sections 9, 12, 19(1-2)",
             "sections 23-24(1)", "sec 19(1a)", "S.87(3), (4)C.A 2022", "103",
             "sec 28(3a)", "S.20(1)(c), (d), (g)", "sec9((g), sec15(1)"]
    for t in tests:
        print(f"{t!r:34} -> {sorted(parse_gold(t))}")
