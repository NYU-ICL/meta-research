#!/usr/bin/env python3
"""Extract ECCV 2024 main-conference titles from ECVA; standard library only."""
import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urljoin

SOURCE = 'https://www.ecva.net/papers.php'

class Papers(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self.href = None
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href', '')
            if 'papers/eccv_2024/papers_ECCV/html/' in href:
                self.href, self.parts = href, []

    def handle_data(self, data):
        if self.href is not None:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == 'a' and self.href is not None:
            title = ' '.join(''.join(self.parts).split())
            if not title:
                raise ValueError('Empty paper title')
            self.rows.append({'title': title, 'url': urljoin(SOURCE, self.href)})
            self.href = None

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--html', type=Path, help='Use a previously downloaded ECVA list')
    ap.add_argument('--out', type=Path, default=Path(__file__).resolve().parent)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    if args.html:
        html = args.html.read_text(encoding='utf-8')
    else:
        req = Request(SOURCE, headers={'User-Agent': 'ECCV-title-export/1.0'})
        with urlopen(req, timeout=60) as response:
            html = response.read().decode('utf-8')
    parser = Papers()
    parser.feed(html)
    rows = parser.rows
    if not rows or len({r['url'] for r in rows}) != len(rows):
        raise ValueError('No papers or duplicate paper URLs; inspect source before exporting')
    (args.out / 'eccv_2024_titles.txt').write_text(''.join(r['title'] + '\n' for r in rows), encoding='utf-8')
    with (args.out / 'eccv_2024_titles.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'url'])
        writer.writeheader()
        writer.writerows(rows)
    counts = Counter(r['title'] for r in rows)
    metadata = {'source': SOURCE, 'year': 2024, 'scope': 'main conference; excludes workshops',
                'exported_at_utc': datetime.now(timezone.utc).isoformat(), 'paper_count': len(rows),
                'unique_titles': len(counts), 'duplicate_titles': {k:v for k,v in counts.items() if v > 1}}
    (args.out / 'metadata.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(metadata, ensure_ascii=False))

if __name__ == '__main__':
    main()
