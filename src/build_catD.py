import json, csv
from pathlib import Path
from collections import Counter

# (id, question, expected_provision, convergence_basis, nigerian_phrasing)
ITEMS = [
 # ---- Duration of literary/artistic works: s.19(1)(a) (4) ----
 ("NCB-D-001","Under Nigerian law, a Lagos novelist died in 2015. Her novels were published in her lifetime. How long does copyright in them last?","19(1)(a)",
  "US 17 USC 302(a) life+70; UK CDPA 1988 s.12(2) life+70","70 years after the end of the YEAR in which the author dies (not 'life plus 70')"),
 ("NCB-D-002","Under Nigerian law, a painter based in Enugu died in March 2020. From what point is the copyright period in his paintings counted?","19(1)(a)",
  "US 17 USC 302(a); UK CDPA s.12(2) - both run from end of calendar year of death","runs from the END OF THE YEAR of death, not the date of death"),
 ("NCB-D-003","Under Nigerian law, a composer wrote a piece of music that was never published before he died in 2018. Does copyright still run, and for how long?","19(1)(a)",
  "US 17 USC 302(a) applies regardless of publication; UK CDPA s.12(2)","70 years after the end of the year in which the author dies"),
 ("NCB-D-004","Under Nigerian law, two Abuja writers co-wrote a book. One died in 2000 and the other in 2019. How is the term worked out?","19(3)",
  "US 17 USC 302(b) last surviving author; UK CDPA s.12(8)","reference to the death of the author shall be to the author who dies last"),

 # ---- Ideas / fixation / eligibility: s.2, s.3 (5) ----
 ("NCB-D-005","Under Nigerian law, I explained a detailed plot idea for a Nollywood film to a producer, who then made a film on the same idea. Does copyright protect the idea itself?","3(a)",
  "US 17 USC 102(b) no protection for ideas, procedures, concepts; UK common law equivalent","ideas, procedures, processes, formats, systems, methods of operation, concepts, principles, discoveries or mere data"),
 ("NCB-D-006","Under Nigerian law, I improvised a melody aloud in a Lagos studio session and it was never written down or recorded. Is it protected?","2(2)(b)",
  "US 17 USC 102(a) requires fixation in a tangible medium; UK CDPA s.3(2) recording requirement","fixed in any medium of expression known or later to be developed, from which it can be perceived, reproduced or otherwise communicated"),
 ("NCB-D-007","Under Nigerian law, a critic said my short story is poorly written and has no literary merit. Does the standard of the work affect whether it is protected?","2(3)",
  "US: no merit requirement (Bleistein v Donaldson); UK CDPA: originality not artistic quality","notwithstanding the QUALITY of the work or the purpose for which the work was created"),
 ("NCB-D-008","Under Nigerian law, does a mere alphabetical list of raw data with no selection or arrangement effort attract protection?","3(a)+2(2)(a)",
  "US 17 USC 102(b) + Feist: mere data not protected absent original selection; UK similar","some effort has been expended on making the work, to give it an ORIGINAL CHARACTER"),
 ("NCB-D-009","Under Nigerian law, I compiled a directory using publicly available data. Does my copyright in the compilation give me rights over the underlying data?","2(5)",
  "US 17 USC 103(b) compilation copyright does not extend to preexisting material; UK equivalent","copyright in a compilation shall NOT confer any exclusive right in the pre-existing material or data"),

 # ---- First ownership: s.28(1) (3) ----
 ("NCB-D-010","Under Nigerian law, a freelance illustrator in Ibadan drew a book cover on her own initiative with no contract in place. Who owns the copyright?","28(1)",
  "US 17 USC 201(a) vests in author; UK CDPA s.11(1) author is first owner","copyright shall INITIALLY VEST in the author, except as otherwise provided in an agreement"),
 ("NCB-D-011","Under Nigerian law, a photographer took photographs at a public event entirely on his own account, with no agreement with anyone. Who is the first owner of copyright?","28(1)",
  "US 17 USC 201(a); UK CDPA s.11(1)","initially vest in the author"),
 ("NCB-D-012","Under Nigerian law, a songwriter and a producer signed a written agreement saying the producer owns the copyright in a track. Does that agreement displace the default rule?","28(1)",
  "US 17 USC 201(d) transfer by written agreement; UK CDPA s.11(1) subject to agreement","EXCEPT AS OTHERWISE PROVIDED IN AN AGREEMENT, copyright shall initially vest in the author"),

 # ---- Writing requirement for assignment: s.30(3) (4) ----
 ("NCB-D-013","Under Nigerian law, a Lagos publisher says I assigned him copyright in my novel during a phone conversation. Is a spoken assignment effective?","30(3)",
  "US 17 USC 204(a) transfer requires signed writing; UK CDPA s.90(3) assignment requires signed writing","an assignment of copyright shall have NO EFFECT unless it is in writing"),
 ("NCB-D-014","Under Nigerian law, a producer claims he holds an exclusive licence to my beat based on a verbal agreement we had. Is that enforceable?","30(3)",
  "US 17 USC 101/204(a) exclusive licence is a transfer requiring writing; UK CDPA s.92(1)","an assignment of copyright OR AN EXCLUSIVE LICENCE ... shall have no effect unless it is in writing"),
 ("NCB-D-015","Under Nigerian law, can I assign copyright in my song to a label for a limited period rather than permanently?","30(2)",
  "US 17 USC 201(d)(2) divisibility; UK CDPA s.90(2) partial assignment","may be limited to only some of the acts ... or to a PART ONLY of the period of the copyright, or to a specified country"),
 ("NCB-D-016","Under Nigerian law, when I die, can my copyright in my books pass to my children under my will?","30(1)",
  "US 17 USC 201(d)(1) transfer by will; UK CDPA s.90(1) transmissible by testamentary disposition","copyright shall be deemed to be MOVABLE PROPERTY and transferable by way of assignment, testamentary disposition or operation of law"),

 # ---- Accessible formats (Marrakesh - both implement): s.26 (4) ----
 ("NCB-D-017","Under Nigerian law, a registered Nigerian non-profit that provides reading services to blind people, and which has lawfully bought a copy of a published novel, wants to produce a braille version and supply it free to blind readers. Does it need the publisher's permission?","26(1)",
  "US 17 USC 121/121A (Marrakesh implementation); UK CDPA s.31A-31F","an AUTHORISED ENTITY may, WITHOUT the permission of the owner, make or procure an ACCESSIBLE FORMAT COPY ... on a non-profit basis"),
 ("NCB-D-018","Under Nigerian law, a blind reader in Kano who has lawfully bought an ebook wants to convert it into a format her screen reader can handle, for her own use. Is she allowed to do that herself?","26(3)",
  "US 17 USC 121A; UK CDPA s.31B personal copies for disabled persons","a BENEFICIARY PERSON is permitted to make an accessible format copy ... for HIS PERSONAL USE, where he has lawful access"),
 ("NCB-D-019","Under Nigerian law, my elderly father is blind and has lawfully bought a printed book. As his carer, may I make an audio version for him?","26(4)",
  "US 17 USC 121A; UK CDPA s.31B(2) person acting on behalf","a person acting on behalf of a beneficiary person, INCLUDING A PRIMARY CARETAKER OR CAREGIVER, may assist"),
 ("NCB-D-020","Under Nigerian law, a Nigerian non-profit serving blind readers has made accessible copies. A registered non-profit in Ghana that also serves blind readers, and which it has no reason to think will misuse them, asks for copies. May it send them?","26(5)",
  "US 17 USC 121A(b) cross-border export; UK CDPA s.31E - both implement Marrakesh Art.5","may distribute or make available accessible format copies TO AN AUTHORISED ENTITY IN ANOTHER COUNTRY ... provided it did not know or have reasonable grounds to know the copy would be misused"),
]

OVERLAP = {"NCB-D-001","NCB-D-004","NCB-D-006","NCB-D-009","NCB-D-012",
           "NCB-D-014","NCB-D-017","NCB-D-020"}

Path("data/eval").mkdir(parents=True, exist_ok=True)
Path("docs").mkdir(exist_ok=True)

internal = [{"item_id": i, "question": q, "expected_provision": p,
             "category": "control", "jurisdiction_cue": "named",
             "convergence_basis": cb, "nigerian_phrasing": np,
             "scored_on": ["answer_correct","citation_correct","phrasing_nigerian_or_foreign"],
             "double_annotated": i in OVERLAP}
            for i, q, p, cb, np in ITEMS]
Path("data/eval/catD_internal.jsonl").write_text(
    "\n".join(json.dumps(x, ensure_ascii=False) for x in internal) + "\n", encoding="utf-8")

with open("docs/catD_annotation_sheet.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["item_id","question","governing_provision","answer","confidence","notes"])
    for i, q, *_ in ITEMS:
        w.writerow([i, q, "", "", "", ""])

dur = sum(1 for i,q,*_ in ITEMS if "how long" in q.lower() or "period" in q.lower() or "term" in q.lower())
print(f"{len(ITEMS)} items | {len(OVERLAP)} double-annotated")
print(f"duration-ish items: {dur}/{len(ITEMS)} ({100*dur/len(ITEMS):.0f}%)")
print("all have convergence_basis:", all(cb for *_, cb, _ in ITEMS))
print("all have nigerian_phrasing:", all(np for *_, np in ITEMS))
print("internal   -> data/eval/catD_internal.jsonl")
print("to lawyers -> docs/catD_annotation_sheet.csv")
