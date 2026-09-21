# NaijaCopyBench - Guidelines for the Adjudicating Reviewer

## What this project is
We are building the first evaluation benchmark for Nigerian copyright law: a set
of questions used to measure how accurately AI language models answer questions
about the Copyright Act 2022. Two junior annotators have answered each question
independently. Your review produces the final gold-standard answers against
which model outputs will be scored.

## Your role
You are not a third independent annotator. You are reviewing two existing
answers and determining the correct position. For each item you may endorse one
annotator, endorse both in part, reject both and supply your own answer, or
record that the Act does not settle the point.

You are being sent ALL items, not only the disputed ones. Rows where the
annotators disagreed are sorted to the top and colour-coded; rows where they
agreed still need your eye, because agreement does not guarantee correctness.

## How the spreadsheet is laid out

READ-ONLY COLUMNS (please do not edit)

  item_id            Our reference for the question. Do not renumber or reorder.

  review_reason      Why this row needs attention, colour-coded:
                       RED    PROVISION DISAGREEMENT - the two annotators cited
                              different provisions. Highest priority.
                       AMBER  LOW CONFIDENCE - one or both marked confidence Low.
                       BLUE   NOTES FLAGGED - an annotator recorded a concern
                              about the question or the provision.
                       (none) AGREED - both cited the same provision. Still
                              needs review, but should be quicker.

  question           The question as put to the annotators. Written in the voice
                     of a creator or ordinary user rather than a lawyer; that is
                     deliberate.

  Euchay_provision   First annotator's citation, answer, confidence and notes.
  Euchay_answer
  Euchay_confidence
  Euchay_notes

  Eloho_provision    Second annotator's citation, answer, confidence and notes.
  Eloho_answer
  Eloho_confidence
  Eloho_notes

COLUMNS FOR YOU TO COMPLETE

  FINAL_provision    The section (and subsection/paragraph) you consider
                     governing. Cite as precisely as the provision allows:
                       section only          s.103
                       + subsection          s.87(3)
                       + paragraph           s.19(1)(d)
                     If more than one provision genuinely applies, list all and
                     mark which is primary.

  FINAL_answer       A concise statement of the legal position in your own words,
                     grounded in that provision. Two to four sentences is usually
                     right. You may adopt an annotator's wording if it is sound.

  basis_of_resolution   Choose one:
                       EUCHAY CORRECT
                       ELOHO CORRECT
                       BOTH PARTIALLY CORRECT
                       NEITHER CORRECT
                       BOTH CORRECT          (for agreed rows you endorse)
                       GENUINELY UNSETTLED   (see below)

  reasoning          Why. One or two sentences. This is the most valuable field
                     on the sheet: it records how a senior practitioner resolves
                     a reading that two competent juniors took differently.

  question_verdict   Is the QUESTION sound, or did it cause the problem?
                       SOUND      the question is fine
                       AMBIGUOUS  reasonably admits more than one reading
                       DEFECTIVE  badly framed, missing facts, or false premise

## GENUINELY UNSETTLED is a permitted outcome
If you conclude the Act does not settle the point - that two readings are both
defensible on the statutory text - say so and record both. Do not manufacture a
resolution. We would rather exclude an item from scoring and report it than
record a false gold answer. This is the single most useful thing you can do for
the integrity of the benchmark.

## Source of truth
Resolve from the Copyright Act 2022 alone (PDF supplied). Not the repealed 2004
Act, not case law, not Commission practice, not another jurisdiction's law.

Where your experience tells you the position in practice differs from the bare
statutory text, that is exactly the observation we want - but put it in
REASONING, not in FINAL_answer. The answer field records what the statute
provides; the reasoning field can record everything else.

## Please do not use AI tools
Do not use ChatGPT, Gemini, Claude, Copilot or any AI assistant at any stage,
including for drafting or checking. This project measures AI accuracy against
human expert judgement; AI-assisted adjudication would invalidate the study.
This is the most important instruction in this document.

## A note on citation formats
The two annotators use different notations for the same provision - for example
"sec 19(1c)" and "S.19(1)(c) C.A 2022". Where the difference is only notational,
please treat them as agreeing and say so in reasoning. Where the difference is
substantive, that is what we need your judgement on.

## Practical
  - Category A: 35 questions. Category B: 25 questions.
  - Expect 5-10 minutes per item; less for the agreed rows.
  - Work in the supplied spreadsheet; do not reorder or renumber rows.
  - The first two columns are frozen so they stay visible as you scroll.

## Attribution
You will be acknowledged in the thesis and any resulting publication as the
adjudicating reviewer, unless you prefer anonymity. Please confirm your
preference, and provide your year of call and principal area of practice, for
the methodology section.

## Contact
[your name] - [your email] - [your phone]
Please return by: [DATE]
