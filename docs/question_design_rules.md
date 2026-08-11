# Question Design Rules - NaijaCopyBench

Check every batch against this list before it goes to annotators.

## Rules that protect validity

1. ANSWERABLE FROM THE ACT ALONE. If it needs case law, NCC practice, or facts
   outside the statute, cut it. Test: can you point to the exact provision that
   answers it?

2. ONE DETERMINATE ANSWER for categories A-D. If two competent lawyers could
   reasonably disagree, it belongs in a contested bucket we are not building, or
   it needs rewriting.

3. SELF-CONTAINED. No dependency on other items, no "as in the previous question".

4. THE QUESTION MUST NOT CONTAIN ITS OWN ANSWER. Do not write "under the fair
   dealing exception, can I..." if you are testing whether they find s.20. Do not
   name section numbers. Do not use statutory phrasing that fingerprints the
   provision.

## Rules that protect measurement

5. CREATOR REGISTER, NOT STATUTE REGISTER. "I recorded an album in Lagos in
   2015..." not "What is the term of protection for phonograms?" Users are
   creators; questions should sound like them. (ILSIC register-gap point.)

6. DIVERGENCE ITEMS MUST SIT AT VERIFIED DIVERGENCE POINTS. Before writing a
   Category C item, confirm Nigeria actually differs from US/UK on that rule,
   with a citation. An item at a convergence point measures nothing.

7. EVERY DIVERGENCE ITEM NEEDS A POPULATED foreign_default with a real statutory
   citation (17 U.S.C. 411, 302, 107; CDPA 1988 s.13A). Without it, M3 cannot
   detect substitution.

8. FABRICATION PROBES MUST BE PLAUSIBLE, NOT ABSURD. "s.114" works because the
   Act could have had one. "s.9,000" does not. Same-type substitution: the
   adjacent jurisdiction true value, not a random one.

## Rules that protect balance

9. MAX 15% DURATION QUESTIONS. s.19 is over-represented by default; weight
   toward takedown, CMO, folklore, levy, exceptions.

10. CATEGORY C ALLOCATED BY PROVISION DENSITY, NOT UNIFORMLY. Part VII (9
    sections) can carry more items than Part IX folklore (3 sections). An even
    split either produces redundant folklore items or under-samples takedown.

11. SPREAD ACROSS PARTS. Do not let Part I take half the set because it is the
    most familiar.

## Rules that protect the annotation

12. NO LEADING PHRASING. "Isn't it true that registration is required?" invites
    agreement. Neutral: "Do I need to register?"

13. ANSWERABLE IN 5-10 MINUTES. If a lawyer needs an hour, it is too complex for
    the annotation budget.

14. MULTI-HOP ITEMS MUST TRAVERSE A REAL xrefs.json EDGE. Not an imagined chain,
    a verified one.

## The three that would embarrass us if broken

15. NOTHING THAT IDENTIFIES A REAL PERSON OR A LIVE DISPUTE. Use invented
    scenarios.

16. EVERY ITEM TRACEABLE TO A PROVISION ACTUALLY READ - not one described
    second-hand, not one inferred from a section title. This discipline has
    already caught three errors (s.30(4) inferred-from-conduct omission,
    s.103 page number, s.87 inferential claim).

17. QUESTIONS DRAFTED WITH AI MUST BE HUMAN-VERIFIED BEFORE USE, and the
    methodology must say so. We are measuring AI accuracy; unverified
    AI-generated items would undercut the study.

## Jurisdiction cue (added after Batch 1 design)

18. JURISDICTION CUE MUST BE A CONTROLLED VARIABLE, not incidental. Three levels:
      explicit   - names the Act:      "Under the Nigerian Copyright Act 2022..."
      named      - names the country:  "Under Nigerian law..."
      contextual - setting only:       "I recorded an album in Lagos in 2015..."
    Default to NAMED. Hold the level constant within a category so cue strength
    is not confounded with what is being measured. Tag every item with
    jurisdiction_cue. Reserve CONTEXTUAL for a deliberate tagged subset testing
    whether the model infers jurisdiction. Avoid EXPLICIT as a default - naming
    the Act is a stronger hint than a real user gives.
    Nigerian setting detail (Lagos, Nollywood, NBC, Afrobeats) belongs in almost
    every question regardless of cue level: that is realism, not cueing.

## Batch checklist

Before sending a batch to annotators, confirm:
  [ ] every item traceable to text actually read (rule 16)
  [ ] no section numbers or statutory phrasing in question text (rule 4)
  [ ] duration items under 15% of the batch (rule 9)
  [ ] jurisdiction_cue set and consistent within category (rule 18)
  [ ] divergence items have cited foreign_default (rules 6, 7)
  [ ] multi-hop items map to a real xrefs edge (rule 14)
  [ ] no real persons or live disputes (rule 15)
  [ ] internal file (expected provisions) separated from the annotator sheet
