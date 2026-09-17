#!/usr/bin/env python3
"""Download original ECVA abstracts. Resumable, cached, no model/API required."""
import csv
import json
import re
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / 'html_cache'

class Detail(HTMLParser):
    def __init__(self, url):
        super().__init__(convert_charrefs=True)
        self.url, self.fields, self.links, self.stack = url, {}, {}, []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'div':
            self.stack.append(attrs.get('id'))
        if tag == 'a':
            href = urljoin(self.url, attrs.get('href', ''))
            if href.endswith('.pdf'):
                self.links['supplement_url' if '-supp.pdf' in href else 'pdf_url'] = href
            elif 'link.springer.com/chapter/' in href:
                self.links['doi_url'] = href
    def handle_endtag(self, tag):
        if tag == 'div' and self.stack:
            self.stack.pop()
    def handle_data(self, data):
        for key in ('papertitle', 'abstract', 'authors'):
            if key in self.stack:
                self.fields.setdefault(key, []).append(data)
    def value(self, key):
        return ' '.join(''.join(self.fields.get(key, [])).split())

def fetch(row):
    pid = re.search(r'/([0-9]+)_ECCV_', row['url']).group(1)
    path = CACHE / (pid + '.html')
    for attempt in range(4):
        try:
            if path.exists():
                html = path.read_text(encoding='utf-8')
            else:
                req = Request(row['url'], headers={'User-Agent': 'Academic-metadata-collector/1.0'})
                with urlopen(req, timeout=40) as response:
                    html = response.read().decode('utf-8')
                time.sleep(0.25)
            p = Detail(row['url'])
            p.feed(html)
            title, abstract = p.value('papertitle'), p.value('abstract')
            if not title or not abstract or not p.links.get('pdf_url'):
                raise ValueError('Missing title, abstract or PDF URL')
            path.write_text(html, encoding='utf-8')
            return {'paper_id': int(pid), 'year': 2024, 'title': title,
                    'abstract': abstract, 'authors': p.value('authors').rstrip('; '),
                    'url': row['url'], 'pdf_url': p.links.get('pdf_url'),
                    'doi_url': p.links.get('doi_url'), 'supplement_url': p.links.get('supplement_url'),
                    'fetched_at_utc': datetime.now(timezone.utc).isoformat()}
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)

def main():
    CACHE.mkdir(exist_ok=True)
    with (ROOT / 'eccv_2024_titles.csv').open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    db = sqlite3.connect(ROOT / 'eccv_2024.sqlite')
    db.execute('''CREATE TABLE IF NOT EXISTS papers (
        paper_id INTEGER PRIMARY KEY, year INTEGER NOT NULL, title TEXT NOT NULL,
        abstract TEXT NOT NULL, authors TEXT, url TEXT UNIQUE NOT NULL, pdf_url TEXT,
        doi_url TEXT, supplement_url TEXT, fetched_at_utc TEXT)''')
    existing = {r[0] for r in db.execute('SELECT url FROM papers WHERE length(abstract)>0')}
    pending = [r for r in rows if r['url'] not in existing]
    print(f'Total {len(rows)}; already saved {len(existing)}; pending {len(pending)}', flush=True)
    errors, done = [], len(existing)
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(fetch, row): row for row in pending}
        for future in as_completed(futures):
            try:
                record = future.result()
                db.execute('INSERT OR REPLACE INTO papers VALUES (?,?,?,?,?,?,?,?,?,?)', tuple(record.values()))
                db.commit()
                done += 1
            except Exception as exc:
                errors.append({'url': futures[future]['url'], 'error': str(exc)})
            if (done + len(errors)) % 100 == 0:
                print(f'Saved {done}/{len(rows)}; errors {len(errors)}', flush=True)
    overrides_path = ROOT / 'abstract_overrides.json'
    db.execute('CREATE TABLE IF NOT EXISTS abstract_provenance (paper_id INTEGER PRIMARY KEY, source_url TEXT, method TEXT)')
    db.execute("INSERT OR IGNORE INTO abstract_provenance SELECT paper_id,url,'ECVA detail page abstract' FROM papers")
    if overrides_path.exists():
        for pid, replacement in json.loads(overrides_path.read_text()).items():
            db.execute('UPDATE papers SET abstract=? WHERE paper_id=?', (replacement['abstract'], int(pid)))
            db.execute('INSERT OR REPLACE INTO abstract_provenance VALUES (?,?,?)', (int(pid), replacement['source_url'], replacement['method']))
    db.commit()
    cursor = db.execute('SELECT p.*, a.source_url AS abstract_source_url FROM papers p JOIN abstract_provenance a USING(paper_id) ORDER BY paper_id')
    fields = [c[0] for c in cursor.description]
    records = [dict(zip(fields, r)) for r in cursor]
    with (ROOT / 'eccv_2024_papers.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)
    with (ROOT / 'eccv_2024_papers.jsonl').open('w', encoding='utf-8') as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    db.execute('CREATE VIRTUAL TABLE IF NOT EXISTS papers_fts USING fts5(title, abstract, authors)')
    db.execute('DELETE FROM papers_fts')
    db.execute('INSERT INTO papers_fts(rowid,title,abstract,authors) SELECT paper_id,title,abstract,authors FROM papers')
    db.commit()
    report = {'expected': len(rows), 'saved': len(records), 'errors': errors,
              'missing_urls': sorted({r['url'] for r in rows} - {r['url'] for r in records}),
              'empty_abstracts': sum(not r['abstract'].strip() for r in records),
              'placeholder_abstracts': sum(r['abstract'].strip() == './abstract' for r in records),
              'integrity_check': db.execute('PRAGMA integrity_check').fetchone()[0]}
    (ROOT / 'database_validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report), flush=True)
    db.close()
    if errors or report['missing_urls']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
