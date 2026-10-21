/* Review UI consumes Python findings; it does not recreate analytical rules. */
'use strict';
(() => {
 let previous, current, preview, completed=new Set(), filter='all';
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const download=(name,text)=>{const u=URL.createObjectURL(new Blob([text],{type:'text/markdown;charset=utf-8'}));const a=document.createElement('a');a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);};
 function paint(){
  const host=document.querySelector('#review-desk'); if(!host||!current)return;
  const items=current.items.filter(x=>filter==='all'||x.severity===filter);
  host.innerHTML=`<div class="review-heading"><div><span class="eyebrow">V2.1 / EVIDENCE TO HANDOFF</span><h2>Review desk</h2><p>${preview?'Synthetic preview — run Python to compute your inputs.':'Computed from your latest Python experiment.'} Mark what you have inspected, then export a handoff.</p></div><a href="https://github.com/m-qazi99/${esc(current.project)}/blob/main/docs/USER_GUIDE.md">User guide ↗</a></div><div class="review-toolbar"><label>Show priorities <select id="review-filter"><option value="all">All priorities</option><option value="high">Investigate</option><option value="review">Review</option><option value="info">Context</option></select></label><span id="review-progress" role="status">${completed.size}/${current.items.length} inspected</span><button id="review-export">Export reviewed handoff ↓</button></div><div class="review-items">${items.map(x=>`<label class="review-item ${esc(x.severity)}"><input type="checkbox" data-review="${esc(x.id)}" ${completed.has(x.id)?'checked':''}><span><small>${esc(x.severity==='high'?'INVESTIGATE':x.severity.toUpperCase())}</small><strong>${esc(x.title)}</strong><span>${esc(x.detail)}</span></span></label>`).join('')||'<p>No priorities in this category.</p>'}</div><p class="review-scope">${esc(current.scope)} Checks stay in memory and reset on a new experiment or reload. They do not alter inputs.</p>`;
  host.querySelector('#review-filter').value=filter;
  host.querySelector('#review-filter').onchange=e=>{filter=e.target.value;paint();};
  host.querySelectorAll('[data-review]').forEach(el=>el.onchange=()=>{el.checked?completed.add(el.dataset.review):completed.delete(el.dataset.review);host.querySelector('#review-progress').textContent=`${completed.size}/${current.items.length} inspected`;});
  host.querySelector('#review-export').onclick=()=>{let text=`# ${current.name} — reviewed handoff\n\n${preview?'Synthetic preview.':'Python-computed experiment.'}\n\n${current.scope}\n\n`;for(const x of current.items)text+=`- [${completed.has(x.id)?'x':' '}] [${x.severity.toUpperCase()}] ${x.title.replace(/[\r\n]/g,' ')}\n  ${x.detail.replace(/[\r\n]/g,' ')}\n`;download('reviewed-handoff.md',text);};
 }
 document.addEventListener('workbench:result',e=>{
  if(e.detail.result===previous)return;previous=e.detail.result;current=previous?.review;preview=e.detail.preview;completed=new Set();filter='all';
  if(!current)return;
  let host=document.querySelector('#review-desk');if(!host){host=document.createElement('section');host.id='review-desk';host.className='review-desk';host.setAttribute('aria-label','Review desk');document.querySelector('#workspace').after(host);}
  paint();
 });
})();
