# ECCV 2024 paper database

Scope: ECCV 2024 main conference, excluding workshops. Source: https://www.ecva.net/papers.php and its linked paper detail pages.

The `abstract` field is the original English abstract published on ECVA, with whitespace normalized. It is not an AI-generated summary or translation. No language model API is used.

Files:
- `eccv_2024.sqlite`: SQLite database; `papers` stores metadata and `papers_fts` provides FTS5 full-text search.
- `eccv_2024_papers.csv`: UTF-8 with BOM, suitable for spreadsheet import.
- `eccv_2024_papers.jsonl`: one complete paper record per line.
- `database_validation.json`: completeness and database integrity checks.
- `html_cache/`: local detail-page cache created when the collector runs; not bundled or tracked.

Fields: paper_id (ECVA submission ID), year, title, abstract, authors (source text), url (detail page), pdf_url, doi_url, supplement_url, fetched_at_utc.

Re-run or resume from the repository root (requires network access):

```bash
python3 eccv/2024/build_database.py
```

Six download workers, a brief delay after each request, four attempts per page, a local HTML cache, and immediate database commits allow interrupted runs to resume. Only HTML is downloaded, not PDFs. Failed URLs appear in the validation JSON.

Search in Python:

```python
import sqlite3
con = sqlite3.connect('eccv/2024/eccv_2024.sqlite')
rows = con.execute('''
    SELECT p.title, p.abstract, p.url
    FROM papers_fts JOIN papers p ON p.paper_id = papers_fts.rowid
    WHERE papers_fts MATCH ? ORDER BY rank LIMIT 20
''', ('"machine unlearning"',)).fetchall()
```

Two ECVA detail pages (IDs 7137 and 7743) contain `./abstract` instead of an abstract. Their abstracts were extracted from the official PDFs with pypdf and saved in `abstract_overrides.json`, automatically applied on reruns. The `abstract_provenance` table records the source and method; CSV/JSONL also include `abstract_source_url`. Only these two PDFs were downloaded.
