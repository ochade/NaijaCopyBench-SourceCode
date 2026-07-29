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
