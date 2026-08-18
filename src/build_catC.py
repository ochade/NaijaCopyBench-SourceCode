"""Category C: divergence items with foreign_default sourced from primary text.
Sources: US Title 17 (Circular 92, Dec 2025); UK CDPA 1988 (revised to 03/08/2026).
Each entry: (id, question, expected_provision, divergence_type, foreign_default).
A self-check at the bottom asserts each foreign_default cites a provision
consistent with the item it belongs to.
"""
import json, csv, re
from pathlib import Path
from collections import Counter

# --- reusable boilerplate ---
UK_NO_TAKEDOWN = ("CDPA 1988 contains no notice-and-takedown or safe-harbour regime; "
    "UK intermediary liability limits derive from the Electronic Commerce (EC Directive) "
    "Regulations 2002, regs 17-19, which sit outside the Act.")
US_NO_FOLKLORE = ("No provision found in 17 USC on search for 'folklore', 'traditional', "
    "'expressions of folklore'. US federal copyright has no sui generis folklore protection.")
UK_FOLKLORE = ("CDPA 1988 s.169 'Folklore, &c.: anonymous unpublished works' is NOT a sui "
    "generis folklore right. It creates a PRESUMPTION that the author of an unpublished work "
    "of unknown authorship qualified for copyright, and empowers designation by Order in "
    "Council of a FOREIGN BODY appointed under another country's law (s.169(2)-(3)). It is "
    "the RECEIVING END of a regime like Nigeria's, not an equivalent.")
US_LEVY = ("17 USC ch.10 (Audio Home Recording Act) imposes royalties ONLY on 'digital audio "
    "recording devices/media', defined at 1001(3)-(4) as devices whose digital recording "
    "function is designed or marketed PRIMARILY for making digital audio copies for private "
    "use. EXPRESSLY EXCLUDES professional models, dictation machines, and media primarily "
    "used for copying motion pictures, audiovisual works, or non-musical literary works "
    "including computer programs. NO general levy on infringement-capable equipment.")
UK_LEVY = ("No provision found in CDPA 1988 on search for 'levy', 'blank media' or "
    "'private copying'. The UK has no private copying levy.")

ITEMS = [
 # ---------- Part VII: takedown / service providers (15) : STRUCTURAL ----------
 ("NCB-C-001","Under Nigerian law, my song was uploaded to a Lagos-based streaming platform without my permission. What must I actually put in the notice I send them?","54(2)","structural",
  {"US":"17 USC 512(c)(3)(A): six elements - signature; identification of the work; identification of the material; contact information; a good-faith-belief statement (clause v); and a statement that the notice is accurate and, UNDER PENALTY OF PERJURY, that the sender is authorised (clause vi).","UK":UK_NO_TAKEDOWN}),
 ("NCB-C-002","Under Nigerian law, when I send a takedown notice about my film, which part of what I say has to be sworn - my belief that the use is unauthorised, or my authority to act for the owner?","54(2)(e)+54(2)(f)","structural",
  {"US":"17 USC 512(c)(3)(A): the PENALTY OF PERJURY attaches ONLY to the statement of AUTHORITY TO ACT (clause vi). The good-faith belief that the use is unauthorised (clause v) is a separate, UNSWORN statement.","UK":UK_NO_TAKEDOWN,"note":"Nigeria s.54(2)(e) swears the BELIEF; s.54(2)(f) leaves accuracy/authority unsworn. The US swears the opposite element."}),
 ("NCB-C-003","Under Nigerian law, someone knowingly filed a false takedown claim against my YouTube channel and my video was pulled. Do I have any remedy against them?","57","structural",
  {"US":"17 USC 512(f): knowing material misrepresentation gives damages INCLUDING COSTS AND ATTORNEYS' FEES to the alleged infringer, ANY copyright owner or licensee, OR THE SERVICE PROVIDER. Nigeria s.57 gives damages only to 'the person' injured by the provider's reliance - narrower class, no costs or fees.","UK":UK_NO_TAKEDOWN}),
 ("NCB-C-004","Under Nigerian law, a Nigerian platform has received my takedown notice about a pirated film. What steps must it take, and who must it tell?","55(1)","structural",
  {"US":"17 USC 512(c)(1)(C) requires expeditious removal on notice; 512(g)(2)(A) requires reasonable steps to notify the subscriber. No statutory ORDER of steps is prescribed, and no duty to notify the OWNER afterwards. Nigeria s.55(1) prescribes a sequence and requires notifying the owner.","UK":UK_NO_TAKEDOWN}),
 ("NCB-C-005","Under Nigerian law, the person who uploaded my track sent the platform a counter-notice. How long do I have to reply before they can put it back up?","55(2)(b)","structural",
  {"US":"17 USC 512(g)(2)(B)-(C): provider tells the notifier it will replace the material in 10 business days, then replaces it not less than 10 nor more than 14 BUSINESS days after the counter notice, UNLESS the notifier has FILED A COURT ACTION to restrain the subscriber. Nigeria s.55(2)(b) uses SEVEN days and requires only a RESPONSE, not litigation.","UK":UK_NO_TAKEDOWN}),
 ("NCB-C-006","Under Nigerian law, a platform removed my pirated album but the same file was uploaded again a week later. Does the platform have any duty to stop that happening?","55(3)","structural",
  {"US":"17 USC 512(m)(1) EXPRESSLY DISCLAIMS any monitoring duty: safe harbour is not conditioned on 'a service provider monitoring its service or affirmatively seeking facts indicating infringing activity'. NO stay-down obligation. Nigeria s.55(3) requires the OPPOSITE - effective steps to prevent reloading and removal without further notice. DIRECTLY OPPOSED POSITIONS.","UK":UK_NO_TAKEDOWN}),
 ("NCB-C-007","Under Nigerian law, I am unhappy with how a Nigerian platform handled my copyright complaint. Is going to court my only option?","55(4)","structural",
  {"US":"17 USC 512 provides NO administrative determination route: 512(h) subpoenas issue from a district court clerk and 512(j) injunctions from a court. Nigeria s.55(4) permits referral to the Commission for determination.","UK":UK_NO_TAKEDOWN}),
 ("NCB-C-008","Under Nigerian law, a Nigerian hosting company received my takedown notice three months ago and has done nothing. What is the company exposed to?","55(6)","structural",
  {"US":"17 USC 512(c)(1): a non-complying provider simply LOSES THE SAFE HARBOUR and faces ordinary secondary-liability analysis. Nigeria s.55(6) deems non-compliance a BREACH OF STATUTORY DUTY and makes the provider liable for the infringement to the SAME EXTENT as the person who posted the content.","UK":UK_NO_TAKEDOWN}),
 ("NCB-C-009","Under Nigerian law, a user keeps re-uploading my films to a Nigerian platform and I have reported it repeatedly. At what point must the platform suspend that account?","56(1)(b)","structural",
  {"US":"17 USC 512(i)(1)(A) requires only a 'policy that provides for the termination in appropriate circumstances' of repeat infringers - NO specified number of notifications. Nigeria s.56(1)(b) requires suspension after a SECOND notification on the same account.","UK":UK_NO_TAKEDOWN}),
 ("NCB-C-010","Under Nigerian law, my account on a Nigerian platform was suspended over copyright complaints I believe were about someone else. How long do I have to object, and who decides?","56(2)","structural",
  {"US":"17 USC 512(g)(3): a counter notification requires signature, identification of the removed material, a penalty-of-perjury statement of mistake or misidentification, contact details, AND consent to federal district court jurisdiction plus agreement to accept service of process. Nigeria s.56(2) sets a 10-day window and refers unresolved challenges to the Commission - no jurisdictional submission.","UK":UK_NO_TAKEDOWN}),
 ("NCB-C-011","Under Nigerian law, a Nigerian platform suspended a repeat infringer account. Is there a minimum period the suspension must run?","56(1)(b)","structural",
  {"US":"17 USC 512(i)(1)(A) specifies NO minimum suspension period; termination 'in appropriate circumstances' only. Nigeria s.56(1)(b) sets a minimum of ONE MONTH.","UK":UK_NO_TAKEDOWN}),
 ("NCB-C-012","Under Nigerian law, I run a Nigerian file-hosting service and users upload material I never review. What must I do to avoid being liable for infringing uploads?","58","structural",
  {"US":"17 USC 512(c)(1): no actual knowledge, no awareness of facts making infringement apparent, no direct financial benefit where the provider can control the activity, expeditious removal on notice; plus 512(c)(2) designated agent and 512(i) repeat-infringer policy. Nigeria s.58 mirrors the knowledge and financial-benefit conditions but ALSO requires compliance with the s.56 suspension procedure.","UK":UK_NO_TAKEDOWN}),
 ("NCB-C-013","Under Nigerian law, my Nigerian website only lists links to other sites, some of which turn out to host pirated films. Am I liable simply for linking?","59","structural",
  {"US":"17 USC 512(d) gives a SEPARATE safe harbour for information location tools - directory, index, reference, pointer, hypertext link - on substantially the 512(c) conditions. 512(d)(3) additionally requires the notice to identify THE REFERENCE OR LINK rather than the material. Nigeria s.59 is closely parallel but omits that refinement.","UK":UK_NO_TAKEDOWN}),
 ("NCB-C-014","Under Nigerian law, I run a Nigerian social platform. Is there anything I must publish on my website before I can rely on the liability protections?","62(1)(b)(ii)","structural",
  {"US":"17 USC 512(c)(2): the agent must be designated BOTH on the provider's website AND by providing the information to the Copyright Office, which maintains a public directory and may charge a fee. Nigeria s.62(1)(b)(ii) requires only website designation - no central registry.","UK":UK_NO_TAKEDOWN}),
 ("NCB-C-015","Under Nigerian law, a website is distributing pirated Nollywood films. Can it be blocked without anyone going to court first?","61","no_analogue",
  {"US":"No administrative blocking power in 17 USC. 512(j) permits INJUNCTIONS only, granted by a COURT, constrained to the least burdensome comparably effective relief (512(j)(2)(D)) and available only after notice to the provider and an opportunity to appear (512(j)(3)).","UK":"CDPA 1988 s.97A(1): 'The High Court (in Scotland, the Court of Session) shall have power to grant an injunction against a service provider, where that service provider has actual knowledge of another person using their service to infringe copyright.' JUDICIAL, not administrative.","note":"BOTH comparators require a COURT. Nigeria s.61 empowers the Commission to block DIRECTLY, notwithstanding any other law, on its own reasonable belief."}),

 # ---------- Folklore (8) + levy (4) : NO-ANALOGUE ----------
 ("NCB-C-016","Under Nigerian law, my band sampled a traditional Yoruba folk song on a track we are releasing commercially. Do we need anyone's permission?","74(1)+74(4)","no_analogue",{"US":US_NO_FOLKLORE,"UK":UK_FOLKLORE}),
 ("NCB-C-017","Under Nigerian law, if permission is needed to use a Nigerian folk song commercially, who grants it - the community it came from, or some other body?","74(4)","no_analogue",{"US":US_NO_FOLKLORE,"UK":UK_FOLKLORE}),
 ("NCB-C-018","Under Nigerian law, does protection for traditional folk expressions ever expire, the way copyright in a book does?","74","no_analogue",{"US":US_NO_FOLKLORE,"UK":UK_FOLKLORE,"note":"Nigeria s.74 specifies NO term - protection is perpetual. Both comparators tie any protection to ordinary copyright terms."}),
 ("NCB-C-019","Under Nigerian law, a lecturer at a Nigerian university used traditional folk riddles in a classroom lesson. Was permission required?","74(2)(b)","no_analogue",{"US":US_NO_FOLKLORE,"UK":UK_FOLKLORE}),
 ("NCB-C-020","Under Nigerian law, a novelist took motifs from Igbo folk tales and wrote an original novel around them. Is that permitted?","74(2)(d)","no_analogue",{"US":US_NO_FOLKLORE,"UK":UK_FOLKLORE}),
 ("NCB-C-021","Under Nigerian law, I am publishing a book that quotes a traditional folk song. Is there anything I am required to state about its origin?","74(3)","no_analogue",{"US":US_NO_FOLKLORE,"UK":UK_FOLKLORE,"note":"Nigeria s.74(3) requires the SOURCE COMMUNITY OR PLACE to be indicated. No attribution duty of this kind in either comparator."}),
 ("NCB-C-022","Under Nigerian law, are traditional Nigerian textile patterns and wood carvings covered by any protection?","74(5)(d)","no_analogue",{"US":US_NO_FOLKLORE,"UK":UK_FOLKLORE}),
 ("NCB-C-023","Under Nigerian law, a Nollywood production filmed a traditional folk dance for a commercial feature without asking anyone. Is folk dance covered?","74(5)(c)","no_analogue",{"US":US_NO_FOLKLORE,"UK":UK_FOLKLORE}),
 ("NCB-C-024","Under Nigerian law, I import blank discs and duplicating equipment for my Lagos business. Is any levy payable on them?","89(1)","no_analogue",{"US":US_LEVY,"UK":UK_LEVY}),
 ("NCB-C-025","Under Nigerian law, who sets the amount of the copyright levy, and by what instrument?","89(2)","no_analogue",{"US":US_LEVY,"UK":UK_LEVY,"note":"Nigeria s.89(2): set by the MINISTER BY ORDER. The AHRA rates are fixed in the statute itself."}),
 ("NCB-C-026","Under Nigerian law, once the copyright levy is collected, where does the money go and who can receive it?","89(3)","no_analogue",{"US":US_LEVY,"UK":UK_LEVY,"note":"Nigeria s.89(3): into the Commission's Fund, disbursed to approved CMOs. AHRA royalties go to the Copyright Office for distribution to interested parties under 17 USC 1006."}),
 ("NCB-C-027","Under Nigerian law, does the copyright levy reach digital and electronic systems, or only physical items like blank discs?","89(5)","no_analogue",{"US":US_LEVY,"UK":UK_LEVY,"note":"Nigeria s.89(5) expressly includes ELECTRONIC OR DIGITAL SYSTEMS. AHRA 1001(4)(B)(ii) expressly EXCLUDES media used for computer programs and non-musical works."}),

 # ---------- Exceptions ss.21-26 (18) : SUBSTITUTIVE ----------
 ("NCB-C-028","Under Nigerian law, a teacher at a Lagos secondary school used the school photocopier to copy textbook pages for her class. Was that permitted?","21(1)","substitutive",
  {"US":"17 USC 107 EXPRESSLY lists 'teaching (including multiple copies for classroom use)' as a fair use purpose; there is NO categorical bar on reprographic copying. Nigeria s.21(1) excludes exactly that method.","UK":"CDPA s.36(1) permits copying extracts by educational establishments for non-commercial instruction, including reprographic copying, subject to the 5% cap."}),
 ("NCB-C-029","Under Nigerian law, a lecturer wrote out a passage from a published poem on the whiteboard while teaching. Did that infringe?","21(1)","substitutive",
  {"US":"17 USC 107 covers teaching generally under the four factors; no distinction by copying METHOD. Nigeria s.21(1) permits instruction copying but only if NOT by a reprographic process - so manual copying is permitted where photocopying is not.","UK":"CDPA s.36 draws no manual/reprographic distinction."}),
 ("NCB-C-030","Under Nigerian law, a private tutorial centre in Abuja that operates for profit copied part of a film to use in a lesson. Can it rely on the teaching exception?","21(2)","substitutive",
  {"US":"17 USC 107(1) treats 'nonprofit educational purposes' as ONE FACTOR in an open balance, not a threshold. Nigeria s.21(2) restricts the audiovisual/sound-recording exception to NON-PROFIT educational institutions - a bar, not a factor.","UK":"CDPA s.36(1)(a) requires a NON-COMMERCIAL purpose - closer to Nigeria than the US is."}),
 ("NCB-C-031","Under Nigerian law, an examiner reproduced several lines of a published poem inside an examination paper. Was the poet's permission needed?","21(3)","substitutive",
  {"US":"17 USC 107 has NO dedicated examination provision; examination use falls to the general factors. Nigeria s.21(3) gives an express exception for setting, communicating or answering examination questions.","UK":"CDPA s.32 provides an express examination exception - convergent with Nigeria."}),
 ("NCB-C-032","Under Nigerian law, a Nigerian polytechnic recorded a television documentary off air to show in class. Was that allowed?","22(1)","substitutive",
  {"US":"17 USC 110(1)-(2) permits performance/display in face-to-face teaching and certain transmissions, but there is no general off-air RECORDING exception; recording is assessed under 107. Nigeria s.22(1) gives an express off-air recording exception for educational establishments.","UK":"CDPA s.35 permits recording of broadcasts by educational establishments - convergent with Nigeria."}),
 ("NCB-C-033","Under Nigerian law, a Nigerian school records television programmes for teaching. A licensing body now offers a scheme covering exactly that. Does the school still have a free hand?","22(2)","substitutive",
  {"US":"No licence-scheme override in 17 USC; the availability of a licence is at most relevant to the fourth fair use factor. Nigeria s.22(2) DISAPPLIES the exception entirely where a licensing scheme exists.","UK":"CDPA s.35(4) likewise disapplies the exception where a certified licensing scheme is available - CONVERGENT WITH UK."}),
 ("NCB-C-034","Under Nigerian law, a Nigerian university wants to photocopy from a published textbook for teaching. How much may it copy, and how often?","23(2)","substitutive",
  {"US":"17 USC 107(3) makes 'amount and substantiality' an open-ended factor with NO statutory percentage or time window.","UK":"CDPA s.36(5): not more than 5% of a work in any period of TWELVE MONTHS. Nigeria s.23(2) uses the SAME 5% but a THREE-MONTH window - divergence is in the WINDOW, not the proportion."}),
 ("NCB-C-035","Under Nigerian law, a publisher's licence agreement tells our Nigerian college we may copy no more than two per cent of any book. Is that term enforceable against us?","23(4)","convergent_uk",
  {"US":"No 17 USC provision voids contractual terms restricting copying below a statutory allowance; licence terms generally govern.","UK":"CDPA s.36(7) is NEAR-IDENTICAL to Nigeria s.23(4): licence terms purporting to restrict the copyable proportion below the statutory allowance are of no effect. CONVERGENT WITH UK - divergent from the US only."}),
 ("NCB-C-036","Under Nigerian law, our Nigerian university already pays an annual licence fee to a copyright body for photocopying. Does that change what we may copy without permission?","23(3)","convergent_uk",
  {"US":"No licence-scheme override in 17 USC 107.","UK":"CDPA s.36(6) states the same rule as Nigeria s.23(3): the exception does not apply where licences are available and the establishment knew or ought to have known. CONVERGENT WITH UK."}),
 ("NCB-C-037","Under Nigerian law, a student at a Lagos university sold me photocopied course material his department had produced for teaching. Is the copy I bought a lawful one?","24(1)","convergent_uk",
  {"US":"17 USC 109 first-sale doctrine permits resale of a LAWFULLY MADE copy; 17 USC 108(f)(2) preserves user liability where use exceeds fair use. There is no provision converting a permitted copy into an infringing one on resale.","UK":"CDPA s.36(8): a copy made under the education exception and subsequently dealt with IS TREATED AS AN INFRINGING COPY. CONVERGENT WITH UK, divergent from the US."}),
 ("NCB-C-038","Under Nigerian law, someone gave false information on a request form to obtain a copy of a work from a Nigerian library. Who bears the liability?","24(2)","substitutive",
  {"US":"17 USC 108(d)-(e) require the library to display a copyright warning, but liability for a false declaration is not addressed in 17 USC. Nigeria s.24(2) makes the REQUESTER liable as if he had made the copy himself.","UK":"CDPA s.42A(4)-(5) makes a person supplying a false declaration liable as if he had made the copy - CONVERGENT WITH UK."}),
 ("NCB-C-039","Under Nigerian law, a Nigerian museum wants to digitise its collection purely for preservation and back-up. Must it clear that with rightsholders first?","25(1)(b)","substitutive",
  {"US":"17 USC 108(b) permits preservation copying of UNPUBLISHED works only, capped at THREE copies, with digital copies not to be made available outside the premises; 108(c) covers published works only for REPLACEMENT of damaged, lost or obsolete items. Nigeria s.25(1)(b) permits back-up and preservation copying with no published/unpublished split, no numerical cap and no premises restriction.","UK":"CDPA s.42 permits replacement copies for libraries and archives - narrower than a general preservation right."}),
 ("NCB-C-040","Under Nigerian law, a Nigerian library has tried hard but cannot trace the owner of an out-of-print book it holds. May it make a copy anyway?","25(1)(e)","substitutive",
  {"US":"17 USC 108(e) permits copying an entire work where a copy CANNOT BE OBTAINED AT A FAIR PRICE after reasonable investigation - an AVAILABILITY trigger, not an untraceable-OWNER trigger; the copy becomes the user's property and is limited to private study, scholarship or research. NARROW ANALOGUE, not an absence.","UK":"CDPA s.44B and s.76A provide permitted uses of ORPHAN WORKS and s.116A empowers orphan-works licensing regulations - closer to Nigeria s.25(1)(e) than the US is."}),
 ("NCB-C-041","Under Nigerian law, a Nigerian university library has a volume with pages missing. Can it obtain the missing part from another institution's copy?","25(1)(c)","substitutive",
  {"US":"17 USC 108(c) permits replacement of a damaged or deteriorating copy, capped at three copies, only after determining an unused replacement cannot be obtained at a fair price. Nigeria s.25(1)(c) permits obtaining a missing PART from another institution with no such precondition.","UK":"CDPA s.42 permits replacement copies for libraries and archives."}),
 ("NCB-C-042","Under Nigerian law, a Nigerian archive made preservation copies of works in its collection. May it lend those copies to users?","25(2)(a)","substitutive",
  {"US":"17 USC 108(b)(2) and (c)(2) EXPRESSLY forbid making digital copies available outside the library premises. Nigeria s.25(2)(a) permits copies made under the exception to be LENT TO USERS.","UK":"Library lending is governed by the public lending right and licensing rather than a general exception."}),
 ("NCB-C-043","Under Nigerian law, a service provider acted in good faith when taking content down after a notice. Can the uploader sue it for the removal?","55(5)","structural",
  {"US":"17 USC 512(g)(1): no liability for good-faith disabling or removal, REGARDLESS of whether the material is ultimately found infringing - but 512(g)(2) makes that protection CONDITIONAL on notifying the subscriber and honouring the counter-notice procedure. Nigeria s.55(5) states the good-faith immunity without that express condition.","UK":UK_NO_TAKEDOWN}),
 ("NCB-C-044","Under Nigerian law, I want the platform to tell me who uploaded my pirated film so I can sue them. Can I simply ask the platform for the name?","60(1)+60(2)","structural",
  {"US":"17 USC 512(h): the owner requests the CLERK OF A DISTRICT COURT to issue a subpoena, filing a copy of the notification, a proposed subpoena and a sworn declaration; the clerk issues it if the papers are in order. Nigeria s.60 requires an APPLICATION TO THE COURT for an order, not a clerk-issued subpoena.","UK":"Disclosure of an alleged infringer's identity requires a Norwich Pharmacal order from the court; no CDPA provision."}),
 ("NCB-C-045","Under Nigerian law, someone distorted a traditional folk song in a way the originating community finds deeply offensive, and sold the recording. Is that an offence?","76(1)(c)","no_analogue",
  {"US":US_NO_FOLKLORE,"UK":UK_FOLKLORE,"note":"Nigeria s.76(1)(c) makes distortion prejudicial to the honour, dignity or CULTURAL INTERESTS OF THE COMMUNITY a criminal offence. Neither comparator has a community-level integrity right; US moral rights (17 USC 106A) are limited to individual authors of visual art."}),
]

OVERLAP = {"NCB-C-005","NCB-C-006","NCB-C-011","NCB-C-015","NCB-C-017",
           "NCB-C-018","NCB-C-021","NCB-C-024","NCB-C-027","NCB-C-028",
           "NCB-C-034","NCB-C-035","NCB-C-040","NCB-C-044","NCB-C-045"}

# ---------------- SELF-CHECK: does each foreign_default match its item? ----------------
# Map expected_provision -> a token that MUST appear in the foreign_default text.
EXPECT = {
 "54(2)":"512(c)(3)(A)", "54(2)(e)+54(2)(f)":"clause vi", "57":"512(f)",
 "55(1)":"512(c)(1)(C)", "55(2)(b)":"512(g)(2)", "55(3)":"512(m)",
 "55(4)":"512(h)", "55(5)":"512(g)(1)", "55(6)":"512(c)(1)",
 "56(1)(b)":"512(i)(1)(A)", "56(2)":"512(g)(3)", "58":"512(c)(2)",
 "59":"512(d)", "60(1)+60(2)":"512(h)", "61":"512(j)", "62(1)(b)(ii)":"512(c)(2)",
 "21(1)":"107", "21(2)":"107(1)", "21(3)":"107", "22(1)":"110", "22(2)":"licence",
 "23(2)":"36(5)", "23(3)":"36(6)", "23(4)":"36(7)", "24(1)":"36(8)", "24(2)":"declaration",
 "25(1)(b)":"108(b)", "25(1)(c)":"108(c)", "25(1)(e)":"108(e)", "25(2)(a)":"108(b)(2)",
}
problems = []
for iid, q, prov, dtype, fd in ITEMS:
    if not fd:
        problems.append(f"{iid}: no foreign_default"); continue
    token = EXPECT.get(prov)
    if token:
        blob = " ".join(str(v) for v in fd.values())
        if token not in blob:
            problems.append(f"{iid} (prov {prov}): foreign_default does not mention '{token}'")
    if prov.startswith("74") or prov.startswith("76"):
        if "folklore" not in " ".join(str(v) for v in fd.values()).lower():
            problems.append(f"{iid}: folklore item without folklore text")
    if prov.startswith("89"):
        if "levy" not in " ".join(str(v) for v in fd.values()).lower() and "AHRA" not in str(fd):
            problems.append(f"{iid}: levy item without levy text")

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
print("divergence types:", dict(Counter(d for _,_,_,d,_ in ITEMS)))
print(f"foreign_default sourced: {sum(1 for *_,fd in ITEMS if fd)}/{len(ITEMS)}")
print()
if problems:
    print("SELF-CHECK FAILURES:")
    for p_ in problems: print("  ", p_)
else:
    print("SELF-CHECK PASSED: every foreign_default cites a provision consistent with its item.")
