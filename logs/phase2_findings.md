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

## Step 6 result: A5 (gpt-4o-mini + RAG, top-5) vs A3, A1  (n=12)
                        A1(3B)   A3(4o-mini)  A5(+RAG)
correct citations        0/9        0/9         1/9
correct (any grain)      0/9        0/9         3/9
fabrication rate        44.4%      25.0%        7.1%
gold chunk retrieved      -          -          3/9

PERFECT SPLIT: all 3 items where the gold chunk was retrieved scored correct or
correct-coarse; all 6 where it was not scored wrong_but_real. On this evidence
the bottleneck is RETRIEVAL, not reasoning. (n=9 - suggestive, not conclusive.)

FABRICATION COLLAPSED 25% -> 7.1%. Supplying real statutory text stops the model
inventing sections even when the retrieved text is the WRONG text. Fabrication
suppression is separable from accuracy improvement.

RETRIEVAL IS THE WEAK LINK: 3/9 gold recall at top-5. Cause: the sanity queries
were clean legal questions and retrieved well; the eval items are creator-register
scenarios ("I recorded an album in Lagos in 2015...") whose narrative framing
dilutes the embedding. The ILSIC register gap degrades the RETRIEVER, not just
the model - a direct consequence of the deliberate choice to write realistic
questions.

Attractor chunks: s6, s32, s36, s77 recur across unrelated queries - candidates
for generic-text crowding.

## Retrieval diagnostic: index is fine, the corpus is too homogeneous for dense-only
TEST 1 (sanity): query the index with s.19's OWN text -> s.19 ranks 1st at 1.000,
next best 0.798. Index, chunk and embedding are all correct.

TEST 2 (the failure): query "what is the term of copyright in a literary work?"
  score spread over all 272 chunks: max 0.765, min 0.380, mean 0.578, std 0.072
  s.19 ("Duration of copyright ... 70 years after the end of the year in which
  the author dies") ranks 45/272, score 0.656, 0.109 below the top hit.

=> NOT a corpus-size problem (272 chunks; top-15 = 5.5% of everything).
=> NOT an index problem (Test 1 is exact).
=> IT IS CORPUS HOMOGENEITY. Every chunk is Nigerian copyright law; EDA-B measured
   only 1,987 distinct word types (Herdan's C 0.760). A general-purpose embedder
   cannot separate "the provision that ANSWERS this" from "another provision ABOUT
   copyright". 44 chunks look more like the question than the one that answers it.
   Matches LexPath: "textually similar but legally inapplicable".

=> WHY BM25 SHOULD HELP: idf downweights "copyright" (near-universal in this corpus)
   and upweights rare discriminative terms - "duration", "70 years", "author dies",
   "Federal High Court". This is precisely inverted from what cosine similarity did.

## SAR (Structure-Aware Reranking) tested: DEGRADES recall (3/9 -> 2/9)
Implemented after Beyond Case Law (arXiv 2604.06173), formula
B(n) = (1/L(n)) * sum_s I(s->n) * S_dense(s)/L(s), alpha=0.5, seed_k=10.
Graph = xrefs.json: 60 edges, only 36 of 109 sections cite anything.

TWO FAILURE MODES OBSERVED:
1. CHUNK-LEVEL FLOODING. s.31 is split into 6 chunks; a single graph edge to s.31
   gave all six the same bonus (0.4696), flooding the top-5 and evicting the
   correct answer on MH-002. The paper's corpus is one document per article, so
   section-level bonuses cannot multiply across chunks there.
2. WRONG EDGE DIRECTION FOR OUR QUESTIONS. SAR propagates OUTWARD from seeds.
   Our graph has 19->7, so s.19 can only help once it is already retrieved -
   which is the thing that fails. Nothing in the top-10 cites s.19 (low in-degree),
   so no bonus reaches it.

=> SAR requires a DENSE citation graph with delegation chains pointing toward the
   answer. A 109-section Act with 60 edges does not provide one. This is a
   scale/structure dependency of the technique, not a defect in the implementation.

CONFIGURATIONS TESTED (gold recall@5, n=9):
  dense-only @5      3/9
  dense-only @15     4/9
  hybrid BM25+RRF    3/9   (RRF also degraded recall in the source paper, Table 4)
  SAR                2/9
DECISION: use plain dense retrieval for the RAG arm. Report retrieval recall as a
stated bound. Four configurations tested; retrieval optimisation is out of scope.

## foreign_default sourcing complete: 45/45
Sources: US Title 17 (Circular 92, Dec 2025); UK CDPA 1988 (revised to 03/08/2026).
Both read in full for the relevant provisions. Null results (folklore in 17 USC;
levy in CDPA) verified by search of the primary texts, not asserted.

### What sourcing changed
1. STRONGEST DIVERGENCE FOUND (C-006). 17 USC 512(m)(1) expressly disclaims a
   monitoring duty; Nigeria s.55(3) imposes one. The statutes take OPPOSITE
   positions on stay-down. Only visible by reading the text.
2. UK CONVERGENCE ON EXCEPTIONS. Nigeria s.23(4) and UK CDPA s.36(7) are
   near-identical (void licence terms); likewise s.23(3)/s.36(6) and s.24(1)/
   s.36(8). Three items were mislabelled as divergence. Nigeria's exceptions
   regime is modelled on the UK.
3. CORRECTION. My earlier claim of "no US orphan works exception" was wrong:
   17 USC 108(e) is a narrow analogue with an AVAILABILITY trigger (copy cannot
   be obtained at a fair price) rather than an untraceable-OWNER trigger.
4. C-002 REWRITTEN. The oath requirement is not a divergence - 512(c)(3)(A)(vi)
   requires a penalty-of-perjury statement. Rewritten to target WHAT is sworn:
   the US swears AUTHORITY TO ACT (vi) and leaves the good-faith belief unsworn
   (v); Nigeria s.54(2)(e) swears the BELIEF and leaves authority unsworn.
5. C-015 CONFIRMED NO-ANALOGUE AGAINST BOTH. 512(j) requires a court; CDPA s.97A
   gives the power to the High Court. Nigeria s.61 empowers the Commission to
   block directly. Both comparators agree with each other and differ from Nigeria.

### METHODOLOGICAL FINDING (Ch.5)
Divergence is JURISDICTION-RELATIVE. In a common-law jurisdiction with colonial
inheritance, displacement toward the UK is far harder to detect than displacement
toward the US, because the UK rule is frequently ALSO the Nigerian rule. An item
can be divergent from one comparator and convergent with the other. Convergence-
control logic must therefore be applied PER COMPARATOR, not globally - otherwise
an item silently becomes a convergence point for the very jurisdiction the model
is most likely to import from.

### PROCESS NOTE
Two regex-based patches silently wrote content into the wrong item slot, and a
third stripped a trailing comma and broke the file. A "44/45 sourced" count
looked like near-success while one entry held another item's text. Counts do not
validate contents. Remaining edits to these files should be made by hand.
