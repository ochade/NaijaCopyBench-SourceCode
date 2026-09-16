# Chapter 3 - Methodology (accumulating; ordered by pipeline stage, not by date)
Rule: every entry states the DECISION, the REASON, and the EVIDENCE.

## 3.1 Source and provenance
- Copyright Act 2022, gazette scan, 68 pages. Text frozen, SHA-256 recorded in
  SOURCE.md; scan hashed separately. Raw file write-once; all cleaning produces
  derived artifacts.
- Numerals gate: durations verified against scan p.13/14; all eight distinct fine
  amounts verified.

## 3.2 Cleaning  (clean = f(raw), reproducible)
- R1 remove 68 running headers (one per page)
- R3 un-fuse s.109 header ("Citation. 109." -> "109.")
- R4 repair 0x02 control byte: 9 compound hyphens restored, 3 soft-hyphen word
  splits rejoined  [E-002, E-003]
- One candidate erratum WITHDRAWN: s.18 "Commencements" is the Act's own wording,
  confirmed on the Arrangement page. Recorded to show corrections were verified,
  not assumed.

## 3.3 Structure extraction
- section_map.json: 109 sections, title, subsections, paragraphs, page, text
- Two parser gaps found by downstream consumption, not by structural validation:
  leading whitespace before "(3)"; internal space in "(f )". Both Act-wide.

## 3.4 Dataset design
- Six categories, 180 items. Question design rules in docs/question_design_rules.md
- jurisdiction_cue controlled: A-D "named", E "explicit", F "contextual"
- Two annotators; ~1/3 of each category double-annotated for Cohen's kappa

## 3.5 Chunking
- EDA-B: median section 149 words; 15 sections >400 -> hybrid strategy
- Cascade: subsection split -> paragraph split -> 350-word cap
- Result: 272 chunks, max 368 words (within bge-small's window, nothing truncated)

## 3.6 Retrieval
- bge-small-en-v1.5, FAISS IndexFlatIP (cosine on normalised vectors)
- [PENDING] hybrid BM25 + dense + RRF, following HyPA-RAG and T2-RAGBench.
  One configuration, no tuning: retrieval optimisation is out of scope.

## 3.7 Model arms
- A1/A2 Qwen2.5-3B-Instruct. Phi-3.5-mini abandoned: its bundled modeling code
  calls a removed transformers API (DynamicCache.from_legacy_cache).
- A3/A5 gpt-4o-mini-2024-07-18, version-pinned for reproducibility
- Identical system prompt and greedy decoding across all arms

## 3.8 Metrics
- M1 citation validity / M2 citation accuracy: decidable against section_map.json,
  no annotation required. Graded fabrication tiers (section / lettered / subsection
  / paragraph / entity).
- Citation regex tightened after false positives: "s." + line break + list number
  was parsed as a citation, inflating valid counts and deflating fabrication rate.

## Scoring rule: partial citation matches (fixed before scoring, all metrics)
A citation to the correct SECTION counts as supported even where the gold
provision specifies a subsection or paragraph. Citing s.19 where the gold is
s.19(1)(d) is scored as supported.

RATIONALE. The two annotators cited the same provisions at different levels of
granularity throughout, and no exact string match occurred between them across
the sixty double-annotated items. Requiring subsection-level precision from a
model would impose a standard the annotating practitioners did not themselves
observe.

CONSEQUENCE FOR REPORTING. M2 retains the distinction as a separate verdict
(correct at section level) so that the stricter figure remains recoverable.
Both are reported: accuracy at section level and accuracy at full gold
granularity. The section-level figure is the headline.

This rule is applied identically to every arm and every category.
