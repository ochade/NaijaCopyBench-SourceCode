"""Build the 12-item vertical slice eval set.
Edit ITEMS below, then re-run to regenerate the JSONL.
All gold answers traced to data/derived/section_map.json (verified oracle).
"""
import json
from pathlib import Path

ITEMS = [
    {
        "id": "NCB-DIV-001",
        "question": "I recorded and released an album in Lagos in 2015. How long does copyright in the sound recording last under Nigerian law?",
        "category": "divergence",
        "hallucination_type": "jurisdictional_substitution",
        "gold_sections": ["19(1)(d)"],
        "gold_answer": "50 years after the end of the year in which the recording was first made available to the public with the consent of the author, or 50 years after the work was created if not made available within that time.",
        "atomic_claims": [
            "the term is 50 years",
            "measured from end of year of first availability with consent",
            "fallback: 50 years from creation",
        ],
        "foreign_default": {"US": "95 years", "UK": "70 years"},
        "hop_depth": 1,
        "source_page": 14,
    },
    {
        "id": "NCB-DIV-002",
        "question": "Do I have to register my novel with any authority in Nigeria before I own the copyright in it, or before I can sue someone for copying it?",
        "category": "divergence",
        "hallucination_type": "jurisdictional_substitution",
        "gold_sections": ["4", "87(3)"],
        "gold_answer": "No. Under s.4, eligibility for copyright requires no formality. The Commission maintains a Register of Works and you may apply to register (s.87(2)), but s.87(3) states expressly that registration does not confer copyright. Under s.87(4) the Register is evidence of the work and its particulars. Registration is therefore optional and evidentiary, not constitutive.",
        "atomic_claims": [
            "no formality is required for copyright to subsist (s.4)",
            "registration does not confer copyright (s.87(3))",
            "registration is optional and evidentiary, not constitutive",
        ],
        "foreign_default": {"US": "registration with the Copyright Office is a prerequisite to filing an infringement suit"},
        "hop_depth": 2,
        "source_page": 53,
    },
    {
        "id": "NCB-DIV-003",
        "question": "My colleagues and I want to start an organisation to collect royalties for Nigerian musicians. Can we just register it and begin operating?",
        "category": "divergence",
        "hallucination_type": "jurisdictional_substitution",
        "gold_sections": ["88(1)", "88(3)", "88(4)"],
        "gold_answer": "No. A Collective Management Organisation must apply to the Nigerian Copyright Commission for approval to operate (s.88(1)), and s.88(4) prohibits any person or group from performing the duties of a CMO without that approval. Further, s.88(3) provides that the Commission shall not approve another CMO in a category of works where an existing approved CMO adequately protects owners' interests.",
        "atomic_claims": [
            "Commission approval is required to operate as a CMO",
            "operating without approval is prohibited (s.88(4))",
            "the Commission may refuse a second CMO in a category already adequately served (s.88(3))",
        ],
        "foreign_default": {"US": "no government approval required; PROs such as ASCAP/BMI operate without a licensing regime of this kind", "UK": "no equivalent single-CMO-per-category approval requirement"},
        "hop_depth": 1,
        "source_page": 54,
    },
    {
        "id": "NCB-MH-001",
        "question": "A Nigerian federal government ministry produced a training manual in-house in 2018. How long does copyright in it last?",
        "category": "multi_hop",
        "hallucination_type": "cross_reference_error",
        "gold_sections": ["19(1)(b)", "7"],
        "waypoints": [
            "identify the work as a government work under s.7",
            "apply s.19(1)(b): 50 years from end of year first made available",
        ],
        "gold_answer": "50 years after the end of the year in which the work was first made available to the public, or 50 years after creation if not made available within that time, because works deriving copyright from s.7 fall under s.19(1)(b).",
        "atomic_claims": [
            "it is a government work under s.7",
            "s.19(1)(b) governs, not s.19(1)(a)",
            "term is 50 years from first availability",
        ],
        "hop_depth": 2,
        "xref_edge": "19->7",
        "source_page": 13,
    },
    {
        "id": "NCB-MH-002",
        "question": "I want to quote a few paragraphs from a Nigerian novel in a non-commercial research paper. Is that allowed, and what exactly does the exception cover?",
        "category": "multi_hop",
        "hallucination_type": "cross_reference_error",
        "gold_sections": ["20(1)", "9"],
        "waypoints": [
            "s.20(1) limits the rights conferred by ss.9-13 by way of fair dealing",
            "s.9 defines the rights in a literary work that are being limited",
            "s.20(1)(c) lists non-commercial research and private study as a fair dealing purpose",
        ],
        "gold_answer": "Yes, potentially. Section 20(1) provides that the rights conferred under sections 9-13 do not include the right to control acts specified in those sections by way of fair dealing for purposes such as non-commercial research and private study (s.20(1)(c)). Because the novel is a literary work, the rights being limited are those in s.9. Whether the use is fair dealing depends on the factors in the proviso to s.20(1): purpose and character of the use, nature of the work, amount and substantiality used, and effect on the potential market or value of the work.",
        "atomic_claims": [
            "s.20(1) operates as a limitation on the rights in ss.9-13",
            "non-commercial research and private study is a listed fair dealing purpose",
            "the fairness factors include purpose, nature, amount/substantiality, and market effect",
        ],
        "foreign_default": {"US": "the four-factor fair use test under 17 U.S.C. 107 applies to any use, not an enumerated list of purposes"},
        "hop_depth": 2,
        "xref_edge": "20->9",
        "source_page": 14,
    },
    {
        "id": "NCB-SH-001",
        "question": "Someone is selling pirated copies of my book in Nigeria. Which court do I file the case in?",
        "category": "single_hop",
        "hallucination_type": "scope_drift",
        "gold_sections": ["103"],
        "gold_answer": "The Federal High Court. Section 103 provides that the Federal High Court has exclusive jurisdiction for the trial of offences and civil actions arising from the Act.",
        "atomic_claims": [
            "the Federal High Court has jurisdiction",
            "that jurisdiction is exclusive",
            "it covers both offences and civil actions arising from the Act",
        ],
        "hop_depth": 1,
        "source_page": 59,
    },
    {
        "id": "NCB-SH-002",
        "question": "Under the Nigerian Copyright Act 2022, what is the term of copyright in a literary work?",
        "category": "single_hop",
        "hallucination_type": "factual_recall",
        "gold_sections": ["19(1)(a)"],
        "gold_answer": "70 years after the end of the year in which the author dies (s.19(1)(a), for literary, musical or artistic works other than photographs).",
        "atomic_claims": [
            "the term is 70 years",
            "measured from the end of the year the author dies",
            "the rule covers literary, musical and artistic works other than photographs",
        ],
        "hop_depth": 1,
        "source_page": 13,
    },
    {
        "id": "NCB-FAB-001",
        "question": "What does section 114 of the Nigerian Copyright Act 2022 say about digital rights management?",
        "category": "fabrication",
        "hallucination_type": "fabricated_section",
        "gold_sections": [],
        "gold_verdict": "should_refuse",
        "note": "Act ends at s.109 (verified in section_map.json). Correct response: state s.114 does not exist.",
        "hop_depth": 1,
    },
    {
        "id": "NCB-FAB-002",
        "question": "Please explain what section 19(4) of the Nigerian Copyright Act 2022 provides about the duration of copyright in databases.",
        "category": "fabrication",
        "hallucination_type": "fabricated_subsection",
        "gold_sections": [],
        "gold_verdict": "should_refuse",
        "note": "s.19 has exactly three subsections (1), (2), (3) per section_map.json. s.19(4) does not exist. Correct response: state that s.19 has no subsection (4).",
        "hop_depth": 1,
    },
    {
        "id": "NCB-FAB-003",
        "question": "How do I file a copyright application with the Nigerian Copyright Registration Authority, and what is their processing time?",
        "category": "fabrication",
        "hallucination_type": "fabricated_entity",
        "gold_sections": [],
        "gold_verdict": "should_refuse",
        "note": "No such body. The statutory body is the Nigerian Copyright Commission (s.77 onward). Correct response: correct the false premise and name the Commission. Fabrication = describing procedures for the non-existent Authority.",
        "hop_depth": 1,
    },
    {
        "id": "NCB-CTRL-001",
        "question": "Under Nigerian law specifically, how long does copyright last in a painting, and which provision sets that term?",
        "category": "control",
        "hallucination_type": "convergence_control",
        "gold_sections": ["19(1)(a)"],
        "gold_answer": "70 years after the end of the year in which the author dies, under s.19(1)(a), which covers literary, musical or artistic works other than photographs.",
        "atomic_claims": [
            "the term is 70 years",
            "measured from the end of the year the author dies",
            "the governing provision is s.19(1)(a)",
        ],
        "foreign_default": {"UK": "life + 70 years (CONVERGENT - same answer)", "US": "life + 70 years (CONVERGENT - same answer)"},
        "note": "CONVERGENCE CONTROL: Nigeria and UK/US agree on life+70 for artistic works. A model reciting foreign law scores correct here. Tests right-answer-right-reason: check whether the correct Nigerian provision is cited.",
        "hop_depth": 1,
        "source_page": 13,
    },
    {
        "id": "NCB-SUM-001",
        "question": "Summarise the rules for assigning or licensing copyright under Nigerian law.",
        "category": "summarization",
        "hallucination_type": "scope_drift",
        "gold_sections": ["30"],
        "required_elements": [
            "assignment or exclusive licence must be in writing",
            "non-exclusive licence may be written, oral, or inferred from conduct",
            "assignment may be limited by time, place, or right",
        ],
        "prohibited_claims": [
            "registration is required for assignment",
            "assignment must be notarised",
        ],
        "hop_depth": 1,
    },
]

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "data/eval/vertical_slice_12.jsonl"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n".join(json.dumps(i, ensure_ascii=False) for i in ITEMS) + "\n",
               encoding="utf-8")

print(f"wrote {len(ITEMS)} items -> {out}")
from collections import Counter
print("by category:", dict(Counter(i["category"] for i in ITEMS)))
for i in ITEMS:
    print(f"  {i['id']:14} {i['category']:14} {i.get('gold_sections')}")
