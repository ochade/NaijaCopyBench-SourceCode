import json, csv
from pathlib import Path
from collections import Counter

# (id, question, provision, part, required_elements, prohibited_claims)
ITEMS = [
 ("NCB-F-001","I'm a Lagos-based writer and I keep hearing different things about what actually qualifies for copyright. Can you explain what does and doesn't get protected?","2+3","I",
  ["six categories: literary, musical, artistic, audiovisual, sound recordings, broadcasts",
   "effort giving original character required for literary/musical/artistic",
   "fixation in a medium required",
   "quality and purpose irrelevant",
   "ideas, procedures, concepts, mere data excluded",
   "official texts and state symbols excluded"],
  ["registration is required for protection","only published works qualify","a work must have artistic merit"]),

 ("NCB-F-002","I'm a musician and I've been told my songs are protected for different lengths of time depending on the format. How does that work?","19","I",
  ["literary/musical/artistic other than photographs: 70 years after end of year author dies",
   "sound recordings: 50 years from end of year first made available, or 50 from creation",
   "broadcasts: 50 years from end of year of broadcast",
   "audiovisual and photographs: 50 years",
   "anonymous/pseudonymous: 70 years from first availability"],
  ["all works get life plus 70","sound recordings get 95 years","terms run from the date of death rather than the end of that year"]),

 ("NCB-F-003","I teach at a Nigerian university and I want to know what my department can legally copy for students. What are the rules?","21+22+23","II",
  ["instruction copying allowed but NOT by reprographic process (s.21(1))",
   "audiovisual/sound recording copying limited to non-profit educational institutions",
   "examination use permitted",
   "reprographic copying by educational establishments allowed up to 5% in three months",
   "these do not apply where a licensing scheme exists",
   "licence terms purporting to allow less than the statutory proportion are void"],
  ["the four-factor fair use test governs","any educational use is permitted","there is no numerical limit"]),

 ("NCB-F-004","I'm a songwriter about to sign my first publishing deal. What should I know about how copyright can be transferred?","30","III",
  ["copyright is movable property, transferable by assignment, will, or operation of law",
   "assignment or exclusive licence has no effect unless in writing",
   "non-exclusive licence may be written, oral, or inferred from conduct",
   "assignment may be limited by acts, period, or territory"],
  ["all licences must be in writing","assignment must be notarised or registered","copyright cannot be left in a will"]),

 ("NCB-F-005","Someone is pirating my textbook. Before I go to a lawyer, what counts as infringement and what can I actually claim?","36+37","IV",
  ["doing an act violating the exclusive rights, without authorisation",
   "importing infringing copies into Nigeria",
   "selling or offering infringing copies",
   "possessing equipment used solely for making infringing copies",
   "permitting premises for infringing public performance, subject to the knowledge defence",
   "must relate to the whole or a substantial part",
   "reliefs include damages, injunction, accounts",
   "innocent infringement: no damages but account of profits available"],
  ["statutory damages are available","registration is a precondition to suing","any copying however small is infringement"]),

 ("NCB-F-006","I run a small Nigerian streaming site. If users upload pirated content, what do I have to do and when am I on the hook?","54+55+58","VII",
  ["owner may send a notice; the notice must meet specified contents including a declaration on oath",
   "provider must notify the subscriber and expeditiously take down, then notify the owner",
   "provider may restore if a counter-notice is forwarded and the owner does not respond within seven days",
   "provider must take steps to prevent the same content being reloaded",
   "no monetary liability if it lacks actual knowledge, gains no direct financial benefit, and acts expeditiously on notice",
   "failure to comply exposes it to liability for the infringement itself"],
  ["10 to 14 business days applies","the rightsholder must file a court action to prevent restoration","there is no obligation to prevent re-uploading"]),

 ("NCB-F-007","I'm a session musician and I'm not sure what rights I have in my own performances. Can you explain?","63","VIII",
  ["performers have rights in their performances under the Act"],
  ["performers have no separate rights, only the songwriter does"]),

 ("NCB-F-008","My family's community has traditional songs that a company wants to use commercially. What protection exists for that kind of material?","74","IX",
  ["expressions of folklore protected against reproduction, public communication, adaptation when for commercial purpose or outside traditional context",
   "the right to authorise vests in the Commission, not the community",
   "exceptions for private/domestic fair dealing, education, illustration, borrowing for an original work, incidental use",
   "source community or place must be indicated in publications",
   "covers folk songs, dances, riddles, and folk art including textiles and carvings"],
  ["folklore is public domain","permission comes from the community itself","protection expires after a fixed term"]),

 ("NCB-F-009","I want to start a royalty collection body for Nigerian producers. What does the law require?","88","X",
  ["must apply to the Commission for approval to operate",
   "approval conditions include incorporation as a company limited by guarantee, stated objects, representing a substantial number of owners, compliance with regulations",
   "the Commission shall not approve a second CMO in a category already adequately served",
   "operating without approval is prohibited and an offence",
   "the Commission may suspend or revoke approval and review tariffs"],
  ["no government approval is needed","multiple competing bodies may operate freely in the same category"]),

 ("NCB-F-010","I'm a publisher and I've heard there's a levy on copying equipment in Nigeria. What is it and who pays?","89","X",
  ["a levy is payable on material used or capable of being used to infringe copyright",
   "the amount and exemptions are prescribed by the Minister by order",
   "proceeds go into the Commission's Fund and may be disbursed to approved CMOs",
   "material includes electronic and digital systems, not only physical media"],
  ["there is no levy in Nigeria","the levy is set by the Commission alone","it applies only to blank discs and tapes"]),

 ("NCB-F-011","I run a Nigerian library. What are we allowed to do with works in our collection without asking permission?","25","II",
  ["applies to archives, libraries, museums and galleries for non-commercial purposes",
   "making and distributing copies as part of ordinary activities",
   "back-up and preservation copies",
   "obtaining a missing part from another institution",
   "copying where the work cannot reasonably be acquired in a needed format",
   "copying where the owner cannot be traced after reasonable effort",
   "copies may be lent or used for private study on the premises"],
  ["libraries need a licence for all copying","there is no provision for untraceable owners"]),

 ("NCB-F-012","I'm a blind reader in Nigeria and I want to know what I and organisations serving me are allowed to do with published books.","26","II",
  ["an authorised entity may make and supply accessible format copies without permission, on a non-profit basis, with lawful access",
   "a beneficiary person may make an accessible copy for personal use",
   "a caregiver may assist",
   "cross-border sending to an authorised entity abroad is permitted subject to good faith",
   "definitions of authorised entity and beneficiary person"],
  ["permission from the publisher is always required","only registered organisations may make copies, never individuals"]),

 ("NCB-F-013","I'm registering a work with the Copyright Commission. What does registration actually do for me?","87","X",
  ["the Commission maintains a Register of Works",
   "a person may apply to register an eligible work",
   "registration does NOT confer copyright",
   "the Register is evidence of the work and its particulars; certified extracts are admissible",
   "false entries are an offence"],
  ["registration creates the copyright","registration is required before suing","unregistered works are unprotected"]),

 ("NCB-F-014","I want to translate a Nigerian textbook for teaching but the publisher won't respond. Is there any route open to me?","31+34","III",
  ["a qualified person may apply to the Commission for a licence to translate for teaching, scholarship or research",
   "qualified person means a Nigerian citizen, habitual resident, or a body corporate incorporated in Nigeria",
   "application in prescribed form stating proposed retail price, with a fee",
   "the licence is non-exclusive and subject to royalty conditions",
   "research excludes industrial or commercial corporate research"],
  ["anyone anywhere may apply","no royalty is payable","the licence is exclusive"]),

 ("NCB-F-015","I'm a photographer and clients keep assuming they own the pictures because they paid me. Who actually owns copyright in different situations?","28+29","III",
  ["copyright initially vests in the author unless an agreement says otherwise",
   "works made under a contract for services or in government employment vest in that government body",
   "private and domestic commissions: the commissioner gets a non-exclusive licence for non-commercial use and may restrain publication",
   "collective works vest in the person on whose initiative they were created",
   "contributors to a collective work may exploit their own contributions independently"],
  ["whoever pays owns the copyright","commissioned photographs always belong to the client"]),

 ("NCB-F-016","Someone edited my artwork for an advert in a way I find humiliating, and left my name off it. Do I have anything beyond the copyright I already sold?","14","I",
  ["right to claim authorship and be identified",
   "right to object to distortion, mutilation or derogatory treatment prejudicial to honour or reputation",
   "right to object to false attribution",
   "these rights are not transmissible during the author's life",
   "they pass on death by testamentary disposition"],
  ["moral rights are lost when copyright is assigned","Nigeria has no moral rights"]),

 ("NCB-F-017","A pirate website is selling my films. Apart from suing the seller, is there anything that can be done about the site itself?","60+61","VII",
  ["the owner may apply to court for an order requiring a service provider to identify an alleged infringer",
   "the application must include a copy of the takedown notification and a sworn declaration",
   "the Commission may directly block or disable access to infringing content, links or websites"],
  ["only a court can order blocking","there is no administrative blocking power"]),

 ("NCB-F-018","I'm being taken to court over copyright and I want to understand where the case goes and what the other side has to prove.","103+37+43","XII",
  ["the Federal High Court has exclusive jurisdiction over offences and civil actions under the Act",
   "action lies at the instance of the owner, assignee or exclusive licensee",
   "where both owner and exclusive licensee have concurrent rights, one may not proceed without joining the other, absent leave",
   "registration under the Act raises presumptions in an infringement action"],
  ["State High Courts have concurrent jurisdiction","any licensee may sue"]),

 ("NCB-F-019","I'm a Nollywood producer. What exactly can I stop other people doing with my film?","11","I",
  ["reproduce the audiovisual work",
   "cause it to be seen or heard in public",
   "communicate it to the public",
   "broadcast it",
   "copy the soundtrack",
   "make it available on demand",
   "distribute copies commercially",
   "make adaptations"],
  ["the producer's rights are the same as those in a literary work"]),

 ("NCB-F-020","I make radio programmes for a Nigerian station. What rights does the station have in what we broadcast?","13","I",
  ["rebroadcasting",
   "communication to the public of the broadcast",
   "making it available on demand",
   "fixation of the broadcast",
   "reproduction of a fixation",
   "adaptation of a fixation",
   "commercial distribution of a fixation",
   "television broadcasts include control over still photographs taken from the broadcast"],
  ["broadcasters have no rights separate from the underlying works"]),
]

OVERLAP = {"NCB-F-002","NCB-F-003","NCB-F-006","NCB-F-008","NCB-F-013","NCB-F-015"}

Path("data/eval").mkdir(parents=True, exist_ok=True)
Path("docs").mkdir(exist_ok=True)

internal = [{"item_id": i, "question": q, "category": "summarization",
             "expected_provision": p, "part": pt,
             "jurisdiction_cue": "contextual",
             "required_elements": req, "prohibited_claims": proh,
             "double_annotated": i in OVERLAP}
            for i, q, p, pt, req, proh in ITEMS]
Path("data/eval/catF_internal.jsonl").write_text(
    "\n".join(json.dumps(x, ensure_ascii=False) for x in internal) + "\n", encoding="utf-8")

with open("docs/catF_annotation_sheet.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["item_id","question","governing_provisions",
                "required_elements_any_correct_summary_must_contain",
                "common_errors_that_would_be_wrong","confidence","notes"])
    for i, q, *_ in ITEMS:
        w.writerow([i, q, "", "", "", "", ""])

print(f"{len(ITEMS)} items | {len(OVERLAP)} double-annotated")
print("by Part:", dict(Counter(pt for *_, pt, _, _ in [(a,b,c,d,e,f_) for a,b,c,d,e,f_ in ITEMS])))
print("cue: contextual (all)")
print("internal   -> data/eval/catF_internal.jsonl")
print("to lawyers -> docs/catF_annotation_sheet.csv")
