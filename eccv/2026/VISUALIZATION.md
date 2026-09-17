# ECCV 2026 topic visualization — English edition

Use `eccv_2026_en.html` for offline viewing in Edge or Chrome. See `Windows_README.txt` for package contents.

## Data and semantics

The September 12, 2026 official-source snapshot contains 2,834 distinct main-conference papers with nonempty original abstracts. Match official accepted-page poster IDs against the event JSON. `id` is the poster-event ID and `paperId` is the submission `sourceid`. Oral and Spotlight presentation events are not additional papers.

Deduplicate a paper's keywords, then count each paper once within each official keyword category. This yields 18 topics and 2,851 assignments: 17 papers have two topics. Shares divide by 2,834. Preserve all original official categories; abbreviated bubble labels do not redefine them. The ranking and hover text retain full English names.

Circle radii are proportional to the square root of count, so areas are proportional to count. A deterministic packing algorithm assigns positions for readability only, not semantic similarity. The original Chinese and English editions have identical paper records, topic counts and circle geometry.

Selecting a topic filters the paper library. Search matches titles, authors and abstracts within that selection and does not change the conference-level statistics. All topics clears the selection and search. Results show 12 papers per page. Abstracts remain original author text; the translation added no model-generated paper summaries or classifications.

## Source and development

`dashboard/src/content/dashboard/` contains authored React/CSS; `dashboard/src/data.json` contains reviewed evidence and source provenance. `prepare_visualization.py` validates the cached source population and reproduces normalized records and the topic CSV using the English topic display configuration in `topic_display.json`. Replacing the data in the app requires a separate deliberate update; the script does not silently alter an already-built artifact.

The app uses the Data plugin prebuilt runtime. Build with `data-app.mjs build --project-dir <project> --separate-data`, then export with `data-app.mjs export-offline --project-dir <project> --output <project>/.data-app-offline/exports/eccv_2026_en.html`. Serve the whole `dist` directory for HTTP preview; use the single HTML export for offline viewing. The compatible runtime and language environments are not included.

Font license: `dashboard/src/content/assets/FONT-LICENSE.txt`.

## Validation

The English UI is checked for untranslated Chinese interface strings, 18 rendered circles, filtering to the largest and smallest topics (247 and 84), return to all 2,834 papers, abstract expansion, no-result search, pagination, mobile overflow and browser runtime errors. The rendered label bounds are checked against each circle. English source definitions and counting rules are retained in the source inspector. See `visual_checks_en.json` for checks actually completed.
