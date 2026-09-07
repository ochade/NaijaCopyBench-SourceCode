## Inter-annotator agreement, Categories A and B (computed pre-adjudication)

                          Cat A (n=35)   Cat B (n=25)
raw string agreement         0.000          0.000
normalised citation   kappa  0.679          0.469
section set           kappa  0.761          0.567
one set contains other          7              3
no shared section               1              4

RAW ZERO IS GENUINE, not an artefact. The two annotators use consistently
different house styles - "section 2(1)" vs "S.2(1) C.A 2022" - so no citation
matches exactly across the 60 double-annotated items. Verified by inspection of
the raw cell values.

INTERPRETATION
- A > B gradient as predicted: single-provision recall is more determinate than
  multi-hop, where the answer spans a chain and annotators legitimately differ
  on how much of it to record.
- 55 of 60 items had at least partial agreement on the governing provision;
  only 5 had no shared section at all (1 in A, 4 in B). Those go to adjudication.
- With ~30 distinct provisions across 35 items, expected chance agreement is
  near zero, so kappa is close to raw agreement. The chance correction does
  little work here, which is itself informative about the task's determinacy.

BEARING ON METRIC DESIGN (see 3.5.1)
If qualified practitioners working from the same statute under the same
instructions never converge on a citation format, exact-string matching would
penalise a model for a variation the profession does not itself observe. This
is empirical support for normalising citations before comparison in M2.

## Category A gold set (n=35)
Provenance:
  both annotators endorsed by adjudicator   29
  adjudicator selected one annotator          1
  researcher override                         5   (14%)

Researcher overrides and their basis:
  A-002  adjudicator's provision kept; answer taken from annotator (fuller statement)
  A-011  adjudicator gave s.30 (assignment); question concerns registration's
         evidential effect = s.87(4). Both annotators had cited s.87.
  A-015  adjudicator's provision kept; her reasoning invoked the right of publicity
         and the Data Protection Act, both outside the Act and excluded by protocol
  A-029  adjudicator gave s.44(1)(b) (criminal); question asks whether the conduct
         INFRINGES, answered by s.36(1)(g)
  A-030  adjudicator gave s.44(1)(c) alone; gold records s.36(1)(d)+s.44(1)(c),
         following Eloho, since the conduct is both an infringement and an offence

NOTE FOR LIMITATIONS: a single adjudicator is a single point of failure. In two
cases she answered from outside the Copyright Act despite the protocol excluding
external sources, and in two she cited the criminal provision for questions asking
about civil infringement. The researcher is not legally qualified, so these
overrides are themselves a limitation, recorded rather than concealed.

## M1 fabrication with 95% bootstrap CIs (item-level resampling, B=10000)
  A1  34.6%  [26.9, 42.3]
  A3  25.9%  [19.7, 32.4]
  A5  12.5%  [ 8.3, 17.0]

PAIRWISE DIFFERENCES (percentage points)
  A1 - A3   +8.7  [-1.3, 18.6]   INCLUDES ZERO - no reliable difference
  A1 - A5  +22.1  [13.2, 31.0]   excludes zero
  A3 - A5  +13.4  [ 6.0, 21.1]   excludes zero

=> Retrieval reliably reduces fabrication. Model SCALE does not: at n=180 the
   3B model cannot be said to fabricate more than the frontier model.

BY CATEGORY, notable:
  A5 divergence and summarisation: 0.0% [0.0, 0.0] - zero fabricated citations
     across 65 items. With statutory text supplied the model stops inventing
     provisions on substantive questions.
  A5 fabrication probes: 38.0% [25.7, 52.0] - retrieval halves fabrication on
     probes but does not stop it. Suppression is conditional on the premise
     being true.
  A3 control: 46.2% [23.8, 66.7] - highest of any category for that arm, on
     questions that do not invite fabrication. Wide interval (n=20). Consistent
     with the pilot pattern of correct answers carrying invented citations;
     confirmation requires gold provisions.

## M1 fabrication with 95% bootstrap CIs (item-level resampling, B=10000)
  A1  34.6%  [26.9, 42.3]
  A3  25.9%  [19.7, 32.4]
  A5  12.5%  [ 8.3, 17.0]

PAIRWISE DIFFERENCES (percentage points)
  A1 - A3   +8.7  [-1.3, 18.6]   INCLUDES ZERO - no reliable difference
  A1 - A5  +22.1  [13.2, 31.0]   excludes zero
  A3 - A5  +13.4  [ 6.0, 21.1]   excludes zero

=> Retrieval reliably reduces fabrication. Model SCALE does not: at n=180 the
   3B model cannot be said to fabricate more than the frontier model.

BY CATEGORY, notable:
  A5 divergence and summarisation: 0.0% [0.0, 0.0] - zero fabricated citations
     across 65 items. With statutory text supplied the model stops inventing
     provisions on substantive questions.
  A5 fabrication probes: 38.0% [25.7, 52.0] - retrieval halves fabrication on
     probes but does not stop it. Suppression is conditional on the premise
     being true.
  A3 control: 46.2% [23.8, 66.7] - highest of any category for that arm, on
     questions that do not invite fabrication. Wide interval (n=20). Consistent
     with the pilot pattern of correct answers carrying invented citations;
     confirmation requires gold provisions.
