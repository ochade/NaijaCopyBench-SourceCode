from pathlib import Path
import json

p = Path("build_catA_gold.py")
t = p.read_text(encoding="utf-8")

OLD = '''OVERRIDE = {"NCB-A-011": {"provision": "87(4)",
                          "note": "adjudicator gave s.30 (assignment); question concerns "
                                  "registration's evidential effect, which is s.87(4). "
                                  "Both annotators cited s.87. Overridden by researcher."}}'''

NEW = '''OVERRIDE = {
 "NCB-A-011": {"provision": "87(4)", "answer_from": "euchay",
   "note": "Adjudicator gave s.30 (assignment). The question concerns registration's "
           "evidential effect, which is s.87(4); both annotators cited s.87. "
           "Researcher override."},
 "NCB-A-002": {"provision": "3(a)", "answer_from": "euchay",
   "note": "Adjudicator's provision accepted. Answer taken from the annotator, whose "
           "statement of the exclusion is fuller than the adjudicator's summary."},
 "NCB-A-015": {"provision": "28(3)", "answer_from": "euchay",
   "note": "Adjudicator's provision accepted. Her reasoning invoked the right of "
           "publicity and the Data Protection Act, both outside the Copyright Act and "
           "excluded by the annotation protocol; the answer is taken from the annotator."},
 "NCB-A-029": {"provision": "36(1)(g)", "answer_from": "euchay",
   "note": "Adjudicator gave s.44(1)(b), the criminal provision. The question asks "
           "whether the club is INFRINGING, which s.36(1)(g) answers. Researcher override."},
 "NCB-A-030": {"provision": "36(1)(d)+44(1)(c)", "answer_from": "eloho",
   "note": "Adjudicator gave s.44(1)(c) alone. Both cited: s.36(1)(d) establishes "
           "infringement, s.44(1)(c) that the conduct is also an offence. Eloho cited "
           "both and her answer is used. Researcher override (partial)."},
}'''
t = t.replace(OLD, NEW)

t = t.replace('''    if iid in OVERRIDE:
        rec["gold_provision"] = OVERRIDE[iid]["provision"]
        rec["gold_answer"] = euchay          # Euchay quoted s.87(4) correctly
        rec["answer_source"] = "Euchay (researcher override)"
        rec["override_note"] = OVERRIDE[iid]["note"]''',
'''    if iid in OVERRIDE:
        o = OVERRIDE[iid]
        rec["gold_provision"] = o["provision"]
        rec["gold_answer"] = eloho if o["answer_from"] == "eloho" else euchay
        rec["answer_source"] = f"{o['answer_from'].title()} (researcher override)"
        rec["override_note"] = o["note"]''')

p.write_text(t, encoding="utf-8")
print("patched: five overrides recorded")
