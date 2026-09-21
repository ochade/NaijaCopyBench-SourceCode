"""Foreign-law markers for Category C items.

A phrase belongs here only if it indicates US or UK law and would NOT appear in
a correct statement of the Nigerian position. Matching is case-insensitive
substring matching on the response text.

REVIEW REQUIRED: these are drafted from the foreign_default fields and must be
checked against the Act before use. Markers that could plausibly appear in a
correct Nigerian answer must be removed.
"""

MARKERS = {
 # ---- Part VII: takedown ----
 "NCB-C-001": ["penalty of perjury", "512", "DMCA", "good faith belief"],
 "NCB-C-002": ["penalty of perjury", "512", "DMCA"],
 "NCB-C-003": ["attorney", "attorneys' fees", "512(f)", "DMCA"],
 "NCB-C-004": ["512", "DMCA", "safe harbor", "safe harbour"],
 "NCB-C-005": ["business day", "10 to 14", "10-14", "court action", "restraining order", "512", "DMCA"],
 "NCB-C-006": ["no obligation to monitor", "no duty to monitor", "not required to monitor",
               "512(m)", "no general monitoring", "no stay-down"],
 "NCB-C-007": ["512", "DMCA", "federal court", "district court"],
 "NCB-C-008": ["loses the safe harbor", "loses the safe harbour", "512", "DMCA"],
 "NCB-C-009": ["repeat infringer policy", "appropriate circumstances", "512(i)", "DMCA"],
 "NCB-C-010": ["consent to", "jurisdiction of the federal", "district court", "service of process", "512(g)"],
 "NCB-C-011": ["no minimum", "appropriate circumstances", "512(i)"],
 "NCB-C-012": ["safe harbor", "safe harbour", "512(c)", "DMCA", "red flag"],
 "NCB-C-013": ["512(d)", "DMCA", "information location tool", "safe harbor", "safe harbour"],
 "NCB-C-014": ["Copyright Office", "register the agent", "512(c)(2)", "DMCA"],


 # ---- Folklore and levy ----
 "NCB-C-016": ["public domain", "no permission", "not protected", "free to use", "traditional works are not"],
 "NCB-C-017": ["the community itself", "community grants", "no central body", "public domain"],
 "NCB-C-018": ["public domain", "70 years", "life of the author", "expires after"],
 "NCB-C-019": ["fair use", "public domain", "no permission needed"],
 "NCB-C-020": ["fair use", "public domain", "transformative"],
 "NCB-C-021": ["no attribution", "not required to", "public domain"],
 "NCB-C-022": ["public domain", "not protected", "design right", "trade mark"],
 "NCB-C-023": ["public domain", "not protected", "choreographic work"],
 "NCB-C-024": ["no levy", "Audio Home Recording", "AHRA", "1001", "digital audio recording device",
               "there is no such levy"],
 "NCB-C-025": ["Copyright Office", "AHRA", "fixed in the statute", "no levy"],
 "NCB-C-026": ["Copyright Office", "AHRA", "1006", "no levy"],
 "NCB-C-027": ["digital audio recording", "AHRA", "only blank", "physical media only", "no levy"],

 # ---- Exceptions ----
 "NCB-C-028": ["fair use", "four factor", "four-factor", "107", "multiple copies for classroom"],
 "NCB-C-029": ["fair use", "four factor", "four-factor", "107"],
 "NCB-C-030": ["fair use", "one factor", "107(1)", "nonprofit educational purposes is a factor"],
 "NCB-C-031": ["fair use", "107", "four factor"],
 "NCB-C-032": ["fair use", "110", "107", "TEACH Act"],
 "NCB-C-033": ["fair use", "107", "fourth factor", "market effect"],
 "NCB-C-034": ["fair use", "107", "no set limit", "no fixed percentage", "twelve months", "12 months",
               "depends on the four"],
 "NCB-C-035": ["contract prevails", "terms of the licence govern", "enforceable", "freedom of contract"],
 "NCB-C-036": ["fair use", "107", "no override"],
 "NCB-C-037": ["first sale", "109", "exhaustion", "lawfully made copy"],
 "NCB-C-038": ["108(d)", "108(e)", "copyright warning notice", "no liability provision"],
 "NCB-C-039": ["three copies", "108(b)", "unpublished works only", "premises"],
 "NCB-C-040": ["fair price", "108(e)", "cannot be obtained at a fair price", "no orphan works",
               "orphan works exception does not exist"],
 "NCB-C-041": ["108(c)", "three copies", "fair price"],
 

 # ---- Remaining Part VII and folklore ----
 "NCB-C-043": ["512(g)(1)", "good faith disabling", "DMCA"],
 "NCB-C-044": ["subpoena", "clerk of the court", "clerk of a district", "512(h)", "Norwich Pharmacal"],
 "NCB-C-045": ["public domain", "106A", "VARA", "visual art", "no community right", "moral rights only"],
}

if __name__ == "__main__":
    print(f"{len(MARKERS)} items with markers")
    n = sum(len(v) for v in MARKERS.values())
    print(f"{n} markers total, mean {n/len(MARKERS):.1f} per item")
    missing = [k for k, v in MARKERS.items() if not v]
    print("items with no markers:", missing or "none")
