import json, csv
from pathlib import Path
from collections import Counter

# (id, question, expected_provision, divergence_type, foreign_default)
# foreign_default: dict or None. None = STILL NEEDS SOURCING before M3 can run.
ITEMS = [
 # ---------- Part VII: takedown / service providers (15) : STRUCTURAL ----------
 ("NCB-C-001","Under Nigerian law, my song was uploaded to a Lagos-based streaming platform without my permission. What must I actually put in the notice I send them?","54(2)","structural",None),
 ("NCB-C-002","Under Nigerian law, I sent a takedown notice by email to a Nigerian platform. They say it is invalid because it was not delivered on paper. Are they right?","54(2)","structural",None),
 ("NCB-C-003","Under Nigerian law, someone knowingly filed a false takedown claim against my YouTube channel and my video was pulled. Do I have any remedy against them?","57","structural",None),
 ("NCB-C-004","Under Nigerian law, a Nigerian platform has received my takedown notice about a pirated film. What steps must it take, and who must it tell?","55(1)","structural",None),
 ("NCB-C-005","Under Nigerian law, the person who uploaded my track sent the platform a counter-notice. How long do I have to reply before they can put it back up?","55(2)(b)","structural",
    {"US":"provider must restore the material not less than 10 nor more than 14 BUSINESS days after the counter notice, unless the rightsholder has FILED A COURT ACTION to restrain the subscriber (17 U.S.C. 512(g)(2)(B)-(C))"}),
 ("NCB-C-006","Under Nigerian law, a platform removed my pirated album but the same file was uploaded again a week later. Does the platform have any duty to stop that happening?","55(3)","structural",None),
 ("NCB-C-007","Under Nigerian law, I am unhappy with how a Nigerian platform handled my copyright complaint. Is going to court my only option?","55(4)","structural",None),
 ("NCB-C-008","Under Nigerian law, a Nigerian hosting company received my takedown notice three months ago and has done nothing. What is the company exposed to?","55(6)","structural",None),
 ("NCB-C-009","Under Nigerian law, a user keeps re-uploading my films to a Nigerian platform and I have reported it repeatedly. At what point must the platform suspend that account?","56(1)(b)","structural",None),
 ("NCB-C-010","Under Nigerian law, my account on a Nigerian platform was suspended over copyright complaints I believe were about someone else. How long do I have to object, and who decides?","56(2)","structural",None),
 ("NCB-C-011","Under Nigerian law, a Nigerian platform suspended a repeat infringer account. Is there a minimum period the suspension must run?","56(1)(b)","structural",None),
 ("NCB-C-012","Under Nigerian law, I run a Nigerian file-hosting service and users upload material I never review. What must I do to avoid being liable for infringing uploads?","58","structural",None),
 ("NCB-C-013","Under Nigerian law, my Nigerian website only lists links to other sites, some of which turn out to host pirated films. Am I liable simply for linking?","59","structural",None),
 ("NCB-C-014","Under Nigerian law, I run a Nigerian social platform. Is there anything I must publish on my website before I can rely on the liability protections?","62(1)(b)(ii)","structural",None),
 ("NCB-C-015","Under Nigerian law, a website is distributing pirated Nollywood films. Can it be blocked without anyone going to court first?","61","no_analogue",None),

 # ---------- Folklore (8) + levy (4) : NO-ANALOGUE ----------
 ("NCB-C-016","Under Nigerian law, my band sampled a traditional Yoruba folk song on a track we are releasing commercially. Do we need anyone's permission?","74(1)+74(4)","no_analogue",None),
 ("NCB-C-017","Under Nigerian law, if permission is needed to use a Nigerian folk song commercially, who grants it - the community it came from, or some other body?","74(4)","no_analogue",None),
 ("NCB-C-018","Under Nigerian law, does protection for traditional folk expressions ever expire, the way copyright in a book does?","74","no_analogue",None),
 ("NCB-C-019","Under Nigerian law, a lecturer at a Nigerian university used traditional folk riddles in a classroom lesson. Was permission required?","74(2)(b)","no_analogue",None),
 ("NCB-C-020","Under Nigerian law, a novelist took motifs from Igbo folk tales and wrote an original novel around them. Is that permitted?","74(2)(d)","no_analogue",None),
 ("NCB-C-021","Under Nigerian law, I am publishing a book that quotes a traditional folk song. Is there anything I am required to state about its origin?","74(3)","no_analogue",None),
 ("NCB-C-022","Under Nigerian law, are traditional Nigerian textile patterns and wood carvings covered by any protection?","74(5)(d)","no_analogue",None),
 ("NCB-C-023","Under Nigerian law, a Nollywood production filmed a traditional folk dance for a commercial feature without asking anyone. Is folk dance covered?","74(5)(c)","no_analogue",None),
 ("NCB-C-024","Under Nigerian law, I import blank discs and duplicating equipment for my Lagos business. Is any levy payable on them?","89(1)","no_analogue",None),
 ("NCB-C-025","Under Nigerian law, who sets the amount of the copyright levy, and by what instrument?","89(2)","no_analogue",None),
 ("NCB-C-026","Under Nigerian law, once the copyright levy is collected, where does the money go and who can receive it?","89(3)","no_analogue",None),
 ("NCB-C-027","Under Nigerian law, does the copyright levy reach digital and electronic systems, or only physical items like blank discs?","89(5)","no_analogue",None),

 # ---------- Exceptions ss.21-26 (18) : SUBSTITUTIVE ----------
 ("NCB-C-028","Under Nigerian law, a teacher at a Lagos secondary school used the school photocopier to copy textbook pages for her class. Was that permitted?","21(1)","substitutive",
    {"US":"no equivalent categorical bar on reprographic copying; classroom copying is assessed under the open-ended fair use factors (17 U.S.C. 107)"}),
 ("NCB-C-029","Under Nigerian law, a lecturer wrote out a passage from a published poem on the whiteboard while teaching. Did that infringe?","21(1)","substitutive",None),
 ("NCB-C-030","Under Nigerian law, a private tutorial centre in Abuja that operates for profit copied part of a film to use in a lesson. Can it rely on the teaching exception?","21(2)","substitutive",None),
 ("NCB-C-031","Under Nigerian law, an examiner reproduced several lines of a published poem inside an examination paper. Was the poet's permission needed?","21(3)","substitutive",None),
 ("NCB-C-032","Under Nigerian law, a Nigerian polytechnic recorded a television documentary off air to show in class. Was that allowed?","22(1)","substitutive",None),
 ("NCB-C-033","Under Nigerian law, a Nigerian school records television programmes for teaching. A licensing body now offers a scheme covering exactly that. Does the school still have a free hand?","22(2)","substitutive",None),
 ("NCB-C-034","Under Nigerian law, a Nigerian university wants to photocopy from a published textbook for teaching. How much may it copy, and how often?","23(2)","substitutive",
    {"US":"no fixed statutory percentage; extent of copying is one of four fair use factors (17 U.S.C. 107(3)) with no bright-line limit"}),
 ("NCB-C-035","Under Nigerian law, a publisher's licence agreement tells our Nigerian college we may copy no more than two per cent of any book. Is that term enforceable against us?","23(4)","substitutive",None),
 ("NCB-C-036","Under Nigerian law, our Nigerian university already pays an annual licence fee to a copyright body for photocopying. Does that change what we may copy without permission?","23(3)","substitutive",None),
 ("NCB-C-037","Under Nigerian law, a student at a Lagos university sold me photocopied course material his department had produced for teaching. Is the copy I bought a lawful one?","24(1)","substitutive",None),
 ("NCB-C-038","Under Nigerian law, someone gave false information on a request form to obtain a copy of a work from a Nigerian library. Who bears the liability?","24(2)","substitutive",None),
 ("NCB-C-039","Under Nigerian law, a Nigerian museum wants to digitise its collection purely for preservation and back-up. Must it clear that with rightsholders first?","25(1)(b)","substitutive",None),
 ("NCB-C-040","Under Nigerian law, a Nigerian library has tried hard but cannot trace the owner of an out-of-print book it holds. May it make a copy anyway?","25(1)(e)","no_analogue",
    {"US":"no general orphan works exception; repeated legislative proposals were not enacted, so use without permission is assessed only under 17 U.S.C. 107"}),
 ("NCB-C-041","Under Nigerian law, a Nigerian university library has a volume with pages missing. Can it obtain the missing part from another institution's copy?","25(1)(c)","substitutive",None),
 ("NCB-C-042","Under Nigerian law, a Nigerian archive made preservation copies of works in its collection. May it lend those copies to users?","25(2)(a)","substitutive",None),
 ("NCB-C-043","Under Nigerian law, a service provider acted in good faith when taking content down after a notice. Can the uploader sue it for the removal?","55(5)","structural",None),
 ("NCB-C-044","Under Nigerian law, I want the platform to tell me who uploaded my pirated film so I can sue them. Can I simply ask the platform for the name?","60(1)+60(2)","structural",None),
 ("NCB-C-045","Under Nigerian law, someone distorted a traditional folk song in a way the originating community finds deeply offensive, and sold the recording. Is that an offence?","76(1)(c)","no_analogue",None),
]

OVERLAP = {"NCB-C-005","NCB-C-006","NCB-C-011","NCB-C-015","NCB-C-017",
           "NCB-C-018","NCB-C-021","NCB-C-024","NCB-C-027","NCB-C-028",
           "NCB-C-034","NCB-C-035","NCB-C-040","NCB-C-044","NCB-C-045"}

Path("data/eval").mkdir(parents=True, exist_ok=True)
Path("docs").mkdir(exist_ok=True)

internal = [{"item_id": i, "question": q, "expected_provision": p,
             "category": "divergence", "divergence_type": d,
             "jurisdiction_cue": "named", "foreign_default": fd,
             "foreign_default_sourced": fd is not None,
             "double_annotated": i in OVERLAP}
            for i, q, p, d, fd in ITEMS]
Path("data/eval/catC_internal.jsonl").write_text(
    "\n".join(json.dumps(x, ensure_ascii=False) for x in internal) + "\n", encoding="utf-8")

with open("docs/catC_annotation_sheet.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["item_id","question","governing_provision","answer","confidence","notes"])
    for i, q, p, d, fd in ITEMS:
        w.writerow([i, q, "", "", "", ""])

print(f"{len(ITEMS)} items | {len(OVERLAP)} double-annotated")
print("divergence types:", dict(Counter(d for *_, d, _ in [(a,b,c,d,e) for a,b,c,d,e in ITEMS])))
sourced = sum(1 for *_, fd in ITEMS if fd)
print(f"foreign_default sourced: {sourced}/{len(ITEMS)}  <-- {len(ITEMS)-sourced} STILL NEED CITATIONS")
dur = sum(1 for _,q,*_ in ITEMS if "how long" in q.lower() and "year" in q.lower())
print(f"duration items: {dur}/{len(ITEMS)}")
print("internal   -> data/eval/catC_internal.jsonl")
print("to lawyers -> docs/catC_annotation_sheet.csv")
