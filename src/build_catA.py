import json, csv
from pathlib import Path

# item_id, question, expected_provision (INTERNAL ONLY - not sent to lawyers)
ITEMS = [
 ("NCB-A-001","Under Nigerian law, what kinds of creative work can have copyright at all?","2(1)"),
 ("NCB-A-002","I described a business idea to a friend in detail and now he is using it. Does Nigerian copyright law protect the idea itself?","3(a)"),
 ("NCB-A-003","I hummed a melody to my producer but never recorded it anywhere. Is it protected under Nigerian law yet?","2(2)(b)"),
 ("NCB-A-004","My painting was called amateurish by a gallery in Lagos. Does the quality of a work affect whether it gets copyright in Nigeria?","2(3)"),
 ("NCB-A-005","I designed a pattern specifically to be used for mass-produced fabric. Is that protected as an artistic work under Nigerian copyright law?","2(6)"),
 ("NCB-A-006","Can anyone claim copyright in the text of a Nigerian statute or a government circular?","3(b)"),
 ("NCB-A-007","Is the Nigerian coat of arms protected by copyright?","3(c)"),
 ("NCB-A-008","I compiled and organised a set of publicly available government notices into a reference book. Can my compilation be protected under Nigerian law?","3(b)/2(5)"),
 ("NCB-A-009","I finished writing a short story last month. Do I need to do anything official before it is protected under Nigerian law?","4"),
 ("NCB-A-010","I registered my song with the Copyright Commission. Does that registration itself give me the copyright?","87(3)"),
 ("NCB-A-011","If I do register a work in Nigeria, what practical use does the registration have if it does not create the copyright?","87(4)"),
 ("NCB-A-012","Someone submitted false information when registering a work with the Commission. Is that an offence under Nigerian law?","87(7)"),
 ("NCB-A-013","Who owns copyright in a work by default under Nigerian law, if there is no agreement saying otherwise?","28(1)"),
 ("NCB-A-014","I work for a federal ministry and wrote a training manual as part of my job. Who owns the copyright?","28(2)"),
 ("NCB-A-015","I paid a photographer to take family portraits at my home in Abuja. Who owns the copyright in those photos under Nigerian law?","28(3)"),
 ("NCB-A-016","I commissioned a private portrait. Can I stop the artist from publishing it or putting it in an exhibition?","28(3)(b)"),
 ("NCB-A-017","An editor assembled an anthology of Nigerian short stories. Who owns copyright in the anthology as a whole?","29(a)"),
 ("NCB-A-018","My story appeared in an anthology someone else compiled. Can I still publish that story separately?","29(b)"),
 ("NCB-A-019","A Lagos photographer died in 2010. How long does copyright in his photographs run under Nigerian law?","19(1)(c)"),
 ("NCB-A-020","How long does copyright last in a radio broadcast under Nigerian law?","19(1)(e)"),
 ("NCB-A-021","A novel was published anonymously in Nigeria in 1990 and the author has never been identified. How long does copyright last?","19(2)"),
 ("NCB-A-022","Two writers co-authored a book and one died in 2005, the other in 2020. From which death is the copyright term counted under Nigerian law?","19(3)"),
 ("NCB-A-023","When does copyright in a work actually begin under Nigerian law - on creation, on publication, or on registration?","18"),
 ("NCB-A-024","A producer says I gave him an exclusive licence to my beat because I agreed over the phone. Is a verbal agreement enough under Nigerian law?","30(3)"),
 ("NCB-A-025","Can I assign my copyright for just five years, or for Nigeria only, rather than giving it away completely?","30(2)"),
 ("NCB-A-026","Does a non-exclusive licence have to be in writing under Nigerian law?","30(4)"),
 ("NCB-A-027","Under Nigerian law, is copyright treated as property that can be left to someone in a will?","30(1)"),
 ("NCB-A-028","A distributor brought copies of my book into Nigeria from abroad without my permission. Is importing infringing under Nigerian law?","36(b)"),
 ("NCB-A-029","A club in Lagos plays my music every weekend to attract customers, without any licence. Is the club infringing under Nigerian law?","36(g)"),
 ("NCB-A-030","Someone owns duplicating machines used only for making pirated CDs. Is mere possession of that equipment infringement under Nigerian law?","36(d)"),
 ("NCB-A-031","A hall owner let a group stage a play using my script without permission, but genuinely did not know it was unlicensed. Is he liable under Nigerian law?","36(e)"),
 ("NCB-A-032","Someone copied two sentences from my 300-page novel. Is that enough to be infringement under Nigerian law?","36(2)"),
 ("NCB-A-033","I hold an exclusive licence, not the copyright itself. Can I sue for infringement in my own name under Nigerian law?","37(1)"),
 ("NCB-A-034","What exclusive rights do I actually get over a literary work under Nigerian law?","9"),
 ("NCB-A-035","Someone is selling counterfeit copies of my textbook in Onitsha. Which court hears a copyright case in Nigeria?","103"),
]

# double-annotated subset (both lawyers) - spread across sub-topics
OVERLAP = {"NCB-A-001","NCB-A-005","NCB-A-009","NCB-A-012","NCB-A-014",
           "NCB-A-016","NCB-A-019","NCB-A-022","NCB-A-026","NCB-A-031",
           "NCB-A-032","NCB-A-035"}

ROOT = Path(__file__).resolve().parents[1] if "__file__" in dir() else Path(".")
Path("data/eval").mkdir(parents=True, exist_ok=True)
Path("docs").mkdir(exist_ok=True)

# 1. INTERNAL file - keeps expected provisions + overlap flags
internal = [{"item_id": i, "question": q, "expected_provision": p,
             "category": "single_hop", "double_annotated": i in OVERLAP}
            for i, q, p in ITEMS]
Path("data/eval/catA_internal.jsonl").write_text(
    "\n".join(json.dumps(x, ensure_ascii=False) for x in internal) + "\n", encoding="utf-8")

# 2. LAWYER sheet - questions only, no hints
with open("docs/catA_annotation_sheet.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["item_id","question","governing_provision","answer","confidence","notes"])
    for i, q, p in ITEMS:
        w.writerow([i, q, "", "", "", ""])

print(f"{len(ITEMS)} items")
print(f"double-annotated: {len(OVERLAP)}")
print("internal  -> data/eval/catA_internal.jsonl")
print("to lawyers-> docs/catA_annotation_sheet.csv")
