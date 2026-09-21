import sys
sys.path.insert(0, "src/score")
from metrics_citation import CITE
from parse_gold import parse_gold

tests = ["This is covered by Section 19(1)(d) of the Act.",
         "See s.87 and section 4.",
         "Under Section 114, technological measures are protected."]
for t in tests:
    print(repr(t))
    for m in CITE.finditer(t):
        print("   groups:", m.groups(), "| full:", m.group(0))
    print()

print("gold parse of an empty string:", parse_gold(""))
print("gold parse of 'no such section':", parse_gold("no such section"))
