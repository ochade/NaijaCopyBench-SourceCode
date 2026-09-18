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

## M2 citation accuracy, 180 items, three arms (Category E excluded)
Category E items cite provisions that do not exist and have no governing
provision, so citation accuracy cannot be assessed on them. They are measured
by M1 instead. Reported n = 145.

              n    correct  coarse   wrong  no_cite   accuracy
  A1        145          2       5     127       10       4.8%
  A3        145          1       4     139        0       3.4%
  A5        145         51      21      70        2      49.7%

BY CATEGORY (section-level accuracy)
                        A1       A3       A5
  single_hop           2.9%     5.7%    31.4%
  multi_hop           20.0%     0.0%    48.0%
  divergence           0.0%     0.0%    62.2%
  control              0.0%     5.0%    40.0%
  summarization        5.0%    10.0%    65.0%

### Finding 1: base models cannot locate the governing provision
Seven of 145 for A1, five for A3. The pilot result of 0/9 was not a small-sample
artefact. Without the statute supplied, neither model identifies the provision
that governs a Nigerian copyright question at any useful rate.

### Finding 2: divergence is where the failure is absolute
0.0% for BOTH base models across all 45 divergence items - not a single correct
citation on the provisions where Nigerian law departs from US and UK law. With
retrieval the same model reaches 62.2%. This is the sharpest contrast in the
study and it is what the divergence-first construction was designed to expose.

### Finding 3: retrieval helps least where jurisdictions coincide
Control category: 0.0% and 5.0% base, 40.0% retrieved - the smallest gain of any
category. Where Nigerian law matches foreign law the model's parametric answer is
already plausible, so supplying the statute adds less. A benchmark built only from
convergent items would have understated retrieval's effect; one built only from
divergent items would have overstated it.

### Qualitative instance (NCB-B-002, A3)
Question: government employee authored a training manual, died 2015; from what
date is the term counted? Gold: s.19(1)(b) via s.28(2), 50 years.
A3 answered: "the copyright in a work created by an employee ... lasts for the
life of the author plus 70 years after their death ... According to Section 22(1)"
and computed an expiry of 2085.
  - wrong rule (life+70 rather than 50 years for government works)
  - foreign FORMULATION ("life of the author plus 70" is the UK/US phrasing; the
    Act says "70 years after the end of the year in which the author dies")
  - wrong provision (s.22 concerns recording of broadcasts by educational
    establishments)
  - delivered with a computed date and no hedging
All three layers of the dissociation in a single response.

## Methodological defects found while scoring M2
1. Gold provisions in Category E frequently state a NEGATIVE ("NO SECTION 112").
   The gold parser read the digits as a citation, so a model fabricating s.112
   scored CORRECT on the item designed to catch that fabrication. Fixed by
   detecting negation phrasing before parsing.
2. Gold provisions are frequently MULTI-PROVISION with ranges
   ("sections 2(1-2), 2(6), 3"). Single-citation matching returned wrong_but_real
   on every summarisation item, producing a spurious 0.0% for all three arms.
   Fixed by parsing gold as a set of (section, subsection) pairs with range
   expansion.
3. A section-range pattern matched digits INSIDE brackets, so "2(1-2)" was read
   as sections 1 to 2. Fixed by masking bracketed content before range detection.

These are the same class of defect as the Phase 2 parser gaps: each produced a
plausible number rather than an error, and each was found only by inspecting
what the metric actually matched.

### Verification: A3's multi-hop citations
An inspection script displayed A3's cited provisions as blank on most multi-hop
items, suggesting the model might be withholding citations on questions requiring
a provision chain. Direct check of M1's extraction on NCB-B-002 returned
n_citations = 1, section 22 subsection 1, verdict valid - the citation is present
and correctly extracted. The blank display was a fault in the inspection script,
not in the metric. A3's 0.0% on multi-hop reflects wrong citations, not absent
ones. With n = 25 the difference from A1's 20.0% amounts to five items and is
reported subject to its confidence interval.

## M2 with 95% bootstrap CIs (item-level, B=10000, Category E excluded, n=145)
  A1   4.8%  [ 1.4,  8.3]
  A3   3.4%  [ 0.7,  6.9]
  A5  49.7%  [41.4, 57.9]

PAIRWISE DIFFERENCES
  A1 - A3   +1.4  [ -3.4,   6.2]  INCLUDES ZERO - base models indistinguishable
  A1 - A5  -44.8  [-53.1, -35.9]  excludes zero
  A3 - A5  -46.2  [-54.5, -37.9]  excludes zero

=> Retrieval produces a large, reliably estimated improvement in citation
   accuracy. Model scale does not: at n=145 the 3B and frontier models cannot be
   distinguished on this measure.

DIVERGENCE CATEGORY, the strongest result in the study:
  A1  0.0%  [0.0, 0.0]   n=45
  A3  0.0%  [0.0, 0.0]   n=45
  A5 62.2%  [48.9, 75.6]
A true zero, not a rounded one: no bootstrap resample of the 45 divergence items
yields a single correct citation from either base model. On the provisions where
Nigerian law departs from US and UK law, neither model without the statute ever
identifies the governing section. Supplying the Act raises the same model to
nearly two-thirds.

A3 also returns a true zero on multi-hop, [0.0, 0.0] at n=25.
A1's 20.0% on multi-hop is real but imprecise, [4.0, 36.0].

## H1 outcome: displacement is NOT the dominant failure mode
Predicted: models substitute US/UK rules on divergence items at a measurable rate.
Measured: 8-11 instances across 135 arm-items (45 items x 3 arms), of which
several are false positives on over-broad markers.

WHAT MODELS DO INSTEAD. On divergence items they generate Nigerian-SOUNDING
answers with fabricated provisions. A3 cited s.36 for the stay-down question,
s.38 for administrative blocking, s.24(1)(a) for educational photocopying and
s.6 for folklore - none of which govern those questions. No US or UK doctrine
appears in the text.

=> The failure is FABRICATION, not DISPLACEMENT, and M1 already measures it.
=> This is the harder failure to detect: a reader alert to American spelling or
   DMCA references would find none.

CAVEAT. The system prompt states "Base your answer on the Nigerian Copyright Act
2022", which names the jurisdiction and may suppress displacement. The
jurisdiction_cue field permits a test of this, comparing items that name the Act,
name the country, or supply Nigerian context only.

H1 is reported as NOT SUPPORTED in its original form, with the substituted
finding stated. A pre-registered hypothesis that fails is a result.

## Cue test: does naming the Act in the system prompt suppress displacement?
Same model (gpt-4o-mini), same decoding, same 45 divergence items. Only the
system prompt varied.

  "Base your answer on the Nigerian Copyright Act 2022"   4/45   8.9%
  "cite the relevant statute" (no jurisdiction named)     7/45  15.6%

Four items displaced under the neutral prompt only, and the substitutions match
the divergence audit exactly:
  C-002  "penalty of perjury"  (US 512(c)(3)(A)(vi); Nigeria s.54(2)(e) requires
         a declaration on oath)
  C-012  "safe harbor"         (DMCA terminology)
  C-019  "public domain" + "fair use" on folklore
  C-023  "public domain" on folk dance
         (both contradict s.74, which vests authorisation in the Commission and
         specifies no term)
One item displaced under the original prompt only (C-031, "fair use").

CAVEATS. Small absolute numbers - a difference interval would span zero. And the
QUESTIONS still contain "Under Nigerian law", so only the system-prompt cue was
removed; the item-level cue was held constant. Directional evidence, not a
demonstrated effect.

CONSEQUENCE FOR H1. The low displacement rate observed in the main run is partly
an artefact of prompt design. Naming the jurisdiction in the system prompt
roughly halves observed displacement. A deployment that does not name the
jurisdiction - which is how an ordinary user would query - should be expected to
displace more often than this benchmark measures.

## Held-out probe: A2 memorised rather than generalised
Ten sections (12, 13, 16, 26, 29, 32, 74, 79, 86, 101) were withheld entirely
from the fine-tuning set. 21 evaluation items have gold provisions in those
sections.

              trained (n=123)        held out (n=21)
  A1           5.7% [ 2.4,  9.8]      0.0% [ 0.0,  0.0]
  A2          32.5% [24.4, 40.7]      4.8% [ 0.0, 14.3]
  A3           3.3% [ 0.8,  6.5]      4.8% [ 0.0, 14.3]
  A5          46.3% [37.4, 55.3]     71.4% [52.4, 90.5]

A2 trained minus held out: +27.8 points [+15.0, +39.0], EXCLUDES ZERO.

INTERPRETATION. A2's headline improvement (4.8% to 28.3% overall) does not
survive the held-out test. On provisions the adapter never saw it performs at
4.8%, indistinguishable from the base model's 5.7%. Fine-tuning installed 967
memorised question-provision mappings; it did not install the statute.

This supports H2's underlying mechanism (Chung et al. 2022; Colombo et al. 2024)
while refuting its surface prediction. The prediction was that fine-tuning would
improve citation FORM but not SUBSTANCE. What occurred is that it improved
substance ONLY within the training distribution, and not at all outside it.

CONTRAST WITH RETRIEVAL. On the same 21 held-out items, A5 scores 71.4% - HIGHER
than its own trained-section figure of 46.3%. Retrieval is indifferent to whether
a provision appeared in any training set; it looks the provision up. This is the
cleanest available statement of the difference between the two interventions:
fine-tuning memorises what it is shown, retrieval generalises across the corpus.

CAVEAT. 21 held-out items is small and the point estimates are imprecise. The
DIFFERENCE interval excludes zero by a wide margin, so the direction is secure
even where the magnitude is not.

## H2 verdict (formal, with intervals)
M1 fabrication  A1 - A2 = -2.5  [-13.2, +8.2]   includes zero: no reliable effect
M2 accuracy     A1 - A2 = -23.4 [-31.7, -15.2]  excludes zero: large improvement

Surface prediction of H2 (form improves, substance does not) is INVERTED:
substance improved, form did not. But the held-out probe shows the M2 gain is
memorisation (4.8% on unseen sections vs 32.5% on trained). Complete finding:
  1. fine-tuning did not reduce fabrication
  2. it raised citation accuracy sharply, but
  3. only within the training distribution - memorisation, not generalisation.

ANOMALY: A2 divergence fabrication 41.0% [25.9, 55.7], highest of any arm. Fine-
tuning increased citations of BOTH kinds - correct and fabricated. It learned to
emit citations, not to distinguish real from invented ones.

## Full metric summary, four arms
M1 fabrication:  A1 34.6  A2 37.1  A3 25.9  A5 12.5
M2 accuracy:     A1  4.8  A2 28.3  A3  3.4  A5 49.7
Reliable differences (interval excludes zero):
  retrieval reduces fabrication (A1-A5, A2-A5, A3-A5)
  retrieval and fine-tuning both raise accuracy over base (A1-A5, A1-A2)
  A5 beats A2 on accuracy (A2-A5: -21.4 [-32.4, -10.3])
No reliable difference: A1 vs A3 on either metric (scale does not matter at n=180)

## H3 verdict: the bottleneck is retrieval, not reasoning
A5 accuracy conditioned on whether the gold provision was retrieved:

  category         gold retrieved   acc|present   acc|absent
  single_hop        12/35 (34%)       83%           4%
  multi_hop         12/25 (48%)      100%           0%
  divergence        28/45 (62%)      100%           0%
  control            8/20 (40%)      100%           0%
  summarization     13/20 (65%)       92%          14%

WHEN GOLD IS RETRIEVED, A5 cites it correctly 83-100% of the time.
WHEN IT IS NOT, 0-14%. This holds across every category.

CONSEQUENCE. The apparent category differences in A5 accuracy are not differences
in reasoning difficulty - they track retrieval success. Multi-hop scored higher
than single-hop only because retrieval found the gold provision more often
(48% vs 34%), not because the model reasoned better over chains.

H3 PREDICTIONS:
  - retrieval reduces fabrication         CONFIRMED (A3-A5 13.4 [5.8, 21.0])
  - retrieval improves accuracy           CONFIRMED (A3-A5 -46.2 [-55.2, -37.2])
  - retrieve-to-copy easier than          NOT SUPPORTED. The model applies a
    retrieve-to-apply                     retrieved rule almost perfectly
                                          regardless of hop depth. The limiting
                                          factor is whether the provision is
                                          retrieved at all.

A5's accuracy ceiling is set by retrieval recall, not by the model's capacity to
apply retrieved text. This is why the retrieval-gap finding (statutory provisions
are hard to retrieve from layperson queries) is load-bearing: it caps the entire
retrieval arm.
