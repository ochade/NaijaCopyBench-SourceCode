# NaijaCopyBench - Annotation Guidelines (Batch 1)

## What this project is
We are building the first evaluation benchmark for Nigerian copyright law: a set
of questions used to measure how accurately AI language models answer questions
about the Copyright Act 2022. Your answers become the gold standard against which
model outputs are scored. The quality of the entire benchmark rests on them.

## What we need from you, per question
1. GOVERNING PROVISION - the section (and subsection/paragraph where applicable)
   that answers the question.
2. ANSWER - a concise statement of the legal position, in your own words,
   grounded in that provision. 2-4 sentences is usually right.
3. CONFIDENCE - High / Medium / Low.
4. NOTES - ambiguity, alternative provisions you considered, or anything you
   think is defective about the question.

## Source of truth - IMPORTANT
Answer ONLY from the Copyright Act 2022 (PDF supplied). Please do NOT rely on:
  - the repealed Copyright Act (Cap. C28 LFN 2004)
  - case law, textbooks, practitioner commentary
  - Nigerian Copyright Commission guidance or registration practice
  - any other jurisdiction's law
This is a deliberate scope decision: the benchmark measures statutory accuracy,
so the statute alone is the reference. If you believe the practical position
differs from the bare statutory text, please say so in NOTES, not in the ANSWER.

## Please do NOT use AI tools
Do not use ChatGPT, Gemini, Claude, Copilot or any AI assistant at any stage,
including for drafting or checking. This benchmark exists to measure AI accuracy;
if the reference answers are AI-generated, the entire study is invalid.
This is the single most important rule in this document.

## Citation format
Cite as precisely as the provision allows:
    section only            s.103
    section + subsection    s.87(3)
    + paragraph             s.19(1)(d)
If more than one provision genuinely applies, list all and mark which is primary.

## Specific situations

MORE THAN ONE PROVISION APPLIES
List each, mark the primary, explain the relationship in NOTES.

THE QUESTION RESTS ON A FALSE PREMISE
Some questions may assume something that is not so. Say so plainly and state the
correct position. Do not answer as though the premise were true.

THE QUESTION IS AMBIGUOUS
Answer the most reasonable reading and record the ambiguity in NOTES. Please do
not contact us for clarification - how a competent practitioner resolves
ambiguity is itself data we want.

YOU ARE UNSURE
Mark confidence LOW and say why. Acknowledged uncertainty is more useful to us
than a confident guess.

THE QUESTION SEEMS DEFECTIVE
Flag it in NOTES and answer as best you can. Do not skip rows.

## Independence
Some questions are given to both annotators. Please work independently and do not
discuss any question with the other annotator until both sets are submitted. We
report inter-annotator agreement as a quality measure, so independent judgement
matters more than consistency between you.

## Practical
- This batch: 35 questions (single-provision recall). Expect 5-10 minutes each.
- Work in the supplied spreadsheet; do not reorder or renumber rows.
- Questions are written in the voice of a creator or ordinary user, not a lawyer.
  That is deliberate; answer the underlying legal question.

## Attribution
Annotators will be acknowledged in the thesis and any resulting publication
unless you prefer anonymity. Please confirm your preference, and provide your
year of call and principal area of practice, for the methodology section.

## Contact
[your name] - [your email] - [your phone]
Please return the completed sheet by [DATE].
