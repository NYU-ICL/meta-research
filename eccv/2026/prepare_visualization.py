"""Reproduce English data exports from the included official source snapshots."""
import collections,csv,json,re
from pathlib import Path
P=Path(__file__).resolve().parent
raw=json.loads((P/'eccv-2026-orals-posters.json').read_text())['results']
abstracts=json.loads((P/'eccv-2026-abstracts.json').read_text())
accepted=set(re.findall(r'/virtual/2026/poster/(\d+)',(P/'eccv2026_accepted.html').read_text()))
rows=[r for r in raw if str(r['id']) in accepted]
assert len(rows)==len({r['sourceid'] for r in rows})==2834
counts=collections.Counter(k for r in rows for k in set(r['keywords']))
topics=json.loads((P/'topic_display.json').read_text())
assert set(counts)=={t['keyword'] for t in topics}
lookup={t['keyword']:t['id'] for t in topics}
for t in topics:
 t['count']=counts[t['keyword']];t['share']=t['count']/len(rows)
papers=[dict(id=r['id'],paperId=r['sourceid'],title=r['name'],authors=', '.join(x['fullname'] for x in r['authors']),abstract=abstracts[str(r['id'])],topics=sorted(lookup[k] for k in set(r['keywords'])),url='https://eccv.ecva.net'+r['virtualsite_url'],pdf=r.get('paper_pdf_url') or '') for r in rows]
assert all(p['abstract'].strip() for p in papers)
snapshot=json.loads((P/'reviewed.json').read_text())
snapshot['queries']['topics']['rows']=topics;snapshot['queries']['papers']['rows']=papers
(P/'reviewed.json').write_text(json.dumps(snapshot,ensure_ascii=False),encoding='utf-8')
with (P/'eccv_2026_keyword_counts.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['official_keyword','paper_count','share_of_all_papers']);w.writerows((t['keyword'],t['count'],t['share']) for t in topics)
print(f'Validated {len(papers)} unique papers, {len(topics)} official topics and {sum(counts.values())} assignments.')
