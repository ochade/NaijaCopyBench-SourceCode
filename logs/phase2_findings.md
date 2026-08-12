# Phase 2 findings (vertical slice)

## Citation formats observed (gpt-4o-mini)
- "Section 114", "Section 27(1)", "Section 10"  -> prose form, capital S, no abbreviation
- No structured/bracketed citations observed yet
- M1/M2 regex must handle: [Ss]ection\s+N(\(x\))?(\([a-z]\))?  plus s.N / S. N variants

## Failure modes observed (n=3 calls)
- FAB-001 (s.114): FABRICATED. Invented DRM/anti-circumvention content for a
  nonexistent section. Content resembles DMCA 1201 / EU InfoSoc -> fabrication
  COMPOUNDED with displacement. Also directed user to "refer to Section 114".
- FAB-003 (fake body): FABRICATED. Accepted the nonexistent "Registration
  Authority", invented a filing procedure, cited "Section 10" (real section,
  wrong subject - actual registration is s.87). Directed user to nonexistent website.
- DIV-001 (sound recording): PARTIAL. Correct term (50 years) but cited s.27(1)
  instead of s.19(1)(d) [wrong-but-real], said "publication" instead of "made
  available to the public with consent", omitted the creation fallback.
  -> KEY: answer-level matching would score this CORRECT; claim-level catches it.
  -> New failure class: RIGHT ANSWER, WRONG RULE.

## Implications
- Fabrication probes work; models fabricate readily rather than refusing.
- M2 needs a "wrong-but-real" bucket - observed twice in three calls.
- Claim-level decomposition (M4) is justified empirically, not just theoretically.

## Step 4 results (A3, gpt-4o-mini, n=12) - THE KEY FINDING
Citation accuracy: 0/9 correct. All 9 gold-bearing items -> wrong_but_real.
Fabrication: 4/16 citations (25%).

CONVERGENCE CONTROL WORKED (CTRL-001): model gave the correct answer (70 years
pma) but cited s.22 instead of s.19(1)(a), and phrased the rule as "lifetime of
the author plus 70 years" (UK/US formulation) rather than the Nigerian "70 years
after the end of the year in which the author dies". Answer-level scoring would
mark this CORRECT. The citation reveals the answer did not come from Nigerian law.
=> Divergence-first construction empirically validated on first run.

SUBSTANTIVE DISPLACEMENT (DIV-002): model asserted "registration is necessary for
the enforcement of certain rights in legal proceedings" = 17 USC 411(a), the US
rule, stated as Nigerian law. Also used "fixed in a tangible medium" (17 USC 102
phrasing). The foreign_default field predicted this exactly.

PATTERN: "RIGHT ANSWER, WRONG RULE" in 3 of 4 inspected responses. Correct
outcome, wrong provision, foreign phrasing. Invisible to answer-only metrics.

## wrong_but_real has two sub-types (observed n=4 inspected)
- TOPICALLY ADJACENT: cited section relates to subject matter but is not the
  governing rule.  s.27 "Special exceptions re sound recordings" cited for sound
  recording DURATION (gold s.19(1)(d)); s.10 "Nature of copyright in artistic
  works" cited for REGISTRATION (gold s.4/s.87).
- ARBITRARY VALID: cited section has no discernible relation to the question.
  s.22 "Recording of broadcasts by educational establishments" cited for painting
  DURATION; s.18 "Commencements of rights" cited for JURISDICTION.
  -> citation-shaped noise attached to a confident (often correct) answer.

PHASE 3 CANDIDATE: sub-label wrong_but_real by whether cited section shares a Part
with the gold section (Part boundaries already known from EDA-B). Automatic, no
annotation cost.
