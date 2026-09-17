ECCV Research Package — English Edition
======================================
Prepared: September 17, 2026. Source data snapshot: September 12, 2026.

QUICK START ON WINDOWS
1. Right-click the ZIP and choose Extract All.
2. Open eccv/2026/eccv_2026_en.html in Microsoft Edge or Google Chrome.
3. Click a bubble or a ranked topic to browse papers. Search titles, authors or
   abstracts, expand an abstract, or follow a paper/PDF link.

The HTML is self-contained: scripts, data and fonts are embedded. No Python,
Node.js, installation or model API is needed for browsing. External paper/PDF
links require an internet connection. On a narrow screen, scroll the bubble
chart sideways. Search only filters the paper library, not the global counts.

CONTENTS
- eccv_2026_en.html: complete interactive visualization in English.
- dashboard-preview-en.png: desktop preview.
- eccv_2026_keyword_counts.csv: official topic counts, readable in Excel.
- reviewed.json: normalized 2026 paper records, topic counts and provenance.
- eccv-2026-*.json and eccv2026_accepted.html: original official source snapshots.
- PLAN.md: archived project plan in English.
- VISUALIZATION.md: methods and developer notes in English.
- prepare_visualization.py: reproducible data preparation from cached sources.
- dashboard/: editable visualization source and compiled HTTP build.
- ../2024/: separately retained 2024 database, exports and scraping scripts.
- ../../docs/source-package-manifest.json: packaged file sizes and SHA-256 hashes.

COUNTING
2026: 2,834 distinct main-conference papers, 18 official topic labels and 2,851
assignments. Seventeen papers have two labels; counts overlap. Each percentage
uses all 2,834 papers as its denominator. Circle area, not radius, is proportional
to count. Positions do not indicate similarity. No generated subtopics are used.
2024: 2,387 papers, kept separately. The included SQLite database is for 2024;
normalized 2026 records are in reviewed.json.

DEVELOPMENT
Open eccv_2026_en.html for normal use. dashboard/dist/index.html is a split build
and requires an HTTP server to load its JSON sidecar. Rebuilding source requires
the compatible Data plugin runtime or a properly configured source environment;
the plugin, Node/Python runtimes and browser tooling are not bundled.
HPC paths in validation scripts or inherited developer guides refer to the
original environment and may need adjustment on Windows.
Browser caches, Python dependencies, duplicated exports and 2024 per-page HTML/PDF
caches are omitted to keep this package compact. Original source records,
abstract-repair provenance and font licensing are included.
