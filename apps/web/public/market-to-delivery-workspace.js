/* Read-only catalog + browser-local intake draft. No customer POST or approval. */
(() => {
  const tag = 'dealix-catalog-workspace';
  if (customElements.get(tag)) return;
  const copy = {
    ar: {
      title: 'من الاحتياج إلى خطة تنفيذ',
      intro: 'استكشف الفرضيات، حدد المشكلة، وجهز ملف التشخيص.',
      note: 'كتالوج بحثي، ليس إثبات قدرة تسليم. التسعير والالتزام بعد التشخيص والمراجعة.',
      arms: 'أذرع خدمات', sectors: 'قطاعات للبحث', projects: 'فرضية مشروع',
      search: 'البحث', sector: 'القطاع', all: 'جميع القطاعات',
      select: 'جهز التشخيص', measure: 'مؤشر قبول مقترح', hypothesis: 'فرضية تحتاج تحققًا',
      specialist: 'مراجعة تخصصية', empty: 'لا توجد نتائج مطابقة.',
      intake: 'مسودة الاحتياج', privacy: 'مسودة محلية في المتصفح فقط. لا تدخل أسرارًا أو بيانات حساسة. لم يتم إرسال طلب إلى Dealix.',
      tenant: 'معرف مساحة العمل للمراجعة',
      problem: 'ما المشكلة؟', workflow: 'كيف يسير العمل حاليًا؟',
      baseline: 'خط الأساس ومصدر قياسه', outcome: 'النتيجة المراد قياسها',
      constraints: 'قيود البيانات والوقت والنطاق',
      authorized: 'أؤكد أن لدي صلاحية استخدام المدخلات للتحضير، وليس هذا إذنًا للتواصل التسويقي.',
      download: 'حفظ مسودة JSON', clear: 'مسح المدخلات',
      saved: 'تم تجهيز ملف محلي؛ لم يتم إرسال أي شيء أو اعتماد عرض.',
      loading: 'جاري تحميل الكتالوج...', error: 'تعذر تحميل الكتالوج. لا نتائج مفترضة.',
    },
    en: {
      title:'From need to delivery plan', intro:'Explore hypotheses. Define the problem. Prepare the diagnostic.',
      note:'Research catalog, not proof of delivery capacity. Pricing and commitment follow discovery and review.',
      arms:'Service arms', sectors:'Research sectors', projects:'Project hypotheses', search:'Search', sector:'Sector', all:'All sectors',
      select:'Prepare diagnostic', measure:'Suggested acceptance measure', hypothesis:'Hypothesis requiring validation', specialist:'Specialist review',
      empty:'No matching hypotheses.', intake:'Requirement draft', privacy:'Browser-local draft only. Do not enter secrets or sensitive data. No request has been sent to Dealix.',
      tenant:'Workspace reference for review', problem:'What is the problem?', workflow:'How does the workflow operate today?',
      baseline:'Baseline and measurement source', outcome:'Outcome to measure', constraints:'Data, time and scope constraints',
      authorized:'I am authorized to use these inputs for preparation. This is not marketing consent.',
      download:'Save JSON draft', clear:'Clear inputs', saved:'Local file prepared. Nothing was sent and no quote was approved.',
      loading:'Loading catalog...', error:'Catalog could not be loaded. No assumed results.',
    },
  };
  const css = `:host{display:block;color:#0f172a;font-family:inherit;--teal:#164e63;--cyan:#22d3ee}*{box-sizing:border-box}button,input,select,textarea{font:inherit}button{cursor:pointer}button:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible{outline:3px solid #0891b2;outline-offset:3px}.wrap{max-width:1200px;margin:auto;padding:32px 20px}.hero{background:#0f172a;color:#f8fafc;border-radius:24px;padding:32px}.top{display:flex;align-items:center;justify-content:space-between;gap:16px}.brand{font-size:13px;letter-spacing:.12em;color:#22d3ee}.lang{border:1px solid #64748b;background:transparent;color:#f8fafc;padding:9px 16px;border-radius:10px}.hero h1{font-size:clamp(28px,4vw,44px);line-height:1.3;margin:24px 0 12px}.hero p{max-width:850px;line-height:1.9}.notice{font-size:14px;color:#cbd5e1}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:22px 0}.stat{border:1px solid #cbd5e1;border-radius:16px;padding:18px;background:white}.num{display:block;color:#164e63;font-size:32px;font-weight:700}.filters{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin:24px 0 12px}label{display:grid;gap:8px;font-size:14px;font-weight:600}input,select,textarea{width:100%;border:1px solid #94a3b8;border-radius:10px;background:white;color:#0f172a;padding:12px;min-height:44px}textarea{resize:vertical;min-height:88px}#count{font-size:14px;color:#475569}.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.card{border:1px solid #cbd5e1;border-radius:18px;padding:22px;background:#fff;display:flex;flex-direction:column;align-items:flex-start;gap:12px;overflow-wrap:anywhere}.card h2{font-size:19px;line-height:1.5;margin:0}.meta{color:#475569;font-size:13px}.badge{border-radius:20px;background:#ecfeff;color:#155e75;font-size:12px;padding:6px 10px}.card p{margin:0;line-height:1.7;font-size:14px}.choose,.save{background:#164e63;color:white;border:0;border-radius:10px;padding:12px 18px}.choose{margin-top:auto}.intake{margin-top:30px;border:1px solid #94a3b8;border-radius:20px;background:#f8fafc;padding:24px}.intake h2{margin:0 0 12px;font-size:26px}.fields{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:20px 0}.full{grid-column:1/-1}.check{display:flex;align-items:flex-start;gap:10px;line-height:1.7}.check input{width:20px;height:20px;min-height:20px;flex-shrink:0}.buttons{display:flex;gap:12px;flex-wrap:wrap}.clear{border:1px solid #94a3b8;background:white;border-radius:10px;padding:12px 18px}.status{white-space:pre-wrap;overflow-wrap:anywhere;font-size:14px;line-height:1.8}.path{color:#64748b;font-size:13px;margin:26px 0;line-height:1.8}@media(max-width:850px){.cards{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:580px){.wrap{padding:18px 12px}.hero{padding:24px 18px;border-radius:18px}.stats{gap:7px}.stat{padding:12px}.num{font-size:26px}.stat span:last-child{font-size:12px}.cards,.filters,.fields{grid-template-columns:1fr}.intake{padding:18px}.hero h1{font-size:29px}}`;

  class Workspace extends HTMLElement {
    connectedCallback() {
      this.lang = this.lang || 'ar'; this.selected = null;
      this.attachShadowIfNeeded();
      const status = document.createElement('p'); status.textContent = copy[this.lang].loading;
      status.setAttribute('role','status'); this.shadowRoot.replaceChildren(status);
      this.controller = new AbortController();
      fetch('/market-to-delivery-catalog.json', {signal:this.controller.signal, credentials:'same-origin'})
        .then(r => {if (!r.ok) throw new Error('catalog_unavailable'); return r.json();})
        .then(data => {
          if (data.status !== 'HYPOTHESES_NOT_PROVEN_DELIVERY' || !Array.isArray(data.sectors) || !Array.isArray(data.arms)) throw new Error('catalog_invalid');
          this.catalog = data; this.render();
        }).catch(e => {if (e.name !== 'AbortError') {status.textContent = copy[this.lang].error; this.shadowRoot.replaceChildren(status);}});
    }
    attachShadowIfNeeded(){if (!this.shadowRoot) this.attachShadow({mode:'open'});}
    disconnectedCallback(){this.controller?.abort();}
    render(){
      const c = copy[this.lang]; const root = this.shadowRoot;
      // Constant markup only. All data and user content use textContent/value.
      root.innerHTML = `<style>${css}</style><div class="wrap"><section class="hero"><div class="top"><strong class="brand">DEALIX / MARKET TO DELIVERY</strong><button class="lang" type="button"></button></div><h1></h1><p class="intro"></p><p class="notice"></p></section><section class="stats" aria-label="Catalog counts"></section><section class="filters"><label><span id="search-label"></span><input id="search" type="search" maxlength="120" /></label><label><span id="sector-label"></span><select id="sector"></select></label></section><p id="count" dir="ltr" role="status" aria-live="polite"></p><section class="cards"></section><section class="intake" hidden><h2 tabindex="-1"></h2><p id="selected"></p><p id="privacy"></p><form><div class="fields"></div><label class="check"><input id="authorized" type="checkbox" required/><span></span></label><div class="buttons"><button class="save" type="submit"></button><button class="clear" type="reset"></button></div></form><p class="status" role="status" aria-live="polite"></p></section><p class="path" dir="ltr">Signal &rarr; Diagnostic &rarr; Quote review &rarr; Verified start &rarr; Delivery &rarr; Customer proof</p></div>`;
      root.querySelector('.wrap').dir = this.lang === 'ar' ? 'rtl' : 'ltr';
      root.querySelector('.wrap').lang = this.lang;
      root.querySelector('h1').textContent = c.title;
      root.querySelector('.intro').textContent = c.intro;
      root.querySelector('.notice').textContent = c.note;
      const language=root.querySelector('.lang'); language.textContent=this.lang==='ar'?'English':'العربية';
      language.onclick=()=>{this.lang=this.lang==='ar'?'en':'ar';this.selected=null;this.render();};
      const total=this.catalog.sectors.reduce((n,s)=>n+s.projects.length,0);
      [[this.catalog.arms.length,c.arms],[this.catalog.sectors.length,c.sectors],[total,c.projects]].forEach(([n,label])=>{
        const card=document.createElement('article');card.className='stat';
        const value=document.createElement('span');value.className='num';value.textContent=String(n);
        const text=document.createElement('span');text.textContent=label;card.append(value,text);root.querySelector('.stats').append(card);
      });
      root.querySelector('#search-label').textContent=c.search;root.querySelector('#sector-label').textContent=c.sector;
      const select=root.querySelector('#sector');select.add(new Option(c.all,''));
      this.catalog.sectors.forEach(s=>select.add(new Option(s[this.lang==='ar'?'name_ar':'name_en'],s.id)));
      select.onchange=()=>this.renderCards();root.querySelector('#search').oninput=()=>this.renderCards();
      root.querySelector('.intake h2').textContent=c.intake;root.querySelector('#privacy').textContent=c.privacy;
      const fields=[['tenant_id',c.tenant,false],['problem',c.problem,true],['current_workflow',c.workflow,true],['baseline',c.baseline,true],['desired_outcome',c.outcome,true],['constraints',c.constraints,true]];
      fields.forEach(([name,label,multi])=>{
        const el=document.createElement('label');if(name==='problem')el.className='full';el.textContent=label;
        const input=document.createElement(multi?'textarea':'input');input.name=name;input.id=name;input.maxLength=multi?4000:80;
        input.setAttribute('data-ph-no-capture','');input.autocomplete='off';
        if(name==='problem'||name==='tenant_id')input.required=true;
        if(name==='tenant_id'){input.pattern='[A-Za-z0-9][A-Za-z0-9_.:-]{0,79}';input.dir='ltr';}
        el.append(input);root.querySelector('.fields').append(el);
      });
      root.querySelector('.check span').textContent=c.authorized;root.querySelector('.save').textContent=c.download;root.querySelector('.clear').textContent=c.clear;
      root.querySelector('form').onsubmit=event=>{event.preventDefault();this.saveDraft();};
      root.querySelector('form').onreset=()=>{root.querySelector('.status').textContent='';};
      this.renderCards();
    }
    renderCards(){
      const root=this.shadowRoot,c=copy[this.lang],query=root.querySelector('#search').value.toLowerCase().trim(),sid=root.querySelector('#sector').value;
      const cards=root.querySelector('.cards');cards.replaceChildren();let count=0;
      this.catalog.sectors.filter(s=>!sid||s.id===sid).forEach(s=>s.projects.filter(p=>`${p.name} ${s.name_ar} ${s.name_en} ${p.acceptance_measure}`.toLowerCase().includes(query)).forEach(p=>{
        count++;const card=document.createElement('article');card.className='card';
        const meta=document.createElement('span');meta.className='meta';meta.textContent=s[this.lang==='ar'?'name_ar':'name_en'];
        const title=document.createElement('h2');title.dir='auto';title.textContent=p.name;
        const badge=document.createElement('span');badge.className='badge';badge.textContent=c.hypothesis;
        const metric=document.createElement('p');const metricLabel=document.createElement('span');metricLabel.textContent=c.measure;metricLabel.style.display='block';const metricValue=document.createElement('span');metricValue.dir='ltr';metricValue.style.display='block';metricValue.textContent=p.acceptance_measure;metric.append(metricLabel,metricValue);
        const button=document.createElement('button');button.type='button';button.className='choose';button.textContent=c.select;
        button.onclick=()=>{this.selected=p;const panel=root.querySelector('.intake');panel.hidden=false;root.querySelector('#selected').textContent=p.name;root.querySelector('.status').textContent='';panel.scrollIntoView({block:'start'});panel.querySelector('h2').focus();};
        card.append(meta,title,badge,metric);
        if(s.domain_review){const review=document.createElement('span');review.className='meta';review.textContent=c.specialist;card.append(review);}
        card.append(button);cards.append(card);
      }));
      root.querySelector('#count').textContent=count?`${count} / ${this.catalog.sectors.reduce((n,s)=>n+s.projects.length,0)}`:c.empty;
    }
    saveDraft(){
      const root=this.shadowRoot;if(!this.selected)return;
      const form=root.querySelector('form');if(!form.reportValidity())return;
      const payload={request_id:'web-'+Array.from(crypto.getRandomValues(new Uint8Array(16)), value=>value.toString(16).padStart(2,'0')).join(''),project_id:this.selected.id,evidence_refs:[],data_authorized:root.querySelector('#authorized').checked};
      ['tenant_id','problem','current_workflow','baseline','desired_outcome','constraints'].forEach(key=>{payload[key]=root.querySelector('#'+key).value.trim()||null;});
      if(!payload.problem || !payload.tenant_id)return;
      const url=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));
      const a=document.createElement('a');a.href=url;a.download='dealix-intake-draft.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
      root.querySelector('.status').textContent=copy[this.lang].saved;
    }
  }
  customElements.define(tag,Workspace);
})();
