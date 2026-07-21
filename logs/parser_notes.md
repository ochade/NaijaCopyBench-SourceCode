# Step 5 parser requirements (from EDA-A body audit)

1. Section body runs L181–L2951 (s.1 "Objectives" to s.109 "Citation").
2. STOP parsing sections at the Schedule boundary (~L2951). The Schedule
   re-numbers its paragraphs 1..12 (Board proceedings) — these are NOT sections.
3. s.109 header is furniture-prefixed: "Citation. 109. This Act may be cited..."
   Special-case an optional marginal-note prefix before the section number.
4. Header forms in body: "N.—(1) ..." (has subsections) and "N. Title/text"
   (no subsections). Both must be matched.
