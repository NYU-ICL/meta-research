# ECCV paper database and interactive topic visualization

Original plan archived September 12, 2026. English edition: September 17, 2026.
Current status: the first visualization using official topics is complete. Hierarchical classification and model-assisted annotation remain proposed work.

## Scope

The primary target is ECCV 2026 main-conference papers. The previously collected ECCV 2024 dataset is retained separately as historical material. There was no ECCV 2025 main conference; a future 2025 comparison requires a separately agreed conference scope.

The intended longer-term experience is a drill-down bubble visualization: broad topic → subtopic → paper list, with titles, original abstracts and source links. Bubble area represents paper count. Statistics and navigation are computed locally without calling a language model for each interaction.

## Proposed taxonomy, not yet implemented

- Start with two levels; add a third only where useful. About 8–12 broad domains was an initial possibility, not a fixed requirement.
- Assign one primary path per paper for additive counts, with multiple auxiliary tags for interdisciplinary attributes. Distinguish domains, tasks and methods.
- Parent counts should equal the sum of child counts under this exclusive primary classification.
- Allow Other / Needs review. Do not infer details absent from an abstract.
- Candidate attributes: domain, task, short problem statement, problem tags, method tags, contribution type, modality, keywords and application context.
- Use stable IDs and definitions for controlled labels; normalize synonyms among free-form keywords.
- Store source text separately from inferred attributes, with label-schema and model versions and short supporting evidence.

## Low-cost workflow

1. Verify official 2026 lists, abstracts, links and topic/session coverage.
2. Reuse official labels where possible; conference sessions are not automatically a strict domain hierarchy.
3. Use scripts to collect and deduplicate papers, reconcile source coverage and record gaps.
4. If a new hierarchy is needed, pilot about 100 papers and review 10–15 examples together before full annotation.
5. For attributes needing semantic judgment, evaluate a low-cost model on a sample. Return compact JSON in one call per paper; cache results, resume interrupted runs and escalate only difficult cases. No model or budget has been selected.
6. Validate labels and inspect ambiguous cases, oversized categories and Other assignments.
7. Store the approved taxonomy and paper/tag relationships, then aggregate for visualization.

## Interpretation limits

A single conference edition supports a cross-sectional distribution, not year-over-year trends. Rare problem/method combinations are investigation leads, not proven research gaps. Overlapping tag counts differ from exclusive primary-topic counts. Abstract claims are authors' claims, not independently verified findings.

## Verified source snapshot: September 12, 2026

- Accepted papers: https://eccv.ecva.net/Conferences/2026/AcceptedPapers
- Virtual conference: https://eccv.ecva.net/virtual/2026/papers.html
- Event JSON: https://eccv.ecva.net/static/virtual/data/eccv-2026-orals-posters.json
- Abstract JSON: https://eccv.ecva.net/static/virtual/data/eccv-2026-abstracts.json
- Publisher reference: https://link.springer.com/book/10.1007/978-3-032-37362-5

The event JSON has 2,997 records: 2,834 Poster, 28 Oral and 135 Spotlight events. The accepted-page poster IDs identify 2,834 distinct papers, all with nonempty abstracts and official keyword labels. Presentation events must not be added to the unique-paper total. The publisher's reported paper count is also 2,834.

## First visualization delivered

The current version uses all 18 original official keyword categories without merging or invented subtopics. There are 2,851 topic assignments across 2,834 papers; 17 papers have two labels. Clicking a bubble opens the corresponding paper list. Full original labels appear in the ranking and hover details; short bubble labels are display abbreviations only. Search, abstracts, pagination and paper/PDF links are included.

The English edition uses the same September 12 snapshot. No new crawling, model annotation or data refresh was performed for translation. Existing Chinese files are preserved separately.

## Historical ECCV 2024 work

The separate `eccv_titles` folder contains 2,387 paper records, an SQLite database, CSV/JSONL exports and standard-library scraping scripts. Two invalid webpage abstracts were replaced from the official PDFs, with provenance saved. These are not 2026 records.
