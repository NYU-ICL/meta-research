from playwright.sync_api import sync_playwright
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
import json,re
P=Path(__file__).resolve().parent
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(P/'dashboard/dist')))
Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,args=['--no-sandbox']);page=b.new_page(viewport={'width':1440,'height':1550})
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(f'http://127.0.0.1:{server.server_port}',wait_until='networkidle');page.locator('.eccv-node').first.wait_for();page.evaluate('document.fonts.ready')
 assert page.locator('.eccv-node').count()==18
 assert not re.search('[\u4e00-\u9fff]',page.locator('.eccv-page').inner_text())
 overflow=page.locator('.eccv-node').evaluate_all('''nodes=>nodes.flatMap(n=>{const r=+n.querySelector('circle').getAttribute('r');return [...n.querySelectorAll('text')].filter(t=>{const b=t.getBBox();return Math.hypot(Math.max(Math.abs(b.x),Math.abs(b.x+b.width)),Math.max(Math.abs(b.y),Math.abs(b.y+b.height)))>r-1;}).map(t=>({topic:n.dataset.topicId,text:t.textContent}));})''')
 print('Circle label overflows',overflow,flush=True)
 page.screenshot(path=str(P/'dashboard-preview-en.png'))
 page.locator('[data-topic-id="t01"]').click();assert page.locator('.eccv-pagination').inner_text().startswith('1–12 / 247')
 page.locator('.eccv-paper summary').first.click();assert len(page.locator('.eccv-abstract').first.inner_text())>100
 page.locator('.eccv-library').scroll_into_view_if_needed();page.screenshot(path=str(P/'dashboard-detail-en.png'))
 page.locator('[data-topic-id="t18"]').click();assert page.locator('.eccv-pagination').inner_text().startswith('1–12 / 84')
 page.get_by_role('button',name='All topics',exact=True).click();assert page.locator('.eccv-pagination').inner_text().startswith('1–12 / 2,834')
 page.get_by_role('textbox',name='Search paper titles, authors or abstracts').fill('zzzznoresultxyz');assert page.locator('.eccv-empty').is_visible()
 page.get_by_role('textbox',name='Search paper titles, authors or abstracts').fill('');page.get_by_role('button',name='Next',exact=True).click();assert page.locator('.eccv-pagination').inner_text().startswith('13–24 / 2,834')
 page.set_viewport_size({'width':390,'height':844});page.evaluate('scrollTo(0,0)');page.screenshot(path=str(P/'dashboard-mobile-en.png'));assert not page.evaluate('document.documentElement.scrollWidth>innerWidth');assert not errors
 result={'rendered_bubbles':18,'largest_topic':247,'smallest_topic':84,'reset_all':2834,'english_ui':True,'abstract_search_pagination':True,'mobile_no_page_overflow':True,'runtime_errors':errors,'circle_label_overflows':overflow}
 (P/'visual_checks_en.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
 b.close()
server.shutdown()
