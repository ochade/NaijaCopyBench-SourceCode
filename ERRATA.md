# Errata

Corrections to OCR errors found in the frozen source (data/act/raw/CopyrightAct2022.txt).
The raw file is NEVER edited. Each entry records the error, the correct reading
(verified against the page image), and where the correction is applied downstream.

Format:
| ID | Location | Raw (OCR) reads | Correct reading | Verified vs page | Applied in |

(none yet)

| E-001 | s.109 header, body (PDF final page, L2951) | "Citation. 109. This Act may be cited..." — marginal note "Citation." fused inline before the section number | Section number is 109; header format is furniture-prefixed, not line-initial | Yes — Arrangement lists s.109 "Citation"; body text present and complete | Step 5 parser: special-case optional marginal-note prefix before section number. s.109 confirmed PRESENT, not missing. |
