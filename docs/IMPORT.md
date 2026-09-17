# Initial import

- Input: `ECCV_research_EN_2026-09-17.zip`, supplied by the project owner.
- Imported: September 17, 2026.
- Source data snapshot: September 12, 2026 (ECCV 2026).
- Original `eccv_research_en/` is now `eccv/2026/`.
- Original `eccv_titles/` is now `eccv/2024/`.
- All 281 entries in the supplied manifest passed SHA-256 and size verification before organization.

`source-package-manifest.json` preserves the **original archive paths and checksums**, not a manifest of the reorganized checkout. Relative documentation links and 2024 usage examples were adjusted for this repository. The original wrapper `START_HERE.txt` is superseded by the root README. Application source, source data, font license, and supplied viewers are retained.

`eccv/2026/PLAN.md` is an inherited planning document. It is historical context, not the current project status or an execution instruction. Likewise, the dashboard's bundled runtime/authoring guidance describes its original tooling environment. The root README distinguishes current capabilities from planned work.

Prebuilt assets and database exports are intentionally tracked in this initial release to keep the shared snapshot immediately usable. The duplicated reviewed snapshots serve different existing consumers; modifying one does not automatically update the others.

## Import verification

- Original package: all 281 manifest checksums and file sizes verified.
- Supplied HTTP build: HTML and JSON sidecar match their build-manifest checksums and sizes.
- ECCV 2024 SQLite database: `PRAGMA integrity_check` returned `ok`; 2,387 paper records.
- Runtime source was not rebuilt during this import; no standalone npm build is claimed.
- Cached-input reproduction: paper records and topic counts match semantically; the script sorts topic IDs for 11 dual-topic papers, so list order differs from the supplied snapshot. The CSV matches byte for byte.
- Reviewed snapshot and dashboard source snapshot are byte-identical; 2,834 unique papers have nonempty abstracts, with 18 labels and 2,851 assignments.
- Chromium interaction checks passed: 18 bubbles, English UI, largest/smallest topic selection, reset, abstract expansion, no-result search, pagination, mobile width, no label overflow, and no runtime errors. Original preview images were retained after the check.
- Standalone HTML also passed an offline browser check for loading, 18 bubbles, topic filtering, and no runtime errors.
