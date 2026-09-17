import React, {useState, useMemo} from 'react';
import {DataComponent, useDataApp, SectionHeader} from '../../data-app-public.jsx';
import './dashboard.css';
const fmt=n=>n.toLocaleString('en-US');
export function DashboardContent(){
 const {queries,visible}=useDataApp();
 const topics=queries.topics.rows, papers=queries.papers.rows;
 const [selected,setSelected]=useState(null),[hover,setHover]=useState(null),[search,setSearch]=useState(''),[page,setPage]=useState(0);
 const topic=topics.find(t=>t.id===selected), pointed=topics.find(t=>t.id===hover)||topic;
 const shown=useMemo(()=>papers.filter(p=>(!selected||p.topics.includes(selected))&&(!search.trim()||[p.title,p.abstract,p.authors].join(' ').toLowerCase().includes(search.trim().toLowerCase()))),[papers,selected,search]);
 const choose=id=>{setSelected(id);setPage(0);setSearch('');};
 const pageRows=shown.slice(page*12,(page+1)*12);
 return <div className="eccv-page">
  <DataComponent id="eccv-overview" queryId="papers" kind="metrics" title="Conference overview" displayRows={papers}>
   <div className="eccv-stats" data-reviewed-rows>
    <div><span>Main-conference papers</span><strong>{fmt(papers.length)}<small>papers</small></strong></div>
    <div><span>Official topics</span><strong>{topics.length}<small>topics</small></strong></div>
    <div><span>Topic assignments</span><strong>{fmt(topics.reduce((a,t)=>a+t.count,0))}<small>assignments</small></strong></div>
    <p>ECCV 2026 · Malmö<br/><span>September 8–12, 2026<br/>Data snapshot: September 12, 2026</span></p>
   </div>
  </DataComponent>
  <div className="eccv-map-grid">
   {visible('eccv-bubbles')&&<DataComponent id="eccv-bubbles" queryId="topics" kind="custom" title="Research topic bubbles" displayRows={topics} sourceRows={topics} variant="card">
    <p className="eccv-note" data-editable-id="eccv:area-note">Area ∝ paper count · Click to explore · Position does not encode topic similarity</p>
    <p className="eccv-mobile-hint">← → Scroll sideways to explore all bubbles</p><div className="eccv-svg-scroll"><svg className="eccv-bubbles" viewBox="0 0 940 720" role="group" aria-label="18 official research topics; bubble area represents paper count">
     {topics.map(t=><g key={t.id} data-topic-id={t.id} transform={`translate(${t.x},${t.y})`} role="button" tabIndex={0} aria-pressed={selected===t.id} aria-label={`${t.label}, ${t.count} papers; ${(t.share*100).toFixed(1)}%`} onClick={()=>choose(t.id)} onKeyDown={e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();choose(t.id);}}} onMouseEnter={()=>setHover(t.id)} onMouseLeave={()=>setHover(null)} onFocus={()=>setHover(t.id)} onBlur={()=>setHover(null)} className={`eccv-node ${selected===t.id?'is-selected':''} ${hover===t.id?'is-hover':''}`}>
      <title>{t.keyword} — {t.count} papers ({(t.share*100).toFixed(1)}%)</title>
      <circle r={t.r} /><text className="eccv-node-count" style={{fontSize:t.r<53?22:24}} y={-17} textAnchor="middle">{t.count}</text>
      {t.lines.map((line,i)=><text key={line} className="eccv-node-label" style={{fontSize:t.r<53?10:11}} y={i*14} textAnchor="middle">{line}</text>)}
     </g>)}
    </svg></div>
    <div className="eccv-hover" aria-live="polite">{pointed?<><strong>{pointed.label}</strong><span>{pointed.keyword}</span><b>{pointed.count} papers · Share of all papers: {(pointed.share*100).toFixed(2)}%</b></>:<><strong>Explore 18 official topics</strong><span>Hover for the full topic name and share; click to filter the paper library below.</span></>}</div>
    <p className="eccv-footnote">17 papers have two topic labels: 2,851 topic assignments across 2,834 unique papers. Counts follow the original official categories. Bubble labels are abbreviated; full names appear in the ranking and on hover.</p>
   </DataComponent>}
   {visible('eccv-rank')&&<DataComponent id="eccv-rank" queryId="topics" kind="custom" title="Topics by paper count" displayRows={topics} sourceRows={topics} variant="card">
    <div className="eccv-rank-head"><span>Official topics</span><span>Papers / share of all</span></div>
    <div className="eccv-rank" data-reviewed-rows>{topics.map((t,i)=><button key={t.id} className={selected===t.id?'active':''} onClick={()=>choose(t.id)} title={t.keyword} aria-label={`${t.label} ${t.count} papers`}>
     <span className="eccv-rank-index">{String(i+1).padStart(2,'0')}</span><span className="eccv-rank-label">{t.label}<span className="eccv-bar"><i style={{width:`${t.count/topics[0].count*100}%`}}/></span></span><span className="eccv-rank-value">{t.count}<small>{(t.share*100).toFixed(1)}%</small></span>
    </button>)}</div>
   </DataComponent>}
  </div>
  <section className="eccv-library">
   <SectionHeader id="eccv:library-heading" title="Paper library"/>
   <div className="eccv-library-tools"><div className="eccv-selection"><button onClick={()=>choose(null)} className={!selected?'active':''}>All topics</button>{topic&&<span>{topic.label}<button onClick={()=>choose(null)} aria-label="Clear topic filter">×</button></span>}</div><input aria-label="Search paper titles, authors or abstracts" placeholder="Search titles, authors or abstracts…" value={search} onChange={e=>{setSearch(e.target.value);setPage(0);}}/></div>
   {topic&&<p className="eccv-original">{topic.keyword}</p>}
   {visible('eccv-paper-list')&&<DataComponent id="eccv-paper-list" queryId="papers" kind="table" title={`${fmt(shown.length)} papers${search?' · search results':''}`} displayRows={shown} sourceRows={shown}>
    <div className="eccv-paper-list" data-reviewed-rows>
     {!shown.length&&<div className="eccv-empty">No matching papers. Try another search or clear the topic filter.</div>}
     {pageRows.map(p=><article key={p.id} className="eccv-paper"><div className="eccv-paper-main"><a className="eccv-paper-title" href={p.url} target="_blank" rel="noreferrer">{p.title}<span>↗</span></a><p className="eccv-authors">{p.authors}</p><div className="eccv-tags">{p.topics.map(id=><button onClick={()=>choose(id)} key={id}>{topics.find(t=>t.id===id)?.label}</button>)}</div><details><summary>Read abstract</summary><p className="eccv-abstract">{p.abstract}</p></details></div><div className="eccv-paper-links"><span>#{p.paperId}</span><a href={p.url} target="_blank" rel="noreferrer">Paper page ↗</a>{p.pdf&&<a href={p.pdf} target="_blank" rel="noreferrer">PDF ↗</a>}</div></article>)}
    </div>
    <div className="eccv-pagination"><span>{shown.length?`${page*12+1}–${Math.min((page+1)*12,shown.length)} / ${fmt(shown.length)}`:'0 papers'}</span><div><button disabled={page===0} onClick={()=>setPage(page-1)}>Previous</button><button disabled={(page+1)*12>=shown.length} onClick={()=>setPage(page+1)}>Next</button></div></div>
   </DataComponent>}
  </section>
  <p className="eccv-source">Source: <a href="https://eccv.ecva.net/Conferences/2026/AcceptedPapers" target="_blank" rel="noreferrer">ECCV 2026 accepted papers</a> and official conference data · Original author abstracts · No model-generated classification</p>
 </div>;
}
