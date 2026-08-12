import json, csv
from pathlib import Path

# item_id, question, expected_chain (INTERNAL ONLY)
ITEMS = [
 ("NCB-B-001","A federal agency produced a public health poster in 2019 as part of its work. How long does copyright in it last under Nigerian law?","7 -> 19(1)(b)"),
 ("NCB-B-002","A ministry employee wrote a training manual in the course of employment and died in 2015. From what date is the copyright term counted?","28(2) -> 19(1)(b)"),
 ("NCB-B-003","I want to quote several paragraphs from a Nigerian novel in a non-commercial research paper. Is that allowed?","9(a) -> 20(1)(c)"),
 ("NCB-B-004","A Lagos comedian made a parody of a popular Afrobeats song. Does the songwriter permission matter?","9 -> 20(1)(b)"),
 ("NCB-B-005","A newspaper reproduced part of my article while reporting a news event without asking. Is there anything they must do to rely on that?","9 -> 20(1)(d)"),
 ("NCB-B-006","A documentary filmed a public sculpture in Abuja that appears in several shots. Does the sculptor permission matter?","10 -> 20(1)(e)"),
 ("NCB-B-007","A TV station news report incidentally captured a mural on a building wall. Is that infringement?","10 -> 20(1)(f)"),
 ("NCB-B-008","Someone recorded a snippet of my podcast episode for private listening at home. Which of my rights is engaged and does an exception apply?","12 -> 20(1)(a)"),
 ("NCB-B-009","A Kano radio station broadcast my song without a licence. Which right has been affected, and is that infringement?","9(g) -> 36(a)"),
 ("NCB-B-010","A cable operator retransmitted a Nigerian TV station live broadcast without permission. Whose right is infringed?","13(1)(a) -> 36(a)"),
 ("NCB-B-011","Someone took still photographs off a Nigerian television broadcast and sold them. Is that covered by the broadcaster rights?","13(2) -> 36(a)"),
 ("NCB-B-012","A streaming site put my album online so listeners can play it whenever they want. Which specific right does that engage?","12(d) -> 36(a)"),
 ("NCB-B-013","A shop rents out copies of my film to customers for a fee. Which right is that, and is it infringement?","11(g)/12(e) -> 36(a)"),
 ("NCB-B-014","A publisher printed my essay but left my name off it entirely. Do I have a claim under Nigerian law even though I sold them the copyright?","14(1)(a) + 14(3)(a) -> 9"),
 ("NCB-B-015","Someone heavily edited my painting for an advert in a way I find humiliating. Do I have any right left after selling the work?","14(1)(b) -> 10"),
 ("NCB-B-016","A magazine published a poem under my name that I did not write. Does Nigerian copyright law give me any remedy?","14(2)"),
 ("NCB-B-017","I am a Kenyan national living in Kenya. Can I apply to the Commission for a licence to translate a Nigerian textbook for teaching?","34(1) -> 31"),
 ("NCB-B-018","My company is incorporated in Nigeria. Can it apply for a licence to translate a published literary work for scholarship?","34(1)(b) -> 31(1)"),
 ("NCB-B-019","A pharmaceutical company wants to translate a technical text for its own commercial research. Does that count as research for the compulsory licence?","34(2) -> 31(1)"),
 ("NCB-B-020","A Nigerian broadcaster wants to translate an educational text for a teaching programme. Is there a route to do that without the owner consent?","33(1) -> 31"),
 ("NCB-B-021","A textbook edition has not been on sale in Nigeria for eight months. Can a Nigerian publisher get permission to reprint it for schools?","32(1)(b) -> 34(1)"),
 ("NCB-B-022","I wrote detailed notes describing how a new mobile app would work. When does copyright begin in what I have made?","3(a) -> 18"),
 ("NCB-B-023","I improvised a guitar solo at a Lagos show; nobody recorded it. Has copyright started?","2(2)(b) -> 18"),
 ("NCB-B-024","I have a written non-exclusive licence to publish a novel. Can I sue someone who pirates it?","30(4) -> 37(1)"),
 ("NCB-B-025","I am the copyright owner and I have also granted an exclusive licence. If I sue alone, is there a procedural requirement?","37(3) -> 30(3)"),
]

# double-annotated subset (both lawyers) - ~1/3, spread across chain types
OVERLAP = {"NCB-B-001","NCB-B-003","NCB-B-006","NCB-B-010","NCB-B-014",
           "NCB-B-017","NCB-B-019","NCB-B-024"}

Path("data/eval").mkdir(parents=True, exist_ok=True)
Path("docs").mkdir(exist_ok=True)

internal = [{"item_id": i, "question": q, "expected_chain": c,
             "category": "multi_hop", "double_annotated": i in OVERLAP}
            for i, q, c in ITEMS]
Path("data/eval/catB_internal.jsonl").write_text(
    "\n".join(json.dumps(x, ensure_ascii=False) for x in internal) + "\n", encoding="utf-8")

with open("docs/catB_annotation_sheet.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["item_id","question","governing_provision","answer","confidence","notes"])
    for i, q, c in ITEMS:
        w.writerow([i, q, "", "", "", ""])

print(f"{len(ITEMS)} items, {len(OVERLAP)} double-annotated")
print("internal   -> data/eval/catB_internal.jsonl")
print("to lawyers -> docs/catB_annotation_sheet.csv")
