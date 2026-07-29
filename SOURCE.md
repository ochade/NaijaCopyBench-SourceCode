# Source provenance

## Statute
- File: data/act/raw/CopyrightAct2022.txt
- Identity: Copyright Act, 2022 (Act No. 8), Federal Republic of Nigeria
  Official Gazette No. 56, Vol. 110, 27 March 2023
- Commencement: 17 March 2023
- Encoding: UTF-8
- Line count: 3039 (PowerShell Get-Content .Count; trailing newline)
- SHA-256: 11A195164E989FE6A3EA745DD4BA5B7615AEE4050213257768432D4C2F39D52E
- Extraction: embedded OCR from per-page scan archive (68 pages)

## Freeze declaration
This file is frozen as of Phase 0. It is stored read-only and MUST NOT be edited.
Any error discovered downstream is recorded in ERRATA.md and corrected only in
derived artifacts (data/act/clean/, data/derived/), never in this raw source.
Verify integrity at any time with:
  Get-FileHash data\act\raw\CopyrightAct2022.txt -Algorithm SHA256
Expected: 11A195164E989FE6A3EA745DD4BA5B7615AEE4050213257768432D4C2F39D52E

## Scan (verification source for numerals gate)
- File: data/act/pages/Copyright-Act-2022.pdf
- Format: PDF v1.7, 68 pages (embedded page scans)
- Size: 855272 bytes
- SHA-256: 78CC1821D5C0189F5E5567344B40B871AFE2E513D073D143E2DA8709690FFA6B
- Page mapping: PDF page N != gazette printed page (A-xxx). Record both in numerals_log.
- Verified so far: s.19(1)(a)-(e) and s.19(2) durations confirmed against PDF p.13 (gazette A-189/A-190). 70yr literary/artistic, 50yr sound recording/broadcast/audiovisual — matches OCR text.
- Page mapping: section_map.json 'page' field = scan page = PDF page (verified: s.19 -> 13). No offset.
- Held but NOT integrated (Phase 2 decision): Collective Management Regulations 2025 (31pp, image-only scan), Copyright (Levy) Order 2026 (8pp, image-only scan). Subsidiary legislation under s.88(6)(c)/s.97 and s.89. Evidence for the regulation-making-power finding; candidate second authority layer for future work.
