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

## Second parser gap found by item construction (Cat E)
The paragraph regex required "(a)" with no internal space, but the gazette prints
paragraph (f) as "(f )" throughout - a typesetting convention for the descender.
Result: EVERY paragraph (f) in the Act was missing from section_map.json.
Found only when Category E fabrication probes needed exact paragraph bounds
(s.2(1)(g), s.54(2)(g)) and the map's counts looked one short.

This is the SECOND time downstream consumption surfaced a parser gap that
structural validation passed:
  1. subsection leading-whitespace  -> found when building M1 (citation validity)
  2. paragraph "(f )" internal space -> found when building Cat E probes

PATTERN: structural validation confirms what the parser found; it cannot reveal
what the parser never looked for. Only a consumer that needs a specific field
tests whether that field is complete.

## Step 5 result: A1 (Qwen2.5-3B) vs A3 (gpt-4o-mini), n=12, identical prompts
                     A1              A3
citations emitted    18              16
fabricated            8 (44.4%)       4 (25.0%)
CORRECT CITATIONS     0/9             0/9

Both models: ZERO correct citations on nine gold-bearing items. Independent
architectures, scales and training corpora - the failure is a property of the
task, not of one model.

Scale gradient in fabrication: the 3B model fabricates at ~1.8x the frontier
model rate, and cites slightly MORE often. More confident output, less grounding.

Qualitative contrast on NCB-DIV-001 (sound recording duration, gold s.19(1)(d) =
50 years):
  A3: correct term (50 years), wrong citation (s.27(1))
  A1: WRONG term (70 years - the UK CDPA 13A figure), wrong citation (s.34(1)),
      plus a computed expiry date (2085) presented as certain
=> A3 fails on citation only; A1 fails on answer AND citation.

NCB-FAB-001 (nonexistent s.114):
  A3: paraphrased invented content
  A1: invented content AND supplied a fabricated DIRECT QUOTATION in statutory
      register - a more severe failure mode, because a quotation looks verifiable.

Third parser gap fixed this step: citation regex was matching "s.\n\n4"
(sentence-end + list number) as a citation. Phantoms scored VALID, inflating
citation counts and deflating fabrication rate. A1 corrected 40.0% -> 44.4%.

## Step 6: retrieval quality before running A5 (bge-small, 272 chunks, top-5)
Q: "How long does copyright last in a sound recording?"  (gold s.19(1)(d))
   1. s12  0.789  Nature of copyright in sound recordings   <- WRONG, ranked first
   2. s19  0.752  Duration of copyright                     <- gold
   3. s27  0.749  Special exceptions re sound recordings    <- what A3 wrongly cited
   Scores 0.789/0.752/0.749: a FLAT distribution. Three sections that mention
   "sound recording" are near-indistinguishable to a general embedder; the one
   that answers the DURATION question is not separated from the ones that do not.

Q: "Do I need to register my book to have copyright?"  (gold s.4 + s.87(3))
   1. s87 0.731 Registration of Works                       <- gold (partial)
   s.4 DOES NOT APPEAR. It is a single-sentence section ("...shall not require
   any formality") and short chunks embed weakly against longer competitors.

=> The retriever reproduces the models' topical-not-doctrinal error, and
   under-retrieves very short provisions. Gold reaches the context window via
   top-5, but ranked below or beside distractors.
=> PREDICTION for A5: retrieval helps but does not solve. Confirms the framework
   rejection "retrieval relevance is not correctness" (CerdasHukum) empirically.
