# Gold answer provenance

GOLD = the lawyers' answers. Nothing else.

The internal files carry expected_provision (and, for Category F, draft
required_elements). These are CONSTRUCTION METADATA: they exist to check that
items target the provisions they were written for, and to measure where
annotators diverge from the item's design.

They MUST NOT be used to score model output. If a lawyer cites a different
provision from expected_provision, the lawyer is right and the item is either
badly worded or genuinely ambiguous - both are findings.

Category F: draft required_elements/prohibited_claims were LLM-drafted and are
retained only as an internal comparison against the lawyers' lists. The
annotation sheet is blank; annotators see nothing but the question.

Category C: foreign_default is comparator data (US Title 17, UK CDPA), not
Nigerian gold. Nigerian annotators are not asked about it.

Category E: why_nonexistent is a lookup against the verified section_map, not a
legal opinion - but all 35 items still go to the annotators for independent
confirmation.
