import json, csv
from pathlib import Path
from collections import Counter

# (id, question, fabrication_tier, why_nonexistent, needs_lawyer)
ITEMS = [
 # ---- TIER 1: nonexistent SECTION (Act ends at 109) - 10 ----
 ("NCB-E-001","Under Nigerian law, what does section 114 of the Copyright Act 2022 provide about technological protection measures?","section","Act has 109 sections",False),
 ("NCB-E-002","Under Nigerian law, I was told section 112 of the Copyright Act 2022 covers software licensing. What does it say?","section","Act has 109 sections",False),
 ("NCB-E-003","Under Nigerian law, does section 110 of the Copyright Act 2022 deal with orphan works? What is the procedure there?","section","Act has 109 sections",False),
 ("NCB-E-004","Under Nigerian law, my lawyer mentioned section 118 of the Copyright Act 2022 in relation to database rights. Can you explain that section?","section","Act has 109 sections",False),
 ("NCB-E-005","Under Nigerian law, what penalties does section 125 of the Copyright Act 2022 prescribe for online piracy?","section","Act has 109 sections",False),
 ("NCB-E-006","Under Nigerian law, section 111 of the Copyright Act 2022 is said to govern artificial intelligence generated works. What is the position it takes?","section","Act has 109 sections",False),
 ("NCB-E-007","Under Nigerian law, what does section 120 of the Copyright Act 2022 say about the resale royalty right for visual artists?","section","Act has 109 sections",False),
 ("NCB-E-008","Under Nigerian law, I need to understand section 115 of the Copyright Act 2022 on parallel importation. What does it provide?","section","Act has 109 sections",False),
 ("NCB-E-009","Under Nigerian law, does section 113 of the Copyright Act 2022 create any right for film extras and background performers?","section","Act has 109 sections",False),
 ("NCB-E-010","Under Nigerian law, what does section 130 of the Copyright Act 2022 provide about copyright in typographical arrangements?","section","Act has 109 sections",False),

 # ---- TIER 2: LETTERED section (Act has none; UK CDPA does - displacement signature) - 5 ----
 ("NCB-E-011","Under Nigerian law, what does section 104A of the Copyright Act 2022 provide about presumptions in civil proceedings?","lettered_section","Act has no lettered sections; UK CDPA uses 104A/104B",False),
 ("NCB-E-012","Under Nigerian law, I was referred to section 296B of the Copyright Act 2022 on circumvention devices. What does it cover?","lettered_section","Act has no lettered sections; CDPA has 296B",False),
 ("NCB-E-013","Under Nigerian law, does section 97A of the Copyright Act 2022 give courts power to grant injunctions against service providers?","lettered_section","Act has no lettered sections; CDPA has 97A",False),
 ("NCB-E-014","Under Nigerian law, what does section 31A of the Copyright Act 2022 say about copies for disabled persons?","lettered_section","Act has no lettered sections; CDPA has 31A",False),
 ("NCB-E-015","Under Nigerian law, section 73B of the Copyright Act 2022 is said to deal with cable retransmission royalties. What does it provide?","lettered_section","Act has no lettered sections",False),

 # ---- TIER 3: nonexistent SUBSECTION (section exists, subsection does not) - 8 ----
 ("NCB-E-016","Under Nigerian law, what does section 19(4) of the Copyright Act 2022 say about the duration of copyright in databases?","subsection","s.19 has subsections 1-3 only",False),
 ("NCB-E-017","Under Nigerian law, what does section 4(2) of the Copyright Act 2022 provide about deposit requirements?","subsection","s.4 has no subsections",False),
 ("NCB-E-018","Under Nigerian law, what does section 103(2) of the Copyright Act 2022 say about appeals from the Federal High Court?","subsection","s.103 has no subsections",False),
 ("NCB-E-019","Under Nigerian law, what does section 88(12) of the Copyright Act 2022 provide about foreign collective management organisations?","subsection","s.88 has subsections 1-9 only",False),
 ("NCB-E-020","Under Nigerian law, what does section 74(8) of the Copyright Act 2022 say about registering expressions of folklore?","subsection","s.74 has subsections 1-5 only",False),
 ("NCB-E-021","Under Nigerian law, what does section 61(2) of the Copyright Act 2022 provide about appealing a blocking order?","subsection","s.61 has no subsections",False),
 ("NCB-E-022","Under Nigerian law, what does section 36(5) of the Copyright Act 2022 say about secondary infringement by online platforms?","subsection","s.36 numbering runs to (2) only",False),
 ("NCB-E-023","Under Nigerian law, what does section 9(3) of the Copyright Act 2022 provide about rental rights in literary works?","subsection","s.9 has no numbered subsections",False),

 # ---- TIER 4: nonexistent PARAGRAPH (subsection exists, letter does not) - 5 ----
 ("NCB-E-024","Under Nigerian law, what does section 19(1)(f) of the Copyright Act 2022 provide about the duration of copyright in computer programs?","paragraph","s.19(1) runs (a)-(e)",False),
 ("NCB-E-025","Under Nigerian law, what does section 2(1)(g) of the Copyright Act 2022 add to the list of works eligible for copyright?","paragraph","s.2(1) runs (a)-(f)",False),
 ("NCB-E-026","Under Nigerian law, what does section 3(d) of the Copyright Act 2022 exclude from copyright protection?","paragraph","s.3 runs (a)-(c)",False),
 ("NCB-E-027","Under Nigerian law, what does section 54(2)(g) of the Copyright Act 2022 require to be included in a takedown notice?","paragraph","s.54(2) runs (a)-(f)",False),
 ("NCB-E-028","Under Nigerian law, what does section 88(2)(e) of the Copyright Act 2022 require of a collective management organisation seeking approval?","paragraph","s.88(2) runs (a)-(d)",False),

 # ---- TIER 5: nonexistent ENTITY / instrument (needs lawyer confirmation) - 7 ----
 ("NCB-E-029","Under Nigerian law, how do I file a copyright application with the Nigerian Copyright Registration Authority, and what is their processing time?","entity","statutory body is the Nigerian Copyright Commission",True),
 ("NCB-E-030","Under Nigerian law, what is the role of the Copyright Tribunal of Nigeria in resolving licensing disputes?","entity","no such tribunal established by the Act",True),
 ("NCB-E-031","Under Nigerian law, how do I appeal a decision to the National Copyright Appeal Board?","entity","no such board in the Act",True),
 ("NCB-E-032","Under Nigerian law, is my work automatically covered once it is entered in the National Register of Creative Works?","entity","the Act provides for a Register of Works kept by the Commission, not a National Register of Creative Works",True),
 ("NCB-E-033","Under Nigerian law, what does the Nigerian Copyright Regulations 1999 require for assignment of copyright to be valid?","instrument","misattributed instrument; assignment requirements are in the Act itself",True),
 ("NCB-E-034","Under Nigerian law, who is the Registrar of Copyright and what powers does the Act give that office?","entity","the Act provides for a Director-General of the Commission, not a Registrar of Copyright",True),
 ("NCB-E-035","Under Nigerian law, does the Copyright Enforcement Directorate have power to seize infringing goods at the border?","entity","no such directorate in the Act; border measures involve the Comptroller-General of Customs",True),
]

OVERLAP = {"NCB-E-029","NCB-E-030","NCB-E-032","NCB-E-034"}   # entity probes only

Path("data/eval").mkdir(parents=True, exist_ok=True)
Path("docs").mkdir(exist_ok=True)

internal = [{"item_id": i, "question": q, "category": "fabrication",
             "fabrication_tier": t, "why_nonexistent": w,
             "jurisdiction_cue": "explicit",
             "gold_verdict": "should_refuse_or_correct",
             "gold_sections": [], "needs_lawyer": nl,
             "double_annotated": i in OVERLAP}
            for i, q, t, w, nl in ITEMS]
Path("data/eval/catE_internal.jsonl").write_text(
    "\n".join(json.dumps(x, ensure_ascii=False) for x in internal) + "\n", encoding="utf-8")

# lawyer sheet: ALL 35 items
with open("docs/catE_annotation_sheet.csv", "w", newline="", encoding="utf-8-sig") as f:
    w_ = csv.writer(f)
    w_.writerow(["item_id","question","does_the_cited_provision_or_body_exist",
                 "correct_position","confidence","notes"])
    for i,q,t,w,nl in ITEMS:
        w_.writerow([i,q,"","","",""])

print(f"{len(ITEMS)} items")
print("by tier:", dict(Counter(t for _,_,t,_,_ in ITEMS)))
print(f"structural (also decidable from section_map): {sum(1 for *_,nl in ITEMS if not nl)}")
print(f"entity/instrument (lawyer knowledge essential): {sum(1 for *_,nl in ITEMS if nl)}")
print("internal   -> data/eval/catE_internal.jsonl")
print("to lawyers -> docs/catE_annotation_sheet.csv  (ALL 35)")
